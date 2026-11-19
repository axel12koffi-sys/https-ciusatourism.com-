# -*- coding: utf-8 -*-
"""Contenu éditorial bilingue des pages Destinations.

Chaque chaîne est un couple (anglais, français). L'anglais sert de version
principale ; le français est extrait automatiquement pour construire le
dictionnaire de traduction (voir lang_fr.py).

Volontairement : pas de prix, pas de dates de festival, pas d'horaires.
Ce sont les informations qui vieillissent mal sur un site.
"""

from paths import IMG as U

# ------------------------------------------------------------------ PLAGES
BEACHES = [
    dict(
        name="Grand-Bassam",
        dist=("45 min from Abidjan", "45 min d'Abidjan"),
        desc=("The country's first colonial capital. Its Quartier France has been on "
              "the UNESCO World Heritage list since 2012 — crumbling red-brick "
              "facades, the national costume museum, and the beach at the end of "
              "every street. It's where Abidjan goes on Sunday, and the easiest place "
              "to understand the country's history without leaving the coast.",
              "Première capitale coloniale du pays. Son quartier France est inscrit au "
              "patrimoine mondial de l'UNESCO depuis 2012 — façades de brique rouge "
              "qui s'effritent, musée national du costume, et la plage au bout de "
              "chaque rue. C'est la sortie du dimanche des Abidjanais, et le meilleur "
              "endroit pour comprendre l'histoire du pays sans quitter le littoral."),
        tips=[("UNESCO-listed Quartier France", "Quartier France classé UNESCO"),
              ("National costume museum", "Musée national du costume"),
              ("Abissa festival of the N'Zima people", "Festival Abissa du peuple N'Zima")],
        img="assets/img/dest/grand-bassam.svg"),

    dict(
        name="Assinie",
        dist=("2 h from Abidjan", "2 h d'Abidjan"),
        desc=("A spit of sand between the Aby lagoon and the Atlantic. Still water, "
              "pirogues and boat trips on one side; ocean swell on the other. It's the "
              "weekend destination, with the best lodges in the country and easy "
              "access to the Ehotilé islands.",
              "Une langue de sable entre la lagune Aby et l'Atlantique. D'un côté eau "
              "calme, pirogues et sorties en bateau ; de l'autre, l'océan et ses "
              "rouleaux. C'est la destination week-end par excellence, avec les plus "
              "beaux lodges du pays et un accès facile aux îles Ehotilé."),
        tips=[("Lagoon and ocean facing each other", "Lagune et océan face à face"),
              ("Watersports and pirogue trips", "Sports nautiques et sorties en pirogue"),
              ("Ehotilé islands national park nearby", "Parc national des îles Ehotilé à proximité")],
        img="assets/img/dest/assinie.svg"),

    dict(
        name="Sassandra",
        dist=("4 h west", "4 h à l'ouest"),
        desc=("A former trading post turned fishing port, sitting at the mouth of the "
              "river of the same name. Sheltered coves on either side, cliffs, and a "
              "fishing rhythm that sets the pace of the day. It's the quietest option, "
              "and the one travellers talk about most on the way home.",
              "Ancien comptoir devenu port de pêche, posé à l'embouchure du fleuve du "
              "même nom. Des criques abritées de part et d'autre, des falaises, et une "
              "activité de pêche qui rythme la journée. C'est l'option la plus calme, "
              "et celle dont les voyageurs reparlent le plus au retour."),
        tips=[("Sheltered coves", "Criques abritées"),
              ("A working fishing port", "Port de pêche en activité"),
              ("Colonial remains above the river", "Vestiges coloniaux au-dessus du fleuve")],
        img="assets/img/dest/sassandra.svg"),

    dict(
        name="San Pedro",
        dist=("6 h west", "6 h à l'ouest"),
        desc=("The country's second port, and the gateway to the wildest beaches on "
              "the western coast. Less visited, rougher, with the forest coming down "
              "to the sand in places. Best combined with Taï National Park, a few "
              "hours inland.",
              "Deuxième port du pays, et point de départ vers les plages les plus "
              "sauvages de la côte ouest. Moins fréquenté, plus brut, avec la forêt "
              "qui descend jusqu'au sable par endroits. À combiner avec le parc de "
              "Taï, à quelques heures de route."),
        tips=[("Long, quiet beaches", "Longues plages peu fréquentées"),
              ("Gateway to Taï National Park", "Porte d'entrée du parc de Taï"),
              ("Reachable by domestic flight", "Accessible en vol intérieur")],
        img="assets/img/dest/san-pedro.svg"),

    dict(
        name="Jacqueville",
        dist=("1 h 30 from Abidjan", "1 h 30 d'Abidjan"),
        desc=("An island joined to the mainland by a bridge, between the Ébrié lagoon "
              "and the ocean. Fishing villages, coconut groves, and a strip of sand "
              "that runs for kilometres. Close enough for a day trip, quiet enough to "
              "stay the night.",
              "Une île reliée au continent par un pont, entre lagune Ébrié et océan. "
              "Villages de pêcheurs, cocoteraies, et une bande de sable qui court sur "
              "des kilomètres. Suffisamment proche pour une journée, assez tranquille "
              "pour y dormir."),
        tips=[("Doable as a day trip", "Accessible à la journée"),
              ("Coconut groves and fishing villages", "Cocoteraies et villages de pêcheurs")],
        img="assets/img/dest/jacqueville.svg"),

    dict(
        name="Grand-Lahou",
        dist=("3 h from Abidjan", "3 h d'Abidjan"),
        desc=("The old town is slowly being reclaimed by the sea — a striking site, "
              "where you walk between colonial buildings the ocean is eating away. "
              "Next to it, the mouth of the Bandama river and Azagny National Park "
              "offer lagoons and mangroves.",
              "La vieille ville est progressivement reprise par la mer — un site "
              "saisissant, où l'on marche entre des bâtiments coloniaux que l'océan "
              "grignote. À côté, l'embouchure du Bandama et le parc national d'Azagny "
              "offrent lagunes et mangroves."),
        tips=[("A town being reclaimed by the ocean", "Ancienne ville reprise par l'océan"),
              ("Mangroves of Azagny National Park", "Mangroves du parc d'Azagny")],
        img="assets/img/dest/grand-lahou.svg"),
]

