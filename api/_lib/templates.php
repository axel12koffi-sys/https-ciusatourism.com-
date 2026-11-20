<?php
/**
 * Contenu des e-mails : confirmation à l'invité, alerte à l'équipe,
 * invitation personnalisée et sa version texte.
 *
 * L'invitation elle-même est le fichier public_html/email/invitation-
 * two-cities-{en,fr}.html : un seul gabarit, utilisé à la fois par la page
 * d'envoi et par quiconque le copie-colle dans Gmail.
 */

declare(strict_types=1);
defined('SUBLIME') || exit;

const SB_EVENT = [
    'title'   => 'Two Cities, One Friendship',
    'slug'    => 'event-two-cities',
    'venue'   => 'Glenview Mansion',
    'address' => '603 Edmonston Drive, Rockville, MD 20851',
    'en'      => ['date' => 'Friday, December 11, 2026', 'time' => '6:00 PM – 10:00 PM'],
    'fr'      => ['date' => 'Vendredi 11 décembre 2026', 'time' => '18h00 – 22h00'],
    // Google Agenda : heure locale de Rockville
    'cal'     => ['start' => '20261211T180000', 'end' => '20261211T220000', 'tz' => 'America/New_York'],
];

function sb_event_url(string $lang): string
{
    return rtrim((string) sb_config()['site_url'], '/') . ($lang === 'fr' ? '/fr/' : '/') . SB_EVENT['slug'];
}

function sb_calendar_url(): string
{
    $e = SB_EVENT;
    return 'https://calendar.google.com/calendar/render?' . http_build_query([
        'action'   => 'TEMPLATE',
        'text'     => $e['title'],
        'dates'    => $e['cal']['start'] . '/' . $e['cal']['end'],
        'ctz'      => $e['cal']['tz'],
        'location' => $e['venue'] . ', ' . $e['address'],
        'details'  => sb_event_url('en'),
    ], '', '&', PHP_QUERY_RFC3986);
}

// ============================================================ CONFIRMATION

