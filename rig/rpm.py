# rig/rpm.py

import os
import shutil

import helper


def rpm_obtenir_repertoire():
    return os.path.join(
        helper.obtenir_repertoire_sortie(),
        "rpm",
    )


def rpm_obtenir_repertoire_build():
    return os.path.join(
        rpm_obtenir_repertoire(),
        "BUILD",
    )


def rpm_obtenir_repertoire_rpms():
    return os.path.join(
        rpm_obtenir_repertoire(),
        "RPMS",
    )


def rpm_obtenir_repertoire_sources():
    return os.path.join(
        rpm_obtenir_repertoire(),
        "SOURCES",
    )


def rpm_obtenir_repertoire_specs():
    return os.path.join(
        rpm_obtenir_repertoire(),
        "SPECS",
    )


def rpm_obtenir_repertoire_sources_app():
    return os.path.join(
        rpm_obtenir_repertoire_sources(),
        "app",
    )


def rpm_obtenir_chemin_spec():
    return os.path.join(
        rpm_obtenir_repertoire_specs(),
        "app.spec",
    )


def rpm_obtenir_nom_architecture():
    architecture = helper.obtenir_architecture()

    correspondances = {
        "amd64": "x86_64",
        "arm64": "aarch64",
        "x86": "i686",
    }

    return correspondances.get(
        architecture,
        architecture,
    )


def rpm_demander_champ(nom, valeur):
    reponse = input(
        nom
        + " ["
        + valeur
        + "] : "
    ).strip()

    if not reponse:
        return valeur

    return reponse


def rpm_demander_description():
    description = input(
        "Description : "
    ).strip()

    while not description:
        print("description vide")

        description = input(
            "Description : "
        ).strip()

    return description


def rpm_demander_controle():
    return {
        "Name": rpm_demander_champ(
            "Name",
            "app",
        ),
        "Version": rpm_demander_champ(
            "Version",
            "1.0.0",
        ),
        "Release": rpm_demander_champ(
            "Release",
            "1",
        ),
        "Summary": rpm_demander_champ(
            "Summary",
            "app",
        ),
        "License": rpm_demander_champ(
            "License",
            "Proprietary",
        ),
        "URL": rpm_demander_champ(
            "URL",
            "",
        ),
        "Description": rpm_demander_description(),
    }


def rpm_preparer_repertoires():
    for repertoire in (
        rpm_obtenir_repertoire_build(),
        rpm_obtenir_repertoire_rpms(),
        rpm_obtenir_repertoire_sources(),
        rpm_obtenir_repertoire_specs(),
    ):
        code = helper.creer_repertoire(
            repertoire
        )

        if code != 0:
            return code

    return 0


def rpm_preparer_application():
    source_app = helper.obtenir_chemin_application(
        "release"
    )

    if not helper.fichier_existe(source_app):
        print(
            "configurer d'abord l'application"
        )
        return 1

    source_lib = helper.obtenir_repertoire_lib()
    destination = rpm_obtenir_repertoire_sources_app()

    code = helper.supprimer_repertoire(
        destination
    )

    if code != 0:
        return code

    code = helper.creer_repertoire(
        destination
    )

    if code != 0:
        return code

    code = helper.copier_fichier(
        source_app,
        os.path.join(
            destination,
            os.path.basename(source_app),
        ),
    )

    if code != 0:
        return code

    return rpm_copier_repertoire(
        source_lib,
        os.path.join(
            destination,
            "lib",
        ),
    )


def rpm_copier_repertoire(
    source,
    destination
):
    if not helper.repertoire_existe(
        source
    ):
        return 1

    for nom in os.listdir(source):
        source_complet = os.path.join(
            source,
            nom,
        )

        destination_complet = os.path.join(
            destination,
            nom,
        )

        if helper.repertoire_existe(
            source_complet
        ):
            code = helper.creer_repertoire(
                destination_complet
            )

            if code != 0:
                return code

            code = rpm_copier_repertoire(
                source_complet,
                destination_complet,
            )

            if code != 0:
                return code

            continue

        code = helper.copier_fichier(
            source_complet,
            destination_complet,
        )

        if code != 0:
            return code

    return 0


