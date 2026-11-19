# -*- coding: utf-8 -*-
# Données extraites de ciusatourism.com/index.php/{hotel,gastronomies,transport}
# Champ "warn" = coordonnées manifestement dupliquées d'une autre fiche sur le
# site actuel : affichées comme "à confirmer" plutôt que reprises telles quelles.

from paths import IMG as U

HOTELS = [
 # nom, zone(filtre), capacité, téléphones, email, localisation, image, warn
 ("Sofitel Abidjan Hôtel Ivoire","cocody","392","+225 27 22 48 26 26","sofitel.abidjan@sofitel.com","Cocody, Boulevard Hassan II",f"{U}/2025/11/aja_p_4555-01_4by3-1024x767.webp",0),
 ("La Maison Palmier","cocody","74","+225 27 22 22 00 00 · +225 07 57 33 73 16","infos.palmier@lamaisonpalmier.com","II Plateaux, Cocody",f"{U}/2025/11/telechargement.webp",0),
 ("Hôtel and Luxury Housing","cocody","9","+225 27 22 41 41 71","info@abidjanluxury.com","Cocody",f"{U}/2025/11/Abidjan-Luxury-1536x1024-1-1024x683.webp",0),
 ("Palm Club","cocody","88","+225 05 56 09 69 46","commercial@hotelpalmclub.ci","Cocody, Lycée technique",f"{U}/2025/11/Abidjan-Luxury-1536x1024-1-1024x683.webp",0),
 ("Robert's Hôtel","cocody","74","+225 27 22 44 55 55 · +225 27 22 44 06 76 · +225 07 59 96 61 10","hotelhorizon@hotmail.com","Cocody, Lycée Sainte-Marie",f"{U}/2025/11/telechargement-3.webp",0),
 ("Capitol Hôtel","cocody","61","+225 01 41 69 94 94 · +225 07 89 22 28 88","","Cocody, Riviera Golf",f"{U}/2025/11/telechargement-4.webp",0),
 ("Radisson Blu","portbouet","—","+225 27 21 22 20 15","mne.abidjan@radissonblu.com","Port-Bouët, aéroport",f"{U}/2025/11/telechargement-5-1.webp",0),
 ("520 Hôtel & Résidence","portbouet","32","+225 07 69 95 68 52 · +225 27 24 33 88 43","commercial@520hotel.ci","Port-Bouët, Anani carrefour Akissi Delta",f"{U}/2025/12/telechargement-23.webp",0),
 ("Hôtel Azalaï","marcory","200","+225 27 21 22 25 55 · +225 07 79 66 40 05","reservationaha@azalaihotels.com","Marcory, Boulevard FHB (ex VGE)",f"{U}/2025/11/telechargement-7.webp",0),
 ("Adagio Appart'hôtel","marcory","110","+225 27 21 71 10 00 · +225 07 18 83 73 17","hb1j6@accor.com","Marcory, Boulevard FHB (ex VGE)",f"{U}/2025/11/telechargement-8.webp",0),
 ("Novotel Abidjan Marcory","marcory","201","+225 27 21 71 00 01","hb1i4@accor.com","Marcory, Boulevard FHB (ex VGE)",f"{U}/2025/11/telechargement-9.webp",0),
 ("Aichti Hôtel","marcory","57","+225 07 77 00 21 21","reservation@aichtihotel.ci","Marcory, Boulevard FHB (ex VGE)",f"{U}/2025/11/telechargement-5-1.webp",0),
 ("Hôtel Byblos","marcory","58","+225 07 07 20 05 55 · +225 27 21 71 05 00","info@bybloshotelci.com","Marcory, Zone 4",f"{U}/2025/12/telechargement-10.webp",0),
 ("L'Avenue Hôtel Apartments","marcory","50","+225 05 44 45 55 51 · +225 07 00 04 04 20","lavenue@lavenueabidjan.com","Marcory, Zone 4",f"{U}/2025/12/telechargement-11.webp",0),
 ("Ibis Marcory","marcory","—","","","Marcory",f"{U}/2025/12/telechargement-12.webp",1),
 ("Pullman Abidjan","plateau","265","+225 27 20 22 11 22 · +225 27 20 30 20 20","abidjan.reservation@accor.com","Plateau",f"{U}/2025/12/telechargement-14.webp",0),
 ("Hôtel Mövenpick","plateau","160","+225 27 20 23 20 23","hotel.abidjan@movenpick.com","Plateau, avenue Terrasson de Fougères",f"{U}/2025/12/telechargement-15.webp",0),
 ("Hôtel Tiama","plateau","150","+225 27 20 31 33 33 · +225 27 20 31 32 32","reservation.tiama@gmail.com","Plateau",f"{U}/2025/12/telechargement-13.webp",0),
 ("Seen Hôtel","plateau","150","+225 27 20 00 67 06 · +225 07 76 99 98 06","emeraude.kouassi@seenhotels.com","Plateau",f"{U}/2025/12/telechargement-18.webp",0),
 ("Novotel Plateau","plateau","—","","","Plateau",f"{U}/2025/12/telechargement-19.webp",1),
 ("Ibis Plateau","plateau","—","","","Plateau",f"{U}/2025/12/telechargement-20.webp",1),
 ("Grand Hôtel","plateau","—","","","Plateau",f"{U}/2025/12/telechargement-22.webp",1),
 ("Ivotel Hôtel","plateau","—","","","Plateau",f"{U}/2025/12/telechargement-21.webp",1),
]