BEACH_FAQ = [
    (("When is the water best?",
      "Quelle est la meilleure période pour se baigner ?"),
     ("November to April, during the southern dry season: calmer sea, clear skies. "
      "From June to September the rain is heavy on the coast and the sea rougher.",
      "De novembre à avril, pendant la grande saison sèche du sud : mer plus calme, "
      "ciel dégagé. De juin à septembre, les pluies sont fortes sur la côte et la "
      "mer plus agitée.")),
    (("Can you swim everywhere?", "Peut-on nager partout ?"),
     ("No. The Atlantic has a strong undertow in places, which is why lagoon-side "
      "lodges and sheltered coves feature so heavily in our itineraries. Your guide "
      "will tell you where to swim on each beach.",
      "Non. L'Atlantique a un fort courant de retour à certains endroits, ce qui "
      "explique la place des lodges en bord de lagune et des criques abritées dans "
      "nos itinéraires. Votre guide vous indique où nager sur chaque plage.")),
    (("How do you travel between beaches?", "Comment circule-t-on entre les plages ?"),
     ("By private vehicle with a driver. Grand-Bassam, Jacqueville and Assinie work "
      "as day trips from Abidjan; Sassandra and San Pedro deserve an overnight.",
      "En véhicule privé avec chauffeur. Grand-Bassam, Jacqueville et Assinie se font "
      "à la journée depuis Abidjan ; Sassandra et San Pedro méritent une nuit sur "
      "place.")),
    (("Is there beachfront accommodation?", "Y a-t-il des hébergements en bord de mer ?"),
     ("Yes, in Assinie, Grand-Bassam and San Pedro in particular. Our Hotel page "
      "lists the properties we book, with their direct contacts.",
      "Oui, à Assinie, Grand-Bassam et San Pedro notamment. Notre page Hôtels liste "
      "les établissements que nous réservons, avec leurs coordonnées.")),
]

