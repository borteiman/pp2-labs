# Mickey's Clock 🕐

An analog clock built with **pygame** that uses Mickey Mouse hand graphics
as clock hands, synced to the system time in real-time.

## Controls

| Hand | Shows |
|------|-------|
| Right hand (pointing finger) | **Minutes** |
| Left hand (open glove) | **Seconds** |

The current **MM:SS** value is also printed as a label at the bottom of the window.

---

## How to run

```bash
pip install pygame
python main.py        # from inside mickeys_clock/
```

Press **Esc** or close the window to quit.

---

## Project structure

```
mickeys_clock/
├── main.py            <- entry point: event loop, asset loading
├── clock.py           <- MickeyClock class (rotation maths + rendering)
├── images/
│   ├── clock.png           <- dial / face  (no hands)
│   ├── hand_left.png       <- original left-hand  sprite
│   ├── hand_left_rgba.png  <- pre-processed: transparent background
│   ├── hand_right.png      <- original right-hand sprite
│   ├── hand_right_rgba.png <- pre-processed: transparent background
│   ├── mUmrP.png           <- original Mickey body
│   └── mUmrP_rgba.png      <- pre-processed: transparent background
└── README.md
```

---

## Rotation maths — explained

Each hand image has the glove at the TOP and the stick pivot at the BOTTOM.
Unrotated = hand points at 12 o'clock.

To rotate N degrees clockwise while keeping the pivot fixed at the clock
centre (see clock.py -> _rotate_hand):

```python
# 1. Vector from image-centre to pivot (pygame y-down coordinates)
offset_to_pivot = Vector2(0, hand_height * (PIVOT_Y_RATIO - 0.5))

# 2. Rotate surface clockwise
#    pygame.transform.rotate is CCW-positive -> negate for clockwise
rotated_surface = pygame.transform.rotate(original_surface, -N)

# 3. Rotate the offset vector by the same clockwise amount
#    Vector2.rotate is CW-positive in pygame's y-down space -> use +N
rotated_offset = offset_to_pivot.rotate(N)

# 4. Place rotated image so its pivot lands exactly on clock_centre
draw_centre = clock_centre - rotated_offset
rect = rotated_surface.get_rect(center=draw_centre)
screen.blit(rotated_surface, rect)
```

### Angle to time mapping

    360 / 60 = 6 degrees per minute or second

    minute_angle = now.minute * 6   (0 min = 0 deg = 12 o'clock)
    second_angle = now.second * 6   (15 sec = 90 deg = 3 o'clock)

---

## Image pre-processing

The original PNGs have a solid black background. A flood-fill seeds from
all four corners and makes connected black pixels fully transparent (alpha=0),
preserving internal black outlines. Results saved as *_rgba.png and loaded
with convert_alpha() in pygame.
