#!/usr/bin/env python3
"""Build the dredge-vs-*.html comparison pages from the prices below. When a host
changes its prices, update its entry (and its `checked` date), then run:
    python3 scripts/make-comparisons.py && python3 scripts/make-share-images.py && python3 scripts/sync-layout.py
"""
import pathlib
from html import escape

SITE = pathlib.Path(__file__).resolve().parent.parent

# Dredge Silt on yearly billing: the same $50 every year. Monthly billing is $5/mo.
DREDGE_YEAR = 50.00
DREDGE_MONTH = 5.00
YEARS = 6

HOSTS = {
    "hostinger": dict(
        name="Hostinger", term=48, plan="Premium", checked="October 16, 2026",
        intro="$2.99", renew="$10.99",
        # Cost of each year of hosting. Prepaid terms are spread over the years they cover.
        yearly=[35.88] * 4 + [131.88] * 2,
        lede="Hostinger's advertised price needs a four-year prepay, and it more than triples at "
             "renewal. Dredge costs more per month in that first term, and the same every year after.",
        rows=[
            ("Advertised price", "$2.99/mo", "$5/mo, or $50/yr"),
            ("To get that price", "Pay $143.52 up front for 48 months", "Pay monthly, or $50 for a year"),
            ("Renewal price", "$10.99/mo", "$5/mo, or $50/yr"),
            ("Websites", "3", "1 (5 on Channel, $12/mo)"),
            ("Storage", "20 GB SSD", "2 GB SSD (6 GB on Channel)"),
            ("Email", "2 mailboxes per site, free for the first year", "10 mailboxes, included for as long as you host"),
            ("Free domain", "First year, on plans of a year or longer", "Not included (.com is $14/yr)"),
            ("Backups", "Weekly", "Download any time, or daily with CodeGuard from $7.50/yr"),
            ("Control panel", "hPanel, Hostinger's own", "Standard cPanel"),
            ("Money-back guarantee", "30 days", "7 days"),
        ],
        cost_note="Hostinger figures use the 48-month intro price ($143.52, spread over four years) "
                  "and the $10.99/mo renewal rate.",
        theirs=[
            "You need more storage or several sites and want the lowest price for the first few years.",
            "You're happy to pay four years up front, and to move hosts again when the term ends.",
            "You want a free domain for the first year, or a 30-day money-back window.",
        ],
        sources=[("Hostinger web hosting plans", "https://www.hostinger.com/web-hosting")],
    ),
    "bluehost": dict(
        name="Bluehost", term=36, plan="Starter", checked="October 16, 2026",
        intro="$3.99", renew="$9.99",
        yearly=[47.88] * 3 + [119.88] * 3,
        lede="Bluehost's advertised price needs a three-year prepay, and renewals cost more than "
             "double, or four times as much if you pay monthly. Dredge charges the same at every renewal.",
        rows=[
            ("Advertised price", "$3.99/mo", "$5/mo, or $50/yr"),
            ("To get that price", "Pay $143.64 up front for 36 months", "Pay monthly, or $50 for a year"),
            ("Renewal price", "$9.99/mo (3-year term) to $15.99/mo (monthly)", "$5/mo, or $50/yr"),
            ("Websites", "10", "1 (5 on Channel, $12/mo)"),
            ("Storage", "10 GB NVMe SSD", "2 GB SSD (6 GB on Channel)"),
            ("Email", "Pro Email free for one month, then $2.50/mo", "10 mailboxes, included for as long as you host"),
            ("Free domain", "First year", "Not included (.com is $14/yr)"),
            ("Backups", "Weekly", "Download any time, or daily with CodeGuard from $7.50/yr"),
            ("Money-back guarantee", "30 days, minus a domain fee", "7 days"),
        ],
        cost_note="Bluehost figures use the 36-month intro price ($143.64, spread over three years), then "
                  "its cheapest renewal, $9.99/mo on another 3-year term. Monthly renewal is $15.99/mo.",
        theirs=[
            "You want more sites and storage than our Silt plan for the first three years.",
            "You're happy to pay three years up front, and to move hosts again when the term ends.",
            "You want a free domain for the first year, or a 30-day money-back window.",
        ],
        sources=[("Bluehost shared hosting plans", "https://www.bluehost.com/hosting/shared"),
                 ("Bluehost renewal price list (updated February 11, 2026)",
                  "https://www.bluehost.com/help/article/renewal-price-faq")],
    ),
    "siteground": dict(
        name="SiteGround", term=12, plan="StartUp", checked="October 16, 2026",
        intro="$2.99", renew="$17.99",
        yearly=[35.88] + [215.88] * 5,
        lede="SiteGround's advertised price lasts for the first year, and renewals cost six times "
             "as much. Dredge costs more per month in year one, and the same every year after.",
        rows=[
            ("Advertised price", "$2.99/mo", "$5/mo, or $50/yr"),
            ("To get that price", "Pay $35.88 up front for 12 months", "Pay monthly, or $50 for a year"),
            ("Renewal price", "$17.99/mo", "$5/mo, or $50/yr"),
            ("Websites", "1", "1 (5 on Channel, $12/mo)"),
            ("Storage", "10 GB", "2 GB SSD (6 GB on Channel)"),
            ("Email", "Included", "10 mailboxes, included for as long as you host"),
            ("Free domain", "First year (.com, .net, or .org)", "Not included (.com is $14/yr)"),
            ("Backups", "Daily", "Download any time, or daily with CodeGuard from $7.50/yr"),
            ("Control panel", "Site Tools, SiteGround's own", "Standard cPanel"),
            ("Money-back guarantee", "30 days", "7 days"),
        ],
        cost_note="SiteGround figures use the 12-month intro price and the $17.99/mo renewal rate.",
        theirs=[
            "You want daily backups and more storage included on the entry plan.",
            "You only need hosting for a year, and plan to move or rebuild after that.",
            "You want a free domain for the first year, or a 30-day money-back window.",
        ],
        sources=[("SiteGround web hosting plans", "https://www.siteground.com/web-hosting.htm")],
    ),
    "dreamhost": dict(
        name="DreamHost", term=12, plan="Launch", checked="October 16, 2026",
        intro="$2.89", renew="$10.99",
        yearly=[34.68] + [131.88] * 5,
        lede="DreamHost's advertised price lasts for the first year, then nearly quadruples. "
             "Dredge costs more per month in year one, and the same every year after.",
        rows=[
            ("Advertised price", "$2.89/mo", "$5/mo, or $50/yr"),
            ("To get that price", "Pay $34.68 up front for the first year", "Pay monthly, or $50 for a year"),
            ("Renewal price", "$10.99/mo", "$5/mo, or $50/yr"),
            ("Websites", "25", "1 (5 on Channel, $12/mo)"),
            ("Storage", "25 GB NVMe SSD", "2 GB SSD (6 GB on Channel)"),
            ("Email", "20 mailboxes, free for 3 months", "10 mailboxes, included for as long as you host"),
            ("Free domain", "First year, on yearly plans", "Not included (.com is $14/yr)"),
            ("Backups", "Daily", "Download any time, or daily with CodeGuard from $7.50/yr"),
            ("Control panel", "DreamHost's own", "Standard cPanel"),
            ("Money-back guarantee", "30 days", "7 days"),
        ],
        cost_note="DreamHost figures use the first-year price and the $10.99/mo renewal rate.",
        theirs=[
            "You want lots of sites and storage on the entry plan.",
            "You only need hosting for a year, and plan to move or rebuild after that.",
            "You want a free domain for the first year, or a 30-day money-back window.",
        ],
        sources=[("DreamHost shared hosting plans", "https://www.dreamhost.com/hosting/shared/")],
    ),
}

