# rig/rig.py
import os

import app
import base
import build
import clean
import debug
import ext
import helper
import menu
import pack


def afficher_menu_rig():
    menu.afficher_gabarit_menu(
        "run>rig",
        [
            ("e", "submenu ext"),
            ("b", "submenu build"),
            ("c", "exec clean"),
            ("r", "exec app"),
            ("d", "submenu debug"),
            ("p", "submenu pack"),
            ("s", "stats"),
        ],
    )


def rig_ext(args):
    if args:
        print("usage: e")
        return 0

    ext.ext_principal()
    return 0


def rig_build(args):
    if args:
        print("usage: b")
        return 0

    build.build_main()
    return 0


def rig_clean(args):
    if args:
        print("usage: c")
        return 0

    return clean.clean_principal()


def rig_app(args):
    if args:
        print("usage: r")
        return 0

    return app.app_principal()


def rig_debug(args):
    if args:
        print("usage: d")
        return 0

    return debug.debug_principal()


def rig_pack(args):
    if args:
        print("usage: p")
        return 0

    return pack.pack_principal()


def rig_distribuer(commande, args):
    if commande == "e":
        return rig_ext(args)

    if commande == "b":
        return rig_build(args)

    if commande == "c":
        return rig_clean(args)

    if commande == "r":
        return rig_app(args)

    if commande == "d":
        return rig_debug(args)

    if commande == "p":
        return rig_pack(args)

    if commande == "s":
        return rig_stats(args)

    print("commande inconnue : " + commande)
    return 0


def rig_session():
    return menu.session_gabarit_menu(
        "rig> ",
        afficher_menu_rig,
        rig_distribuer,
        base.decouper_commande_base,
    )


def rig_principal():
    return rig_session()


def rig_stats(args):
    if args:
        print("usage: s")
        return 0

    applications = helper.obtenir_applications_existantes()

    if not applications:
        print("aucune application")
        return 0

    for chemin in applications:
        taille = helper.obtenir_taille_fichier_kiloctets(
            chemin
        )

        ligne = (
            os.path.basename(chemin)
            + " -- "
            + format(taille, ".1f")
            + " kB"
        )

        if helper.obtenir_systeme() == "linux":
            statique = helper.verifier_liaison_statique_linux(
                chemin
            )

            if statique is None:
                ligne += " -- liaison inconnue"
            elif statique:
                ligne += " -- statique"
            else:
                ligne += " -- dynamique"

        print(ligne)

    return 0


if __name__ == "__main__":
    rig_principal()