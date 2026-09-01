# rig/app.py

import helper


def app_executable_existe():
    return helper.fichier_existe(
        helper.obtenir_chemin_application(
            "release"
        )
    )


def app_executer_application():
    if not app_executable_existe():
        print("configurer d'abord l'application")
        return 1

    return helper.executer_commande(
        [
            helper.obtenir_chemin_application(
                "release"
            ),
        ],
        helper.obtenir_repertoire_sortie(),
    )


def app_principal():
    app_executer_application()
    return 0


if __name__ == "__main__":
    app_principal()