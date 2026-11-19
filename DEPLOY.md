# Mise en ligne sur cPanel

Ce site est du **HTML / CSS / JS statique + 3 fichiers PHP**. Ce n'est pas un
thème WordPress, ce n'est pas un CMS : ni plugin, ni base de données, ni étape
de compilation. Tu déposes les fichiers, ça tourne.

Prérequis : un hébergement cPanel mutualisé standard, PHP 8.1 ou plus.

---

## Étape 0 — Récupérer les photos (à faire en premier)

Les 69 photos du site sont dans `public_html/wp-content/uploads/` sur ton
serveur. Il faut les copier vers `assets/img/` avant de nettoyer.

⚠️ **Ne zippe pas le dossier `uploads` entier.** Il pèse environ 1 Go — c'est
toute la médiathèque de l'ancien site, dont la quasi-totalité ne sert plus. Le
téléchargement échoue (erreur 500). Le site n'a besoin que de 69 fichiers.

### A. Copie sur le serveur — recommandé, rien ne transite par ta connexion

1. Envoie le site sur le serveur (étape 2 ci-dessous), **sans supprimer**
   `wp-content/` pour l'instant
2. Ouvre dans ton navigateur :
   `https://ton-domaine/collect-images.php?go=ciusa2026`
3. Le script trouve tout seul l'ancien dossier `uploads`, copie les 69 fichiers
   nécessaires dans `assets/img/` en les renommant, et affiche un rapport
4. **Supprime `collect-images.php`** — un script de copie n'a rien à faire en
   production
5. Tu peux alors supprimer `wp-content/` et le reste de l'ancien site

Si le script annonce « Dossier uploads introuvable », corrige la liste
`$SOURCES` en haut du fichier avec le vrai chemin.

### B. Téléchargement HTTP — depuis ton poste, si l'ancien site répond encore

```bash
chmod +x tools/download-images.sh
./tools/download-images.sh
```

Environ 20 Mo, pas 1 Go : le script ne prend que les fichiers utiles.

### C. À la main — si les deux échouent

Dans le Gestionnaire de fichiers, télécharge les fichiers **un par un** depuis
`wp-content/uploads/`, puis renomme-les : `2025/03/photo.jpg` devient
`202503-photo.jpg`. La liste complète des 69 noms attendus est dans
`collect-images.php`.

### Dans tous les cas

Vérifie qu'`assets/img/` contient bien **69 fichiers**. Pour voir ce que les
pages réclament :

```bash
grep -oh 'assets/img/[^"]*' *.html | sort -u
```

Rien ne t'oblige à garder les anciennes photos : tu peux déposer les tiennes en
respectant les mêmes noms de fichiers.

---

## Étape 1 — Nettoyer le serveur

Une fois les photos en sécurité sur ton poste :

1. cPanel > **Assistant de sauvegarde** > **Télécharger une sauvegarde
   complète**. Garde-la quelques semaines. Ça ne coûte rien et ça évite les
   regrets.
2. Dans `public_html`, sélectionne tout et **supprime**. S'il y avait une base
   de données, tu peux la supprimer aussi dans **Bases de données MySQL** : le
   nouveau site ne s'en sert pas.

Si tu préfères la prudence : crée un sous-domaine de recette
(`new.ciusatourism.com`, racine `/home/<user>/new`), installe le site dedans,
valide tout, et ne nettoie `public_html` qu'ensuite.

---

## Étape 2 — Envoyer les fichiers

**Option A — Gestionnaire de fichiers**

1. cPanel > Gestionnaire de fichiers > `public_html`
2. **Charger** > dépose `ciusa-tourism.zip`
3. Clic droit sur le zip > **Extraire**
4. Le zip crée un dossier `ciusa-tourism/`. Entre dedans, `Ctrl+A`,
   **Déplacer** vers `/public_html`. Supprime ensuite le dossier vide et le zip.

**Option B — FTP** : dépose le *contenu* du dossier `ciusa-tourism`
(pas le dossier lui-même) dans `public_html`.

⚠️ Active **Paramètres > Afficher les fichiers cachés (dotfiles)** dans le
Gestionnaire de fichiers, sinon tu ne verras pas `.htaccess` et tu croiras
qu'il ne s'est pas envoyé. C'est l'oubli le plus fréquent.

Arborescence finale :

```
public_html/
├── index.html  destinations.html  hotel.html  …  404.html
├── .htaccess
├── assets/css/style.css
├── assets/js/{main.js, aya.js, chatbot.js}
├── assets/img/                    69 fichiers
├── api/{contact.php, chat.php}
├── storage/                       journal des demandes
├── build.py  data.py  paths.py    sources, non servies
└── tools/
```

---

---

## ⚠️ Ne jamais remplacer `assets/img/` en entier

Le zip contient **le logo et les visuels `dest/`**, mais **pas** les 59 photos
d'hôtels, de restaurants et de partenaires. Celles-là ne vivent que sur ton
serveur : elles viennent de ton ancien dossier `uploads/`, récupérées avec
`fix-site.php`.

Au moment d'envoyer une mise à jour :

- **Remplace** : les fichiers `.html`, le dossier `fr/`, `assets/css/`,
  `assets/js/`, `assets/img/dest/`, et les fichiers `assets/img/logo-*`
