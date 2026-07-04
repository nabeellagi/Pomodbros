from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtGui import QPixmap


@dataclass
class Hitbox:
    x: int
    y: int
    width: int
    height: int

@dataclass
class Physics:
    gravity: float
    fall_speed_max: float
    hop_velocity: float
    bounce_velocity: float
    throw_multiplier: float
    horizontal_friction: float
    
@dataclass
class Behavior:
    walk_speed: float
    walk_frame_duration: float
    walk_min_cycles: int
    walk_max_cycles: int
    walk_chance: float
    idle_min_wait: float
    idle_max_wait: float



class Character:
    """Loads a character folder: config.json + its sprite states."""

    def __init__(self, name: str, folder: Path, config: dict):
        self.name = name
        self.folder = folder
        self.display_name = config.get("display_name", name)
        self.scale = float(config.get("scale", 1.0))

        self.hitbox_mode = config.get("hitbox_mode", "custom" if "hitbox" in config else "full_sprite")
        self.hitbox = None
        if self.hitbox_mode == "custom":
            hb = config["hitbox"]
            self.hitbox = Hitbox(hb["x"], hb["y"], hb["width"], hb["height"])

        ph = config.get("physics", {})
        self.physics = Physics(
            gravity=float(ph.get("gravity", 500)),
            fall_speed_max=float(ph.get("fall_speed_max", 450)),
            hop_velocity=float(ph.get("hop_velocity", 120)),
            bounce_velocity=float(ph.get("bounce_velocity", 90)),
            throw_multiplier=float(ph.get("throw_multiplier", 0.35)),
            horizontal_friction=float(ph.get("horizontal_friction", 0.96)),
        )
        
        bh = config.get("behavior", {})
        self.behavior = Behavior(
            walk_speed=float(bh.get("walk_speed", 40)),
            walk_frame_duration=float(bh.get("walk_frame_duration", 0.35)),
            walk_min_cycles=int(bh.get("walk_min_cycles", 2)),
            walk_max_cycles=int(bh.get("walk_max_cycles", 4)),
            walk_chance=float(bh.get("walk_chance", 0.5)),
            idle_min_wait=float(bh.get("idle_min_wait", 1.5)),
            idle_max_wait=float(bh.get("idle_max_wait", 4.0)),
        )

        self.states: dict[str, QPixmap] = {}
        for state_name, filename in config["states"].items():
            path = folder / filename
            if not path.exists():
                raise FileNotFoundError(f"Sprite for state '{state_name}' not found: {path}")
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                raise ValueError(f"Failed to load sprite: {path}")
            self.states[state_name] = pixmap

    @classmethod
    def load(cls, name: str, characters_root: Path) -> "Character":
        folder = characters_root / name
        config_path = folder / "config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Character '{name}' not found at {folder}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        return cls(name, folder, config)

    def scaled_size(self, state: str = "normal"):
        """Master sprite stays high-res; we only ever scale DOWN for display."""
        pixmap = self.states[state]
        return int(pixmap.width() * self.scale), int(pixmap.height() * self.scale)