OURS = [
    "You'd rather not prepay years in advance, or be surprised by the renewal bill.",
    "You want standard cPanel, so moving later means nothing to relearn.",
    "You want email included for as long as you host, not just at the start.",
    "You want your support email answered by the people who run the servers.",
]


def money(x):
    return f"${x:,.2f}" if x != int(x) else f"${int(x):,}"


def short(x):
    return f"${round(x):,}"


def cumulative(values):
    out, total = [], 0.0
    for v in values:
        total += v
        out.append(round(total, 2))
    return out


def nice_step(top):
    for step in (50, 100, 200, 250, 300, 500, 1000):
        if top / step <= 5:
            return step
    return 1000


def chart(name, theirs, ours):
    """Inline SVG: cumulative cost by year, two lines, end labels, hover targets."""
    w, h = 640, 300
    left, right, top, bottom = 80, 104, 16, 44
    pw, ph = w - left - right, h - top - bottom
    step = nice_step(max(theirs))
    ymax = step * -(-max(theirs) // step)
    x = lambda i: left + pw * i / (YEARS - 1)
    y = lambda v: top + ph * (1 - v / ymax)
    grid = []
    v = 0
    while v <= ymax:
        grid.append(f'<line class="vs-grid" x1="{left}" x2="{left + pw}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>'
                    f'<text class="vs-tick" x="{left - 10}" y="{y(v) + 4:.1f}" text-anchor="end">{short(v)}</text>')
        v += step
    years = "".join(f'<text class="vs-tick" x="{x(i):.1f}" y="{h - 12}" text-anchor="middle">Year {i + 1}</text>'
                    for i in range(YEARS))
    path = lambda vals: " ".join(f"{'M' if i == 0 else 'L'}{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
    end = YEARS - 1
    # Keep the two end labels apart when the lines finish close together.
    ty, oy = y(theirs[end]), y(ours[end])
    if oy - ty < 30:
        ty, oy = min(ty, oy - 30), max(oy, ty + 30)
    hits = "".join(
        f'<rect class="vs-hit" x="{x(i) - pw / (2 * (YEARS - 1)):.1f}" y="{top}" width="{pw / (YEARS - 1):.1f}" '
        f'height="{ph}" data-x="{x(i):.1f}" data-year="{i + 1}" data-them="{money(theirs[i])}" '
        f'data-us="{money(ours[i])}"/>'
        for i in range(YEARS))
    return f"""<svg class="vs-chart" viewBox="0 0 {w} {h}" role="img"
                    aria-label="Total cost over six years: {escape(name)} {money(theirs[end])}, Dredge {money(ours[end])}">
                    {''.join(grid)}
                    {years}
                    <line class="vs-cursor" x1="0" x2="0" y1="{top}" y2="{top + ph}"/>
                    <path class="vs-line vs-them" d="{path(theirs)}"/>
                    <path class="vs-line vs-us" d="{path(ours)}"/>
                    <circle class="vs-dot vs-them-dot" cx="{x(end):.1f}" cy="{y(theirs[end]):.1f}" r="5"/>
                    <circle class="vs-dot vs-us-dot" cx="{x(end):.1f}" cy="{y(ours[end]):.1f}" r="5"/>
                    <text class="vs-end" x="{x(end) + 12:.1f}" y="{ty + 4:.1f}">{short(theirs[end])}</text>
                    <text class="vs-end" x="{x(end) + 12:.1f}" y="{oy + 4:.1f}">{short(ours[end])}</text>
                    {hits}
                </svg>"""


def page(slug, p):
    fn = f"dredge-vs-{slug}.html"
    name, plan = p["name"], p["plan"]
    title = f"Dredge vs {name}: Renewal Prices Compared | Dredge Host"
    theirs = cumulative(p["yearly"])
    ours = cumulative([DREDGE_YEAR] * YEARS)
    jump = float(p["renew"][1:]) / float(p["intro"][1:])
    desc = (f"{name} {plan} is advertised at {p['intro']}/mo, then renews at {p['renew']}/mo. Dredge Silt is "
            f"$5/mo or $50/yr, at the same price every renewal. Here's the full comparison.")
    tr = lambda cells: "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
    rows = "\n".join("                        " + tr(r) for r in p["rows"])
    years = "\n".join(f"                            <tr><td>Year {i + 1}</td><td>{money(t)}</td><td>{money(o)}</td></tr>"
                      for i, (t, o) in enumerate(zip(theirs, ours)))
    li = lambda xs: "\n".join(f"                            <li>{escape(x)}</li>" for x in xs)
    src = "\n".join(f'                    <li><a href="{u}" rel="noopener">{escape(t)}</a></li>' for t, u in p["sources"])
    others = "\n".join(
        f'                    <a class="doc-card" href="dredge-vs-{s}.html"><span class="doc-cat">Comparison</span>'
        f'<h3>Dredge vs {o["name"]}</h3><p>{o["intro"]}/mo at sign-up, {o["renew"]}/mo at renewal.</p></a>'
        for s, o in HOSTS.items() if s != slug)
    return fn, f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{escape(desc)}">
    <link rel="canonical" href="https://dredgehost.com/{fn}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Dredge Host">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="What {name}'s intro price turns into at renewal, compared with Dredge's same-price renewals.">
    <meta property="og:url" content="https://dredgehost.com/{fn}">
    <meta property="og:image" content="https://dredgehost.com/assets/og/pages/{fn[:-5]}.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="theme-color" content="#0f5c58">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="assets/dredge-app-tile-180.png">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://dredgehost.com/"}},
        {{"@type": "ListItem", "position": 2, "name": "Why Dredge", "item": "https://dredgehost.com/why-dredge.html"}},
        {{"@type": "ListItem", "position": 3, "name": "Dredge vs {name}", "item": "https://dredgehost.com/{fn}"}}
      ]
    }}
    </script>
