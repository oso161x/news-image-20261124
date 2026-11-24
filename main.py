#!/usr/bin/env python3
"""THE WORLD — Tuesday 24 November 2026.

A one-day newspaper front page: 50 stories from Tuesday 24 November 2026,
every one first reported (or happening) that day, across 8 regions and
15 fields. Leads with photographs, a UTC timeline, twelve more stories,
a numbered world map, a 35-story index with a source tag on every story,
a DATE CHECK box that names the big stories left out (wrong day) and the
ones that have not happened yet, and a markets strip.

The program reads stories.json and the photo panels in assets/ (all
generated for this entry) and draws the page with Pillow. It takes no
network, no clock and no random input, so two runs write identical bytes.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(HERE, "out"))

W, H = 1024, 1024
MX = 16                      # side margin
CW = W - 2 * MX              # content width

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
NAVY = (20, 33, 61)
GRAY = (92, 88, 78)
FAINT = (232, 227, 214)
DOT_GREEN = (27, 107, 46)
DOT_AMBER = (146, 92, 0)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_line(draw, text, fnt, max_w):
    """Shorten one line with an ellipsis until it fits max_w."""
    if text_w(draw, text, fnt) <= max_w:
        return text
    while text and text_w(draw, text + "…", fnt) > max_w:
        text = text[:-1].rstrip()
    return text + "…"


def centre(draw, y, text, fnt, fill, x0=MX, x1=W - MX):
    tw = text_w(draw, text, fnt)
    draw.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)


def rule(draw, y, fill=INK, weight=2, x0=MX, x1=W - MX):
    for i in range(weight):
        draw.line([(x0, y + i), (x1, y + i)], fill=fill)


def load_panel(name):
    path = os.path.join(HERE, "assets", name + ".png")
    return Image.open(path).convert("RGB")


def draw_masthead(draw, data):
    """Kicker line, giant dated masthead, red subhead of the three leads."""
    kick = font(SANS_B, 11)
    centre(draw, 10, data["kicker"], kick, INK)
    head = font(SERIF_B, 40)
    centre(draw, 26, "Tuesday 24 November 2026", head, INK)
    rule(draw, 70, fill=RED, weight=2)
    sub = font(SANS_B, 13)
    lines = wrap(draw, data["subhead"], sub, CW)
    y = 77
    for line in lines[:2]:
        centre(draw, y, line, sub, RED)
        y += 16


def draw_timeline(draw, data):
    """Navy UTC band: six timed moments from the day."""
    y0, y1 = 108, 142
    draw.rectangle([MX, y0, W - MX, y1], fill=NAVY)
    cells = len(data["timeline"])
    cw = CW / cells
    f_time = font(SANS_B, 10)
    f_txt = font(SANS, 9)
    for i, (when, what) in enumerate(data["timeline"]):
        cx = MX + i * cw
        centre(draw, y0 + 3, when, f_time, (255, 255, 255), x0=cx, x1=cx + cw)
        centre(draw, y0 + 17, fit_line(draw, what, f_txt, cw - 8), f_txt,
               (220, 226, 238), x0=cx, x1=cx + cw)


def draw_leads(draw, data):
    """Three lead cards: photo, kicker, headline, deck, source line."""
    y0 = 148
    card_w, gap = 325, 8
    f_kick = font(SANS_B, 10)
    f_head = font(SERIF_B, 15)
    f_deck = font(SANS, 10)
    f_src = font(SANS, 9)
    for i, lead in enumerate(data["leads"]):
        x = MX + i * (card_w + gap)
        photo = load_panel(lead["img"]).resize((card_w, 120), Image.LANCZOS)
        draw._image.paste(photo, (x, y0))
        badge = {"CONFIRMED": DOT_GREEN, "OFFICIAL": NAVY,
                 "REPORTED": DOT_AMBER}.get(lead["badge"], GRAY)
        draw.text((x, y0 + 126), lead["kicker"], font=f_kick, fill=RED)
        bw = text_w(draw, lead["badge"], f_kick)
        draw.rectangle([x + card_w - bw - 8, y0 + 125,
                        x + card_w, y0 + 138], fill=badge)
        draw.text((x + card_w - bw - 4, y0 + 126), lead["badge"],
                  font=f_kick, fill=(255, 255, 255))
        y = y0 + 142
        for line in wrap(draw, lead["head"], f_head, card_w)[:2]:
            draw.text((x, y), line, font=f_head, fill=INK)
            y += 18
        y += 2
        for line in wrap(draw, lead["deck"], f_deck, card_w)[:3]:
            draw.text((x, y), line, font=f_deck, fill=INK)
            y += 13
        draw.text((x, y + 2), "Source: " + lead["source"],
                  font=f_src, fill=GRAY)


def draw_minis(draw, data):
    """Twelve more stories in a 4 x 3 grid: photo or big-number panel left,
    kicker (field, place and short source) plus headline and deck right."""
    rule(draw, 386)
    head = font(SANS_B, 13)
    draw.text((MX, 392), "THE DAY IN TWELVE MORE", font=head, fill=INK)
    right = "12 stories  ·  6 regions  ·  9 fields"
    draw.text((W - MX - text_w(draw, right, head), 392), right,
              font=head, fill=GRAY)
    f_kick = font(SANS_B, 9)
    f_head = font(SANS_B, 11)
    f_deck = font(SANS, 9)
    card_w, card_h, gap = 242, 64, 8
    for i, mini in enumerate(data["minis"]):
        r, c = divmod(i, 4)
        x = MX + c * (card_w + gap)
        y = 412 + r * (card_h + 6)
        if mini["img"]:
            photo = load_panel("mini-" + mini["img"]).resize((62, 64),
                                                             Image.LANCZOS)
            draw._image.paste(photo, (x, y))
        else:
            draw.rectangle([x, y, x + 62, y + 64], fill=FAINT)
            draw.rectangle([x, y, x + 62, y + 64], outline=INK, width=1)
            big = mini["bignum"]
            done = False
            for size in (15, 13, 12, 11, 10):
                f_try = font(SANS_B, size)
                if text_w(draw, big, f_try) <= 56:
                    th = text_w(draw, big, f_try)
                    draw.text((x + (62 - th) / 2, y + (64 - size) / 2 - 1),
                              big, font=f_try, fill=RED)
                    done = True
                    break
            if not done:
                f_big = font(SANS_B, 12)
                lines = wrap(draw, big, f_big, 56)
                yy = y + (64 - 13 * len(lines)) // 2
                for line in lines[:2]:
                    centre(draw, yy, line, f_big, RED, x0=x, x1=x + 62)
                    yy += 14
        tx = x + 68
        tw = card_w - 68 - 2
        kick = mini["kicker"] + " — " + mini["src"]
        draw.text((tx, y + 1), fit_line(draw, kick, f_kick, tw),
                  font=f_kick, fill=RED)
        yy = y + 13
        for line in wrap(draw, mini["head"], f_head, tw)[:2]:
            draw.text((tx, yy), line, font=f_head, fill=INK)
            yy += 13
        for line in wrap(draw, mini["deck"], f_deck, tw)[:2]:
            draw.text((tx, yy), line, font=f_deck, fill=(58, 56, 48))
            yy += 11


def map_xy(lon, lat):
    """Calibrated linear fit from lon/lat to the generated map's pixels
    (map source is 2240x1120, cropped to y 40..1000, shown at 460x183)."""
    px = 224 + (lon + 122) * 6.63
    py = 573 - 6.35 * lat - 40
    return px * 460 / 2240, py * 183 / 960


def draw_map_index(draw, data):
    """Numbered world map on the left, 35-story index on the right."""
    rule(draw, 624, weight=1)
    f_sec = font(SANS_B, 12)
    draw.text((MX, 630), "WHERE IT HAPPENED — dots are story numbers 1–15",
              font=f_sec, fill=INK)
    draw.text((488, 630), "ALSO ON TUESDAY 24 NOVEMBER — 35 MORE STORIES",
              font=f_sec, fill=INK)
    world = load_panel("map").resize((460, 183), Image.LANCZOS)
    draw._image.paste(world, (MX, 642))
    dots = []
    for lead in data["leads"]:
        dots.append((lead["n"], lead["lon"], lead["lat"]))
    for mini in data["minis"]:
        dots.append((mini["n"], mini["lon"], mini["lat"]))
    f_dot = font(SANS_B, 8)
    for n, lon, lat in dots:
        dx, dy = map_xy(lon, lat)
        cx, cy = MX + dx, 642 + dy
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                     outline=(255, 255, 255), width=1)
        tw = text_w(draw, str(n), f_dot)
        draw.text((cx - tw / 2, cy - 4), str(n), font=f_dot,
                  fill=(255, 255, 255))
    f_idx = font(SANS, 8)
    cols = [data["index"][:18], data["index"][18:]]
    for ci, col in enumerate(cols):
        cx = 488 + ci * 262
        yy = 642
        for n, head, src in col:
            line = "%d. %s — %s" % (n, head, src)
            draw.text((cx, yy),
                      fit_line(draw, line, f_idx, 256),
                      font=f_idx, fill=INK)
            yy += 10


def draw_datecheck(draw, data):
    """DATE CHECK: the big stories deliberately left out, and the ones
    that have not happened yet. Date discipline, printed on the page."""
    y0 = 840
    draw.rectangle([MX, y0, W - MX, y0 + 140], outline=INK, width=2)
    draw.rectangle([MX, y0, W - MX, y0 + 20], fill=INK)
    f_title = font(SANS_B, 11)
    draw.text((MX + 8, y0 + 4),
              "DATE CHECK — every story above happened or was first reported "
              "on Tuesday 24 November 2026", font=f_title,
              fill=(255, 255, 255))
    f_lab = font(SANS_B, 9)
    f_it = font(SANS, 9)
    left = data["datecheck_left"]
    halves = [left[:9], left[9:]]
    for ci, col in enumerate(halves):
        cx = MX + 8 + ci * 330
        draw.text((cx, y0 + 26), "LEFT OUT — big news, wrong day",
                  font=f_lab, fill=RED)
        yy = y0 + 38
        for item in col:
            draw.text((cx, yy), "· " + fit_line(draw, item, f_it, 316),
                      font=f_it, fill=INK)
            yy += 11
    cx = MX + 8 + 2 * 330
    draw.text((cx, y0 + 26), "NOT YET — still to come",
              font=f_lab, fill=RED)
    yy = y0 + 38
    for item in data["datecheck_notyet"]:
        draw.text((cx, yy), "· " + fit_line(draw, item, f_it, 316),
                  font=f_it, fill=INK)
        yy += 11


def draw_footer(draw, data):
    """Markets strip and the verification legend."""
    f_mkt = font(SANS_B, 10)
    centre(draw, 988, data["markets"], f_mkt, NAVY)
    f_leg = font(SANS, 9)
    centre(draw, 1004, data["legend"] + "  ·  THE WORLD — built 24 Nov 2026  ·  "
           "All times UTC; sources on each story", f_leg, GRAY)


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    draw_masthead(draw, data)
    draw_timeline(draw, data)
    draw_leads(draw, data)
    draw_minis(draw, data)
    draw_map_index(draw, data)
    draw_datecheck(draw, data)
    draw_footer(draw, data)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "entry.png")
    page.save(out, optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
