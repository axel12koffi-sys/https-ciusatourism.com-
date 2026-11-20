<?php
/**
 * Réponses RSVP : un fichier CSV hors du web, une ligne par invité.
 * Un invité qui répond deux fois (même e-mail) met à jour sa ligne au
 * lieu d'en créer une seconde : la liste reste juste s'il change d'avis.
 */

declare(strict_types=1);
defined('SUBLIME') || exit;

const SB_RSVP_COLS = ['updated', 'lang', 'attending', 'name', 'email',
                      'phone', 'guests', 'heard', 'comments', 'ip'];

function sb_rsvp_file(): string
{
    return sb_private_dir() . '/rsvp.csv';
}

/** @return list<array<string,string>> du plus récent au plus ancien */
function sb_rsvp_all(): array
{
    $rows = sb_rsvp_read();
    usort($rows, fn ($a, $b) => strcmp($b['updated'], $a['updated']));
    return $rows;
}

function sb_rsvp_read(): array
{
    $f = sb_rsvp_file();
    if (!is_file($f) || !($h = fopen($f, 'r'))) {
        return [];
    }
    flock($h, LOCK_SH);
    $rows = [];
    $cols = fgetcsv($h, 0, ',', '"', '');
    while ($cols && ($r = fgetcsv($h, 0, ',', '"', '')) !== false) {
        if (count($r) === count($cols)) {
            $rows[] = array_combine($cols, $r);
        }
    }
    flock($h, LOCK_UN);
    fclose($h);
    return $rows;
}

/** @return 'new'|'updated'|false */
function sb_rsvp_upsert(array $row): string|false
{
    return sb_rsvp_write(function (array $rows) use ($row) {
        $key = strtolower($row['email']);
        foreach ($rows as $i => $r) {
            if (strtolower($r['email']) === $key) {
                $rows[$i] = $row;
                return [$rows, 'updated'];
            }
        }
        $rows[] = $row;
        return [$rows, 'new'];
    });
}

function sb_rsvp_delete(string $email): bool
{
    return (bool) sb_rsvp_write(function (array $rows) use ($email) {
        $key  = strtolower($email);
        $keep = array_values(array_filter($rows, fn ($r) => strtolower($r['email']) !== $key));
        return [$keep, count($keep) !== count($rows)];
    });
}

/** Lecture-modification-écriture sous verrou exclusif. */
function sb_rsvp_write(callable $change): mixed
{
    if (!sb_ensure_private()) {
        return false;
    }
    $lock = fopen(sb_private_dir() . '/rsvp.lock', 'c');
    if (!$lock || !flock($lock, LOCK_EX)) {
        return false;
    }
    try {
        [$rows, $result] = $change(sb_rsvp_read());
        $tmp = sb_rsvp_file() . '.tmp';
        $h = fopen($tmp, 'w');
        if (!$h) {
            return false;
        }
        fputcsv($h, SB_RSVP_COLS, ',', '"', '');
        foreach ($rows as $r) {
            fputcsv($h, array_map(fn ($c) => (string) ($r[$c] ?? ''), SB_RSVP_COLS), ',', '"', '');
        }
        fclose($h);
        @chmod($tmp, 0600);
        return rename($tmp, sb_rsvp_file()) ? $result : false;
    } finally {
        flock($lock, LOCK_UN);
        fclose($lock);
    }
}

/** Libellés lisibles pour « How did you hear about this event? » */
const SB_HEARD = [
    'website'    => ['Website', 'Site web'],
    'friend'     => ['Friend', 'Un proche'],
    'newsletter' => ['Newsletter', 'Newsletter'],
    'ad'         => ['Advertisement', 'Publicité'],
];
