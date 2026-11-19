#!/usr/bin/env bash
# Importe les images depuis un dossier "uploads" récupéré à la main
# (cPanel > Gestionnaire de fichiers > wp-content > uploads > Compresser,
#  puis téléchargement du zip et décompression sur ton poste).
#
# Aplatit l'arborescence AAAA/MM/fichier.ext en AAAAMM-fichier.ext,
# qui est le nommage attendu par les pages.
#
# Usage :  ./tools/import-uploads.sh ~/Téléchargements/uploads
#
# Aucun serveur, aucune connexion : c'est de la copie de fichiers.

set -u
cd "$(dirname "$0")/.." || exit 1

SRC="${1:-}"
if [ -z "$SRC" ] || [ ! -d "$SRC" ]; then
  echo "Usage : ./tools/import-uploads.sh /chemin/vers/uploads"
  echo "Le dossier doit contenir des sous-dossiers du type 2025/03/."
  exit 1
fi

mkdir -p assets/img
n=0

# on ne garde que les années/mois, on ignore les miniatures WordPress
find "$SRC" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
     -o -iname '*.webp' -o -iname '*.avif' -o -iname '*.svg' \) | while read -r f; do
  rel="${f#$SRC/}"                       # 2025/03/photo.jpg
  year="$(echo "$rel"  | cut -d/ -f1)"
  month="$(echo "$rel" | cut -d/ -f2)"
  name="$(basename "$rel")"

  case "$year" in
    [0-9][0-9][0-9][0-9]) ;;             # on attend une année
    *) continue ;;
  esac

  cp "$f" "assets/img/${year}${month}-${name}"
  n=$((n+1))
  echo "  + ${year}${month}-${name}"
done

echo ""
echo "Fichiers dans assets/img/ : $(find assets/img -type f | wc -l | tr -d ' ')"
echo "Les pages en attendent 69. Si le compte n'y est pas, lance :"
echo "  grep -oh 'assets/img/[^\"]*' *.html | sort -u"
echo "pour voir lesquelles manquent."
