import random
from dataclasses import dataclass
from enum import Enum, auto


class WalkFrame(Enum):
    WALK_0 = auto()
    WALK_1 = auto()


class WalkBehavior:
    """Self-contained walking state machine.

    Sequence shape: walk_0 -> walk_1 -> walk_0 -> walk_1 -> ... -> walk_0
    i.e. (2 * cycles + 1) frames, always starting AND ending on walk_0.
    """

    def __init__(self, walk_speed: float, frame_duration: float,
                 min_cycles: int, max_cycles: int):
        self.walk_speed = walk_speed
        self.frame_duration = frame_duration
        self.min_cycles = min_cycles
        self.max_cycles = max_cycles

        self.active = False
        self.direction = -1  # -1 = left (default sprite), 1 = right (mirrored)!
        self._frame_index = 0
        self._frame_elapsed = 0.0
        self._total_frames = 0

    def start(self):
        cycles = random.randint(self.min_cycles, self.max_cycles)
        self._total_frames = cycles * 2 + 1
        self._frame_index = 0
        self._frame_elapsed = 0.0
        self.direction = random.choice([-1, 1])
        self.active = True

    def cancel(self):
        """Hard stop — used when the pet gets grabbed mid-walk."""
        self.active = False
        self._frame_index = 0
        self._frame_elapsed = 0.0

    @property
    def current_frame(self) -> WalkFrame:
        return WalkFrame.WALK_0 if self._frame_index % 2 == 0 else WalkFrame.WALK_1

    def update(self, dt: float) -> tuple[WalkFrame, float, bool]:
        """Advance the walk by dt. Returns (frame_to_show, dx_this_tick, finished)."""
        if not self.active:
            return WalkFrame.WALK_0, 0.0, False

        dx = self.walk_speed * dt * self.direction if self.current_frame == WalkFrame.WALK_1 else 0.0

        self._frame_elapsed += dt
        finished = False

        if self._frame_elapsed >= self.frame_duration:
            self._frame_elapsed = 0.0
            self._frame_index += 1
            if self._frame_index >= self._total_frames:
                self.active = False
                finished = True

        return self.current_frame, dx, finished


@dataclass
class IdleScheduler:
    """Decides, after a random wait, whether the pet should start walking
    or keep standing."""
    min_wait: float
    max_wait: float
    walk_chance: float

    def next_delay_ms(self) -> int:
        return int(random.uniform(self.min_wait, self.max_wait) * 1000)

    def should_walk(self) -> bool:
        return random.random() < self.walk_chance