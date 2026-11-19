# Sécurité — ciusatourism.com

Un site statique offre déjà bien moins de prise qu'un WordPress : pas de base
de données, pas de plugins, pas d'espace d'administration, pas de compte à
pirater. L'essentiel des attaques automatisées visant les CMS n'a rien à
attaquer ici. Ce document couvre le reste.

---

## Ce qui est en place

### `.htaccess` — 12 blocs numérotés

Si quelque chose casse après une modification, commente le bloc suspect plutôt
que le fichier entier.

| Bloc | Rôle |
|---|---|
| 1 | HTTPS forcé — **à décommenter une fois le certificat actif** |
| 2 | URLs propres + redirections des anciennes adresses WordPress |
| 3 | Pas de listing de dossier ; injections SQL et XSS bloquées dans l'URL |
| 4 | Sources, docs, sauvegardes et fichiers cachés jamais servis |
| 5 | **Aucun PHP exécutable hors de `api/`** |
| 6 | Sondes WordPress renvoyées immédiatement |
| 7 | Moissonneurs connus refusés |
| 8 | En-têtes de sécurité, dont la CSP |
| 9 | Taille des requêtes plafonnée à 2 Mo |
| 10-12 | Compression, cache, types MIME |

**Le bloc 5 est le plus important.** Si un jour un fichier malveillant se
retrouve dans `assets/` ou `uploads/` — par une faille, un accès FTP compromis,
un envoi mal contrôlé — il ne s'exécutera pas. C'est ce qui transforme une
intrusion en simple fichier inerte.

**Le bloc 6 vaut pour le confort.** Ton domaine a hébergé un WordPress : les
robots vont chercher `/wp-login.php` et `/xmlrpc.php` pendant des mois. Ils
reçoivent maintenant un refus immédiat, ce qui économise de la bande passante
et garde les logs lisibles.

### Content-Security-Policy

Le navigateur n'exécute que les scripts servis depuis le domaine. **Aucun
script inline n'est autorisé** — c'est pourquoi l'attribut `onerror=""` des
images a été déplacé dans `main.js`. Concrètement : même si du HTML malveillant
parvenait à s'insérer dans une page, le code qu'il contiendrait ne
s'exécuterait pas.

Seules exceptions : les styles inline (les gabarits utilisent des attributs
`style=""`) et Google Fonts.

### Formulaire de contact — 8 défenses

Testées une par une, pas seulement écrites :

| Défense | Comportement |
|---|---|
| Méthode POST obligatoire | rejet en 405 |
| Origine vérifiée | rejet en 403 si la requête ne vient pas du site |
| Pot de miel (`website`) | faux succès silencieux — le robot croit avoir réussi |
| Piège temporel | envoi en moins de 3 s ignoré |
| Limite par IP | 5 par heure, puis 429 |
| Longueurs plafonnées | 60 à 4000 caractères selon le champ |
| Filtrage des liens | plus de 2 URLs dans le message = spam ignoré |
| Nettoyage des en-têtes | `\r` et `\0` retirés, contre l'injection de destinataires |

Les faux succès sont volontaires : un robot qui reçoit une erreur réessaie
avec une autre méthode, un robot qui croit avoir réussi passe à autre chose.

Chaque demande est écrite dans `storage/requests.log` — si un mail se perd, la
demande reste récupérable. Ce dossier est inaccessible depuis le web (bloc 4).

### `robots.txt` et `security.txt`

`robots.txt` interdit `/api/`, `/storage/`, `/tools/` et refuse les
moissonneurs commerciaux. C'est une convention, pas une barrière : les robots
honnêtes la respectent, les autres sont bloqués par le bloc 7.

`.well-known/security.txt` donne une adresse de contact aux chercheurs en
sécurité, plutôt que de les laisser chercher.

---

## Ce qu'il te reste à faire

Ces points-là ne dépendent pas du code. Ils comptent autant, souvent plus.

### Sur cPanel

1. **Active l'authentification à deux facteurs** sur ton compte cPanel.
   Sécurité > Authentification à deux facteurs. C'est la mesure la plus
   rentable de toute cette liste : la majorité des sites compromis le sont par
   un mot de passe cPanel ou FTP, jamais par le code.
2. **Vérifie que ModSecurity est actif** (Sécurité > ModSecurity). C'est le
   pare-feu applicatif de l'hébergeur ; il filtre en amont du `.htaccess`.
3. **Supprime les comptes FTP inutilisés** (Fichiers > Comptes FTP). Chacun est
   une porte, et les identifiants FTP circulent en clair sur les vieux clients.
4. **Active les sauvegardes automatiques** si ton offre les propose, et
   télécharge une copie de temps en temps. Une sauvegarde qui vit uniquement
   sur le serveur attaqué ne sert à rien.
5. **Change le mot de passe cPanel** s'il a été utilisé ailleurs ou partagé
   avec un prestataire.

### Après la mise en ligne

6. **Décommente le bloc 1** du `.htaccess` une fois le certificat SSL actif.
7. **Attends quelques jours, puis décommente HSTS** (bloc 8). Attention :
   c'est irréversible pendant six mois. Ne l'active que si le HTTPS fonctionne
   sans accroc.
8. **Supprime les scripts de maintenance** — `fix-site.php`, `fix-images.php`,
   `collect-images.php`. Ils sont déjà bloqués par le bloc 4, mais un script
   qui écrit des fichiers n'a rien à faire sur un site en production.
9. **Supprime `build.py`, `data.py`, `paths.py` et `tools/`** du serveur si tu
   développes en local. Ils sont bloqués, mais autant ne pas les y mettre.

### À surveiller

- **Métriques > Erreurs** dans cPanel, une fois par mois. Un pic d'erreurs 403
  signale une campagne de scan ; c'est normal et sans gravité, mais bon à voir.
- **`storage/requests.log`** — si tu y vois des demandes absurdes, les défenses
  du formulaire ont été contournées et il faudra resserrer.

---

## Ce que tout ceci ne protège pas

Autant être clair sur les limites.

- **Un mot de passe cPanel volé** donne un accès complet. Aucune règle
  `.htaccess` n'y peut quoi que ce soit. D'où le point 1.
- **Le filtrage par User-Agent (bloc 7)** arrête le bruit, pas un attaquant :
  il suffit de mentir sur son identité. C'est de l'économie de ressources plus
  que de la sécurité.
- **La limite par IP** du formulaire se contourne avec un réseau de proxys. Si
  le spam devient un problème réel, il faudra un CAPTCHA — dis-le moi, ça
  s'ajoute en une demi-heure.
- **Une faille chez l'hébergeur**, ou sur un site voisin en mutualisé, n'est
  pas de ton ressort. C'est l'argument principal pour garder des sauvegardes
  hors du serveur.

Le risque résiduel réel, pour un site comme celui-ci, c'est un accès
d'administration compromis. Pas le code.
