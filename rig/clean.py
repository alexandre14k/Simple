# rig/clean.py

import ext
import helper


def nettoyer_confirmer(cible):
    reponse = input(
        "supprimer " + cible + " ? [y/N] "
    ).strip().lower()

    return reponse == "y"


def nettoyer_repertoire(chemin, etiquette):
    if not helper.repertoire_existe(chemin):
        print("rien à nettoyer : " + etiquette)
        return 0

    if not nettoyer_confirmer(etiquette):
        return 0

    return helper.supprimer_repertoire(chemin)


def nettoyer_repertoire_sortie():
    return nettoyer_repertoire(
        helper.obtenir_repertoire_sortie(),
        "out",
    )


def nettoyer_repertoire_ext():
    return nettoyer_repertoire(
        ext.ext_obtenir_repertoire_repo(),
        "ext/repo",
    )


def clean_principal():
    code = nettoyer_repertoire_sortie()

    if code != 0:
        return code

    code = nettoyer_repertoire_ext()

    if code != 0:
        return code

    return nettoyer_repertoire(
        helper.obtenir_repertoire_construction_repli(),
        "rig/build",
    )


if __name__ == "__main__":
    clean_principal()