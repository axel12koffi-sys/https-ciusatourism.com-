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
require __DIR__ . '/../api/_lib/invites.php';

sb_admin_start();
sb_require_login();

const SB_SUBJECTS = [
    'en' => "You're Cordially Invited — Two Cities, One Friendship, December 11",
    'fr' => 'Invitation VIP — Two Cities, One Friendship, le 11 décembre',
];
const SB_REMINDER = ['en' => 'Reminder: ', 'fr' => 'Rappel : '];

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
$relance = in_array($_GET['relance'] ?? '', ['en', 'fr'], true) ? $_GET['relance'] : '';
$prefill = '';
if ($relance) {
    foreach (sb_invites() as $i) {
        if ($i['state'] === 'pending' && $i['lang'] === $relance) {
            $prefill .= ($i['name'] !== '' ? $i['name'] . ', ' : '') . $i['email'] . "\n";
        }
    }
}
$lang0 = $relance ?: 'en';
$subj0 = ($relance ? SB_REMINDER[$relance] : '') . SB_SUBJECTS[$lang0];
$delay = max(1, (int) sb_config()['send_delay']);
$smtp  = sb_configured('smtp_pass');
sb_page_top('Envoyer l’invitation', 'send');
?>
<div class="head"><div><h1>Envoyer l’invitation</h1>
  <p class="muted">Depuis <b><?= sb_h((string) sb_config()['from_email']) ?></b> · les réponses des invités arrivent à <b><?= sb_h((string) sb_config()['reply_to']) ?></b></p></div></div>

<?php if (!$smtp): ?>
<p class="alert warn">Le mot de passe SMTP n’est pas configuré : l’envoi passera par mail(), avec un risque élevé d’arriver en spam. Complétez <code>smtp_pass</code> dans config.php avant un envoi réel.</p>
<?php endif ?>

<?php if ($relance): ?>
<p class="alert info">Relance : la liste contient les invités <?= $relance === 'fr' ? 'francophones' : 'anglophones' ?> qui n’ont pas encore répondu, et l’objet commence par « <?= sb_h(trim(SB_REMINDER[$relance])) ?> ». Relisez, envoyez-vous un test, puis lancez l’envoi.</p>
<?php endif ?>
<div class="sendgrid">
  <div class="card">
    <h2>1. Destinataires</h2>
    <p class="muted small">Une personne par ligne : <code>Prénom Nom, adresse@exemple.com</code> — le nom est facultatif mais permet de personnaliser l’invitation (« Dear Jane, »). Collage direct depuis Excel accepté.</p>
    <textarea id="list" rows="10" placeholder="Jane Doe, jane@example.com&#10;john@example.com&#10;Aminata Koné; aminata@example.org"><?= sb_h($prefill) ?></textarea>
    <p class="small" id="count"></p>

    <h2>2. Message</h2>
    <div class="row">
      <label class="radio"><input type="radio" name="lang" value="en"<?= $lang0 === 'en' ? ' checked' : '' ?>> Anglais</label>
      <label class="radio"><input type="radio" name="lang" value="fr"<?= $lang0 === 'fr' ? ' checked' : '' ?>> Français</label>
    </div>
    <label for="subject">Objet</label>
    <input id="subject" value="<?= sb_h($subj0) ?>">
    <label class="check"><input type="checkbox" id="force"<?= $relance ? ' checked' : '' ?>> Renvoyer aussi aux personnes qui l’ont déjà reçue
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

<script type="application/json" id="sendCfg"><?= json_encode([
  'csrf'  => sb_csrf(),
  'delay' => $delay * 1000,
  'subj'  => SB_SUBJECTS,
  'sent'  => array_keys($sent),
], JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP) ?></script>

<?php
sb_page_bottom();
