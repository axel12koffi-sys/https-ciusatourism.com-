<?php
/**
 * SUBLIME CI-USA — configuration privée.
 *
 * À COPIER SUR LE SERVEUR, renommé config.php, dans :
 *     /home/ciusatou/sublime-private/config.php
 * (à côté de public_html, PAS dedans). Ne jamais le mettre dans GitHub.
 *
 * Seules les deux lignes « CHANGE » sont à remplir.
 */
return [
    // Mot de passe de la boîte invitation@ciusatourism.com (cPanel > Comptes de messagerie)
    'smtp_pass'      => 'CHANGE',

    // Mot de passe de l'administration ciusatourism.com/admin/ — choisissez-en un nouveau,
    // long (15 caractères et plus), différent de tous les autres
    'admin_password' => 'CHANGE',

    // ----- réglages déjà corrects, à ne modifier que si besoin -----
    'smtp_host'   => 'mail.ciusatourism.com',
    'smtp_port'   => 465,
    'smtp_secure' => 'ssl',          // si l'envoi échoue : 587 + 'tls'
    'smtp_verify' => true,           // si « certificate verify failed » : false
    'smtp_user'   => 'invitation@ciusatourism.com',
    'from_email'  => 'invitation@ciusatourism.com',
    'from_name'   => 'Sublime CI-USA',
    'reply_to'    => 'tourism@ambaciusa.org',   // où arrivent les réponses des invités
    'notify_to'   => 'tourism@ambaciusa.org',   // qui est prévenu de chaque RSVP
    'send_delay'  => 4,                         // secondes entre deux invitations
];
