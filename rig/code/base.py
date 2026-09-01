# rig/code/base.py

import shlex


def afficher_menu_base(chemin, entrees):
    print(chemin)
    for commande, libelle in entrees:
        print(commande + " -- " + libelle)


def afficher_aide_base(titre, entrees):
    print(titre)
    for commande, description in entrees:
        print(commande + " -- " + description)


def decouper_commande_base(ligne):
    try:
        return shlex.split(ligne)
    except ValueError:
        return []


def obtenir_commande_base(ligne):
    parties = decouper_commande_base(ligne)

    if not parties:
        return ""

    return parties[0]


def boucle_base(invite, menu, gestionnaires, commande_sortie="x"):
    menu()

    while True:
        ligne = input(invite).strip()
        parties = decouper_commande_base(ligne)

        if not parties:
            continue

        commande = parties[0]

        if commande == commande_sortie:
            return 0

        gestionnaire = gestionnaires.get(commande)

        if gestionnaire is None:
            continue

        code = gestionnaire(parties[1:])

        if code is not None and code != 0:
            return code