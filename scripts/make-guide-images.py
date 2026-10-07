#!/usr/bin/env python3
"""Render a 1200x630 share image for every guide into assets/og/guides/. Needs Chromium:
    python3 scripts/make-guide-images.py
"""
import html
import pathlib
import re
import subprocess
import tempfile

SITE = pathlib.Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "og" / "guides"

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: #125d59; color: #fff; font-family: "IBM Plex Sans", sans-serif;
         position: relative; box-sizing: border-box; padding: 84px 96px; }}
  img {{ height: 128px; display: block; margin-left: -6px; }}
  .tag {{ margin-top: 52px; font-size: 26px; font-weight: 500; letter-spacing: 0.12em;
          text-transform: uppercase; color: #b9d6d3; }}
  h1 {{ margin: 18px 0 0; font-family: "Poppins", sans-serif; font-weight: 600;
        font-size: {size}px; line-height: 1.12; max-width: 1000px; }}
  .bar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 16px; background: #0c4744; }}
</style></head><body>
<img src="{logo}" alt="">
<div class="tag">Guide &middot; {category}</div>
<h1>{title}</h1>
<div class="bar"></div>
</body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    logo = (SITE / "assets" / "logo-light.png").as_uri()
    for page in sorted((SITE / "guides").glob("*.html")):
        text = page.read_text()
        title = html.unescape(re.search(r"<h1>(.*?)</h1>", text, re.S).group(1).strip())
        category = re.search(r'<a href="\.\./guides\.html">Guides</a> / ([^<]+)</p>', text).group(1).strip()
        size = 64 if len(title) <= 40 else 54
        doc = TEMPLATE.format(logo=logo, category=html.escape(category), title=html.escape(title), size=size)
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as tmp:
            tmp.write(doc)
        out = OUT / f"{page.stem}.png"
        subprocess.run(
            ["chromium", "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--window-size=1200,630", "--virtual-time-budget=5000",
             f"--screenshot={out}", pathlib.Path(tmp.name).as_uri()],
            check=True, capture_output=True,
        )
        pathlib.Path(tmp.name).unlink()
        print(f"wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    main()
