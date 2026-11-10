/* GONI static website: settings, consent, analytics, tracking and the inquiry form. No dependencies. */

// ---------- Settings: replace before launch ----------
var WHATSAPP_NUMBER = '6281200000000';  // international format, no plus sign
var DEMO_MODE = true;                   // false removes the sample-data banner
var GA_ID = '';                         // GA4 measurement ID, for example 'G-XXXXXXXXXX'. Empty = analytics off
var CLARITY_ID = '';                    // optional Microsoft Clarity project ID for heatmaps. Empty = off
var INQUIRY_ENDPOINT = '/api/inquiry';  // Cloudflare Pages Function in functions/api/inquiry.js

(function () {
  'use strict';

  // ---------- Text in each language (page language comes from <html lang>) ----------
  var LANG = document.documentElement.lang === 'id' ? 'id' : 'en';
  var TXT = {
    en: {
      demo: 'Proposal mockup. Prices, volumes, names and statistics are sample data and will be replaced with real company data.',
      consent: 'We use analytics cookies to understand which pages are useful. Nothing is collected unless you accept.',
      privacy: 'Privacy Policy', privacyHref: '/privacy-policy/', accept: 'Accept', decline: 'Decline', consentLabel: 'Cookie preferences',
      send: 'Send Inquiry', sending: 'Sending...',
      ok: 'Thank you. Your inquiry has been sent and our team will reply within one business day.',
      fail: 'The form could not be sent right now. Please send the same details by WhatsApp: ', openWa: 'Open WhatsApp',
      waIntro: 'Hello GONI, I would like to discuss a product project.', name: 'Name', wa: 'WhatsApp', cat: 'Category',
      vol: 'Estimated first order', idea: 'Product idea',
      cta: '/contact/'
    },
    id: {
      demo: 'Contoh untuk proposal. Harga, volume, nama, dan statistik adalah data contoh dan akan diganti dengan data asli perusahaan.',
      consent: 'Kami memakai cookie analitik untuk memahami halaman mana yang bermanfaat. Tidak ada data yang dikumpulkan kecuali Anda menyetujui.',
      privacy: 'Kebijakan Privasi', privacyHref: '/id/kebijakan-privasi/', accept: 'Setuju', decline: 'Tolak', consentLabel: 'Preferensi cookie',
      send: 'Kirim Permintaan', sending: 'Mengirim...',
      ok: 'Terima kasih. Permintaan Anda sudah terkirim dan tim kami akan membalas dalam satu hari kerja.',
      fail: 'Formulir belum bisa dikirim saat ini. Silakan kirim data yang sama lewat WhatsApp: ', openWa: 'Buka WhatsApp',
      waIntro: 'Halo GONI, saya ingin berdiskusi tentang proyek produk.', name: 'Nama', wa: 'WhatsApp', cat: 'Kategori',
      vol: 'Perkiraan pesanan pertama', idea: 'Ide produk',
      cta: '/id/kontak/'
    }
  }[LANG];

  // ---------- Small helpers ----------
  function store(key, val) {
    try {
      if (val === undefined) return window.localStorage.getItem(key);
      window.localStorage.setItem(key, val);
    } catch (e) { /* storage blocked */ }
    return null;
  }
  function session(key, val) {
    try {
      if (val === undefined) return window.sessionStorage.getItem(key);
      window.sessionStorage.setItem(key, val);
    } catch (e) { /* storage blocked */ }
    return null;
  }
  function waUrl(text) {
    return 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(text);
  }

  // ---------- Demo banner ----------
  if (DEMO_MODE) {
    var banner = document.createElement('div');
    banner.className = 'demo-banner';
    banner.textContent = TXT.demo;
    document.body.insertBefore(banner, document.body.firstChild);
  }

  // ---------- Mobile navigation ----------
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ---------- Footer year ----------
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // The Contact page has its own WhatsApp button, so the floating one would overlap the form.
  if (location.pathname.indexOf(TXT.cta) === 0) {
    var floatBtn = document.querySelector('.wa-float');
    if (floatBtn) floatBtn.remove();
  }

  // ---------- WhatsApp links ----------
  document.querySelectorAll('[data-wa]').forEach(function (a) {
    a.href = waUrl(a.getAttribute('data-wa') || '');
    a.target = '_blank';
    a.rel = 'noopener';
  });

  // ---------- Campaign source (UTM) ----------
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  (function captureUtm() {
    var params = new URLSearchParams(location.search);
    var found = {};
    UTM_KEYS.forEach(function (k) { if (params.get(k)) found[k] = params.get(k).slice(0, 100); });
    if (Object.keys(found).length) session('goni_utm', JSON.stringify(found));
    if (!session('goni_ref') && document.referrer) {
      try { session('goni_ref', new URL(document.referrer).hostname); } catch (e) { /* ignore */ }
    }
  })();
  function readUtm() {
    try { return JSON.parse(session('goni_utm') || '{}'); } catch (e) { return {}; }
  }

  // ---------- Analytics (loaded only after consent) ----------
  var analyticsLoaded = false;
  function consentGranted() { return store('goni_consent') === 'granted'; }

  function loadAnalytics() {
    if (analyticsLoaded || !consentGranted()) return;
    analyticsLoaded = true;
    if (GA_ID) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
      document.head.appendChild(s);
      window.gtag('js', new Date());
      window.gtag('config', GA_ID, { anonymize_ip: true });
    }
    if (CLARITY_ID) {
      (function (c, l, a, r, i, t, y) {
        c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
        t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
        y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
      })(window, document, 'clarity', 'script', CLARITY_ID);
    }
  }

  function track(name, params) {
    if (!analyticsLoaded || !window.gtag || !GA_ID) return;
    params = params || {};
    params.page_path = location.pathname;
    window.gtag('event', name, params);
  }

  // ---------- Consent banner ----------
  function showConsent() {
    var box = document.createElement('div');
    box.className = 'consent';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', TXT.consentLabel);
    box.innerHTML =
      '<p>' + TXT.consent + ' <a href="' + TXT.privacyHref + '">' + TXT.privacy + '</a></p>' +
      '<div class="consent-actions"><button type="button" class="btn btn-accent" data-consent="granted">' + TXT.accept + '</button>' +
      '<button type="button" class="btn btn-outline" data-consent="denied">' + TXT.decline + '</button></div>';
    document.body.appendChild(box);
    box.addEventListener('click', function (e) {
      var v = e.target.getAttribute && e.target.getAttribute('data-consent');
      if (!v) return;
      store('goni_consent', v);
      box.remove();
      if (v === 'granted') loadAnalytics();
    });
  }

  if (GA_ID || CLARITY_ID) {
    if (consentGranted()) loadAnalytics();
    else if (!store('goni_consent')) showConsent();
    var reset = document.querySelector('[data-consent-reset]');
    if (reset) {
      reset.hidden = false;
      reset.addEventListener('click', function (e) {
        e.preventDefault();
        store('goni_consent', '');
        if (!document.querySelector('.consent')) showConsent();
      });
    }
  }

  // ---------- Click tracking ----------
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (a.hasAttribute('data-wa') || href.indexOf('wa.me/') > -1) {
      track('whatsapp_click', { link_location: a.classList.contains('wa-float') ? 'floating_button' : 'page' });
    } else if (a.classList.contains('btn') && href.indexOf(TXT.cta) === 0) {
      track('cta_click', { cta_text: a.textContent.trim().slice(0, 40) });
    }
  });

  // ---------- Inquiry form ----------
  var form = document.getElementById('consult-form');
  if (!form) return;

  var statusEl = document.getElementById('form-status');
  var submitBtn = document.getElementById('send-form');
  var waBtn = document.getElementById('send-wa');

  var pre = new URLSearchParams(location.search).get('category');
  var catSel = document.getElementById('f-cat');
  if (pre && catSel) {
    for (var i = 0; i < catSel.options.length; i++) {
      if (catSel.options[i].value === pre) catSel.selectedIndex = i;
    }
  }

  function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }

  function collect() {
    return {
      name: val('f-name'), whatsapp: val('f-wa'), category: val('f-cat'),
      volume: val('f-vol'), message: val('f-msg'), website: val('f-website'),
      page: location.pathname, lang: LANG, referrer: session('goni_ref') || '', utm: readUtm()
    };
  }

  function waText(d) {
    return [
      TXT.waIntro,
      TXT.name + ': ' + d.name, TXT.wa + ': ' + d.whatsapp, TXT.cat + ': ' + d.category,
      TXT.vol + ': ' + d.volume, TXT.idea + ': ' + (d.message || '-')
    ].join('\n');
  }

  function setStatus(kind, html) {
    statusEl.hidden = false;
    statusEl.className = 'form-status ' + kind;
    statusEl.innerHTML = html;
  }

  function busy(on) {
    submitBtn.disabled = on;
    submitBtn.textContent = on ? TXT.sending : TXT.send;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = collect();
    busy(true);
    statusEl.hidden = true;

    fetch(INQUIRY_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(d)
    }).then(function (r) {
      if (!r.ok) throw new Error('status ' + r.status);
      return r.json();
    }).then(function () {
      track('generate_lead', { method: 'form', product_category: d.category, estimated_order: d.volume });
      setStatus('ok', TXT.ok);
      form.reset();
      if (catSel && pre) { /* keep the preselected category after reset */
        for (var j = 0; j < catSel.options.length; j++) { if (catSel.options[j].value === pre) catSel.selectedIndex = j; }
      }
    }).catch(function () {
      setStatus('warn', TXT.fail +
        '<a href="' + waUrl(waText(d)) + '" target="_blank" rel="noopener" data-wa-fallback>' + TXT.openWa + '</a>');
    }).then(function () { busy(false); });
  });

  if (waBtn) {
    waBtn.addEventListener('click', function () {
      if (!form.reportValidity()) return;
      var d = collect();
      track('whatsapp_click', { link_location: 'form' });
      track('generate_lead', { method: 'whatsapp', product_category: d.category, estimated_order: d.volume });
      window.open(waUrl(waText(d)), '_blank', 'noopener');
    });
  }

  statusEl.addEventListener('click', function (e) {
    if (e.target.hasAttribute && e.target.hasAttribute('data-wa-fallback')) {
      track('whatsapp_click', { link_location: 'form_fallback' });
    }
  });
})();
