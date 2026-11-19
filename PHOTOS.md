# Brief photo

## L'état actuel, sans détour

Les 18 destinations affichent aujourd'hui des **visuels de remplacement
dessinés** — des dégradés aux couleurs du site, un par lieu, générés par
`make-covers.py`. Ils tiennent la place proprement et ne se répètent pas, mais
**ce ne sont pas des photos**. Sur un site d'agence de voyage, la photo est
l'argument de vente principal : c'est ce qui déclenche la demande de devis.

Avant, c'était pire : Grand-Bassam, Assinie et Sassandra partageaient la même
image. Le remplacement était donc une amélioration, pas une solution.

---

## Remplacer un visuel

Déposer un fichier du **même nom** dans `assets/img/dest/`, en `.jpg`, `.webp`
ou `.png`. Le générateur le détecte tout seul et abandonne le `.svg`. Aucune
autre modification, aucun code à toucher.

```
assets/img/dest/grand-bassam.svg   ← visuel de remplacement
assets/img/dest/grand-bassam.jpg   ← ta photo, prioritaire dès qu'elle est là
```

Puis `./build-all.sh` pour régénérer les deux langues.

---

## Ce qu'il faut, lieu par lieu

**Format** : paysage, minimum 1600 px de large, idéalement 2000. Ratio 16:10.
Les cartes recadrent au centre, donc éviter les sujets collés aux bords.

### Littoral — `assets/img/dest/`

| Fichier | Ce qu'on veut voir |
|---|---|
| `grand-bassam.jpg` | Le quartier France : façades coloniales en brique, ou la plage avec les bâtiments derrière |
| `assinie.jpg` | La langue de sable entre lagune et océan, vue large. Pirogues, cocotiers |
| `sassandra.jpg` | Le port de pêche en activité, ou une crique vue depuis les hauteurs |
| `san-pedro.jpg` | Plage longue et vide, forêt qui descend vers le sable |
| `jacqueville.jpg` | Cocoteraie en bord de mer, ou village de pêcheurs |
| `grand-lahou.jpg` | Les bâtiments repris par l'océan — c'est l'image la plus forte de la liste |

### Culture

| Fichier | Ce qu'on veut voir |
|---|---|
| `yamoussoukro.jpg` | La basilique Notre-Dame de la Paix, vue d'ensemble |
| `korhogo.jpg` | Une toile de Korhogo en cours de peinture, ou un atelier de Fakaha |
| `man-masques.jpg` | Danse d'échasses ou masque en cérémonie — **avec autorisation** |
| `abidjan.jpg` | Le Plateau depuis la lagune, ou un marché animé |
| `bouake.jpg` | Le carnaval, ou les potières de Katiola au travail |
| `tiegba.jpg` | Le village sur pilotis vu depuis une pirogue |

### Nature

| Fichier | Ce qu'on veut voir |
|---|---|
| `tai.jpg` | Canopée de forêt primaire, ou sentier sous les grands arbres |
| `comoe.jpg` | Savane avec le fleuve, ou faune de savane |
| `man-region.jpg` | Un pont de lianes, ou une cascade. Le pont est plus identifiable |
| `banco.jpg` | Forêt dense, ou le fanico au bord de la rivière |
| `ehotile.jpg` | Mangrove vue de l'eau, pirogue dans le cadre |
| `nimba.jpg` | Le massif, vue large |

---

## Où les obtenir

Par ordre de préférence.

**1. Vos propres photos, ou celles de vos partenaires sur place.** Ce sont les
meilleures : elles montrent ce que le voyageur verra réellement, et vous en
détenez les droits. Demandez aux guides et aux lodges — ils en ont, et ils sont
généralement ravis d'apparaître.

**2. L'office du tourisme.** Côte d'Ivoire Tourisme et le Ministère du Tourisme
disposent de banques d'images promotionnelles. Une demande écrite, en précisant
l'usage commercial, obtient souvent une autorisation gratuite pour une agence
qui promeut la destination.

**3. Banques d'images libres.** Unsplash, Pexels, Wikimedia Commons. La
couverture de la Côte d'Ivoire y est inégale : Abidjan et Grand-Bassam sont
bien représentés, Tiégba ou Fakaha beaucoup moins. Termes de recherche utiles :
`Grand-Bassam`, `Abidjan Plateau`, `Ivory Coast beach`, `Senufo`,
`Taï National Park`, `Man Ivory Coast waterfall`.

**4. Banques payantes.** Getty, Adobe Stock, Shutterstock. Comptez 10 à 50 $
par image. Pour 18 photos, c'est un budget de quelques centaines de dollars —
à mettre en regard du prix d'un seul voyage vendu.

---

## Deux points à ne pas négliger

**Les droits.** Ne prenez pas une photo trouvée par recherche d'images : la
plupart sont protégées, et une agence de voyage est une cible facile pour une
réclamation. Vérifiez toujours la licence, et gardez une trace écrite.

**Les personnes photographiées.** Pour les cérémonies de masques en
particulier, il faut l'accord des personnes et des familles. C'est une question
juridique, mais surtout une question de respect — et c'est cohérent avec ce que
le site affirme par ailleurs sur ces traditions.

---

## Le reste du site

Les mêmes doublons existent ailleurs, à un degré moindre :

- **`blog.html`** — les 6 articles se partagent 4 images
- **`index.html`** — le slider et les cartes réutilisent les mêmes photos
- **Hôtels et restaurants** — celles-ci viennent de l'ancien site et sont déjà
  distinctes par établissement, rien à faire

Une fois les 18 destinations pourvues, ces photos-là pourront servir à alimenter
le blog et la page d'accueil : le problème se résout en grande partie tout seul.
