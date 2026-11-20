<?php
/**
 * SUBLIME CI-USA — socle commun (RSVP, administration, envoi).
 *
 * Tout ce qui est privé vit HORS du site public, dans :
 *     /home/ciusatou/sublime-private/
 *         config.php      mots de passe (SMTP, administration)
 *         rsvp.csv        réponses des invités
 *         sent-*.log      journal des invitations envoyées
 *
 * Ce dossier n'est ni dans public_html, ni dans le dépôt GitHub : il
 * n'est accessible ni depuis le web, ni depuis le code source publié.
 */

declare(strict_types=1);
defined('SUBLIME') || exit;

// l'événement et l'équipe sont à Washington : dates affichées à l'heure de l'Est
date_default_timezone_set('America/New_York');

const SB_DEFAULTS = [
    'smtp_host'      => 'mail.ciusatourism.com',
    'smtp_port'      => 465,
    'smtp_secure'    => 'ssl',            // ssl (465), tls (587) ou '' (aucun)
    'smtp_verify'    => true,             // vérifier le certificat du serveur
    'smtp_user'      => 'invitation@ciusatourism.com',
    'smtp_pass'      => '',
    'from_email'     => 'invitation@ciusatourism.com',
    'from_name'      => 'Sublime CI-USA',
    'reply_to'       => 'tourism@ambaciusa.org',
    'notify_to'      => 'tourism@ambaciusa.org',
    'admin_password' => '',
    'send_delay'     => 4,                // secondes entre deux invitations
    'site_url'       => 'https://ciusatourism.com',
];

function sb_private_dir(): string
{
    $env = getenv('SUBLIME_PRIVATE');           // utilisé pour les tests
    if ($env) {
        return rtrim($env, '/');
    }
    $root = rtrim((string) ($_SERVER['DOCUMENT_ROOT'] ?? ''), '/');
    return dirname($root !== '' ? $root : dirname(__DIR__, 2)) . '/sublime-private';
}

function sb_config(): array
{
    static $cfg = null;
    if ($cfg === null) {
        $file = sb_private_dir() . '/config.php';
        $own  = is_file($file) ? require $file : [];
        $cfg  = (is_array($own) ? $own : []) + SB_DEFAULTS;
    }
    return $cfg;
}

/** Le dossier privé existe et le mot de passe a été changé. */
function sb_configured(string $key): bool
{
    $v = (string) (sb_config()[$key] ?? '');
    return $v !== '' && stripos($v, 'CHANGE') === false;
}

function sb_ensure_private(): bool
{
    $dir = sb_private_dir();
    if (!is_dir($dir) && !@mkdir($dir, 0700, true)) {
        return false;
    }
    return is_writable($dir);
}

/* certains hébergements n'ont pas mbstring */
function sb_cut(string $v, int $max): string
{
    return function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max);
}

/** Texte d'un champ : sans balises, sans retours chariot parasites. */
function sb_clean(string $v, int $max, bool $multiline = false): string
{
    $v = str_replace(["\0", "\r"], '', $v);
    if (!$multiline) {
        $v = str_replace("\n", ' ', $v);
    }
    return sb_cut(trim(strip_tags($v)), $max);
}

function sb_h(string $v): string
{
    return htmlspecialchars($v, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function sb_ip(): string
{
    return (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
}

/** Journal des incidents (envois ratés, etc.), hors du web. */
function sb_log(string $file, array $entry): void
{
    if (!sb_ensure_private()) {
        return;
    }
    @file_put_contents(
        sb_private_dir() . '/' . $file,
        json_encode(['t' => date('c')] + $entry, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n",
        FILE_APPEND | LOCK_EX
    );
}