# ---------------------------------------------------------------- CULTURE
CULTURE = [
    dict(
        name="Yamoussoukro",
        dist=("3 h from Abidjan", "3 h d'Abidjan"),
        desc=("The political capital, grown out of Félix Houphouët-Boigny's home "
              "village. You visit the Basilica of Our Lady of Peace, consecrated in "
              "1990 by John Paul II and one of the largest churches in the world, then "
              "the presidential palace and its crocodile lake.",
              "La capitale politique, née du village natal de Félix Houphouët-Boigny. "
              "On y visite la basilique Notre-Dame de la Paix, consacrée en 1990 par "
              "Jean-Paul II et l'une des plus grandes églises du monde, puis le palais "
              "présidentiel et son lac aux crocodiles."),
        tips=[("Basilica of Our Lady of Peace", "Basilique Notre-Dame de la Paix"),
              ("Presidential palace and its lake", "Palais présidentiel et son lac"),
              ("Houphouët-Boigny Foundation", "Fondation Houphouët-Boigny")],
        img="assets/img/dest/yamoussoukro.svg"),

    dict(
        name="Korhogo and Senufo country",
        dist=("Northern Côte d'Ivoire", "Nord du pays"),
        desc=("The capital of the north and the heart of Senufo culture. The nearby "
              "village of Fakaha produces the Korhogo cloth — cotton painted with "
              "plant pigments, now an emblem of the country. Around it, villages of "
              "carvers, blacksmiths and weavers.",
              "Capitale du nord et cœur de la culture sénoufo. Le village de Fakaha, "
              "tout proche, produit la toile de Korhogo — ces cotonnades peintes aux "
              "pigments végétaux devenues emblème du pays. Autour, des villages de "
              "sculpteurs, de forgerons et de tisserands."),
        tips=[("Painted cloth from Fakaha", "Toiles peintes de Fakaha"),
              ("Carving and blacksmith villages", "Villages de sculpteurs et de forgerons"),
              ("Senufo markets", "Marchés sénoufo")],
        img="assets/img/dest/korhogo.svg"),

    dict(
        name="Man and the masks of the West",
        dist=("8 h from Abidjan", "8 h d'Abidjan"),
        desc=("The Man region is Dan and Wè mask country, where mask appearances "
              "remain tied to village ceremonies rather than performance. You come "
              "with a local guide and an introduction: these are living traditions, "
              "not an attraction.",
              "La région de Man est le pays des masques dan et wè, dont les sorties "
              "restent liées aux cérémonies villageoises plutôt qu'au spectacle. On y "
              "vient avec un guide local et une introduction : ce sont des traditions "
              "vivantes, pas une attraction."),
        tips=[("Dan and Wè traditions", "Traditions dan et wè"),
              ("Stilt dancing", "Danses d'échasses"),
              ("Visits arranged with the families", "Rencontres organisées avec les familles")],
        img="assets/img/dest/man.svg"),

    dict(
        name="Abidjan",
        dist=("Your starting point", "Point de départ"),
        desc=("The Plateau and its towers, Saint Paul's Cathedral, the museum of "
              "civilisations, the Cocody artisan village, and the markets of "
              "Treichville and Adjamé. A well-run day in the city teaches you as much "
              "as a week elsewhere.",
              "Le Plateau et ses tours, la cathédrale Saint-Paul, le musée des "
              "civilisations, le village artisanal de Cocody, et les marchés de "
              "Treichville et d'Adjamé. Une journée bien menée dans la ville en "
              "apprend autant qu'une semaine ailleurs."),
        tips=[("Museum of civilisations", "Musée des civilisations"),
              ("Cocody artisan village", "Village artisanal de Cocody"),
              ("Treichville and Adjamé markets", "Marchés de Treichville et d'Adjamé")],
        img="assets/img/dest/abidjan.svg"),

    dict(
        name="Bouaké",
        dist=("Central Côte d'Ivoire", "Centre du pays"),
        desc=("The second city and the Baoulé capital, known for its carnival and its "
              "large market. Nearby, Katiola and its Mangoro potters, whose skill has "
              "passed from woman to woman for generations.",
              "Deuxième ville du pays et capitale baoulé, connue pour son carnaval et "
              "son grand marché. À proximité, Katiola et ses potières mangoro, dont le "
              "savoir-faire se transmet entre femmes depuis des générations."),
        tips=[("Bouaké carnival", "Carnaval de Bouaké"),
              ("Katiola pottery", "Poteries de Katiola"),
              ("The great market", "Grand marché")],
        img="assets/img/dest/bouake.svg"),

    dict(
        name="Tiégba",
        dist=("2 h from Abidjan", "2 h d'Abidjan"),
        desc=("A village built on stilts above the lagoon, reached by pirogue. Life is "
              "organised around the water: fishing, movement, trade. Half a day that "
              "changes your perspective on the country.",
              "Un village bâti sur pilotis au-dessus de la lagune, que l'on atteint en "
              "pirogue. La vie s'organise autour de l'eau : pêche, déplacements, "
              "commerce. Une demi-journée qui change la perspective sur le pays."),
        tips=[("Stilt village on the lagoon", "Village lacustre sur pilotis"),
              ("Reached by pirogue", "Accès en pirogue")],
        img="assets/img/dest/tiegba.svg"),
]

