# Photos à fournir

Le site utilise actuellement des **visuels de remplacement dessinés** — un par
emplacement, tous différents, aux couleurs du projet. Ils tiennent la place
proprement, mais ce ne sont pas des photos.

## Comment les remplacer

Déposer la photo dans `assets/img/dest/` **avec exactement le même nom**, en
`.jpg` ou `.webp`. Le générateur préfère automatiquement la photo au visuel de
remplacement — aucune autre modification n'est nécessaire.

```
assets/img/dest/tai.svg      ← visuel actuel
assets/img/dest/tai.jpg      ← déposer ici, il prend le dessus
```

Puis `python3 build.py` et renvoyer les pages.

**Format conseillé :** 1200 × 750 px minimum, en paysage, format `.webp` de
préférence (deux fois plus léger qu'un `.jpg` à qualité égale).

## Liste des fichiers

Les lignes en gras sont celles que le client a explicitement demandées.

| Fichier | Sujet attendu | Apparaît sur |
|---|---|---|
| `abidjan.jpg` | Le Plateau depuis la lagune, ou la cathédrale Saint-Paul | `destination-culture`, `destinations`, `mediatheque` +4 |
| `assinie.jpg` | La langue de sable entre lagune et océan, vue large | `destination-beaches`, `destinations`, `mediatheque` +6 |
| `banco.jpg` | Forêt du Banco, ou le fanico au bord de la rivière | `destination-eco`, `destinations`, `place-banco` +4 |
| `blog-city.jpg` | Article « une semaine à Abidjan » | `blog` |
| `blog-coast.jpg` | Article plages | `blog` |
| `blog-culture.jpg` | Article Femua — concert, foule | `blog`, `index` |
| `blog-gastronomy.jpg` | Article Embassy Chef Challenge — **image envoyée par mail** | `blog`, `index` |
| `blog-nature.jpg` | Article forêt de Taï | `blog` |
| `bouake.jpg` | Le grand marché, ou les potières de Katiola | `destination-culture`, `destinations`, `place-bouake` |
| `cat-beach.jpg` | Image d'appel du littoral (carte d'accueil) | `destinations`, `index`, `transport` |
| `cat-culture.jpg` | **Image d'appel culture** — masque, danse, festival | `destination-culture`, `destinations`, `index` |
| `cat-eco.jpg` | **Image d'appel nature** — forêt ou montagne | `destination-eco`, `destinations`, `index` |
| `comoe.jpg` | **Savane et fleuve Comoé**, hippopotames ou oiseaux | `destination-eco`, `destinations`, `mediatheque` +5 |
| `deal-food.jpg` | Un plat ivoirien, attiéké poisson de préférence | `blog`, `destination-beaches`, `gastronomies` +2 |
| `deal-hotel.jpg` | Un hôtel ou lodge (rubrique Hôtels) | `good-deal`, `hotel`, `index` |
| `deal-transport.jpg` | Route, véhicule ou chauffeur | `good-deal`, `transport` |
| `ehotile.jpg` | Mangrove et pirogue dans la lagune Aby | `destination-eco`, `destinations`, `mediatheque` +4 |
| `gallery.jpg` | Bannière de la médiathèque | `mediatheque` |
| `grand-bassam.jpg` | Quartier France : façades coloniales en brique rouge, ou la plage | `destination-beaches`, `destinations`, `mediatheque` +6 |
| `grand-lahou.jpg` | Les bâtiments repris par l'océan, ou la mangrove d'Azagny | `destination-beaches`, `destinations`, `place-grand-lahou` |
| `hero-1.jpg` | Diapo d'accueil 1 — plage ou lagune | `contact`, `index` |
| `hero-2.jpg` | Diapo d'accueil 2 — culture | `faq`, `index` |
| `hero-3.jpg` | Diapo d'accueil 3 — nature | `index` |
| `jacqueville.jpg` | Cocoteraie ou plage, avec des pirogues | `destination-beaches`, `destinations`, `place-jacqueville` |
| `korhogo.jpg` | Toiles peintes de Fakaha, ou un atelier de tisserand | `destination-culture`, `destinations`, `mediatheque` +6 |
| `man.jpg` | **Cascade ou pont de lianes** — le client a demandé les montagnes | `destination-culture`, `destination-eco`, `destinations` +7 |
| `nimba.jpg` | Le massif, prairies d'altitude | `destination-eco`, `destinations`, `place-nimba` |
| `san-pedro.jpg` | Une plage de la côte ouest, Grand-Béréby si possible | `destination-beaches`, `destinations`, `place-assinie` +3 |
| `sassandra.jpg` | Le port de pêche et ses pirogues, ou une crique | `destination-beaches`, `destinations`, `place-assinie` +5 |
| `tai.jpg` | **Forêt primaire** — canopée, troncs à contreforts, ou un chimpanzé | `destination-eco`, `destinations`, `mediatheque` +5 |
| `tiegba.jpg` | Le village sur pilotis vu depuis l'eau | `destination-culture`, `destinations`, `place-tiegba` |
| `yamoussoukro.jpg` | La basilique Notre-Dame de la Paix, vue d'ensemble | `destination-culture`, `destinations`, `place-abidjan` +5 |

## Priorités du client

1. ~~Logo SUBLIME CI-USA~~ — **fait**. Détouré depuis l'image fournie et
   installé : `assets/img/logo-mark.webp` (en-tête) et `logo-full.webp`
   (pied de page), avec les `.png` en secours.
