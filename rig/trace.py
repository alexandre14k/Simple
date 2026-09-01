# rig/trace.py

import traceback

import base
import code
import menu


def trace_afficher_exception(exception):
    cadre = exception.__traceback__
    cadres = []

    while cadre is not None:
        cadres.append(cadre.tb_frame)
        cadre = cadre.tb_next

    for index, cadre in enumerate(cadres):
        chemin = cadre.f_code.co_filename
        nom = cadre.f_code.co_name
        ligne = cadre.f_lineno

        if index == len(cadres) - 1:
            print(
                "#"
                + str(index)
                + " -- "
                + trace_obtenir_chemin(chemin)
                + ":"
                + str(ligne)
                + " in "
                + nom
            )
        else:
            print(
                "#"
                + str(index)
                + " -- "
                + trace_obtenir_chemin(chemin)
                + ":"
                + str(ligne)
            )

    dernier = cadres[-1]

    try:
        ligne_source = traceback.extract_tb(
            exception.__traceback__
        )[-1]

        if ligne_source.line:
            print(
                "    "
                + ligne_source.line.strip()
            )

            if (
                ligne_source.colno is not None
                and ligne_source.end_colno is not None
            ):
                largeur = max(
                    0,
                    ligne_source.colno,
                )

                longueur = max(
                    1,
                    ligne_source.end_colno - ligne_source.colno,
                )

                print(
                    "    "
                    + " " * largeur
                    + "^" * longueur
                )
    except (IndexError, AttributeError):
        pass

    print(
        type(exception).__name__
        + ": "
        + str(exception)
    )


def trace_obtenir_chemin(chemin):
    try:
        import helper

        return (
            chemin
            .replace(
                helper.obtenir_repertoire_racine() + "/",
                "",
            )
            .replace("\\", "/")
        )
    except Exception:
        return chemin.replace("\\", "/")


def afficher_menu_trace():
    menu.afficher_gabarit_menu(
        "run>rig>debug",
        [
            ("c", "entrer dans le code"),
        ],
    )


def trace_entrer_code(args):
    if args:
        print("usage: c")
        return 0

    return code.code_principal()


def trace_distribuer(commande, args):
    if commande == "c":
        return trace_entrer_code(args)

    print("commande inconnue : " + commande)
    return 0


def trace_session():
    return menu.session_gabarit_menu(
        "debug> ",
        afficher_menu_trace,
        trace_distribuer,
        base.decouper_commande_base,
    )


def trace_main():
    return trace_session()


if __name__ == "__main__":
    trace_main()