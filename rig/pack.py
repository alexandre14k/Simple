# rig/pack.py

import base
import debian
import rpm
import menu
import windows
import helper


def obtenir_entrees_pack():
    if helper.obtenir_systeme() == "windows":
        return [
            ("w", "windows pack"),
        ]

    return [
        ("d", "debian pack"),
        ("r", "rpm pack"),
    ]


def afficher_menu_pack():
    menu.afficher_gabarit_menu(
        "run>rig>pack",
        obtenir_entrees_pack(),
    )


def pack_debian(args):
    if args:
        print("usage: d")
        return 0

    if helper.obtenir_systeme() == "windows":
        print("commande inconnue : d")
        return 0

    return debian.debian_principal()


def pack_rpm(args):
    if args:
        print("usage: r")
        return 0

    if helper.obtenir_systeme() != "linux":
        print("commande inconnue : r")
        return 0

    code = rpm.rpm_principal()

    if code != 0:
        print("échec paquet rpm")
        return 0

    return 0


def pack_windows(args):
    if args:
        print("usage: w")
        return 0

    if helper.obtenir_systeme() != "windows":
        print("commande inconnue : w")
        return 0

    return windows.windows_principal()


def pack_distribuer(
    commande,
    args
):
    if commande == "d":
        return pack_debian(args)

    if commande == "r":
        return pack_rpm(args)

    if commande == "w":
        return pack_windows(args)

    print(
        "commande inconnue : "
        + commande
    )

    return 0


def pack_session():
    return menu.session_gabarit_menu(
        "pack> ",
        afficher_menu_pack,
        pack_distribuer,
        base.decouper_commande_base,
    )


def pack_principal():
    return pack_session()


if __name__ == "__main__":
    pack_principal()