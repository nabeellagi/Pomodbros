class FallPhysics:
    """Simple vertical gravity simulation for a dropped pet."""

    def __init__(self, gravity: float, fall_speed_max: float):
        self.gravity = gravity
        self.fall_speed_max = fall_speed_max
        self.velocity_y = 0.0
        self.active = False

    def start_fall(self):
        self.velocity_y = 0.0
        self.active = True

    def stop(self):
        self.active = False
        self.velocity_y = 0.0

    def step(self, dt: float, current_y: float, ground_y: float) -> tuple[float, bool]:
        """Advance one physics tick. Returns (new_y, landed)."""
        if not self.active:
            return current_y, False

        self.velocity_y += self.gravity * dt
        self.velocity_y = min(self.velocity_y, self.fall_speed_max)

        new_y = current_y + self.velocity_y * dt
        if new_y >= ground_y:
            self.stop()
            return ground_y, True

        return new_y, False
    
class ProjectilePhysics:

    def __init__(self, gravity: float, fall_speed_max: float, horizontal_friction: float):
        self.gravity = gravity
        self.fall_speed_max = fall_speed_max
        self.horizontal_friction = horizontal_friction

        self.vx = 0.0
        self.vy = 0.0
        self.active = False
        self.past_apex = False

    def launch(self, vx: float, vy: float):
        self.vx = vx
        self.vy = vy
        self.active = True
        self.past_apex = vy >= 0

    def stop(self):
        self.active = False
        self.vx = 0.0
        self.vy = 0.0
        self.past_apex = False

    def step(self, dt: float, x: float, y: float, ground_y: float,
              min_x: float, max_x: float) -> tuple[float, float, bool, bool]:
        """Returns (new_x, new_y, landed, just_passed_apex)."""
        if not self.active:
            return x, y, False, False

        self.vy += self.gravity * dt
        self.vy = min(self.vy, self.fall_speed_max)
        self.vx *= self.horizontal_friction

        just_passed_apex = False
        if not self.past_apex and self.vy >= 0:
            self.past_apex = True
            just_passed_apex = True

        new_x = x + self.vx * dt
        new_y = y + self.vy * dt

        # keep it on-screen horizontally
        if new_x < min_x:
            new_x = min_x
            self.vx = 0
        elif new_x > max_x:
            new_x = max_x
            self.vx = 0

        landed = False
        if new_y >= ground_y:
            new_y = ground_y
            landed = True
            self.stop()

        return new_x, new_y, landed, just_passed_apex