CULTURE_FAQ = [
    (("Can we attend a mask ceremony?", "Peut-on assister à des cérémonies de masques ?"),
     ("Sometimes, when the village calendar allows and provided you are properly "
      "introduced. These are ritual ceremonies, not performances: we ask permission "
      "in advance and explain the etiquette before the visit. We never promise a mask "
      "appearance on a fixed date.",
      "Parfois, quand le calendrier villageois le permet et à condition d'être "
      "introduit. Ce sont des cérémonies rituelles, pas des représentations : nous "
      "demandons l'autorisation en amont et expliquons les usages avant la visite. "
      "Nous ne promettons jamais une sortie de masque à date fixe.")),
    (("What are the major festivals?", "Quels sont les grands festivals ?"),
     ("FEMUA in Abidjan, the urban music festival born in the Anoumabo "
      "neighbourhood; Abissa in Grand-Bassam, the festival of the N'Zima people; the "
      "Bouaké carnival; and many traditional celebrations in the north and west. Send "
      "us your dates and we'll see what falls during your stay.",
      "Le FEMUA à Abidjan, festival de musiques urbaines né dans le quartier "
      "d'Anoumabo ; l'Abissa à Grand-Bassam, fête du peuple N'Zima ; le carnaval de "
      "Bouaké ; et de nombreuses fêtes traditionnelles dans le nord et l'ouest. "
      "Donnez-nous vos dates, nous regardons ce qui tombe pendant votre séjour.")),
    (("Do we need to speak French?", "Faut-il parler français ?"),
     ("No. French is the official language, but all our guides work in English and "
      "also translate the local languages.",
      "Non. Le français est la langue officielle, mais tous nos guides travaillent en "
      "anglais et traduisent aussi les langues locales.")),
    (("Can we take photographs?", "Peut-on photographier ?"),
     ("In markets and villages, you ask first. Some objects and ceremonies are not "
      "photographed at all. Your guide will tell you when to take the camera out, and "
      "it's a rule to follow without arguing.",
      "Dans les marchés et les villages, on demande d'abord. Certains objets et "
      "cérémonies ne se photographient pas du tout. Votre guide vous dira quand "
      "sortir l'appareil, et c'est une règle qui se respecte sans discussion.")),
    (("Can we buy crafts on site?", "Peut-on acheter de l'artisanat sur place ?"),
     ("Yes, directly from the workshops in Fakaha, Katiola or the Cocody artisan "
      "village. Buying at the workshop supports the maker rather than the middleman, "
      "and the quality has nothing to do with the tourist stalls.",
      "Oui, directement aux ateliers de Fakaha, de Katiola ou au village artisanal de "
      "Cocody. Acheter à l'atelier fait vivre l'artisan plutôt que l'intermédiaire, et "
      "la qualité n'a rien à voir avec celle des étals touristiques.")),
]

