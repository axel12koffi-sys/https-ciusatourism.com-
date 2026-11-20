# Envoyer l'invitation « Two Cities, One Friendship »

Deux fichiers, prêts à l'emploi :

| Fichier | Langue |
|---|---|
| `email/invitation-two-cities-en.html` | anglais |
| `email/invitation-two-cities-fr.html` | français |

Les boutons RSVP ouvrent le formulaire de la page de l'événement
(`ciusatourism.com/event-two-cities#rsvp`). **Pour envoyer à une liste,
utiliser plutôt la page d'envoi `/admin/send.php` (voir `RSVP.md`)** :
même mise en forme, invitation personnalisée, suivi des envois.

---

## À faire une fois, avant le premier envoi

**Déployer le site.** Les images de l'e-mail sont chargées depuis
`ciusatourism.com`. Tant que le déploiement n'est pas fait, les destinataires
verront des cadres vides à la place de la bannière et de l'affiche.

Vérifier dans un navigateur que ces trois adresses affichent bien une image :

- `https://ciusatourism.com/assets/img/logo-mark.png`
- `https://ciusatourism.com/assets/img/dest/event-two-cities.jpg`
- `https://ciusatourism.com/assets/img/dest/event-two-cities-poster.jpg`

---

## Méthode 1 — Gmail (la plus simple)

1. Ouvrir dans Chrome : `https://ciusatourism.com/email/invitation-two-cities-en.html`
2. Cliquer dans la page, puis **Ctrl + A** (tout sélectionner), **Ctrl + C** (copier)
3. Dans Gmail, **Nouveau message**, cliquer dans le corps, **Ctrl + V**
4. Renseigner l'objet, puis envoyer

Gmail conserve la mise en page, les images et le bouton. Ne pas retoucher le
texte dans Gmail après le collage : l'éditeur a tendance à casser les colonnes.
Pour corriger quelque chose, il vaut mieux le corriger dans le fichier et
recoller.

**Toujours s'envoyer un test d'abord**, et l'ouvrir sur téléphone en plus de
l'ordinateur.

### Destinataires en nombre

Gmail bloque au-delà de 500 envois par jour, et un envoi en copie visible
expose les adresses de tous les invités.

- Jusqu'à ~50 invités : mettre les adresses en **Cci** (copie cachée).
- Au-delà : passer par un outil d'emailing (méthode 2). L'invitation « People
  to People » reçue par la cliente était d'ailleurs envoyée par Constant
  Contact.

---

## Méthode 2 — Outil d'emailing (Mailchimp, Constant Contact, Brevo…)

Ces outils gèrent les listes, les désinscriptions et la délivrabilité.

1. Créer une campagne, choisir le modèle **« Code HTML »** / *Paste in code*
2. Ouvrir le fichier `.html` dans le Bloc-notes, tout copier, tout coller dans
   le champ prévu
3. Envoyer un test, puis la campagne

---

## Objet du message

Quelques formulations qui s'affichent entièrement sur mobile :

- `You're invited — Two Cities, One Friendship, December 11`
- `Rockville × Korhogo: an evening of culture, December 11`
- *(FR)* `Invitation — Two Cities, One Friendship, le 11 décembre`

Le texte d'aperçu (la ligne grise à côté de l'objet dans la boîte de réception)
est déjà inscrit dans le fichier : *Friday, December 11, 2026 · Glenview
Mansion, Rockville, Maryland · Please RSVP by December 5.*

---

## Modifier le contenu

Tout est en clair dans le fichier. Les points à surveiller :

- **Date limite de réponse** — « December 5 » / « 5 décembre » apparaît deux
  fois par fichier (bloc RSVP et texte d'aperçu).
- **Lien RSVP** — `ciusatourism.com/event-two-cities#rsvp` apparaît deux fois
  (bouton RSVP et bouton « Reserve your seat »). Ne pas le modifier : la page
  d'envoi s'en sert pour pré-remplir le nom et l'adresse de chaque invité.
- **`<!--GREETING-->`** — emplacement de la salutation « Dear Jane, » ajoutée
  par la page d'envoi. À laisser en place.
- **Ne pas remplacer les tableaux par des `div`.** Outlook ne sait pas les
  afficher : la mise en page se retrouverait en une seule colonne.
- **Ne pas utiliser d'images `.webp`.** Outlook ne les affiche pas. C'est pour
  cette raison que l'e-mail utilise les versions `.jpg` et `.png`.

---

## Aperçu du lien seul

Si le lien `ciusatourism.com/event-two-cities` est collé dans un message,
WhatsApp, LinkedIn ou Facebook, l'aperçu affiche désormais la bannière de
l'événement, le titre et la description. Ces balises de partage sont générées
pour les 64 pages du site.

Après le déploiement, Facebook garde l'ancien aperçu en cache. Pour le forcer
à relire la page : `developers.facebook.com/tools/debug/`, coller l'adresse,
cliquer sur *Scrape Again*.
