<?php
/**
 * SUBLIME CI-USA — tableau de bord de l'événement.
 * Invitations envoyées et leur état, réponses RSVP, exports Excel,
 * suppression d'une réponse.
 */

declare(strict_types=1);
define('SUBLIME', 1);
require __DIR__ . '/../api/_lib/admin.php';
require __DIR__ . '/../api/_lib/store.php';
require __DIR__ . '/../api/_lib/invites.php';
require __DIR__ . '/../api/_lib/xlsx.php';

sb_admin_start();

// ------------------------------------------------------------ actions
$flash = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    if (!sb_csrf_ok()) {
        sb_login_page('Session expirée, merci de réessayer.');
    }
    $action = (string) ($_POST['action'] ?? '');
    if ($action === 'login') {
        $err = sb_login((string) ($_POST['password'] ?? ''));
        if ($err !== '') {
            sb_login_page($err);
        }
        header('Location: ./');
        exit;
    }
    if ($action === 'logout') {
        sb_logout();
        header('Location: ./');
        exit;
    }
    sb_require_login();
    if ($action === 'delete') {
        $flash = sb_rsvp_delete((string) ($_POST['email'] ?? '')) ? 'Réponse supprimée.' : 'Rien à supprimer.';
    }
}

if (!sb_admin_logged()) {
    sb_login_page();
}

$rows = sb_rsvp_all();

$invites = sb_invites();
const SB_STATE = [
    'pending' => ['En attente de réponse', 'wait'],
    'yes'     => ['A répondu : oui', 'yes'],
    'no'      => ['A répondu : non', 'no'],
    'failed'  => ['Échec d’envoi', 'fail'],
];
$fmt = fn (string $t) => $t !== '' ? date('d/m H:i', strtotime($t) ?: time()) : '—';
$xl  = fn (string $t) => $t !== '' ? date('Y-m-d H:i', strtotime($t) ?: time()) : '';

// ------------------------------------------------------------ chiffres
$yes = array_filter($rows, fn ($r) => $r['attending'] === 'yes');
$no  = count($rows) - count($yes);
/* nombre de personnes : les noms listés, ou 1 si le champ est vide */
$people = 0;
foreach ($yes as $r) {
    $names = array_filter(array_map('trim', preg_split('/[,;\n]| and | et |&/i', $r['guests']) ?: []));
    $people += max(1, count($names));
}

$count = array_count_values(array_column($invites, 'state')) + ['pending' => 0, 'yes' => 0, 'no' => 0, 'failed' => 0];
$sentN = count($invites) - $count['failed'];
$pendingLang = ['en' => 0, 'fr' => 0];
foreach ($invites as $i) {
    if ($i['state'] === 'pending') {
        $pendingLang[$i['lang']]++;
    }
}

