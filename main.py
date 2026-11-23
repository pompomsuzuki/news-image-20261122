#!/usr/bin/env python3
"""The World in One Day - Sunday 22 November 2026.

Draws a dense newspaper front page that sums up the day's world news
in one 1024x1024 PNG and writes it to /output/entry.png (or to
$MAKEFUN_OUTPUT_DIR). 43 stories: one lead, three secondary stories,
a round-the-clock strip and 39 briefs in five regional sections.
Pure standard library, no network, deterministic output.
"""

import os
import struct
import zlib

W = H = 1024

PAPER = (247, 243, 232)
INK = (24, 24, 36)
FAINT = (100, 96, 92)
RED = (178, 34, 52)
BLUE = (28, 52, 110)
SKY = (38, 84, 150)
SEA = (52, 96, 138)
GOLD = (190, 140, 40)
GREEN = (34, 110, 64)
ORANGE = (224, 122, 26)
WHITE = (250, 250, 248)
SAND = (226, 214, 188)

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", ".#.#.", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"],
    "3": [".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".....", ".##..", ".#..."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "'": [".##..", ".##..", ".#...", ".....", ".....", ".....", "....."],
    ":": [".....", ".##..", ".##..", ".....", ".....", ".##..", ".##.."],
    "%": ["##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    ">": ["#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."],
    "<": ["....#", "...#.", "..#..", ".#...", "..#..", "...#.", "....#"],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "(": ["...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"],
    ")": [".##..", "..#..", "...#.", "...#.", "...#.", "..#..", ".##.."],
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bytes(bg) * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def frame(self, x, y, w, h, color, t=3):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=2):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(t):
                for oy in range(t):
                    self.set(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d2 <= r * r:
                    self.set(xx, yy, color)
                if not fill and r * r - 2 * r <= d2 <= r * r:
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color, bold=False):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale + (1 if bold else 0), scale, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def text_c(self, cx, y, s, scale, color, bold=False):
        return self.text(cx - self.text_w(s, scale) // 2, y, s, scale,
                         color, bold)


def wrap(s, width):
    """Word-wrap s to lines of at most width characters."""
    lines = []
    cur = ""
    for word in s.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = cur + " " + word if cur else word
    if cur:
        lines.append(cur)
    return lines


def star(cv, cx, cy, r, color):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    for yy in range(int(cy - r), int(cy + r) + 1):
        for xx in range(int(cx - r), int(cx + r) + 1):
            inside = False
            j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > yy) != (yj > yy) and \
                        xx < (xj - xi) * (yy - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            if inside:
                cv.set(xx, yy, color)


def tanker_scene(cv, x, y, w, h):
    """A tanker in a strait, one flank burning, under a night sky."""
    cv.rect(x, y, w, h, (30, 44, 74))
    # stars
    for i in range(28):
        sx = x + (i * 53) % (w - 8) + 4
        sy = y + (i * 29) % (h // 3) + 4
        cv.set(sx, sy, WHITE)
        cv.set(sx + 1, sy, WHITE)
    # moon
    cv.circle(x + w - 42, y + 26, 13, (232, 226, 200))
    cv.circle(x + w - 36, y + 22, 11, (30, 44, 74))
    # far shore
    cv.rect(x, y + h - 52, w, 10, SAND)
    # sea
    cv.rect(x, y + h - 42, w, 42, SEA)
    for i in range(9):
        wy = y + h - 36 + i * 4
        cv.line(x + (i * 37) % 60, wy, x + (i * 37) % 60 + 42, wy,
                (120, 160, 190), 1)
    # tanker hull and deck
    hx, hy = x + 34, y + h - 66
    cv.rect(hx, hy + 18, 190, 16, (16, 16, 20))
    cv.line(hx - 12, hy + 22, hx, hy + 22, (16, 16, 20), 4)
    cv.rect(hx + 12, hy + 8, 120, 10, (90, 96, 104))
    cv.rect(hx + 138, hy, 26, 18, (200, 200, 205))
    cv.rect(hx + 146, hy - 8, 6, 8, (60, 60, 66))
    for i in range(4):
        cv.rect(hx + 18 + i * 28, hy + 11, 20, 4, GOLD)
    # fire on the stern
    star(cv, hx + 168, hy - 6, 17, ORANGE)
    star(cv, hx + 168, hy - 6, 10, RED)
    star(cv, hx + 158, hy + 2, 8, GOLD)
    # smoke
    for i in range(5):
        cv.circle(hx + 150 + i * 9, hy - 22 - i * 6, 6 + i, (70, 70, 78))
    cv.text(x + 10, y + h - 16, "STRAIT OF HORMUZ", 1, WHITE)


def sun_icon(cv, x, y):
    cv.circle(x + 30, y + 26, 15, GOLD)
    for dx, dy in ((0, -22), (0, 22), (-22, 0), (22, 0), (-16, -16),
                   (16, -16), (-16, 16), (16, 16)):
        cv.line(x + 30 + dx // 2, y + 26 + dy // 2, x + 30 + dx,
                y + 26 + dy, ORANGE, 3)
    # thermometer
    cv.rect(x + 66, y + 8, 7, 34, SKY)
    cv.circle(x + 69, y + 48, 9, RED)
    cv.rect(x + 67, y + 22, 3, 22, RED)


def badge_icon(cv, x, y):
    cv.circle(x + 34, y + 32, 27, BLUE, fill=False)
    cv.circle(x + 34, y + 32, 24, BLUE, fill=False)
    star(cv, x + 34, y + 32, 17, GOLD)
    cv.rect(x + 62, y + 44, 22, 6, RED)
    cv.rect(x + 62, y + 54, 22, 6, INK)


def chart_icon(cv, x, y):
    cv.line(x + 4, y + 4, x + 4, y + 56, INK, 3)
    cv.line(x + 4, y + 56, x + 84, y + 56, INK, 3)
    pts = [(x + 10, y + 12), (x + 30, y + 22), (x + 46, y + 16),
           (x + 64, y + 36), (x + 80, y + 46)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 4)
    cv.line(x + 80, y + 46, x + 66, y + 44, RED, 4)
    cv.line(x + 80, y + 46, x + 76, y + 32, RED, 4)


LEAD_HEAD = ["IRAN HITS BAHRAIN SITE;", "TANKERS STRUCK IN HORMUZ"]
LEAD_BRIEF = [
    "BAHRAIN SAYS AN IRANIAN STRIKE SET FIRE TO A",
    "CIVILIAN INDUSTRIAL SITE. TWO OIL TANKERS WERE",
    "HIT NEAR THE STRAIT, A UK AGENCY REPORTS.",
]

SECONDARY = [
    ("CLIMATE - ANTALYA, TURKEY", GREEN, "sun",
     "COP31 TALKS RUN INTO OVERTIME",
     "A SECOND DAY OF OVERTIME WITH NO NEW TEXT. NATIONS SPLIT OVER "
     "FOSSIL FUELS AND FINANCE; THE EU WANTS A GOOD DEAL OR NO DEAL."),
    ("JUSTICE - GUASAVE, MEXICO", BLUE, "badge",
     "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
     "SPECIAL FORCES ARREST FBI TOP-10 FUGITIVE FAUSTO ISIDRO MEZA "
     "FLORES. 11 PEOPLE DIE IN THE VIOLENCE THAT FOLLOWS IN SINALOA."),
    ("MARKETS - NEW YORK", RED, "chart",
     "AI SELL-OFF TIPS US INTO CORRECTION",
     "THE DOW AND S&P 500 SLIDE INTO CORRECTION AS AI AND CHIP "
     "SHARES FALL. NVIDIA FACES A REPORTED US ACCOUNTING PROBE."),
]

SECTIONS_LEFT = [
    ("EUROPE", BLUE, [
        ("UKRAINE STRAINS RUSSIAN LOGISTICS",
         "KYIV STRIKES THE CRIMEAN BRIDGE AS RUSSIA HITS KRYVYI RIH, "
         "KILLING TWO AND WOUNDING DOZENS"),
        ("NATO VOWS TO DEFEND EVERY INCH OF POLAND",
         "THE PLEDGE FOLLOWS ANOTHER RUSSIAN AIRSPACE VIOLATION"),
        ("FRANCE MARCHES FOR A SIXTH WEEKEND",
         "PROTESTERS RALLY OVER LIVING COSTS AND PUBLIC SERVICES"),
        ("DENMARK EXPELS RUSSIAN ATTACHE",
         "COPENHAGEN ALLEGES A PLOT BEHIND THE DIPLOMAT'S COVER"),
        ("FRENCH POLICE JAILED FOR RACIST VIOLENCE",
         "OFFICERS CONVICTED OVER AN ATTACK ON A BLACK MAN"),
        ("SENATE OKAYS POLICE SHOOTING LAW",
         "CRITICS DUB THE FRENCH MEASURE A 'LICENCE TO KILL'"),
        ("UN TALKS PLEDGE KILLER-ROBOT RULES BY 2028",
         "A DRAFTING GOAL AGREED AFTER RUSSIAN PUSHBACK"),
        ("CROATIA DEMANDS JUSTICE OVER HOSPITAL DEATH",
         "VIDEO SHOWS STAFF HOLDING A PILLOW OVER A PATIENT"),
        ("PAOLO BULGARI DIES AT 89",
         "THE JEWELLER TO HOLLYWOOD STARS BUILT A LUXURY BRAND"),
        ("BURNHAM EYES REJOINING",
         "UK-EU DEALS STACK UP A DAY AFTER THE RESET PACKAGE"),
        ("EX-ITALY POLICE CHIEF DIES AMID MAFIA PROBE",
         "DE GENNARO WAS ACCUSED OVER A 1992 BOMBING INQUIRY"),
    ]),
    ("ASIA-PACIFIC", RED, [
        ("JAKARTA FACTORY FIRE KILLS THREE",
         "36 MISSING AS THE SEARCH GOES ON AT THE SWEETS PLANT"),
        ("EU AND INDONESIA SIGN TRADE DEAL",
         "PUTTING SIGNATURES TO TEN YEARS OF TALKS"),
        ("CHINA OPPOSES US TELECOM BAN",
         "BEIJING WARNS OF RETALIATION OVER NUMBER ACCESS"),
        ("SEOUL EDUCATION CHIEF QUITS",
         "THE RESIGNATION FOLLOWS AN AI CHEATING SCANDAL"),
        ("AUSTRALIA CRITICIZES US OVER AUKUS",
         "CANBERRA HITS BACK AT BUDGET OFFICE COMMENTS"),
        ("TOXIC ALCOHOL KILLS 11 IN MANIPUR",
         "MORE THAN 180 IN HOSPITAL IN INDIA'S NORTH-EAST"),
        ("JAPAN'S BIG ACCOUNTS SURGE",
         "BANK DEPOSITS OVER 100 MILLION YEN CLIMB, BOJ SAYS"),
        ("JAPAN EYES CRITICAL CHEMICALS LIST",
         "ORGANIC CHEMICALS MAY JOIN THE PRODUCTS REGISTER"),
        ("LDP FIGURE HINTS AT MINISTER SWAP",
         "A SCANDAL-HIT EDUCATION MINISTER MAY BE REPLACED"),
        ("PAKISTAN DELEGATION CLEARED FOR TAJ MAHAL",
         "THE VISITORS WERE DENIED A DELHI SHRINE VISIT"),
    ]),
]

SECTIONS_RIGHT = [
    ("AMERICAS", (140, 90, 20), [
        ("TRUMP VOWS 10% CREDIT CARD CAP",
         "HE PROMISES TO WORK WITH DEMOCRATS ON RATES"),
        ("US AGENCIES BREACHED BY HACKERS",
         "THE AGRICULTURE DEPARTMENT AND THE FBI, REPORTS SAY"),
        ("MIDTERM DEFEAT CORNERS VANCE",
         "REPUBLICAN LOSSES WIDEN THE 2028 FIELD"),
        ("FLORIDA RIVER BREAKS 73-YEAR RECORD",
         "FLOODS FROM MIAMI TO BREVARD MAY LAST TO JANUARY"),
        ("SEATTLE AIRPORT ICE ARRESTS FUEL ANGER",
         "A DISTRESSING SCENE DELAYS A LOS ANGELES FLIGHT"),
        ("TRUMP THREATENS TAX ON AI FIRMS",
         "A 'TREMENDOUS TAX' ON OVERSEAS DATA CENTRES"),
        ("DELTA OUTAGE DELAYS 1,600 FLIGHTS",
         "ITS WEIGHT-AND-BALANCE SYSTEM FAILED; NOT A HACK"),
        ("SENATE VOTE TESTS NEW DEMOCRATS",
         "A LEADERSHIP VOTE TESTS THE PARTY OF CHANGE EARLY"),
    ]),
    ("MIDDLE EAST + AFRICA", (120, 60, 130), [
        ("HOUTHIS FIRE MISSILES AT RIYADH",
         "THE COALITION INTERCEPTS THREE AND HITS HODEIDAH"),
        ("ISRAELI STRIKES CONTINUE IN GAZA",
         "AN AID VEHICLE IS HIT IN GAZA CITY"),
        ("LEBANON'S AOUN BLAMES ISRAEL AND IRAN",
         "HE SAYS BOTH THREATEN HIS COUNTRY'S SOVEREIGNTY"),
        ("IRAQ POWER PLANT FIRE KILLS FOUR",
         "35 INJURED AT THE HARTHA STATION NEAR BASRA"),
        ("NIGERIA FUNERAL BOAT CAPSIZES",
         "AT LEAST 24 DEAD ON THE WAY TO A FUNERAL"),
        ("IRAN SIGNALS ON HORMUZ",
         "THE STRAIT MAY REOPEN ON 'REASONABLE' TERMS"),
    ]),
    ("SPORT + LIFE", GREEN, [
        ("SHIMADA WINS FINLANDIA TROPHY",
         "THE JAPANESE SKATER BOOKS A GRAND PRIX FINAL SPOT"),
        ("SCOTLAND OVERPOWER JAPAN",
         "JAPAN WELL BEATEN IN THE NATIONS CHAMPIONSHIP"),
        ("MAN CITY SLUMP DEEPENS",
         "FRUSTRATION MOUNTS AS THE POOR RUN CONTINUES"),
        ("RENNIE ON THE HOT SEAT",
         "THE ALL BLACKS COACH FEELS THE ENGLAND LOSS HEAT"),
        ("ALCARAZ WINS FIRST ATP FINALS TITLE",
         "HE BEATS ZVEREV IN TURIN TO END THE SEASON ON TOP"),
    ]),
]


def section(cv, x, y, w, name, color, items):
    cv.rect(x, y, w, 17, color)
    cv.text(x + 8, y + 4, name, 1, WHITE, bold=True)
    cv.text(x + w - 8 - cv.text_w(str(len(items)), 1), y + 4,
            str(len(items)), 1, WHITE, bold=True)
    y += 21
    for head, tail in items:
        cv.rect(x + 1, y + 1, 5, 5, color)
        cv.text(x + 11, y, head, 1, INK, bold=True)
        y += 9
        for ln in wrap(tail, 79):
            cv.text(x + 11, y, ln, 1, FAINT)
            y += 9
        y += 2
    return y


def main():
    cv = Canvas(W, H, PAPER)

    # masthead
    cv.text_c(512, 12, "THE WORLD IN ONE DAY", 5, INK)
    cv.rect(14, 54, 996, 4, INK)
    cv.text(14, 64, "SUNDAY 22 NOVEMBER 2026", 2, INK)
    cv.text(1010 - cv.text_w("44 STORIES - 6 REGIONS - ONE PAGE", 2), 64,
            "44 STORIES - 6 REGIONS - ONE PAGE", 2, RED)
    cv.rect(14, 84, 996, 2, INK)

    # lead story
    lx, ly, lw, lh = 14, 94, 996, 176
    cv.frame(lx, ly, lw, lh, INK, 4)
    cv.rect(lx, ly, lw, 24, RED)
    cv.text(lx + 12, ly + 5, "LEAD STORY - MANAMA, BAHRAIN", 2, WHITE)
    ty = ly + 40
    for ln in LEAD_HEAD:
        cv.text(lx + 14, ty, ln, 4, INK)
        ty += 34
    by = ty + 4
    for ln in LEAD_BRIEF:
        cv.text(lx + 14, by, ln, 2, INK)
        by += 18
    tanker_scene(cv, lx + lw - 344, ly + 34, 330, 132)
    cv.text(lx + lw - 344, ly + lh - 14, "", 1, FAINT)

    # round-the-clock strip
    sy = 280
    cv.rect(14, sy, 996, 22, SAND)
    x = 22
    x = cv.text(x, sy + 7, "AROUND THE CLOCK:", 1, RED, bold=True) + 12
    strip = ("OVERNIGHT: TANKERS HIT IN HORMUZ >> COP31 INTO OVERTIME "
             ">> CARTEL BOSS HELD IN SINALOA >> FLORIDA RIVER AT A "
             "RECORD LEVEL")
    cv.text(x, sy + 7, strip, 1, INK)

    # secondary cards
    cy = 312
    cw, chh, gap = 324, 148, 12
    icons = {"sun": sun_icon, "badge": badge_icon, "chart": chart_icon}
    for i, (kick, color, icon, head, brief) in enumerate(SECONDARY):
        x = 14 + i * (cw + gap)
        cv.frame(x, cy, cw, chh, INK, 3)
        cv.rect(x, cy, cw, 20, color)
        cv.text(x + 10, cy + 5, kick, 1, WHITE, bold=True)
        icons[icon](cv, x + cw - 96, cy + 28)
        hy = cy + 30
        for ln in wrap(head, 17):
            cv.text(x + 12, hy, ln, 2, INK, bold=True)
            hy += 17
        by = cy + 98
        for ln in wrap(brief, 50):
            cv.text(x + 12, by, ln, 1, INK)
            by += 10

    # briefs in two columns
    y1 = 472
    for name, color, items in SECTIONS_LEFT:
        y1 = section(cv, 14, y1, 488, name, color, items) + 6
    y2 = 472
    for name, color, items in SECTIONS_RIGHT:
        y2 = section(cv, 522, y2, 488, name, color, items) + 6
    assert max(y1, y2) <= 1002, (y1, y2)

    # footer
    cv.rect(14, 1004, 996, 2, INK)
    cv.text_c(512, 1010,
              "EVERY STORY REPORTED ON SUNDAY 22 NOVEMBER 2026 - "
              "DRAWN IN CODE, NO PHOTOGRAPHS", 1, FAINT)

    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw += cv.px[yy * W * 3:(yy + 1) * W * 3]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png)


if __name__ == "__main__":
    main()
