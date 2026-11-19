# -*- coding: utf-8 -*-
"""Chemins d'images.

Les gabarits écrivent toujours l'URL du WordPress actuel ; la réécriture
vers assets/img/ se fait à l'écriture des pages, via localize().

LOCAL_IMG = True  -> assets/img/AAAAMM-fichier.ext (production : le site
                     n'a plus aucune dépendance vers l'ancien WordPress)
LOCAL_IMG = False -> on garde les URLs distantes (pratique tant que les
                     images ne sont pas rapatriées)

Lancer tools/download-images.sh une fois pour remplir assets/img/.
"""
import re

LOCAL_IMG = True
REMOTE = "https://ciusatourism.com/wp-content/uploads"
IMG = REMOTE

_RE = re.compile(re.escape(REMOTE) + r'/(\d{4})/(\d{2})/([^"\'\)\s]+)')


def localize(html):
    if not LOCAL_IMG:
        return html
    return _RE.sub(lambda m: f"assets/img/{m.group(1)}{m.group(2)}-{m.group(3)}", html)


# ------------------------------------------------------------------
# URLs propres : destinations.html -> destinations
# Nécessite mod_rewrite (bloc 2 du .htaccess). Mets CLEAN_URLS = False
# si ton hébergeur ne le supporte pas.
# ------------------------------------------------------------------
CLEAN_URLS = True

_HREF = re.compile(r'(href=")(?!https?:|mailto:|tel:|#|/)([A-Za-z0-9._-]+)\.html((?:#[^"]*)?)"')


def clean_links(html):
    if not CLEAN_URLS:
        return html
    def sub(m):
        page = m.group(2)
        target = './' if page == 'index' else page
        return f'{m.group(1)}{target}{m.group(3)}"'
    return _HREF.sub(sub, html)
