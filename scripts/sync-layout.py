#!/usr/bin/env python3
"""Write the shared header and footer into every page. Edit them here, then run:
    python3 scripts/sync-layout.py
"""
import datetime
import pathlib
import re

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
        '<a href="https://github.com/Dredge-Host" rel="noopener">GitHub</a>'
        '<a href="https://x.com/DredgeHost" rel="noopener">X (Twitter)</a>'
        '<a href="https://osm.pm/i/HvWItOqDiLXq1VhB" rel="noopener">Osmium Support</a>'
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


def replace_block(html, start, end, placeholder, content):
    block = f"{start}{content}{end}"
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.S)
    if pattern.search(html):
        return pattern.sub(lambda _: block, html, count=1)
    if placeholder in html:
        return html.replace(placeholder, block, 1)
    raise ValueError(f"no {start} block or {placeholder} placeholder")


def main():
    pages = sorted(SITE.glob("*.html")) + sorted(SITE.glob("guides/*.html"))
    for page in pages:
        html = page.read_text()
        body = re.search(r'<body data-root="([^"]*)" data-active="([^"]*)"', html)
        if not body:
            raise ValueError(f"{page}: <body> is missing data-root/data-active")
        root, active = body.groups()
        new = replace_block(html, HEADER_START, HEADER_END, '<div id="site-header"></div>', header(root, active))
        new = replace_block(new, FOOTER_START, FOOTER_END, '<div id="site-footer"></div>', footer(root))
        if new != html:
            page.write_text(new)
            print(f"updated {page.relative_to(SITE)}")


if __name__ == "__main__":
    main()