- **Ne touche pas** : les fichiers `assets/img/2025*` et `assets/img/2026*`

Si tu as un doute, `tools/check-images.php` te dit en une page exactement
quelles images manquent sur le serveur et pourquoi.


## Étape 3 — Permissions

Généralement correctes après extraction. Sinon : dossiers **755**, fichiers
**644**. Jamais 777, même « juste pour tester ».

Le dossier `storage/` doit être inscriptible (755 suffit dans la plupart des
configurations cPanel) pour que le journal des demandes fonctionne.

---

## Étape 4 — Version de PHP

cPanel > **MultiPHP Manager** > sélectionne le domaine > **PHP 8.1** ou plus >
Appliquer.

---

## Étape 5 — SSL

cPanel > **SSL/TLS Status** > coche `ciusatourism.com` et
`www.ciusatourism.com` > **Run AutoSSL**. Compte quelques minutes.

Le cadenas actif, **décommente le bloc 1 du `.htaccess`** (redirection HTTPS).
Il est livré désactivé exprès : l'activer avant que le certificat existe rend
le site inaccessible.

---

## Étape 6 — Recette

- [ ] les images s'affichent, aucun carré gris
- [ ] `/destinations` fonctionne sans le `.html`
- [ ] le menu mobile s'ouvre, les sous-menus se déplient
- [ ] l'avion du rail latéral descend au scroll (écran large)
- [ ] Aya fait coucou, réfléchit, puis parle
- [ ] la recherche et les filtres de `/hotel` et `/gastronomies` répondent
- [ ] le formulaire de contact envoie **et le mail arrive**
- [ ] une URL inventée affiche la 404 maison

### Si le mail n'arrive pas

1. Crée `no-reply@ciusatourism.com` dans **cPanel > Comptes de messagerie**.
   C'est déjà l'expéditeur déclaré dans `api/contact.php` (constante `FROM`) ;
   un expéditeur du domaine passe bien mieux les filtres anti-spam.
2. `TO` est réglé sur `tourism@ambaciusa.org` — change-le si besoin.
3. Toute demande est aussi écrite dans `storage/requests.log`. Même si un mail
   se perd, la demande est conservée.
4. **cPanel > Suivi des e-mails** montre où le message a été bloqué.

### Si les URLs propres ne marchent pas

Certains hébergeurs désactivent `mod_rewrite`. Commente le bloc 2 du
`.htaccess` : le site fonctionne alors avec les `.html`, sans rien casser.

---

## Étape 7 — Redirections des anciennes URLs

L'ancien site servait des adresses en `/index.php/...`. Si elles sont indexées
ou partagées quelque part, ajoute ceci dans le `.htaccess`, juste après
`RewriteEngine On` :

```apache
RewriteRule ^index\.php/hotel/?$          /hotel              [R=301,L]
RewriteRule ^index\.php/gastronomies/?$   /gastronomies       [R=301,L]
RewriteRule ^index\.php/transport/?$      /transport          [R=301,L]
RewriteRule ^index\.php/faq/?$            /faq                [R=301,L]
RewriteRule ^index\.php/contact/?$        /contact            [R=301,L]
RewriteRule ^index\.php/mediatheque/?$    /mediatheque        [R=301,L]
RewriteRule ^index\.php/destination/best-beaches-in-ivory-coast/?$ /destination-beaches [R=301,L]
RewriteRule ^index\.php/destination/?$    /destinations       [R=301,L]
RewriteRule ^index\.php/?                 /                   [R=301,L]
```

---

## À savoir après la mise en ligne

- L'ancien site envoyait `noindex, nofollow` sur toutes ses pages : il était
  invisible pour Google. Le nouveau ne le fait pas. Si tu veux rester discret
  pendant la recette, dis-le, je remets la balise.
- Le chatbot tourne **entièrement dans le navigateur** : zéro charge serveur,
  zéro coût. Pour le basculer sur `api/chat.php`, mets `USE_API = true` en haut
  de `assets/js/chatbot.js`.
- Il n'y a **pas encore de sitemap.xml**. Dis-moi si tu en veux un.

---

## Modifier le site plus tard

Les pages `.html` sont **générées** : ne les édite pas directement, elles
seraient écrasées au prochain build.

| Ce que tu veux changer | Le fichier |
|---|---|
| textes, structure des pages | `build.py` |
| hôtels, restaurants, VTC | `data.py` |
| couleurs, espacements, typo | `assets/css/style.css` |
| comportements, animations | `assets/js/*.js` |
| réponses du chatbot | `assets/js/chatbot.js` |

Puis, à la racine du projet :

```bash
python3 build.py
```

et tu renvoies les `.html` modifiés sur le serveur.

### Le jour où tu passes en PHP

Chaque page contient des blocs balisés :

```html
<!-- ===== partials/header.php ===== -->  …  <!-- ===== /partials/header.php ===== -->
```

Tu coupes ces deux blocs vers `partials/header.php` et `partials/footer.php`,
tu renommes les pages en `.php`, tu remplaces par
`<?php include 'partials/header.php'; ?>`. Rien d'autre à toucher.