# ------------------------------------------------------ AVENTURE & NATURE
ECO = [
    dict(
        name="Taï National Park",
        dist=("South-west", "Sud-ouest"),
        desc=("One of the last stands of primary rainforest in West Africa, on the "
              "UNESCO World Heritage list. You can see chimpanzees, known for their "
              "tool use, along with many forest primates and birds. Groups stay small "
              "and a guide is mandatory.",
              "L'un des derniers massifs de forêt tropicale primaire d'Afrique de "
              "l'Ouest, inscrit au patrimoine mondial de l'UNESCO. On y observe des "
              "chimpanzés, connus pour leur usage d'outils, ainsi que de nombreux "
              "primates et oiseaux forestiers. Les groupes restent petits et "
              "l'encadrement est obligatoire."),
        tips=[("UNESCO-listed primary forest", "Forêt primaire classée UNESCO"),
              ("Chimpanzees and forest primates", "Chimpanzés et primates forestiers"),
              ("Guided walks in small groups", "Marches guidées en petit groupe")],
        img="assets/img/dest/tai.svg"),

    dict(
        name="Comoé National Park",
        dist=("North-east", "Nord-est"),
        desc=("One of the largest protected areas in West Africa, also UNESCO-listed. "
              "Savanna, gallery forest along the Comoé river, and savanna wildlife: "
              "antelope, warthog, hippopotamus, and remarkable birdlife.",
              "L'une des plus vastes aires protégées d'Afrique de l'Ouest, également "
              "classée UNESCO. Savane, forêts-galeries le long du fleuve Comoé, et une "
              "faune de savane : antilopes, phacochères, hippopotames, une avifaune "
              "remarquable."),
        tips=[("Savanna and gallery forest", "Savane et forêts-galeries"),
              ("Savanna wildlife and birdlife", "Faune de savane et avifaune"),
              ("The country's largest park", "Le plus grand parc du pays")],
        img="assets/img/dest/comoe.svg"),

    dict(
        name="The Man region",
        dist=("West", "Ouest"),
        desc=("The city of eighteen mountains. Waterfalls, liana bridges woven above "
              "the rivers, Mount Tonkoui and its viewpoints, the Dent de Man for "
              "walkers. The most dramatic landscape in the country.",
              "La « cité des dix-huit montagnes ». Cascades, ponts de lianes tressés "
              "au-dessus des rivières, mont Tonkoui et ses points de vue, dent de Man "
              "pour les marcheurs. Le relief le plus spectaculaire du pays."),
        tips=[("Waterfalls and liana bridges", "Cascades et ponts de lianes"),
              ("Mount Tonkoui", "Mont Tonkoui"),
              ("Mountain hiking", "Randonnées en montagne")],
        img="assets/img/dest/man.svg"),

    dict(
        name="Banco National Park",
        dist=("Inside Abidjan", "Dans Abidjan"),
        desc=("Thousands of hectares of rainforest inside the city itself. An "
              "arboretum, marked trails, and the famous fanico — the open-air "
              "traditional laundry on the riverbank. Ideal for half a day without "
              "leaving Abidjan.",
              "Une forêt tropicale de plusieurs milliers d'hectares à l'intérieur même "
              "de la ville. Arboretum, sentiers balisés, et le célèbre « fanico », la "
              "laverie traditionnelle à ciel ouvert au bord de la rivière. Idéal en "
              "demi-journée, sans quitter Abidjan."),
        tips=[("Primary forest inside the city", "Forêt primaire en pleine ville"),
              ("Marked trails and an arboretum", "Sentiers balisés et arboretum"),
              ("Doable in half a day", "Faisable en demi-journée")],
        img="assets/img/dest/banco.svg"),

    dict(
        name="Ehotilé Islands",
        dist=("Near Assinie", "Près d'Assinie"),
        desc=("An archipelago in the Aby lagoon, protected as a national park. "
              "Mangroves, water birds, and islets the local communities consider "
              "sacred. Reached by pirogue from Assinie.",
              "Un archipel d'îles dans la lagune Aby, classé parc national. Mangroves, "
              "oiseaux d'eau, et des îlots considérés comme sacrés par les populations "
              "riveraines. On y accède en pirogue depuis Assinie."),
        tips=[("Mangroves and water birds", "Mangroves et oiseaux d'eau"),
              ("Reached by pirogue", "Accès en pirogue"),
              ("Sacred islets", "Îlots sacrés")],
        img="assets/img/dest/ehotile.svg"),

    dict(
        name="Mount Nimba",
        dist=("Western border", "Frontière ouest"),
        desc=("A strict nature reserve on the World Heritage list, shared with Guinea "
              "and Liberia. A massif of exceptional biodiversity, with endemic "
              "species. Access is regulated and takes a long time to arrange.",
              "Réserve intégrale classée au patrimoine mondial, partagée avec la "
              "Guinée et le Liberia. Un massif d'une biodiversité exceptionnelle, avec "
              "des espèces endémiques. L'accès est réglementé et se prépare longtemps "
              "à l'avance."),
        tips=[("UNESCO-listed reserve", "Réserve classée UNESCO"),
              ("Endemic species", "Espèces endémiques"),
              ("Regulated access, arrange early", "Accès réglementé, à préparer en amont")],
        img="assets/img/dest/nimba.svg"),
]

