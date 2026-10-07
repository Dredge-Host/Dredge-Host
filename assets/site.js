/* ============================================================
   Dredge Host — shared site script
   Injects the header + footer on every page, and wires up the
   mobile nav and the FAQ accordion.
   Pages set data-active on <body> to highlight the right nav link.
   Use data-root="" for root pages and data-root="../" for pages
   in subfolders so links and asset paths stay correct.
   ============================================================ */
(function () {
    'use strict';

    /* Privacy-friendly analytics (Plausible): no cookies, no personal data.
       The site must also be added at https://plausible.io. Blank disables it. */
    var PLAUSIBLE_DOMAIN = "dredgehost.com";

    var root = document.body.getAttribute('data-root') || '';
    var active = document.body.getAttribute('data-active') || '';
    var year = new Date().getFullYear();

    /* Load analytics only if a domain is configured. */
    if (PLAUSIBLE_DOMAIN) {
        var pl = document.createElement('script');
        pl.defer = true;
        pl.setAttribute('data-domain', PLAUSIBLE_DOMAIN);
        pl.src = 'https://plausible.io/js/script.js';
        document.head.appendChild(pl);
    }

    /* ---- Header ---- */
    var headerHTML =
        '<a class="skip-link" href="#main">Skip to content</a>' +
        '<header class="site-header">' +
          '<div class="wrap header-inner">' +
            '<a class="brand" href="' + (root || './') + '" aria-label="Dredge Host home">' +
              '<img src="' + root + 'assets/logo.png" alt="Dredge Host" class="brand-logo" width="296" height="150">' +
            '</a>' +
            '<nav class="site-nav" aria-label="Primary">' +
              '<a href="' + (root || './') + '#features"' + (active === 'features' ? ' aria-current="page"' : '') + '>Features</a>' +
              '<a href="' + root + 'pricing.html"' + (active === 'pricing' ? ' aria-current="page"' : '') + '>Pricing</a>' +
              '<a href="' + root + 'about.html"' + (active === 'about' ? ' aria-current="page"' : '') + '>About</a>' +
              '<a href="' + root + 'guides.html"' + (active === 'guides' ? ' aria-current="page"' : '') + '>Guides</a>' +
              '<a href="' + root + 'status.html"' + (active === 'status' ? ' aria-current="page"' : '') + '>Status</a>' +
              '<a class="nav-cta" href="' + root + 'pricing.html">Get started</a>' +
            '</nav>' +
            '<button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">' +
              '<span></span><span></span><span></span>' +
            '</button>' +
          '</div>' +
        '</header>';

    /* ---- Footer ---- */
    var footerHTML =
        '<footer class="site-footer">' +
          '<div class="wrap footer-inner">' +
            '<div class="footer-brand">' +
              '<img src="' + root + 'assets/logo-light.png" alt="Dredge Host" class="footer-logo" width="296" height="150">' +
              '<p class="footer-blurb">Independent cPanel hosting.</p>' +
            '</div>' +
            '<nav class="footer-links" aria-label="Footer">' +
              '<div class="footer-col">' +
                '<span class="footer-head">Product</span>' +
                '<a href="' + (root || './') + '#features">Features</a>' +
                '<a href="' + root + 'pricing.html">Pricing</a>' +
                '<a href="' + root + 'status.html">Status</a>' +
                '<a href="' + root + 'guides.html">Guides</a>' +
              '</div>' +
              '<div class="footer-col">' +
                '<span class="footer-head">Company</span>' +
                '<a href="' + root + 'about.html">About</a>' +
                '<a href="' + root + 'why-dredge.html">Why Dredge</a>' +
                '<a href="' + root + 'contact.html">Contact</a>' +
              '</div>' +
              '<div class="footer-col">' +
                '<span class="footer-head">Legal</span>' +
                '<a href="' + root + 'privacy.html">Privacy</a>' +
                '<a href="' + root + 'terms.html">Terms</a>' +
                '<a href="' + root + 'aup.html">Acceptable Use</a>' +
                '<a href="' + root + 'refunds.html">Refunds</a>' +
              '</div>' +
              '<div class="footer-col">' +
                '<span class="footer-head">Connect</span>' +
                '<a href="mailto:support@dredgehost.com">Email</a>' +
                '<a href="https://github.com/Dredge-Host" rel="noopener">GitHub</a>' +
                '<a href="https://x.com/DredgeHost" rel="noopener">X (Twitter)</a>' +
                '<a href="https://osm.pm/i/HvWItOqDiLXq1VhB" rel="noopener">Osmium Support</a>' +
              '</div>' +
            '</nav>' +
          '</div>' +
          '<div class="wrap footer-payment">' +
            '<p>We accept Visa, Mastercard, Amex, Discover, Apple Pay &amp; Google Pay via Stripe.</p>' +
          '</div>' +
          '<div class="wrap footer-bottom">' +
            '<p>&copy; ' + year + ' Dredge Host</p>' +
            '<p><a href="mailto:support@dredgehost.com">support@dredgehost.com</a></p>' +
          '</div>' +
        '</footer>';

    /* ---- Promo banner ---- */
    var promoHTML = '';
    var promoDismissed = false;
    try { promoDismissed = localStorage.getItem('promo_early35') === '1'; } catch (e) {}
    if (!promoDismissed) {
        promoHTML =
            '<div class="promo-banner" role="status">' +
              '35% off your first month — use code ' +
              '<span class="promo-code">EARLY35</span> at checkout.' +
              ' <a class="promo-cta" href="' + root + 'pricing.html">See plans &rarr;</a>' +
              '<button class="promo-close" aria-label="Dismiss">&times;</button>' +
            '</div>';
    }

    /* ---- Inject ---- */
    var headerMount = document.getElementById('site-header');
    var footerMount = document.getElementById('site-footer');
    if (headerMount) headerMount.outerHTML = headerHTML + promoHTML;
    if (footerMount) footerMount.outerHTML = footerHTML;

    /* ---- Mobile nav toggle ---- */
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');
    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            var open = nav.classList.toggle('open');
            toggle.setAttribute('aria-expanded', String(open));
        });
        nav.addEventListener('click', function (e) {
            if (e.target.tagName === 'A') {
                nav.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    /* ---- Promo dismiss ---- */
    var promoClose = document.querySelector('.promo-close');
    if (promoClose) {
        promoClose.addEventListener('click', function () {
            var banner = document.querySelector('.promo-banner');
            if (banner) banner.remove();
            try { localStorage.setItem('promo_early35', '1'); } catch (e) {}
        });
    }

    /* ---- FAQ accordion ---- */
    var faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(function (item) {
        var q = item.querySelector('.faq-q');
        if (!q) return;
        q.addEventListener('click', function () {
            var open = item.classList.toggle('open');
            q.setAttribute('aria-expanded', String(open));
        });
    });
})();