def rpm_generer_script_lancement():
    chemin = os.path.join(
        rpm_obtenir_repertoire_sources_app(),
        "run-app",
    )

    contenu = "\n".join(
        [
            "#!/bin/sh",
            "exec /usr/lib/app/app",
            "",
        ]
    )

    code = helper.ecrire_fichier(
        chemin,
        contenu,
    )

    if code != 0:
        return code

    try:
        os.chmod(
            chemin,
            0o755,
        )
    except OSError:
        return 1

    return 0


def rpm_generer_spec():
    champs = rpm_demander_controle()

    contenu = "\n".join(
        [
            "Name: " + champs["Name"],
            "Version: " + champs["Version"],
            "Release: " + champs["Release"],
            "Summary: " + champs["Summary"],
            "License: " + champs["License"],
            "URL: " + champs["URL"],
            "BuildArch: " + rpm_obtenir_nom_architecture(),
            "",
            "%description",
            champs["Description"],
            "",
            "%install",
            "rm -rf %{buildroot}",
            "mkdir -p %{buildroot}/usr/bin",
            "mkdir -p %{buildroot}/usr/lib/app",
            "cp -a %{_sourcedir}/app/app "
            "%{buildroot}/usr/lib/app/app",
            "cp -a %{_sourcedir}/app/lib "
            "%{buildroot}/usr/lib/app/lib",
            "cp -a %{_sourcedir}/app/run-app "
            "%{buildroot}/usr/bin/run-app",
            "",
            "%files",
            "/usr/bin/run-app",
            "/usr/lib/app/app",
            "/usr/lib/app/lib",
            "",
        ]
    )

    return helper.ecrire_fichier(
        rpm_obtenir_chemin_spec(),
        contenu,
    )


def rpm_obtenir_rpmbuild():
    executable = shutil.which(
        "rpmbuild"
    )

    if executable:
        return executable

    return None


def rpm_construire_paquet():
    executable = rpm_obtenir_rpmbuild()

    if executable is None:
        print("rpmbuild introuvable")
        return 1

    commandes = [
        executable,
        "--define",
        "_topdir "
        + rpm_obtenir_repertoire(),
        "-bb",
        rpm_obtenir_chemin_spec(),
    ]

    print("building rpm")

    code, sortie = (
        helper.executer_commande_capturee(
            commandes,
            rpm_obtenir_repertoire(),
        )
    )

    if sortie:
        print(sortie)

    return code


def rpm_trouver_paquet():
    repertoire = os.path.join(
        rpm_obtenir_repertoire_rpms(),
        rpm_obtenir_nom_architecture(),
    )

    if not helper.repertoire_existe(
        repertoire
    ):
        return None

    fichiers = []

    for nom in os.listdir(
        repertoire
    ):
        if nom.endswith(".rpm"):
            fichiers.append(
                os.path.join(
                    repertoire,
                    nom,
                )
            )

    if not fichiers:
        return None

    fichiers.sort()

    return fichiers[-1]


def rpm_principal():
    if helper.obtenir_systeme() != "linux":
        print("commande rpm indisponible")
        return 0

    code = rpm_preparer_repertoires()

    if code != 0:
        return code

    code = rpm_preparer_application()

    if code != 0:
        return code

    code = rpm_generer_script_lancement()

    if code != 0:
        return code

    code = rpm_generer_spec()

    if code != 0:
        return code

    print(
        "spec : "
        + os.path.relpath(
            rpm_obtenir_chemin_spec(),
            helper.obtenir_repertoire_racine(),
        )
    )

    code = rpm_construire_paquet()

    if code != 0:
        return code

    paquet = rpm_trouver_paquet()

    if paquet is None:
        print("paquet rpm introuvable")
        return 1

    chemin_relatif = os.path.relpath(
        paquet,
        helper.obtenir_repertoire_racine(),
    )

    print(
        chemin_relatif.replace(
            os.sep,
            "/",
        )
    )

    return 0


if __name__ == "__main__":
    rpm_principal()