<?php
/**
 * Envoi d'e-mails par SMTP authentifié, sans bibliothèque externe.
 *
 * Pourquoi pas mail() : un message envoyé par l'adresse réelle
 * invitation@ciusatourism.com, authentifiée, a beaucoup plus de chances
 * d'arriver en boîte de réception qu'un message anonyme du serveur.
 * mail() reste le repli si le mot de passe SMTP n'est pas configuré.
 *
 * Chaque message part en deux versions (texte + HTML) : les filtres
 * anti-spam se méfient des messages uniquement HTML.
 */

declare(strict_types=1);
defined('SUBLIME') || exit;

final class SbMailer
{
    public string $error = '';
    /** @var resource|null */
    private $sock = null;

    public function __construct(private array $cfg)
    {
    }

    /**
     * @param array{reply_to?:string, unsubscribe?:bool} $opt
     */
    public function send(string $toEmail, string $toName, string $subject,
                         string $html, string $text, array $opt = []): bool
    {
        $this->error = '';
        $toEmail = $this->line($toEmail);
        if (!filter_var($toEmail, FILTER_VALIDATE_EMAIL)) {
            $this->error = 'adresse invalide';
            return false;
        }

        $from   = $this->line((string) $this->cfg['from_email']);
        $domain = substr((string) strrchr($from, '@'), 1) ?: 'localhost';
        $bound  = 'sb_' . bin2hex(random_bytes(12));

        $head = [
            'Date: ' . date('r'),
            'From: ' . $this->addr((string) $this->cfg['from_name'], $from),
            'To: ' . $this->addr($toName, $toEmail),
            'Subject: ' . $this->enc($subject),
            'Message-ID: <' . bin2hex(random_bytes(16)) . '@' . $domain . '>',
            'MIME-Version: 1.0',
            'Content-Type: multipart/alternative; boundary="' . $bound . '"',
        ];
        $reply = $this->line((string) ($opt['reply_to'] ?? ''));
        if ($reply !== '' && filter_var($reply, FILTER_VALIDATE_EMAIL)) {
            $head[] = 'Reply-To: ' . $reply;
        }
        if (!empty($opt['unsubscribe'])) {
            $head[] = 'List-Unsubscribe: <mailto:' . $from . '?subject=unsubscribe>';
        }

        $body = "--$bound\r\n"
              . "Content-Type: text/plain; charset=UTF-8\r\n"
              . "Content-Transfer-Encoding: base64\r\n\r\n"
              . chunk_split(base64_encode($text), 76, "\r\n")
              . "--$bound\r\n"
              . "Content-Type: text/html; charset=UTF-8\r\n"
              . "Content-Transfer-Encoding: base64\r\n\r\n"
              . chunk_split(base64_encode($html), 76, "\r\n")
              . "--$bound--\r\n";

        if ((string) ($this->cfg['smtp_pass'] ?? '') === '') {
            return $this->viaMail($toEmail, $subject, $head, $body, $from);
        }

        try {
            $this->open();
            $this->cmd('MAIL FROM:<' . $from . '>', [250]);
            $this->cmd('RCPT TO:<' . $toEmail . '>', [250, 251]);
            $this->cmd('DATA', [354]);
            $data = implode("\r\n", $head) . "\r\n\r\n" . $body;
            $data = preg_replace('/^\./m', '..', $data);   // dot-stuffing
            $this->write($data . "\r\n.");
            $this->expect([250]);
            $this->cmd('QUIT', [221]);
            return true;
        } catch (Throwable $e) {
            $this->error = $e->getMessage();
            return false;
        } finally {
            if ($this->sock) {
                @fclose($this->sock);
                $this->sock = null;
            }
        }
    }

    // ------------------------------------------------------------ SMTP

    private function open(): void
    {
        $host   = (string) $this->cfg['smtp_host'];
        $port   = (int) $this->cfg['smtp_port'];
        $secure = strtolower((string) $this->cfg['smtp_secure']);
        $verify = (bool) $this->cfg['smtp_verify'];

        $ctx = stream_context_create(['ssl' => [
            'verify_peer'       => $verify,
            'verify_peer_name'  => $verify,
            'allow_self_signed' => !$verify,
            'SNI_enabled'       => true,
            'peer_name'         => $host,
        ]]);
        $remote = ($secure === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port;
        $sock = @stream_socket_client($remote, $no, $str, 20, STREAM_CLIENT_CONNECT, $ctx);
        if (!$sock) {
            throw new RuntimeException("connexion impossible à $remote ($str)");
        }
        stream_set_timeout($sock, 30);
        $this->sock = $sock;

        $helo = substr((string) strrchr((string) $this->cfg['from_email'], '@'), 1) ?: 'localhost';
        $this->expect([220]);
        $this->cmd('EHLO ' . $helo, [250]);

        if ($secure === 'tls') {
            $this->cmd('STARTTLS', [220]);
            if (!@stream_socket_enable_crypto($sock, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new RuntimeException('STARTTLS refusé');
            }
            $this->cmd('EHLO ' . $helo, [250]);
        }

        $this->cmd('AUTH LOGIN', [334]);
        $this->cmd(base64_encode((string) $this->cfg['smtp_user']), [334]);
        $this->cmd(base64_encode((string) $this->cfg['smtp_pass']), [235], 'mot de passe SMTP refusé');
    }

    private function cmd(string $c, array $ok, string $why = ''): void
    {
        $this->write($c);
        $this->expect($ok, $why);
    }

    private function write(string $s): void
    {
        if (fwrite($this->sock, $s . "\r\n") === false) {
            throw new RuntimeException('écriture SMTP impossible');
        }
    }

    private function expect(array $ok, string $why = ''): void
    {
        $resp = '';
        while (($line = fgets($this->sock, 1024)) !== false) {
            $resp .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') {
                break;
            }
        }
        $code = (int) substr($resp, 0, 3);
        if (!in_array($code, $ok, true)) {
            $msg = trim(preg_replace('/\s+/', ' ', $resp)) ?: 'pas de réponse du serveur';
            throw new RuntimeException(($why ? "$why — " : '') . $msg);
        }
    }

    // ------------------------------------------------------------ repli

    private function viaMail(string $to, string $subject, array $head, string $body, string $from): bool
    {
        // mail() ajoute lui-même To et Subject
        $head = array_values(array_filter($head, fn ($h) =>
            !str_starts_with($h, 'To:') && !str_starts_with($h, 'Subject:')));
        $ok = @mail($to, $this->enc($subject), $body, implode("\r\n", $head), '-f' . $from);
        if (!$ok) {
            $this->error = 'mail() a échoué (SMTP non configuré)';
        }
        return $ok;
    }

    // ------------------------------------------------------------ en-têtes

    private function line(string $v): string
    {
        return trim(str_replace(["\r", "\n", "\0"], '', $v));
    }

    private function enc(string $v): string
    {
        $v = $this->line($v);
        return preg_match('/[^\x20-\x7E]/', $v) ? '=?UTF-8?B?' . base64_encode($v) . '?=' : $v;
    }

    private function addr(string $name, string $email): string
    {
        $name = $this->line($name);
        if ($name === '') {
            return '<' . $email . '>';
        }
        if (preg_match('/[^\x20-\x7E]/', $name)) {
            return $this->enc($name) . ' <' . $email . '>';
        }
        return '"' . addcslashes($name, '"\\') . '" <' . $email . '>';
    }
}