// ------------------------------------------------------------ export Excel
$export = (string) ($_GET['export'] ?? '');
if ($export !== '' && SbXlsx::available()) {
    $tz = new DateTimeZone(date_default_timezone_get());
    $dt = function (string $t) use ($tz): ?DateTime {
        if ($t === '') return null;
        try { return (new DateTime($t))->setTimezone($tz); } catch (Exception) { return null; }
    };
    $nb = function (array $r): int {
        $n = array_filter(array_map('trim', preg_split('/[,;\n]| and | et |&/i', $r['guests']) ?: []));
        return max(1, count($n));
    };
    $H = fn (array $labels) => array_map(fn ($l) => [$l, SbXlsx::S_HEADER], $labels);
    $stateStyle = ['pending' => SbXlsx::S_WAIT, 'yes' => SbXlsx::S_YES, 'no' => SbXlsx::S_NO, 'failed' => SbXlsx::S_FAIL];
    $stateLabel = ['pending' => 'En attente', 'yes' => 'Oui', 'no' => 'Non', 'failed' => 'Échec d’envoi'];
    $T = SbXlsx::S_TEXT;

    $x = new SbXlsx();

    // --- Résumé
    $L = SbXlsx::S_LABEL; $B = SbXlsx::S_BIG;
    $x->addSheet('Résumé', [
        [['Two Cities, One Friendship', SbXlsx::S_TITLE]],
        [['Vendredi 11 décembre 2026 · 18 h – 22 h · Glenview Mansion, 603 Edmonston Drive, Rockville, MD 20851', SbXlsx::S_MUTED]],
        [['Fichier généré le ' . date('d/m/Y à H:i') . ' (heure de Washington)', SbXlsx::S_MUTED]],
        [],
        $H(['Indicateur', 'Nombre']),
        [['Invitations envoyées', $L], [$sentN, $B]],
        [['En attente de réponse', $L], [$count['pending'], $B]],
        [['Réponses « oui »', $L], [count($yes), $B]],
        [['Personnes attendues (estimation)', $L], [$people, $B]],
        [['Réponses « non »', $L], [$no, $B]],
        [['Échecs d’envoi', $L], [$count['failed'], $B]],
        [['Réponses reçues au total', $L], [count($rows), $B]],
        [],
        [['Onglets : « Accueil » = liste des personnes attendues, à imprimer pour le jour J ;', SbXlsx::S_MUTED]],
        [['« Invitations » = suivi des envois ; « Réponses » = détail des formulaires reçus.', SbXlsx::S_MUTED]],
    ], ['widths' => [46, 14], 'heights' => [0 => 30, 4 => 24]]);

    // --- Accueil : les « oui », par ordre alphabétique, avec une case à cocher
    $guests = array_values($yes);
    usort($guests, fn ($a, $b) => strcasecmp($a['name'], $b['name']));
    $acc = [$H(['Présent', 'Nom', 'Participants', 'Personnes', 'Téléphone', 'E-mail'])];
    foreach ($guests as $r) {
        $acc[] = [['☐', SbXlsx::S_NUM], [$r['name'], SbXlsx::S_BOLD], [$r['guests'], $T], [$nb($r), SbXlsx::S_NUM],
                  [$r['phone'], $T], [$r['email'], $T]];
    }
    $acc[] = [];
    $acc[] = [['', 0], ['Total attendu (estimation)', SbXlsx::S_BOLD], ['', 0], [$people, SbXlsx::S_BIG]];
    $x->addSheet('Accueil', $acc, ['widths' => [9, 28, 40, 11, 18, 32], 'freeze' => true, 'heights' => [0 => 26]]);

    // --- Invitations
    $inv = [$H(['État', 'Nom', 'E-mail', 'Langue', 'Invitée le', 'Envois', 'Dernier envoi', 'Réponse le'])];
    foreach ($invites as $i) {
        $inv[] = [[$stateLabel[$i['state']], $stateStyle[$i['state']]], [$i['name'], $T], [$i['email'], $T],
                  [strtoupper($i['lang']), SbXlsx::S_NUM], [$dt($i['first']), SbXlsx::S_DATE], [$i['sends'], SbXlsx::S_NUM],
                  [$dt($i['last']), SbXlsx::S_DATE], [$dt($i['answered']), SbXlsx::S_DATE]];
    }
    $x->addSheet('Invitations', $inv, ['widths' => [18, 26, 34, 9, 18, 9, 18, 18], 'freeze' => true, 'filter' => true, 'heights' => [0 => 26]]);

    // --- Réponses : les « oui » d'abord, puis les « non », du plus récent au plus ancien
    $resp = $rows;
    usort($resp, fn ($a, $b) => [$a['attending'] !== 'yes', $b['updated']] <=> [$b['attending'] !== 'yes', $a['updated']]);
    $rep = [$H(['Présence', 'Nom', 'E-mail', 'Téléphone', 'Personnes', 'Participants', 'Connu par', 'Commentaire', 'Langue', 'Reçu le'])];
    foreach ($resp as $r) {
        $isYes = $r['attending'] === 'yes';
        $rep[] = [[$isYes ? 'Oui' : 'Non', $isYes ? SbXlsx::S_YES : SbXlsx::S_NO], [$r['name'], SbXlsx::S_BOLD], [$r['email'], $T],
                  [$r['phone'], $T], [$isYes ? $nb($r) : 0, SbXlsx::S_NUM], [$r['guests'], $T],
                  [SB_HEARD[$r['heard']][1] ?? '', $T], [$r['comments'], $T], [strtoupper($r['lang']), SbXlsx::S_NUM],
                  [$dt($r['updated']), SbXlsx::S_DATE]];
    }
    $x->addSheet('Réponses', $rep, ['widths' => [11, 24, 32, 16, 11, 34, 14, 46, 9, 18], 'freeze' => true, 'filter' => true, 'heights' => [0 => 26]]);

    $x->download('two-cities-invites-' . date('Y-m-d') . '.xlsx');
}