ECO_FAQ = [
    (("Is this like an East African safari?", "Peut-on faire un safari comme en Afrique de l'Est ?"),
     ("No, and it's better to know that before you come. Côte d'Ivoire is a country "
      "of forest and moist savanna: you see primates, birds, antelope, sometimes "
      "hippos and forest elephants. It is not the big five of the Kenyan plains. "
      "People who come for that leave disappointed; people who come for the forest "
      "leave converted.",
      "Non, et il vaut mieux le savoir avant de partir. La Côte d'Ivoire est un pays "
      "de forêt et de savane humide : on y observe des primates, des oiseaux, des "
      "antilopes, parfois des hippopotames et des éléphants de forêt. Ce n'est pas le "
      "« big five » des plaines du Kenya. Ceux qui viennent pour ça repartent déçus ; "
      "ceux qui viennent pour la forêt repartent conquis.")),
    (("What fitness level is needed?", "Quel niveau physique faut-il ?"),
     ("Forest walks are flat but long, hot and humid. The Man region asks a little "
      "more because of the terrain. We match the days to your pace — just tell us "
      "what you're after.",
      "Les marches en forêt sont plates mais longues, chaudes et humides. La région de "
      "Man demande un peu plus de souffle à cause du relief. Nous adaptons les "
      "journées à votre rythme, dites-nous simplement ce que vous visez.")),
    (("How far ahead should we book?", "Faut-il réserver longtemps à l'avance ?"),
     ("For Taï and Mount Nimba, well ahead: access is controlled and permits take "
      "time. Allow at least two months. Banco and the Ehotilé islands can be arranged "
      "in a few days.",
      "Pour Taï et le mont Nimba, oui : les accès sont encadrés et les autorisations "
      "prennent du temps. Comptez au moins deux mois. Le Banco et les îles Ehotilé "
      "s'organisent en quelques jours.")),
    (("What's the best season?", "Quelle est la meilleure saison ?"),
     ("The dry season, November to April, for the tracks and for walking comfort. In "
      "the rainy season the forest is greener but access becomes difficult.",
      "La saison sèche, de novembre à avril, pour les pistes et le confort de marche. "
      "En saison des pluies la forêt est plus verte mais les accès deviennent "
      "difficiles.")),
    (("Where do you stay near the parks?", "Comment se loge-t-on près des parcs ?"),
     ("In ecolodges and community-run accommodation — simple but well kept. It's also "
      "what supports the surrounding villages, and therefore what protects the park.",
      "En écolodges et hébergements communautaires, simples mais bien tenus. C'est "
      "aussi ce qui fait vivre les villages riverains, et donc ce qui protège le "
      "parc.")),
]


# ------------------------------------------------------------------ OUTILS
def en(v):
    """Extrait la version anglaise d'un couple (en, fr)."""
    return v[0] if isinstance(v, tuple) else v


def pairs():
    """Tous les couples (anglais, français) du fichier, pour lang_fr.py.

    Inclut les noms composés et les premières phrases tronquées utilisées
    dans la grille des destinations : sans elles, le remplacement partiel
    produirait des phrases mi-anglaises mi-françaises.
    """
    out = []
    for group in (BEACHES, CULTURE, ECO):
        for p in group:
            out.append(p['dist'])
            out.append(p['desc'])
            out.extend(p['tips'])
            # première phrase seule, telle que la grille l'affiche
            out.append((p['desc'][0].split('. ')[0] + '.',
                        p['desc'][1].split('. ')[0] + '.'))
    for faq in (BEACH_FAQ, CULTURE_FAQ, ECO_FAQ):
        for q, a in faq:
            out.append(q)
            out.append(a)
    return out
