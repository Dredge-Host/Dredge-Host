#!/usr/bin/env python3
"""Render 1200x630 share images for the main pages into assets/og/pages/ and point each
page's og:image at its own image, plus the site-wide default, assets/og-image.png. Comparison images use the prices in make-comparisons.py,
so run that first when prices change. Needs Chromium:
    python3 scripts/make-share-images.py
"""
import html
import importlib.util
import pathlib
import re
import subprocess
import tempfile

SITE = pathlib.Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "og" / "pages"

spec = importlib.util.spec_from_file_location("comparisons", SITE / "scripts" / "make-comparisons.py")
comparisons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comparisons)

PAGES = {
    "pricing": ("Pricing", "Simple cPanel hosting from $3 a month",
                "Same price at renewal · 17% off yearly · 7-day money-back guarantee"),
    "domains": ("Domains", ".com domains, $14 a year",
                "Register, transfer, or bring your own, with renewal prices listed up front"),
    "wordpress-hosting": ("WordPress hosting", "WordPress hosting from $3 a month",
                          "One-click install · Any plugin or theme · Same price at renewal"),
    "website-builder": ("Website builder", "Build a website without code, from $3 a month",
                        "Templates · Drag-and-drop editing · Your own domain and free HTTPS"),
    "why-dredge": ("Why Dredge", "Hosting without the fine print",
                   "Renewal prices compared with Hostinger, Bluehost, SiteGround, and DreamHost"),
}

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<style>
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: #125d59; color: #fff; font-family: "IBM Plex Sans", sans-serif;
         position: relative; box-sizing: border-box; padding: 76px 96px; }}
  img {{ height: 112px; display: block; margin-left: -6px; }}
  .tag {{ margin-top: 40px; font-size: 26px; font-weight: 500; letter-spacing: 0.12em;
          text-transform: uppercase; color: #b9d6d3; }}
  h1 {{ margin: 14px 0 0; font-family: "Poppins", sans-serif; font-weight: 600;
        font-size: 66px; line-height: 1.1; max-width: 1010px; }}
  .sub {{ margin-top: 22px; font-size: 30px; color: #d9ebe9; max-width: 1010px; }}
  .stats {{ display: flex; gap: 28px; margin-top: 34px; }}
  .stat {{ background: #fff; color: #111; border-radius: 6px; padding: 20px 28px; min-width: 330px; }}
  .stat p {{ margin: 0; font-size: 24px; color: #4a5b59; }}
  .stat strong {{ display: block; font-family: "IBM Plex Mono", monospace; font-weight: 500;
                  font-size: 52px; margin-top: 4px; }}
  .stat.them strong {{ color: #8a3f16; }}
  .stat.us strong {{ color: #0f5c58; }}
  .bar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 16px; background: #0c4744; }}
</style></head><body>
<img src="{logo}" alt="">
<div class="tag">{tag}</div>
<h1>{title}</h1>
{extra}
<div class="bar"></div>
</body></html>"""


# The default share image, used by the home page and every page without its own.
HOME_TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&family=IBM+Plex+Sans:wght@400&display=swap" rel="stylesheet">
<style>
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: #125d59; color: #fff; font-family: "IBM Plex Sans", sans-serif;
         position: relative; box-sizing: border-box; padding: 132px 96px; }}
  img {{ height: 150px; display: block; margin-left: -8px; }}
  h1 {{ margin: 24px 0 0; font-family: "Poppins", sans-serif; font-weight: 600;
        font-size: 64px; line-height: 1.12; max-width: 620px; }}
  .sub {{ margin-top: 20px; font-size: 26px; color: #d9ebe9; }}
  .tile {{ position: absolute; right: 96px; top: 164px; width: 300px; height: 300px; box-sizing: border-box;
           border: 1.5px solid rgba(255, 255, 255, 0.22); border-radius: 56px;
           display: flex; align-items: center; justify-content: center; }}
  .tile svg {{ width: 104px; }}
  .bar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 16px; background: #0c4744; }}
</style></head><body>
<img src="{logo}" alt="">
<h1>Hosting that gets out of your way.</h1>
<div class="sub">cPanel · Free TLS · Email · Plans from {price}/mo</div>
<div class="tile"><svg viewBox="0 0 18 32" aria-hidden="true">
  <path d="M1 2 L17 2 L15 22 L3 22 Z" fill="#fff"/>
  <rect x="4" y="7" width="10" height="2.6" rx="1" fill="#125d59"/>
  <rect x="4" y="12" width="9" height="2.6" rx="1" fill="#125d59"/>
  <rect x="4" y="17" width="10" height="2.6" rx="1" fill="#125d59"/>
  <path d="M9 24 C7 27 7 30 9 31.5 C11 30 11 27 9 24 Z" fill="#fff"/>
</svg></div>
<div class="bar"></div>
</body></html>"""


def render(name, doc, out=None):
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as tmp:
        tmp.write(doc)
    out = out or OUT / f"{name}.png"
    subprocess.run(
        ["chromium", "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--window-size=1200,630", "--virtual-time-budget=5000",
         f"--screenshot={out}", pathlib.Path(tmp.name).as_uri()],
        check=True, capture_output=True,
    )
    pathlib.Path(tmp.name).unlink()
    print(f"wrote {out.relative_to(SITE)}")


def point_page_at_image(name):
    page = SITE / f"{name}.html"
    text = page.read_text()
    new = re.sub(r'<meta property="og:image" content="[^"]*">',
                 f'<meta property="og:image" content="https://dredgehost.com/assets/og/pages/{name}.png">',
                 text, count=1)
    if new != text:
        page.write_text(new)
        print(f"updated {page.relative_to(SITE)}")


def main():
    logo = (SITE / "assets" / "logo-light.png").as_uri()
    render("og-image", HOME_TEMPLATE.format(logo=logo, price=comparisons.short(comparisons.DREDGE_MONTH)),
           out=SITE / "assets" / "og-image.png")
    for name, (tag, title, sub) in PAGES.items():
        extra = f'<div class="sub">{html.escape(sub)}</div>'
        render(name, TEMPLATE.format(logo=logo, tag=html.escape(tag), title=html.escape(title), extra=extra))
        point_page_at_image(name)
    for slug, p in comparisons.HOSTS.items():
        theirs = comparisons.cumulative(p["yearly"])[-1]
        ours = comparisons.DREDGE_YEAR * comparisons.YEARS
        extra = (
            '<div class="stats">'
            f'<div class="stat them"><p>{html.escape(p["name"])} {html.escape(p["plan"])}, 6 years</p>'
            f'<strong>{comparisons.short(theirs)}</strong></div>'
            f'<div class="stat us"><p>Dredge Silt, 6 years</p><strong>{comparisons.short(ours)}</strong></div>'
            '</div>')
        render(f"dredge-vs-{slug}", TEMPLATE.format(
            logo=logo, tag="Renewal prices compared", title=f"Dredge vs {html.escape(p['name'])}", extra=extra))


if __name__ == "__main__":
    main()
