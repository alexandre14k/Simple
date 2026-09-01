# rig/strip.py

import re


MOTIF_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def strip_retirer_codes_ansi(texte):
    return MOTIF_ANSI.sub("", texte)


def strip_nettoyer_ligne(ligne):
    return strip_retirer_codes_ansi(ligne).rstrip()


def strip_nettoyer_bloc(bloc):
    if not bloc:
        return []

    resultat = []

    for ligne in bloc.splitlines():
        ligne = strip_nettoyer_ligne(ligne)

        if ligne:
            resultat.append(ligne)

    return resultat