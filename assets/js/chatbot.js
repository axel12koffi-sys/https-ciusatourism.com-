/* ============================================================
   SUBLIME CI-USA — chatbot.js
   « Aya » — assistante virtuelle du bureau du tourisme.
   Personnage : ivoiro-américaine, entre Washington D.C. et
   Abidjan. Ton chaleureux, direct, jamais commercial.

   Bilingue FR / EN : la langue suit le sélecteur du site
   (localStorage 'ciusa-lang') et bascule automatiquement si
   l'internaute écrit dans l'autre langue.

   PASSAGE AU PHP : mettre USE_API = true. api/chat.php reçoit
   { message, history, lang } et renvoie { reply }. Le moteur de
   règles ci-dessous reste le filet de sécurité si l'API échoue.
   ============================================================ */
(function () {
  'use strict';

  var USE_API   = false;
  var API_URL   = '/api/chat.php';
  var STORE_KEY = 'ciusa-chat-aya';

  var btn   = document.getElementById('chatBtn');
  var panel = document.getElementById('chatPanel');
  if (!btn || !panel) return;

  var log   = document.getElementById('chatLog');
  var input = document.getElementById('chatInput');
  var send  = document.getElementById('chatSend');
  var quick = document.getElementById('chatQuick');
  var close = document.getElementById('chatClose');

  var history = [];
  try { history = JSON.parse(sessionStorage.getItem(STORE_KEY) || '[]'); } catch (e) {}

  /* raccourci vers le rig animé (aya.js) — silencieux s'il est absent */
  function pose(state, hold) { if (window.Aya) window.Aya.set(state, hold); }

  function L(list) {
    return '<ul class="cl">' + list.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>';
  }

  /* ============================================================
     BASE DE CONNAISSANCES
     Chaque entrée : { id, re (motifs FR + EN), en, fr }
     L'ordre compte : les intentions les plus spécifiques d'abord.
     ============================================================ */
  var KB = [

  /* ---------- identité & courtoisie ---------- */
  { id: 'who', re: /(qui (es|est)[- ]tu|qui (etes|êtes)|t(u es|'es) qui|who are you|what are you|your name|ton nom|^aya)/i,
    en: "I'm <b>Aya</b> — Ivorian-American, and I answer questions about visiting Côte d'Ivoire. I grew up between Abidjan and the D.C. area, so I know both ends of this trip. Ask me anything: visas, beaches, food, budget, safety.",
    fr: "Moi c'est <b>Aya</b> — ivoiro-américaine, et je réponds aux questions sur un voyage en Côte d'Ivoire. J'ai grandi entre Abidjan et la région de Washington, donc je connais les deux bouts du trajet. Demandez-moi ce que vous voulez : visa, plages, cuisine, budget, sécurité." },

  { id: 'greet', re: /^\s*(hi|hello|hey|good (morning|evening|afternoon)|bonjour|bonsoir|salut|coucou|yo)\b/i,
    en: "Hello! I'm <b>Aya</b>, your guide to Côte d'Ivoire. Visas, best season, beaches, food, hotels, budget — ask away, in English or French.",
    fr: "Bonjour ! Moi c'est <b>Aya</b>, votre guide pour la Côte d'Ivoire. Visa, meilleure saison, plages, cuisine, hôtels, budget — posez votre question, en français ou en anglais." },

  { id: 'thanks', re: /(thank|thanks|thx|merci|nickel|parfait|super|g(e|é)nial)/i,
    en: "With pleasure. Anything else you'd like to know before you go?",
    fr: "Avec plaisir. Autre chose avant votre départ ?" },

  { id: 'human', re: /(parler (a|à) (quelqu'un|un humain|un conseiller)|speak to (someone|a human|an agent)|real person|vrai humain|conseiller|advisor)/i,
    en: "Of course. Email <b>tourism@ambaciusa.org</b> or call <b>(240) 756-8332</b> — the office is at 2424 Massachusetts Avenue N.W., Washington, D.C. You can also use the contact form; we reply within two business days.",
    fr: "Bien sûr. Écrivez à <b>tourism@ambaciusa.org</b> ou appelez le <b>(240) 756-8332</b> — le bureau est au 2424 Massachusetts Avenue N.W., Washington D.C. Vous pouvez aussi passer par le formulaire de contact, réponse sous deux jours ouvrés." },

  /* ---------- informations générales ---------- */
  { id: 'why', re: /(pourquoi (visiter|aller|venir)|why (visit|go|come)|worth (visiting|it)|(c|ç)a vaut le coup|int(e|é)r(e|ê)t)/i,
    en: "Côte d'Ivoire offers a rare mix of culture, food, beaches, nature, music and modern city life. From the energy of Abidjan to traditional villages in the north, the experience is authentic and the welcome is real.",
    fr: "La Côte d'Ivoire offre une combinaison rare : culture, gastronomie, plages, nature, musique et modernité. Des villes dynamiques comme Abidjan aux villages traditionnels du nord, l'expérience est authentique et l'accueil chaleureux." },

  { id: 'season', re: /(best (time|season|period)|when (should|to) (go|visit|travel)|meilleure (p(e|é)riode|saison)|quand (partir|aller|voyager)|quel mois)/i,
    en: "<b>November to April</b> — the dry season. That's the window for sightseeing, beaches and anything outdoors. Rain is heaviest on the coast between June and September.",
    fr: "<b>De novembre à avril</b>, pendant la saison sèche. C'est la fenêtre idéale pour les visites et les activités de plein air. Les pluies sont les plus fortes sur la côte entre juin et septembre." },

  { id: 'safety', re: /(safe|safety|s(e|é)curit(e|é)|s(u|û)ret(e|é)|est[- ]ce s(u|û)r|c'est s(u|û)r|dangereux|dangerous|risqu|crime|is it ok to (go|travel))/i,
    en: "Yes. Côte d'Ivoire welcomes visitors from all over the world every year. As with any international destination, follow the usual travel and safety recommendations and stick to well-established tourist areas. Our team in Abidjan is reachable throughout your trip.",
    fr: "Oui. La Côte d'Ivoire accueille chaque année des visiteurs du monde entier. Comme pour tout voyage international, suivez les conseils de sécurité habituels et privilégiez les zones touristiques reconnues. Notre équipe à Abidjan reste joignable pendant tout le séjour." },

  { id: 'mustsee', re: /(must[- ]see|incontournable|top (places|spots)|what to see|quoi voir|o(u|ù) aller|places to visit|itin(e|é)raire|yamoussoukro|korhogo)/i,
    en: "The places people come back talking about:" + L(['Abidjan', 'Grand-Bassam', 'Yamoussoukro', 'Assinie', 'Korhogo', 'Man and its mountains', 'Taï National Park']),
    fr: "Les lieux dont on parle encore au retour :" + L(['Abidjan', 'Grand-Bassam', 'Yamoussoukro', 'Assinie', 'Korhogo', 'Man et ses montagnes', 'le Parc National de Taï']) },

  { id: 'duration', re: /(how (many|long) days|combien de (jours|temps)|dur(e|é)e (du|de)|length of (trip|stay)|how long)/i,
    en: "<b>7 to 10 days</b> lets you cover several regions comfortably. Even a short stay in Abidjan and Grand-Bassam gives you a real cultural immersion.",
    fr: "<b>7 à 10 jours</b> permettent de découvrir plusieurs régions sans courir. Même un court séjour à Abidjan et Grand-Bassam offre déjà une belle immersion culturelle." },

  /* ---------- visa & formalités ---------- */
  { id: 'evisa', re: /(e[- ]?visa|visa en ligne|online visa|snedai|demande de visa|apply for (a )?visa)/i,
    en: "There is an <b>e-visa</b> system: you apply online before you travel, upload the required documents, and the process is quick. The application goes through <a href='https://snedai.com/e-visa/' target='_blank' rel='noopener noreferrer'>snedai.com/e-visa</a>, the only accredited government portal — other sites add fees for nothing. We prepare the whole file for you as part of our Travel Assistance service.",
    fr: "Un système d'<b>e-visa</b> existe : la demande se fait en ligne avant le départ, avec téléchargement des documents requis. Elle se fait sur <a href='https://snedai.com/e-visa/' target='_blank' rel='noopener noreferrer'>snedai.com/e-visa</a>, le seul portail gouvernemental accrédité — les autres sites ajoutent des frais sans contrepartie. Nous montons le dossier complet pour vous dans le cadre de notre service d'assistance." },

  { id: 'visadocs', re: /(documents? (n(e|é)cessaires|requis|required|needed)|quels documents|what (documents|papers)|pi(e|è)ces (a|à) fournir)/i,
    en: "Usually:" + L(['A valid passport', 'Your flight itinerary', 'A hotel reservation or letter of invitation', 'A passport photo']) + "Your passport should be valid at least <b>6 months</b> beyond your entry date.",
    fr: "En général :" + L(["un passeport valide", "le billet d'avion", "une réservation d'hôtel ou une lettre d'invitation", "une photo d'identité"]) + "Le passeport doit être valide au moins <b>6 mois</b> après la date d'entrée." },

  { id: 'passport', re: /(passport valid|validit(e|é) (du )?passeport|passeport valide|6 months|six mois)/i,
    en: "Your passport should be valid for at least <b>6 months</b> beyond your date of entry into Côte d'Ivoire.",
    fr: "Votre passeport doit être valide au moins <b>6 mois</b> après la date d'entrée sur le territoire ivoirien." },

  { id: 'vaccine', re: /(vaccin|vaccine|fi(e|è)vre jaune|yellow fever|health requirement|malaria|paludisme)/i,
    en: "The <b>yellow fever vaccine is mandatory</b> to enter Côte d'Ivoire — you'll be asked for the certificate on arrival. Talk to a travel clinic about malaria prophylaxis too; we send a full health briefing before departure.",
    fr: "Le <b>vaccin contre la fièvre jaune est obligatoire</b> pour entrer en Côte d'Ivoire — le certificat est demandé à l'arrivée. Parlez aussi du paludisme à un centre de vaccination internationale ; nous envoyons un briefing santé complet avant le départ." },

  { id: 'visa', re: /(visa|formalit(e|é)s|entry requirement|immigration|entrer dans le pays)/i,
    en: "Most international travelers need a visa for Côte d'Ivoire, and an <b>e-visa</b> is available to make it straightforward. Yellow fever vaccination is required. We handle the application file for you — ask me about the documents if you want the list.",
    fr: "La plupart des voyageurs internationaux ont besoin d'un visa pour la Côte d'Ivoire, et un <b>e-visa</b> existe pour simplifier la démarche. La vaccination contre la fièvre jaune est obligatoire. Nous montons le dossier pour vous — demandez-moi la liste des documents si besoin." },

  /* ---------- vols & transport ---------- */
  { id: 'airport', re: /(a(e|é)roport|airport|houphou(e|ë)t|\bfhb\b|\babj\b|\biad\b|dulles)/i,
    en: "The main gateway is <b>Félix Houphouët-Boigny International Airport</b> in Abidjan (ABJ), in Port-Bouët. Several international airlines fly in from Europe, the United States, the Middle East and across Africa — from Washington you'll connect, usually via Paris, Brussels, Casablanca or Addis Ababa.",
    fr: "La porte d'entrée principale est l'<b>aéroport international Félix Houphouët-Boigny</b> d'Abidjan (ABJ), à Port-Bouët. Plusieurs compagnies internationales le desservent depuis l'Europe, les États-Unis, le Moyen-Orient et l'Afrique — depuis Washington il y a une escale, généralement Paris, Bruxelles, Casablanca ou Addis-Abeba." },

  { id: 'domestic', re: /(domestic flight|vol (int(e|é)rieur|domestique|national)|inland flight)/i,
    en: "Yes — domestic flights connect several major Ivorian cities, which saves a long drive if you're heading to San Pedro, Korhogo or Man. We can book them alongside your international ticket.",
    fr: "Oui — des vols intérieurs relient plusieurs grandes villes ivoiriennes, ce qui évite de longues routes vers San Pedro, Korhogo ou Man. Nous pouvons les réserver en même temps que le billet international." },

  { id: 'carrental', re: /(louer une voiture|location de voiture|rent a car|car rental|hire a car|conduire|driving)/i,
    en: "Yes. Certified agencies rent vehicles, and it's the option that gives you the most freedom — you can reach places well off the usual routes. If you'd rather not drive, we arrange a private driver instead. Full detail on our Transport page.",
    fr: "Oui. Des agences certifiées louent des véhicules, et c'est l'option qui offre le plus de liberté — vous atteignez des lieux hors des sentiers battus. Si vous préférez ne pas conduire, nous mettons un chauffeur privé à disposition. Tout le détail sur notre page Transport." },

  { id: 'transport', re: /(transport|se d(e|é)placer|get(ting)? around|taxi|\bvtc\b|uber|yango|heetch|\bbus\b|chauffeur|driver)/i,
    en: "Inside the country you can use:" + L(['taxis', 'ride-hailing apps (Yango, Uber, Heetch)', 'buses', 'private vehicles with a driver', 'domestic flights']) + "For airport transfers and excursions we arrange insured drivers we work with regularly.",
    fr: "Sur place, vous pouvez utiliser :" + L(['les taxis', 'les applis VTC (Yango, Uber, Heetch)', 'les bus', 'les véhicules privés avec chauffeur', 'les vols domestiques']) + "Pour les transferts aéroport et les excursions, nous mettons des chauffeurs assurés que nous connaissons." },

  { id: 'flight', re: /(flight|\bvol\b|avion|airline|compagnie|nonstop|direct|escale|layover)/i,
    en: "Several international airlines serve Abidjan from Europe, the US, the Middle East and Africa. There is no nonstop from Washington — itineraries connect through Paris, Brussels, Casablanca or Addis Ababa. We can hold and issue the reservation for you.",
    fr: "Plusieurs compagnies internationales desservent Abidjan depuis l'Europe, les États-Unis, le Moyen-Orient et l'Afrique. Il n'y a pas de vol direct depuis Washington : les itinéraires passent par Paris, Bruxelles, Casablanca ou Addis-Abeba. Nous pouvons poser l'option et émettre le billet." },

  /* ---------- hébergement ---------- */
  { id: 'wherestay', re: /(o(u|ù) (dormir|loger|s(e|é)journer)|where (to )?stay|quartier|neighbourhood|neighborhood|plateau|cocody|marcory|zone 4)/i,
    en: "In Abidjan the areas visitors like most are <b>Plateau</b> (business district), <b>Cocody</b> (residential, embassies), <b>Marcory</b> and <b>Zone 4</b> (restaurants and nightlife). Our Hotel page lists 23 properties across all four, with capacity and direct contacts.",
    fr: "À Abidjan, les quartiers préférés des visiteurs sont le <b>Plateau</b> (quartier d'affaires), <b>Cocody</b> (résidentiel, ambassades), <b>Marcory</b> et la <b>Zone 4</b> (restaurants et vie nocturne). Notre page Hôtels liste 23 établissements dans ces quatre quartiers, avec capacités et contacts directs." },

  { id: 'budgethotel', re: /(cheap|budget hotel|pas cher|(e|é)conomique|affordable|guesthouse|maison d'h(o|ô)tes|auberge)/i,
    en: "Yes — affordable hotels and guesthouses exist in most tourist areas, alongside the big names. Tell me your nightly budget and I'll point you to the right bracket.",
    fr: "Oui — des hôtels abordables et des maisons d'hôtes existent dans la plupart des zones touristiques, à côté des grandes enseignes. Dites-moi votre budget par nuit et je vous oriente sur la bonne gamme." },

  { id: 'beachhotel', re: /(h(o|ô)tel (de |en bord de )?(plage|mer)|beachfront|near the beach|pr(e|è)s de la (plage|mer)|san pedro)/i,
    en: "<b>Assinie</b>, <b>Grand-Bassam</b> and <b>San Pedro</b> all have accommodation right by the ocean and close to the main attractions. Assinie is the weekend favourite, with the lagoon on one side and the Atlantic on the other.",
    fr: "<b>Assinie</b>, <b>Grand-Bassam</b> et <b>San Pedro</b> offrent des hébergements en bord d'océan, proches des sites touristiques. Assinie est le favori du week-end, avec la lagune d'un côté et l'Atlantique de l'autre." },

  { id: 'hotel', re: /(h(o|ô)tel|h(e|é)bergement|accommodation|lodge|resort|sofitel|m(o|ö)venpick|palmier|radisson|pullman|noom|dormir)/i,
    en: "Côte d'Ivoire has luxury hotels, beach resorts, business hotels, guesthouses and budget options. Well-known addresses include the <b>Sofitel Abidjan Hôtel Ivoire</b>, <b>Mövenpick</b>, <b>Pullman</b>, <b>La Maison Palmier</b> and <b>Coconut Grove Lodge</b>. Our Hotel page has 23 of them with capacity, phone and email.",
    fr: "La Côte d'Ivoire propose des hôtels de luxe, des resorts balnéaires, des hôtels d'affaires, des maisons d'hôtes et des options économiques. Parmi les adresses connues : le <b>Sofitel Abidjan Hôtel Ivoire</b>, le <b>Mövenpick</b>, le <b>Pullman</b>, <b>La Maison Palmier</b> et le <b>Coconut Grove Lodge</b>. Notre page Hôtels en liste 23 avec capacité, téléphone et e-mail." },

  /* ---------- culture ---------- */
  { id: 'food', re: /(food|eat|dish|cuisine|gastronom|manger|plat|sp(e|é)cialit|atti(e|é)k(e|é)|alloco|garba|foutou|kedjenou|sauce graine|restaurant)/i,
    en: "The dishes to try:" + L(['attiéké with grilled fish', 'alloco (fried plantain)', 'garba', 'foutou', 'sauce graine', 'kedjenou']) + "Our Gastronomies page lists 26 restaurants in Abidjan by neighbourhood.",
    fr: "Les plats à goûter :" + L(['attiéké poisson', 'alloco (banane plantain frite)', 'garba', 'foutou', 'sauce graine', 'kedjenou']) + "Notre page Gastronomie liste 26 restaurants d'Abidjan par quartier." },

  { id: 'festival', re: /(festival|(e|é)v(e|é)nement culturel|cultural event|femua|abissa|carnaval|concert|spectacle|music)/i,
    en: "Côte d'Ivoire hosts dance festivals, concerts, culinary events, traditional celebrations and craft exhibitions all year. The big ones:" + L(["<b>FEMUA</b> — Festival des Musiques Urbaines d'Anoumabo, Abidjan", '<b>Abissa</b> — Grand-Bassam', '<b>Carnaval de Bouaké</b>', 'Traditional festivals around Korhogo']),
    fr: "La Côte d'Ivoire accueille toute l'année festivals de danse, concerts, événements gastronomiques, célébrations traditionnelles et expositions artisanales. Les grands rendez-vous :" + L(["<b>FEMUA</b> — Festival des Musiques Urbaines d'Anoumabo, Abidjan", '<b>Abissa</b> — Grand-Bassam', '<b>Carnaval de Bouaké</b>', 'les festivals traditionnels de Korhogo']) },

  { id: 'artisan', re: /(artisan|craft|village artisanal|artisanat|souvenir|pagne|tissage|masque|mask)/i,
    en: "The <b>artisan village in Cocody</b>, Abidjan, and the <b>craft workshops in Korhogo</b> are the two best known — weaving, painted cloth, carving. Markets and traditional villages are where you'll find the rest.",
    fr: "Le <b>village artisanal de Cocody</b>, à Abidjan, et les <b>ateliers de Korhogo</b> sont les plus réputés — tissage, toiles peintes, sculpture. Les marchés et villages traditionnels complètent le tableau." },

  { id: 'dance', re: /(danse|dance|traditional performance|spectacle traditionnel|folklore)/i,
    en: "Traditional performances and festivals happen across the country, especially in the <b>north and west</b>. We build them into cultural itineraries when the calendar lines up with your dates.",
    fr: "Spectacles et festivals traditionnels sont organisés dans tout le pays, surtout dans le <b>nord et l'ouest</b>. Nous les intégrons aux circuits culturels quand le calendrier correspond à vos dates." },

  { id: 'culture', re: /(culture|cultural|mus(e|é)e|museum|tradition|patrimoine|heritage|village traditionnel)/i,
    en: "You'll find Ivorian culture in artisan markets, museums, traditional villages and the festival calendar. Our Cultural Trips are built around exactly that, with local guides who grew up with the stories.",
    fr: "La culture ivoirienne se découvre dans les marchés artisanaux, les musées, les villages traditionnels et le calendrier des festivals. Nos voyages culturels sont construits là-dessus, avec des guides locaux qui ont grandi avec ces histoires." },

  /* ---------- nature ---------- */
  { id: 'beach', re: /(beach|plage|\bmer\b|ocean|oc(e|é)an|swim|baign|surf|assinie|bassam|sassandra)/i,
    en: "The favourites:" + L(['<b>Assinie</b> — lagoon and Atlantic, surf and boat trips', '<b>Grand-Bassam</b> — UNESCO colonial quarter, an hour from Abidjan', '<b>San Pedro</b>', '<b>Sassandra</b> — fishing port and quiet coves']) + "December to April is the best swimming window.",
    fr: "Les préférées :" + L(["<b>Assinie</b> — lagune et Atlantique, surf et sorties en bateau", "<b>Grand-Bassam</b> — quartier colonial classé UNESCO, à une heure d'Abidjan", '<b>San Pedro</b>', '<b>Sassandra</b> — port de pêche et criques tranquilles']) + "De décembre à avril, c'est la meilleure période pour se baigner." },

  { id: 'park', re: /(parc|park|ta(i|ï)|como(e|é)|banco|r(e|é)serve|reserve|for(e|ê)t|forest|jungle|randonn)/i,
    en: "Three that visitors rate highly:" + L(['<b>Taï National Park</b> — primary rainforest, UNESCO listed', '<b>Comoé National Park</b> — savanna, rivers, birdlife', '<b>Banco National Park</b> — rainforest inside Abidjan itself']),
    fr: "Trois parcs très appréciés :" + L(['<b>le Parc National de Taï</b> — forêt primaire classée UNESCO', '<b>le Parc National de la Comoé</b> — savane, rivières, avifaune', "<b>le Parc du Banco</b> — forêt tropicale à l'intérieur même d'Abidjan"]) },

  { id: 'safari', re: /(safari|wildlife|animaux|(e|é)l(e|é)phant|elephant|faune|monkey|singe|birdwatch)/i,
    en: "Yes — several parks and reserves offer wildlife observation, and the protected areas preserve real biodiversity. It's not East-African-style big-game safari; expect forest primates, birds and, in Comoé, savanna species.",
    fr: "Oui — plusieurs parcs et réserves proposent l'observation de la faune, et les aires protégées préservent une vraie biodiversité. Ce n'est pas le safari « big five » de l'Afrique de l'Est : attendez-vous aux primates de forêt, aux oiseaux et, à la Comoé, aux espèces de savane." },

  { id: 'family', re: /(famil|enfant|kids|children|family[- ]friendly)/i,
    en: "Very much so. Families do beaches, nature excursions, cultural tours, lagoon cruises, craft workshops and food experiences. Tell me the ages and I'll tell you what tends to work.",
    fr: "Tout à fait. Les familles combinent plages, excursions nature, visites culturelles, croisières lagunaires, ateliers artisanaux et découvertes gastronomiques. Dites-moi les âges et je vous dis ce qui fonctionne le mieux." },

  /* ---------- business & événementiel ---------- */
  { id: 'business', re: /(business|conf(e|é)rence|conference|(e|é)v(e|é)nement professionnel|s(e|é)minaire|seminar|congr(e|è)s|convention|salon|\bmice\b|corporate|forum)/i,
    en: "Yes. Abidjan is one of West Africa's leading economic and financial hubs, with modern infrastructure for conferences, exhibitions and international events. Several hotels have venues sized for large professional gatherings, and the city regularly hosts economic forums and international conferences.",
    fr: "Oui. Abidjan est l'un des principaux centres économiques et financiers d'Afrique de l'Ouest, avec des infrastructures modernes pour conférences, salons et événements internationaux. Plusieurs hôtels disposent d'espaces adaptés aux grands rassemblements professionnels, et la ville accueille régulièrement forums économiques et conférences internationales." },

  /* ---------- pratique ---------- */
  { id: 'money', re: /(monnaie|currency|franc|\bcfa\b|\bxof\b|argent|money|change|exchange|carte bancaire|credit card|paiement|payer|\batm\b|distributeur)/i,
    en: "The currency is the <b>West African CFA franc (XOF)</b>. Credit cards are accepted in many hotels, restaurants and modern businesses in the cities — carry cash for markets, taxis and anything outside Abidjan.",
    fr: "La monnaie est le <b>franc CFA (XOF)</b>. Les cartes bancaires sont acceptées dans de nombreux hôtels, restaurants et commerces modernes en ville — prévoyez du liquide pour les marchés, les taxis et tout ce qui est hors d'Abidjan." },

  { id: 'budget', re: /(budget|co(u|û)t|cost|combien (c|ç)a co(u|û)te|how much|price|prix|tarif|expensive|cher|devis|quote)/i,
    en: "It depends entirely on travel style — Côte d'Ivoire works for both budget and high-end travelers. For a Sublime CI-USA trip we quote individually based on length, comfort level and group size: send your dates through the contact form and you get a route and a price within two business days.",
    fr: "Tout dépend du style de voyage — la Côte d'Ivoire convient aussi bien aux petits budgets qu'au haut de gamme. Chez Sublime CI-USA, chaque voyage est chiffré sur mesure selon la durée, le niveau de confort et la taille du groupe : envoyez vos dates via le formulaire, vous recevez un itinéraire et un prix sous deux jours ouvrés." },

  { id: 'language', re: /(langue|language|parle|speak|fran(c|ç)ais|french|english|anglais|dioula|baoul)/i,
    en: "French is the official language, alongside around sixty local languages. English isn't widely spoken in the street, but English-speaking guides are available — all of ours work in English.",
    fr: "Le français est la langue officielle, aux côtés d'une soixantaine de langues locales. L'anglais est peu parlé dans la rue, mais des guides anglophones existent — tous les nôtres travaillent en anglais." },

  { id: 'guide', re: /(guide|english[- ]speaking|tour operator|agence|accompagnateur)/i,
    en: "Yes — several operators and guides work in English, and we can connect you with certified local guides. Ours are Ivorian, and they explain context and etiquette, not just landmarks.",
    fr: "Oui — plusieurs agences et guides travaillent en anglais, et nous pouvons vous orienter vers des guides locaux certifiés. Les nôtres sont ivoiriens, et expliquent le contexte et les usages, pas seulement les monuments." },

  { id: 'internet', re: /(internet|wifi|wi[- ]?fi|\bsim\b|donn(e|é)es mobiles|mobile data|connexion|network|r(e|é)seau|esim)/i,
    en: "Mobile internet and Wi-Fi are widely available in the main cities and tourist areas. A local SIM is cheap and easy to get on arrival — worth doing if you'll be using ride-hailing apps.",
    fr: "Internet mobile et Wi-Fi sont largement disponibles dans les grandes villes et les zones touristiques. Une carte SIM locale est bon marché et facile à obtenir à l'arrivée — utile si vous comptez utiliser les applis VTC." },

  { id: 'plug', re: /(adapt(a|e)teur|adapter|prise|plug|voltage|220|electric|(e|é)lectricit)/i,
    en: "Yes, American visitors need an adapter. Côte d'Ivoire uses <b>type C and E</b> plugs at <b>220V</b> — a standard Europe adapter works, and check that your devices are dual-voltage.",
    fr: "Oui, les visiteurs américains ont besoin d'un adaptateur. La Côte d'Ivoire utilise les prises de <b>type C et E</b> en <b>220V</b> — un adaptateur Europe standard convient, et vérifiez que vos appareils sont bi-tension." },

  { id: 'weather', re: /(climat|climate|m(e|é)t(e|é)o|weather|temp(e|é)rature|pluie|rain|saison|humid|chaud|\bhot\b)/i,
    en: "Tropical, with dry and rainy seasons that vary by region. The south has its main dry season from November to April; the north follows a different rhythm, with rain concentrated between June and September.",
    fr: "Tropical, avec des saisons sèches et pluvieuses variables selon les régions. Le sud connaît sa grande saison sèche de novembre à avril ; le nord suit un autre rythme, avec des pluies concentrées entre juin et septembre." },

  /* ---------- profils voyageurs ---------- */
  { id: 'firsttime', re: /(first (time|trip) (in|to) africa|premi(e|è)re fois en afrique|premier voyage|beginner|d(e|é)butant)/i,
    en: "It's an excellent first stop in West Africa. Modern infrastructure, genuine hospitality and deep culture, without the logistics being difficult. Abidjan plus Grand-Bassam plus one beach makes a very solid first week.",
    fr: "C'est une excellente première étape en Afrique de l'Ouest. Infrastructures modernes, hospitalité réelle et culture profonde, sans logistique compliquée. Abidjan + Grand-Bassam + une plage : voilà une très bonne première semaine." },

  /* ---------- promotion & partenariats ---------- */
  { id: 'package', re: /(package|circuit|forfait|s(e|é)jour organis(e|é)|tour package|offre|promo)/i,
    en: "Yes — cultural, beach, culinary and eco-tourism packages exist through partner agencies, and Sublime CI-USA builds tailor-made itineraries from scratch. Tell me what kind of trip you want and I'll point you to the right one.",
    fr: "Oui — des circuits culturels, balnéaires, gastronomiques et nature sont proposés par des agences partenaires, et Sublime CI-USA construit des itinéraires sur mesure de A à Z. Dites-moi le type de voyage souhaité et je vous oriente." },

  { id: 'brochure', re: /(brochure|documentation|d(e|é)pliant|catalogue|plaquette)/i,
    en: "Brochures are available on the site, at tourism offices and at our promotional events. Ask through the contact form and we'll send the current one.",
    fr: "Les brochures sont disponibles sur le site, dans les offices du tourisme et lors des événements promotionnels. Demandez-la via le formulaire de contact et nous vous envoyons la version en cours." },

  { id: 'partner', re: /(partenariat|partner|collaborat|travailler avec vous|work with you|\bb2b\b|professionnel|press|presse)/i,
    en: "Partners are welcome — agencies, media, event organisers. Use the contact form and mark it as a professional enquiry, and the right person gets back to you.",
    fr: "Les partenaires sont les bienvenus — agences, médias, organisateurs d'événements. Passez par le formulaire de contact en précisant qu'il s'agit d'une demande professionnelle, la bonne personne vous répondra." },

  /* ---------- liens officiels ---------- */
  { id: 'links', re: /(lien|link|site officiel|official (site|website)|url|adresse (du )?site|o(u|ù) (demander|faire) (le |la )?(visa|demande))/i,
    en: "The official sources:" + L([
      "<b>e-Visa</b> — <a href='https://snedai.com/e-visa/' target='_blank' rel='noopener noreferrer'>snedai.com/e-visa</a>, the only accredited government portal. Be wary of intermediaries that add fees.",
      "<b>Ministry of Tourism</b> — <a href='https://www.tourisme.gouv.ci/' target='_blank' rel='noopener noreferrer'>tourisme.gouv.ci</a>",
      "<b>Côte d'Ivoire Tourisme</b> — <a href='https://www.cotedivoiretourisme.ci/' target='_blank' rel='noopener noreferrer'>cotedivoiretourisme.ci</a>",
      "<b>Embassy in Washington, D.C.</b> — <a href='https://ambaciusa.org/' target='_blank' rel='noopener noreferrer'>ambaciusa.org</a>"]),
    fr: "Les sources officielles :" + L([
      "<b>e-Visa</b> — <a href='https://snedai.com/e-visa/' target='_blank' rel='noopener noreferrer'>snedai.com/e-visa</a>, le seul portail gouvernemental accrédité. Méfiez-vous des intermédiaires qui ajoutent des frais.",
      "<b>Ministère du Tourisme</b> — <a href='https://www.tourisme.gouv.ci/' target='_blank' rel='noopener noreferrer'>tourisme.gouv.ci</a>",
      "<b>Côte d'Ivoire Tourisme</b> — <a href='https://www.cotedivoiretourisme.ci/' target='_blank' rel='noopener noreferrer'>cotedivoiretourisme.ci</a>",
      "<b>Ambassade à Washington D.C.</b> — <a href='https://ambaciusa.org/' target='_blank' rel='noopener noreferrer'>ambaciusa.org</a>"]) },

  /* ---------- coordonnées ---------- */
  { id: 'contact', re: /(contact|t(e|é)l(e|é)phone|phone|email|mail|adresse|address|joindre|call|appeler|bureau|office)/i,
    en: "<b>tourism@ambaciusa.org</b> · <b>(240) 756-8332</b><br>2424 Massachusetts Avenue N.W., Washington, D.C. 20008. The contact form on this site reaches the same team.",
    fr: "<b>tourism@ambaciusa.org</b> · <b>(240) 756-8332</b><br>2424 Massachusetts Avenue N.W., Washington D.C. 20008. Le formulaire de contact du site arrive chez la même équipe." }
  ];

  var FALLBACK = {
    en: "That one I don't have yet. Try me on visas, best season, beaches, hotels, food, transport, budget or safety — or write to <b>tourism@ambaciusa.org</b> and a colleague will answer personally.",
    fr: "Celle-là, je ne l'ai pas encore. Essayez visa, meilleure saison, plages, hôtels, cuisine, transport, budget ou sécurité — ou écrivez à <b>tourism@ambaciusa.org</b>, un collègue vous répondra personnellement."
  };

  var QUICK = {
    en: ['Do I need a visa?', 'Best time to visit?', 'Where should I stay?', 'What should I eat?', 'Is it safe?', 'What budget?'],
    fr: ['Faut-il un visa ?', 'Meilleure période ?', 'Où loger ?', 'Que manger ?', 'Est-ce sûr ?', 'Quel budget ?']
  };

  /* ============================================================
     MOTEUR
     ============================================================ */
  function siteLang() { return (document.documentElement.lang === 'fr') ? 'fr' : 'en'; }

  /* bascule automatique si l'internaute écrit dans l'autre langue */
  var FR_HINT = /\b(je|tu|vous|nous|est-ce|quel|quelle|quels|comment|pourquoi|combien|o(u|ù)|faut|besoin|bonjour|merci|dois|c'est|des|une|pour|avec|dans)\b/i;
  var EN_HINT = /\b(i|you|we|the|is|are|do|does|what|where|when|how|why|need|should|can|thanks|hello|with|for)\b/i;

  function detect(text) {
    var fr = (text.match(new RegExp(FR_HINT.source, 'gi')) || []).length;
    var en = (text.match(new RegExp(EN_HINT.source, 'gi')) || []).length;
    if (fr > en) return 'fr';
    if (en > fr) return 'en';
    return siteLang();
  }

  function answer(text) {
    var lang = detect(text);
    for (var i = 0; i < KB.length; i++) {
      if (KB[i].re.test(text)) return KB[i][lang];
    }
    return FALLBACK[lang];
  }

  /* ---------- rendu ---------- */
  function push(role, html, save) {
    if (role !== 'me') {
      /* Aya « parle » le temps de lire son message, environ 45 ms
         par mot, puis revient au repos */
      pose('talk', true);
      var words = html.replace(/<[^>]+>/g, ' ').trim().split(/\s+/).length;
      setTimeout(function () { if (window.Aya) window.Aya.idle(); }, Math.min(4200, 700 + words * 45));
    }
    var d = document.createElement('div');
    d.className = 'msg msg--' + (role === 'me' ? 'me' : 'bot');
    d.innerHTML = html;
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    if (save !== false) {
      history.push({ role: role, html: html });
      try { sessionStorage.setItem(STORE_KEY, JSON.stringify(history.slice(-40))); } catch (e) {}
    }
  }
  function typing(on) {
    if (on) pose('think', true); 
    var t = log.querySelector('.typing');
    if (on && !t) {
      t = document.createElement('div');
      t.className = 'typing';
      t.innerHTML = '<i></i><i></i><i></i>';
      log.appendChild(t);
      log.scrollTop = log.scrollHeight;
    } else if (!on && t) { t.remove(); }
  }
  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }
  function renderQuick() {
    var list = QUICK[siteLang()];
    quick.innerHTML = '';
    list.forEach(function (q) {
      var b = document.createElement('button');
      b.type = 'button'; b.textContent = q;
      b.addEventListener('click', function () { ask(q); });
      quick.appendChild(b);
    });
  }

  /* ---------- envoi ---------- */
  function ask(text) {
    text = (text || '').trim();
    if (!text) return;
    push('me', escapeHtml(text));
    input.value = '';
    typing(true);

    if (USE_API) {
      fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history: history.slice(-10), lang: detect(text) })
      })
        .then(function (r) { return r.json(); })
        .then(function (d) { typing(false); push('bot', d.reply || answer(text)); })
        .catch(function () { typing(false); push('bot', answer(text)); });
    } else {
      /* délai proportionnel à la longueur : Aya écrit, elle ne
         récite pas une base de données */
      var reply = answer(text);
      setTimeout(function () { typing(false); push('bot', reply); },
                 Math.min(1700, 520 + reply.length * 2.2));
    }
  }

  /* ---------- ouverture / fermeture ---------- */
  function open(v) {
    panel.classList.toggle('on', v);
    btn.classList.toggle('hidden', v);
    if (v) {
      if (!log.children.length) {
        if (history.length) history.forEach(function (m) { push(m.role, m.html, false); });
        else push('bot', KB[1][siteLang()], false);
      }
      renderQuick();
      if (window.Aya) window.Aya.stopAttract();
      setTimeout(function () { pose('wave'); }, 260);
      setTimeout(function () { input.focus(); }, 320);
    } else {
      pose('idle');
    }
  }
  btn.addEventListener('click', function () { open(true); });
  close.addEventListener('click', function () { open(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel.classList.contains('on')) open(false);
  });

  send.addEventListener('click', function () { ask(input.value); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') ask(input.value); });

  renderQuick();
})();
