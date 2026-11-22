[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/pompomsuzuki/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/pompomsuzuki/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — 22 November 2026

Entry for make.fun's bounty [“Sum up 22 November's world news in one image”](https://make.fun/bounty/news-image-20261122).

`main.py` is a dependency-free Python program (standard library only, no
network) that draws a newspaper front page of Sunday 22 November 2026 and
writes it to `/output/entry.png` (1024×1024 PNG). It renders its own PNG
encoder, raster canvas and 5×7 pixel font, so the two grading runs produce
byte-identical output.

The front page carries 44 stories of the day:

- **Lead — Manama / Strait of Hormuz:** Bahrain says an Iranian strike set
  fire to a civilian industrial site, and two oil tankers were hit near the
  Strait of Hormuz, according to a UK maritime agency.
- **Climate — Antalya:** the COP31 talks run into a second day of overtime
  with no new text, split over fossil fuels and finance.
- **Justice — Guasave, Mexico:** special forces capture FBI top-10 fugitive
  “El Chapo Isidro”; 11 people die in the violence that follows in Sinaloa.
- **Markets — New York:** an AI sell-off tips the Dow and S&P 500 into
  correction, and Nvidia faces a reported US accounting probe.
- **39 briefs in five sections** — Europe (11), Asia-Pacific (10),
  Americas (8), Middle East + Africa (6) and Sport + Life (5) — plus a
  round-the-clock strip across the page.

Every story was reported on Sunday 22 November 2026.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

## License

MIT — see `LICENSE`.
