# rig/menu.py

import base
import combine
import helper
import updown


def formater_chemin_menu(elements):
    return ">".join(elements)


def construire_entrees_menu(entrees):
    completes = list(entrees)

    completes.append(
        ("m", "afficher menu")
    )

    completes.append(
        ("k", "effacer affichage")
    )

    completes.append(
        ("x", "quitter")
    )

    return completes


def afficher_gabarit_menu(
    chemin,
    entrees
):
    print(chemin)

    for commande, libelle in (
        construire_entrees_menu(
            entrees
        )
    ):
        print(
            commande
            + " -- "
            + libelle
        )


def distribuer_base_menu(
    commande,
    args,
    gestionnaire_menu
):
    if commande == "m":
        if args:
            print("usage: m")
            return 0

        gestionnaire_menu()

        return 0

    if commande == "k":
        if args:
            print("usage: k")
            return 0

        return helper.effacer_ecran()

    if commande == "x":
        if args:
            print("usage: x")
            return 0

        return 1

    return None


def session_gabarit_menu(
    invite,
    gestionnaire_menu,
    distribuer,
    decouper,
):
    historique = []

    gestionnaire_menu()

    while True:
        ligne = updown.updown_lire(
            invite,
            historique
        ).strip()

        if not ligne:
            continue

        historique.append(
            ligne
        )

        commandes = combine.combine_decouper(
            ligne
        )

        for commande_ligne in commandes:
            parties = decouper(
                commande_ligne
            )

            if not parties:
                continue

            commande = parties[0]
            args = parties[1:]

            resultat = (
                distribuer_base_menu(
                    commande,
                    args,
                    gestionnaire_menu,
                )
            )

            if resultat is None:
                try:
                    resultat = distribuer(
                        commande,
                        args,
                    )
                except Exception as exception:
                    import trace

                    print()

                    trace.trace_afficher_exception(
                        exception
                    )

                    print()

                    resultat = 0

            if resultat == 1:
                return 0

            if resultat != 0:
                return resultat