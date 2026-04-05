"""
clock.py
--------
MickeyClock: renders the clock face, Mickey's body, and both rotating hands.

Rotation maths
--------------
Each hand image has the glove at the TOP and the stick pivot at the BOTTOM.
Unrotated → hand points at 12 o'clock.

To rotate a hand N degrees clockwise while keeping its pivot fixed at the
clock centre we use:

    offset_to_pivot  = Vector2(0, h * (PIVOT_Y_RATIO - 0.5))   # image-space
    rotated_surface  = pygame.transform.rotate(original, -N)    # cw = negative
    rotated_offset   = offset_to_pivot.rotate(N)                # cw = positive
    draw_centre      = clock_centre - rotated_offset
    rect             = rotated_surface.get_rect(centre=draw_centre)

Why .rotate(+N) for the vector when pygame.transform.rotate uses -N?
In pygame's y-down coordinate system, Vector2.rotate(+angle) is visually
clockwise, while pygame.transform.rotate(surface, +angle) is counter-clockwise.
So we negate for the surface and keep positive for the vector.
"""

import datetime
import pygame

# ── tuneable constants ──────────────────────────────────────────────────────

# Fraction of hand height where the stick base (pivot) sits.
# Measured from the TOP of the image.  0.92 ≈ "near the very bottom".
PIVOT_Y_RATIO = 0.92

# Sizes relative to the clock-face diameter
FACE_SCALE   = 0.90   # clock face  vs window short side
MICKEY_SCALE = 0.50   # Mickey body vs clock face diameter
HAND_SCALE   = 0.44   # hand height vs clock face diameter

# Colorkey used during pre-processing (flood-filled background)
# ───────────────────────────────────────────────────────────────────────────


def _scale_keep_ratio(surf: pygame.Surface, target_h: int) -> pygame.Surface:
    orig_w, orig_h = surf.get_size()
    target_w = int(orig_w * target_h / orig_h)
    return pygame.transform.smoothscale(surf, (target_w, target_h))


class MickeyClock:
    """
    Renders a Mickey-Mouse-themed analog clock.

    Parameters
    ----------
    screen      : pygame display surface
    clock_face  : clock-dial image  (cream background, no hands)
    mickey_body : Mickey body image (magenta-keyed background)
    left_hand   : left  glove image (magenta-keyed) → SECONDS hand
    right_hand  : right glove image (magenta-keyed) → MINUTES hand
    """

    def __init__(
        self,
        screen: pygame.Surface,
        clock_face: pygame.Surface,
        mickey_body: pygame.Surface,
        left_hand: pygame.Surface,
        right_hand: pygame.Surface,
    ):
        self.screen = screen
        sw, sh = screen.get_size()
        self.centre = pygame.math.Vector2(sw // 2, sh // 2)

        # ── scale assets ───────────────────────────────────────────────────
        face_px = int(min(sw, sh) * FACE_SCALE)
        # Preserve the clock-face aspect ratio so the dial stays circular
        cfw, cfh = clock_face.get_size()
        cf_ratio = min(face_px / cfw, face_px / cfh)
        self.clock_face = pygame.transform.smoothscale(
            clock_face, (int(cfw * cf_ratio), int(cfh * cf_ratio))
        )

        mickey_px = int(face_px * MICKEY_SCALE)
        self.mickey_body = pygame.transform.smoothscale(
            mickey_body, (mickey_px, mickey_px)
        )

        hand_h = int(face_px * HAND_SCALE)
        self.left_hand  = _scale_keep_ratio(left_hand,  hand_h)   # seconds
        self.right_hand = _scale_keep_ratio(right_hand, hand_h)   # minutes

        # ── UI font ────────────────────────────────────────────────────────
        self.font = pygame.font.SysFont("Arial", 42, bold=True)

    # ── private helpers ────────────────────────────────────────────────────

    def _rotate_hand(
        self, image: pygame.Surface, angle_deg: float
    ) -> tuple[pygame.Surface, pygame.Rect]:
        """
        Return (rotated_surface, dest_rect) so that the pivot (base of stick)
        sits exactly at self.centre.

        angle_deg : clockwise degrees from 12-o'clock (0 = up).
        """
        w, h = image.get_size()

        # Offset from image centre → pivot  (in pygame's y-down coords)
        offset_to_pivot = pygame.math.Vector2(0.0, h * (PIVOT_Y_RATIO - 0.5))

        # Rotate surface clockwise  (pygame: positive angle = CCW, so negate)
        rotated = pygame.transform.rotate(image, -angle_deg)

        # Rotate offset vector clockwise  (Vector2: positive = CW in y-down)
        rotated_offset = offset_to_pivot.rotate(angle_deg)

        # Draw centre keeps pivot fixed at clock centre
        draw_centre = self.centre - rotated_offset

        rect = rotated.get_rect(
            center=(int(draw_centre.x), int(draw_centre.y))
        )
        return rotated, rect

    @staticmethod
    def _time_to_angles() -> tuple[float, float]:
        """Return (minute_angle_deg, second_angle_deg) for the current time."""
        now = datetime.datetime.now()
        # 360° / 60 units = 6° per unit
        return now.minute * 6.0, now.second * 6.0

    # ── public API ─────────────────────────────────────────────────────────

    def draw(self) -> None:
        """Draw one frame: face → hands → Mickey body → time label."""
        minute_angle, second_angle = self._time_to_angles()
        cx, cy = int(self.centre.x), int(self.centre.y)

        # 1. Clock face (background dial)
        face_rect = self.clock_face.get_rect(center=(cx, cy))
        self.screen.blit(self.clock_face, face_rect)

        # 2. Right hand = MINUTES (drawn first → behind seconds)
        rh_surf, rh_rect = self._rotate_hand(self.right_hand, minute_angle)
        self.screen.blit(rh_surf, rh_rect)

        # 3. Left hand = SECONDS (on top of minutes)
        lh_surf, lh_rect = self._rotate_hand(self.left_hand, second_angle)
        self.screen.blit(lh_surf, lh_rect)

        # 4. Mickey body (covers the hub / pivot area)
        mk_rect = self.mickey_body.get_rect(center=(cx, cy))
        self.screen.blit(self.mickey_body, mk_rect)

        # 5. Numeric time label at bottom of screen
        now = datetime.datetime.now()
        label = self.font.render(now.strftime("%M:%S"), True, (255, 255, 255))
        label_rect = label.get_rect(
            center=(cx, self.screen.get_height() - 28)
        )
        self.screen.blit(label, label_rect)
