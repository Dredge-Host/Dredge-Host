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

    /* ---- Monthly / yearly switch on the plan cards ---- */
    document.querySelectorAll('.billing-toggle').forEach(function (group) {
        var scope = group.parentNode;
        group.hidden = false;
        group.addEventListener('click', function (e) {
            var button = e.target.closest('button[data-cycle]');
            if (!button) return;
            var cycle = button.getAttribute('data-cycle');
            group.querySelectorAll('button').forEach(function (b) {
                b.setAttribute('aria-pressed', String(b === button));
            });
            scope.querySelectorAll('[data-' + cycle + ']').forEach(function (el) {
                el.textContent = el.getAttribute('data-' + cycle);
            });
            scope.querySelectorAll('[data-' + cycle + '-href]').forEach(function (el) {
                el.href = el.getAttribute('data-' + cycle + '-href');
            });
        });
    });

    /* ---- Comparison charts: crosshair and tooltip per year ---- */
    document.querySelectorAll('.vs-chart-wrap').forEach(function (wrap) {
        var svg = wrap.querySelector('svg');
        var tip = wrap.querySelector('.vs-tip');
        var cursor = svg.querySelector('.vs-cursor');
        var names = Array.prototype.map.call(
            wrap.closest('.chart-card').querySelectorAll('.vs-legend span'),
            function (el) { return el.textContent.trim(); });
        function show(hit) {
            var x = hit.getAttribute('data-x');
            cursor.setAttribute('x1', x); cursor.setAttribute('x2', x);
            cursor.style.opacity = 1;
            tip.innerHTML = '<strong>Total by year ' + hit.getAttribute('data-year') + '</strong>' +
                '<i class="key key-them"></i>' + names[0] + ': ' + hit.getAttribute('data-them') + '<br>' +
                '<i class="key key-us"></i>' + names[1] + ': ' + hit.getAttribute('data-us');
            tip.hidden = false;
            var scale = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
            var left = x * scale + 12;
            if (left + tip.offsetWidth > wrap.clientWidth) left = x * scale - tip.offsetWidth - 12;
            tip.style.left = Math.max(0, left) + 'px';
        }
        function hide() { cursor.style.opacity = 0; tip.hidden = true; }
        svg.querySelectorAll('.vs-hit').forEach(function (hit) {
            hit.addEventListener('pointerenter', function () { show(hit); });
        });
        svg.addEventListener('pointerleave', hide);
    });

    /* ---- Slider of comparisons on the Why Dredge page ---- */
    document.querySelectorAll('.vs-slider').forEach(function (slider) {
        var track = slider.querySelector('.vs-track');
        var slides = track.querySelectorAll('.vs-slide');
        var prev = slider.querySelector('.vs-prev');
        var next = slider.querySelector('.vs-next');
        var dots = slider.querySelectorAll('.vs-dot-btn');
        [prev, next, slider.querySelector('.vs-dots')].forEach(function (el) { el.hidden = false; });
        function current() {
            var best = 0;
            slides.forEach(function (s, n) {
                if (Math.abs(s.offsetLeft - track.scrollLeft) < Math.abs(slides[best].offsetLeft - track.scrollLeft)) best = n;
            });
            return best;
        }
        function go(i) {
            i = Math.max(0, Math.min(slides.length - 1, i));
            track.scrollTo({ left: slides[i].offsetLeft });
        }
        function update() {
            var i = current();
            prev.disabled = i === 0;
            next.disabled = i === slides.length - 1;
            dots.forEach(function (d, n) { d.setAttribute('aria-current', String(n === i)); });
        }
        prev.addEventListener('click', function () { go(current() - 1); });
        next.addEventListener('click', function () { go(current() + 1); });
        dots.forEach(function (d) {
            d.addEventListener('click', function () { go(Number(d.getAttribute('data-slide'))); });
        });
        track.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowRight') { e.preventDefault(); go(current() + 1); }
            if (e.key === 'ArrowLeft') { e.preventDefault(); go(current() - 1); }
        });
        track.addEventListener('scroll', update);
        window.addEventListener('resize', update);
        update();
    });

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