</head>
<body data-root="" data-active="">
    <!-- site-header:start --><!-- site-header:end -->

    <main id="main">
        <section class="page-hero">
            <div class="wrap vs-hero">
                <div>
                    <p class="crumb"><a href="./">Home</a> / <a href="why-dredge.html">Why Dredge</a> / Dredge vs {name}</p>
                    <h1>Dredge vs {name}</h1>
                    <p class="lede">{escape(p['lede'])}</p>
                </div>
                <div class="jump-card" aria-label="Entry plan prices at sign-up and at renewal">
                    <div class="jump-row">
                        <p class="jump-name">{name} {plan}</p>
                        <p class="jump-prices"><span>{p['intro']}</span><span class="jump-arrow" aria-hidden="true">&rarr;</span><strong>{p['renew']}</strong><span class="jump-per">/mo</span></p>
                        <p class="jump-tag jump-up">{jump:.1f}&times; at renewal</p>
                    </div>
                    <div class="jump-row">
                        <p class="jump-name">Dredge Silt</p>
                        <p class="jump-prices"><span>$5</span><span class="jump-arrow" aria-hidden="true">&rarr;</span><strong>$5</strong><span class="jump-per">/mo</span></p>
                        <p class="jump-tag jump-same">Same price at renewal</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="wrap">
                <h2 class="section-title">What it costs over six years</h2>
                <div class="vs-stats">
                    <div class="vs-stat"><p class="vs-stat-label">{name} {plan}, six years</p><p class="vs-stat-value">{money(theirs[-1])}</p></div>
                    <div class="vs-stat"><p class="vs-stat-label">Dredge Silt, six years</p><p class="vs-stat-value">{money(ours[-1])}</p><p class="vs-stat-sub">Billed $50 yearly. {money(DREDGE_MONTH * 12 * YEARS)} if you pay monthly.</p></div>
                    <div class="vs-stat"><p class="vs-stat-label">You'd save with Dredge</p><p class="vs-stat-value">{money(theirs[-1] - ours[-1])}</p></div>
                </div>
                <div class="chart-card">
                    <div class="vs-legend">
                        <span><i class="key key-them"></i>{name} {plan}</span>
                        <span><i class="key key-us"></i>Dredge Silt</span>
                    </div>
                    <div class="vs-chart-wrap">
                        {chart(name, theirs, ours)}
                        <div class="vs-tip" hidden></div>
                    </div>
                    <details class="vs-table">
                        <summary>Show the numbers</summary>
                        <table class="compare-table compare-compact">
                            <thead><tr><th>Total by</th><th>{name} {plan}</th><th>Dredge Silt</th></tr></thead>
                            <tbody>
{years}
                            </tbody>
                        </table>
                    </details>
                </div>
                <p class="addon-note">{escape(p['cost_note'])} Dredge figures use Silt on yearly billing. Prices exclude tax.</p>
                <p class="addon-note">{name} prices checked {p['checked']} from <a href="{p['sources'][0][1]}" rel="noopener">its own pricing page</a>.
                Its intro price requires prepaying {p['term']} months.</p>
            </div>
        </section>

        <section class="section tint">
            <div class="wrap">
                <h2 class="section-title">Entry plans side by side</h2>
                <p class="plans-lead">{name} includes more storage, and often more sites, on its entry plan.
                Dredge keeps the same price at every renewal and includes email for as long as you host.</p>
                <div class="compare-wrap">
                <table class="compare-table compare-compact vs-compare">
                    <thead>
                        <tr><th></th><th>{name} {plan}</th><th>Dredge Silt</th></tr>
                    </thead>
                    <tbody>
{rows}
                    </tbody>
                </table>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="wrap">
                <div class="value-grid compare-fit">
                    <div class="value-card fit-card">
                        <h3>{name} is the better pick if</h3>
                        <ul class="fit-list">
{li(p['theirs'])}
                        </ul>
                    </div>
                    <div class="value-card fit-card fit-us">
                        <h3>Dredge is the better pick if</h3>
                        <ul class="fit-list">
{li(OURS)}
                        </ul>
                    </div>
                </div>
                <div class="hero-actions page-hero-actions">
                    <a class="btn btn-primary" href="pricing.html">See Dredge plans</a>
                    <a class="btn btn-ghost" href="why-dredge.html">How we compare in general</a>
                </div>
            </div>
        </section>

        <section class="section tint">
            <div class="wrap">
                <h2 class="section-title">More comparisons</h2>
                <div class="doc-grid">
{others}
                </div>
            </div>
        </section>

        <section class="section help-line">
            <div class="wrap">
                <p>{name} prices checked on {p['checked']}, from:</p>
                <ul class="source-list">
{src}
                </ul>
                <p>Their offers change often, so check their site before you decide. {name} is a trademark of
                its owner; Dredge Host isn't affiliated with it. Spotted something out of date? Email
                <a href="mailto:support@dredgehost.com">support@dredgehost.com</a> and we'll fix it.</p>
            </div>
        </section>
    </main>
    <!-- site-footer:start --><!-- site-footer:end -->
    <script src="assets/site.js"></script>
