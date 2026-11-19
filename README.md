# Sublime CI-USA — refonte

Site multi-pages statique (HTML/CSS/JS), structuré pour un passage en PHP.

## Arborescence
```
index.html                  Accueil
destinations.html           Liste + filtres + process (accordéon)
destination-beaches.html    Gabarit page destination
good-deal.html              Hôtels / Gastronomie / Transport
blog.html                   Blog & News + filtres
mediatheque.html            Galerie + lightbox
faq.html                    Accordéon FAQ (deep-link #q3)
contact.html                Formulaire + validation
assets/css/style.css        Design system complet (Poppins)
assets/js/main.js           17 modules, auto-désactivés si markup absent
assets/js/chatbot.js        Widget de chat
api/                        Endpoints PHP (stubs)
```

## Passage en PHP
Dans chaque page, les blocs sont balisés :
`<!-- ===== partials/header.php ===== -->` … `<!-- ===== /partials/header.php ===== -->`
Il suffit de couper ces blocs vers `partials/header.php` et `partials/footer.php`,
de renommer les pages en `.php` et de remplacer par `<?php include 'partials/header.php'; ?>`.

## Chatbot — « Aya »
Personnage : Aya, ivoiro-américaine, entre Washington D.C. et Abidjan.

### Personnage animé — `assets/js/aya.js` (5,7 ko)
Rig SVG 2D injecté dans tout élément portant `[data-aya]`. Aucune image,
aucune dépendance. Cinq états pilotés par `data-state` sur le `<svg>` :

| état | ce qu'elle fait | déclencheur |
|---|---|---|
| `idle` | respiration, clignements irréguliers | par défaut |
| `wave` | salut de la main, tête inclinée | ouverture du chat, et toutes les 14 s sur le bouton tant qu'on n'a pas ouvert |
| `think` | main au menton, tête penchée, bulles de réflexion | pendant l'indicateur de frappe |
| `talk` | bouche animée, hochement de tête | pendant l'affichage d'une réponse (durée ≈ 45 ms/mot) |
| `happy` | petit saut, yeux plissés | disponible, non câblé |

API : `Aya.set('wave')` (ponctuel), `Aya.set('think', true)` (maintenu),
`Aya.idle()`, `Aya.stopAttract()`.
Pour ajouter un état : une entrée dans le CSS `.aya[data-state="…"]` et
éventuellement une durée dans l'objet `DURATION` de `aya.js`.

`prefers-reduced-motion` coupe toutes les animations et fige la pose.

`assets/js/chatbot.js` contient **45 intentions bilingues FR/EN** couvrant la
base de réponses du Bureau du Tourisme : informations générales, visa et
formalités, vols et transport, hébergement, culture, nature, business et
événementiel, questions pratiques, profils voyageurs, promotion et partenariats.

Détection de langue automatique : Aya répond en français si la question est
posée en français, même si le site est en anglais.

Pour brancher le backend : passer `USE_API = true` en haut du fichier.
L'endpoint `api/chat.php` reçoit `{ message, history, lang }` et renvoie
`{ reply }`. Le moteur de règles reste le filet de sécurité si l'API échoue.

## Formulaires
- Contact : validation front OK, `fetch('api/contact.php')` commenté dans main.js (module 13).
- Newsletter : idem, module 14.

## Langues
Système i18n léger sur `data-i18n`, dictionnaire dans main.js (module 17),
choix mémorisé en localStorage. À remplacer par WPML si retour sur WordPress.

## Données Good Deal (extraites du site actuel)
- `hotel.html` — 23 hôtels, filtres par quartier (Cocody / Plateau / Marcory / Port-Bouët) + recherche live.
- `gastronomies.html` — 26 restaurants, filtres par zone + recherche live.
- `transport.html` — location de voiture, VTC (Yango, Uber, Heetch), chauffeur privé.

### Anomalies relevées dans les données d'origine (marquées "Contact details to confirm")
- **La Maison Palmier** apparaissait deux fois → dédoublonnée.
- **Ibis Marcory** portait les coordonnées du Capitol Hôtel.
- **Novotel Plateau**, **Ibis Plateau** portaient celles du Pullman / Mövenpick.
- **Grand Hôtel**, **Ivotel** portaient celles du Tiama / Seen Hôtel.
- **Restaurant Liva** portait celles de l'Hôtel Byblos.
- **Kajazoma** apparaissait deux fois, la seconde avec l'image « Route des Vins » → renommée.
- Capitol Hôtel : le champ e-mail contenait une URL, retiré.
- Le lien « Utiliser Heetch » pointait vers Yango → corrigé vers heetch.com.
Ces fiches affichent un bandeau rouge tant que les vraies coordonnées ne sont pas fournies.