/** @return array{subject:string, html:string, text:string} */
function sb_confirmation(string $lang, string $name, bool $yes): array
{
    $fr = $lang === 'fr';
    $e  = SB_EVENT;
    $d  = $e[$fr ? 'fr' : 'en'];
    $first = trim(explode(' ', trim($name))[0] ?? '');

    $hello = $first !== '' ? ($fr ? "Bonjour $first," : "Dear $first,") : ($fr ? 'Bonjour,' : 'Hello,');

    if ($yes) {
        $subject = $fr ? 'Votre présence est confirmée — Two Cities, One Friendship'
                       : 'You are confirmed — Two Cities, One Friendship';
        $lead = $fr ? 'Merci, votre réponse est bien enregistrée. Nous serons ravis de vous accueillir.'
                    : 'Thank you — your RSVP is confirmed. We look forward to welcoming you.';
        $outro = $fr ? 'Si vos plans changent, répondez simplement à nouveau via le formulaire : votre réponse sera mise à jour.'
                     : 'If your plans change, simply reply again through the form — your answer will be updated.';
    } else {
        $subject = $fr ? 'Merci pour votre réponse — Two Cities, One Friendship'
                       : 'Thank you for your reply — Two Cities, One Friendship';
        $lead = $fr ? 'Merci de nous avoir prévenus. Vous nous manquerez — nous espérons vous retrouver lors d’un prochain événement.'
                    : 'Thank you for letting us know. You will be missed — we hope to see you at a future event.';
        $outro = $fr ? 'Si vos plans changent, vous pouvez répondre à nouveau via le formulaire.'
                     : 'If your plans change, you can reply again through the form.';
    }

    $labels = $fr ? ['Date', 'Horaire', 'Lieu'] : ['Date', 'Time', 'Venue'];
    $cal    = $fr ? 'Ajouter à mon agenda' : 'Add to my calendar';
    $page   = $fr ? 'Voir la page de l’événement' : 'View the event page';
    $sign   = $fr ? 'L’équipe Sublime CI-USA — Office du tourisme de Côte d’Ivoire'
                  : 'The Sublime CI-USA team — Tourism Office of Côte d’Ivoire';

    $f = "font-family:'Trebuchet MS',Arial,Helvetica,sans-serif";
    $facts = '';
    foreach ([[$labels[0], $d['date']], [$labels[1], $d['time']],
              [$labels[2], $e['venue'] . '<br>' . sb_h($e['address'])]] as [$k, $v]) {
        $facts .= '<tr><td style="padding:0 0 12px 0;' . $f . '">'
                . '<span style="display:block;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:#8793a8;font-weight:bold;">' . sb_h($k) . '</span>'
                . '<span style="display:block;font-size:16px;line-height:23px;color:#0A3161;font-weight:bold;">' . $v . '</span></td></tr>';
    }

    $btn = fn (string $href, string $label, string $bg) =>
        '<table role="presentation" border="0" cellpadding="0" cellspacing="0" style="margin:0 auto;"><tr>'
      . '<td align="center" bgcolor="' . $bg . '" style="background-color:' . $bg . ';border-radius:6px;">'
      . '<a href="' . sb_h($href) . '" target="_blank" style="display:inline-block;padding:14px 28px;' . $f . ';font-size:15px;font-weight:bold;color:#ffffff;text-decoration:none;border-radius:6px;">'
      . sb_h($label) . '</a></td></tr></table>';

    $html = '<!DOCTYPE html><html lang="' . ($fr ? 'fr' : 'en') . '"><head><meta charset="UTF-8">'
          . '<meta name="viewport" content="width=device-width,initial-scale=1"><title>' . sb_h($subject) . '</title></head>'
          . '<body style="margin:0;padding:0;background:#eef1f6;">'
          . '<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" style="background:#eef1f6;"><tr><td align="center" style="padding:24px 12px;">'
          . '<table role="presentation" width="560" border="0" cellpadding="0" cellspacing="0" style="width:100%;max-width:560px;background:#ffffff;border-radius:10px;overflow:hidden;">'
          . '<tr><td bgcolor="#0A3161" align="center" style="background:#0A3161;padding:18px 24px;' . $f . ';">'
          . '<span style="font-size:20px;font-weight:bold;color:#ffffff;">Sublime CI-USA</span><br>'
          . '<span style="font-size:11px;letter-spacing:1.8px;color:#F77F00;font-weight:bold;">WASHINGTON &middot; ABIDJAN</span></td></tr>'
          . '<tr><td style="padding:30px 36px 6px 36px;' . $f . ';">'
          . '<p style="margin:0 0 14px 0;font-size:16px;line-height:24px;color:#33405a;">' . sb_h($hello) . '</p>'
          . '<p style="margin:0 0 20px 0;font-size:16px;line-height:25px;color:#33405a;">' . sb_h($lead) . '</p>'
          . '<p style="margin:0 0 4px 0;font-size:13px;letter-spacing:2px;text-transform:uppercase;color:#B31942;font-weight:bold;">' . sb_h($e['title']) . '</p>'
          . '</td></tr>'
          . '<tr><td style="padding:10px 36px 6px 36px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">' . $facts . '</table></td></tr>'
          . ($yes ? '<tr><td style="padding:6px 36px 4px 36px;">' . $btn(sb_calendar_url(), $cal, '#B31942') . '</td></tr>' : '')
          . '<tr><td style="padding:16px 36px 6px 36px;' . $f . ';">'
          . '<p style="margin:0 0 14px 0;font-size:15px;line-height:23px;color:#33405a;">' . sb_h($outro) . '</p>'
          . '<p style="margin:0 0 6px 0;font-size:15px;line-height:23px;"><a href="' . sb_h(sb_event_url($lang)) . '" target="_blank" style="color:#0A3161;font-weight:bold;">' . sb_h($page) . '</a></p>'
          . '</td></tr>'
          . '<tr><td style="padding:16px 36px 28px 36px;' . $f . ';"><p style="margin:0;font-size:14px;line-height:21px;color:#5b6880;">' . sb_h($sign) . '<br>'
          . '<a href="mailto:tourism@ambaciusa.org" style="color:#5b6880;">tourism@ambaciusa.org</a></p></td></tr>'
          . '</table></td></tr></table></body></html>';

    $text = "$hello\n\n$lead\n\n" . $e['title'] . "\n"
          . "{$labels[0]} : {$d['date']}\n{$labels[1]} : {$d['time']}\n{$labels[2]} : {$e['venue']}, {$e['address']}\n\n"
          . ($yes ? "$cal : " . sb_calendar_url() . "\n\n" : '')
          . "$outro\n" . sb_event_url($lang) . "\n\n$sign\ntourism@ambaciusa.org\n";

    return ['subject' => $subject, 'html' => $html, 'text' => $text];
}

// ============================================================ ALERTE ÉQUIPE

