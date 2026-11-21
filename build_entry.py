"""Draw the passport spread of the invented Republic of Vespera."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 724
NAVY_TOP, NAVY_BOT = (24, 36, 78), (13, 20, 48)
GOLD = (212, 175, 95)
GOLD_DIM = (150, 124, 70)
PAPER = (233, 228, 210)
INK = (38, 44, 66)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), NAVY_BOT)
d = ImageDraw.Draw(img, "RGBA")
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3)))

# guilloche arcs
for r in range(60, 900, 26):
    d.ellipse([W // 2 - r, H // 2 - int(r * 0.72), W // 2 + r, H // 2 + int(r * 0.72)], outline=(255, 255, 255, 7), width=1)
# spine
for x in range(W // 2 - 16, W // 2 + 16):
    a = int(90 * (1 - abs(x - W // 2) / 16))
    d.line([(x, 0), (x, H)], fill=(0, 0, 0, a))
# gold frames
d.rectangle([26, 26, W // 2 - 26, H - 26], outline=GOLD + (200,), width=2)
d.rectangle([W // 2 + 26, 26, W - 26, H - 26], outline=GOLD + (200,), width=2)

# --- emblem: sun over waves ---
cx, cy, R = W // 4 + 13, 238, 74
for k in range(12):
    a = k * math.pi / 6
    x1, y1 = cx + int((R + 8) * math.cos(a)), cy + int((R + 8) * math.sin(a))
    x2, y2 = cx + int((R + 30) * math.cos(a)), cy + int((R + 30) * math.sin(a))
    d.line([(x1, y1), (x2, y2)], fill=GOLD, width=4)
d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=GOLD, width=4)
d.ellipse([cx - R + 12, cy - R + 12, cx + R - 12, cy + R - 12], outline=GOLD_DIM, width=2)
for i, dy in enumerate((26, 44, 62)):
    pts = [(cx - 52 + j * 4, cy + dy + int(7 * math.sin(j / 4.4))) for j in range(27)]
    d.line(pts, fill=GOLD, width=3)
d.ellipse([cx - 15, cy - 34, cx + 15, cy - 4], fill=GOLD)

def centered(text, y, font, fill, cx_at):
    w = d.textlength(text, font=font)
    d.text((cx_at - w / 2, y), text, font=font, fill=fill)

LX = W // 4 + 13
centered("REPUBLIC OF VESPERA", 392, F(SERIF, 33), GOLD, LX)
centered("P A S S P O R T", 452, F(SERIF, 27), PAPER, LX)
centered("By dusk we wander, by dawn we return", 528, F(SANS, 16), (190, 196, 220), LX)
centered("MINISTRY OF TIDES · PORT LUMEN", 566, F(SANS, 13), GOLD_DIM, LX)

# --- data page ---
RX = W // 2 + 52
centered("VESPERA", 44, F(SERIF, 21), GOLD, W // 2 + W // 4 - 13)
d.line([(RX, 84), (W - 52, 84)], fill=GOLD + (160,), width=1)
# photo box
px, py, pw, ph = RX, 104, 148, 188
d.rectangle([px, py, px + pw, py + ph], fill=(196, 200, 214), outline=GOLD, width=2)
d.ellipse([px + 44, py + 26, px + 104, py + 86], fill=(112, 120, 148))
d.pieslice([px + 18, py + 88, px + 130, py + 208], 180, 360, fill=(112, 120, 148))
d.text((px + 8, py + ph - 22), "VESPERA · VSP", font=F(SANS, 11), fill=(90, 96, 120))

fx = px + pw + 26
rows = [
    ("Type / Type", "P", "Code / Code", "VSP"),
    ("Passport No.", "V0420697", None, None),
    ("Surname / Nom", "MARLOWE", None, None),
    ("Given names / Prénoms", "ELIA JUNE", None, None),
    ("Nationality / Nationalité", "VESPERAN", None, None),
    ("Date of birth", "14 MAR 1998", "Place of birth", "PORT LUMEN"),
    ("Date of issue", "03 JUN 2024", "Date of expiry", "03 JUN 2034"),
    ("Authority / Autorité", "MINISTRY OF TIDES", None, None),
]
y = 108
for label, value, label2, value2 in rows:
    d.text((fx, y), label.upper(), font=F(SANS, 10), fill=GOLD_DIM)
    d.text((fx, y + 14), value, font=F(SANSB, 16), fill=PAPER)
    if label2:
        d.text((fx + 148, y), label2.upper(), font=F(SANS, 10), fill=GOLD_DIM)
        d.text((fx + 148, y + 14), value2, font=F(SANSB, 15), fill=PAPER)
    y += 46
sig_y = y + 2
d.line([(fx, sig_y + 22), (fx + 180, sig_y + 22)], fill=(160, 166, 190), width=1)
d.text((fx, sig_y), "E. Marlowe", font=F(SERIF, 19), fill=(198, 204, 226))
d.text((fx, sig_y + 26), "HOLDER'S SIGNATURE", font=F(SANS, 9), fill=GOLD_DIM)

# MRZ
mrz = ["P<VSPMARLOWE<<ELIA<JUNE<<<<<<<<<<<<<<<<",
       "V0420697<4VSP9803146F3406032<<<<<<<<<08"]
my = H - 92
d.rectangle([RX - 14, my - 10, W - 40, my + 62], fill=(222, 218, 198))
for i, line in enumerate(mrz):
    d.text((RX - 2, my + i * 26), line, font=F(MONO, 16), fill=INK)

# stamps
def stamp(cx_s, cy_s, r, color, top, bottom, angle):
    layer = Image.new("RGBA", (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    sd.ellipse([4, 4, r * 2 + 4, r * 2 + 4], outline=color + (205,), width=3)
    sd.ellipse([13, 13, r * 2 - 5, r * 2 - 5], outline=color + (150,), width=1)
    w1 = sd.textlength(top, font=F(SANSB, 13))
    sd.text((r + 4 - w1 / 2, r - 24), top, font=F(SANSB, 13), fill=color + (215,))
    w2 = sd.textlength(bottom, font=F(SANSB, 12))
    sd.text((r + 4 - w2 / 2, r + 8), bottom, font=F(SANSB, 12), fill=color + (215,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(cx_s - layer.width / 2), int(cy_s - layer.height / 2)), layer)

stamp(448, 128, 62, (64, 178, 168), "ARRIVED", "12 OCT 2026", -14)
stamp(898, 552, 50, (206, 96, 74), "DEPARTED", "KITE HARBOUR", 11)

img = img.filter(ImageFilter.GaussianBlur(0.4))
img.save("entry.png", optimize=True)
print("saved", img.size)
