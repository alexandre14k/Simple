# rig/debian.py

import os

import helper


def debian_obtenir_repertoire_paquet():
    return os.path.join(
        helper.obtenir_repertoire_sortie(),
        "deb",
    )


def debian_obtenir_repertoire_controle():
    return os.path.join(
        debian_obtenir_repertoire_paquet(),
        "DEBIAN",
    )


def debian_obtenir_repertoire_binaire():
    return os.path.join(
        debian_obtenir_repertoire_paquet(),
        "usr",
        "bin",
    )


def debian_creer_structure():
    repertoires = [
        debian_obtenir_repertoire_controle(),
        debian_obtenir_repertoire_binaire(),
    ]

    for repertoire in repertoires:
        code = helper.creer_repertoire(
            repertoire
        )

        if code != 0:
            return code

    return 0


def debian_copier_executable():
    source = helper.obtenir_chemin_application(
        "release"
    )

    if not helper.fichier_existe(source):
        print("configurer d'abord l'application")
        return 1

    destination = os.path.join(
        debian_obtenir_repertoire_binaire(),
        "app",
    )

    return helper.copier_fichier(
        source,
        destination,
    )


def debian_demander_champ(nom, valeur):
    reponse = input(
        nom
        + " ["
        + valeur
        + "] : "
    ).strip()

    if not reponse:
        return valeur

    return reponse


def debian_demander_description():
    description = input(
        "Description : "
    ).strip()

    while not description:
        print("description vide")

        description = input(
            "Description : "
        ).strip()

    return description


def debian_demander_controle():
    return {
        "Package": debian_demander_champ(
            "Package",
            "app",
        ),
        "Version": debian_demander_champ(
            "Version",
            "1.0.0",
        ),
        "Section": debian_demander_champ(
            "Section",
            "base",
        ),
        "Priority": debian_demander_champ(
            "Priority",
            "optional",
        ),
        "Architecture": debian_demander_champ(
            "Architecture",
            "amd64",
        ),
        "Maintainer": debian_demander_champ(
            "Maintainer",
            "app",
        ),
        "Description": debian_demander_description(),
    }


def debian_generer_controle():
    chemin = os.path.join(
        debian_obtenir_repertoire_controle(),
        "control",
    )

    champs = debian_demander_controle()

    contenu = "\n".join(
        [
            "Package: " + champs["Package"],
            "Version: " + champs["Version"],
            "Section: " + champs["Section"],
            "Priority: " + champs["Priority"],
            "Architecture: " + champs["Architecture"],
            "Maintainer: " + champs["Maintainer"],
            "Description: " + champs["Description"],
            "",
        ]
    )

    return helper.ecrire_fichier(
        chemin,
        contenu,
    )


def debian_construire_paquet():
    repertoire_sortie = helper.obtenir_repertoire_sortie()

    chemin_paquet = os.path.join(
        repertoire_sortie,
        "app.deb",
    )

    commandes = [
        "dpkg-deb",
        "--build",
        debian_obtenir_repertoire_paquet(),
        chemin_paquet,
    ]

    code, sortie = helper.executer_commande_capturee(
        commandes,
        repertoire_sortie,
    )

    if code == 0:
        print("out/app.deb")
    else:
        print(sortie)

    return code


def debian_principal():
    code = debian_creer_structure()

    if code != 0:
        return code

    code = debian_copier_executable()

    if code != 0:
        return code

    code = debian_generer_controle()

    if code != 0:
        return code

    return debian_construire_paquet()


if __name__ == "__main__":
    debian_principal()