"""Build entry.png v8.1 (1024x1024) for news-image-20261124.
International broadsheet front page, layout fixed with measured heights:
  masthead 30-146, lead+secondary 158-470, 3 columns 486-750, IN BRIEF 766-962.
  1 lead + 2 secondary + 9 column stories + 23 brief = 35 stories.
Deterministic: fixed date, fixed text, no network.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (250, 248, 243)
INK = (17, 17, 17)
MUTED = (80, 76, 68)
RED = (160, 30, 20)
BLUE = (27, 79, 114)
TEAL = (14, 116, 109)
GREEN = (22, 101, 52)
GOLD = (146, 96, 0)
PURPLE = (90, 40, 140)
NAVY = (13, 32, 54)
RULE = (190, 182, 166)

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

def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([18, 18, W-19, H-19], outline=INK, width=3)

# masthead
d.line([(36, 30), (988, 30)], fill=INK, width=2)
d.text((36, 40), "TUESDAY, 24 NOVEMBER 2026", font=font(SANS_B, 12), fill=INK)
d.text((988, 40), "35 STORIES  •  WORLD EDITION", font=font(SANS_B, 12), fill=INK, anchor="ra")
d.text((512, 52), "THE WORLD TODAY", font=font(SERIF_B, 56), fill=INK, anchor="ma")
d.text((512, 118), "The day's news, in one image", font=font(SERIF, 16), fill=MUTED, anchor="ma")
d.line([(36, 142), (988, 142)], fill=INK, width=3)
d.line([(36, 146), (988, 146)], fill=INK, width=1)

# lead: Nvidia
LX, LW = 36, 600
d.rounded_rectangle([LX, 158, LX+LW, 268], radius=8, fill=NAVY)
d.rounded_rectangle([LX+30, 178, LX+130, 238], radius=8, fill=(34, 197, 94), outline=(255, 255, 255), width=3)
d.rounded_rectangle([LX+62, 192, LX+98, 224], radius=4, fill=NAVY, outline=(255, 255, 255), width=2)
pts = [(LX+170, 238), (LX+260, 224), (LX+350, 230), (LX+450, 198), (LX+560, 178)]
d.line(pts, fill=(255, 255, 255), width=5, joint="curve")
d.ellipse([LX+555, 173, LX+565, 183], fill=(250, 204, 21))
d.text((LX+LW-16, 238), "+31%", font=font(SANS_B, 22), fill=(250, 204, 21), anchor="ra")
d.text((LX, 280), "TECH  •  MARKETS  —  LEAD STORY", font=font(SANS_B, 11), fill=GREEN)
yy = draw_lines(d, wrap(d, "Nvidia brings back Huang as chief", font(SERIF_B, 38), LW), LX, 298, font(SERIF_B, 38), INK, 44)
d.text((LX, yy+4), "By The World Today Staff  •  SANTA CLARA, Calif.", font=font(SANS_B, 11), fill=INK)
draw_lines(d, wrap(d, "Shares jump 31% in a day and the S&P 500 rises 4.73% after Donald Trump presses the board to reinstate Jensen Huang, less than two weeks after he resigned.", font(SERIF, 15), LW), LX, yy+24, font(SERIF, 15), MUTED, 20)

# secondary, right column, each 150px tall
RX, RW = 652, 336
def secondary(y, col, kick, head, sub, visual):
    d.line([(RX, y), (RX+RW, y)], fill=RULE, width=1)
    visual(RX, y+6, RW)
    d.text((RX, y+58), kick, font=font(SANS_B, 11), fill=col)
    yy = draw_lines(d, wrap(d, head, font(SERIF_B, 21), RW), RX, y+74, font(SERIF_B, 21), INK, 25)
    draw_lines(d, wrap(d, sub, font(SERIF, 13), RW), RX, yy+3, font(SERIF, 13), MUTED, 17)

def vis_ship(x, y, w):
    d.polygon([(x+60, y+28), (x+220, y+28), (x+195, y+48), (x+85, y+48)], fill=BLUE)
    d.rectangle([x+130, y+6, x+140, y+28], fill=BLUE)
    d.polygon([(x+140, y+6), (x+172, y+18), (x+140, y+26)], fill=RED)

def vis_gaza(x, y, w):
    for bx, bh in ((x+20, 20), (x+70, 30), (x+122, 16), (x+176, 26), (x+232, 22)):
        d.rectangle([bx, y+48-bh, bx+40, y+48], fill=(124, 29, 29))

secondary(158, BLUE, "CONFLICT  •  LIBYA", "Ukraine sinks Russian warship off Libya",
          "BENGHAZI, Libya — Seven naval drones hit the corvette Merkury. The UN calls for a probe.", vis_ship)
secondary(318, RED, "GAZA", "Israeli strikes kill Hamas security chief",
          "GAZA CITY — Naeem Abu Nahel among 7 killed. A UNRWA worker died a day earlier.", vis_gaza)

# 3 columns, 9 stories
d.line([(36, 486), (988, 486)], fill=INK, width=2)
cols = [
    [("IRAN  •  GULF", TEAL, "US blockade, Hormuz mines", "WASHINGTON — Iran vows to confront the blockade. Three tankers hit mines."),
     ("ROHINGYA  •  ICJ", RED, "14 nations back genocide ruling", "THE HAGUE — UK sanctions five Myanmar generals after the ruling."),
     ("NATO  •  SPACE", BLUE, "NATO vows to defend space", "BRUSSELS — Russia may put a nuclear weapon in orbit.")],
    [("AI", PURPLE, "UN wants global AI rules in a year", "NEW YORK — US states sue over Grok images; Korea pays to catch cheating."),
     ("CLIMATE  •  COP31", GREEN, "Climate summit ends with no deal", "ANTALYA — Talks fail over fossil fuels and finance."),
     ("INDONESIA", GOLD, "Factory fire in Banten kills 26", "BANTEN — Dozens missing after a fire at a factory.")],
    [("NEPAL", TEAL, "Nepal quake, 5.6 near China", "KATHMANDU — Tremor felt near the China border."),
     ("SPACE", TEAL, "Pakistan astronaut for Tiangong", "ISLAMABAD — Zeeshan Ali, first foreign astronaut on the station."),
     ("USA", RED, "Democrats take US House", "WASHINGTON — The party wins by its largest margin in decades.")],
]
for ci, col in enumerate(cols):
    x = 36 + ci * 324
    if ci:
        d.line([(x-12, 500), (x-12, 752)], fill=RULE, width=1)
    y = 500
    for kick, colr, head, sub in col:
        d.text((x, y), kick, font=font(SANS_B, 11), fill=colr)
        yy = draw_lines(d, wrap(d, head, font(SERIF_B, 15), 300), x, y+16, font(SERIF_B, 15), INK, 19)
        y = draw_lines(d, wrap(d, sub, font(SERIF, 11), 300), x, yy+2, font(SERIF, 11), MUTED, 15) + 10

# IN BRIEF: remaining 23 stories
d.line([(36, 766), (988, 766)], fill=INK, width=2)
d.text((36, 778), "IN BRIEF", font=font(SANS_B, 14), fill=RED)
d.text((988, 778), "23 MORE STORIES", font=font(SANS_B, 12), fill=MUTED, anchor="ra")
brief = [
    "Zaporizhzhia hit: 2 killed, 40 hurt", "Russian deaths pass 700,000", "Russia warns Estonia",
    "Qatar PM meets Vance, Rubio", "Libya demands Kyiv explain", "Oxfam: Gaza 'toxic land'",
    "UN: Gaza war undone 77 years", "UK logs Iranian attacks", "Germany gets Delta access",
    "Congo Ebola teams trapped", "EU limits Russian visas", "Iraq orders oilfields control",
    "US blacklists Megaspeed", "Pentagon accuses Canada", "Trump death penalty order",
    "US loses measles status", "Sanofi buys Insmed $41B", "Somalia, Uganda hit Al-Shabaab",
    "Houthis: Saudi strike kills 17", "Zelensky urges NATO admission", "Spain amnesties Puigdemont",
    "Mexico to try 'El Chapo Isidro'", "Car bomb in Villavicencio",
]
for i, item in enumerate(brief):
    x = 36 + (i % 3) * 324
    y = 804 + (i // 3) * 20
    d.text((x, y), "•  " + item, font=font(SANS, 13), fill=INK)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
