<?php
/**
 * SUBLIME CI-USA — liste des réponses RSVP.
 * Connexion, tableau, export CSV (Excel), suppression d'une réponse.
 */

declare(strict_types=1);
define('SUBLIME', 1);
require __DIR__ . '/../api/_lib/admin.php';
require __DIR__ . '/../api/_lib/store.php';

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

// ------------------------------------------------------------ export CSV
if (($_GET['export'] ?? '') === 'csv') {
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

// ------------------------------------------------------------ chiffres
$yes = array_filter($rows, fn ($r) => $r['attending'] === 'yes');
$no  = count($rows) - count($yes);
/* nombre de personnes : les noms listés, ou 1 si le champ est vide */
$people = 0;
foreach ($yes as $r) {
    $names = array_filter(array_map('trim', preg_split('/[,;\n]| and | et |&/i', $r['guests']) ?: []));
    $people += max(1, count($names));
}

sb_page_top('Réponses RSVP', 'list');

if (!sb_configured('smtp_pass')) {
    echo '<p class="alert warn">Le mot de passe SMTP n’est pas configuré : les e-mails partent via la fonction mail() du serveur, plus souvent classée en spam. Voir RSVP.md.</p>';
}
if ($flash) {
    echo '<p class="alert ok">' . sb_h($flash) . '</p>';
}
?>
<div class="head">
  <div><h1>Two Cities, One Friendship</h1><p class="muted">Vendredi 11 décembre 2026 · Glenview Mansion, Rockville</p></div>
  <?php if ($rows): ?><a class="btn ghost" href="?export=csv">Exporter (Excel)</a><?php endif ?>
</div>

<div class="stats">
  <div><b><?= count($yes) ?></b><span>réponses « oui »</span></div>
  <div><b><?= $people ?></b><span>personnes attendues*</span></div>
  <div><b><?= $no ?></b><span>réponses « non »</span></div>
  <div><b><?= count($rows) ?></b><span>réponses au total</span></div>
</div>
<p class="muted small">* Estimation à partir des noms listés dans « participants » ; une réponse sans nom compte pour une personne.</p>

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
<?php endif;
sb_page_bottom();
