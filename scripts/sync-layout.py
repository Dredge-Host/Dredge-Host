#!/usr/bin/env python3
"""Write the shared header and footer into every page. Edit them here, then run:
    python3 scripts/sync-layout.py
"""
import datetime
import json
import pathlib
import re
from html import escape, unescape

SITE = pathlib.Path(__file__).resolve().parent.parent

HEADER_START, HEADER_END = "<!-- site-header:start -->", "<!-- site-header:end -->"
FOOTER_START, FOOTER_END = "<!-- site-footer:start -->", "<!-- site-footer:end -->"


def header(root, active):
    home = root or "./"

    def nav(href, key, label):
        current = ' aria-current="page"' if active == key else ""
        return f'<a href="{href}"{current}>{label}</a>'

    return (
        '<a class="skip-link" href="#main">Skip to content</a>'
        '<header class="site-header">'
        '<div class="wrap header-inner">'
        f'<a class="brand" href="{home}" aria-label="Dredge Host home">'
        f'<img src="{root}assets/logo.png" alt="Dredge Host" class="brand-logo" width="296" height="150">'
        '</a>'
        '<nav class="site-nav" aria-label="Primary">'
        + nav(f"{home}#features", "features", "Features")
        + nav(f"{root}pricing.html", "pricing", "Pricing")
        + nav(f"{root}about.html", "about", "About")
        + nav(f"{root}guides.html", "guides", "Guides")
        + nav(f"{root}status.html", "status", "Status")
        + '<a href="https://my.dredgehost.com/clientarea.php">Log in</a>'
        + f'<a class="nav-cta" href="{root}pricing.html">Get started</a>'
        '</nav>'
        '<button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">'
        '<span></span><span></span><span></span>'
        '</button>'
        '</div>'
        '</header>'
    )


def footer(root):
    home = root or "./"
    year = datetime.date.today().year
    return (
        '<footer class="site-footer">'
        '<div class="wrap footer-inner">'
        '<div class="footer-brand">'
        f'<img src="{root}assets/logo-light.png" alt="Dredge Host" class="footer-logo" width="296" height="150">'
        '<p class="footer-blurb">Independent cPanel hosting.</p>'
        '</div>'
        '<nav class="footer-links" aria-label="Footer">'
        '<div class="footer-col">'
        '<span class="footer-head">Product</span>'
        f'<a href="{home}#features">Features</a>'
        f'<a href="{root}pricing.html">Pricing</a>'
        f'<a href="{root}status.html">Status</a>'
        f'<a href="{root}guides.html">Guides</a>'
        '<a href="https://my.dredgehost.com/clientarea.php">Client area</a>'
        '</div>'
        '<div class="footer-col">'
        '<span class="footer-head">Company</span>'
        f'<a href="{root}about.html">About</a>'
        f'<a href="{root}why-dredge.html">Why Dredge</a>'
        f'<a href="{root}contact.html">Contact</a>'
        '</div>'
        '<div class="footer-col">'
        '<span class="footer-head">Legal</span>'
        f'<a href="{root}privacy.html">Privacy</a>'
        f'<a href="{root}terms.html">Terms</a>'
        f'<a href="{root}aup.html">Acceptable Use</a>'
        f'<a href="{root}refunds.html">Refunds</a>'
        '</div>'
        '<div class="footer-col">'
        '<span class="footer-head">Connect</span>'
        '<a href="mailto:support@dredgehost.com">Email</a>'
        '<a href="https://x.com/DredgeHost" rel="noopener">X (Twitter)</a>'
        '<a href="https://osm.pm/i/HvWItOqDiLXq1VhB" rel="noopener">Osmium community</a>'
        '<a href="https://www.trustpilot.com/review/dredgehost.com" rel="noopener">Trustpilot</a>'
        '</div>'
        '</nav>'
        '</div>'
        '<div class="wrap footer-payment">'
        '<p>We accept Visa, Mastercard, Amex, Discover, Apple&nbsp;Pay &amp; Google&nbsp;Pay via Stripe.</p>'
        '</div>'
        '<div class="wrap footer-bottom">'
        f'<p>&copy; <span class="footer-year">{year}</span> Dredge Host</p>'
        '<p><a href="mailto:support@dredgehost.com">support@dredgehost.com</a></p>'
        '</div>'
        '</footer>'
    )


ARTICLE_START, ARTICLE_END = "<!-- article-schema:start -->", "<!-- article-schema:end -->"