RESTOS = [
 # nom, zone, téléphone, localisation, image, warn
 ("Saakan","plateau","+225 07 58 55 47 63","Plateau, avenue Chardy, en face de l'AIP, à la descente de Radio Nostalgie",f"{U}/2026/01/SAAK.webp",0),
 ("Chez Georges","plateau","+225 27 20 32 19 89","Plateau, rue du Commerce",f"{U}/2026/01/CHEZ-GORGE.webp",0),
 ("La Croisette","plateau","+225 27 20 21 27 86","Plateau, rue Botreau-Roussel",f"{U}/2026/01/CROISSTE.webp",0),
 ("Le Toit d'Abidjan","plateau","+225 27 22 48 26 26","Boulevard Hassan II, 08 BP 01",f"{U}/2026/01/TOIT-D.webp",0),
 ("Le Jardin","plateau","+225 27 20 21 89 51","8 boulevard Hassan II",f"{U}/2026/01/LE-JARDIN.webp",0),
 ("La Taverne Romaine","plateau","+225 27 20 21 89 51","Boulevard Lagunaire, à côté de l'hôtel Pullman",f"{U}/2026/01/TAVERN.webp",0),
 ("Norima","cocody","+225 27 22 51 03 14","Deux Plateaux Les Vallons, rue Claire Fontaine",f"{U}/2026/01/NORI.webp",0),
 ("Le Bistrot Palmier","cocody","+225 27 22 22 00 00","Rue des Jardins x carrefour Duncan, II Plateaux — BP 4387",f"{U}/2026/01/BISTRO.webp",0),
 ("Regina Margherita","cocody","+225 27 22 46 40 69","Deux Plateaux, carrefour Duncan",f"{U}/2026/01/REGINA.webp",0),
 ("Kamandjè","cocody","+225 07 07 43 01 63","Rue de l'Université, Cocody Cité des Arts, intersection boulevard Booker Washington",f"{U}/2026/01/KAMA.webp",0),
 ("Nuit de Saigon","cocody","+225 27 20 41 40 44","Rue des Jardins, Deux Plateaux carrefour Attoban",f"{U}/2026/01/NUIT.webp",0),
 ("Kajazoma Restaurant-Art","cocody","+225 27 22 41 78 62","Deux Plateaux, boulevard Latrille",f"{U}/2026/01/KAJI.webp",0),
 ("Roxy Lounge","cocody","+225 07 10 60 63 23","Deux Plateaux Vallon, station Corlay, Cocody",f"{U}/2026/01/ROXY.webp",0),
 ("La Route des Vins","cocody","+225 27 22 41 78 62","Deux Plateaux, boulevard Latrille",f"{U}/2026/01/ROUTE-DE-VIN.webp",1),
 ("Parenthèse","zone4","+225 27 20 00 15 00","Rue du Canal, Zone 4",f"{U}/2026/01/PARENT.webp",0),
 ("Le Méchoui","zone4","+225 27 07 98 52 99","Athlétic Club, boulevard de Marseille, Zone 4 Marcory",f"{U}/2026/01/MICHOUI.webp",0),
 ("Montparnasse","zone4","+225 27 21 34 35 01","Rue Pierre et Marie Curie, Zone 4",f"{U}/2026/01/MONT-PA.webp",0),
 ("La Villa di Sorrento","zone4","+225 05 56 34 49 52","Boulevard de Marseille",f"{U}/2026/01/LA-VILLA.webp",0),
 ("Villa Savoia","zone4","+225 27 21 35 86 03","Boulevard de Marseille, derrière la Pergola",f"{U}/2026/01/VILLA-SOV.webp",0),
 ("Le Grand Large","zone4","+225 07 48 00 00 00","149 boulevard de Marseille",f"{U}/2026/01/GRAND-LARGE.webp",0),
 ("Restaurant Liva","zone4","","Marcory Zone 4",f"{U}/2026/01/LIVA.webp",1),
 ("Le Débarcadère","autre","+225 01 02 04 81 50","Avenue Christiani, Treichville Centre",f"{U}/2026/01/DEBARC.webp",0),
 ("Coconut Grove","autre","+225 27 07 07 05 10","Île Boulay",f"{U}/2026/01/COCO.webp",0),
 ("La Langouste chez Cakpo","autre","+225 27 21 71 10 10","Abidjan",f"{U}/2026/01/RESTAURANT-LANG.webp",0),
 ("Chez Arthur","autre","+225 05 05 92 67 55","Abidjan",f"{U}/2026/01/ARTHUR.webp",0),
 ("Richard's","autre","","Abidjan",f"{U}/2026/01/RICHARD.webp",1),
]

VTC = [
 ("Yango","An international platform, simple and widely available, operating in Abidjan and other cities such as Bouaké.",
  "https://yango.com/fr_ci/rider/calltaxi/","Open Yango",f"{U}/2026/01/yango-logo-brandlogos.net_zfi74ddhl.svg"),
 ("Uber","The global ride-hailing leader is also present on the Ivorian market, mainly in Abidjan.",
  "https://www.uber.com/global/fr/r/cities/abidjan-abidjan-ci/","Order an Uber",f"{U}/2026/01/8aa4d1f60de468d00fdce0b58108857c-1536x636-1-1024x424.webp"),
 ("Heetch","Another popular ride-hailing app, well suited to evenings, weekends and city trips.",
  "https://www.heetch.com/","Open Heetch",f"{U}/2026/01/66363a80a941c086eadfd60f_logo_white.svg"),
]
