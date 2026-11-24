"""Build entry.png v3.1 (1024x1024) for news-image-20261124.
Deterministic: fixed date, fixed text, no network, no random.
Picture-led front page: visual header band on every story panel,
headline + sub below it, no text ever reaches the accent line.
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
d.text((512, 38), "THE DAY IN ONE IMAGE", font=font(SERIF_B, 52), fill=INK, anchor="ma")
d.text((512, 102), "TUESDAY  •  24 NOVEMBER 2026  •  WORLD NEWS", font=font(SANS_B, 19), fill=RED, anchor="ma")
d.line([(48, 138), (976, 138)], fill=RED, width=4)

def panel_visual(x, y, w, h, band_h, bg, kicker, headline, sub, accent, draw_visual, hs=27, hl=32, ss=16, sl=21):
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
    cx, cy = x+95, y+58
    d.rounded_rectangle([cx-46, cy-24, cx+46, cy+24], radius=8, fill=(34, 197, 94), outline=(255, 255, 255), width=3)
    d.rounded_rectangle([cx-22, cy-12, cx+22, cy+12], radius=4, fill=DARK_GREEN, outline=(255, 255, 255), width=2)
    for px in (cx-34, cx-12, cx+12, cx+34):
        d.rectangle([px-3, cy-33, px+3, cy-24], fill=(255, 255, 255))
        d.rectangle([px-3, cy+24, px+3, cy+33], fill=(255, 255, 255))
    pts = [(x+200, y+82), (x+260, y+72), (x+320, y+76), (x+380, y+54), (x+440, y+38)]
    d.line(pts, fill=(255, 255, 255), width=5, joint="curve")
    d.ellipse([x+435, y+33, x+445, y+43], fill=(250, 204, 21))
    d.text((x+w-16, y+band_h-26), "+31%", font=font(SANS_B, 20), fill=(250, 204, 21), anchor="ra")

def vis_ship(x, y, w, band_h):
    d.ellipse([x+w-66, y+12, x+w-34, y+44], fill=(249, 115, 22))
    d.rectangle([x+205, y+26, x+217, y+66], fill=(255, 255, 255))
    d.polygon([(x+140, y+66), (x+330, y+66), (x+302, y+90), (x+168, y+90)], fill=(255, 255, 255))
    d.polygon([(x+217, y+26), (x+252, y+38), (x+217, y+48)], fill=(239, 68, 68))
    for wx in (x+36, x+356):
        d.arc([wx, y+82, wx+64, y+104], 180, 360, fill=(147, 197, 253), width=4)

def vis_gaza(x, y, w, band_h):
    # buildings along the bottom of a 48px band; sun top-right
    for bx, bh in ((x+30, 22), (x+95, 32), (x+165, 18), (x+235, 28), (x+305, 24), (x+375, 34)):
        d.rectangle([bx, y+band_h-bh, bx+52, y+band_h], fill=(69, 10, 10))
    d.ellipse([x+w-58, y+8, x+w-36, y+30], fill=(253, 224, 71))

def vis_iran(x, y, w, band_h):
    # tanker: tapered hull, bridge tower, no overlap with kicker (kicker is top-left, hull is centred low)
    d.polygon([(x+150, y+28), (x+330, y+28), (x+310, y+44), (x+170, y+44)], fill=(255, 255, 255))
    d.rectangle([x+225, y+14, x+255, y+28], fill=(255, 255, 255))

# lead row h=250, band=100
panel_visual(36, 156, 466, 250, 100, DARK_GREEN, "TECH  •  MARKETS", "Nvidia brings back Huang",
             "Shares jump 31% in a day. S&P 500 +4.73% after Trump pressure.", GREEN, vis_nvidia, hs=29, hl=34, ss=17, sl=22)
panel_visual(522, 156, 466, 250, 100, DARK_BLUE, "CONFLICT  •  LIBYA", "Ukraine sinks Russian warship off Libya",
             "Seven naval drones hit the corvette Merkury at Benghazi. UN calls for a probe.", BLUE, vis_ship, hs=29, hl=34, ss=17, sl=22)
# second row h=180, band=48, smaller type
panel_visual(36, 426, 466, 180, 48, DARK_RED, "GAZA", "Israeli strikes kill Hamas security chief in Gaza",
             "Naeem Abu Nahel among 7 killed. A UNRWA worker was killed a day earlier.", RED, vis_gaza, hs=26, hl=31, ss=15, sl=20)
panel_visual(522, 426, 466, 180, 48, DARK_TEAL, "IRAN  •  GULF", "US blockade, Hormuz mines",
             "Iran vows to confront the blockade. Three tankers hit mines in Hormuz.", TEAL, vis_iran, hs=26, hl=31, ss=15, sl=20)

# small cards 3 x 2
cards = [
    ("ROHINGYA  •  ICJ", "14 nations back genocide ruling", "UK sanctions five Myanmar generals after the court ruling.", RED, "§"),
    ("NATO  •  SPACE", "NATO vows to defend space", "Reports say Russia may put a nuclear weapon in orbit.", BLUE, "★"),
    ("AI", "UN wants global AI rules in a year", "US states sue over Grok images; Korea pays to catch AI cheating.", (90, 40, 140), "AI"),
    ("CLIMATE  •  COP31", "Climate summit ends with no deal", "Talks fail after a split over fossil fuels and finance.", GREEN, "◉"),
    ("INDONESIA", "Factory fire in Banten kills 26", "Dozens missing after a fire at a factory in Banten.", GOLD, "!"),
    ("WORLD", "Nepal quake; Pakistan astronaut", "5.6 quake near China. Zeeshan Ali to join China's Tiangong station.", TEAL, "✦"),
]
cw, ch, gap = 304, 138, 16
for i, (kick, head, sub, col, mark) in enumerate(cards):
    x = 36 + (i % 3) * (cw + gap)
    y = 626 + (i // 3) * (ch + gap)
    d.rounded_rectangle([x, y, x+cw, y+ch], radius=8, fill=CARD, outline=LINE, width=2)
    d.ellipse([x+cw-38, y+10, x+cw-12, y+36], fill=col)
    d.text((x+cw-25, y+12), mark, font=font(SANS_B, 14), fill=(255, 255, 255), anchor="ma")
    d.text((x+12, y+10), kick, font=font(SANS_B, 13), fill=col)
    yy = draw_lines(d, wrap(d, head, font(SERIF_B, 19), cw-24), x+12, y+34, font(SERIF_B, 19), INK, 23)
    draw_lines(d, wrap(d, sub, font(SANS, 14), cw-24), x+12, yy+4, font(SANS, 14), MUTED, 18)
    d.line([(x+12, y+ch-12), (x+cw-12, y+ch-12)], fill=col, width=3)

d.line([(48, 934), (976, 934)], fill=LINE, width=2)
d.text((512, 946), "24 NOVEMBER 2026  —  NVIDIA  •  UKRAINE  •  GAZA  •  IRAN  •  ROHINGYA  •  AI  •  CLIMATE", font=font(SANS_B, 14), fill=MUTED, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
