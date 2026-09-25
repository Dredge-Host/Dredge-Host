/* ============================================================
   Dredge Host — shared site script
   Injects the header + footer on every page, wires up nav,
   scroll reveals, the notify form, and the current year.
   Pages set data-active on <body> to highlight the right nav link.
   Use data-root="" for root pages and data-root="../" for pages
   in subfolders so links and asset paths stay correct.
   ============================================================ */
(function () {
    'use strict';

    /* ============================================================
       CONFIG — edit these two lines after you create the forms.
       1. Make a free account at https://formspree.io
       2. Create a form, copy its endpoint (looks like
          https://formspree.io/f/abcdwxyz)
       3. Paste the "abcdwxyz" part below (the form ID).
       Leave as "" to keep the site in demo mode (validates and shows
       a success message locally, but does not send anywhere).
       ============================================================ */
    var NOTIFY_FORM_ID  = "";   // e.g. "abcdwxyz"  -> notify / signup form
    var CONTACT_FORM_ID = "";   // e.g. "wxyzabcd"  -> contact page form
    var FORMSPREE = "https://formspree.io/f/";

    /* Optional: privacy-friendly analytics (Plausible). Leave blank to disable.
       Set to your live domain, e.g. "dredgehost.com", after you add
       the site at https://plausible.io — no cookies, no personal data. */
    var PLAUSIBLE_DOMAIN = "";

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
              '<img src="' + root + 'assets/logo-horizontal.png" alt="Dredge Host" class="brand-logo">' +
            '</a>' +
            '<nav class="site-nav" aria-label="Primary">' +
              '<a href="' + (root || './') + '#features"' + (active === 'features' ? ' aria-current="page"' : '') + '>Features</a>' +
              '<a href="' + root + 'pricing.html"' + (active === 'pricing' ? ' aria-current="page"' : '') + '>Pricing</a>' +
              '<a href="' + root + 'about.html"' + (active === 'about' ? ' aria-current="page"' : '') + '>About</a>' +
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
              '<img src="' + root + 'assets/logo-horizontal-light.png" alt="Dredge Host" class="footer-logo">' +
              '<p class="footer-blurb">Fast, honest, independent web hosting. Every limit published.</p>' +
            '</div>' +
            '<nav class="footer-links" aria-label="Footer">' +
              '<div class="footer-col">' +
                '<span class="footer-head">Product</span>' +
                '<a href="' + (root || './') + '#features">Features</a>' +
                '<a href="' + root + 'pricing.html">Pricing</a>' +
                '<a href="' + root + 'status.html">Status</a>' +
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

    /* ---- Notify form ---- */
    var form = document.getElementById('notifyForm');
    var status = document.getElementById('notifyStatus');
    if (form && status) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var input = form.querySelector('input[type="email"]');
            var value = (input.value || '').trim();
            var valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

            if (!valid) {
                status.textContent = 'That email doesn\u2019t look right \u2014 mind checking it?';
                status.className = 'notify-status err';
                input.focus();
                return;
            }

            // Demo mode: no endpoint configured yet.
            if (!NOTIFY_FORM_ID) {
                status.textContent = 'Thanks \u2014 you\u2019re signed up.';
                status.className = 'notify-status ok';
                form.reset();
                return;
            }

            // Live mode: POST to Formspree.
            var btn = form.querySelector('button[type="submit"]');
            var label = btn ? btn.textContent : '';
            if (btn) { btn.disabled = true; btn.textContent = 'Sending\u2026'; }
            status.textContent = '';
            status.className = 'notify-status';

            fetch(FORMSPREE + NOTIFY_FORM_ID, {
                method: 'POST',
                headers: { 'Accept': 'application/json' },
                body: new FormData(form)
            }).then(function (res) {
                if (res.ok) {
                    // Prefer a dedicated thank-you page if present.
                    window.location.href = root + 'thanks.html';
                } else {
                    return res.json().then(function (data) {
                        var msg = (data && data.errors && data.errors.length)
                            ? data.errors.map(function (x) { return x.message; }).join(', ')
                            : 'Something went wrong. Please try again, or email support@dredgehost.com.';
                        throw new Error(msg);
                    });
                }
            }).catch(function (err) {
                status.textContent = err.message || 'Network error \u2014 please try again.';
                status.className = 'notify-status err';
                if (btn) { btn.disabled = false; btn.textContent = label; }
            });
        });
    }

    /* ---- Contact form ---- */
    var cform = document.getElementById('contactForm');
    var cstatus = document.getElementById('contactStatus');
    if (cform && cstatus) {
        cform.addEventListener('submit', function (e) {
            e.preventDefault();
            var name = (cform.querySelector('#cname').value || '').trim();
            var email = (cform.querySelector('#cemail').value || '').trim();
            var msg = (cform.querySelector('#cmsg').value || '').trim();
            var okEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

            if (!name || !okEmail || !msg) {
                cstatus.textContent = 'Please fill in your name, a valid email, and a message.';
                cstatus.className = 'form-status err';
                return;
            }

            if (!CONTACT_FORM_ID) {
                cstatus.textContent = 'Thanks \u2014 your message is ready to send. (Demo mode \u2014 add a Formspree ID to deliver it.)';
                cstatus.className = 'form-status ok';
                cform.reset();
                return;
            }

            var btn = cform.querySelector('button[type="submit"]');
            var label = btn ? btn.textContent : '';
            if (btn) { btn.disabled = true; btn.textContent = 'Sending\u2026'; }
            cstatus.textContent = '';
            cstatus.className = 'form-status';

            fetch(FORMSPREE + CONTACT_FORM_ID, {
                method: 'POST',
                headers: { 'Accept': 'application/json' },
                body: new FormData(cform)
            }).then(function (res) {
                if (res.ok) {
                    cstatus.textContent = 'Thanks \u2014 your message is on its way. We\u2019ll reply by email.';
                    cstatus.className = 'form-status ok';
                    cform.reset();
                } else {
                    return res.json().then(function (data) {
                        var m = (data && data.errors && data.errors.length)
                            ? data.errors.map(function (x) { return x.message; }).join(', ')
                            : 'Something went wrong. Please try again, or email support@dredgehost.com.';
                        throw new Error(m);
                    });
                }
            }).catch(function (err) {
                cstatus.textContent = err.message || 'Network error \u2014 please try again.';
                cstatus.className = 'form-status err';
                if (btn) { btn.disabled = false; btn.textContent = label; }
            });
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
