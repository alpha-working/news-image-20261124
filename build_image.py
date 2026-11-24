"""Build entry.png v5 (1024x1024) for news-image-20261124.
35 stories, kept legible in 3 tiers:
  4 main panels (visual band + headline + sub)
  8 cards (kicker + headline + 1-line sub)
  23 one-line stories in ALSO TODAY strip, 3 columns, 14pt
Deterministic: fixed date, fixed text, no network, no random.
"""
from PIL import Image, ImageDraw, ImageFont
import os

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
DARK_GREEN = (18, 77, 43)
DARK_BLUE = (11, 61, 92)
DARK_RED = (124, 29, 29)
DARK_TEAL = (13, 84, 82)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

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

def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([18, 18, W-19, H-19], outline=INK, width=3)
d.rectangle([24, 24, W-25, H-25], outline=LINE, width=1)
d.text((512, 38), "THE DAY IN ONE IMAGE  —  35 STORIES", font=font(SERIF_B, 36), fill=INK, anchor="ma")
d.text((512, 102), "TUESDAY  •  24 NOVEMBER 2026  •  WORLD NEWS", font=font(SANS_B, 19), fill=RED, anchor="ma")
d.line([(48, 138), (976, 138)], fill=RED, width=4)

def panel_visual(x, y, w, h, band_h, bg, kicker, headline, sub, accent, draw_visual, hs=24, hl=29, ss=13, sl=18):
    d.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([x, y, x+w, y+band_h], radius=10, fill=bg)
    d.rectangle([x, y+band_h-12, x+w, y+band_h], fill=bg)
    draw_visual(x, y, w, band_h)
    d.text((x+14, y+8), kicker, font=font(SANS_B, 14), fill=(255, 255, 255))
    ty = y + band_h + 10
    yy = draw_lines(d, wrap(d, headline, font(SERIF_B, hs), w-28), x+14, ty, font(SERIF_B, hs), INK, hl)
    draw_lines(d, wrap(d, sub, font(SANS, ss), w-28), x+14, yy+4, font(SANS, ss), MUTED, sl)
    d.line([(x+14, y+h-12), (x+w-14, y+h-12)], fill=accent, width=4)

def vis_nvidia(x, y, w, band_h):
    cx, cy = x+95, y+52
    d.rounded_rectangle([cx-42, cy-22, cx+42, cy+22], radius=8, fill=(34, 197, 94), outline=(255, 255, 255), width=3)
    d.rounded_rectangle([cx-20, cy-11, cx+20, cy+11], radius=4, fill=DARK_GREEN, outline=(255, 255, 255), width=2)
    for px in (cx-30, cx-10, cx+10, cx+30):
        d.rectangle([px-3, cy-30, px+3, cy-22], fill=(255, 255, 255))
        d.rectangle([px-3, cy+22, px+3, cy+30], fill=(255, 255, 255))
    pts = [(x+200, y+68), (x+260, y+60), (x+320, y+64), (x+380, y+44), (x+440, y+30)]
    d.line(pts, fill=(255, 255, 255), width=5, joint="curve")
    d.ellipse([x+435, y+25, x+445, y+35], fill=(250, 204, 21))
    d.text((x+w-16, y+band_h-24), "+31%", font=font(SANS_B, 20), fill=(250, 204, 21), anchor="ra")

def vis_ship(x, y, w, band_h):
    d.ellipse([x+w-66, y+12, x+w-34, y+44], fill=(249, 115, 22))
    d.rectangle([x+205, y+24, x+217, y+60], fill=(255, 255, 255))
    d.polygon([(x+140, y+60), (x+330, y+60), (x+302, y+78), (x+168, y+78)], fill=(255, 255, 255))
    d.polygon([(x+217, y+24), (x+252, y+36), (x+217, y+46)], fill=(239, 68, 68))

def vis_gaza(x, y, w, band_h):
    for bx, bh in ((x+30, 18), (x+95, 26), (x+165, 15), (x+235, 23), (x+305, 20), (x+375, 28)):
        d.rectangle([bx, y+band_h-bh, bx+52, y+band_h], fill=(69, 10, 10))
    d.ellipse([x+w-58, y+6, x+w-36, y+28], fill=(253, 224, 71))

def vis_iran(x, y, w, band_h):
    d.polygon([(x+150, y+22), (x+330, y+22), (x+310, y+38), (x+170, y+38)], fill=(255, 255, 255))
    d.rectangle([x+225, y+10, x+255, y+22], fill=(255, 255, 255))

# 4 main stories
panel_visual(36, 156, 466, 206, 80, DARK_GREEN, "TECH  •  MARKETS", "Nvidia brings back Huang",
             "Shares jump 31% in a day. S&P 500 +4.73% after Trump pressure.", GREEN, vis_nvidia)
