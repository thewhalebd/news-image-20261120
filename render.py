#!/usr/bin/env python3
"""Render the Nov 20 2026 world-news summary image, 1024x1024, deterministic.
Original illustration only: PIL shapes + text. No photos, no logos, no network.
Stories verified from Reuters / AP / Japan Times / NDTV / CNN / The Standard,
checked Fri 20 Nov 2026 ~07:10 Asia/Dhaka (01:10 UTC). See README.md for sources.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)
INK = (15, 36, 64)
WHITE = (255, 255, 255)
ACCENT = (196, 30, 58)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, font, color, max_w, lh):
    for ln in wrap(draw, text, font, max_w):
        draw.text((x, y), ln, font=font, fill=color)
        y += lh
    return y

# ---------- header ----------
d.rectangle([0, 0, W, 112], fill=INK)
d.rectangle([0, 112, W, 118], fill=ACCENT)
d.text((32, 14), "THE WORLD IN ONE PICTURE", font=f(SERIF_B, 30), fill=WHITE)
d.text((32, 56), "FRIDAY  20  NOVEMBER  2026", font=f(SANS_B, 34), fill=(255, 214, 90))
d.text((W - 32, 22), "WORLD NEWS", font=f(SANS_B, 22), fill=WHITE, anchor="ra")
d.text((W - 32, 52), "ONE DAY  •  ONE IMAGE", font=f(SANS, 20), fill=(200, 210, 225), anchor="ra")

# ---------- lead: GTA VI ----------
LX, LY, LW, LH = 24, 134, 976, 208
# sunset gradient
for i in range(LH):
    t = i / LH
    r = int(255 - 60 * t); g = int(120 + 40 * t); b = int(90 + 90 * t)
    d.line([(LX, LY + i), (LX + LW, LY + i)], fill=(r, g, b))
# sun
d.ellipse([LX + 790, LY + 18, LX + 900, LY + 128], fill=(255, 236, 150))
# skyline silhouette
import random
random.seed(7)
x = LX
while x < LX + LW:
    bw = random.randint(34, 70); bh = random.randint(28, 88)
    d.rectangle([x, LY + LH - bh, x + bw, LY + LH], fill=(30, 16, 60))
    x += bw + 4
d.rectangle([LX, LY, LX + LW, LY + LH], outline=(30, 16, 60), width=3)
d.text((LX + 24, LY + 16), "GTA VI TAKES OVER THE WORLD", font=f(SANS_B, 40), fill=WHITE)
d.text((LX + 24, LY + 66), "THE GAME EVERYONE IS PLAYING", font=f(SANS_B, 20), fill=(255, 236, 150))
para(d, LX + 24, LY + 100,
     "A day after launch: 99/100 from critics, record livestreams — 132m hours watched in one day — and about $1.8bn in sales.",
     f(SANS, 22), WHITE, LW - 48, 30)

# ---------- grid panels ----------
panels = [
    ("SUMMIT  •  SHENZHEN", (196, 30, 58),
     "THREE LEADERS, ONE TABLE",
     "Trump, Xi and Putin hold rare three-way talks on nuclear risks and issue a joint \u2018peace declaration\u2019 — but no breakthrough on Ukraine.",
     "flags"),
    ("UKRAINE", (15, 80, 140),
     "CRIMEA BRIDGE HIT AGAIN",
     "Ukraine strikes the bridge to Crimea for a third time this week. Putin vows to hit back hard and drops any energy truce.",
     "bridge"),
    ("GULF  •  OIL", (120, 70, 10),
     "TANKERS BURN NEAR HORMUZ",
     "Three oil tankers catch fire after hitting mines east of the Strait of Hormuz as Iran steps up attacks — while oil prices slide.",
     "tanker"),
    ("JUSTICE  •  THE HAGUE", (20, 90, 70),
     "MYANMAR GUILTY OF GENOCIDE",
     "The top UN court finds Myanmar committed state-sponsored genocide against the Muslim Rohingya.",
     "scales"),
    ("MARKETS", (90, 40, 120),
     "AI IPO SOARS, STOCKS SLUMP",
     "Anthropic debuts at $83 a share, briefly worth $2 trillion — yet Wall Street falls 2% to seven-month lows.",
     "chart"),
    ("WEATHER  •  INDIA", (10, 110, 130),
     "CYCLONE AKVAN HITS INDIA",
     "The severe storm makes landfall on India\u2019s east coast. 120,000 people evacuated; dozens of trains cancelled.",
     "storm"),
]

GX, GY, PW, PH, GAP = 24, 354, 482, 184, 12
for i, (tag, col, head, cap, icon) in enumerate(panels):
    px = GX + (i % 2) * (PW + GAP)
    py = GY + (i // 2) * (PH + GAP)
    d.rectangle([px, py, px + PW, py + PH], fill=WHITE, outline=(200, 195, 180), width=2)
    d.rectangle([px, py, px + PW, py + 34], fill=col)
    d.text((px + 14, py + 6), tag, font=f(SANS_B, 19), fill=WHITE)
    # icon zone right of headline
    ix, iy = px + PW - 78, py + 44
    if icon == "flags":
        for j, c in enumerate([(196, 30, 58), (30, 90, 180), (220, 180, 40)]):
            d.ellipse([ix + j * 22 - 8, iy, ix + j * 22 + 14, iy + 22], fill=c, outline=INK)
            d.rectangle([ix + j * 22 + 2, iy + 22, ix + j * 22 + 4, iy + 44], fill=INK)
    elif icon == "bridge":
        d.arc([ix - 10, iy, ix + 70, iy + 60], 180, 360, fill=INK, width=5)
        d.line([(ix - 10, iy + 34), (ix + 70, iy + 34)], fill=INK, width=5)
        for j in range(4):
            d.line([(ix + j * 20, iy + 12), (ix + j * 20, iy + 34)], fill=INK, width=3)
    elif icon == "tanker":
        d.polygon([(ix - 12, iy + 22), (ix + 72, iy + 22), (ix + 58, iy + 48), (ix + 2, iy + 48)], fill=(120, 70, 10))
        d.rectangle([ix + 14, iy, ix + 40, iy + 22], fill=(120, 70, 10))
        d.line([(ix - 12, iy + 52), (ix + 72, iy + 52)], fill=(40, 110, 160), width=3)
    elif icon == "scales":
        d.line([(ix + 30, iy), (ix + 30, iy + 48)], fill=INK, width=4)
        d.line([(ix + 4, iy + 6), (ix + 56, iy + 6)], fill=INK, width=4)
        d.arc([ix - 2, iy + 20, ix + 20, iy + 42], 0, 180, fill=INK, width=3)
        d.arc([ix + 40, iy + 20, ix + 62, iy + 42], 0, 180, fill=INK, width=3)
    elif icon == "chart":
        for j, h in enumerate([18, 34, 26, 44]):
            d.rectangle([ix + j * 16, iy + 48 - h, ix + j * 16 + 11, iy + 48], fill=(196, 30, 58) if j == 3 else (90, 40, 120))
        d.line([(ix - 4, iy + 8), (ix + 64, iy + 40)], fill=(196, 30, 58), width=4)
    elif icon == "storm":
        for r in (34, 24, 14):
            d.arc([ix + 30 - r, iy + 24 - r, ix + 30 + r, iy + 24 + r], 20, 300, fill=(10, 110, 130), width=4)
    y = para(d, px + 14, py + 44, head, f(SANS_B, 24), INK, PW - 100, 29)
    para(d, px + 14, py + 102, cap, f(SANS, 18), (50, 50, 50), PW - 28, 23)

# ---------- footer ticker ----------
FY = 354 + 3 * 184 + 2 * 12 + 10
d.rectangle([24, FY, 1000, FY + 72], fill=INK)
d.text((40, FY + 6), "ALSO TODAY:", font=f(SANS_B, 19), fill=(255, 214, 90))
para(d, 40, FY + 30,
     "Nicholls hits 113* as New Zealand reach 243/5 vs India  •  Voyager 1 phones home from a light-day away  •  Riyadh\u2019s tallest tower damaged in a Houthi strike",
     f(SANS, 16), WHITE, 936, 20)

img.save("entry.png", optimize=True)
print("saved entry.png")
