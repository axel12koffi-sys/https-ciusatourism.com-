/* ============================================================
   SUBLIME CI-USA — main.js
   Modules : preloader, header, drawer, rail de vol, reveals,
   slider hero, compteurs, filtres, accordéon, formulaires,
   newsletter, lightbox, back-to-top, i18n FR/EN.
   Chaque module se désactive tout seul si son markup est absent,
   donc le fichier est chargé tel quel sur toutes les pages.
   ============================================================ */
(function () {
  'use strict';

  var REDUCE = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------------------------------------------------------
     1. PRELOADER
     --------------------------------------------------------- */
  (function preloader() {
    var el = $('#preloader');
    if (!el) return;
    var bar = $('.pl-bar i', el), p = 0;
    var t = setInterval(function () {
      p = Math.min(100, p + Math.random() * 22);
      if (bar) bar.style.width = p + '%';
      if (p >= 100) { clearInterval(t); setTimeout(function () { el.classList.add('done'); }, 260); }
    }, 130);
    window.addEventListener('load', function () {
      p = 100; if (bar) bar.style.width = '100%';
      setTimeout(function () { el.classList.add('done'); }, 300);
    });
  })();

  /* ---------------------------------------------------------
     2. HEADER : sticky, masquage au scroll bas, progression
     --------------------------------------------------------- */
  var hdr = $('#hdr'), bar = $('#hdrProgress'), lastY = 0;

  function headerFrame(y) {
    if (!hdr) return;
    hdr.classList.toggle('is-stuck', y > 12);
    hdr.classList.toggle('is-hidden', y > 420 && y > lastY && !$('#drawer.is-open'));
    lastY = y;
  }

  /* ---------------------------------------------------------
     3. DRAWER MOBILE (avec sous-menus accordéon)
     --------------------------------------------------------- */
  (function drawer() {
    var d = $('#drawer'), b = $('#burger'), c = $('#drawerClose');
    if (!d || !b) return;
    function open(v) {
      d.classList.toggle('is-open', v);
      b.classList.toggle('on', v);
      document.body.classList.toggle('no-scroll', v);
      b.setAttribute('aria-expanded', v ? 'true' : 'false');
    }
    b.addEventListener('click', function () { open(!d.classList.contains('is-open')); });
    if (c) c.addEventListener('click', function () { open(false); });
    $$('a', d).forEach(function (a) { a.addEventListener('click', function () { open(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') open(false); });

    $$('.m-group > button', d).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var g = btn.parentElement, sub = $('.m-sub', g), isOpen = g.classList.toggle('open');
        sub.style.maxHeight = isOpen ? sub.scrollHeight + 'px' : 0;
      });
    });
  })();

  /* ---------------------------------------------------------
     4. REVEALS AU SCROLL
     --------------------------------------------------------- */
  (function reveals() {
    var items = $$('.rv');
    if (!items.length) return;
    if (!('IntersectionObserver' in window) || REDUCE) {
      items.forEach(function (i) { i.classList.add('in'); }); return;
    }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: .14, rootMargin: '0px 0px -7% 0px' });
    items.forEach(function (i) { io.observe(i); });
  })();

  /* ---------------------------------------------------------
     5. RAIL DE VOL — avion + waypoints (élément signature)
     --------------------------------------------------------- */
  var track = $('#track'), trail = $('#trail'), railPlane = $('#railPlane');
  var sections = $$('[data-way]'), dots = [];

  if (track) {
    sections.forEach(function () {
      var d = document.createElement('div');
      d.className = 'flightrail__dot';
      track.appendChild(d); dots.push(d);
    });
  }
  function placeDots() {
    if (!track) return;
    var docH = document.documentElement.scrollHeight, h = track.clientHeight;
    sections.forEach(function (s, i) {
      dots[i].style.top = ((s.offsetTop + s.offsetHeight * .35) / docH) * h + 'px';
    });
  }
  function railFrame(p) {
    if (!track) return;
    var h = track.clientHeight;
    railPlane.style.transform = 'translateY(' + (p * h) + 'px) rotate(' + (Math.sin(p * Math.PI * 2) * 5) + 'deg)';
    trail.style.height = (p * h) + 'px';
    dots.forEach(function (d, i) {
      var r = sections[i].getBoundingClientRect();
      d.classList.toggle('on', r.top < innerHeight * .55 && r.bottom > innerHeight * .25);
    });
  }

  /* ---------------------------------------------------------
     6. ARC DE ROUTE animé (section Welcome)
     --------------------------------------------------------- */
  var arcLive = $('#arcLive'), arcPlane = $('#arcPlane'), routemap = $('.routemap');
  function arcFrame() {
    if (!routemap || !arcLive) return;
    var r = routemap.getBoundingClientRect();
    var t = Math.min(1, Math.max(0, 1 - (r.top / (innerHeight * .85))));
    var L = arcLive.getTotalLength();
    arcLive.style.strokeDasharray = L;
    arcLive.style.strokeDashoffset = L * (1 - t);
    var a = arcLive.getPointAtLength(L * t), b = arcLive.getPointAtLength(Math.min(L, L * t + 1));
    var ang = Math.atan2(b.y - a.y, b.x - a.x) * 180 / Math.PI + 90;
    arcPlane.setAttribute('transform', 'translate(' + a.x + ',' + a.y + ') rotate(' + ang + ')');
    arcPlane.style.opacity = (t > .02 && t < .995) ? 1 : 0;
  }

  /* ---------------------------------------------------------
     7. BACK TO TOP
     --------------------------------------------------------- */
  var toTop = $('#toTop');
  if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: REDUCE ? 'auto' : 'smooth' }); });

  /* ---------------------------------------------------------
     8. BOUCLE DE SCROLL UNIQUE (rAF)
     --------------------------------------------------------- */
  var ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY;
    var max = document.documentElement.scrollHeight - innerHeight;
    var p = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
    headerFrame(y);
    if (bar) bar.style.width = (p * 100) + '%';
    railFrame(p);
    arcFrame();
    if (toTop) toTop.classList.toggle('on', y > 700);
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { placeDots(); onScroll(); });
  window.addEventListener('load', function () { placeDots(); onScroll(); });
  placeDots(); onScroll();

  /* ---------------------------------------------------------
     9. SLIDER HERO (autoplay + puces + clavier + pause onglet)
     --------------------------------------------------------- */
  (function heroSlider() {
    var slides = $$('.hero__slide'), dotsBox = $('#heroDots');
    if (slides.length < 2) { if (slides[0]) slides[0].classList.add('on'); return; }
    var i = 0, timer = null, DELAY = 6000;

    slides.forEach(function (_, n) {
      var b = document.createElement('button');
      b.setAttribute('aria-label', 'Slide ' + (n + 1));
      b.addEventListener('click', function () { go(n); restart(); });
      dotsBox.appendChild(b);
    });
    function go(n) {
      slides[i].classList.remove('on');
      dotsBox.children[i].classList.remove('on');
      i = (n + slides.length) % slides.length;
      slides[i].classList.add('on');
      dotsBox.children[i].classList.add('on');
    }
    function next() { go(i + 1); }
    function restart() { clearInterval(timer); if (!REDUCE) timer = setInterval(next, DELAY); }
    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { next(); restart(); }
      if (e.key === 'ArrowLeft') { go(i - 1); restart(); }
    });
    document.addEventListener('visibilitychange', function () {
      document.hidden ? clearInterval(timer) : restart();
    });
    go(0); restart();
  })();

  /* ---------------------------------------------------------
     10. COMPTEURS ANIMÉS
     --------------------------------------------------------- */
  (function counters() {
    var els = $$('[data-count]');
    if (!els.length || !('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.textContent = e.dataset.count + (e.dataset.suffix || ''); }); return;
    }
    var io = new IntersectionObserver(function (list) {
      list.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, target = parseFloat(el.dataset.count), suf = el.dataset.suffix || '';
        if (REDUCE) { el.textContent = target + suf; io.unobserve(el); return; }
        el.textContent = '0' + suf;   /* on repart de zéro pour l'animation */
        var start = performance.now(), dur = 1300;
        (function step(now) {
          var t = Math.min(1, (now - start) / dur);
          var eased = 1 - Math.pow(1 - t, 3);
          el.textContent = Math.round(target * eased) + suf;
          if (t < 1) requestAnimationFrame(step);
        })(start);
        io.unobserve(el);
      });
    }, { threshold: .5 });
    els.forEach(function (e) { io.observe(e); });
  })();

  /* ---------------------------------------------------------
     11. FILTRES + RECHERCHE (destinations, blog, hôtels,
     restaurants). Les deux critères se combinent, et le
     compteur se met à jour à chaque frappe.
     --------------------------------------------------------- */
  (function filters() {
    var box = $('#filters');
    if (!box) return;
    var items  = $$('.grid-item');
    var search = $('#listingSearch');
    var count  = $('#listCount');
    var empty  = $('#listEmpty');
    var cat = 'all', q = '';

    function apply() {
      var n = 0;
      items.forEach(function (it) {
        var okCat = (cat === 'all' || it.dataset.cat === cat);
        var okQ   = (!q || (it.dataset.name || it.textContent).toLowerCase().indexOf(q) > -1);
        var show  = okCat && okQ;
        it.classList.toggle('hide', !show);
        if (show) n++;
      });
      if (count) count.textContent = n;
      if (empty) empty.classList.toggle('on', n === 0);
    }

    $$('button', box).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('button', box).forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        cat = b.dataset.filter;
        apply();
      });
    });

    if (search) {
      var t = null;
      search.addEventListener('input', function () {
        clearTimeout(t);
        t = setTimeout(function () { q = search.value.trim().toLowerCase(); apply(); }, 120);
      });
      search.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { search.value = ''; q = ''; apply(); }
      });
    }
  })();

  /* ---------------------------------------------------------
     12. ACCORDÉON FAQ (+ deep-link #q3)
     --------------------------------------------------------- */
  (function accordion() {
    var items = $$('.acc__i');
    if (!items.length) return;
    function toggle(it, force) {
      var a = $('.acc__a', it);
      var open = force !== undefined ? force : !it.classList.contains('open');
      items.forEach(function (o) {
        if (o !== it) { o.classList.remove('open'); $('.acc__a', o).style.maxHeight = 0; }
      });
      it.classList.toggle('open', open);
      a.style.maxHeight = open ? a.scrollHeight + 'px' : 0;
    }
    items.forEach(function (it) {
      $('.acc__q', it).addEventListener('click', function () { toggle(it); });
    });
    if (location.hash) {
      var t = document.getElementById(location.hash.slice(1));
      if (t && t.classList.contains('acc__i')) { toggle(t, true); t.scrollIntoView({ block: 'center' }); }
    }
  })();

  /* ---------------------------------------------------------
     13. FORMULAIRE DE CONTACT (validation front)
     PHP : remplacer le setTimeout par un fetch('/api/contact.php')
     --------------------------------------------------------- */
  (function contactForm() {
    var f = $('#contactForm');
    if (!f) return;
    var alertOk = $('#formOk');
    var alertKo = $('#formKo');

    /* piège temporel : on note l'instant où le formulaire s'affiche.
       Un robot renvoie en une fraction de seconde, un humain met
       au moins quelques secondes à écrire. */
    var started = $('#started', f);
    if (started) started.value = String(Date.now());

    function invalid(field) {
      var el = $('input,select,textarea', field);
      if (!el) return false;
      var v = el.value.trim();
      if (el.required && !v) return true;
      if (el.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return true;
      return false;
    }
    $$('.field', f).forEach(function (field) {
      var el = $('input,select,textarea', field);
      if (el) el.addEventListener('input', function () { field.classList.remove('err'); });
    });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = 0;
      $$('.field', f).forEach(function (field) {
        var ko = invalid(field);
        field.classList.toggle('err', ko);
        if (ko) bad++;
      });
      if (bad) { $('.field.err input,.field.err select,.field.err textarea', f).focus(); return; }

      var btn = $('button[type=submit]', f), label = btn.textContent;
      btn.textContent = 'Sending…'; btn.disabled = true;

      function done() {
        btn.textContent = label; btn.disabled = false;
        f.reset(); alertOk.classList.add('on');
        alertOk.scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth', block: 'center' });
      }
      function fail(msg) {
        btn.textContent = label; btn.disabled = false;
        alertKo.textContent = msg;
        alertKo.classList.add('on');
      }

      fetch('/api/contact.php', { method: 'POST', body: new FormData(f) })
        .then(function (r) { return r.json().then(function (d) { return { s: r.status, d: d }; }); })
        .then(function (r) {
          alertKo.classList.remove('on');
          if (r.d.ok) return done();
          if (r.s === 429) return fail('Too many requests. Please try again in an hour, or email us directly.');
          if (r.d.fields) {
            r.d.fields.forEach(function (name) {
              var el = f.querySelector('[name="' + name + '"]');
              if (el) el.closest('.field').classList.add('err');
            });
            return fail('Please check the highlighted fields.');
          }
          fail('Something went wrong on our side. Email tourism@ambaciusa.org and we will pick it up.');
        })
        .catch(function () {
          fail('Could not reach the server. Email tourism@ambaciusa.org and we will pick it up.');
        });
    });
  })();

  /* ---------------------------------------------------------
     13b. RSVP (page événement) → /api/rsvp.php
     Messages lus dans les data-* du formulaire : ils sont traduits
     avec la page, le script reste unique pour les deux langues.
     --------------------------------------------------------- */
  (function rsvpForm() {
    var f = $('#rsvpForm');
    if (!f) return;
    var ok = $('#rsvpOk'), ko = $('#rsvpKo'), d = f.dataset;
    var started = $('.started', f);
    if (started) started.value = String(Date.now());

    /* lien personnalisé de l'invitation : ?n=Nom&e=adresse */
    try {
      var q = new URLSearchParams(location.search);
      /* f.name désigne le nom du formulaire, pas le champ : on passe par elements */
      var fn = f.elements.namedItem('name'), fe = f.elements.namedItem('email');
      if (q.get('n') && !fn.value) fn.value = q.get('n').slice(0, 100);
      if (q.get('e') && !fe.value) fe.value = q.get('e').slice(0, 160);
    } catch (e) {}

    /* « Non » : la liste des participants n'a plus lieu d'être */
    function sync() {
      var v = (f.querySelector('input[name=attending]:checked') || {}).value;
      f.classList.toggle('is-hidden-guests', v === 'no');
    }
    $$('input[name=attending]', f).forEach(function (r) {
      r.addEventListener('change', function () { $('#attField').classList.remove('err'); sync(); });
    });

    function invalid(field) {
      if (field.id === 'attField') return !f.querySelector('input[name=attending]:checked');
      var el = $('input,select,textarea', field);
      if (!el) return false;
      var v = el.value.trim();
      if (el.required && !v) return true;
      if (el.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return true;
      return false;
    }
    $$('.field', f).forEach(function (field) {
      var el = $('input:not([type=radio]),select,textarea', field);
      if (el) el.addEventListener('input', function () { field.classList.remove('err'); });
    });

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      ok.classList.remove('on'); ko.classList.remove('on');
      var bad = 0;
      $$('.field', f).forEach(function (field) {
        var x = invalid(field);
        field.classList.toggle('err', x);
        if (x) bad++;
      });
      if (bad) {
        var first = $('.field.err', f);
        first.scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth', block: 'center' });
        var el = $('input,select,textarea', first); if (el) el.focus({ preventScroll: true });
        return;
      }
      var btn = $('button[type=submit]', f), label = btn.innerHTML;
      btn.textContent = d.sending; btn.disabled = true;

      function fail(m) { btn.innerHTML = label; btn.disabled = false; ko.textContent = m; ko.classList.add('on'); }

      fetch('/api/rsvp.php', { method: 'POST', body: new FormData(f), credentials: 'same-origin' })
        .then(function (r) { return r.json().then(function (j) { return { s: r.status, j: j }; }); })
        .then(function (r) {
          if (r.j.ok) {
            btn.innerHTML = label; btn.disabled = false;
            ok.textContent = r.j.attending === 'no' ? d.okNo : d.okYes;
            ok.classList.add('on');
            f.reset(); sync();
            if (started) started.value = String(Date.now());
            ok.scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth', block: 'center' });
            return;
          }
          if (r.s === 429) return fail(d.errRate);
          if (r.j.fields) {
            r.j.fields.forEach(function (n) {
              var el = f.querySelector('[name="' + n + '"]');
              if (el) el.closest('.field').classList.add('err');
            });
            return fail(d.errFields);
          }
          fail(d.errServer);
        })
        .catch(function () { fail(d.errNet); });
    });
  })();

  /* ---------------------------------------------------------
     14. NEWSLETTER (footer, toutes les pages)
     --------------------------------------------------------- */
  (function newsletter() {
    var box = $('#nlForm');
    if (!box) return;
    var input = $('input', box), msg = $('#nlMsg');
    function send() {
      var v = input.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) { msg.textContent = 'Enter a valid email address.'; return; }
      msg.textContent = 'Thanks — you are on the list.';
      input.value = '';
      // PHP : fetch('api/newsletter.php', {method:'POST', body:JSON.stringify({email:v})})
    }
    $('button', box).addEventListener('click', send);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') send(); });
  })();

  /* ---------------------------------------------------------
     15. LIGHTBOX (médiathèque)
     --------------------------------------------------------- */
  (function lightbox() {
    var gal = $('#gallery'), lb = $('#lightbox');
    if (!gal || !lb) return;
    var imgs = $$('img', gal), img = $('#lbImg'), idx = 0;
    function open(n) { idx = (n + imgs.length) % imgs.length; img.src = imgs[idx].dataset.full || imgs[idx].src; lb.classList.add('on'); document.body.classList.add('no-scroll'); }
    function close() { lb.classList.remove('on'); document.body.classList.remove('no-scroll'); }
    $$('button', gal).forEach(function (b, n) { b.addEventListener('click', function () { open(n); }); });
    $('#lbClose').addEventListener('click', close);
    $('#lbPrev').addEventListener('click', function () { open(idx - 1); });
    $('#lbNext').addEventListener('click', function () { open(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('on')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') open(idx + 1);
      if (e.key === 'ArrowLeft') open(idx - 1);
    });
  })();

  /* ---------------------------------------------------------
     16. MARQUEE PARTENAIRES (duplication pour boucle continue)
     --------------------------------------------------------- */
  (function marquee() {
    var m = $('#marquee');
    if (!m) return;
    m.innerHTML += m.innerHTML;
    if (REDUCE) m.style.animation = 'none';
  })();

  /* ---------------------------------------------------------
     17. LANGUE
     Le site existe en deux versions statiques : la racine en
     anglais, /fr/ en français. Le sélecteur navigue de l'une à
     l'autre et mémorise le choix, pour que la visite suivante
     arrive directement dans la bonne langue.
     --------------------------------------------------------- */
  var LANG = document.documentElement.lang === 'fr' ? 'fr' : 'en';

  $$('.langs a, .langs button').forEach(function (el) {
    el.addEventListener('click', function () {
      var to = el.dataset.lang || (el.textContent.trim().toLowerCase());
      try { localStorage.setItem('ciusa-lang', to); } catch (e) {}
    });
  });

  /* redirection au premier chargement, une seule fois par session,
     et jamais si l'internaute est arrivé par un lien direct vers
     l'autre version */
  (function autoLang() {
    var saved = null, redirected = false;
    try {
      saved = localStorage.getItem('ciusa-lang');
      redirected = sessionStorage.getItem('ciusa-lang-done') === '1';
    } catch (e) { return; }
    if (!saved || redirected || saved === LANG) return;
    try { sessionStorage.setItem('ciusa-lang-done', '1'); } catch (e) {}
    var path = location.pathname;
    var target = saved === 'fr'
      ? path.replace(/\/([^\/]*)$/, '/fr/$1')
      : path.replace('/fr/', '/');
    if (target !== path) location.replace(target);
  })();

  /* expose pour le chatbot */
  window.CIUSA = { lang: function () { return LANG; }, reduce: REDUCE };
})();
