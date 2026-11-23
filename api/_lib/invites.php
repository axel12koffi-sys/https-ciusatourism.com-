<?php
/**
 * Journal des invitations envoyées, croisé avec les réponses RSVP.
 *
 * Chaque envoi (réussi ou non) est une ligne du fichier
 * sublime-private/sent-two-cities.log. Les envois de test sont ignorés.
 * L'état d'un invité se déduit de ce journal et de rsvp.csv :
 *   yes / no   il a répondu au formulaire avec la même adresse
 *   pending    l'invitation est partie, pas encore de réponse
 *   failed     aucun envoi n'a abouti
 */

declare(strict_types=1);
defined('SUBLIME') || exit;

require_once __DIR__ . '/store.php';

const SB_CAMPAIGN = 'two-cities';

function sb_sent_file(): string
{
    return sb_private_dir() . '/sent-' . SB_CAMPAIGN . '.log';
}

/** @return list<array<string,mixed>> lignes du journal, hors tests */
function sb_sent_entries(): array
{
    $out = [];
    if (is_file(sb_sent_file())) {
        foreach (file(sb_sent_file(), FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [] as $l) {
            $e = json_decode($l, true);
            if (is_array($e) && empty($e['test']) && !empty($e['email'])) {
                $out[] = $e;
            }
        }
    }
    return $out;
}

/** @return array<string,string> e-mail => date du dernier envoi réussi */
function sb_already_sent(): array
{
    $done = [];
    foreach (sb_sent_entries() as $e) {
        if (($e['status'] ?? '') === 'sent') {
            $done[strtolower((string) $e['email'])] = (string) $e['t'];
        }
    }
    return $done;
}

/**
 * Un invité par adresse, avec son état.
 * @return list<array{email:string,name:string,lang:string,first:string,last:string,sends:int,error:string,state:string,answered:string}>
 */
function sb_invites(): array
{
    $inv = [];
    foreach (sb_sent_entries() as $e) {
        $k = strtolower((string) $e['email']);
        $i = $inv[$k] ?? ['email' => $k, 'name' => '', 'lang' => 'en', 'first' => '', 'last' => '',
                          'sends' => 0, 'error' => '', 'state' => 'failed', 'answered' => ''];
        if (!empty($e['name'])) {
            $i['name'] = (string) $e['name'];
        }
        $i['lang'] = ($e['lang'] ?? '') === 'fr' ? 'fr' : 'en';
        if (($e['status'] ?? '') === 'sent') {
            $i['sends']++;
            $i['first'] = $i['first'] ?: (string) $e['t'];
            $i['last']  = (string) $e['t'];
            $i['error'] = '';
            $i['state'] = 'pending';
        } elseif ($i['sends'] === 0) {
            $i['error'] = (string) ($e['error'] ?? '');
        }
        $inv[$k] = $i;
    }

    $rsvp = [];
    foreach (sb_rsvp_read() as $r) {
        $rsvp[strtolower($r['email'])] = $r;
    }
    foreach ($inv as $k => $i) {
        if (isset($rsvp[$k])) {
            $inv[$k]['state']    = $rsvp[$k]['attending'] === 'yes' ? 'yes' : 'no';
            $inv[$k]['answered'] = $rsvp[$k]['updated'];
        }
    }

    // en attente d'abord, puis échecs, puis réponses ; dans chaque groupe, envoi le plus récent en haut
    $rank = ['pending' => 0, 'failed' => 1, 'yes' => 2, 'no' => 3];
    $list = array_values($inv);
    usort($list, fn ($a, $b) => [$rank[$a['state']], $b['last']] <=> [$rank[$b['state']], $a['last']]);
    return $list;
}