// repli si l'extension zip manque sur le serveur : anciens exports CSV
if (($_GET['export'] ?? '') === 'invites') {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="invitations-two-cities-' . date('Y-m-d') . '.csv"');
    $out = fopen('php://output', 'w');
    fwrite($out, "\xEF\xBB\xBF");
    $safe = fn (string $v) => preg_match('/^[=+\-@\t\r]/', $v) ? "'" . $v : $v;
    fputcsv($out, ['État', 'Nom', 'E-mail', 'Langue', 'Invitée le', 'Dernier envoi', 'Envois', 'Réponse le'], ';', '"', '');
    foreach ($invites as $i) {
        fputcsv($out, array_map($safe, [SB_STATE[$i['state']][0], $i['name'], $i['email'], strtoupper($i['lang']),
            $xl($i['first']), $xl($i['last']), (string) $i['sends'], $xl($i['answered'])]), ';', '"', '');
    }
    exit;
}

// ------------------------------------------------------------ export CSV
if (in_array($_GET['export'] ?? '', ['csv', 'xlsx'], true)) {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="rsvp-two-cities-' . date('Y-m-d') . '.csv"');
    $out = fopen('php://output', 'w');
    fwrite($out, "\xEF\xBB\xBF");                       // accents corrects dans Excel
    $safe = fn (string $v) => preg_match('/^[=+\-@\t\r]/', $v) ? "'" . $v : $v;  // anti-formules
    fputcsv($out, ['Date', 'Présence', 'Nom', 'E-mail', 'Téléphone', 'Participants',
                   'Connu par', 'Commentaire', 'Langue'], ';', '"', '');
    foreach ($rows as $r) {
        fputcsv($out, array_map($safe, [
            $r['updated'], $r['attending'] === 'yes' ? 'Oui' : 'Non', $r['name'], $r['email'],
            $r['phone'], $r['guests'], SB_HEARD[$r['heard']][1] ?? '', $r['comments'], strtoupper($r['lang']),
        ]), ';', '"', '');
    }
    exit;
}

sb_page_top('Tableau de bord', 'list');

if (!sb_configured('smtp_pass')) {
    echo '<p class="alert warn">Le mot de passe SMTP n’est pas configuré : les e-mails partent via la fonction mail() du serveur, plus souvent classée en spam. Voir RSVP.md.</p>';
}
if ($flash) {
    echo '<p class="alert ok">' . sb_h($flash) . '</p>';
}
?>
<div class="head">
  <div><h1>Two Cities, One Friendship</h1><p class="muted">Vendredi 11 décembre 2026 · Glenview Mansion, Rockville</p></div>
</div>

<div class="stats">
  <div><b><?= $sentN ?></b><span>invitations envoyées</span></div>
  <div class="st-wait"><b><?= $count['pending'] ?></b><span>en attente de réponse</span></div>
  <div class="st-yes"><b><?= count($yes) ?></b><span>réponses « oui » · <?= $people ?> personne<?= $people > 1 ? 's' : '' ?> attendue<?= $people > 1 ? 's' : '' ?>*</span></div>
  <div><b><?= $no ?></b><span>réponses « non »</span></div>
</div>
<p class="muted small">* Estimation à partir des noms listés dans « participants » ; une réponse sans nom compte pour une personne. Les réponses comptent aussi les personnes qui ont répondu sans avoir reçu l’invitation par e-mail.</p>

<!-- ============================================================ invitations -->
<section class="sect" id="invitations">
  <div class="head">
    <div><h2>Invitations envoyées</h2>
      <p class="muted">L’état se met à jour dès que l’invité répond au formulaire avec la même adresse e-mail.</p></div>
    <div class="row">
      <?php foreach (['en' => 'EN', 'fr' => 'FR'] as $lg => $lbl): if ($pendingLang[$lg]): ?>
        <a class="btn" href="send.php?relance=<?= $lg ?>">Relancer <?= $pendingLang[$lg] === 1 ? '1 personne' : $pendingLang[$lg] . ' personnes' ?> en attente (<?= $lbl ?>)</a>
      <?php endif; endforeach ?>
      <?php if ($invites || $rows): ?><a class="btn ghost" href="?export=xlsx">Télécharger le fichier Excel</a><?php endif ?>
    </div>
  </div>

<?php if (!$invites): ?>
  <div class="card empty"><p>Aucune invitation envoyée pour l’instant.</p>
    <p class="muted">Les invitations parties depuis <a href="send.php">Envoyer l’invitation</a> apparaîtront ici, avec leur état.</p></div>
