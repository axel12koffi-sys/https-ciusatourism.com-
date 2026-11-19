# -*- coding: utf-8 -*-
"""Bascule de langue du générateur.

Les gabarits écrivent t("English text", "Texte français").
build.py fixe LANG puis génère une fois par langue, dans en/ et fr/.
"""

LANG = 'en'
LANGS = ('en', 'fr')
LABEL = {'en': 'English', 'fr': 'Français'}


def set_lang(code):
    global LANG
    LANG = code


def t(en, fr):
    """Choisit la variante selon la langue courante."""
    return fr if LANG == 'fr' else en


def pick(pair):
    """Idem, pour un tuple (en, fr) déjà constitué."""
    return pair[1] if LANG == 'fr' else pair[0]


def other():
    return 'fr' if LANG == 'en' else 'en'
