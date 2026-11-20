<?php
/**
 * SUBLIME CI-USA — réponses au formulaire RSVP de la page événement.
 *
 * Mêmes défenses que le formulaire de contact (méthode, origine, pot de
 * miel, piège temporel, limite par IP, longueurs, liens), puis :
 *   1. la réponse est enregistrée (hors du web) — c'est ce qui compte ;
 *   2. l'équipe reçoit une alerte ;
 *   3. l'invité reçoit une confirmation.
 * Si un e-mail échoue, la réponse reste enregistrée et visible dans
 * l'administration : rien n'est perdu.
 */

declare(strict_types=1);
define('SUBLIME', 1);
require __DIR__ . '/_lib/boot.php';
require __DIR__ . '/_lib/store.php';
require __DIR__ . '/_lib/mailer.php';
require __DIR__ . '/_lib/templates.php';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

const MAX_PER_HOUR = 6;
const MIN_SECONDS  = 3;
const MAX_LINKS    = 2;

function out(int $code, array $data): never
{
    http_response_code($code);
    exit(json_encode($data));
}

// ------------------------------------------------------------ 1. méthode
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    out(405, ['ok' => false, 'error' => 'method']);
}

// ------------------------------------------------------------ 2. origine
$host   = (string) ($_SERVER['HTTP_HOST'] ?? '');
$origin = (string) ($_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? ''));
if ($origin !== '' && stripos((string) parse_url($origin, PHP_URL_HOST), preg_replace('/:\d+$/', '', $host)) === false) {
    out(403, ['ok' => false, 'error' => 'origin']);
}

// ------------------------------------------------------------ 3. pot de miel
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    out(200, ['ok' => true, 'attending' => 'yes']);
}

// ------------------------------------------------------------ 4. piège temporel
$started = (int) ($_POST['started'] ?? 0);
if ($started > 0 && (microtime(true) * 1000 - $started) < MIN_SECONDS * 1000) {
    out(200, ['ok' => true, 'attending' => 'yes']);
}

// ------------------------------------------------------------ 5. limite par IP
$stamp = sys_get_temp_dir() . '/sb_rsvp_' . hash('sha256', sb_ip());
$fresh = is_file($stamp) && (time() - filemtime($stamp) < 3600);
$hits  = $fresh ? (int) file_get_contents($stamp) : 0;
if ($hits >= MAX_PER_HOUR) {
    out(429, ['ok' => false, 'error' => 'rate']);
}
@file_put_contents($stamp, (string) ($hits + 1));

// ------------------------------------------------------------ 6. validation
$r = [
    'updated'   => date('Y-m-d H:i:s'),
    'lang'      => ($_POST['lang'] ?? '') === 'fr' ? 'fr' : 'en',
    'attending' => (string) ($_POST['attending'] ?? ''),
    'name'      => sb_clean((string) ($_POST['name'] ?? ''), 100),
    'email'     => strtolower(sb_clean((string) ($_POST['email'] ?? ''), 160)),
    'phone'     => sb_clean((string) ($_POST['phone'] ?? ''), 40),
    'guests'    => sb_clean((string) ($_POST['guests'] ?? ''), 500),
    'heard'     => (string) ($_POST['heard'] ?? ''),
    'comments'  => sb_clean((string) ($_POST['comments'] ?? ''), 3000, true),
    'ip'        => sb_ip(),
];

$bad = [];
if (!in_array($r['attending'], ['yes', 'no'], true)) $bad[] = 'attending';
if ($r['name'] === '')                               $bad[] = 'name';
if (!filter_var($r['email'], FILTER_VALIDATE_EMAIL)) $bad[] = 'email';
if (!isset(SB_HEARD[$r['heard']]))                   $r['heard'] = '';
if ($bad) {
    out(422, ['ok' => false, 'error' => 'fields', 'fields' => $bad]);
}

// ------------------------------------------------------------ 7. liens
if (preg_match_all('#https?://#i', $r['comments'] . ' ' . $r['guests']) > MAX_LINKS) {
    out(200, ['ok' => true, 'attending' => $r['attending']]);
}

// ------------------------------------------------------------ enregistrement
$status = sb_rsvp_upsert($r);
if ($status === false) {
    sb_log('errors.log', ['where' => 'rsvp-store', 'email' => $r['email']]);
    out(500, ['ok' => false, 'error' => 'store']);
}

// ------------------------------------------------------------ e-mails
$cfg    = sb_config();
$mailer = new SbMailer($cfg);

$n = sb_notification($r, $status);
if (!$mailer->send((string) $cfg['notify_to'], 'Sublime CI-USA', $n['subject'], $n['html'], $n['text'],
                   ['reply_to' => $r['email']])) {
    sb_log('errors.log', ['where' => 'rsvp-notify', 'email' => $r['email'], 'error' => $mailer->error]);
}

$c = sb_confirmation($r['lang'], $r['name'], $r['attending'] === 'yes');
$confirmed = $mailer->send($r['email'], $r['name'], $c['subject'], $c['html'], $c['text'],
                           ['reply_to' => (string) $cfg['reply_to']]);
if (!$confirmed) {
    sb_log('errors.log', ['where' => 'rsvp-confirm', 'email' => $r['email'], 'error' => $mailer->error]);
}

out(200, ['ok' => true, 'attending' => $r['attending'], 'mailed' => $confirmed]);
