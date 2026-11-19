# -*- coding: utf-8 -*-
"""Traduction française du site.

Principe : les pages sont générées en anglais, puis traduites par
remplacement de chaînes exactes. Les couples issus de content.py
(descriptions de lieux, FAQ des destinations) sont ajoutés
automatiquement — ce fichier ne contient que le reste : navigation,
accueil, services, pages Good Deal, formulaires, pied de page.

Pour ajouter une traduction : une ligne ('anglais', 'français').
Les chaînes doivent correspondre exactement au HTML généré.
Le contrôle de couverture se lance avec :  python3 build.py --check-fr
"""

from content import pairs as _content_pairs
from places import pairs as _places_pairs

# ---------------------------------------------------------------- CHROME
CHROME = [
    # --- barre utilitaire, navigation ---
    ("A great destination for <strong>American travelers</strong>",
     "Une grande destination pour les <strong>voyageurs américains</strong>"),
    ("Washington · Abidjan", "Washington · Abidjan"),
    (">Home<", ">Accueil<"),
    (">Media library<", ">Médiathèque<"),
    (">Blog &amp; News<", ">Blog &amp; actualités<"),
    (">Destinations — overview<", ">Destinations — vue d'ensemble<"),
    (">Beaches &amp; coastline<", ">Plages &amp; littoral<"),
    (">Cultural trips<", ">Voyages culturels<"),
    (">Adventure &amp; ecotourism<", ">Aventure &amp; écotourisme<"),
    (">Good Deal — overview<", ">Bons plans — vue d'ensemble<"),
    (">Overview<", ">Vue d'ensemble<"),
    (">Hotel<", ">Hôtels<"),
    (">Gastronomies<", ">Gastronomie<"),
    (">Transport<", ">Transport<"),
    (">Contact us<", ">Nous contacter<"),
    (">Plan your trip<", ">Planifier mon voyage<"),
    (">See destinations<", ">Voir les destinations<"),
    ("Open menu", "Ouvrir le menu"),
    ("Close menu", "Fermer le menu"),
    ("Back to top", "Haut de page"),

    # --- hero accueil ---
    ("Abidjan is closer<br>than you <em>think</em>.",
     "Abidjan est plus proche<br>que vous ne le <em>croyez</em>."),
    ("Sublime CI-USA plans the whole journey from Washington, D.C. — beaches, culture, "
     "forests and food — with people on the ground in Côte d'Ivoire.",
     "Sublime CI-USA organise le voyage de bout en bout depuis Washington — plages, "
     "culture, forêts et cuisine — avec des équipes présentes en Côte d'Ivoire."),
    (">Departure<", ">Départ<"),
    (">Arrival<", ">Arrivée<"),
    (">Best season<", ">Meilleure saison<"),
    ("December — April", "Décembre — avril"),
    ("Ready when you are", "Quand vous voulez"),
    (">Get a quote<", ">Demander un devis<"),
    ("Washington, D.C.", "Washington D.C."),
    ("Abidjan, Côte d'Ivoire", "Abidjan, Côte d'Ivoire"),

    # --- accueil : destinations ---
    ("Three ways to see<br>Côte d'Ivoire", "Trois façons de découvrir<br>la Côte d'Ivoire"),
    (">All destinations<", ">Toutes les destinations<"),
    (">Coastline<", ">Littoral<"),
    (">Culture<", ">Culture<"),
    (">Nature<", ">Nature<"),
    ("Best Beaches in Ivory Coast", "Les plus belles plages"),
    ("Cultural Trips", "Voyages culturels"),
    ("Adventure &amp; Ecotourism", "Aventure &amp; écotourisme"),
    ("Assinie, Grand-Bassam, Sassandra — a southern coast of lagoons, surf and fishing "
     "villages, mapped end to end.",
     "Assinie, Grand-Bassam, Sassandra — une côte sud de lagunes, de vagues et de "
     "villages de pêcheurs, connue de bout en bout."),
    ("Festivals, mask traditions, markets and music — travel alongside guides who grew "
     "up with these stories.",
     "Festivals, traditions de masques, marchés et musique — accompagné de guides qui "
     "ont grandi avec ces histoires."),
    ("Taï rainforest, Man's waterfalls and highlands — small groups, low impact, local "
     "hosts.",
     "Forêt de Taï, cascades et montagnes de Man — petits groupes, faible impact, "
     "hôtes locaux."),
    (">Explore <", ">Découvrir <"),

    # --- accueil : news ---
    (">News<", ">Actualités<"),
    ("Unforgettable experiences", "Des expériences qu'on n'oublie pas"),
    (">Read the blog<", ">Lire le blog<"),
    ("Passport DC: Côte d'Ivoire opens its doors",
     "Passport DC : la Côte d'Ivoire ouvre ses portes"),
    (">Washington<", ">Washington<"),
    ("Femua, the festival that fills Abidjan", "Le Femua, le festival qui remplit Abidjan"),
    ("Côte d'Ivoire, guest of honour at the Embassy Chef Challenge",
     "La Côte d'Ivoire, invitée d'honneur de l'Embassy Chef Challenge"),
    ("Where to swim: the beaches worth the drive",
     "Où se baigner : les plages qui valent la route"),
    ("A first-timer's week in Abidjan", "Une première semaine à Abidjan"),
    ("Taï forest: what you actually see", "Forêt de Taï : ce qu'on y voit vraiment"),
    ("Five dishes to order before you leave", "Cinq plats à commander avant de repartir"),
    (">Gastronomy<", ">Gastronomie<"),
    (">City<", ">Ville<"),
    (">Travel notes<", ">Carnets de route<"),
    (">All<", ">Tout<"),

    # --- accueil : welcome ---
    ("Welcome to Sublime CI-USA", "Bienvenue chez Sublime CI-USA"),
    ("One agency on<br>both ends of<br>the route.",
     "Une agence aux<br>deux bouts<br>du trajet."),
    ("We are based in Washington, D.C. and work with partners in Abidjan, so the trip "
     "you book here is the trip that happens there. Landscapes, culture, history — "
     "organised by people who answer the phone in both time zones.",
     "Nous sommes basés à Washington et travaillons avec des partenaires à Abidjan : "
     "le voyage réservé ici est exactement celui qui se déroule là-bas. Paysages, "
     "culture, histoire — organisés par des gens qui décrochent le téléphone dans les "
     "deux fuseaux horaires."),
    ("Cities, one team", "Villes, une équipe"),
    ("Services end to end", "Services de bout en bout"),
    ("Partners on the ground", "Partenaires sur place"),
    ("Tailor-made itineraries", "Itinéraires sur mesure"),
    (">Learn more <", ">En savoir plus <"),
    ("Washington Dulles", "Washington Dulles"),
    ("Félix-Houphouët-Boigny", "Félix-Houphouët-Boigny"),

    # --- accueil : services ---
    (">Our services<", ">Nos services<"),
    ("Explore, discover, and<br>experience Côte d'Ivoire",
     "Explorer, découvrir et<br>vivre la Côte d'Ivoire"),
    ("Tailor-Made Trips", "Voyages sur mesure"),
    ("Itineraries built around what you actually want — adventure, rest, eco-tourism "
     "or culture.",
     "Des itinéraires construits autour de ce que vous voulez vraiment — aventure, "
     "repos, écotourisme ou culture."),
    (">Booking<", ">Réservation<"),
    ("Hotels, lodges and guesthouses we have visited, chosen for comfort and character.",
     "Hôtels, lodges et maisons d'hôtes que nous avons visités, choisis pour leur "
     "confort et leur caractère."),
    ("Transportation &amp; Logistics", "Transport &amp; logistique"),
    ("Airport transfers, city drivers and excursion vehicles — vetted and insured.",
     "Transferts aéroport, chauffeurs en ville et véhicules d'excursion — vérifiés et "
     "assurés."),
    ("Experienced Tour Guides", "Guides expérimentés"),
    ("Local guides who translate more than language — context, etiquette and history.",
     "Des guides locaux qui traduisent plus que la langue — le contexte, les usages et "
     "l'histoire."),
    ("Travel Assistance", "Assistance au voyage"),
    ("Visa paperwork, flight reservations and the small administrative steps in "
     "between.",
     "Dossier de visa, réservation des vols et toutes les petites démarches entre les "
     "deux."),
    ("Tell us where you want to go.", "Dites-nous où vous voulez aller."),
    ("Send a few dates and we come back with a route.",
     "Envoyez quelques dates, nous revenons avec un itinéraire."),
    (">Start planning <", ">Commencer <"),

    # --- accueil : vision ---
    (">Our vision<", ">Notre vision<"),
    ("Travel is discovery,<br>exchange, and<br>something you keep.",
     "Voyager, c'est découvrir,<br>échanger, et<br>en garder quelque chose."),
    ("We are committed to responsible, sustainable tourism that shows Côte d'Ivoire's "
     "natural and cultural treasures while supporting the communities that keep them "
     "alive.",
     "Nous sommes engagés dans un tourisme responsable et durable, qui met en valeur "
     "les trésors naturels et culturels de la Côte d'Ivoire tout en soutenant les "
     "communautés qui les font vivre."),

    # --- accueil : good deal ---
    ("Where to sleep,<br>what to eat", "Où dormir,<br>que manger"),
    (">All good deals<", ">Tous les bons plans<"),
    ("Hotels &amp; Restaurants", "Hôtels &amp; restaurants"),
    ("Places we send our own families", "Les adresses où nous envoyons nos proches"),
    ("From lagoon-side lodges to the maquis worth queueing for.",
     "Des lodges en bord de lagune aux maquis pour lesquels on fait la queue."),
    ("Content of interest", "À lire avant de partir"),
    ("Read before you fly", "À lire avant le départ"),
    ("Practical guides on transport, gastronomy and the seasons.",
     "Guides pratiques sur le transport, la gastronomie et les saisons."),
    (">Learn more <", ">En savoir plus <"),
    (">Our partners<", ">Nos partenaires<"),

    # --- pied de page + CTA ---
    (">Next departure<", ">Prochain départ<"),
    ("Plan your dream trip<br>to Côte d'Ivoire",
     "Organisez le voyage<br>dont vous rêvez"),
    ("Send us your dates and what you want out of the trip. We reply with a route, a "
     "price and the names of the people who will meet you.",
     "Envoyez-nous vos dates et ce que vous attendez du voyage. Nous répondons avec un "
     "itinéraire, un prix et le nom des personnes qui vous accueilleront."),
    ("Sublime CI-USA is a travel agency specialising in trips to Côte d'Ivoire, helping "
     "American travelers explore its cultural, natural and historical heritage.",
     "Sublime CI-USA est une agence de voyage spécialisée dans les séjours en Côte "
     "d'Ivoire, qui accompagne les voyageurs américains à la découverte de son "
     "patrimoine culturel, naturel et historique."),
    (">Site map<", ">Plan du site<"),
    (">Hotels<", ">Hôtels<"),
    ("Official e-Visa (SNEDAI)", "e-Visa officiel (SNEDAI)"),
    ("Ministry of Tourism", "Ministère du Tourisme"),
    ("Embassy in Washington, D.C.", "Ambassade à Washington D.C."),
    (">Newsletter<", ">Newsletter<"),
    ("Your email address", "Votre adresse e-mail"),
    (">Send</button>", ">Envoyer</button>"),
    ("All rights reserved.", "Tous droits réservés."),

    # --- destinations : page d'aiguillage ---
    ("Eighteen places, in three families of trip. Each category has its own page, with "
     "what you see, what you do and the questions we get asked most.",
     "Dix-huit lieux, répartis en trois familles de voyage. Chaque catégorie a sa "
     "page, avec ce qu'on y voit, ce qu'on y fait et les questions qu'on nous pose le "
     "plus."),
    ("Three families of trip", "Trois familles de voyage"),
    ("Where to start", "Par où commencer"),
    ("Most of our travellers combine two categories over ten days: a coastal base and "
     "a cultural or nature excursion.",
     "La plupart de nos voyageurs combinent deux catégories sur dix jours : une base "
     "côtière et une incursion culturelle ou nature."),
    (">6 places<", ">6 lieux<"),
    ("Beaches &amp; coastline", "Plages &amp; littoral"),
    ("Grand-Bassam, Assinie, Sassandra, San Pedro, Jacqueville, Grand-Lahou. Lagoons, "
     "coves and fishing villages.",
     "Grand-Bassam, Assinie, Sassandra, San Pedro, Jacqueville, Grand-Lahou. Lagunes, "
     "criques et villages de pêcheurs."),
    (">See the coast <", ">Voir le littoral <"),
    ("Yamoussoukro, Korhogo, Man, Abidjan, Bouaké, Tiégba. Masks, crafts, festivals "
     "and heritage.",
     "Yamoussoukro, Korhogo, Man, Abidjan, Bouaké, Tiégba. Masques, artisanat, "
     "festivals et patrimoine."),
    (">See the culture <", ">Voir la culture <"),
    ("Taï, Comoé, Banco, Man, Ehotilé islands, Mount Nimba. Primary forest, savanna "
     "and mountains.",
     "Taï, Comoé, Banco, Man, îles Ehotilé, mont Nimba. Forêt primaire, savane et "
     "montagnes."),
    (">See the nature <", ">Voir la nature <"),
    ("The 18 places", "Les 18 lieux"),
    ("The whole country,<br>filterable", "Tout le pays,<br>filtrable"),
    ("No place matches.", "Aucun lieu ne correspond."),
    (">Beaches<", ">Plages<"),
    (">Nature<", ">Nature<"),

    # --- destinations : process ---
    ("How it works", "Comment ça marche"),
    ("From a first email<br>to the arrivals hall.",
     "D'un premier message<br>au hall d'arrivée."),
    ("Every itinerary is written from scratch. Here is the sequence, and it really is "
     "a sequence — each step depends on the one before it.",
     "Chaque itinéraire est écrit à partir de zéro. Voici la séquence, et c'en est "
     "vraiment une : chaque étape dépend de la précédente."),
    ("1 — You tell us the shape of the trip", "1 — Vous décrivez le voyage"),
    ("Dates, how many of you, what you want out of it, and a rough budget. Five "
     "minutes on a form or ten on the phone.",
     "Dates, nombre de personnes, ce que vous en attendez, un budget approximatif. "
     "Cinq minutes sur le formulaire ou dix au téléphone."),
    ("2 — We draft a route", "2 — Nous proposons un itinéraire"),
    ("Within two business days you get a day-by-day route with hotels, distances and a "
     "price. Nothing is booked yet.",
     "Sous deux jours ouvrés, un parcours jour par jour avec hôtels, distances et "
     "prix. Rien n'est encore réservé."),
    ("3 — We adjust it together", "3 — On l'ajuste ensemble"),
    ("Swap a beach for a park, add two days, drop the internal flight. As many rounds "
     "as it takes.",
     "Échanger une plage contre un parc, ajouter deux jours, supprimer le vol "
     "intérieur. Autant d'allers-retours que nécessaire."),
    ("4 — Booking and paperwork", "4 — Réservations et formalités"),
    ("We confirm hotels and transport, and prepare the visa file. You get a single "
     "itinerary document with every contact on it.",
     "Nous confirmons hôtels et transports, et montons le dossier de visa. Vous "
     "recevez un document unique avec tous les contacts."),
    ("5 — On the ground", "5 — Sur place"),
    ("Someone from our Abidjan team meets you at the airport, and there is a phone "
     "number that works for the whole trip.",
     "Quelqu'un de notre équipe d'Abidjan vous accueille à l'aéroport, et un numéro "
     "reste joignable pendant tout le séjour."),

    # --- pages destination ---
    (">Add to my trip <", ">Inclure dans mon voyage <"),
    (">Learn more <", ">En savoir plus <"),
    (">6 places<", ">6 lieux<"),
    ("Where we take<br>our travellers", "Où nous emmenons<br>nos voyageurs"),
    ("Good to know", "Bon à savoir"),
    ("Frequently asked", "Questions fréquentes"),
    ("Plages et littoral", "Plages et littoral"),

    ("Beaches &amp; coastline", "Plages &amp; littoral"),
    ("Five hundred kilometres of Atlantic, lagoons behind the dunes and a coast road "
     "that makes most of it reachable in a day.",
     "Cinq cents kilomètres d'Atlantique, des lagunes derrière les dunes et une route "
     "côtière qui rend la majeure partie accessible dans la journée."),
    ("From lagoon to ocean,<br>east to west.", "De la lagune à l'océan,<br>d'est en ouest."),
    ("The coast runs from the Ghanaian border to Liberia. To the east, the lagoons and "
     "coconut groves of Assinie and Grand-Bassam, an hour or two from Abidjan. To the "
     "west it turns wilder, down to Sassandra and San Pedro. Each stretch has its own "
     "character, and you can chain them or keep just one.",
     "Le littoral court de la frontière ghanéenne au Liberia. À l'est, les lagunes et "
     "les cocoteraies d'Assinie et de Grand-Bassam, à une heure ou deux d'Abidjan. À "
     "l'ouest, la côte devient plus sauvage jusqu'à Sassandra et San Pedro. Chaque "
     "étape a son caractère, et on peut les enchaîner ou n'en garder qu'une."),
    ("Build a coastal itinerary", "Construire un itinéraire littoral"),

    ("Around sixty languages, mask traditions that are still alive, recognised crafts "
     "and festivals that bring the whole country together.",
     "Une soixantaine de langues, des traditions de masques toujours vivantes, un "
     "artisanat reconnu et des festivals qui rassemblent le pays entier."),
    ("Living traditions,<br>not a museum.", "Des traditions vivantes,<br>pas un musée."),
    ("Côte d'Ivoire has more than sixty cultural groups, and it shows in everything: "
     "the music, the cloth, the masks, the food. Our cultural trips are built around "
     "real encounters — craft workshops, markets, ceremonies when the village calendar "
     "allows — with Ivorian guides who explain the context and the etiquette.",
     "La Côte d'Ivoire compte plus de soixante groupes culturels, et ça se voit dans "
     "tout : la musique, les tissus, les masques, la cuisine. Nos circuits culturels "
     "se construisent autour de rencontres réelles — ateliers d'artisans, marchés, "
     "cérémonies quand le calendrier villageois le permet — avec des guides ivoiriens "
     "qui expliquent le contexte et les usages."),
    ("Build a cultural trip", "Construire un circuit culturel"),

    ("Adventure &amp; ecotourism", "Aventure &amp; écotourisme"),
    ("Two World Heritage parks, one of the last primary rainforests in West Africa, "
     "and a mountain range in the west.",
     "Deux parcs classés au patrimoine mondial, une forêt primaire parmi les dernières "
     "d'Afrique de l'Ouest, et un massif montagneux à l'ouest."),
    ("From primary forest<br>to eighteen mountains.",
     "De la forêt primaire<br>aux dix-huit montagnes."),
    ("The country holds three environments within a short distance: the rainforest of "
     "the south-west, the savanna of the north-east, and the western highlands around "
     "Man. We work in small groups, with local guides and community accommodation — "
     "which is what supports the surrounding villages, and therefore what protects the "
     "parks.",
     "Le pays réunit trois milieux sur une distance courte : la forêt tropicale du "
     "sud-ouest, la savane du nord-est, et le relief de l'Ouest autour de Man. Nous "
     "travaillons en petits groupes, avec des guides et des hébergements "
     "communautaires — c'est ce qui fait vivre les villages riverains, et donc ce qui "
     "protège les parcs."),
    ("Build a nature trip", "Construire un circuit nature"),

    # --- good deal / hôtels / gastronomie / transport ---
    (">Good deal<", ">Bons plans<"),
    (">Good Deal<", ">Bons plans<"),
    ("Where to sleep, what to eat, how to get around. Three directories, all of them "
     "addresses we use ourselves.",
     "Où dormir, que manger, comment circuler. Trois répertoires, avec des adresses "
     "que nous utilisons nous-mêmes."),
    (">23 properties<", ">23 établissements<"),
    (">26 addresses<", ">26 adresses<"),
    (">3 options<", ">3 options<"),
    ("Cocody, Plateau, Marcory, Port-Bouët — capacity, contacts and neighbourhood for "
     "each one.",
     "Cocody, Plateau, Marcory, Port-Bouët — capacité, contacts et quartier pour "
     "chacun."),
    (">Browse hotels <", ">Voir les hôtels <"),
    ("Lagoon terraces, Italian kitchens, maquis and the classics to order on your "
     "first night.",
     "Terrasses sur la lagune, tables italiennes, maquis et les classiques à commander "
     "le premier soir."),
    (">Browse restaurants <", ">Voir les restaurants <"),
    ("Car rental, ride-hailing apps, and private drivers arranged through us.",
     "Location de voiture, applications VTC, et chauffeurs privés que nous organisons."),
    (">See the options <", ">Voir les options <"),

    ("Hotels in Abidjan", "Hôtels à Abidjan"),
    ("23 properties across Cocody, Plateau, Marcory and Port-Bouët, with capacity and "
     "direct contacts. Book any of them through us and you get our negotiated rate.",
     "23 établissements à Cocody, au Plateau, à Marcory et à Port-Bouët, avec capacité "
     "et contacts directs. Réservez par notre intermédiaire et vous bénéficiez de "
     "notre tarif négocié."),
    ("Search a hotel or a neighbourhood…", "Chercher un hôtel ou un quartier…"),
    (">results<", ">résultats<"),
    (" rooms", " chambres"),
    ("Capacity n/a", "Capacité non communiquée"),
    ("Contact details to confirm", "Coordonnées à confirmer"),
    (">Book through us <", ">Réserver avec nous <"),
    ("No hotel matches that search. Try a neighbourhood name, or ask us directly.",
     "Aucun hôtel ne correspond. Essayez un nom de quartier, ou demandez-nous "
     "directement."),
    ("Booking through Sublime CI-USA", "Réserver avec Sublime CI-USA"),
    ("One booking,<br>one contact.", "Une réservation,<br>un interlocuteur."),
    ("You can call these hotels yourself — the numbers are right there. But when we "
     "book, we hold the room against your itinerary, handle the deposit from the US, "
     "and you keep a single point of contact for the whole trip.",
     "Vous pouvez appeler ces hôtels vous-même, les numéros sont là. Mais quand nous "
     "réservons, nous bloquons la chambre en fonction de votre itinéraire, gérons "
     "l'acompte depuis les États-Unis, et vous gardez un seul interlocuteur pour tout "
     "le séjour."),
    (">Ask for availability <", ">Demander les disponibilités <"),

    ("Where to eat in Abidjan", "Où manger à Abidjan"),
    ("26 addresses across Plateau, Cocody, Zone 4 and beyond — from lagoon terraces to "
     "Italian kitchens and the maquis worth queueing for.",
     "26 adresses au Plateau, à Cocody, en Zone 4 et ailleurs — des terrasses sur la "
     "lagune aux tables italiennes, en passant par les maquis pour lesquels on fait la "
     "queue."),
    ("Search a restaurant or a street…", "Chercher un restaurant ou une rue…"),
    (">Reserve a table <", ">Réserver une table <"),
    ("No restaurant matches that search. Try a neighbourhood name, or ask us directly.",
     "Aucun restaurant ne correspond. Essayez un nom de quartier, ou demandez-nous "
     "directement."),
    ("Cocody &amp; Deux Plateaux", "Cocody &amp; Deux Plateaux"),
    ("Zone 4 &amp; Marcory", "Zone 4 &amp; Marcory"),
    (">Elsewhere<", ">Ailleurs<"),
    ("Ivorian classics", "Les classiques ivoiriens"),
    ("What to order,<br>wherever you sit", "Que commander,<br>où que vous soyez"),
    ("Attiéké &amp; grilled fish", "Attiéké poisson"),
    ("Cassava couscous with braised tilapia — the dish to order on your first evening.",
     "Semoule de manioc et tilapia braisé — le plat à commander le premier soir."),
    (">Kedjenou<", ">Kedjenou<"),
    ("Chicken slow-cooked in a sealed pot with peppers and tomato. Order it ahead.",
     "Poulet mijoté en cocotte scellée avec piments et tomate. À commander à l'avance."),
    (">Garba<", ">Garba<"),
    ("Fried tuna and attiéké, sold from street kiosks. The national snack.",
     "Thon frit et attiéké, vendu dans les kiosques de rue. L'en-cas national."),
    ("Sauce graine", "Sauce graine"),
    ("Palm nut stew with fish or beef, served over rice. Rich, and worth the nap after.",
     "Sauce de noix de palme au poisson ou au bœuf, servie sur du riz. Riche, et la "
     "sieste qui suit est méritée."),
    (">Alloco<", ">Alloco<"),
    ("Fried plantain with chilli onion relish. Ordered as a side, eaten as a meal.",
     "Banane plantain frite avec oignons pimentés. Commandé en accompagnement, mangé "
     "comme un plat."),
    ("Want a food-led itinerary?", "Envie d'un voyage autour de la cuisine ?"),
    ("Markets, maquis and cooking sessions, built into the route.",
     "Marchés, maquis et ateliers de cuisine, intégrés à l'itinéraire."),
    (">Tell us <", ">Dites-nous <"),

    ("Getting around Côte d'Ivoire", "Circuler en Côte d'Ivoire"),
    ("Whether you are visiting or living here, several options cover your journeys. "
     "Here are the main ones, and what each is good for.",
     "Que vous soyez de passage ou installé, plusieurs options couvrent vos "
     "déplacements. Voici les principales, et à quoi chacune convient."),
    (">Option 1<", ">Option 1<"),
    (">Option 2<", ">Option 2<"),
    (">Option 3<", ">Option 3<"),
    ("Car rental", "Location de voiture"),
    ("For maximum freedom, rent a vehicle from a certified agency.",
     "Pour une liberté maximale, louez un véhicule auprès d'une agence certifiée."),
    ("Freedom, autonomy and flexibility to explore the country at your own pace",
     "Liberté, autonomie et souplesse pour explorer le pays à votre rythme"),
    ("Access to places well off the usual routes",
     "Accès à des lieux hors des sentiers battus"),
    ("Comfort and convenience, and a schedule that is entirely yours",
     "Confort et commodité, avec un programme entièrement à vous"),
    (">Ask us to arrange it <", ">Nous le faire organiser <"),
    ("Ride-hailing (VTC)", "VTC"),
    ("For more comfort, tighter regulation, drivers who know the city, and the ability "
     "to book at any hour, use a ride-hailing service. Three platforms operate in "
     "Abidjan.",
     "Pour plus de confort, un cadre réglementé, des chauffeurs qui connaissent la "
     "ville et la possibilité de réserver à toute heure, utilisez un VTC. Trois "
     "plateformes opèrent à Abidjan."),
    ("An international platform, simple and widely available, operating in Abidjan and "
     "other cities such as Bouaké.",
     "Une plateforme internationale, simple et largement disponible, présente à "
     "Abidjan et dans d'autres villes comme Bouaké."),
    (">Open Yango <", ">Ouvrir Yango <"),
    ("The global ride-hailing leader is also present on the Ivorian market, mainly in "
     "Abidjan.",
     "Le leader mondial du VTC est également présent sur le marché ivoirien, "
     "principalement à Abidjan."),
    (">Order an Uber <", ">Commander un Uber <"),
    ("Another popular ride-hailing app, well suited to evenings, weekends and city "
     "trips.",
     "Une autre application populaire, bien adaptée aux soirées, aux week-ends et aux "
     "trajets en ville."),
    (">Open Heetch <", ">Ouvrir Heetch <"),
    ("Private driver,<br>arranged by us.", "Chauffeur privé,<br>organisé par nous."),
    ("For airport transfers and excursions we work with drivers we know, insured and "
     "reachable on one number for the whole trip. It is the option most of our "
     "travelers end up taking outside Abidjan, where apps thin out.",
     "Pour les transferts aéroport et les excursions, nous travaillons avec des "
     "chauffeurs que nous connaissons, assurés et joignables sur un seul numéro "
     "pendant tout le séjour. C'est l'option que la plupart de nos voyageurs "
     "retiennent hors d'Abidjan, là où les applications se raréfient."),
    (">Arrange transport <", ">Organiser le transport <"),
    ("Places to stay", "Où dormir"),
    ("From lagoon-side lodges in Assinie to business hotels in Plateau. We book the "
     "room and you get the rate we get.",
     "Des lodges en bord de lagune à Assinie aux hôtels d'affaires du Plateau. Nous "
     "réservons la chambre et vous bénéficiez de notre tarif."),
    (">Coast<", ">Littoral<"),
    ("Lodges &amp; beach houses", "Lodges &amp; maisons de plage"),
    ("Assinie, Grand-Bassam and Sassandra — small properties, mostly family-run.",
     "Assinie, Grand-Bassam et Sassandra — de petits établissements, souvent "
     "familiaux."),
    (">Abidjan<", ">Abidjan<"),
    ("City hotels", "Hôtels de ville"),
    ("Plateau, Cocody and Marcory, chosen for location as much as comfort.",
     "Plateau, Cocody et Marcory, choisis autant pour l'emplacement que pour le "
     "confort."),
    (">Ask for options <", ">Demander des options <"),

    # --- blog / médiathèque / FAQ ---
    ("Blog &amp; News", "Blog &amp; actualités"),
    ("Festivals, food, and notes from the road — written by the people who run the "
     "trips.",
     "Festivals, cuisine et carnets de route — écrits par ceux qui organisent les "
     "voyages."),
    ("Media library", "Médiathèque"),
    ("Photographs from our trips and from partners across Côte d'Ivoire. Click any "
     "image to open it full size.",
     "Photographies de nos voyages et de nos partenaires en Côte d'Ivoire. Cliquez sur "
     "une image pour l'ouvrir en grand."),
    (">Photos<", ">Photos<"),
    ("The country, as we found it", "Le pays, tel que nous l'avons trouvé"),
    ("Frequently asked questions", "Questions fréquentes"),
    ("Visas, seasons, flights, prices. If your question isn't here, the chat button at "
     "the bottom right answers most things instantly.",
     "Visas, saisons, vols, tarifs. Si votre question n'y est pas, le bouton de "
     "discussion en bas à droite répond à la plupart des demandes instantanément."),

    # --- contact ---
    ("Tell us about your trip", "Parlez-nous de votre voyage"),
    ("Dates, group size and what you want out of it. We reply within two business days "
     "with a route and a price.",
     "Dates, taille du groupe et ce que vous en attendez. Nous répondons sous deux "
     "jours ouvrés avec un itinéraire et un prix."),
    ("Request a quote", "Demander un devis"),
    ("Thanks — your request is in. We reply within two business days.",
     "Merci — votre demande est enregistrée. Nous répondons sous deux jours ouvrés."),
    ("First name", "Prénom"),
    ("Last name", "Nom"),
    (">Email<", ">E-mail<"),
    (">Phone<", ">Téléphone<"),
    ("Type of trip", "Type de voyage"),
    ("Choose one", "Choisissez"),
    ("Cultural trip", "Voyage culturel"),
    ("Mixed / not sure yet", "Mixte / pas encore décidé"),
    ("Approximate dates", "Dates approximatives"),
    ("e.g. March 2027, 10 days", "ex. mars 2027, 10 jours"),
    ("Your message", "Votre message"),
    ("How many of you, what you'd like to see, anything we should know.",
     "Combien vous êtes, ce que vous aimeriez voir, tout ce qu'il faut savoir."),
    ("Send request", "Envoyer la demande"),
    ("By sending this form you agree that we may contact you about your trip. We do "
     "not share your details with anyone else.",
     "En envoyant ce formulaire, vous acceptez que nous vous contactions au sujet de "
     "votre voyage. Vos coordonnées ne sont transmises à personne d'autre."),
    ("Leave this empty", "Laissez ce champ vide"),
    (">Required.<", ">Champ obligatoire.<"),
    ("Enter a valid email address.", "Saisissez une adresse e-mail valide."),
    (">Office<", ">Bureau<"),

    # --- 404 ---
    ("Error 404", "Erreur 404"),
    ("This route<br>doesn't exist.", "Cette route<br>n'existe pas."),
    ("The page you were looking for has moved or never existed. The ones below "
     "definitely do.",
     "La page que vous cherchiez a été déplacée ou n'a jamais existé. Celles "
     "ci-dessous, si."),
    ("Back to home", "Retour à l'accueil"),

    # --- chatbot ---
    ("Chat with Aya", "Discuter avec Aya"),
    ("Ivorian-American · online", "Ivoiro-américaine · en ligne"),
    ("Ask Aya a question…", "Posez votre question à Aya…"),

    # --- titres d'onglet ---
    ("Washington D.C. to Abidjan", "De Washington D.C. à Abidjan"),
    (">Hotels<", ">Hôtels<"),
    ("Beaches & coastline", "Plages & littoral"),
    ("Cultural trips", "Voyages culturels"),
    ("Adventure & ecotourism", "Aventure & écotourisme"),
    ("Media library", "Médiathèque"),
    ("Blog & News", "Blog & actualités"),
    ("Good Deal", "Bons plans"),
    ("Page not found", "Page introuvable"),
    ("Contact us", "Nous contacter"),
    ("Gastronomies", "Gastronomie"),
    ("Transport", "Transport"),
    ("Destinations", "Destinations"),
    ("Hotels", "Hôtels"),
    ("FAQ", "FAQ"),

    # --- événement Two Cities, One Friendship ---
    ("Two Cities,<br>One Friendship", "Deux villes,<br>une amitié"),
    ("Two Cities, One Friendship: Rockville meets Korhogo",
     "Two Cities, One Friendship : Rockville à la rencontre de Korhogo"),
    ("Two Cities, One Friendship", "Two Cities, One Friendship"),
    ("Rockville, Maryland and Korhogo, Côte d'Ivoire — an evening of culture, music and heritage. Friday, December 11, 2026.",
     "Rockville (Maryland) et Korhogo (Côte d'Ivoire) — une soirée de culture, de musique et de patrimoine. Vendredi 11 décembre 2026."),
    ("Rockville, Maryland and Korhogo, Côte d'Ivoire — a celebration of culture and heritage, December 11, 2026.",
     "Rockville (Maryland) et Korhogo (Côte d'Ivoire) — une célébration de la culture et du patrimoine, le 11 décembre 2026."),

    ("Admission is by invitation. Let us know you are coming so we can plan the evening.",
     "L'entrée se fait sur invitation. Dites-nous que vous venez, pour que nous puissions préparer la soirée."),
    ("RSVP for this event", "Confirmer ma présence"),
    ("Reserve your place", "Réserver ma place"),
    (">The evening<", ">La soirée<"),
    ("One evening,<br>two cultures.", "Une soirée,<br>deux cultures."),
    ("On December 11, Glenview Mansion in Rockville becomes the meeting point between Maryland and northern Côte d'Ivoire. The evening celebrates what the two communities share and what each brings: music, dance, craft, food and the people who carry them.",
     "Le 11 décembre, Glenview Mansion à Rockville devient le point de rencontre entre le Maryland et le nord de la Côte d'Ivoire. La soirée célèbre ce que les deux communautés ont en commun et ce que chacune apporte : musique, danse, artisanat, cuisine, et les gens qui les font vivre."),
    ("Ivorian rhythms and dance, the woven and painted textiles of the Senufo country, and a table that puts the two cuisines side by side. It is a cultural evening before it is a formal one — come to meet people.",
     "Rythmes et danses ivoiriens, tissages et toiles peintes du pays sénoufo, et une table où les deux cuisines se côtoient. C'est une soirée culturelle avant d'être une soirée officielle : on y vient pour rencontrer des gens."),

    (">The other city<", ">L'autre ville<"),
    ("Where Korhogo sits", "Où se trouve Korhogo"),
    ("Korhogo is the capital of northern Côte d'Ivoire and the heart of Senufo country — the region behind the painted cloth, the carving and the weaving you will see at Glenview Mansion.",
     "Korhogo est la capitale du nord de la Côte d'Ivoire et le cœur du pays sénoufo — la région d'où viennent les toiles peintes, la sculpture et le tissage que vous verrez à Glenview Mansion."),
    (">Discover Korhogo <", ">Découvrir Korhogo <"),
    ("Northern Côte d'Ivoire", "Nord de la Côte d'Ivoire"),
    ("Festivals, mask traditions, craft workshops and markets — the trips built around the culture you will meet that evening.",
     "Festivals, traditions de masques, ateliers d'artisans et marchés — les voyages construits autour de la culture que vous découvrirez ce soir-là."),
    (">Plan a trip<", ">Préparer un voyage<"),
    ("Go and see for yourself", "Aller voir par vous-même"),
    ("If the evening makes you want to travel, we build the itinerary — from Washington to Abidjan and up to Korhogo.",
     "Si la soirée vous donne envie de partir, nous construisons l'itinéraire — de Washington à Abidjan, puis jusqu'à Korhogo."),
    (">Talk to us <", ">Nous en parler <"),

    ("Before you come", "Avant de venir"),
    ("How do I confirm my attendance?", "Comment confirmer ma présence ?"),
    ("Confirm through the RSVP form on this page, listing everyone coming with you so the welcome desk has their names. You can also call",
     "Par le formulaire de confirmation sur cette page, en indiquant le nom des personnes qui vous accompagnent pour que l'accueil les ait. Vous pouvez aussi appeler le"),
    ("Where exactly is Glenview Mansion?", "Où se trouve exactement Glenview Mansion ?"),
    ("603 Edmonston Drive, Rockville, MD 20851, inside Rockville Civic Center Park. On-site parking is available in the park.",
     "603 Edmonston Drive, Rockville, MD 20851, dans le Rockville Civic Center Park. Un stationnement est disponible sur place."),
    ("Can I bring guests?", "Puis-je venir accompagné ?"),
    ("Yes — list them by name in the RSVP form so we can account for them.",
     "Oui — indiquez leurs noms dans le formulaire pour que nous puissions les compter."),
    ("Who do I contact with a question?", "Qui contacter pour une question ?"),
    ("Write to", "Écrivez à"),
    (", or leave your question in the comments box at the end of the RSVP form.",
     ", ou laissez votre question dans la zone de commentaires à la fin du formulaire."),
    (">Date<", ">Date<"),
    (">Time<", ">Horaire<"),
    (">Venue<", ">Lieu<"),
    (">Address<", ">Adresse<"),
    ("Friday, December 11, 2026", "Vendredi 11 décembre 2026"),
    ("6:00 PM – 10:00 PM", "18 h – 22 h"),
    (">Event<", ">Événement<"),
    (">Upcoming<", ">À venir<"),

    # --- méta-descriptions ---
    ("Tailor-made trips to Côte d'Ivoire for American travelers.",
     "Des voyages sur mesure en Côte d'Ivoire pour les voyageurs américains."),
    ("Beaches, cultural trips and ecotourism in Côte d'Ivoire.",
     "Plages, voyages culturels et écotourisme en Côte d'Ivoire."),
    ("The Ivorian coastline, from Grand-Bassam to San Pedro.",
     "Le littoral ivoirien, de Grand-Bassam à San Pedro."),
    ("Festivals, masks, crafts and heritage in Côte d'Ivoire.",
     "Festivals, masques, artisanat et patrimoine en Côte d'Ivoire."),
    ("National parks, primary rainforest and the western highlands.",
     "Parcs nationaux, forêt primaire et montagnes de l'Ouest."),
    ("Hotels, gastronomy and transport in Côte d'Ivoire.",
     "Hôtels, gastronomie et transport en Côte d'Ivoire."),
    ("Hotels in Abidjan — capacity, contacts and neighbourhood.",
     "Hôtels d'Abidjan — capacité, contacts et quartier."),
    ("Restaurants in Abidjan by neighbourhood.",
     "Les restaurants d'Abidjan, quartier par quartier."),
    ("Car rental, ride-hailing and private drivers in Côte d'Ivoire.",
     "Location de voiture, VTC et chauffeurs privés en Côte d'Ivoire."),
    ("News and travel notes from Côte d'Ivoire.",
     "Actualités et carnets de route de Côte d'Ivoire."),
    ("Photos and videos of Côte d'Ivoire.",
     "Photos et vidéos de Côte d'Ivoire."),
    ("Answers about visas, seasons, flights and prices.",
     "Réponses sur les visas, les saisons, les vols et les tarifs."),
    ("Plan your trip to Côte d'Ivoire with Sublime CI-USA.",
     "Organisez votre voyage en Côte d'Ivoire avec Sublime CI-USA."),
    ("This page does not exist.", "Cette page n'existe pas."),

    # --- noms composés (à garder avant les mots isolés) ---
    ("Korhogo and Senufo country", "Korhogo et le pays sénoufo"),
    ("Man and the masks of the West", "Man et les masques de l'Ouest"),
    ("The Man region", "La région de Man"),
    ("Taï National Park", "Le parc national de Taï"),
    ("Comoé National Park", "Le parc national de la Comoé"),
    ("Banco National Park", "Le parc national du Banco"),
    ("Ehotilé Islands", "Les îles Ehotilé"),
    ("Mount Nimba", "Le mont Nimba"),

    # --- FAQ ---
    ("Do American travelers need a visa for Côte d'Ivoire?",
     "Les voyageurs américains ont-ils besoin d'un visa pour la Côte d'Ivoire ?"),
    ("Most US passport holders do. We prepare the application file as part of our "
     "Travel Assistance service, and yellow fever vaccination is required for entry.",
     "La plupart des détenteurs d'un passeport américain, oui. Nous montons le dossier "
     "dans le cadre de notre service d'assistance, et la vaccination contre la fièvre "
     "jaune est obligatoire à l'entrée."),
    ("When is the best time to go?", "Quelle est la meilleure période pour partir ?"),
    ("December to April is the main dry season in the south and the most reliable "
     "window for beaches. The north has a different rhythm, with rain concentrated "
     "between June and September.",
     "De décembre à avril, c'est la grande saison sèche du sud et la fenêtre la plus "
     "fiable pour les plages. Le nord suit un autre rythme, avec des pluies "
     "concentrées entre juin et septembre."),
    ("Is there a nonstop flight from Washington?",
     "Existe-t-il un vol direct depuis Washington ?"),
    ("No. Itineraries connect through Paris, Brussels, Casablanca or Addis Ababa. We "
     "can hold and issue the reservation for you.",
     "Non. Les itinéraires passent par Paris, Bruxelles, Casablanca ou Addis-Abeba. "
     "Nous pouvons poser l'option et émettre le billet pour vous."),
    ("What language is spoken?", "Quelle langue parle-t-on ?"),
    ("French is the official language, alongside around sixty local languages. All our "
     "guides work in English.",
     "Le français est la langue officielle, aux côtés d'une soixantaine de langues "
     "locales. Tous nos guides travaillent aussi en anglais."),
    ("How much does a trip cost?", "Combien coûte un voyage ?"),
    ("It depends on length, comfort level and group size, so every trip is quoted "
     "individually. Send your dates and we come back within two business days with a "
     "route and a price.",
     "Cela dépend de la durée, du niveau de confort et de la taille du groupe : chaque "
     "voyage est chiffré sur mesure. Envoyez vos dates, nous revenons sous deux jours "
     "ouvrés avec un itinéraire et un prix."),
    ("Can you organise trips for groups?",
     "Organisez-vous des voyages de groupe ?"),
    ("Yes — families, church groups, diaspora reunions and small corporate "
     "delegations. Above eight people we build the itinerary differently, so tell us "
     "the group size early.",
     "Oui — familles, groupes paroissiaux, retrouvailles de la diaspora et petites "
     "délégations d'entreprise. Au-delà de huit personnes, l'itinéraire se construit "
     "autrement : indiquez-nous la taille du groupe dès le départ."),
    ("What about health and safety?", "Qu'en est-il de la santé et de la sécurité ?"),
    ("We brief you before departure on vaccinations, water, and which areas to avoid, "
     "and our Abidjan team is reachable throughout the trip.",
     "Nous vous informons avant le départ sur les vaccins, l'eau et les zones à "
     "éviter, et notre équipe d'Abidjan reste joignable pendant tout le séjour."),
]


def all_pairs():
    """Chrome + contenu des destinations, triés du plus long au plus court
    pour éviter qu'une chaîne courte ne casse une chaîne longue."""
    out = list(CHROME) + [(a, b) for a, b in _content_pairs() + _places_pairs() if a != b]
    seen, uniq = set(), []
    for a, b in out:
        if a not in seen:
            seen.add(a)
            uniq.append((a, b))
    return sorted(uniq, key=lambda p: -len(p[0]))