def article_schema(html):
    def find(pattern):
        match = re.search(pattern, html, re.S)
        if not match:
            raise ValueError(f"guide is missing {pattern}")
        return unescape(match.group(1).strip())

    data = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": find(r"<h1>(.*?)</h1>"),
        "description": find(r'<meta name="description" content="([^"]*)"'),
        "image": find(r'<meta property="og:image" content="([^"]*)"'),
        "mainEntityOfPage": find(r'<link rel="canonical" href="([^"]*)"'),
        "dateModified": find(r'<time datetime="([^"]*)"'),
        "author": {"@type": "Organization", "name": "Dredge Host", "url": "https://dredgehost.com/"},
        "publisher": {
            "@type": "Organization",
            "name": "Dredge Host",
            "logo": {"@type": "ImageObject", "url": "https://dredgehost.com/assets/dredge-app-tile-512.png"},
        },
    }
    body = json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")
    return f'\n    <script type="application/ld+json">\n{body}\n    </script>\n    '


def replace_block(html, start, end, placeholder, content, where="replace"):
    """Swap the content between start/end markers. On first run, put the block in place of
    the placeholder, or just before/after it."""
    block = f"{start}{content}{end}"
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.S)
    if pattern.search(html):
        return pattern.sub(lambda _: block, html, count=1)
    if placeholder not in html:
        raise ValueError(f"no {start} block or {placeholder} placeholder")
    new = {"replace": block, "before": block + "\n" + placeholder, "after": placeholder + block}[where]
    return html.replace(placeholder, new, 1)


TOC_START, TOC_END = "<!-- toc:start -->", "<!-- toc:end -->"
PAGER_START, PAGER_END = "<!-- guide-pager:start -->", "<!-- guide-pager:end -->"
PROSE_OPEN = '<div class="wrap prose">'
TOC_MIN_MINUTES = 4


def plain(fragment):
    return unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def add_heading_ids(html):
    """Give each plain <h2> in a guide a stable id so it can be linked to."""
    used = set(re.findall(r'<h2 id="([^"]+)"', html))

    def add_id(match):
        slug = re.sub(r"[^a-z0-9]+", "-", plain(match.group(1)).lower()).strip("-")
        candidate, n = slug, 2
        while candidate in used:
            candidate, n = f"{slug}-{n}", n + 1
        used.add(candidate)
        return f'<h2 id="{candidate}">{match.group(1)}</h2>'

    return re.sub(r"<h2>(.*?)</h2>", add_id, html, flags=re.S)


def toc(html):
    minutes = int(re.search(r'class="page-meta">(\d+) min read', html).group(1))
    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html, re.S)
    if minutes < TOC_MIN_MINUTES or len(headings) < 3:
        return ""
    items = "".join(f'<li><a href="#{hid}">{escape(plain(text))}</a></li>' for hid, text in headings)
    return f'<nav class="toc" aria-label="On this page"><p class="toc-title">On this page</p><ol>{items}</ol></nav>'


def guide_topics():
    """Guides grouped by topic, in the order they appear on guides.html."""
    index = (SITE / "guides.html").read_text()
    cards = re.findall(
        r'<a class="doc-card guide-card" href="guides/([a-z0-9-]+)\.html" data-cat="([a-z]+)">.*?<h3>(.*?)</h3>',
        index, re.S)
    topics = {}
    for slug, cat, title in cards:
        topics.setdefault(cat, []).append((slug, title))
    return topics


def pager(slug, topics):
    for guides in topics.values():
        slugs = [s for s, _ in guides]
        if slug not in slugs:
            continue
        i = slugs.index(slug)
        links = ""
        if i > 0:
            prev_slug, prev_title = guides[i - 1]
            links += (f'<a class="pager-prev" href="{prev_slug}.html">'
                      f'<span class="pager-label">&larr; Previous</span>{prev_title}</a>')
        if i < len(guides) - 1:
            next_slug, next_title = guides[i + 1]
            links += (f'<a class="pager-next" href="{next_slug}.html">'
                      f'<span class="pager-label">Next &rarr;</span>{next_title}</a>')
        return f'<nav class="guide-pager" aria-label="More guides on this topic">{links}</nav>' if links else ""
    return ""


def main():
    pages = sorted(SITE.glob("*.html")) + sorted(SITE.glob("guides/*.html"))
    topics = guide_topics()
    for page in pages:
        html = page.read_text()
        body = re.search(r'<body data-root="([^"]*)" data-active="([^"]*)"', html)
        if not body:
            raise ValueError(f"{page}: <body> is missing data-root/data-active")
        root, active = body.groups()
        new = replace_block(html, HEADER_START, HEADER_END, '<div id="site-header"></div>', header(root, active))
        new = replace_block(new, FOOTER_START, FOOTER_END, '<div id="site-footer"></div>', footer(root))
        if page.parent.name == "guides":
            new = replace_block(new, ARTICLE_START, ARTICLE_END, "</head>", article_schema(new), where="before")
            new = add_heading_ids(new)
            new = replace_block(new, TOC_START, TOC_END, PROSE_OPEN, toc(new), where="after")
            new = replace_block(new, PAGER_START, PAGER_END, '<p class="guide-back">',
                                pager(page.stem, topics), where="before")
        if new != html:
            page.write_text(new)
            print(f"updated {page.relative_to(SITE)}")


if __name__ == "__main__":
    main()
