"""Generate the 1200x630 social preview card (public/og.png).

Reuses the site's own hero.webp backdrop and the Ocean Deep OKLCH tokens, so the
link preview looks like the page it opens. Re-run this if the tokens or the copy
on the card change; the PNG it writes is what gets committed.

Usage:  python3 scripts/make-og.py <repo-root> <fonts-dir>

Needs Pillow, plus the two variable TTFs in <fonts-dir> (the site itself loads
woff2, which Pillow can't read, so fetch the TTFs once into a temp folder):

  curl -L -o SpaceGrotesk.ttf \
    'https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf'
  curl -L -o DMSans.ttf \
    'https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf'
"""
import math, sys
from PIL import Image, ImageDraw, ImageFont

SITE = sys.argv[1]
SCRATCH = sys.argv[2]  # folder holding SpaceGrotesk.ttf and DMSans.ttf


def oklch(L, C, h):
    """OKLCH -> 8-bit sRGB, so the card uses the exact same tokens as global.css."""
    hr = math.radians(h)
    a, b = C * math.cos(hr), C * math.sin(hr)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    lin = (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )
    out = []
    for c in lin:
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        out.append(max(0, min(255, round(c * 255))))
    return tuple(out)


BACKGROUND = oklch(0.22, 0.06, 250)
FOREGROUND = oklch(0.95, 0.01, 245)
ACCENT = oklch(0.74, 0.09, 192)
MUTED = oklch(0.65, 0.03, 235)

W, H = 1200, 630

# Backdrop: the site's own hero image, cover-cropped, under the same 82% navy
# overlay body uses. Same picture, same dimming, so the card reads as the site.
hero = Image.open(f"{SITE}/public/hero.webp").convert("RGB")
scale = max(W / hero.width, H / hero.height)
hero = hero.resize((round(hero.width * scale), round(hero.height * scale)), Image.LANCZOS)
left, top = (hero.width - W) // 2, (hero.height - H) // 2
img = hero.crop((left, top, left + W, top + H))
img = Image.blend(img, Image.new("RGB", (W, H), BACKGROUND), 0.82)

d = ImageDraw.Draw(img)


def font(path, size, weight):
    f = ImageFont.truetype(f"{SCRATCH}/{path}", size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


grotesk_bold = font("SpaceGrotesk.ttf", 96, 700)
dm_bold = font("DMSans.ttf", 26, 700)
dm_reg = font("DMSans.ttf", 34, 400)
dm_metric = font("DMSans.ttf", 26, 500)

X = 90
d.text((X, 150), "PRODUCT MANAGER", font=dm_bold, fill=ACCENT)
d.text((X, 205), "Tim Russell", font=grotesk_bold, fill=FOREGROUND)
d.text((X, 335), "I ship consumer products through the hard parts.", font=dm_reg, fill=MUTED)

# One metric, per the review: enough to say what the work was worth.
pill = "$3M year-over-year lift in live wagering volume"
box = d.textbbox((0, 0), pill, font=dm_metric)
pw, ph = box[2] - box[0], box[3] - box[1]
py = 430
d.rounded_rectangle(
    (X, py, X + pw + 56, py + ph + 34), radius=(ph + 34) // 2,
    fill=BACKGROUND, outline=ACCENT, width=2,
)
d.text((X + 28, py + 17 - box[1]), pill, font=dm_metric, fill=ACCENT)

# Accent rule down the left edge, echoing the rail.
d.rectangle((0, 0, 8, H), fill=ACCENT)

img.save(f"{SITE}/public/og.png", optimize=True)
print("wrote public/og.png", img.size)
