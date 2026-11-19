#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importe les photos de destination dans le site.

Prend un dossier de photos nommées par identifiant de lieu, les recadre
en 4:3, les redimensionne, les convertit en WebP et les installe dans
assets/img/dest/ — où le générateur les préfère automatiquement aux
visuels de remplacement.

    python3 tools/import-photos.py ~/photos-destinations

Les fichiers doivent porter le nom de l'identifiant, quelle que soit
l'extension : grand-bassam.jpg, tai.png, abidjan.webp…
Les noms acceptés sont listés plus bas ; tout autre nom est signalé.

Options :
    --width 1400     largeur de sortie (défaut 1200)
    --keep-jpg       garde aussi une version .jpg de secours
    --dry-run        montre ce qui serait fait, sans rien écrire
"""

import argparse
import pathlib
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow est requis :  pip install Pillow")

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = ROOT / 'assets' / 'img' / 'dest'

# identifiants attendus, groupés comme sur le site
SLOTS = {
    'Lieux — littoral': ['grand-bassam', 'assinie', 'sassandra', 'san-pedro',
                         'jacqueville', 'grand-lahou'],
    'Lieux — culture': ['yamoussoukro', 'korhogo', 'man', 'abidjan',
                        'bouake', 'tiegba'],
    'Lieux — nature': ['tai', 'comoe', 'banco', 'ehotile', 'nimba'],
    'Cartes de catégorie': ['cat-beach', 'cat-culture', 'cat-eco'],
    'Diaporama d\'accueil': ['hero-1', 'hero-2', 'hero-3'],
    'Blog': ['blog-culture', 'blog-gastronomy', 'blog-coast', 'blog-city',
             'blog-nature', 'blog-passport'],
    'Bons plans': ['deal-hotel', 'deal-food', 'deal-transport'],
    'Divers': ['gallery'],
}
KNOWN = {s for group in SLOTS.values() for s in group}
EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP')


def crop_43(im):
    """Recadre au centre en 4:3, sans déformer."""
    w, h = im.size
    target = 4 / 3
    if abs(w / h - target) < 0.01:
        return im
    if w / h > target:                      # trop large : on rogne les côtés
        new_w = round(h * target)
        x = (w - new_w) // 2
        return im.crop((x, 0, x + new_w, h))
    new_h = round(w / target)               # trop haut : on rogne haut et bas
    y = (h - new_h) // 3                    # un tiers/deux tiers : le ciel
    return im.crop((0, y, w, y + new_h))    # compte moins que le sujet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', help='dossier contenant les photos')
    ap.add_argument('--width', type=int, default=1200)
    ap.add_argument('--keep-jpg', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    src = pathlib.Path(a.source).expanduser()
    if not src.is_dir():
        sys.exit(f"Dossier introuvable : {src}")

    files = [f for f in sorted(src.iterdir()) if f.suffix in EXTS]
    if not files:
        sys.exit(f"Aucune image dans {src}")

    DEST.mkdir(parents=True, exist_ok=True)
    done, unknown, errors, small = [], [], [], []

    for f in files:
        slug = f.stem.lower().strip()
        if slug not in KNOWN:
            unknown.append(f.name)
            continue
        try:
            im = Image.open(f).convert('RGB')
        except Exception as e:
            errors.append(f'{f.name} : {e}')
            continue

        im = crop_43(im)
        # on n'agrandit jamais : une image étirée est pire que floue,
        # elle est visiblement dégradée. On garde la taille native.
        width = min(a.width, im.width)
        if width < a.width:
            small.append(f'{f.name} ({im.width} px, il en faudrait {a.width})')
        h = round(width * 3 / 4)
        im = im.resize((width, h), Image.LANCZOS)

        if a.dry_run:
            done.append(f'{slug}  ({f.name} → {width}×{h})')
            continue

        im.save(DEST / f'{slug}.webp', quality=82, method=6)
        if a.keep_jpg:
            im.save(DEST / f'{slug}.jpg', quality=82,
                    optimize=True, progressive=True)
        kb = (DEST / f'{slug}.webp').stat().st_size // 1024
        done.append(f'{slug}  ({width}×{h}, {kb} ko)')

    print(f"\n{'(simulation) ' if a.dry_run else ''}"
          f"{len(done)} photo(s) installée(s)")
    for d in done:
        print('  +', d)

    if unknown:
        print(f"\n{len(unknown)} fichier(s) au nom non reconnu, ignoré(s) :")
        for u in unknown:
            print('  ?', u)
        print("  Renomme-les avec l'un des identifiants attendus.")

    if small:
        print(f"\n{len(small)} image(s) trop petite(s) — elles paraîtront floues :")
        for x in small:
            print('  ⚠', x)
        print("  Redemande les originaux : ce sont probablement des vignettes.")

    if errors:
        print(f"\n{len(errors)} erreur(s) :")
        for e in errors:
            print('  !', e)

    # ce qui manque encore
    have = {p.stem for p in DEST.glob('*') if p.suffix in ('.webp', '.jpg', '.png')}
    print("\n--- État des emplacements ---")
    for group, slugs in SLOTS.items():
        miss = [s for s in slugs if s not in have]
        state = 'complet' if not miss else f"manque : {', '.join(miss)}"
        print(f'  {group:24} {state}')

    if not a.dry_run and done:
        print("\nRelance maintenant :  python3 build.py")


if __name__ == '__main__':
    main()
