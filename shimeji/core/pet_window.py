import sys
import time
import random
import subprocess
from pathlib import Path
from collections import deque

from PySide6.QtCore import Qt, QTimer, QPoint, QRect
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtWidgets import QWidget, QLabel, QApplication, QMenu

from .character import Character
from .physics import ProjectilePhysics
from .behavior import WalkBehavior, WalkFrame, IdleScheduler

TICK_MS = 16  # ~60fps

WALK_FRAME_TO_STATE = {
    WalkFrame.WALK_0: "walk_0",
    WalkFrame.WALK_1: "walk_1",
}


class PetWindow(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character = character

        self._setup_window_flags()

        self.sprite_label = QLabel(self)
        self.sprite_label.setScaledContents(False)
        self.sprite_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self._dragging = False
        self._drag_offset = QPoint()
        self._drag_history: deque[tuple[float, QPoint]] = deque(maxlen=6)
        
        self._pos_x = 0.0
        self._pos_y = 0.0

        self.physics = ProjectilePhysics(
            character.physics.gravity,
            character.physics.fall_speed_max,
            character.physics.horizontal_friction,
        )
        self._hop_velocity = character.physics.hop_velocity
        self._bounce_velocity = character.physics.bounce_velocity
        self._throw_multiplier = character.physics.throw_multiplier

        # "idle"   -> standing still, eligible to start walking
        # "drag"   -> being held
        # "thrown" -> airborne after release, falls until it hits ground
        # "bounce" -> post-land recoil hop
        # "walk"   -> mid walk-cycle
        self._motion_phase = "idle"

        self._walk = WalkBehavior(
            character.behavior.walk_speed,
            character.behavior.walk_frame_duration,
            character.behavior.walk_min_cycles,
            character.behavior.walk_max_cycles,
        )
        self._idle_scheduler = IdleScheduler(
            character.behavior.idle_min_wait,
            character.behavior.idle_max_wait,
            character.behavior.walk_chance,
        )

        self.set_state("normal")

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)
        self._timer.start(TICK_MS)

        self._spawn_at_top_center()

    # ---------- window setup ----------

    def _setup_window_flags(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

    def _spawn_at_top_center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        w = self.width()
        self._set_position(screen.center().x() - w // 2, screen.top())
        self._motion_phase = "thrown"
        self.set_state("fall")
        self.physics.launch(vx=0.0, vy=0.0)

    # ---------- sprite / state ----------

    def set_state(self, state_name: str, mirrored: bool = False):
        pixmap: QPixmap = self.character.states[state_name]
        w, h = self.character.scaled_size(state_name)

        scaled = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if mirrored:
            scaled = scaled.transformed(QTransform().scale(-1, 1))

        self.resize(w, h)
        self.sprite_label.setPixmap(scaled)
        self.sprite_label.setGeometry(0, 0, w, h)
        self.setMask(scaled.mask())

    def _is_drag_hit(self, pos: QPoint) -> bool:
        if self.character.hitbox_mode == "full_sprite":
            return True
        hb = self.character.hitbox
        return QRect(hb.x, hb.y, hb.width, hb.height).contains(pos)

    # ---------- input ----------

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton or not self._is_drag_hit(event.position().toPoint()):
            return

        # Rule #2: dragging mid-walk cancels the walk immediately.
        if self._motion_phase == "walk":
            self._walk.cancel()

        self._motion_phase = "drag"
        self._dragging = True
        self.physics.stop()
        self._drag_offset = event.globalPosition().toPoint() - self.pos()
        self._drag_history.clear()
        self._drag_history.append((time.monotonic(), event.globalPosition().toPoint()))
        self.set_state("drag")

    def mouseMoveEvent(self, event):
        if self._dragging:
            new_pos = event.globalPosition().toPoint() - self._drag_offset
            self._set_position(new_pos.x(), new_pos.y())
            self._drag_history.append((time.monotonic(), event.globalPosition().toPoint()))

    def mouseReleaseEvent(self, event):
        if not self._dragging:
            return
        self._dragging = False

        vx, vy = self._compute_flick_velocity()
        launch_vx = vx * self._throw_multiplier
        launch_vy = (-self._hop_velocity) + (vy * self._throw_multiplier)

        self._motion_phase = "thrown"
        self.set_state("fall")
        self.physics.launch(launch_vx, launch_vy)

    def _compute_flick_velocity(self) -> tuple[float, float]:
        if len(self._drag_history) < 2:
            return 0.0, 0.0
        t_end, p_end = self._drag_history[-1]
        t_start, p_start = self._drag_history[max(0, len(self._drag_history) - 4)]
        dt = t_end - t_start
        if dt <= 0:
            return 0.0, 0.0
        return (p_end.x() - p_start.x()) / dt, (p_end.y() - p_start.y()) / dt

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        destroy_action = menu.addAction("Destroy em")
        spawn_action = menu.addAction("Add one more")
        chosen = menu.exec(event.globalPos())
        if chosen == destroy_action:
            self._destroy()
        elif chosen == spawn_action:
            self._spawn_sibling()

    def _destroy(self):
        self._timer.stop()
        self.close()
        QApplication.instance().quit()

    def _spawn_sibling(self):
        if getattr(sys, "frozen", False):
            args = [sys.executable, f"--chara={self.character.name}"]
        else:
            script = Path(__file__).resolve().parent.parent / "main.py"
            args = [sys.executable, str(script), f"--chara={self.character.name}"]
        subprocess.Popen(args)

    # ---------- idle / walk scheduling ----------

    def _schedule_next_idle_decision(self):
        QTimer.singleShot(self._idle_scheduler.next_delay_ms(), self._maybe_start_walk)

    def _maybe_start_walk(self):
        # Rule #1: only ever start a walk from a clean idle state —
        # if something else happened meanwhile (grabbed, thrown), just drop this decision.
        if self._motion_phase != "idle":
            return

        if self._idle_scheduler.should_walk():
            self._motion_phase = "walk"
            self._walk.start()
            self._apply_walk_frame(self._walk.current_frame)
        else:
            self._schedule_next_idle_decision()

    def _apply_walk_frame(self, frame: WalkFrame):
        mirrored = self._walk.direction == 1  # right = mirrored
        self.set_state(WALK_FRAME_TO_STATE[frame], mirrored=mirrored)

    def _enter_idle(self):
        self._motion_phase = "idle"
        self.set_state("normal")
        self._schedule_next_idle_decision()

    # ---------- physics / walk tick ----------
    
    
    def _set_position(self, x: float, y: float):
        self._pos_x = x
        self._pos_y = y
        self.move(round(x), round(y))

    def _screen_bounds(self):
        screen = QApplication.screenAt(self.pos()) or QApplication.primaryScreen()
        available = screen.availableGeometry()
        ground_y = available.bottom() - self.height() + 1
        min_x = available.left()
        max_x = available.right() - self.width() + 1
        return ground_y, min_x, max_x

    def _on_tick(self):
        if self._dragging:
            return

        dt = TICK_MS / 1000.0

        if self._motion_phase in ("thrown", "bounce"):
            self._tick_physics(dt)
        elif self._motion_phase == "walk":
            self._tick_walk(dt)
        # "idle" -> nothing to do each tick, the scheduler runs on its own timer

    def _tick_physics(self, dt: float):
        if not self.physics.active:
            return

        ground_y, min_x, max_x = self._screen_bounds()
        new_x, new_y, landed, just_passed_apex = self.physics.step(
            dt, self._pos_x, self._pos_y, ground_y, min_x, max_x
        )
        self._set_position(new_x, new_y)

        if self._motion_phase == "thrown":
            if landed:
                self._motion_phase = "bounce"
                self.set_state("fall")
                self.physics.launch(vx=0.0, vy=-self._bounce_velocity)

        elif self._motion_phase == "bounce":
            if just_passed_apex:
                self.set_state("normal")
            if landed:
                self.physics.stop()
                self._enter_idle()

    def _tick_walk(self, dt: float):
        frame, dx, finished = self._walk.update(dt)

        if dx != 0.0:
            _, min_x, max_x = self._screen_bounds()
            new_x = max(min_x, min(max_x, self._pos_x + dx))
            self._set_position(new_x, self._pos_y)

        self._apply_walk_frame(frame)

        if finished:
            self._enter_idle()