# RSVP et envoi des invitations

Trois pièces, toutes sur ciusatourism.com, sans Google Forms :

| Adresse | Pour qui | Rôle |
|---|---|---|
| `/event-two-cities#rsvp` | les invités | formulaire de réponse (EN et FR) |
| `/admin/` | l'équipe | tableau de bord : invitations envoyées et leur état, réponses, exports Excel |
| `/admin/send.php` | l'équipe | envoi de l'invitation, avec aperçu et test |

Quand un invité répond : sa réponse est enregistrée, `tourism@ambaciusa.org`
reçoit une alerte, et l'invité reçoit une confirmation (avec bouton « Ajouter
à mon agenda » s'il vient). S'il répond une seconde fois avec le même e-mail,
sa ligne est mise à jour au lieu d'être dupliquée.

---

## Mise en service (une seule fois)

### 1. Déployer
Push sur GitHub, puis cPanel → Git Version Control → *Update from Remote* →
*Deploy HEAD Commit*. Le déploiement crée aussi le dossier privé
`/home/ciusatou/sublime-private/`.

### 2. Déposer le fichier de configuration
1. Ouvrir `setup/config.sample.php` (dans le dépôt)
2. Remplacer les deux `CHANGE` :
   - `smtp_pass` : le mot de passe de `invitation@ciusatourism.com`
   - `admin_password` : un **nouveau** mot de passe pour `/admin/`, long
3. cPanel → Gestionnaire de fichiers → aller dans `/home/ciusatou/sublime-private/`
   (au-dessus de `public_html`, pas dedans)
4. Téléverser le fichier, puis le **renommer en `config.php`**

Ce dossier n'est pas accessible depuis le web et n'est pas dans GitHub :
c'est là que vivent les mots de passe et les réponses des invités.

### 3. Tester
1. Ouvrir `ciusatourism.com/admin/`, se connecter
2. Onglet *Envoyer l'invitation* → mettre votre adresse dans le champ test →
   *Envoyer un test*
3. Vérifier la boîte de réception **et le dossier spam**
4. Répondre au formulaire de la page de l'événement avec votre propre adresse :
   la réponse doit apparaître dans `/admin/`, et deux e-mails doivent arriver
   (alerte + confirmation)
5. Supprimer cette réponse de test dans `/admin/`

### Si le test échoue
Le message d'erreur s'affiche dans la page. Les cas courants :

| Message | Correction dans `config.php` |
|---|---|
| `mot de passe SMTP refusé` | vérifier `smtp_pass` |
| `certificate verify failed` | `'smtp_verify' => false` |
| `connexion impossible … 465` | `'smtp_port' => 587` et `'smtp_secure' => 'tls'` |

Le serveur exact est indiqué dans cPanel → Comptes de messagerie →
*Connect Devices*, à côté de l'adresse.

Pour éviter le spam : cPanel → **Email Deliverability** → le domaine
`ciusatourism.com` doit afficher SPF et DKIM valides. Sinon, bouton
*Repair*.

---

## Envoyer l'invitation

1. `/admin/send.php`
2. Coller la liste, une personne par ligne : `Prénom Nom, adresse@exemple.com`
   (le nom est facultatif ; s'il est là, l'invitation commence par « Dear Jane, »)
3. Choisir la langue — faire deux envois si la liste est mixte
4. *Envoyer un test*, vérifier, puis *Envoyer l'invitation*

Les messages partent un par un, à 4 secondes d'intervalle (50 invités ≈ 3
minutes). Garder la page ouverte pendant l'envoi. Une personne déjà invitée
est ignorée si on relance la liste, sauf si la case *Renvoyer* est cochée.

Le bouton RSVP de chaque invitation ouvre le formulaire avec le nom et
l'adresse de l'invité déjà remplis.

---

## Suivre les invitations

Le tableau de bord (`/admin/`) liste chaque invitation envoyée avec son état :

| État | Signification |
|---|---|
| En attente de réponse | l'invitation est partie, l'invité n'a pas encore répondu |
| A répondu : oui / non | l'invité a répondu au formulaire **avec la même adresse e-mail** |
| Échec d'envoi | le serveur de messagerie a refusé l'adresse (le motif s'affiche) |

Les boutons *Relancer N personnes en attente* ouvrent la page d'envoi avec la
liste déjà remplie (une langue à la fois), l'objet préfixé par « Reminder: » /
« Rappel : » et la case *Renvoyer* cochée. Un invité qui répond avec une autre
adresse que celle de l'invitation reste « en attente » : sa réponse apparaît
quand même dans *Réponses reçues*.

## Où sont les données

`/home/ciusatou/sublime-private/` :

- `config.php` — mots de passe
- `rsvp.csv` — réponses (aussi exportables depuis `/admin/`)
- `sent-two-cities.log` — journal des invitations envoyées
- `errors.log` — e-mails qui n'ont pas pu partir (la réponse, elle, est gardée)
