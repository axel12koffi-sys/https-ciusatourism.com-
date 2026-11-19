#!/usr/bin/env bash
# Génère les deux versions du site : en/ et fr/
cd "$(dirname "$0")" || exit 1
set -e
CIUSA_LANG=en python3 build.py --lang
CIUSA_LANG=fr python3 build.py --lang
echo
echo "Site bilingue prêt. Racine : index.html redirige selon la langue du navigateur."
