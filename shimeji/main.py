"""
Transparent, SELF-MOVING window in Pyglet ("Option B").

This is the architecture real desktop pets use: the window is small
(just big enough for one sprite), fully transparent except the sprite
itself, and it's the WINDOW'S OWN SCREEN POSITION that changes every
frame — not a sprite moving around inside a fixed canvas. That makes
"am I over the taskbar / touching the edge of another app" a simple
comparison between this window's rect and the rest of the screen,
which is most of what makes a desktop pet feel like it's really there.

KEY FIX vs the original snippet:
glClearColor(0,0,0,0) only controls the OpenGL framebuffer's alpha.
It does NOT make the OS window transparent. Desktop window transparency
is a platform/window-manager feature and needs platform-specific calls.
See the platform_transparency() block below — set it up ONCE after
window creation, before pyglet.app.run().

Movement is added via pyglet.clock.schedule_interval, which is Pyglet's
proper game-loop hook (don't try to animate inside on_draw itself).
"""
import sys
import pyglet
from pyglet.gl import *

# Small window — just enough room for one pet, not the whole screen.
PET_SIZE = 100
WIDTH, HEIGHT = PET_SIZE, PET_SIZE

# If True, mouse clicks pass straight through the pet to whatever's
# underneath (Windows only, see platform_transparency()). Set False if
# you want to eventually support click-dragging the pet around.
CLICK_THROUGH = True

window = pyglet.window.Window(
    width=WIDTH, height=HEIGHT,
    style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
)

# Always on top — relevant for a desktop-pet use case
window.set_always_on_top = True  # no-op placeholder; see platform notes below

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# --- Screen bounds the pet is allowed to wander in ---
display = pyglet.canvas.get_display()
screen = display.get_default_screen()
SCREEN_W, SCREEN_H = screen.width, screen.height

# --- Pet state, in SCREEN coordinates now, not window-local ---
pos = [200.0, 200.0]          # window's top-left-ish position on the screen
velocity = [120.0, 90.0]      # pixels per second
window.set_location(int(pos[0]), int(pos[1]))

# Sprite is drawn at a fixed spot WITHIN the window (centered), since the
# window itself is what moves now.
shape = pyglet.shapes.Rectangle(
    x=10, y=10, width=PET_SIZE - 20, height=PET_SIZE - 20,
    color=(255, 0, 0),
)
shape.opacity = 220


def update(dt):
    """Move the WINDOW across real screen coordinates, bounce off screen edges."""
    pos[0] += velocity[0] * dt
    pos[1] += velocity[1] * dt

    if pos[0] <= 0 or pos[0] + WIDTH >= SCREEN_W:
        velocity[0] *= -1
        pos[0] = max(0, min(pos[0], SCREEN_W - WIDTH))
    if pos[1] <= 0 or pos[1] + HEIGHT >= SCREEN_H:
        velocity[1] *= -1
        pos[1] = max(0, min(pos[1], SCREEN_H - HEIGHT))

    # This is the part that's actually different from Option A:
    # we reposition the OS window every tick instead of moving a shape.
    window.set_location(int(pos[0]), int(pos[1]))


pyglet.clock.schedule_interval(update, 1 / 60.0)


@window.event
def on_draw():
    glClearColor(0, 0, 0, 0)
    window.clear()
    shape.draw()


def platform_transparency():
    """
    OS-level call to actually make the window background see-through.
    Pyglet does not provide this cross-platform — you call into the
    native windowing API yourself. This is the piece the original
    snippet was missing entirely.
    """
    if sys.platform == "win32":
        # Windows: use ctypes to set WS_EX_LAYERED + a transparent color key,
        # or LWA_ALPHA for per-pixel alpha with DWM composition.
        import ctypes
        from ctypes import wintypes

        hwnd = window._hwnd  # pyglet's internal win32 handle
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020  # clicks pass through to whatever's underneath
        LWA_COLORKEY = 0x00000001
        LWA_ALPHA = 0x00000002

        user32 = ctypes.windll.user32
        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        extra = WS_EX_TRANSPARENT if CLICK_THROUGH else 0
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | extra)
        # Note: with WS_EX_TRANSPARENT set, you can't click-drag the pet anymore —
        # clicks fall straight through to the window/desktop behind it. If you
        # want "click to pick up and drag" behavior later, you'd toggle this
        # flag off while the mouse is over the pet (needs a small hit-test loop,
        # since the OS won't even tell you about the hover once transparent).

        # Color-key approach: any pixel matching this RGB becomes fully transparent.
        # Simple, but means you can't use that exact color in your sprite.
        # (0,0,0) chosen here — your clear color above should match this key.
        colorkey = 0x000000  # 0x00BBGGRR format
        user32.SetLayeredWindowAttributes(hwnd, colorkey, 255, LWA_COLORKEY)

        # For true per-pixel alpha (sprite edges anti-aliased against desktop),
        # you'd instead use UpdateLayeredWindow with a DIB section — more setup,
        # but no color-key artifacts. Worth it once you have real sprite art.

    elif sys.platform == "darwin":
        # macOS: pyglet's Cocoa backend doesn't expose this directly either.
        # You'd typically need pyobjc to reach into NSWindow:
        #   window._nswindow.setOpaque_(False)
        #   window._nswindow.setBackgroundColor_(NSColor.clearColor())
        # This requires `pip install pyobjc-framework-Cocoa` and digging into
        # pyglet's private _nswindow attribute (version-dependent, fragile).
        print("macOS transparency requires pyobjc + NSWindow access — "
              "see comments in platform_transparency().")

    else:
        # Linux/X11: depends on compositor (picom, KWin, Mutter etc. must be
        # running and support ARGB visuals). Commonly done by requesting an
        # ARGB visual at window-creation time via raw Xlib, which is awkward
        # to retrofit onto an already-created pyglet window. Some people
        # instead use GLX_EXT_buffer_age + composited WMs, or just accept
        # color-keying via the WM as a simpler fallback.
        print("Linux transparency depends on your compositor (picom/KWin/Mutter) "
              "supporting ARGB visuals — see comments in platform_transparency().")


if __name__ == "__main__":
    platform_transparency()
    pyglet.app.run()