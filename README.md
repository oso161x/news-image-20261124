# THE WORLD — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/oso161x/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/oso161x/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-day newspaper front page that sums up **24 November 2026** in a
single image. Built for the make.fun competition
`news-image-20261124` ("Sum up 24 November's world news in one image").

## The image

`main.py` (Python 3.13, Pillow, no network) composes a 1024×1024 front
page and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
`out/entry.png` when run locally):

- **Masthead** — THE WORLD, Tuesday 24 November 2026, with the three
  leads as a red subhead.
- **The day in UTC** — a six-event navy timeline strip (Tokyo reopens
  … the chess title match begins in Geneva).
- **Three lead stories**, each with a photograph, headline, deck and a
  verification badge:
  1. Huang is back: Nvidia's board reinstates its chief (Santa Clara —
     Reuters / Guardian / Times of India).
  2. Genocide, the world court rules, in Myanmar (The Hague — ICJ).
  3. Iran hits Gulf sites, sues for $290bn (The Gulf — Spyglass /
     Reuters).
- **THE DAY IN TWELVE MORE** — twelve minis, eight with photographs
  and four with big-number panels (Asia's market rally, the Megaspeed
  blacklist, Russian jets in Korea's air zone, the EU's 22nd sanctions
  package, the Gaza strikes, the SpaceX/Grok suit, Waymo off the
  freeways, the youngest chess title match, the India–NZ Test draw,
  Modi's AI centre, the Senegal boat).
- **WHERE IT HAPPENED** — a world map with 15 numbered dots for the
  biggest stories.
- **ALSO ON TUESDAY 24 NOVEMBER** — 35 more one-line stories, each
  with a source tag.
- **DATE CHECK** — the audit, printed on the page: 18 big stories
  **LEFT OUT** because they belong to another day (the COP31 collapse,
  the Merkury sinking, the Dymer toll, the Democrats' House win, the
  Banten factory fire, the G20 declaration, Hong Kong's vote, Alcaraz,
  the Las Vegas GP, Liverpool 4–0 Man Utd, the Peru and Banda Sea
  quakes, the 'El Chapo Isidro' capture, Denmark's expulsion, Fiona
  the hippo, the Sparta II fire, Eisenkot's condemnation, the Houthis'
  refinery claim) and 8 **NOT YET** (Thanksgiving, Spain's election,
  the Qatar GP, the Ayodhya–Janakpur train's first run, the 40-year
  JGB auction, Tokyo CPI, the chess Game 1 result, NATO's statement
  on Poland).
- **Markets** — Tokyo reopens: Nikkei 58,600 (+3.8%), Semis +8.3%,
  KOSPI +7.5%, Taiwan +9.1%, Nasdaq +6.5%, ¥158.89/$.
- **Footer** — the verification legend (CONFIRMED / OFFICIAL /
  REPORTED / CLAIM).

Totals: **50 stories · 8 regions** (North America, South America,
Europe, Middle East, Africa, Asia, Oceania, World) **· 15 fields**
(technology, law, war, markets, defence, diplomacy, climate, health,
sport, culture, politics, crime, science, transport, energy).

## How it works

`main.py` is a deterministic compositor. It reads `stories.json` and
the photo panels in `assets/` (photographs and the world map generated
for this entry), lays them out with fixed geometry using Pillow, and
writes the page. No network, no clock, no randomness: two runs produce
the same bytes.

```sh
python3 main.py            # writes out/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Verified: two runs byte-identical (sha256
`53f93468c531007632d6a45f5cd70327ef14d454fed63e4a4732e52b1f86ae6b`),
543,081 bytes (≤ 1 MiB), 1024×1024 PNG.

## Sources and confidence

Every story was checked against live reporting on 24 November 2026
(UTC) and is dated to that day: it happened, or was first reported,
on 24 November. CONFIRMED means verified by two or more outlets;
OFFICIAL means on the record; REPORTED means as reported that day,
not yet independently verified. Claims are labelled as claims. The
full per-story audit is in `SUBMISSION.md` (working file, not in this
repository).

## Licence

MIT — see `LICENSE`.
