/* SUBLIME CI-USA — administration.
   Fichier séparé (pas de script dans la page) : compatible avec la
   Content-Security-Policy « script-src 'self' » du serveur. */

/* confirmation avant suppression d'une réponse (page Réponses) */
document.querySelectorAll('form[data-confirm]').forEach(function (f) {
  f.addEventListener('submit', function (e) {
    if (!confirm(f.getAttribute('data-confirm'))) e.preventDefault();
  });
});

/* filtre des invitations par état (tableau de bord) */
(function () {
  var table = document.getElementById('invTable');
  if (!table) return;
  var chips = document.querySelectorAll('.chip[data-filter]');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.getAttribute('data-filter');
      chips.forEach(function (x) { x.classList.toggle('on', x === c); });
      table.querySelectorAll('tbody tr').forEach(function (tr) {
        tr.hidden = f !== 'all' && tr.getAttribute('data-state') !== f;
      });
    });
  });
})();

/* page d'envoi */
if (document.getElementById('sendCfg')) (function () {
  var C = JSON.parse(document.getElementById('sendCfg').textContent);
  var CSRF = C.csrf, DELAY = C.delay, SUBJ = C.subj, SENT = C.sent;
  var $ = function (s) { return document.querySelector(s); };
  var list = $('#list'), subj = $('#subject'), frame = $('#frame'), msg = $('#msg');
  var stop = false, busy = false;

  function lang() { return document.querySelector('input[name=lang]:checked').value; }

  /* « Nom, e-mail » / « e-mail » / « Nom <e-mail> » / colonnes Excel */
  function parse() {
    var seen = {}, out = [], bad = [];
    list.value.split(/\n/).forEach(function (line) {
      line = line.trim(); if (!line) return;
      var m = line.match(/[^\s<>,;\t"]+@[^\s<>,;\t"]+\.[^\s<>,;\t"]+/);
      if (!m) { bad.push(line); return; }
      var email = m[0].toLowerCase();
      var name = line.replace(m[0], '').replace(/[<>"]/g, '').replace(/[,;\t]+/g, ' ').replace(/\s+/g, ' ').trim();
      if (seen[email]) return;
      seen[email] = 1; out.push({ email: email, name: name });
    });
    return { ok: out, bad: bad };
  }

  function refresh() {
    var p = parse(), force = $('#force').checked;
    var already = p.ok.filter(function (r) { return SENT.indexOf(r.email) >= 0; }).length;
    var txt = p.ok.length + ' destinataire' + (p.ok.length > 1 ? 's' : '');
    if (already) txt += ' — dont ' + already + ' déjà invité' + (already > 1 ? 's' : '') + (force ? ' (seront relancés)' : ' (seront ignorés)');
    if (p.bad.length) txt += ' — ' + p.bad.length + ' ligne(s) sans adresse valide : ' + p.bad.slice(0, 3).join(' | ');
    $('#count').textContent = p.ok.length || p.bad.length ? txt : '';
    $('#goBtn').disabled = busy || !p.ok.length;
    var first = p.ok[0] && p.ok[0].name ? p.ok[0].name : '';
    var src = 'send.php?preview=' + lang() + (first ? '&n=' + encodeURIComponent(first) : '');
    if (frame.getAttribute('src') !== src) frame.setAttribute('src', src);
  }

  function say(text, kind) { msg.hidden = false; msg.className = 'alert ' + kind; msg.textContent = text; }

  function post(r, test) {
    var fd = new FormData();
    fd.append('csrf', CSRF); fd.append('email', r.email); fd.append('name', r.name || '');
    fd.append('lang', lang()); fd.append('subject', subj.value);
    if (test) fd.append('test', '1');
    if ($('#force').checked) fd.append('force', '1');
    return fetch('send.php', { method: 'POST', body: fd, headers: { Accept: 'application/json' }, credentials: 'same-origin' })
      .then(function (res) { return res.json(); })
      .catch(function () { return { ok: false, status: 'error', error: 'Serveur injoignable' }; });
  }

  document.querySelectorAll('input[name=lang]').forEach(function (i) {
    i.addEventListener('change', function () {
      var R = { en: 'Reminder: ', fr: 'Rappel : ' };
      if (subj.value === SUBJ.en || subj.value === SUBJ.fr) subj.value = SUBJ[lang()];
      else if (subj.value === R.en + SUBJ.en || subj.value === R.fr + SUBJ.fr) subj.value = R[lang()] + SUBJ[lang()];
      refresh();
    });
  });
  list.addEventListener('input', refresh);
  $('#force').addEventListener('change', refresh);

  $('#testBtn').addEventListener('click', function () {
    var to = $('#testTo').value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(to)) { say('Indiquez une adresse valide pour le test.', 'ko'); return; }
    var first = parse().ok[0];
    say('Envoi du test…', 'info');
    post({ email: to, name: first ? first.name : '' }, true).then(function (d) {
      d.ok ? say('Test envoyé à ' + to + '. Vérifiez la boîte de réception — et le dossier spam.', 'ok')
           : say('Échec du test : ' + d.error, 'ko');
    });
  });

  $('#stopBtn').addEventListener('click', function () { stop = true; say('Arrêt demandé : l’envoi en cours se termine, puis tout s’arrête.', 'info'); });

  $('#goBtn').addEventListener('click', function () {
    var rows = parse().ok;
    if (!rows.length) return;
    if (!confirm('Envoyer l’invitation (' + (lang() === 'fr' ? 'français' : 'anglais') + ') à ' + rows.length + ' destinataire(s) ?')) return;
    busy = true; stop = false;
    $('#goBtn').disabled = true; $('#stopBtn').hidden = false; list.readOnly = true;
    var ol = $('#progress'); ol.innerHTML = '';
    var items = rows.map(function (r) {
      var li = document.createElement('li'); li.className = 'wait';
      li.textContent = (r.name ? r.name + ' — ' : '') + r.email; ol.appendChild(li); return li;
    });
    var n = { sent: 0, skipped: 0, error: 0 }, i = 0;

    function next() {
      if (stop || i >= rows.length) {
        busy = false; $('#stopBtn').hidden = true; list.readOnly = false; refresh();
        say((stop ? 'Interrompu. ' : 'Terminé. ') + n.sent + ' envoyée(s), ' + n.skipped + ' ignorée(s), ' + n.error + ' en échec.',
            n.error ? 'ko' : 'ok');
        return;
      }
      var li = items[i]; li.className = 'run';
      post(rows[i], false).then(function (d) {
        n[d.status] = (n[d.status] || 0) + 1;
        li.className = d.status;
        if (d.error) li.title = d.error;
        if (d.status === 'sent' && SENT.indexOf(rows[i].email) < 0) SENT.push(rows[i].email);
        if (d.status !== 'sent') li.textContent += ' — ' + (d.error || d.status);
        i++;
        say('Envoi en cours : ' + i + ' / ' + rows.length, 'info');
        setTimeout(next, d.status === 'sent' ? DELAY : 150);
      });
    }
    next();
  });

  refresh();
})();
