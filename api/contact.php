<?php
/**
 * SUBLIME CI-USA — formulaire de contact.
 *
 * Défenses en place, de la moins à la plus intrusive :
 *   1. méthode POST obligatoire
 *   2. origine de la requête vérifiée (le formulaire doit venir du site)
 *   3. pot de miel : un champ caché que seuls les robots remplissent
 *   4. piège temporel : moins de 3 secondes entre l'affichage et l'envoi
 *   5. limite de 5 envois par heure et par IP
 *   6. longueurs maximales, pour éviter les envois massifs
 *   7. filtrage des liens : un message bourré d'URLs est du spam
 *   8. nettoyage des en-têtes, contre l'injection de destinataires
 *
 * Chaque demande est journalisée dans storage/requests.log : si un mail
 * se perd en route, la demande reste récupérable.
 */

declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

// ------------------------------------------------------------ réglages
const TO           = 'tourism@ambaciusa.org';
const FROM         = 'no-reply@ciusatourism.com'; // doit appartenir au domaine
const SUBJECT      = 'Nouvelle demande de voyage — ciusatourism.com';
const LOG_FILE     = __DIR__ . '/../storage/requests.log';
const MAX_PER_HOUR = 5;
const MIN_SECONDS  = 3;
const MAX_LINKS    = 2;

const LIMITS = [
    'first_name' => 60, 'last_name' => 60, 'email' => 120,
    'phone' => 40, 'trip_type' => 60, 'dates' => 80, 'message' => 4000,
];

function reject(int $code, string $err, array $extra = []): never
{
    http_response_code($code);
    exit(json_encode(['ok' => false, 'error' => $err] + $extra));
}

// ------------------------------------------------------------ 1. méthode
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    reject(405, 'method');
}

// ------------------------------------------------------------ 2. origine
$host   = $_SERVER['HTTP_HOST'] ?? '';
$origin = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
if ($origin !== '' && stripos((string) parse_url($origin, PHP_URL_HOST), $host) === false) {
    reject(403, 'origin');
}

// ------------------------------------------------------------ 3. pot de miel
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    exit(json_encode(['ok' => true])); // on fait semblant d'accepter
}

// ------------------------------------------------------------ 4. piège temporel
$started = (int) ($_POST['started'] ?? 0);
if ($started > 0 && (microtime(true) * 1000 - $started) < MIN_SECONDS * 1000) {
    exit(json_encode(['ok' => true]));
}

// ------------------------------------------------------------ 5. limite par IP
$ip    = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$stamp = sys_get_temp_dir() . '/ciusa_' . hash('sha256', $ip);
$fresh = is_file($stamp) && (time() - filemtime($stamp) < 3600);
$hits  = $fresh ? (int) file_get_contents($stamp) : 0;
if ($hits >= MAX_PER_HOUR) {
    reject(429, 'rate');
}
file_put_contents($stamp, (string) ($hits + 1));

// ------------------------------------------------------------ validation
/* certains hébergements mutualisés n'ont pas l'extension mbstring :
   on retombe sur substr, quitte à couper un caractère accentué. */
function cut(string $v, int $max): string
{
    return function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max);
}

function field(string $k, int $max): string
{
    $v = (string) ($_POST[$k] ?? '');
    $v = str_replace(["\r", "\0"], '', $v);          // anti-injection d'en-têtes
    $v = strip_tags($v);
    return cut(trim($v), $max);
}

$data = [];
foreach (LIMITS as $k => $max) {
    $data[$k] = field($k, $max);
}

$errors = [];
foreach (['first_name', 'last_name', 'email', 'trip_type', 'message'] as $f) {
    if ($data[$f] === '') $errors[] = $f;
}
if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'email';
if (preg_match('/[\r\n]/', $data['email']))              $errors[] = 'email';

if ($errors) {
    reject(422, 'fields', ['fields' => array_values(array_unique($errors))]);
}

// ------------------------------------------------------------ 7. anti-spam contenu
if (preg_match_all('#https?://#i', $data['message']) > MAX_LINKS) {
    exit(json_encode(['ok' => true]));
}

// ------------------------------------------------------------ envoi
$body = "Nouvelle demande depuis ciusatourism.com\n"
      . str_repeat('-', 46) . "\n"
      . "Nom       : {$data['first_name']} {$data['last_name']}\n"
      . "Email     : {$data['email']}\n"
      . "Téléphone : " . ($data['phone'] ?: '—') . "\n"
      . "Voyage    : {$data['trip_type']}\n"
      . "Dates     : " . ($data['dates'] ?: '—') . "\n"
      . str_repeat('-', 46) . "\n\n"
      . $data['message'] . "\n\n"
      . str_repeat('-', 46) . "\n"
      . 'IP : ' . $ip . ' — ' . date('d/m/Y H:i') . "\n";

$headers = implode("\r\n", [
    'From: Sublime CI-USA <' . FROM . '>',
    'Reply-To: ' . $data['first_name'] . ' ' . $data['last_name'] . ' <' . $data['email'] . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'MIME-Version: 1.0',
]);

$sent = @mail(TO, '=?UTF-8?B?' . base64_encode(SUBJECT) . '?=', $body, $headers, '-f' . FROM);

@mkdir(dirname(LOG_FILE), 0755, true);
@file_put_contents(
    LOG_FILE,
    date('c') . "\t" . ($sent ? 'sent' : 'FAILED') . "\t"
        . json_encode($data, JSON_UNESCAPED_UNICODE) . "\n",
    FILE_APPEND | LOCK_EX
);

if (!$sent) {
    reject(500, 'mail');
}

echo json_encode(['ok' => true]);
