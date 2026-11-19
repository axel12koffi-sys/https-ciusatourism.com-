#!/usr/bin/env bash
# Télécharge en local toutes les images encore hébergées sur le WordPress actuel.
# À lancer UNE FOIS, depuis la racine du projet, tant que ciusatourism.com est
# toujours en ligne. Ensuite le site n'a plus aucune dépendance externe.
#   chmod +x tools/download-images.sh && ./tools/download-images.sh
set -u
cd "$(dirname "$0")/.." || exit 1
mkdir -p assets/img
ok=0; ko=0
dl() {
  if [ -s "assets/img/$2" ]; then echo "  = $2"; ok=$((ok+1)); return; fi
  if curl -fsSL --retry 2 --max-time 30 -o "assets/img/$2" "$1"; then
    echo "  + $2"; ok=$((ok+1))
  else
    rm -f "assets/img/$2"; echo "  ! ÉCHEC $1"; ko=$((ko+1))
  fi
}

dl "https://ciusatourism.com/wp-content/uploads/2025/03/81e292_c66c8f5254b443deb9a91931a77e7705mv2.avif" "202503-81e292_c66c8f5254b443deb9a91931a77e7705mv2.avif"
dl "https://ciusatourism.com/wp-content/uploads/2025/03/caption-768x536.jpg" "202503-caption-768x536.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2025/03/image-AM-423-424-page-72-73_0-1024x649.jpg" "202503-image-AM-423-424-page-72-73_0-1024x649.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2025/04/caption.jpg" "202504-caption.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2025/05/1.png" "202505-1.png"
dl "https://ciusatourism.com/wp-content/uploads/2025/05/2.png" "202505-2.png"
dl "https://ciusatourism.com/wp-content/uploads/2025/05/3.png" "202505-3.png"
dl "https://ciusatourism.com/wp-content/uploads/2025/05/4.png" "202505-4.png"
dl "https://ciusatourism.com/wp-content/uploads/2025/05/6.png" "202505-6.png"
dl "https://ciusatourism.com/wp-content/uploads/2025/05/7.png" "202505-7.png"
dl "https://ciusatourism.com/wp-content/uploads/2025/05/Baaba_Mal_au_Femua_15_jour4_19-768x512.jpg" "202505-Baaba_Mal_au_Femua_15_jour4_19-768x512.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2025/05/Baaba_Mal_au_Femua_15_jour4_19-scaled.jpg" "202505-Baaba_Mal_au_Femua_15_jour4_19-scaled.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2025/07/518962291_1174462791381517_2182541855198391979_n.jpg" "202507-518962291_1174462791381517_2182541855198391979_n.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2025/09/telechargement-1.png" "202509-telechargement-1.png"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/Abidjan-Luxury-1536x1024-1-1024x683.webp" "202511-Abidjan-Luxury-1536x1024-1-1024x683.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/aja_p_4555-01_4by3-1024x767.webp" "202511-aja_p_4555-01_4by3-1024x767.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/telechargement-3.webp" "202511-telechargement-3.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/telechargement-4.webp" "202511-telechargement-4.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/telechargement-5-1.webp" "202511-telechargement-5-1.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/telechargement-7.webp" "202511-telechargement-7.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/telechargement-8.webp" "202511-telechargement-8.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/telechargement-9.webp" "202511-telechargement-9.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/11/telechargement.webp" "202511-telechargement.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-10.webp" "202512-telechargement-10.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-11.webp" "202512-telechargement-11.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-12.webp" "202512-telechargement-12.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-13.webp" "202512-telechargement-13.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-14.webp" "202512-telechargement-14.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-15.webp" "202512-telechargement-15.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-18.webp" "202512-telechargement-18.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-19.webp" "202512-telechargement-19.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-20.webp" "202512-telechargement-20.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-21.webp" "202512-telechargement-21.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-22.webp" "202512-telechargement-22.webp"
dl "https://ciusatourism.com/wp-content/uploads/2025/12/telechargement-23.webp" "202512-telechargement-23.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/1.jpg" "202601-1.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/2.jpg" "202601-2.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/20980.webp" "202601-20980.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/3.jpg" "202601-3.jpg"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/66363a80a941c086eadfd60f_logo_white.svg" "202601-66363a80a941c086eadfd60f_logo_white.svg"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/8aa4d1f60de468d00fdce0b58108857c-1536x636-1-1024x424.webp" "202601-8aa4d1f60de468d00fdce0b58108857c-1536x636-1-1024x424.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/ARTHUR.webp" "202601-ARTHUR.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/BISTRO.webp" "202601-BISTRO.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/CHEZ-GORGE.webp" "202601-CHEZ-GORGE.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/COCO.webp" "202601-COCO.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/CROISSTE.webp" "202601-CROISSTE.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/DEBARC.webp" "202601-DEBARC.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/GRAND-LARGE.webp" "202601-GRAND-LARGE.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/KAJI.webp" "202601-KAJI.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/KAMA.webp" "202601-KAMA.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/LA-VILLA.webp" "202601-LA-VILLA.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/LE-JARDIN.webp" "202601-LE-JARDIN.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/LIVA.webp" "202601-LIVA.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/MICHOUI.webp" "202601-MICHOUI.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/MONT-PA.webp" "202601-MONT-PA.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/NORI.webp" "202601-NORI.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/NUIT.webp" "202601-NUIT.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/PARENT.webp" "202601-PARENT.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/REGINA.webp" "202601-REGINA.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/RESTAURANT-LANG.webp" "202601-RESTAURANT-LANG.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/RICHARD.webp" "202601-RICHARD.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/ROUTE-DE-VIN.webp" "202601-ROUTE-DE-VIN.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/ROXY.webp" "202601-ROXY.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/SAAK.webp" "202601-SAAK.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/TAVERN.webp" "202601-TAVERN.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/TOIT-D.webp" "202601-TOIT-D.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/VILLA-SOV.webp" "202601-VILLA-SOV.webp"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/logo-300x68.png" "202601-logo-300x68.png"
dl "https://ciusatourism.com/wp-content/uploads/2026/01/yango-logo-brandlogos.net_zfi74ddhl.svg" "202601-yango-logo-brandlogos.net_zfi74ddhl.svg"

echo ""
echo "$ok téléchargées, $ko en échec."
[ "$ko" -gt 0 ] && echo "Récupère les manquantes à la main dans cPanel > Gestionnaire de fichiers > wp-content/uploads."
exit 0
