# rig/code/filter.py

import re


MOTIF_ANSI = re.compile(r"\x1b\[[0-9;]*m")

MOTIF_DEMARRAGE_GDB = re.compile(
    r"^Starting program: "
)

MOTIF_THREAD_GDB = re.compile(
    r"^Using host libthread_db library "
)


def filtrer_ligne_code(ligne):
    ligne = ligne.rstrip()

    if not ligne:
        return None

    if ligne == "(gdb)":
        return None

    if MOTIF_DEMARRAGE_GDB.match(ligne):
        return None

    if MOTIF_THREAD_GDB.match(ligne):
        return None

    if ligne.startswith(
        "[Thread debugging using libthread_db enabled]"
    ):
        return None

    return ligne


def filtrer_sortie_code(sortie):
    if not sortie:
        return ""

    sortie = MOTIF_ANSI.sub(
        "",
        sortie,
    )

    resultat = []

    for ligne in sortie.splitlines():
        ligne_propre = filtrer_ligne_code(
            ligne
        )

        if ligne_propre is not None:
            resultat.append(
                ligne_propre
            )

    return "\n".join(resultat)


def afficher_sortie_code(sortie):
    resultat = filtrer_sortie_code(
        sortie
    )

    if not resultat:
        return

    print(
        resultat,
        flush=True,
    )