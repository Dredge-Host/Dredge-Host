/* ============================================================
   Dredge Host — shared site script
   Adds the promo banner, keeps the footer year current, and wires up
   the mobile nav and the FAQ accordion. The header and footer markup
   itself lives in each page; edit scripts/sync-layout.py and run it.
   ============================================================ */
(function () {
    'use strict';

    /* Privacy-friendly analytics (Plausible): no cookies, no personal data.
       The site must also be added at https://plausible.io. Blank disables it. */
    var PLAUSIBLE_DOMAIN = "dredgehost.com";

    var root = document.body.getAttribute('data-root') || '';

    /* Load analytics only if a domain is configured. */
    if (PLAUSIBLE_DOMAIN) {
        var pl = document.createElement('script');
        pl.defer = true;
        pl.setAttribute('data-domain', PLAUSIBLE_DOMAIN);
        pl.src = 'https://plausible.io/js/script.outbound-links.js';
        document.head.appendChild(pl);
    }

    /* ---- Promo banner ---- */
    var promoHTML = '';
    var promoEnds = new Date('2027-01-01T00:00:00-05:00');
    var promoDismissed = false;
    try { promoDismissed = localStorage.getItem('promo_early35') === '1'; } catch (e) {}
    if (!promoDismissed && new Date() < promoEnds) {
        promoHTML =
            '<div class="promo-banner" role="status">' +
              '35% off your first order<span class="promo-long"> — use code</span><span class="promo-short">:</span> ' +
              '<span class="promo-code">EARLY35</span><span class="promo-long"> at checkout. Ends Dec&nbsp;31.</span>' +
              ' <a class="promo-cta" href="' + root + 'pricing.html">See&nbsp;plans&nbsp;&rarr;</a>' +
              '<button class="promo-close" aria-label="Dismiss">&times;</button>' +
            '</div>';
    }

    var siteHeader = document.querySelector('.site-header');
    if (siteHeader && promoHTML) siteHeader.insertAdjacentHTML('afterend', promoHTML);

    var footerYear = document.querySelector('.footer-year');
    if (footerYear) footerYear.textContent = new Date().getFullYear();

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

    /* ---- Copy buttons on code blocks ---- */
    if (navigator.clipboard) {
        document.querySelectorAll('.prose pre').forEach(function (pre) {
            var wrap = document.createElement('div');
            wrap.className = 'code-block';
            pre.parentNode.insertBefore(wrap, pre);
            wrap.appendChild(pre);
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'copy-btn';
            btn.textContent = 'Copy';
            btn.addEventListener('click', function () {
                navigator.clipboard.writeText(pre.textContent).then(function () {
                    btn.textContent = 'Copied';
                    setTimeout(function () { btn.textContent = 'Copy'; }, 2000);
                });
            });
            wrap.appendChild(btn);
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
