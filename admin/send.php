<?php
/**
 * SUBLIME CI-USA — envoi de l'invitation.
 *
 * Le navigateur envoie les invitations une par une (une requête par
 * destinataire, avec une pause entre deux) : pas de délai d'exécution PHP
 * dépassé, une progression visible, et un rythme qui ne déclenche pas les
 * filtres anti-spam. Chaque envoi est journalisé : relancer la liste
 * n'écrit pas deux fois à la même personne, sauf si on le demande.
 */

declare(strict_types=1);
define('SUBLIME', 1);
require __DIR__ . '/../api/_lib/admin.php';
require __DIR__ . '/../api/_lib/store.php';
require __DIR__ . '/../api/_lib/mailer.php';
require __DIR__ . '/../api/_lib/templates.php';

sb_admin_start();
sb_require_login();

const SB_CAMPAIGN = 'two-cities';
const SB_SUBJECTS = [
    'en' => "You're invited — Two Cities, One Friendship, December 11",
    'fr' => 'Invitation — Two Cities, One Friendship, le 11 décembre',
];

function sb_sent_file(): string
{
    return sb_private_dir() . '/sent-' . SB_CAMPAIGN . '.log';
}

/** @return array<string,string> e-mail => date du dernier envoi réussi */
function sb_already_sent(): array
{
    $done = [];
    if (is_file(sb_sent_file())) {
        foreach (file(sb_sent_file(), FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [] as $l) {
            $e = json_decode($l, true);
            if (($e['status'] ?? '') === 'sent' && empty($e['test'])) {
                $done[strtolower((string) $e['email'])] = (string) $e['t'];
            }
        }
    }
    return $done;
}

// ------------------------------------------------------------ aperçu
if (isset($_GET['preview'])) {
    $lang = $_GET['preview'] === 'fr' ? 'fr' : 'en';
    header('Content-Type: text/html; charset=utf-8');
    echo sb_invitation($lang, (string) ($_GET['n'] ?? ''), '')['html'];
    exit;
}

// ------------------------------------------------------------ envoi d'un message
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    header('Content-Type: application/json; charset=utf-8');
    if (!sb_csrf_ok()) {
        exit(json_encode(['ok' => false, 'status' => 'error', 'error' => 'Session expirée : rechargez la page.']));
    }
    $email = strtolower(sb_clean((string) ($_POST['email'] ?? ''), 160));
    $name  = sb_clean((string) ($_POST['name'] ?? ''), 100);
    $lang  = ($_POST['lang'] ?? '') === 'fr' ? 'fr' : 'en';
    $subj  = sb_clean((string) ($_POST['subject'] ?? ''), 200) ?: SB_SUBJECTS[$lang];
    $test  = !empty($_POST['test']);
    $force = !empty($_POST['force']);

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        exit(json_encode(['ok' => false, 'status' => 'error', 'error' => 'Adresse invalide']));
    }
    if (!$test && !$force && isset(sb_already_sent()[$email])) {
        $when = strtotime(sb_already_sent()[$email]) ?: time();
        exit(json_encode(['ok' => true, 'status' => 'skipped', 'error' => 'déjà invitée le ' . date('d/m à H:i', $when)]));
    }

    $inv    = sb_invitation($lang, $name, $email);
    $mailer = new SbMailer(sb_config());
    $ok     = $mailer->send($email, $name, ($test ? '[TEST] ' : '') . $subj, $inv['html'], $inv['text'],
                            ['reply_to' => (string) sb_config()['reply_to'], 'unsubscribe' => true]);
    sb_log('sent-' . SB_CAMPAIGN . '.log', ['email' => $email, 'name' => $name, 'lang' => $lang,
           'status' => $ok ? 'sent' : 'error', 'test' => $test, 'error' => $mailer->error]);

    exit(json_encode(['ok' => $ok, 'status' => $ok ? 'sent' : 'error', 'error' => $mailer->error]));
}

// ------------------------------------------------------------ page
$sent  = sb_already_sent();
$delay = max(1, (int) sb_config()['send_delay']);
$smtp  = sb_configured('smtp_pass');
sb_page_top('Envoyer l’invitation', 'send');
?>
<div class="head"><div><h1>Envoyer l’invitation</h1>
  <p class="muted">Depuis <b><?= sb_h((string) sb_config()['from_email']) ?></b> · les réponses des invités arrivent à <b><?= sb_h((string) sb_config()['reply_to']) ?></b></p></div></div>

<?php if (!$smtp): ?>
<p class="alert warn">Le mot de passe SMTP n’est pas configuré : l’envoi passera par mail(), avec un risque élevé d’arriver en spam. Complétez <code>smtp_pass</code> dans config.php avant un envoi réel.</p>
<?php endif ?>

<div class="sendgrid">
  <div class="card">
    <h2>1. Destinataires</h2>
    <p class="muted small">Une personne par ligne : <code>Prénom Nom, adresse@exemple.com</code> — le nom est facultatif mais permet de personnaliser l’invitation (« Dear Jane, »). Collage direct depuis Excel accepté.</p>
    <textarea id="list" rows="10" placeholder="Jane Doe, jane@example.com&#10;john@example.com&#10;Aminata Koné; aminata@example.org"></textarea>
    <p class="small" id="count"></p>

    <h2>2. Message</h2>
    <div class="row">
      <label class="radio"><input type="radio" name="lang" value="en" checked> Anglais</label>
      <label class="radio"><input type="radio" name="lang" value="fr"> Français</label>
    </div>
    <label for="subject">Objet</label>
    <input id="subject" value="<?= sb_h(SB_SUBJECTS['en']) ?>">
    <label class="check"><input type="checkbox" id="force"> Renvoyer aussi aux personnes qui l’ont déjà reçue
      <span class="muted">(<?= count($sent) ?> envoi<?= count($sent) > 1 ? 's' : '' ?> réussi<?= count($sent) > 1 ? 's' : '' ?> à ce jour)</span></label>

    <h2>3. Test, puis envoi</h2>
    <div class="row">
      <input id="testTo" type="email" placeholder="votre adresse pour le test" style="flex:1">
      <button class="btn ghost" id="testBtn" type="button">Envoyer un test</button>
    </div>
    <button class="btn big" id="goBtn" type="button" disabled>Envoyer l’invitation</button>
    <button class="btn ghost" id="stopBtn" type="button" hidden>Arrêter</button>
    <p class="alert" id="msg" hidden></p>
    <ol id="progress" class="progress"></ol>
  </div>

  <div class="card preview">
    <h2>Aperçu</h2>
    <iframe id="frame" src="send.php?preview=en" title="Aperçu de l’invitation"></iframe>
  </div>
</div>

<script>
(function () {
  var CSRF = <?= json_encode(sb_csrf()) ?>, DELAY = <?= $delay ?> * 1000;
  var SUBJ = <?= json_encode(SB_SUBJECTS, JSON_UNESCAPED_UNICODE) ?>;
  var SENT = <?= json_encode(array_keys($sent)) ?>;
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
      if (subj.value === SUBJ.en || subj.value === SUBJ.fr) subj.value = SUBJ[lang()];
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
</script>
<?php
sb_page_bottom();