<?php else: ?>
  <div class="filters" role="group" aria-label="Filtrer les invitations">
    <button type="button" class="chip on" data-filter="all">Toutes <span><?= count($invites) ?></span></button>
    <button type="button" class="chip" data-filter="wait">En attente <span><?= $count['pending'] ?></span></button>
    <button type="button" class="chip" data-filter="yes">Oui <span><?= $count['yes'] ?></span></button>
    <button type="button" class="chip" data-filter="no">Non <span><?= $count['no'] ?></span></button>
    <?php if ($count['failed']): ?><button type="button" class="chip" data-filter="fail">Échec <span><?= $count['failed'] ?></span></button><?php endif ?>
  </div>
  <div class="card table">
    <table id="invTable">
      <thead><tr><th>État</th><th>Invité</th><th>Langue</th><th>Invitée le</th><th>Relances</th><th>Réponse le</th></tr></thead>
      <tbody>
      <?php foreach ($invites as $i): [$label, $cls] = SB_STATE[$i['state']]; ?>
        <tr data-state="<?= $cls ?>">
          <td><span class="pill <?= $cls ?>"><?= $label ?></span></td>
          <td><?= $i['name'] !== '' ? '<b>' . sb_h($i['name']) . '</b><br>' : '' ?><a href="mailto:<?= sb_h($i['email']) ?>"><?= sb_h($i['email']) ?></a>
            <?= $i['state'] === 'failed' && $i['error'] !== '' ? '<br><span class="small err">' . sb_h($i['error']) . '</span>' : '' ?></td>
          <td><?= strtoupper($i['lang']) ?></td>
          <td class="nowrap muted"><?= $fmt($i['first']) ?></td>
          <td class="muted"><?= $i['sends'] > 1 ? ($i['sends'] - 1) . ' · dernière le ' . $fmt($i['last']) : '—' ?></td>
          <td class="nowrap muted"><?= $fmt($i['answered']) ?></td>
        </tr>
      <?php endforeach ?>
      </tbody>
    </table>
  </div>
<?php endif ?>
</section>

<!-- ============================================================ réponses -->
<section class="sect" id="reponses">
  <div class="head">
    <div><h2>Réponses reçues</h2><p class="muted">Tout ce qui a été envoyé depuis le formulaire de la page de l’événement.</p></div>
    <?php if ($invites || $rows): ?><a class="btn ghost" href="?export=xlsx">Télécharger le fichier Excel</a><?php endif ?>
  </div>
<?php if (!$rows): ?>
  <div class="card empty"><p>Aucune réponse pour l’instant.</p>
    <p class="muted">Les réponses envoyées depuis <a href="/event-two-cities#rsvp" target="_blank">la page de l’événement</a> apparaîtront ici.</p></div>
<?php else: ?>
<div class="card table">
  <table>
    <thead><tr><th>Présence</th><th>Invité</th><th>Participants</th><th>Connu par</th><th>Commentaire</th><th>Reçu le</th><th></th></tr></thead>
    <tbody>
    <?php foreach ($rows as $r): ?>
      <tr>
        <td><span class="pill <?= $r['attending'] === 'yes' ? 'yes' : 'no' ?>"><?= $r['attending'] === 'yes' ? 'Oui' : 'Non' ?></span></td>
        <td><b><?= sb_h($r['name']) ?></b><br><a href="mailto:<?= sb_h($r['email']) ?>"><?= sb_h($r['email']) ?></a>
          <?= $r['phone'] !== '' ? '<br><span class="muted">' . sb_h($r['phone']) . '</span>' : '' ?></td>
        <td><?= $r['guests'] !== '' ? sb_h($r['guests']) : '<span class="muted">—</span>' ?></td>
        <td><?= sb_h(SB_HEARD[$r['heard']][1] ?? '—') ?></td>
        <td class="wrap"><?= $r['comments'] !== '' ? nl2br(sb_h($r['comments'])) : '<span class="muted">—</span>' ?></td>
        <td class="nowrap muted"><?= sb_h(date('d/m H:i', strtotime($r['updated']) ?: time())) ?><br><?= strtoupper(sb_h($r['lang'])) ?></td>
        <td><form method="post" data-confirm="Supprimer la réponse de <?= sb_h($r['name']) ?> ?">
          <input type="hidden" name="csrf" value="<?= sb_h(sb_csrf()) ?>"><input type="hidden" name="email" value="<?= sb_h($r['email']) ?>">
          <button class="link danger" name="action" value="delete">Supprimer</button></form></td>
      </tr>
    <?php endforeach ?>
    </tbody>
  </table>
</div>
<?php endif ?>
</section>
<?php
sb_page_bottom();