</body>
</html>
"""


SLIDER_START, SLIDER_END = "<!-- vs-slider:start -->", "<!-- vs-slider:end -->"


def slider(title, lead, more=""):
    """One slide per host, with arrows and dots, for the home and Why Dredge pages."""
    slides = []
    for i, (slug, p) in enumerate(HOSTS.items(), 1):
        six = cumulative(p["yearly"])[-1]
        jump = float(p["renew"][1:]) / float(p["intro"][1:])
        slides.append(f"""
                    <article class="vs-slide" id="vs-slide-{slug}" aria-roledescription="slide" aria-label="{i} of {len(HOSTS)}: {p['name']}">
                        <h3 class="vs-slide-title">Dredge vs {p['name']}</h3>
                        <div class="vs-slide-cols">
                            <div class="vs-slide-col">
                                <p class="jump-name">{p['name']} {p['plan']}</p>
                                <p class="jump-prices"><span>{p['intro']}</span><span class="jump-arrow" aria-hidden="true">&rarr;</span><strong>{p['renew']}</strong><span class="jump-per">/mo</span></p>
                                <p class="jump-tag jump-up">{jump:.1f}&times; at renewal</p>
                                <p class="vs-slide-six">{money(six)} over six years</p>
                            </div>
                            <div class="vs-slide-col vs-slide-us">
                                <p class="jump-name">Dredge Silt</p>
                                <p class="jump-prices"><span>$5</span><span class="jump-arrow" aria-hidden="true">&rarr;</span><strong>$5</strong><span class="jump-per">/mo</span></p>
                                <p class="jump-tag jump-same">Same price at renewal</p>
                                <p class="vs-slide-six">{money(DREDGE_YEAR * YEARS)} over six years, billed yearly at $50/yr</p>
                            </div>
                        </div>
                        <a class="vs-slide-link" href="dredge-vs-{slug}.html">Full comparison with {p['name']} &rarr;</a>
                    </article>""")
    months = sorted({" ".join(p["checked"].replace(",", "").split()[::2]) for p in HOSTS.values()})
    links = ", ".join(f'<a href="{p["sources"][0][1]}" rel="noopener">{p["name"]}</a>' for p in HOSTS.values())
    terms = sorted({p["term"] for p in HOSTS.values()})
    checked = (f'\n                <p class="plans-note">Prices checked {" and ".join(months)} from each host\'s own '
               f'pricing page: {links}. Intro prices usually require prepaying {terms[0]}&ndash;{terms[-1]} months. '
               f'Silt over six years is billed yearly, or {money(DREDGE_MONTH * 12 * YEARS)} if you pay monthly.</p>')
    dots = "".join(f'<button type="button" class="vs-dot-btn" aria-label="Show {p["name"]}" data-slide="{i}"></button>'
                   for i, p in enumerate(HOSTS.values()))
    return f"""
        <section class="section">
            <div class="wrap">
                <h2 class="section-title">{title}</h2>
                <p class="plans-lead">{lead}</p>
                <div class="vs-slider" aria-roledescription="carousel" aria-label="Price comparisons with other hosts">
                    <button type="button" class="vs-arrow vs-prev" aria-label="Previous host" hidden>&larr;</button>
                    <div class="vs-track" tabindex="0">{''.join(slides)}
                    </div>
                    <button type="button" class="vs-arrow vs-next" aria-label="Next host" hidden>&rarr;</button>
                    <div class="vs-dots" hidden>{dots}</div>
                </div>{checked}{more}
            </div>
        </section>
        """


def main():
    for slug, p in HOSTS.items():
        fn, text = page(slug, p)
        (SITE / fn).write_text(text)
        print(f"wrote {fn}")
    sliders = {
        "why-dredge.html": slider(
            "Compared with specific hosts",
            "Entry-plan prices at sign-up and at renewal, from each host's own website. "
            "Use the arrows to move between them."),
        "index.html": slider(
            "What you'd pay elsewhere",
            "Most big hosts advertise a low first-term price, then raise it at renewal. Here's their "
            "entry plan against Silt, from each host's own website.",
            '\n                <p class="plans-note plans-compare"><a href="why-dredge.html">'
            'See how we compare in more detail &rarr;</a></p>'),
    }
    for name, html in sliders.items():
        target = SITE / name
        text = target.read_text()
        start, end = text.index(SLIDER_START) + len(SLIDER_START), text.index(SLIDER_END)
        target.write_text(text[:start] + html + text[end:])
        print(f"updated {name}")


if __name__ == "__main__":
    main()
