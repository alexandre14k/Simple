# rig/release.py

import os

import helper


def release_obtenir_repertoire_projet():
    return os.path.join(
        helper.obtenir_repertoire_racine(),
        "rig",
    )


def release_configurer(repertoire_sortie):
    commandes = [
        helper.obtenir_executable_xmake(),
        "f",
        "-m",
        "release",
        "-o",
        repertoire_sortie,
    ]

    return helper.executer_commande(
        commandes,
        release_obtenir_repertoire_projet(),
    )


def release_compiler():
    commandes = [
        helper.obtenir_executable_xmake(),
    ]

    return helper.executer_commande(
        commandes,
        release_obtenir_repertoire_projet(),
    )


def release_construire():
    repertoire_sortie = helper.obtenir_repertoire_construction(
        "release"
    )

    code = helper.creer_repertoire(
        repertoire_sortie
    )

    if code != 0:
        return code

    code = release_configurer(
        repertoire_sortie
    )

    if code != 0:
        return code

    return release_compiler()


def release_principal():
    return release_construire()


if __name__ == "__main__":
    release_principal()