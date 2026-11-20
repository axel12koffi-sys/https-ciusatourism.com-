<?php
/**
 * Administration : session, connexion, jeton anti-CSRF, mise en page.
 *
 *  - mot de passe lu dans sublime-private/config.php (jamais dans le dépôt)
 *  - 5 essais ratés en 15 minutes depuis une même IP = blocage 15 minutes
 *  - session limitée au chemin /admin, cookie HttpOnly + SameSite=Strict
 *  - inactivité de 8 heures = déconnexion
 */

declare(strict_types=1);
defined('SUBLIME') || exit;

require_once __DIR__ . '/boot.php';

const SB_IDLE      = 8 * 3600;
const SB_MAX_FAILS = 5;
const SB_FAIL_WIN  = 15 * 60;

function sb_admin_start(): void
{
    header('X-Robots-Tag: noindex, nofollow');
    header('X-Frame-Options: SAMEORIGIN');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: same-origin');
    header('Cache-Control: no-store');

    $https = (($_SERVER['HTTPS'] ?? '') !== '' && $_SERVER['HTTPS'] !== 'off')
          || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
    session_name('sbadmin');
    session_set_cookie_params([
        'lifetime' => 0, 'path' => '/admin', 'secure' => $https,
        'httponly' => true, 'samesite' => 'Strict',
    ]);
    session_start();

    if (!empty($_SESSION['ok']) && time() - (int) ($_SESSION['seen'] ?? 0) > SB_IDLE) {
        $_SESSION = [];
    }
    $_SESSION['seen'] = time();
    $_SESSION['csrf'] ??= bin2hex(random_bytes(16));
}

function sb_admin_logged(): bool
{
    return !empty($_SESSION['ok']);
}

function sb_csrf(): string
{
    return (string) $_SESSION['csrf'];
}

function sb_csrf_ok(): bool
{
    return hash_equals(sb_csrf(), (string) ($_POST['csrf'] ?? ''));
}

// ------------------------------------------------------------ connexion

function sb_fails_file(): string
{
    return sb_private_dir() . '/login-fails.json';
}

function sb_fails(): array
{
    $all = is_file(sb_fails_file()) ? json_decode((string) file_get_contents(sb_fails_file()), true) : [];
    $all = is_array($all) ? $all : [];
    return array_filter($all, fn ($v) => time() - (int) ($v['first'] ?? 0) < SB_FAIL_WIN);
}

/** @return string message d'erreur, '' si connecté */
function sb_login(string $password): string
{
    if (!sb_configured('admin_password')) {
        return 'Le mot de passe d’administration n’est pas encore défini (voir RSVP.md).';
    }
    $key   = hash('sha256', sb_ip());
    $fails = sb_fails();
    if (($fails[$key]['n'] ?? 0) >= SB_MAX_FAILS) {
        return 'Trop d’essais. Réessayez dans 15 minutes.';
    }
    if (hash_equals((string) sb_config()['admin_password'], $password)) {
        unset($fails[$key]);
        if (sb_ensure_private()) {
            @file_put_contents(sb_fails_file(), json_encode($fails), LOCK_EX);
        }
        session_regenerate_id(true);
        $_SESSION['ok'] = true;
        return '';
    }
    $fails[$key] = ['n' => ($fails[$key]['n'] ?? 0) + 1, 'first' => $fails[$key]['first'] ?? time()];
    if (sb_ensure_private()) {
        @file_put_contents(sb_fails_file(), json_encode($fails), LOCK_EX);
    }
    sleep(1);
    return 'Mot de passe incorrect.';
}

function sb_logout(): void
{
    $_SESSION = [];
    session_destroy();
}

// ------------------------------------------------------------ mise en page

function sb_page_top(string $title, string $active = ''): void
{
    $nav = '';
    if (sb_admin_logged()) {
        $tab = fn ($href, $label, $id) => '<a href="' . $href . '"' . ($active === $id ? ' class="on"' : '') . '>' . $label . '</a>';
        $nav = '<nav>' . $tab('./', 'Réponses RSVP', 'list') . $tab('send.php', 'Envoyer l’invitation', 'send')
             . '<form method="post" action="./"><input type="hidden" name="csrf" value="' . sb_h(sb_csrf()) . '">'
             . '<button name="action" value="logout" class="link">Déconnexion</button></form></nav>';
    }
    echo '<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">'
       . '<meta name="viewport" content="width=device-width, initial-scale=1">'
       . '<meta name="robots" content="noindex, nofollow">'
       . '<title>' . sb_h($title) . ' — Sublime CI-USA</title>'
       . '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
       . '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
       . '<link rel="stylesheet" href="admin.css"></head><body>'
       . '<header class="top"><div class="in"><a class="brand" href="./"><img src="/assets/img/logo-mark.png" alt="">'
       . '<span>Sublime CI-USA<small>Administration</small></span></a>' . $nav . '</div></header><main class="in">';
}

function sb_page_bottom(): void
{
    echo '</main><script src="admin.js"></script></body></html>';
}

function sb_login_page(string $error = ''): never
{
    sb_page_top('Connexion');
    echo '<form class="card login" method="post" action="./">'
       . '<h1>Connexion</h1><p class="muted">Réservé à l’équipe Sublime CI-USA.</p>'
       . ($error ? '<p class="alert ko">' . sb_h($error) . '</p>' : '')
       . '<input type="hidden" name="csrf" value="' . sb_h(sb_csrf()) . '">'
       . '<label for="pw">Mot de passe</label><input id="pw" type="password" name="password" autocomplete="current-password" required autofocus>'
       . '<button class="btn" name="action" value="login">Se connecter</button></form>';
    sb_page_bottom();
    exit;
}

/** Bloque toute page tant que l'utilisateur n'est pas connecté. */
function sb_require_login(): void
{
    if (!sb_admin_logged()) {
        if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && str_contains((string) ($_SERVER['HTTP_ACCEPT'] ?? ''), 'json')) {
            http_response_code(401);
            header('Content-Type: application/json');
            exit(json_encode(['ok' => false, 'error' => 'login']));
        }
        header('Location: ./');
        exit;
    }
}
