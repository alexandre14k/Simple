# rig/build.py

import os

import ext
import helper
import log
import strip


def construire_journaliser_bloc(
    domaine,
    bloc
):
    for ligne in strip.strip_nettoyer_bloc(
        bloc
    ):
        log.log_evenement(
            domaine,
            ligne
        )


def construire_obtenir_includes():
    repertoire_racine = (
        helper.obtenir_repertoire_racine()
    )

    repertoire_imgui = (
        ext.ext_obtenir_repertoire_depot(
            "imgui"
        )
    )

    includes = [
        os.path.join(
            repertoire_racine,
            "app",
            "src",
        ),
        repertoire_imgui,
        os.path.join(
            repertoire_imgui,
            "backends",
        ),
    ]

    repertoire_sdl3 = (
        helper.obtenir_repertoire_includes_xmake(
            "libsdl3"
        )
    )

    if repertoire_sdl3 is not None:
        includes.append(
            repertoire_sdl3
        )

    return includes


def construire_obtenir_bibliotheques():
    chemin_imgui = (
        helper.trouver_bibliotheque_partagee(
            helper.obtenir_repertoire_lib_dependance(
                "imgui"
            )
        )
    )

    chemin_sdl3 = (
        helper.trouver_bibliotheque_partagee(
            helper.obtenir_repertoire_lib_dependance(
                "sdl3"
            )
        )
    )

    if chemin_imgui is None:
        return None

    if chemin_sdl3 is None:
        return None

    return [
        chemin_imgui,
        chemin_sdl3,
    ]


def construire_application(mode):
    repertoire_racine = (
        helper.obtenir_repertoire_racine()
    )

    repertoire_sortie = (
        helper.obtenir_repertoire_sortie()
    )

    code = helper.creer_repertoire(
        repertoire_sortie
    )

    if code != 0:
        return code

    bibliotheques = (
        construire_obtenir_bibliotheques()
    )

    if bibliotheques is None:
        print(
            "construire les dépendances d'abord "
            "(rig>ext>b)"
        )
        return 1

    sources = (
        construire_obtenir_sources()
    )

    commandes = (
        helper.obtenir_commande_compilation(
            mode
        )
    )

    if helper.obtenir_systeme() != "windows":
        commandes.extend(
            [
                "-Wl,-rpath,$ORIGIN/lib/imgui",
                "-Wl,-rpath,$ORIGIN/lib/sdl3",
            ]
        )

    commandes.append(
        "-Wl,--gc-sections"
    )

    commandes.extend(
        sources
    )

    for repertoire_include in (
        construire_obtenir_includes()
    ):
        commandes.extend(
            [
                "-I",
                repertoire_include,
            ]
        )

    commandes.extend(
        bibliotheques
    )

    commandes.extend(
        [
            "-o",
            helper.obtenir_chemin_application(
                mode
            ),
        ]
    )

    print(
        "building app (" + mode + ")"
    )

    log.log_evenement(
        "app",
        "construction application démarrée : "
        + mode,
    )

    code, sortie = (
        helper.executer_commande_capturee(
            commandes,
            repertoire_racine,
        )
    )

    print(sortie)

    construire_journaliser_bloc(
        "app",
        sortie,
    )

    if code != 0:
        log.log_evenement(
            "app",
            "construction application échouée : "
            + mode,
        )
        return code

    log.log_evenement(
        "app",
        "construction application terminée : "
        + mode,
    )

    return 0


def construire_obtenir_sources():
    repertoire_racine = (
        helper.obtenir_repertoire_racine()
    )

    repertoire_app = os.path.join(
        repertoire_racine,
        "app",
    )

    sources = []

    for (
        racine,
        dossiers,
        fichiers
    ) in os.walk(
        repertoire_app
    ):
        dossiers.sort()

        for fichier in sorted(fichiers):
            if not fichier.endswith(".cpp"):
                continue

            chemin = os.path.join(
                racine,
                fichier,
            )

            sources.append(
                os.path.relpath(
                    chemin,
                    repertoire_racine,
                )
            )

    return sources


def construire_demander_mode():
    reponse = input(
        "construire release ou debug ? [b/d/N] "
    ).strip().lower()

    if reponse == "b":
        return "release"

    if reponse == "d":
        return "debug"

    return None


def build_main():
    mode = construire_demander_mode()

    if mode is None:
        return 0

    return construire_application(
        mode
    )


if __name__ == "__main__":
    build_main()