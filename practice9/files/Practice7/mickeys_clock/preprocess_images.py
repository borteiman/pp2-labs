"""
preprocess_images.py
--------------------
Run this ONCE to convert the original hand / Mickey images (black background)
into RGBA PNGs with a transparent background.

The flood-fill seeds from all 4 corners so only the outer background black is
made transparent — internal black outlines (glove edges, stick) are preserved.

Usage:
    python preprocess_images.py
"""

import os
import numpy as np
from PIL import Image
from collections import deque


def make_transparent_bg(img_path: str, out_path: str, threshold: int = 15) -> None:
    """
    Flood-fill connected black pixels starting from the 4 corners and
    set their alpha channel to 0 (fully transparent).

    Parameters
    ----------
    img_path  : input image file path
    out_path  : output RGBA PNG file path
    threshold : pixels with R, G, B all below this value are treated as black
    """
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]

    visited = np.zeros((h, w), dtype=bool)
    queue: deque = deque()

    def is_bg(y: int, x: int) -> bool:
        r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
        return r < threshold and g < threshold and b < threshold

    # Seed from all four corners
    for sy, sx in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
        if is_bg(sy, sx) and not visited[sy, sx]:
            queue.append((sy, sx))
            visited[sy, sx] = True

    # 4-connected flood fill
    while queue:
        y, x = queue.popleft()
        arr[y, x, 3] = 0  # transparent
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and is_bg(ny, nx):
                visited[ny, nx] = True
                queue.append((ny, nx))

    Image.fromarray(arr, "RGBA").save(out_path)
    print(f"  Saved  {out_path}")


if __name__ == "__main__":
    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

    targets = [
        ("hand_left.png",  "hand_left_rgba.png"),
        ("hand_right.png", "hand_right_rgba.png"),
        ("mUmrP.png",      "mUmrP_rgba.png"),
    ]

    print("Pre-processing images …")
    for src, dst in targets:
        make_transparent_bg(
            os.path.join(images_dir, src),
            os.path.join(images_dir, dst),
        )
    print("Done.  All *_rgba.png files are ready.")
