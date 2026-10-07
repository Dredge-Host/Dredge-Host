# Dredge Host

The website for [Dredge Host](https://dredgehost.com), a small, independent cPanel web hosting company.

Every plan includes cPanel, SSD storage, free HTTPS certificates, email on your own domain, one-click WordPress, and support from the people who run the platform.

| Plan | Price | Sites | SSD storage | Transfer / month |
|------|-------|-------|-------------|------------------|
| Silt | $5/mo | 1 | 2 GB | 50 GB |
| Channel | $12/mo | 5 | 6 GB | 150 GB |
| Harbor | $25/mo | 15 | 15 GB | 300 GB |

Sign up and manage your account at [my.dredgehost.com](https://my.dredgehost.com). Questions go to [support@dredgehost.com](mailto:support@dredgehost.com).

## Guides

Step-by-step help for new customers lives at [dredgehost.com/guides.html](https://dredgehost.com/guides.html):

- Find your way around your client area and cPanel
- Buy a domain from Porkbun or Namecheap and connect it
- Add a subdomain
- Install WordPress in one click
- Move a WordPress site to Dredge
- Set up email on your domain
- Upload a website with File Manager or FTP
- Turn on HTTPS everywhere
- Back up and restore your site

## How the site is built

Plain HTML and CSS with no build step, served by GitHub Pages from the `main` branch.

- `*.html`: top-level pages (home, pricing, about, guides, status, contact, and legal pages)
- `guides/`: one page per guide
- `style.css`: the whole stylesheet
- `scripts/sync-layout.py`: the shared header and footer. Every page has a copy between `<!-- site-header:start -->` / `<!-- site-footer:start -->` markers, so edit the script and run `python3 scripts/sync-layout.py` to update them all. Each page sets `data-active` on `<body>` to highlight its nav link, and `data-root="../"` for pages inside a subfolder.
- `assets/site.js`: adds the promo banner, keeps the footer year current, and runs the mobile menu and FAQ accordions.
- `assets/`: logo, favicons, and social preview image

To preview locally, run `python3 -m http.server` in this folder and open http://localhost:8000.
