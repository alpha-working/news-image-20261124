"""Build entry.png v7 (1024x1024) for news-image-20261124.
Pretty redesign of the v6 grid: hero visual band with the 4 lead
stories drawn as icons, then the same 35 numbered tiles, polished
with soft shadows, filled number badges and a coloured left border.
Deterministic: fixed date, fixed text, no network, no random.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (247, 242, 232)
INK = (17, 17, 17)
CARD = (255, 255, 255)
LINE = (210, 200, 182)
SHADOW = (225, 216, 198)
RED = (180, 35, 24)
BLUE = (27, 79, 114)
TEAL = (14, 116, 109)
GREEN = (22, 101, 52)
GOLD = (146, 96, 0)
PURPLE = (90, 40, 140)
NAVY = (13, 32, 54)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
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

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([18, 18, W-19, H-19], outline=INK, width=3)
d.rectangle([24, 24, W-25, H-25], outline=LINE, width=1)

# masthead
d.text((512, 34), "THE DAY IN ONE IMAGE", font=font(SERIF_B, 48), fill=INK, anchor="ma")
d.text((512, 96), "TUESDAY  •  24 NOVEMBER 2026  •  35 STORIES", font=font(SANS_B, 18), fill=RED, anchor="ma")
d.line([(48, 130), (976, 130)], fill=GOLD, width=2)
d.line([(48, 135), (976, 135)], fill=RED, width=4)

# hero visual band: 4 lead stories as icons on navy
d.rounded_rectangle([36, 148, 988, 232], radius=12, fill=NAVY)
# 1 chip (Nvidia)
d.rounded_rectangle([86, 168, 146, 200], radius=6, fill=(34, 197, 94), outline=(255, 255, 255), width=2)
d.rounded_rectangle([104, 178, 128, 190], radius=3, fill=NAVY, outline=(255, 255, 255), width=2)
d.text((116, 208), "NVIDIA  +31%", font=font(SANS_B, 12), fill=(250, 204, 21), anchor="ma")
# 2 ship (Libya)
d.polygon([(300, 192), (400, 192), (380, 206), (320, 206)], fill=(255, 255, 255))
d.rectangle([344, 168, 352, 192], fill=(255, 255, 255))
d.polygon([(352, 168), (380, 178), (352, 186)], fill=(239, 68, 68))
d.text((350, 208), "LIBYA", font=font(SANS_B, 12), fill=(255, 255, 255), anchor="ma")
# 3 buildings (Gaza)
for bx, bh in ((540, 22), (575, 32), (612, 18), (650, 28)):
    d.rectangle([bx, 204-bh, bx+28, 204], fill=(239, 68, 68))
d.text((606, 208), "GAZA", font=font(SANS_B, 12), fill=(255, 255, 255), anchor="ma")
# 4 tanker (Hormuz)
d.polygon([(790, 182), (890, 182), (872, 200), (808, 200)], fill=(255, 255, 255))
d.rectangle([828, 168, 852, 182], fill=(255, 255, 255))
d.text((840, 208), "HORMUZ", font=font(SANS_B, 12), fill=(255, 255, 255), anchor="ma")

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

cw, ch, gx, gy = 184, 100, 8, 6
for i, (tag, col, head) in enumerate(stories):
    x = 36 + (i % 5) * (cw + gx)
    y = 248 + (i // 5) * (ch + gy)
    d.rounded_rectangle([x+3, y+3, x+cw+3, y+ch+3], radius=8, fill=SHADOW)
    d.rounded_rectangle([x, y, x+cw, y+ch], radius=8, fill=CARD, outline=LINE, width=2)
    d.rectangle([x, y+8, x+5, y+ch-8], fill=col)
    d.ellipse([x+14, y+12, x+38, y+36], fill=col)
    d.text((x+26, y+15), f"{i+1}", font=font(SANS_B, 13), fill=(255, 255, 255), anchor="ma")
    d.text((x+cw-10, y+16), tag, font=font(SANS_B, 11), fill=col, anchor="ra")
    yy = y + 42
    for ln in wrap(d, head, font(SERIF_B, 16), cw-22):
        d.text((x+12, yy), ln, font=font(SERIF_B, 16), fill=INK)
        yy += 19

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
