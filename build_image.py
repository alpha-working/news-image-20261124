"""Build entry.png v6 (1024x1024) for news-image-20261124.
35 stories as a numbered 5x7 tile grid. Each story gets its own tile,
headline-only at 16pt serif — no dense 14pt strip, no subtext to shrink.
At full 1024 every tile is legible; the grid itself shows the count.
Deterministic: fixed date, fixed text, no network, no random.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (247, 242, 232)
INK = (17, 17, 17)
CARD = (255, 255, 255)
LINE = (210, 200, 182)
RED = (180, 35, 24)
BLUE = (27, 79, 114)
TEAL = (14, 116, 109)
GREEN = (22, 101, 52)
GOLD = (146, 96, 0)
PURPLE = (90, 40, 140)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([18, 18, W-19, H-19], outline=INK, width=3)
d.rectangle([24, 24, W-25, H-25], outline=LINE, width=1)
d.text((512, 38), "THE DAY IN ONE IMAGE", font=font(SERIF_B, 52), fill=INK, anchor="ma")
d.text((512, 102), "TUESDAY  •  24 NOVEMBER 2026  •  35 STORIES", font=font(SANS_B, 19), fill=RED, anchor="ma")
d.line([(48, 138), (976, 138)], fill=RED, width=4)

stories = [
    ("TECH", GREEN, "Nvidia brings back Huang"),
    ("CONFLICT", BLUE, "Ukraine sinks Russian warship off Libya"),
    ("GAZA", RED, "Gaza strikes kill Hamas chief"),
    ("IRAN", TEAL, "US blockade, Hormuz mines"),
    ("ICJ", RED, "Rohingya genocide ruling backed"),
    ("SPACE", BLUE, "NATO vows to defend space"),
    ("AI", PURPLE, "UN wants global AI rules"),
    ("CLIMATE", GREEN, "COP31 ends with no deal"),
    ("INDONESIA", GOLD, "Banten factory fire kills 26"),
    ("WORLD", TEAL, "Nepal quake, 5.6 near China"),
    ("SPACE", TEAL, "Pakistan astronaut for Tiangong"),
    ("USA", RED, "Democrats take US House"),
    ("WAR", BLUE, "Zaporizhzhia hit: 2 killed"),
    ("WAR", BLUE, "Russian deaths pass 700,000"),
    ("WAR", BLUE, "Russia warns Estonia"),
    ("DIPLOMACY", TEAL, "Qatar PM meets Vance, Rubio"),
    ("LIBYA", BLUE, "Libya demands Kyiv explain"),
    ("GAZA", RED, "Oxfam: Gaza 'toxic land'"),
    ("GAZA", RED, "UN: Gaza war undone 77 years"),
    ("IRAN", TEAL, "UK logs Iranian attacks"),
    ("WAR", BLUE, "Germany gets Delta access"),
    ("AFRICA", GOLD, "Congo Ebola teams trapped"),
    ("EU", BLUE, "EU limits Russian visas"),
    ("IRAQ", GOLD, "Iraq orders oilfields control"),
    ("TECH", GREEN, "US blacklists Megaspeed"),
    ("USA", RED, "Pentagon accuses Canada"),
    ("USA", RED, "Trump death penalty order"),
    ("HEALTH", PURPLE, "US loses measles status"),
    ("BUSINESS", GREEN, "Sanofi buys Insmed $41B"),
    ("AFRICA", GOLD, "Somalia, Uganda hit Al-Shabaab"),
    ("YEMEN", RED, "Houthis: Saudi strike kills 17"),
    ("WAR", BLUE, "Zelensky urges NATO admission"),
    ("EU", BLUE, "Spain amnesties Puigdemont"),
    ("MEXICO", GOLD, "Mexico to try 'El Chapo Isidro'"),
    ("COLOMBIA", GOLD, "Car bomb in Villavicencio"),
]

cw, ch, gx, gy = 184, 112, 8, 8
for i, (tag, col, head) in enumerate(stories):
    x = 36 + (i % 5) * (cw + gx)
    y = 156 + (i // 5) * (ch + gy)
    d.rounded_rectangle([x, y, x+cw, y+ch], radius=8, fill=CARD, outline=LINE, width=2)
    d.line([(x+10, y+6), (x+cw-10, y+6)], fill=col, width=4)
    d.text((x+10, y+14), f"{i+1:02d}", font=font(SANS_B, 13), fill=col)
    d.text((x+cw-10, y+14), tag, font=font(SANS_B, 11), fill=col, anchor="ra")
    yy = y + 36
    for ln in wrap(d, head, font(SERIF_B, 16), cw-20):
        d.text((x+10, yy), ln, font=font(SERIF_B, 16), fill=INK)
        yy += 20

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
