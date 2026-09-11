"""Stamp a name onto every frame of the space-shooter animation.

gh-space-shooter has no text option, so the workflow runs it with
`no-commit`, then this script rewrites the animated WebP with the name in
the top-left corner of each frame, preserving frame timing and looping.
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageSequence

path = sys.argv[1]
text = sys.argv[2]

src = Image.open(path)
try:
    font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 15)
except OSError:
    font = ImageFont.load_default(size=15)

frames, durations = [], []
for frame in ImageSequence.Iterator(src):
    f = frame.convert("RGBA")
    d = ImageDraw.Draw(f)
    x, y = 14, 10
    # Soft dark plate under the text so it reads over stars and bullets.
    w = d.textlength(text, font=font)
    d.rounded_rectangle((x - 8, y - 5, x + w + 8, y + 20), radius=6, fill=(8, 10, 18, 190))
    d.text((x, y), text, font=font, fill=(245, 245, 240, 255))
    frames.append(f.convert("RGB"))
    durations.append(frame.info.get("duration", 25))

frames[0].save(
    path,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    quality=80,
    method=4,
)
print(f"stamped {len(frames)} frames")
