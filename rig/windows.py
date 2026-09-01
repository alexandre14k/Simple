# rig/windows.py

import os

import helper


def windows_obtenir_repertoire_paquet():
    return os.path.join(
        helper.obtenir_repertoire_sortie(),
        "win",
    )


def windows_creer_structure():
    return helper.creer_repertoire(
        windows_obtenir_repertoire_paquet()
    )


def windows_copier_executable():
    source = helper.obtenir_chemin_application(
        "release"
    )

    if not helper.fichier_existe(source):
        print("configurer d'abord l'application")
        return 1

    destination = os.path.join(
        windows_obtenir_repertoire_paquet(),
        "app.exe",
    )

    return helper.copier_fichier(
        source,
        destination,
    )


def windows_copier_dll():
    repertoire_construction = helper.obtenir_repertoire_construction(
        "release"
    )

    fichiers_dll = helper.lister_fichiers_extension(
        repertoire_construction,
        ".dll",
    )

    repertoire_paquet = windows_obtenir_repertoire_paquet()

    for source in fichiers_dll:
        destination = os.path.join(
            repertoire_paquet,
            os.path.basename(source),
        )

        code = helper.copier_fichier(
            source,
            destination,
        )

        if code != 0:
            return code

    return 0


def windows_generer_script():
    chemin = os.path.join(
        windows_obtenir_repertoire_paquet(),
        "run.bat",
    )

    contenu = "\n".join(
        [
            "@echo off",
            "cd /d %~dp0",
            "app.exe",
            "",
        ]
    )

    return helper.ecrire_fichier(
        chemin,
        contenu,
    )


def windows_principal():
    code = windows_creer_structure()

    if code != 0:
        return code

    code = windows_copier_executable()

    if code != 0:
        return code

    code = windows_copier_dll()

    if code != 0:
        return code

    return windows_generer_script()


if __name__ == "__main__":
    windows_principal()