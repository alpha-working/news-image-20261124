"""Build entry.png (1024x1024) for news-image-20261124.
Deterministic: fixed date, fixed text, no network, no random.
Run: python3 build_image.py  -> writes ../entry.png
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1024, 1024
PAPER = (247, 242, 232)
INK = (17, 17, 17)
MUTED = (90, 84, 74)
RED = (180, 35, 24)
BLUE = (27, 79, 114)
TEAL = (14, 116, 109)
GREEN = (22, 101, 52)
GOLD = (146, 96, 0)
CARD = (255, 255, 255)
LINE = (210, 200, 182)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
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

def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# border
d.rectangle([18, 18, W-19, H-19], outline=INK, width=3)
d.rectangle([24, 24, W-25, H-25], outline=LINE, width=1)

# masthead
d.text((512, 38), "THE DAY IN ONE IMAGE", font=font(SERIF_B, 52), fill=INK, anchor="ma")
d.text((512, 102), "TUESDAY  •  24 NOVEMBER 2026  •  WORLD NEWS", font=font(SANS_B, 19), fill=RED, anchor="ma")
d.line([(48, 138), (976, 138)], fill=RED, width=4)

def panel(x, y, w, h, kicker, kcolor, headline, sub, accent):
    d.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([x, y, x+w, y+34], radius=10, fill=kcolor)
    d.rectangle([x, y+20, x+w, y+34], fill=kcolor)
    d.text((x+14, y+7), kicker, font=font(SANS_B, 16), fill=(255, 255, 255))
    yy = draw_lines(d, wrap(d, headline, font(SERIF_B, 30), w-28), x+14, y+48, font(SERIF_B, 30), INK, 36)
    draw_lines(d, wrap(d, sub, font(SANS, 18), w-28), x+14, yy+6, font(SANS, 18), MUTED, 24)
    d.line([(x+14, y+h-14), (x+w-14, y+h-14)], fill=accent, width=4)

# lead row
panel(36, 156, 466, 272, "TECH  •  MARKETS", GREEN,
      "Nvidia brings back Huang",
      "Shares jump 31% in a day. S&P 500 +4.73% after Trump pressure.", GREEN)

panel(522, 156, 466, 272, "CONFLICT  •  LIBYA", BLUE,
      "Ukraine sinks Russian warship off Libya",
      "Seven naval drones hit the corvette Merkury at Benghazi. UN calls for a probe.", BLUE)

# visuals in the empty strip at the bottom of the lead panels (below the text)
# Nvidia: rising chart, +31% label
d.line([(60, 405), (130, 395), (200, 400), (270, 375), (340, 380), (410, 350), (470, 335)], fill=GREEN, width=5, joint="curve")
for (px, py) in [(60, 405), (200, 400), (340, 380), (470, 335)]:
    d.ellipse([px-5, py-5, px+5, py+5], fill=GREEN)
d.text((60, 342), "+31% in a day", font=font(SANS_B, 18), fill=GREEN, anchor="la")
# Libya: ship silhouette on waves
d.rectangle([618, 348, 642, 382], fill=BLUE)
d.polygon([(560, 382), (700, 382), (672, 406), (588, 406)], fill=BLUE)

# second row
panel(36, 448, 466, 196, "GAZA", RED,
      "Israeli strikes kill Hamas security chief in Gaza",
      "Naeem Abu Nahel among 7 killed. A UNRWA worker was killed a day earlier.", RED)
panel(522, 448, 466, 196, "IRAN  •  GULF", TEAL,
      "US blockade, Hormuz mines",
      "Iran vows to confront the blockade. Three tankers hit mines in Hormuz.", TEAL)

# small cards 3 x 2
cards = [
    ("ROHINGYA  •  ICJ", "14 nations back genocide ruling", "UK sanctions five Myanmar generals after the court ruling.", RED),
    ("NATO  •  SPACE", "NATO vows to defend space", "Reports say Russia may put a nuclear weapon in orbit.", BLUE),
    ("AI", "UN wants global AI rules in a year", "US states sue over Grok images; Korea pays to catch AI cheating.", (90, 40, 140)),
    ("CLIMATE  •  COP31", "Climate summit ends with no deal", "Talks fail after a split over fossil fuels and finance.", GREEN),
    ("INDONESIA", "Factory fire in Banten kills 26", "Dozens missing after a fire at a factory in Banten.", GOLD),
    ("WORLD", "Nepal quake; Pakistan astronaut", "5.6 quake near China. Zeeshan Ali to join China's Tiangong station.", TEAL),
]
cw, ch, gap = 304, 138, 16
for i, (kick, head, sub, col) in enumerate(cards):
    x = 36 + (i % 3) * (cw + gap)
    y = 664 + (i // 3) * (ch + gap)
    d.rounded_rectangle([x, y, x+cw, y+ch], radius=8, fill=CARD, outline=LINE, width=2)
    d.text((x+12, y+10), kick, font=font(SANS_B, 13), fill=col)
    yy = draw_lines(d, wrap(d, head, font(SERIF_B, 19), cw-24), x+12, y+34, font(SERIF_B, 19), INK, 23)
    draw_lines(d, wrap(d, sub, font(SANS, 14), cw-24), x+12, yy+4, font(SANS, 14), MUTED, 18)
    d.line([(x+12, y+ch-12), (x+cw-12, y+ch-12)], fill=col, width=3)

# footer
d.line([(48, 968), (976, 968)], fill=LINE, width=2)
d.text((512, 980), "24 NOVEMBER 2026  —  NVIDIA  •  UKRAINE  •  GAZA  •  IRAN  •  ROHINGYA  •  AI  •  CLIMATE", font=font(SANS_B, 14), fill=MUTED, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
