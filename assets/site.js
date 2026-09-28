/* ============================================================
   Dredge Host — shared site script
   Injects the header + footer on every page, wires up nav,
   scroll reveals, the FAQ accordion, and the current year.
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
              '<a class="nav-cta" href="' + (root || './') + '#get-started">Get started</a>' +
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
              '<p class="footer-blurb">Fast, honest, independent web hosting. Every limit published.</p>' +
            '</div>' +
            '<nav class="footer-links" aria-label="Footer">' +
              '<div class="footer-col">' +
                '<span class="footer-head">Product</span>' +
                '<a href="' + (root || './') + '#features">Features</a>' +
                '<a href="' + root + 'pricing.html">Pricing</a>' +
                '<a href="' + root + 'status.html">Status</a>' +
                '<a href="' + root + 'guides.html">Guides</a>' +
                '<a href="' + (root || './') + '#get-started">Get started</a>' +
              '</div>' +
              '<div class="footer-col">' +
                '<span class="footer-head">Company</span>' +
                '<a href="' + root + 'about.html">About</a>' +
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
                '<a href="https://dredgehost.com/">Website</a>' +
                '<a href="https://github.com/Dredge-Host" rel="noopener">GitHub</a>' +
              '</div>' +
            '</nav>' +
          '</div>' +
          '<div class="wrap footer-bottom">' +
            '<p>&copy; ' + year + ' Dredge Host. All rights reserved.</p>' +
            '<p class="footer-status"><span class="dot"></span> <a href="' + root + 'status.html" style="color:inherit;">All systems operational</a></p>' +
          '</div>' +
        '</footer>';

    /* ---- Inject ---- */
    var headerMount = document.getElementById('site-header');
    var footerMount = document.getElementById('site-footer');
    if (headerMount) headerMount.outerHTML = headerHTML;
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

    /* ---- Scroll reveal ---- */
    var revealTargets = document.querySelectorAll(
        '.feature, .plan-card, .about-copy, .section-title, .notify-inner, ' +
        '.reveal-me, .doc-card, .post-card, .faq-item, .status-row, .value-card'
    );
    revealTargets.forEach(function (el) { el.classList.add('reveal'); });

    if ('IntersectionObserver' in window && revealTargets.length) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        revealTargets.forEach(function (el) { io.observe(el); });
    } else {
        revealTargets.forEach(function (el) { el.classList.add('in'); });
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
