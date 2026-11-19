# -*- coding: utf-8 -*-
"""Contenu des pages de lieu, une par destination.

Structure de chaque entrée :
    slug      identifiant d'URL, donne place-<slug>.html
    cat       beach | culture | eco  (pour le fil d'Ariane)
    name      nom affiché, identique dans les deux langues
    tag       situation courte (en, fr)
    lede      accroche sous le titre (en, fr)
    intro     deux paragraphes de présentation (en, fr)
    see       ce qu'on y voit : liste de (titre, texte), bilingue
    events    festivals et rendez-vous, liste de (titre, texte) — peut être vide
    facts     encadré pratique : liste de (libellé, valeur)
    img       image de couverture

Les couples (en, fr) alimentent automatiquement lang_fr.py.
"""

from paths import IMG as U

PLACES = []

# ============================================================== LITTORAL

PLACES.append(dict(
    slug="grand-bassam", cat="beach", name="Grand-Bassam",
    img="assets/img/dest/grand-bassam.svg",
    tag=("Coastline · 45 min from Abidjan", "Littoral · 45 min d'Abidjan"),
    lede=("The country's first colonial capital, a UNESCO World Heritage site, and the "
          "beach at the end of every street.",
          "Première capitale coloniale du pays, site du patrimoine mondial de l'UNESCO, "
          "et la plage au bout de chaque rue."),
    intro=(
        "Grand-Bassam was the capital of French Côte d'Ivoire from 1893, until a yellow "
        "fever epidemic pushed the administration inland. What it left behind is a "
        "colonial quarter that has aged without being restored into a theme park: "
        "customs houses, the governor's palace, a post office and merchant villas, red "
        "brick and shuttered verandas, standing between the Ébrié lagoon and the "
        "Atlantic. UNESCO listed the town in 2012.\n\n"
        "It's forty-five minutes from Abidjan on a good road, which makes it the city's "
        "Sunday outing — busy at weekends, quiet during the week. Most visitors combine "
        "the heritage quarter in the morning with the beach in the afternoon, and that "
        "works well. If you only have one day outside Abidjan, this is the one to take.",
        "Grand-Bassam fut la capitale de la Côte d'Ivoire française à partir de 1893, "
        "jusqu'à ce qu'une épidémie de fièvre jaune pousse l'administration vers "
        "l'intérieur. Il en reste un quartier colonial qui a vieilli sans être "
        "transformé en décor : maison des douanes, palais du gouverneur, poste et "
        "villas de commerçants, brique rouge et vérandas à persiennes, entre lagune "
        "Ébrié et Atlantique. L'UNESCO a classé la ville en 2012.\n\n"
        "C'est à quarante-cinq minutes d'Abidjan par une bonne route, ce qui en fait la "
        "sortie du dimanche des Abidjanais — animée le week-end, calme en semaine. La "
        "plupart des visiteurs enchaînent le quartier historique le matin et la plage "
        "l'après-midi, et ça fonctionne bien. Si vous n'avez qu'une journée hors "
        "d'Abidjan, c'est celle-là qu'il faut prendre."),
    see=[
        (("The Quartier France", "Le quartier France"),
         ("The old administrative and trading district, listed by UNESCO. You walk it in "
          "an hour or two — the buildings are unequally maintained, some restored, some "
          "half swallowed by vegetation, which is precisely what gives the place its "
          "atmosphere.",
          "L'ancien quartier administratif et commerçant, classé par l'UNESCO. On le "
          "parcourt en une heure ou deux — les bâtiments sont inégalement entretenus, "
          "certains restaurés, d'autres à moitié repris par la végétation, et c'est "
          "précisément ce qui fait l'atmosphère du lieu.")),
        (("The National Costume Museum", "Le musée national du costume"),
         ("Housed in the former governor's palace, it displays the ceremonial dress of "
          "the country's cultural groups. Small, well laid out, and the best half-hour "
          "of context you can get before travelling further inland.",
          "Installé dans l'ancien palais du gouverneur, il présente les tenues de "
          "cérémonie des groupes culturels du pays. Petit, bien agencé, et la meilleure "
          "demi-heure de contexte avant de partir vers l'intérieur.")),
        (("The beach and the lagoon", "La plage et la lagune"),
         ("The ocean side has a strong undertow — swim where the locals swim, and ask. "
          "The lagoon side is calm, and pirogues will take you across for very little.",
          "Côté océan, le courant de retour est fort : baignez-vous là où les habitants "
          "se baignent, et demandez. Côté lagune, l'eau est calme, et les pirogues vous "
          "font traverser pour presque rien.")),
        (("Craft workshops", "Les ateliers d'artisanat"),
         ("Batik, basketwork and woodcarving are made and sold along the main street. "
          "Prices are negotiated, calmly and without hurry — it's part of the exchange.",
          "Batik, vannerie et sculpture sur bois se fabriquent et se vendent le long de "
          "la rue principale. Les prix se négocient, calmement et sans hâte : cela fait "
          "partie de l'échange.")),
    ],
    events=[
        (("The Abissa festival", "Le festival Abissa"),
         ("The great festival of the N'Zima people, held in Grand-Bassam. For a week, "
          "the community settles its accounts publicly through song and dance: grievances "
          "of the past year are aired, mocked and forgiven, and the social slate is wiped "
          "clean. It is a real ritual, not a show put on for visitors — and it is one of "
          "the most striking things you can witness in the country. Dates move with the "
          "traditional calendar; tell us your travel window and we'll check.",
          "La grande fête du peuple N'Zima, à Grand-Bassam. Pendant une semaine, la "
          "communauté règle ses comptes publiquement par le chant et la danse : les "
          "griefs de l'année sont exposés, moqués et pardonnés, et l'ardoise sociale est "
          "effacée. C'est un vrai rituel, pas un spectacle pour visiteurs — et l'une des "
          "choses les plus frappantes à voir dans le pays. Les dates suivent le "
          "calendrier traditionnel ; donnez-nous votre période, nous vérifions.")),
    ],
    facts=[
        (("Getting there", "Y aller"), ("45 min by road from Abidjan", "45 min de route depuis Abidjan")),
        (("Time needed", "Durée"), ("Half a day to a full day", "Une demi-journée à une journée")),
        (("Best season", "Saison"), ("November to April", "De novembre à avril")),
        (("Combine with", "À combiner avec"), ("Assinie, or a day in Abidjan", "Assinie, ou une journée à Abidjan")),
    ]))

