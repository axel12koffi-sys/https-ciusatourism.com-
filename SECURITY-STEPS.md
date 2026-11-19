# Sécurité — réintroduction par étapes

Le `.htaccess` complet a provoqué une erreur 500. On le remonte **un bloc à la
fois**, en testant après chacun. Ça prend vingt minutes, et on saura
exactement lequel pose problème au lieu de tout perdre d'un coup.

## Méthode

Avant chaque ajout :

1. Gestionnaire de fichiers > clic droit sur `.htaccess` > **Copier** >
   nomme la copie `htaccess-ok.bak`. C'est ton filet.
2. Ajoute le bloc suivant **à la fin** du `.htaccess`.
3. Recharge le site, plus une page intérieure (`hotel.html` par exemple).
4. **Ça marche** → passe à l'étape suivante.
   **Erreur 500** → supprime le bloc que tu viens d'ajouter, note son numéro,
   et passe au suivant. On regardera ce bloc-là séparément.

Ne saute pas d'étape et n'en ajoute jamais deux d'un coup : c'est tout
l'intérêt de la méthode.

---

## Point de départ

Ton `.htaccess` actuel, celui qui fonctionne :

```apache
DirectoryIndex index.html index.php
ErrorDocument 404 /404.html
Options -Indexes

<FilesMatch "\.(md|py|sh|log|sql|bak|zip)$">
  Require all denied
</FilesMatch>

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
```

---

## Étape 1 — Aucun PHP exécutable hors de `api/`

**C'est le bloc le plus utile de tout le fichier.** Si un fichier malveillant
atterrit un jour dans `assets/` ou `uploads/`, il ne s'exécutera pas. Commence
par celui-là : même si tu t'arrêtes après, tu auras gagné l'essentiel.

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteRule ^(assets|uploads|storage)/.*\.(php|phtml|php[0-9]|pht|phar|cgi|pl|py|sh)$ - [F,L]
</IfModule>
```

**Test :** ouvre `ciusatourism.com/assets/test.php` — tu dois obtenir un refus,
pas une page blanche.

---

## Étape 2 — Sondes WordPress

Ton domaine a hébergé un WordPress. Les robots chercheront `/wp-login.php`
pendant des mois. Ce bloc leur répond immédiatement, ce qui économise de la
bande passante et garde tes logs lisibles.

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteRule ^(wp-login\.php|wp-admin|wp-includes|wp-json|xmlrpc\.php|wp-config\.php) - [F,L]
  RewriteRule ^(administrator|phpmyadmin|pma|myadmin|\.env)(/|$) - [F,L]
</IfModule>
```

**Test :** `ciusatourism.com/wp-login.php` doit refuser.

---

## Étape 3 — Fichiers sensibles

Élargit la protection déjà en place aux fichiers cachés et aux dossiers de
travail.

```apache
<FilesMatch "^\.">
  Require all denied
</FilesMatch>
<FilesMatch "^(fix-|collect-|check|install|setup|phpinfo|adminer|shell)">
  Require all denied
</FilesMatch>
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteRule ^(storage|partials|tools)(/|$) - [F,L]
</IfModule>
```

**Attention :** `<FilesMatch "^\.">` bloque aussi `.well-known/`, utilisé par
Let's Encrypt pour renouveler ton certificat. Si le renouvellement échoue dans
trois mois, c'est ce bloc. Ajoute alors juste avant :

```apache
<IfModule mod_rewrite.c>
  RewriteRule ^\.well-known/ - [L]
</IfModule>
```

---

## Étape 4 — En-têtes de sécurité complets

```apache
<IfModule mod_headers.c>
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=()"
  Header always set Cross-Origin-Opener-Policy "same-origin"
  Header unset X-Powered-By
</IfModule>
```

---

## Étape 5 — Content-Security-Policy

Le navigateur n'exécute plus que les scripts servis depuis ton domaine. Même
si du HTML malveillant parvenait à s'insérer dans une page, le code qu'il
contient ne s'exécuterait pas.

```apache
<IfModule mod_headers.c>
  Header always set Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'"
</IfModule>
```

**Test soigneusement :** ouvre le site, puis la console du navigateur (F12 >
Console). Si tu vois des erreurs `Content Security Policy`, quelque chose est
bloqué — envoie-moi le message et j'ajusterai la règle. Vérifie surtout que la
police Poppins s'affiche et qu'Aya s'anime.

---

## Étape 6 — Compression et cache

Sans effet sur la sécurité, mais le site charge plus vite.

```apache
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css
  AddOutputFilterByType DEFLATE application/javascript image/svg+xml
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html              "access plus 0 seconds"
  ExpiresByType text/css               "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/jpeg             "access plus 1 year"
  ExpiresByType image/webp             "access plus 1 year"
</IfModule>
```

---

## Étape 7 — URLs propres (facultatif)

À ne tenter qu'une fois tout le reste stable. C'est ce bloc qui avait cassé le
site la première fois.

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_FILENAME}\.html -f
  RewriteRule ^(.+?)/?$ $1.html [L]
</IfModule>
```

**Test :** `ciusatourism.com/destinations` doit afficher la page.

- **Ça marche** → passe `CLEAN_URLS = True` dans `paths.py`, relance
  `python3 build.py`, et renvoie les `.html`. Les liens perdront leur
  extension.
- **File not found** → `mod_rewrite` est inactif chez ton hébergeur. Retire le
  bloc et reste en `.html`. Aucune conséquence pour tes visiteurs.

---

## Étape 8 — HSTS

**En dernier, et seulement après plusieurs jours de HTTPS sans accroc.**

```apache
<IfModule mod_headers.c>
  Header always set Strict-Transport-Security "max-age=15768000; includeSubDomains"
</IfModule>
```

Le navigateur refusera toute connexion non chiffrée à ton domaine pendant six
mois. **C'est irréversible** : si ton certificat expire ou qu'un sous-domaine
n'a pas de HTTPS, le site devient inaccessible et tu ne peux rien y faire
avant l'expiration du délai.

Si tu as le moindre doute, saute cette étape. Le gain est marginal quand la
redirection HTTPS fonctionne déjà.

---

## Si un bloc casse le site

1. Supprime-le, note son numéro.
2. Si tu as perdu le fil, renomme `.htaccess` en `htaccess.bak` : le site
   remarche immédiatement, sans aucune règle.
3. Repars de `htaccess-ok.bak`, ta dernière version fonctionnelle.

Une erreur 500 sur un `.htaccess` signifie presque toujours qu'une directive
n'est pas reconnue par le serveur — pas que ta configuration est dangereuse.
Les blocs sont tous entourés de `<IfModule>` pour l'éviter, mais certains
hébergeurs interdisent aussi des directives précises via `AllowOverride`.