2. `cat-culture` et `cat-eco` — les cartes de l'accueil.
3. `blog-gastronomy` — l'image de remplacement envoyée par mail.
4. `tai`, `comoe`, `man` — les parcs et les montagnes.
5. `blog-culture`, `blog-gastronomy`, `blog-coast`, `blog-city`, `blog-nature`,
   `deal-food` — la rubrique « All » du blog.
6. Les 17 lieux, pour les pages de destination.

---

# Prompts pour les visuels manquants

Les 17 prompts de destination reçus couvrent les lieux. Il manque **11 autres
emplacements**, dont ceux que le client a demandés en priorité. Même direction
artistique que les autres : *photorealistic premium tourism photography,
authentic Côte d'Ivoire, natural lighting, no text, no logos, no watermark,
4:3 landscape composition.*

### cat-culture — carte « Voyages culturels » (accueil, priorité client)
> Ultra-realistic professional tourism photograph representing Ivorian cultural
> heritage, a traditional Dan or Senufo mask ceremony in a village setting,
> dancers in raffia costume, drummers, villagers watching, warm afternoon light,
> respectful documentary framing, authentic West African atmosphere,
> photorealistic, natural colors, 4:3 aspect ratio, no text, no logos.

### cat-eco — carte « Aventure & écotourisme » (accueil, priorité client)
> Ultra-realistic professional tourism photograph of the Ivorian western
> highlands, green mountain ridges, a woven liana bridge crossing a forest
> river, dense tropical vegetation, two hikers on the bridge seen from a
> distance, soft morning light, adventurous atmosphere, photorealistic,
> natural colors, 4:3 aspect ratio, no text, no logos.

### cat-beach — carte « Plages & littoral » (accueil)
> Ultra-realistic aerial tourism photograph of the Ivorian coastline where a
> lagoon meets the Atlantic, a narrow sand spit lined with coconut palms,
> turquoise water on one side and ocean swell on the other, a few small boats,
> bright tropical daylight, photorealistic, 4:3 aspect ratio, no text, no logos.

### hero-1 / hero-2 / hero-3 — diaporama d'accueil, plein écran
Ces trois-là sont affichées en très grand, derrière du texte blanc. Il leur
faut une **zone sombre ou calme à gauche**, sinon le titre devient illisible.

> **hero-1** — Ultra-realistic wide tourism photograph of an Ivorian beach at
> golden hour, long shoreline, coconut palms on the left in shadow, warm light
> on the water to the right, empty space in the left third of the frame,
> cinematic, photorealistic, 16:9 aspect ratio, no text, no logos.

> **hero-2** — Ultra-realistic wide photograph of Abidjan at dusk, the Plateau
> skyline reflected in the Ébrié lagoon, warm city lights, darker foreground on
> the left, cinematic, photorealistic, 16:9 aspect ratio, no text, no logos.

> **hero-3** — Ultra-realistic wide photograph of the Taï rainforest canopy seen
> from above at sunrise, mist between the trees, deep greens, darker vegetation
> filling the left third, cinematic, photorealistic, 16:9 aspect ratio, no text,
> no logos.

### deal-hotel — rubrique Hôtels
> Ultra-realistic tourism photograph of a lagoon-side lodge terrace in Assinie,
> wooden deck, rattan furniture, palm shade, calm water beyond, late afternoon
> light, warm and inviting, photorealistic, 4:3 aspect ratio, no text, no logos.

### deal-food — rubrique Gastronomie
> Ultra-realistic food photograph of an Ivorian meal served at a maquis: grilled
> tilapia with attiéké, alloco and pepper sauce on an enamel plate, wooden
> table, natural daylight, appetising but unstyled, authentic, photorealistic,
> 4:3 aspect ratio, no text, no logos.

### deal-transport — rubrique Transport
> Ultra-realistic photograph of a coastal road in Côte d'Ivoire, a clean 4x4
> travelling between palm plantations, green vegetation, blue sky, sense of
> journey, photorealistic, natural colors, 4:3 aspect ratio, no text, no logos.

### blog-culture / blog-coast / blog-city / blog-nature — vignettes du blog
Ces quatre peuvent reprendre les visuels de lieu si le budget est limité :
`abidjan` pour blog-city, `tai` pour blog-nature, `grand-bassam` pour
blog-coast. Seule `blog-culture` (article Femua) mérite sa propre image :

> Ultra-realistic photograph of an outdoor urban music festival in Abidjan at
> night, a large crowd with hands raised, stage lights, energetic atmosphere,
> photorealistic, natural colors, 4:3 aspect ratio, no text, no logos.

### gallery — bannière de la médiathèque
> Ultra-realistic photograph of an Ivorian craft market stall, painted Korhogo
> cloth, carved wood, woven baskets, warm daylight, rich textures,
> photorealistic, 4:3 aspect ratio, no text, no logos.

---

# Installer les photos

Une fois les images produites, nommez chaque fichier avec son identifiant
(`grand-bassam.jpg`, `tai.png`, `cat-culture.webp`…), placez-les dans un
dossier, puis :

```bash
python3 tools/import-photos.py ~/mon-dossier-photos
python3 build.py
```

Le script recadre en 4:3, redimensionne à 1200 px, convertit en WebP et
installe dans `assets/img/dest/`. Il signale les noms non reconnus et affiche
ce qui manque encore. `--dry-run` pour simuler sans rien écrire.