PLACES.append(dict(
    slug="assinie", cat="beach", name="Assinie",
    img="assets/img/dest/assinie.svg",
    tag=("Coastline · 2 h from Abidjan", "Littoral · 2 h d'Abidjan"),
    lede=("A spit of sand with the lagoon on one side and the Atlantic on the other — "
          "the country's weekend destination.",
          "Une langue de sable, la lagune d'un côté et l'Atlantique de l'autre — la "
          "destination week-end du pays."),
    intro=(
        "Assinie sits on a narrow strip between the Aby lagoon and the ocean, about two "
        "hours east of Abidjan near the Ghanaian border. The geography is the whole "
        "point: still, warm water on one side for kayaks, pirogues and swimming; open "
        "Atlantic on the other for the swell and the wind. You cross from one to the "
        "other in a few minutes on foot.\n\n"
        "It is the most developed beach area in the country, which cuts both ways. There "
        "are proper lodges, restaurants and boat operators, so the logistics are easy. "
        "But it fills up at weekends and during holidays, and prices follow. Come "
        "midweek if you can — the same place, half the people.",
        "Assinie occupe une bande étroite entre la lagune Aby et l'océan, à deux heures "
        "à l'est d'Abidjan, près de la frontière ghanéenne. Toute la particularité tient "
        "à cette géographie : d'un côté une eau calme et chaude pour le kayak, la "
        "pirogue et la baignade ; de l'autre, l'Atlantique ouvert, ses rouleaux et son "
        "vent. On passe de l'un à l'autre en quelques minutes à pied.\n\n"
        "C'est la zone balnéaire la plus équipée du pays, ce qui a deux faces. Les "
        "lodges, restaurants et loueurs de bateaux existent vraiment, donc la logistique "
        "est simple. Mais le lieu se remplit le week-end et pendant les vacances, et les "
        "prix suivent. Venez en semaine si vous le pouvez : le même endroit, moitié "
        "moins de monde."),
    see=[
        (("The lagoon", "La lagune"),
         ("Aby is vast and calm. Pirogue trips, kayaking and paddleboarding all work "
          "here, and a boat outing at the end of the afternoon, when the light drops, is "
          "the thing people remember.",
          "La lagune Aby est vaste et calme. Sorties en pirogue, kayak et paddle y "
          "fonctionnent, et une balade en bateau en fin d'après-midi, quand la lumière "
          "tombe, reste le souvenir le plus fort.")),
        (("The Ehotilé Islands", "Les îles Ehotilé"),
         ("A national park of islands in the lagoon, reached by pirogue: mangroves, water "
          "birds, and islets the surrounding communities hold sacred. Half a day, and "
          "worth it.",
          "Un parc national d'îles dans la lagune, accessible en pirogue : mangroves, "
          "oiseaux d'eau, et des îlots tenus pour sacrés par les populations riveraines. "
          "Une demi-journée, et elle vaut le détour.")),
        (("Assouindé and the fishing villages", "Assouindé et les villages de pêcheurs"),
         ("Just along the coast, life carries on outside the resorts: nets brought in at "
          "dawn, smoked fish, and a rhythm that has nothing to do with the weekend crowd.",
          "Un peu plus loin sur la côte, la vie continue hors des complexes : filets "
          "relevés à l'aube, poisson fumé, et un rythme qui n'a rien à voir avec "
          "l'affluence du week-end.")),
        (("Watersports", "Les sports nautiques"),
         ("The ocean side gets a consistent swell — surfing, bodyboarding and kitesurfing "
          "all happen here. Equipment can be rented locally, but check condition before "
          "you pay.",
          "Côté océan, la houle est régulière : surf, bodyboard et kitesurf s'y "
          "pratiquent. Le matériel se loue sur place, mais vérifiez son état avant de "
          "payer.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("2 h by road from Abidjan", "2 h de route depuis Abidjan")),
        (("Time needed", "Durée"), ("Two nights minimum", "Deux nuits minimum")),
        (("Best season", "Saison"), ("November to April", "De novembre à avril")),
        (("Watch out for", "À savoir"), ("Crowded and pricier at weekends", "Affluence et prix plus élevés le week-end")),
    ]))

PLACES.append(dict(
    slug="sassandra", cat="beach", name="Sassandra",
    img="assets/img/dest/sassandra.svg",
    tag=("Coastline · 4 h west", "Littoral · 4 h à l'ouest"),
    lede=("A working fishing port at a river mouth, with sheltered coves on either side. "
          "The quiet option.",
          "Un port de pêche en activité à l'embouchure d'un fleuve, avec des criques "
          "abritées de part et d'autre. L'option tranquille."),
    intro=(
        "Sassandra was a trading post before it was anything else — French, then briefly "
        "English, then French again — and a few colonial buildings still stand on the "
        "heights above the river. Today it is first and foremost a fishing port, and the "
        "day is organised around the boats: out before dawn, back in the morning, with "
        "the catch sold on the quay.\n\n"
        "What brings travellers here are the coves either side of the town, sheltered by "
        "headlands and far quieter than anything closer to Abidjan. There are fewer "
        "facilities than at Assinie, and getting here takes most of a day's drive. That "
        "filters the crowd, which is exactly why the people who go tend to talk about it "
        "afterwards.",
        "Sassandra fut d'abord un comptoir — français, puis brièvement anglais, puis "
        "français de nouveau — et quelques bâtiments coloniaux tiennent encore sur les "
        "hauteurs au-dessus du fleuve. C'est aujourd'hui avant tout un port de pêche, et "
        "la journée s'organise autour des pirogues : sortie avant l'aube, retour en "
        "matinée, et la prise vendue sur le quai.\n\n"
        "Ce qui attire les voyageurs, ce sont les criques de part et d'autre de la "
        "ville, abritées par des pointes rocheuses et bien plus calmes que tout ce qu'on "
        "trouve près d'Abidjan. Il y a moins d'équipements qu'à Assinie, et il faut "
        "presque une journée de route. Cela filtre le monde, et c'est exactement pour "
        "cela que ceux qui y vont en reparlent."),
    see=[
        (("The coves", "Les criques"),
         ("Poly beach and the small bays around the town are the reason to come: rock "
          "headlands, calm water between them, and often no one else.",
          "La plage de Poly et les petites baies autour de la ville sont la raison de "
          "venir : pointes rocheuses, eau calme entre elles, et souvent personne "
          "d'autre.")),
        (("The port at dawn", "Le port à l'aube"),
         ("Worth setting an alarm for. The pirogues come in, the fish is sorted and sold "
          "on the spot, and the whole town passes through in an hour.",
          "Cela vaut la peine de mettre un réveil. Les pirogues rentrent, le poisson est "
          "trié et vendu sur place, et toute la ville y passe en une heure.")),
        (("The Sassandra river", "Le fleuve Sassandra"),
         ("Boat trips upstream take you into a different landscape entirely — mangrove, "
          "birds, and villages only reachable by water.",
          "Les remontées en bateau vous emmènent dans un tout autre paysage — mangrove, "
          "oiseaux, et des villages qu'on n'atteint que par l'eau.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("4 h by road from Abidjan", "4 h de route depuis Abidjan")),
        (("Time needed", "Durée"), ("At least one night", "Une nuit minimum")),
        (("Best season", "Saison"), ("November to April", "De novembre à avril")),
        (("Combine with", "À combiner avec"), ("San Pedro and Taï National Park", "San Pedro et le parc de Taï")),
    ]))

PLACES.append(dict(
    slug="san-pedro", cat="beach", name="San Pedro",
    img="assets/img/dest/san-pedro.svg",
    tag=("Coastline · 6 h west", "Littoral · 6 h à l'ouest"),
    lede=("The country's second port, and the way into the wildest stretch of the "
          "western coast.",
          "Deuxième port du pays, et la porte d'entrée de la côte ouest la plus sauvage."),
    intro=(
        "San Pedro is a working city: the second port of Côte d'Ivoire, built in the "
        "1960s to ship cocoa, timber and coffee out of the south-west. It is not a "
        "postcard, and that is worth knowing before you arrive. What it offers is access "
        "— to long, empty beaches running west towards the Liberian border, and to Taï "
        "National Park a few hours inland.\n\n"
        "There is a domestic airport, which changes the calculation completely: a flight "
        "from Abidjan turns a six-hour drive into an hour. For travellers combining "
        "coast and rainforest, San Pedro is the logical base.",
        "San Pedro est une ville de travail : deuxième port de Côte d'Ivoire, construit "
        "dans les années 1960 pour exporter le cacao, le bois et le café du sud-ouest. "
        "Ce n'est pas une carte postale, et mieux vaut le savoir avant d'arriver. Ce "
        "qu'elle offre, c'est un accès — à de longues plages désertes qui filent vers la "
        "frontière libérienne, et au parc national de Taï à quelques heures de route.\n\n"
        "Un aéroport domestique change complètement le calcul : un vol depuis Abidjan "
        "transforme six heures de route en une heure. Pour qui veut combiner côte et "
        "forêt tropicale, San Pedro est la base logique."),
    see=[
        (("The western beaches", "Les plages de l'ouest"),
         ("Grand-Béréby, about an hour further west, has the bays people come for: rock "
          "points, clear water and almost no development.",
          "Grand-Béréby, à une heure plus à l'ouest, offre les baies pour lesquelles on "
          "vient : pointes rocheuses, eau claire et presque aucun aménagement.")),
        (("The port", "Le port"),
         ("One of the busiest in West Africa, and a reminder that this coast is a working "
          "economy before it is a holiday destination.",
          "L'un des plus actifs d'Afrique de l'Ouest, et un rappel que cette côte est "
          "d'abord une économie avant d'être une destination de vacances.")),
        (("Access to Taï", "L'accès à Taï"),
         ("The national park is a few hours inland. Permits and guides are arranged in "
          "advance, and San Pedro is where most itineraries stage from.",
          "Le parc national est à quelques heures de route. Autorisations et guides se "
          "préparent à l'avance, et San Pedro sert de base à la plupart des "
          "itinéraires.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("6 h by road, or 1 h by domestic flight", "6 h de route, ou 1 h en vol intérieur")),
        (("Time needed", "Durée"), ("Two to three nights", "Deux à trois nuits")),
        (("Best season", "Saison"), ("November to April", "De novembre à avril")),
        (("Combine with", "À combiner avec"), ("Taï National Park", "Le parc national de Taï")),
    ]))

PLACES.append(dict(
    slug="jacqueville", cat="beach", name="Jacqueville",
    img="assets/img/dest/jacqueville.svg",
    tag=("Coastline · 1 h 30 from Abidjan", "Littoral · 1 h 30 d'Abidjan"),
    lede=("An island joined to the mainland by a bridge, between the Ébrié lagoon and "
          "the ocean.",
          "Une île reliée au continent par un pont, entre lagune Ébrié et océan."),
    intro=(
        "Jacqueville is on a long island west of Abidjan, closed off by the Ébrié lagoon "
        "on one side and the Atlantic on the other. Until 2015 you reached it by ferry; "
        "a bridge now makes it an easy ninety minutes from the city, which has opened it "
        "up without yet crowding it.\n\n"
        "The appeal is straightforward: coconut groves, a strip of sand that runs for "
        "kilometres, and Alladian fishing villages where the day is still organised "
        "around the nets. It works as a day trip, and it works better as an overnight — "
        "the beach empties completely once the Abidjan cars leave.",
        "Jacqueville occupe une longue île à l'ouest d'Abidjan, fermée par la lagune "
        "Ébrié d'un côté et l'Atlantique de l'autre. Jusqu'en 2015, on y accédait par "
        "bac ; un pont la met désormais à une heure et demie de la ville, ce qui l'a "
        "ouverte sans encore l'encombrer.\n\n"
        "L'attrait est simple : cocoteraies, une bande de sable qui court sur des "
        "kilomètres, et des villages de pêcheurs alladians où la journée s'organise "
        "encore autour des filets. Cela fonctionne à la journée, et mieux encore sur une "
        "nuit — la plage se vide entièrement quand les voitures d'Abidjan repartent."),
    see=[
        (("The beach", "La plage"),
         ("Long, open and largely undeveloped. The ocean has current here too: ask "
          "locally before swimming.",
          "Longue, ouverte et peu aménagée. L'océan a du courant ici aussi : demandez sur "
          "place avant de vous baigner.")),
        (("The fishing villages", "Les villages de pêcheurs"),
         ("Alladian communities work this coast. Nets are hauled in collectively in the "
          "morning, and visitors who ask politely are usually welcome to watch.",
          "Les communautés alladianes travaillent cette côte. Les filets sont halés "
          "collectivement le matin, et les visiteurs qui demandent poliment sont "
          "généralement bienvenus.")),
        (("The coconut groves", "Les cocoteraies"),
         ("Plantations run most of the island's length, and the road through them is one "
          "of the more pleasant drives near Abidjan.",
          "Les plantations couvrent presque toute la longueur de l'île, et la route qui "
          "les traverse est l'une des plus agréables autour d'Abidjan.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("1 h 30 by road, over the bridge", "1 h 30 de route, par le pont")),
        (("Time needed", "Durée"), ("A day, or one night", "Une journée, ou une nuit")),
        (("Best season", "Saison"), ("November to April", "De novembre à avril")),
        (("Good for", "Idéal pour"), ("A first escape from Abidjan", "Une première échappée depuis Abidjan")),
    ]))

PLACES.append(dict(
    slug="grand-lahou", cat="beach", name="Grand-Lahou",
    img="assets/img/dest/grand-lahou.svg",
    tag=("Coastline · 3 h from Abidjan", "Littoral · 3 h d'Abidjan"),
    lede=("A town the ocean is slowly taking back, next to the mangroves of Azagny "
          "National Park.",
          "Une ville que l'océan reprend peu à peu, à côté des mangroves du parc "
          "national d'Azagny."),
    intro=(
        "Old Grand-Lahou is one of the strangest sites on the coast. Built on a sand spit "
        "at the mouth of the Bandama river, the colonial town has been losing ground to "
        "the sea for decades — buildings collapse, the shoreline advances, and the "
        "population has progressively moved to a new settlement inland. What remains is a "
        "half-abandoned town being dismantled by the ocean, in slow motion.\n\n"
        "It is a sobering visit rather than a pretty one, and it is also one of the "
        "clearest places in the country to see coastal erosion at work. Next door, Azagny "
        "National Park protects lagoons, mangrove and a forest elephant population, and "
        "the two together make a strong day.",
        "Le vieux Grand-Lahou est l'un des sites les plus étranges de la côte. Bâtie sur "
        "un cordon de sable à l'embouchure du Bandama, la ville coloniale perd du terrain "
        "face à la mer depuis des décennies — les bâtiments s'effondrent, le trait de "
        "côte avance, et la population s'est progressivement déplacée vers un nouveau "
        "site à l'intérieur. Il reste une ville à demi abandonnée, démontée par l'océan "
        "au ralenti.\n\n"
        "C'est une visite qui donne à réfléchir plus qu'elle n'est jolie, et c'est aussi "
        "l'un des endroits du pays où l'érosion côtière se lit le plus clairement. Juste "
        "à côté, le parc national d'Azagny protège lagunes, mangrove et une population "
        "d'éléphants de forêt : les deux ensemble font une belle journée."),
    see=[
        (("The old town", "La vieille ville"),
         ("Colonial buildings in various stages of collapse, right at the water's edge. "
          "Go with a local guide — they know which structures are safe to approach.",
          "Des bâtiments coloniaux à divers stades d'effondrement, au bord de l'eau. "
          "Allez-y avec un guide local : il sait lesquels on peut approcher.")),
        (("Azagny National Park", "Le parc national d'Azagny"),
         ("Mangrove, lagoon and savanna, visited by boat. Forest elephants live here, "
          "though sightings are never guaranteed — birds and monkeys are far more "
          "reliable.",
          "Mangrove, lagune et savane, qui se visitent en bateau. Des éléphants de forêt "
          "y vivent, mais l'observation n'est jamais garantie — oiseaux et singes le sont "
          "bien davantage.")),
        (("The Bandama mouth", "L'embouchure du Bandama"),
         ("Where the country's main river meets the Atlantic. Pirogues cross constantly, "
          "and the fishing here supports the whole town.",
          "Là où le principal fleuve du pays rejoint l'Atlantique. Les pirogues "
          "traversent en permanence, et la pêche y fait vivre toute la ville.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("3 h by road from Abidjan", "3 h de route depuis Abidjan")),
        (("Time needed", "Durée"), ("A full day, or one night", "Une journée complète, ou une nuit")),
        (("Best season", "Saison"), ("November to April", "De novembre à avril")),
        (("Combine with", "À combiner avec"), ("Azagny National Park", "Le parc national d'Azagny")),
    ]))

# =============================================================== CULTURE

PLACES.append(dict(
    slug="yamoussoukro", cat="culture", name="Yamoussoukro",
    img="assets/img/dest/yamoussoukro.svg",
    tag=("Culture · 3 h from Abidjan", "Culture · 3 h d'Abidjan"),
    lede=("The political capital, and the site of one of the largest churches in the "
          "world.",
          "La capitale politique, et le site de l'une des plus grandes églises du "
          "monde."),
    intro=(
        "Yamoussoukro was Félix Houphouët-Boigny's home village. When he became the "
        "country's first president he transferred the capital here in 1983 and built at "
        "a scale the town has never grown into: eight-lane boulevards that carry little "
        "traffic, vast institutional buildings, and the Basilica of Our Lady of Peace.\n\n"
        "The result is disconcerting and worth seeing precisely for that. It is a "
        "monumental capital in a town of modest size, and it says a great deal about a "
        "particular moment in the country's history. Three hours from Abidjan on the "
        "motorway, it works as a long day trip or as a stop on the way north.",
        "Yamoussoukro était le village natal de Félix Houphouët-Boigny. Devenu premier "
        "président du pays, il y transféra la capitale en 1983 et y bâtit à une échelle "
        "que la ville n'a jamais atteinte : des boulevards à huit voies presque déserts, "
        "de vastes bâtiments institutionnels, et la basilique Notre-Dame de la Paix.\n\n"
        "Le résultat est déroutant, et c'est précisément pour cela qu'il faut le voir. "
        "Une capitale monumentale dans une ville de taille modeste, qui en dit long sur "
        "un moment particulier de l'histoire du pays. À trois heures d'Abidjan par "
        "l'autoroute, cela fait une longue journée ou une étape en montant vers le nord."),
    see=[
        (("The Basilica of Our Lady of Peace", "La basilique Notre-Dame de la Paix"),
         ("Consecrated by John Paul II in 1990 and among the largest churches in the "
          "world, with a dome inspired by Saint Peter's in Rome and stained glass "
          "covering thousands of square metres. Whatever you make of the project, the "
          "building itself is extraordinary.",
          "Consacrée par Jean-Paul II en 1990 et parmi les plus grandes églises du "
          "monde, avec une coupole inspirée de Saint-Pierre de Rome et des milliers de "
          "mètres carrés de vitraux. Quoi qu'on pense du projet, l'édifice lui-même est "
          "hors norme.")),
        (("The presidential palace and the crocodile lake", "Le palais présidentiel et le lac aux caïmans"),
         ("You don't go inside, but the lake around it holds crocodiles that have become "
          "part of the town's folklore. Feeding time draws a small crowd.",
          "On n'entre pas, mais le lac qui l'entoure abrite des caïmans devenus un "
          "élément du folklore local. Le nourrissage attire toujours un petit public.")),
        (("The Houphouët-Boigny Foundation", "La fondation Houphouët-Boigny"),
         ("A conference centre and institution dedicated to peace research, and another "
          "piece of the same monumental ensemble.",
          "Centre de conférences et institution consacrée à la recherche sur la paix, "
          "autre pièce du même ensemble monumental.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("3 h by motorway from Abidjan", "3 h d'autoroute depuis Abidjan")),
        (("Time needed", "Durée"), ("A long day, or a stop en route", "Une longue journée, ou une étape")),
        (("Dress code", "Tenue"), ("Cover shoulders and knees at the basilica", "Épaules et genoux couverts à la basilique")),
        (("Combine with", "À combiner avec"), ("Bouaké, or the road north", "Bouaké, ou la route du nord")),
    ]))

PLACES.append(dict(
    slug="korhogo", cat="culture", name="Korhogo",
    img="assets/img/dest/korhogo.svg",
    tag=("Culture · Northern Côte d'Ivoire", "Culture · Nord du pays"),
    lede=("Capital of the north, heart of Senufo country, and home of the painted cloth "
          "that became an emblem of the country.",
          "Capitale du nord, cœur du pays sénoufo, et berceau des toiles peintes "
          "devenues emblème national."),
    intro=(
        "Korhogo is the main city of the north and the centre of Senufo culture. The "
        "landscape changes completely on the way up: forest gives way to savanna, the "
        "air dries out, and the architecture shifts to mud and thatch. The rhythm "
        "changes too.\n\n"
        "The region is known above all for its craftsmanship, organised village by "
        "village — one for weaving, one for carving, one for blacksmithing. The most "
        "famous is Fakaha, about forty kilometres away, where the Korhogo cloth is "
        "painted: cotton strips woven locally, then drawn on with fermented mud and "
        "plant dyes, in figures of animals, dancers and masks. What you buy at the "
        "workshop and what you find on a tourist stall are not the same object.",
        "Korhogo est la principale ville du nord et le centre de la culture sénoufo. Le "
        "paysage change complètement en montant : la forêt cède à la savane, l'air "
        "s'assèche, et l'architecture passe à la terre et au chaume. Le rythme change "
        "aussi.\n\n"
        "La région est surtout connue pour son artisanat, organisé village par village — "
        "l'un pour le tissage, l'autre pour la sculpture, un autre pour la forge. Le plus "
        "réputé est Fakaha, à une quarantaine de kilomètres, où se peignent les toiles "
        "de Korhogo : des bandes de coton tissées sur place, puis dessinées à la boue "
        "fermentée et aux teintures végétales, en figures d'animaux, de danseurs et de "
        "masques. Ce qu'on achète à l'atelier et ce qu'on trouve sur un étal touristique "
        "ne sont pas le même objet."),
    see=[
        (("Fakaha and the painted cloth", "Fakaha et les toiles peintes"),
         ("The village where the cloth is made. You see the whole chain — weaving, "
          "preparing the dyes, drawing — and buy directly from the person who made it.",
          "Le village où se fait la toile. On y voit toute la chaîne — tissage, "
          "préparation des teintures, dessin — et on achète directement à celui qui l'a "
          "faite.")),
        (("The craft villages", "Les villages d'artisans"),
         ("Around Korhogo, work is specialised by village: blacksmiths, carvers, "
          "weavers, potters. A day spent moving between them is worth more than any "
          "museum.",
          "Autour de Korhogo, le travail est spécialisé par village : forgerons, "
          "sculpteurs, tisserands, potiers. Une journée à circuler entre eux vaut mieux "
          "que n'importe quel musée.")),
        (("Mount Korhogo", "Le mont Korhogo"),
         ("The hill above the town gives the view over the savanna and the surrounding "
          "villages — best at the end of the day.",
          "La colline au-dessus de la ville donne la vue sur la savane et les villages "
          "alentour — surtout en fin de journée.")),
        (("The Senufo sacred wood", "Le bois sacré sénoufo"),
         ("Initiation groves surround many villages. They are not visitor sites: some "
          "can be approached with permission, most cannot, and your guide will tell you "
          "which is which.",
          "Des bois d'initiation entourent de nombreux villages. Ce ne sont pas des "
          "sites de visite : certains s'approchent avec autorisation, la plupart non, et "
          "votre guide vous dira lesquels.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("Road from Abidjan, or domestic flight", "Route depuis Abidjan, ou vol intérieur")),
        (("Time needed", "Durée"), ("Two to three days", "Deux à trois jours")),
        (("Best season", "Saison"), ("November to February — the north is hot", "De novembre à février — le nord est chaud")),
        (("Buy at", "Acheter"), ("The workshops, not the roadside stalls", "Aux ateliers, pas sur les étals de bord de route")),
    ]))

PLACES.append(dict(
    slug="man", cat="culture", name="Man",
    img="assets/img/dest/man.svg",
    tag=("Culture & nature · 8 h from Abidjan", "Culture & nature · 8 h d'Abidjan"),
    lede=("The city of eighteen mountains: mask country, waterfalls and liana bridges.",
          "La cité des dix-huit montagnes : pays des masques, cascades et ponts de "
          "lianes."),
    intro=(
        "Man sits in the western highlands, ringed by the peaks that give it its "
        "nickname. It is the one place in Côte d'Ivoire where culture and landscape are "
        "impossible to separate: this is Dan and Wè country, where masks remain part of "
        "village life, and it is also the most dramatic terrain in the country.\n\n"
        "It is a long way — eight hours by road from Abidjan, or a domestic flight — and "
        "that distance is the price of admission. People who make the trip generally "
        "stay three or four days, because everything worth seeing is spread across the "
        "valleys and you spend a good part of each day travelling between them.",
        "Man se trouve dans les montagnes de l'Ouest, cernée par les sommets qui lui "
        "donnent son surnom. C'est le seul endroit de Côte d'Ivoire où culture et "
        "paysage sont indissociables : c'est le pays dan et wè, où les masques font "
        "toujours partie de la vie villageoise, et c'est aussi le relief le plus "
        "spectaculaire du pays.\n\n"
        "C'est loin — huit heures de route depuis Abidjan, ou un vol intérieur — et cette "
        "distance est le prix d'entrée. Ceux qui font le voyage restent en général trois "
        "ou quatre jours, parce que tout ce qui mérite d'être vu est dispersé dans les "
        "vallées et qu'une bonne partie de chaque journée se passe sur la route."),
    see=[
        (("The masks", "Les masques"),
         ("Dan and Wè masks are not decoration: they appear at funerals, judgements and "
          "initiations, and each has a role. Visits are arranged with the families who "
          "hold them, with permission asked in advance. We never promise an appearance "
          "on a fixed date — that is not how it works.",
          "Les masques dan et wè ne sont pas des décorations : ils sortent lors de "
          "funérailles, de jugements et d'initiations, et chacun a une fonction. Les "
          "visites s'organisent avec les familles qui les détiennent, autorisation "
          "demandée en amont. Nous ne promettons jamais une sortie à date fixe — ce n'est "
          "pas ainsi que cela fonctionne.")),
        (("Stilt dancing", "La danse d'échasses"),
         ("The Dan stilt dancers perform on poles several metres high, in full costume. "
          "It is genuinely astonishing, and it is also a ritual form, not street "
          "entertainment.",
          "Les danseurs dan évoluent sur des échasses de plusieurs mètres, en costume "
          "complet. C'est réellement stupéfiant, et c'est aussi une forme rituelle, pas "
          "un spectacle de rue.")),
        (("The liana bridges", "Les ponts de lianes"),
         ("Woven from living vines across the rivers, maintained by the villages that "
          "use them. The best known is at Lieupleu. Crossing one is a short, memorable "
          "experience.",
          "Tressés en lianes vivantes au-dessus des rivières, entretenus par les "
          "villages qui les utilisent. Le plus connu est celui de Lieupleu. La traversée "
          "est brève et marquante.")),
        (("Mount Tonkoui and the waterfalls", "Le mont Tonkoui et les cascades"),
         ("Tonkoui is among the highest points in the country, with views across to "
          "Guinea on a clear morning. The Man waterfall, in forest just outside town, is "
          "an easy walk.",
          "Le Tonkoui est l'un des points les plus élevés du pays, avec vue jusqu'en "
          "Guinée par temps clair. La cascade de Man, en forêt aux portes de la ville, "
          "s'atteint facilement à pied.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("8 h by road, or a domestic flight", "8 h de route, ou un vol intérieur")),
        (("Time needed", "Durée"), ("Three to four days", "Trois à quatre jours")),
        (("Best season", "Saison"), ("November to April", "De novembre à avril")),
        (("Etiquette", "Usages"), ("Always ask before photographing", "Toujours demander avant de photographier")),
    ]))

PLACES.append(dict(
    slug="abidjan", cat="culture", name="Abidjan",
    img="assets/img/dest/abidjan.svg",
    tag=("Culture · Your starting point", "Culture · Point de départ"),
    lede=("The economic capital and the point of arrival — a lagoon city of five million "
          "people.",
          "La capitale économique et le point d'arrivée — une ville-lagune de cinq "
          "millions d'habitants."),
    intro=(
        "Abidjan is built around the Ébrié lagoon, and the water shapes everything: the "
        "districts are separated by it, joined by bridges, and the boat is still a "
        "practical way to cross. The Plateau, the business district, has the towers and "
        "the cathedral; Cocody is residential and holds the embassies and the university; "
        "Treichville and Adjamé have the markets; Marcory and Zone 4 have the "
        "restaurants.\n\n"
        "Most travellers pass through without stopping, and that is a mistake. A "
        "well-planned day here — a market, the museum, a craft village, an evening in a "
        "maquis — teaches you more about the country than a week of driving. It also "
        "makes everything that follows more legible.",
        "Abidjan est construite autour de la lagune Ébrié, et l'eau organise tout : les "
        "quartiers en sont séparés, reliés par des ponts, et le bateau reste un moyen "
        "pratique de traverser. Le Plateau, quartier d'affaires, a les tours et la "
        "cathédrale ; Cocody est résidentiel et abrite les ambassades et l'université ; "
        "Treichville et Adjamé ont les marchés ; Marcory et la Zone 4, les restaurants.\n\n"
        "La plupart des voyageurs ne font que passer, et c'est une erreur. Une journée "
        "bien construite ici — un marché, le musée, un village artisanal, une soirée en "
        "maquis — en apprend plus sur le pays qu'une semaine de route. Et elle rend tout "
        "le reste plus lisible."),
    see=[
        (("The Museum of Civilisations", "Le musée des civilisations"),
         ("The national collection of masks, statuary and everyday objects from across "
          "the country's cultural groups. Go on your first day: everything you see "
          "afterwards makes more sense.",
          "La collection nationale de masques, statuaire et objets du quotidien des "
          "différents groupes culturels du pays. À faire le premier jour : tout ce qu'on "
          "voit ensuite prend du sens.")),
        (("Saint Paul's Cathedral", "La cathédrale Saint-Paul"),
         ("A striking piece of modern architecture on the Plateau, designed by Aldo "
          "Spirito, with the facade shaped as a figure drawing the roof behind it.",
          "Une architecture moderne saisissante au Plateau, conçue par Aldo Spirito, "
          "dont la façade figure un personnage tirant le toit derrière lui.")),
        (("The Cocody artisan village", "Le village artisanal de Cocody"),
         ("Workshops and stalls in one place — wood, bronze, cloth, leather. Prices are "
          "negotiated; take your time and buy on the second pass.",
          "Ateliers et étals réunis — bois, bronze, tissu, cuir. Les prix se négocient : "
          "prenez votre temps et achetez au second passage.")),
        (("The markets", "Les marchés"),
         ("Treichville for food and fabric, Adjamé for scale and noise. Both are "
          "overwhelming and both are the real city. Go with a guide the first time.",
          "Treichville pour la nourriture et les tissus, Adjamé pour l'ampleur et le "
          "bruit. Les deux sont écrasants, et les deux sont la vraie ville. Avec un guide "
          "la première fois.")),
        (("Banco National Park", "Le parc national du Banco"),
         ("Rainforest inside the city limits, with marked trails and the fanico — the "
          "open-air laundry where hundreds of men wash clothes in the river.",
          "De la forêt tropicale dans les limites de la ville, avec des sentiers balisés "
          "et le fanico, la laverie à ciel ouvert où des centaines d'hommes lavent le "
          "linge dans la rivière.")),
    ],
    events=[
        (("FEMUA", "Le FEMUA"),
         ("The Festival des Musiques Urbaines d'Anoumabo, founded by the group Magic "
          "System in their home neighbourhood. It has grown into one of West Africa's "
          "major music events, with free concerts across the city alongside the ticketed "
          "main stage.",
          "Le Festival des Musiques Urbaines d'Anoumabo, fondé par le groupe Magic System "
          "dans son quartier d'origine. Il est devenu l'un des grands rendez-vous "
          "musicaux d'Afrique de l'Ouest, avec des concerts gratuits dans la ville en "
          "plus de la scène principale payante.")),
    ],
    facts=[
        (("Getting there", "Y aller"), ("Your point of arrival — ABJ airport", "Votre point d'arrivée — aéroport ABJ")),
        (("Time needed", "Durée"), ("Two days minimum", "Deux jours minimum")),
        (("Getting around", "Se déplacer"), ("Ride-hailing apps, or a driver", "Applications VTC, ou un chauffeur")),
        (("Evenings", "Le soir"), ("Zone 4 and Marcory for maquis", "Zone 4 et Marcory pour les maquis")),
    ]))

PLACES.append(dict(
    slug="bouake", cat="culture", name="Bouaké",
    img="assets/img/dest/bouake.svg",
    tag=("Culture · Central Côte d'Ivoire", "Culture · Centre du pays"),
    lede=("The second city, the Baoulé capital, and the site of the country's biggest "
          "carnival.",
          "Deuxième ville du pays, capitale baoulé, et théâtre du plus grand carnaval "
          "national."),
    intro=(
        "Bouaké sits at the centre of the country, at the meeting point between the "
        "forest of the south and the savanna of the north. It is the second largest city "
        "and the heart of Baoulé country, and its market is one of the biggest in West "
        "Africa — the place where goods from both halves of the country change hands.\n\n"
        "The city carries the marks of the years of political crisis, during which it was "
        "the headquarters of the northern forces. That history is recent and still "
        "visible, and it is part of understanding the place rather than a reason to avoid "
        "it. Bouaké makes a natural stop on the way north.",
        "Bouaké se trouve au centre du pays, à la jonction entre la forêt du sud et la "
        "savane du nord. C'est la deuxième ville et le cœur du pays baoulé, et son marché "
        "est l'un des plus grands d'Afrique de l'Ouest — le lieu où les marchandises des "
        "deux moitiés du pays changent de mains.\n\n"
        "La ville porte les traces des années de crise politique, pendant lesquelles elle "
        "fut le siège des forces du nord. Cette histoire est récente et encore visible : "
        "elle fait partie de la compréhension du lieu plutôt qu'une raison de l'éviter. "
        "Bouaké est une étape naturelle en montant vers le nord."),
    see=[
        (("The grand market", "Le grand marché"),
         ("Vast, and organised by trade rather than by aisle. Fabric, food, hardware, "
          "medicine — it takes hours and it is the best introduction to the city.",
          "Immense, et organisé par métier plutôt que par allée. Tissu, alimentation, "
          "quincaillerie, pharmacopée — il faut des heures, et c'est la meilleure "
          "introduction à la ville.")),
        (("Katiola and the Mangoro potters", "Katiola et les potières mangoro"),
         ("An hour north, the women of the Mangoro caste make pottery by hand without a "
          "wheel, a skill passed down between women for generations. You watch the whole "
          "process and buy at source.",
          "À une heure au nord, les femmes de la caste mangoro façonnent la poterie à la "
          "main, sans tour, un savoir-faire transmis entre femmes depuis des "
          "générations. On assiste à tout le processus et on achète à la source.")),
        (("Baoulé weaving", "Le tissage baoulé"),
         ("The region's woven cloth is worked in narrow strips then sewn together — a "
          "different tradition from the painted cloth of the north.",
          "Les tissus de la région sont travaillés en bandes étroites puis assemblés — "
          "une tradition différente de la toile peinte du nord.")),
    ],
    events=[
        (("The Bouaké carnival", "Le carnaval de Bouaké"),
         ("A large street carnival with parades, masks and music that draws groups from "
          "across the country and from neighbouring states. Dates vary; ask us and we "
          "will check against your travel window.",
          "Un grand carnaval de rue avec défilés, masques et musique, qui attire des "
          "troupes de tout le pays et des États voisins. Les dates varient ; "
          "demandez-nous, nous vérifions selon votre période.")),
    ],
    facts=[
        (("Getting there", "Y aller"), ("About 4 h by road from Abidjan", "Environ 4 h de route depuis Abidjan")),
        (("Time needed", "Durée"), ("One to two days", "Un à deux jours")),
        (("Combine with", "À combiner avec"), ("Yamoussoukro, or the road to Korhogo", "Yamoussoukro, ou la route de Korhogo")),
        (("Don't miss", "À ne pas manquer"), ("Katiola pottery, one hour north", "Les poteries de Katiola, à une heure au nord")),
    ]))

PLACES.append(dict(
    slug="tiegba", cat="culture", name="Tiégba",
    img="assets/img/dest/tiegba.svg",
    tag=("Culture · 2 h from Abidjan", "Culture · 2 h d'Abidjan"),
    lede=("A village built on stilts above the lagoon, reached only by pirogue.",
          "Un village sur pilotis au-dessus de la lagune, qu'on n'atteint qu'en "
          "pirogue."),
    intro=(
        "Tiégba is a lake village on the Ébrié lagoon, west of Abidjan. Part of it stands "
        "on the shore, part on stilts over the water, joined by walkways. The community "
        "settled here generations ago, and the reason is the same today as it was then: "
        "the lagoon is the field, the road and the market all at once.\n\n"
        "The visit is short — half a day, including the pirogue crossing — but it "
        "reframes things. You see how a village organises itself around water rather than "
        "land, and the fishing techniques, the house-building and the movement of "
        "children between them all follow from that.",
        "Tiégba est un village lacustre sur la lagune Ébrié, à l'ouest d'Abidjan. Une "
        "partie tient sur la berge, une autre sur pilotis au-dessus de l'eau, reliée par "
        "des passerelles. La communauté s'y est installée il y a des générations, et la "
        "raison est la même aujourd'hui qu'alors : la lagune est à la fois le champ, la "
        "route et le marché.\n\n"
        "La visite est courte — une demi-journée, traversée en pirogue comprise — mais "
        "elle change la perspective. On voit comment un village s'organise autour de "
        "l'eau plutôt que de la terre, et les techniques de pêche, la construction des "
        "maisons et les déplacements des enfants en découlent tous."),
    see=[
        (("The stilt village", "Le village sur pilotis"),
         ("Houses and walkways built out over the lagoon. People live here year-round; "
          "it is a community, not a site, so the usual courtesies apply.",
          "Maisons et passerelles construites au-dessus de la lagune. On y vit toute "
          "l'année : c'est une communauté, pas un site, et les usages habituels "
          "s'appliquent.")),
        (("The pirogue crossing", "La traversée en pirogue"),
         ("The only way in. Twenty minutes across the water, and the approach is half the "
          "experience.",
          "Le seul accès. Vingt minutes sur l'eau, et l'approche fait la moitié de "
          "l'expérience.")),
        (("Lagoon fishing", "La pêche en lagune"),
         ("Nets, traps and lines, worked from small pirogues. Fishermen will explain the "
          "techniques if you ask, and it is genuinely interesting.",
          "Filets, nasses et lignes, travaillés depuis de petites pirogues. Les pêcheurs "
          "expliquent volontiers leurs techniques si on demande, et c'est réellement "
          "intéressant.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("2 h by road, then pirogue", "2 h de route, puis pirogue")),
        (("Time needed", "Durée"), ("Half a day", "Une demi-journée")),
        (("Etiquette", "Usages"), ("Ask before photographing people or homes", "Demander avant de photographier les gens ou les maisons")),
        (("Combine with", "À combiner avec"), ("Grand-Lahou or Jacqueville", "Grand-Lahou ou Jacqueville")),
    ]))

# ========================================================= NATURE & PARCS

PLACES.append(dict(
    slug="tai", cat="eco", name="Taï National Park",
    img="assets/img/dest/tai.svg",
    tag=("Nature · South-west", "Nature · Sud-ouest"),
    lede=("One of the last primary rainforests in West Africa, and a UNESCO World "
          "Heritage site.",
          "L'une des dernières forêts primaires d'Afrique de l'Ouest, classée au "
          "patrimoine mondial de l'UNESCO."),
    intro=(
        "Taï protects the largest remaining block of primary rainforest in West Africa. "
        "The region was almost entirely cleared for cocoa and timber over the last "
        "century; what survives inside the park boundary gives an idea of what the whole "
        "south-west looked like before. UNESCO listed it in 1982.\n\n"
        "It is best known for its chimpanzees, studied here for decades and observed "
        "using stones to crack nuts — one of the clearest cases of tool use in wild "
        "primates. But the forest itself is the experience: closed canopy, enormous "
        "buttressed trunks, and a soundscape that never stops. Visits are guided, groups "
        "are small, and permits are arranged well in advance.",
        "Taï protège le plus grand massif de forêt primaire subsistant en Afrique de "
        "l'Ouest. La région a été presque entièrement défrichée pour le cacao et le bois "
        "au cours du siècle dernier ; ce qui survit à l'intérieur du parc donne une idée "
        "de ce qu'était tout le sud-ouest auparavant. L'UNESCO l'a classé en 1982.\n\n"
        "Il est surtout connu pour ses chimpanzés, étudiés ici depuis des décennies et "
        "observés cassant des noix avec des pierres — l'un des cas les plus nets d'usage "
        "d'outils chez les primates sauvages. Mais c'est la forêt elle-même qui fait "
        "l'expérience : canopée fermée, troncs immenses à contreforts, et un fond sonore "
        "qui ne s'arrête jamais. Les visites sont guidées, les groupes petits, et les "
        "autorisations se préparent longtemps à l'avance."),
    see=[
        (("The chimpanzees", "Les chimpanzés"),
         ("Habituated groups can sometimes be tracked with researchers and guides. "
          "Sightings are never guaranteed, and anyone who promises you otherwise is "
          "selling something.",
          "Des groupes habitués peuvent parfois être suivis avec chercheurs et guides. "
          "L'observation n'est jamais garantie, et quiconque vous promet le contraire "
          "vend quelque chose.")),
        (("The forest itself", "La forêt elle-même"),
         ("Closed canopy, buttress roots, lianas, and a permanent green half-light. Even "
          "without a single large animal, the walk is the point.",
          "Canopée fermée, racines-contreforts, lianes, et une pénombre verte permanente. "
          "Même sans croiser un seul grand animal, la marche vaut à elle seule le "
          "déplacement.")),
        (("Pygmy hippopotamus", "L'hippopotame nain"),
         ("Taï is one of the last strongholds of this rare, nocturnal and extremely shy "
          "species. Tracks and traces are far more likely than a sighting.",
          "Taï est l'un des derniers bastions de cette espèce rare, nocturne et "
          "extrêmement farouche. Les traces sont bien plus probables que l'observation.")),
        (("Birds", "Les oiseaux"),
         ("Hornbills, turacos, greenbuls — the forest bird list is long and includes "
          "species found nowhere else in the region.",
          "Calaos, touracos, bulbuls — la liste des oiseaux forestiers est longue et "
          "comprend des espèces qu'on ne trouve nulle part ailleurs dans la région.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("Via San Pedro or Guiglo", "Par San Pedro ou Guiglo")),
        (("Book ahead", "Réservation"), ("At least two months — permits take time", "Au moins deux mois — les autorisations sont longues")),
        (("Time needed", "Durée"), ("Two to three days", "Deux à trois jours")),
        (("Bring", "À prévoir"), ("Long sleeves, boots, rain layer", "Manches longues, chaussures montantes, protection pluie")),
    ]))

PLACES.append(dict(
    slug="comoe", cat="eco", name="Comoé National Park",
    img="assets/img/dest/comoe.svg",
    tag=("Nature · North-east", "Nature · Nord-est"),
    lede=("One of the largest protected areas in West Africa: savanna, gallery forest "
          "and a great river.",
          "L'une des plus vastes aires protégées d'Afrique de l'Ouest : savane, "
          "forêts-galeries et un grand fleuve."),
    intro=(
        "Comoé covers an enormous area in the north-east, and its interest lies in the "
        "range of habitats packed into it: wooded savanna, open grassland, and gallery "
        "forest following the Comoé river through the middle of it. That gradient — from "
        "dry savanna species to forest species along the water — is why UNESCO listed it "
        "in 1983.\n\n"
        "The park went through difficult decades and was on the List of World Heritage in "
        "Danger for many years before being removed in 2017 following conservation work. "
        "Wildlife densities are lower than in the great East African parks, and the "
        "experience is closer to a naturalist's outing than to a game drive. Come for the "
        "landscape and the birds, and treat mammal sightings as a bonus.",
        "La Comoé couvre une superficie considérable au nord-est, et son intérêt tient à "
        "la variété des milieux qu'elle réunit : savane boisée, prairies ouvertes, et "
        "forêts-galeries qui suivent le fleuve Comoé en son centre. Ce gradient — des "
        "espèces de savane sèche aux espèces forestières le long de l'eau — a valu son "
        "classement par l'UNESCO en 1983.\n\n"
        "Le parc a traversé des décennies difficiles et est resté de longues années sur "
        "la liste du patrimoine en péril, avant d'en être retiré en 2017 à la suite d'un "
        "travail de conservation. Les densités de faune sont plus faibles que dans les "
        "grands parcs d'Afrique de l'Est, et l'expérience tient plus de la sortie "
        "naturaliste que du safari. Venez pour le paysage et les oiseaux, et considérez "
        "les mammifères comme un bonus."),
    see=[
        (("The Comoé river", "Le fleuve Comoé"),
         ("The park's spine. Hippos, crocodiles and a constant traffic of birds along the "
          "banks, especially early and late.",
          "La colonne vertébrale du parc. Hippopotames, crocodiles et un trafic constant "
          "d'oiseaux le long des berges, surtout tôt et tard.")),
        (("Savanna wildlife", "La faune de savane"),
         ("Kob, bushbuck, warthog, baboon and several monkey species. Elephants and "
          "buffalo are present but rarely seen.",
          "Cobs, guibs, phacochères, babouins et plusieurs espèces de singes. Éléphants "
          "et buffles sont présents mais rarement observés.")),
        (("Birdlife", "L'avifaune"),
         ("This is the real strength of the park — hundreds of species, and the mix of "
          "savanna and forest birds in one place is unusual.",
          "C'est la vraie force du parc — des centaines d'espèces, et le mélange "
          "d'oiseaux de savane et de forêt en un seul lieu est rare.")),
        (("Gallery forest", "Les forêts-galeries"),
         ("Ribbons of dense forest along the watercourses, cutting through open savanna. "
          "Walking from one into the other is a striking transition.",
          "Des rubans de forêt dense le long des cours d'eau, qui tranchent la savane "
          "ouverte. Passer de l'un à l'autre à pied est une transition saisissante.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("Via Bouna or Kong, in the north-east", "Par Bouna ou Kong, au nord-est")),
        (("Best season", "Saison"), ("December to April, when tracks are passable", "De décembre à avril, quand les pistes sont praticables")),
        (("Time needed", "Durée"), ("Three days minimum", "Trois jours minimum")),
        (("Expect", "À prévoir"), ("A naturalist trip, not a big-game safari", "Une sortie naturaliste, pas un safari")),
    ]))

PLACES.append(dict(
    slug="banco", cat="eco", name="Banco National Park",
    img="assets/img/dest/banco.svg",
    tag=("Nature · Inside Abidjan", "Nature · Dans Abidjan"),
    lede=("Thousands of hectares of rainforest inside the city — half a day, no travel "
          "required.",
          "Des milliers d'hectares de forêt tropicale dans la ville — une demi-journée, "
          "sans trajet."),
    intro=(
        "Banco is a genuine rainforest inside a city of five million people, and the "
        "contrast is the whole point. You leave the traffic, drive through a gate, and "
        "within a few minutes you are under closed canopy with monkeys overhead. Very few "
        "capitals have anything comparable.\n\n"
        "It also serves an entirely practical purpose: if your trip is short, or your "
        "first day is jet-lagged, this gives you the forest without the eight-hour drive. "
        "The arboretum and the marked trails make it easy to visit without a full "
        "expedition setup.",
        "Le Banco est une véritable forêt tropicale à l'intérieur d'une ville de cinq "
        "millions d'habitants, et c'est tout l'intérêt du contraste. On quitte la "
        "circulation, on franchit un portail, et en quelques minutes on se trouve sous "
        "canopée fermée avec des singes au-dessus de la tête. Peu de capitales ont "
        "l'équivalent.\n\n"
        "Il rend aussi un service très pratique : si votre séjour est court, ou si votre "
        "premier jour est marqué par le décalage horaire, il vous donne la forêt sans les "
        "huit heures de route. L'arboretum et les sentiers balisés permettent de le "
        "visiter sans logistique lourde."),
    see=[
        (("The trails", "Les sentiers"),
         ("Marked paths through primary and secondary forest, walkable in ordinary shoes. "
          "Monkeys, squirrels and a long list of birds.",
          "Des sentiers balisés à travers forêt primaire et secondaire, praticables en "
          "chaussures ordinaires. Singes, écureuils et une longue liste d'oiseaux.")),
        (("The arboretum", "L'arboretum"),
         ("Labelled specimens of the region's tree species — useful before going to Taï, "
          "where nothing is labelled at all.",
          "Des spécimens étiquetés des essences de la région — utile avant d'aller à Taï, "
          "où plus rien ne l'est.")),
        (("The fanico", "Le fanico"),
         ("At the river's edge, hundreds of men wash clothes by hand in individual "
          "hollows worn into the rock. It is a working laundry, not a display; ask before "
          "you photograph.",
          "Au bord de la rivière, des centaines d'hommes lavent le linge à la main dans "
          "des cuvettes creusées dans la roche. C'est une laverie en activité, pas un "
          "spectacle : demandez avant de photographier.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("20–30 min from central Abidjan", "20 à 30 min du centre d'Abidjan")),
        (("Time needed", "Durée"), ("Half a day", "Une demi-journée")),
        (("Good for", "Idéal pour"), ("A first or last day in the country", "Un premier ou un dernier jour")),
        (("Bring", "À prévoir"), ("Insect repellent and water", "Répulsif et eau")),
    ]))

PLACES.append(dict(
    slug="ehotile", cat="eco", name="Ehotilé Islands",
    img="assets/img/dest/ehotile.svg",
    tag=("Nature · Near Assinie", "Nature · Près d'Assinie"),
    lede=("A national park of lagoon islands: mangrove, water birds, and islets held "
          "sacred.",
          "Un parc national d'îles lagunaires : mangrove, oiseaux d'eau et îlots "
          "sacrés."),
    intro=(
        "The Ehotilé islands sit in the Aby lagoon near Assinie, and are protected as a "
        "national park. They are small — a handful of wooded islands and mangrove "
        "channels — and you reach them by pirogue, which is a large part of the "
        "pleasure.\n\n"
        "The islands also hold a place in the history of the Ehotilé people, who consider "
        "several of them sacred and who buried their kings there. Some can be visited "
        "with a local guide, others are not open at all, and that distinction is "
        "respected without negotiation.",
        "Les îles Ehotilé se trouvent dans la lagune Aby près d'Assinie, et sont "
        "protégées en parc national. Elles sont petites — quelques îles boisées et des "
        "chenaux de mangrove — et l'on y accède en pirogue, ce qui fait une bonne part du "
        "plaisir.\n\n"
        "Ces îles occupent aussi une place dans l'histoire du peuple ehotilé, qui en "
        "considère plusieurs comme sacrées et y a enterré ses rois. Certaines se visitent "
        "avec un guide local, d'autres ne s'ouvrent pas du tout, et cette distinction se "
        "respecte sans négociation."),
    see=[
        (("The mangrove channels", "Les chenaux de mangrove"),
         ("Narrow waterways between the islands, navigated by pirogue. Quiet, shaded, and "
          "full of birds.",
          "D'étroits bras d'eau entre les îles, parcourus en pirogue. Calmes, ombragés et "
          "pleins d'oiseaux.")),
        (("Water birds", "Les oiseaux d'eau"),
         ("Herons, egrets, kingfishers and waders. Early morning is by far the best time.",
          "Hérons, aigrettes, martins-pêcheurs et limicoles. Le petit matin est de loin "
          "le meilleur moment.")),
        (("The sacred islands", "Les îles sacrées"),
         ("Burial sites of the Ehotilé kings. Access is restricted and conditional; your "
          "guide will explain what may and may not be approached.",
          "Sites funéraires des rois ehotilé. L'accès est restreint et conditionnel ; "
          "votre guide vous expliquera ce qui peut ou non être approché.")),
    ],
    events=[],
    facts=[
        (("Getting there", "Y aller"), ("By pirogue from Assinie", "En pirogue depuis Assinie")),
        (("Time needed", "Durée"), ("Half a day", "Une demi-journée")),
        (("Best time", "Meilleur moment"), ("Early morning, for the birds", "Tôt le matin, pour les oiseaux")),
        (("Combine with", "À combiner avec"), ("A stay in Assinie", "Un séjour à Assinie")),
    ]))

PLACES.append(dict(
    slug="nimba", cat="eco", name="Mount Nimba",
    img="assets/img/dest/nimba.svg",
    tag=("Nature · Western border", "Nature · Frontière ouest"),
    lede=("A strict nature reserve on the World Heritage list, shared with Guinea and "
          "Liberia.",
          "Une réserve intégrale classée au patrimoine mondial, partagée avec la Guinée "
          "et le Liberia."),
    intro=(
        "The Nimba range rises at the point where Côte d'Ivoire, Guinea and Liberia meet, "
        "and its isolation has produced an exceptional concentration of species found "
        "nowhere else — including a toad that gives birth to live young rather than "
        "laying eggs. UNESCO listed the massif in 1981 and 1982 across the borders.\n\n"
        "This is the least accessible site in this list, and deliberately so. It is a "
        "strict reserve: access is regulated, permits are required, and there is no "
        "tourist infrastructure. If you are a naturalist and you want to go, tell us "
        "early and we will start the paperwork. If you want a straightforward hiking "
        "trip, Man is the better answer.",
        "Le massif du Nimba s'élève au point de rencontre de la Côte d'Ivoire, de la "
        "Guinée et du Liberia, et son isolement a produit une concentration "
        "exceptionnelle d'espèces qu'on ne trouve nulle part ailleurs — dont un crapaud "
        "qui met bas des petits vivants au lieu de pondre. L'UNESCO a classé le massif en "
        "1981 et 1982 de part et d'autre des frontières.\n\n"
        "C'est le site le moins accessible de cette liste, et volontairement. Il s'agit "
        "d'une réserve intégrale : l'accès est réglementé, des autorisations sont "
        "nécessaires, et il n'existe aucune infrastructure touristique. Si vous êtes "
        "naturaliste et voulez y aller, dites-le tôt et nous lancerons les démarches. Si "
        "vous cherchez simplement de la randonnée, Man est la meilleure réponse."),
    see=[
        (("Endemic species", "Les espèces endémiques"),
         ("The massif's isolation has produced species restricted to these slopes alone — "
          "the reason for its protected status.",
          "L'isolement du massif a produit des espèces limitées à ces seuls versants — la "
          "raison de son statut de protection.")),
        (("High-altitude grassland", "Les prairies d'altitude"),
         ("Above the forest line, open grassland covers the ridges, a landscape unlike "
          "anything else in the country.",
          "Au-dessus de la limite forestière, des prairies ouvertes couvrent les crêtes, "
          "un paysage sans équivalent dans le pays.")),
    ],
    events=[],
    facts=[
        (("Access", "Accès"), ("Regulated — permits required", "Réglementé — autorisations obligatoires")),
        (("Book ahead", "Réservation"), ("Several months", "Plusieurs mois")),
        (("Who it suits", "Pour qui"), ("Naturalists and specialists", "Naturalistes et spécialistes")),
        (("Alternative", "Alternative"), ("Man, for accessible mountain walking", "Man, pour une randonnée accessible")),
    ]))


def pairs():
    """Tous les couples (anglais, français) de ce fichier, pour lang_fr.py."""
    out = []
    for p in PLACES:
        out.append(p['tag'])
        out.append(p['lede'])
        # les paragraphes sont découpés comme dans le gabarit
        en_paras = p['intro'][0].split('\n\n')
        fr_paras = p['intro'][1].split('\n\n')
        for a, b in zip(en_paras, fr_paras):
            out.append((a.strip(), b.strip()))
        for group in (p['see'], p['events']):
            for t, x in group:
                out.append(t)
                out.append(x)
        for k, v in p['facts']:
            out.append(k)
            out.append(v)
    return out