panel_visual(522, 156, 466, 206, 80, DARK_BLUE, "CONFLICT  •  LIBYA", "Ukraine sinks Russian warship off Libya",
             "Seven naval drones hit the corvette Merkury at Benghazi. UN calls for a probe.", BLUE, vis_ship)
panel_visual(36, 376, 466, 156, 40, DARK_RED, "GAZA", "Israeli strikes kill Hamas security chief in Gaza",
             "Naeem Abu Nahel among 7 killed. A UNRWA worker was killed a day earlier.", RED, vis_gaza, hs=21, hl=26, ss=13, sl=17)
panel_visual(522, 376, 466, 156, 40, DARK_TEAL, "IRAN  •  GULF", "US blockade, Hormuz mines",
             "Iran vows to confront the blockade. Three tankers hit mines in Hormuz.", TEAL, vis_iran, hs=21, hl=26, ss=13, sl=17)

# 8 cards, 4 x 2
cards = [
    ("ROHINGYA  •  ICJ", "14 nations back genocide ruling", "UK sanctions 5 Myanmar generals.", RED, "§"),
    ("NATO  •  SPACE", "NATO vows to defend space", "Russia may put a nuke in orbit.", BLUE, "★"),
    ("AI", "UN wants global AI rules in a year", "US states sue over Grok images.", (90, 40, 140), "AI"),
    ("CLIMATE  •  COP31", "Climate summit ends with no deal", "90+ nations rejected the draft.", GREEN, "◉"),
    ("INDONESIA", "Factory fire in Banten kills 26", "Dozens missing after the fire.", GOLD, "!"),
    ("NEPAL", "Nepal quake, 5.6 near China", "Tremor near the China border.", TEAL, "✦"),
    ("SPACE", "Pakistan astronaut for Tiangong", "Zeeshan Ali to fly Tiangong.", TEAL, "✦"),
    ("USA", "Democrats take US House", "Largest margin in decades.", RED, "★"),
]
cw, ch, gap = 229, 118, 12
for i, (kick, head, sub, col, mark) in enumerate(cards):
    x = 36 + (i % 4) * (cw + gap)
    y = 548 + (i // 4) * (ch + gap)
    d.rounded_rectangle([x, y, x+cw, y+ch], radius=8, fill=CARD, outline=LINE, width=2)
    d.ellipse([x+cw-34, y+8, x+cw-12, y+30], fill=col)
    d.text((x+cw-23, y+9), mark, font=font(SANS_B, 12), fill=(255, 255, 255), anchor="ma")
    d.text((x+10, y+8), kick, font=font(SANS_B, 12), fill=col)
    yy = draw_lines(d, wrap(d, head, font(SERIF_B, 16), cw-20), x+10, y+32, font(SERIF_B, 16), INK, 20)
    draw_lines(d, wrap(d, sub, font(SANS, 12), cw-20), x+10, yy+3, font(SANS, 12), MUTED, 16)
    d.line([(x+10, y+ch-8), (x+cw-10, y+ch-8)], fill=col, width=3)

# ALSO TODAY strip: 23 more stories, 3 columns
d.rounded_rectangle([36, 804, 988, 984], radius=10, fill=CARD, outline=LINE, width=2)
d.text((52, 814), "ALSO TODAY  —  23 MORE STORIES", font=font(SANS_B, 14), fill=RED)
also = [
    "Zaporizhzhia hit: 2 killed, 40 hurt",
    "Russian deaths pass 700,000",
    "Russia warns Estonia",
    "Qatar PM meets Vance, Rubio",
    "Libya demands Kyiv explain",
    "Oxfam: Gaza 'toxic land'",
    "UN: Gaza war undone 77 years",
    "UK logs Iranian attacks",
    "Germany gets Delta access",
    "Congo Ebola teams trapped",
    "EU limits Russian visas",
    "Iraq orders oilfields control",
    "US blacklists Megaspeed",
    "Pentagon accuses Canada",
    "Trump death penalty order",
    "US loses measles status",
    "Sanofi buys Insmed $41B",
    "Somalia, Uganda hit Al-Shabaab",
    "Houthis: Saudi strike kills 17",
    "Zelensky urges NATO admission",
    "Spain amnesties Puigdemont",
    "Mexico to try 'El Chapo Isidro'",
    "Car bomb in Villavicencio",
]
cols = [also[0:8], also[8:16], also[16:23]]
for ci, col in enumerate(cols):
    x = 52 + ci * 318
    for r, item in enumerate(col):
        d.text((x, 840 + r * 18), "•  " + item, font=font(SANS, 14), fill=INK)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