function sb_notification(array $r, string $status): array
{
    $yes = $r['attending'] === 'yes';
    $subject = ($yes ? '✓ RSVP oui' : '✗ RSVP non') . ' — ' . $r['name']
             . ($status === 'updated' ? ' (mise à jour)' : '');
    $heard = SB_HEARD[$r['heard']][1] ?? '—';
    $text = "Nouvelle réponse au formulaire « Two Cities, One Friendship »\n"
          . str_repeat('-', 50) . "\n"
          . 'Présence     : ' . ($yes ? 'OUI' : 'non') . "\n"
          . "Nom          : {$r['name']}\n"
          . "E-mail       : {$r['email']}\n"
          . 'Téléphone    : ' . ($r['phone'] ?: '—') . "\n"
          . 'Participants : ' . ($r['guests'] ?: '—') . "\n"
          . "Connu par    : $heard\n"
          . 'Langue       : ' . strtoupper($r['lang']) . "\n"
          . str_repeat('-', 50) . "\n"
          . ($r['comments'] !== '' ? "Commentaire :\n{$r['comments']}\n" . str_repeat('-', 50) . "\n" : '')
          . ($status === 'updated' ? "Cette personne avait déjà répondu : sa ligne a été mise à jour.\n" : '')
          . "\nListe complète : " . rtrim((string) sb_config()['site_url'], '/') . "/admin/\n";
    $html = '<pre style="font:14px/1.5 Menlo,Consolas,monospace;">' . sb_h($text) . '</pre>';
    return ['subject' => $subject, 'html' => $html, 'text' => $text];
}

// ============================================================ INVITATION

function sb_invitation_file(string $lang): string
{
    return dirname(__DIR__, 2) . '/email/invitation-two-cities-' . ($lang === 'fr' ? 'fr' : 'en') . '.html';
}

/** Gabarit personnalisé : salutation + lien RSVP pré-rempli. */
function sb_invitation(string $lang, string $name, string $email): array
{
    $fr   = $lang === 'fr';
    $html = (string) @file_get_contents(sb_invitation_file($lang));
    $base = sb_event_url($lang);

    $first = trim(explode(' ', trim($name))[0] ?? '');
    $greet = '';
    if ($first !== '') {
        $greet = '<p style="margin:0 0 14px 0;font-family:\'Trebuchet MS\',Arial,Helvetica,sans-serif;font-size:17px;line-height:24px;color:#33405a;">'
               . sb_h(($fr ? 'Bonjour ' : 'Dear ') . $first . ',') . '</p>';
    }
    $html = str_replace('<!--GREETING-->', $greet, $html);

    $q = http_build_query(array_filter(['n' => $name, 'e' => $email]), '', '&', PHP_QUERY_RFC3986);
    $html = str_replace($base . '#rsvp', sb_h($base . ($q ? '?' . $q : '') . '#rsvp'), $html);

    $d = SB_EVENT[$fr ? 'fr' : 'en'];
    $text = ($first !== '' ? ($fr ? "Bonjour $first,\n\n" : "Dear $first,\n\n") : '')
          . ($fr ? "Vous êtes convié(e) à\n" : "You're invited to\n")
          . "TWO CITIES, ONE FRIENDSHIP\nRockville, Maryland · Korhogo, Côte d'Ivoire\n\n"
          . ($fr ? 'Date : ' : 'Date: ') . $d['date'] . "\n"
          . ($fr ? 'Horaire : ' : 'Time: ') . $d['time'] . "\n"
          . ($fr ? 'Lieu : ' : 'Venue: ') . SB_EVENT['venue'] . ', ' . SB_EVENT['address'] . "\n\n"
          . ($fr ? "Une soirée, deux cultures : rythmes et danses ivoiriens, saveurs de la cuisine ivoirienne,\nartisanat sénoufo. Le nombre de places est limité.\n\n"
                 : "One evening, two cultures: Ivorian rhythms and dance, a taste of Ivorian cuisine,\nSenufo craft on display. Seating is limited.\n\n")
          . ($fr ? 'Répondre (RSVP) : ' : 'RSVP: ') . $base . ($q ? '?' . $q : '') . "#rsvp\n\n"
          . "Sublime CI-USA — " . ($fr ? 'Office du tourisme de Côte d’Ivoire' : 'Tourism Office of Côte d’Ivoire') . "\n"
          . "2424 Massachusetts Avenue N.W., Washington, D.C. 20008\ntourism@ambaciusa.org\n";

    return ['html' => $html, 'text' => $text];
}
