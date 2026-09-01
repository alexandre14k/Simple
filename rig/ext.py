# rig/ext.py

import os
import re

import base
import helper
import init
import log
import menu
import strip


def ext_obtenir_repertoire():
    return os.path.join(
        helper.obtenir_repertoire_racine(),
        "ext",
    )


def ext_obtenir_repertoire_repo():
    return os.path.join(
        ext_obtenir_repertoire(),
        "repo",
    )


def ext_obtenir_repertoire_depot(nom):
    return os.path.join(
        ext_obtenir_repertoire_repo(),
        nom,
    )


def ext_obtenir_repertoire_projet():
    return os.path.join(
        helper.obtenir_repertoire_racine(),
        "rig",
    )


def ext_obtenir_repertoire_scratch_xmake():
    return os.path.join(
        ext_obtenir_repertoire_projet(),
        "build",
    )


def ext_entree_desactivee(nom):
    return nom.startswith("#")


def ext_depot_existe(nom):
    return helper.repertoire_existe(
        ext_obtenir_repertoire_depot(nom)
    )


def ext_organiser_git_bibliotheque(nom):
    predicat = (
        helper.fichier_est_bibliotheque_partagee
    )

    chemin = helper.rechercher_fichier_plat(
        helper.obtenir_repertoire_lib(),
        predicat,
    )

    if chemin is not None:
        return chemin

    return helper.rechercher_fichier(
        helper.obtenir_repertoire_construction_repli(),
        predicat,
    )


def ext_organiser_git_licence(nom):
    return helper.trouver_fichier_licence(
        ext_obtenir_repertoire_depot(nom)
    )


def ext_organiser_xmake_bibliotheque(cible):
    repertoire_paquet = (
        helper.trouver_installation_paquet_xmake_partagee(
            cible
        )
    )

    if repertoire_paquet is None:
        return None

    chemin = helper.trouver_bibliotheque_partagee(
        os.path.join(
            repertoire_paquet,
            "lib",
        )
    )

    if chemin is not None:
        return chemin

    return helper.trouver_bibliotheque_partagee(
        repertoire_paquet
    )


def ext_organiser_xmake_licence(cible):
    repertoire_paquet = (
        helper.trouver_installation_paquet_xmake(
            cible
        )
    )

    if repertoire_paquet is None:
        return None

    return helper.trouver_fichier_licence(
        repertoire_paquet
    )


def ext_sortie_existe(nom):
    repertoire = (
        helper.obtenir_repertoire_lib_dependance(
            nom
        )
    )

    if not helper.repertoire_existe(
        repertoire
    ):
        return False

    return len(
        os.listdir(repertoire)
    ) > 0


def ext_journaliser_bloc(
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


def ext_reference_flottante(reference):
    return reference == "latest"


MOTIF_HASH_COMPLET = re.compile(
    r"^[0-9a-fA-F]{40}$"
)

MOTIF_URL_COMMIT = re.compile(
    r"^https?://[^\s]+/commit/"
    r"([0-9a-fA-F]{40})$"
)


def ext_resoudre_hash_depuis_reference(
    reference
):
    correspondance = (
        MOTIF_URL_COMMIT.match(
            reference
        )
    )

    if correspondance:
        return correspondance.group(1)

    if MOTIF_HASH_COMPLET.match(
        reference
    ):
        return reference

    return None


def ext_reference_est_hash(
    reference
):
    return (
        ext_resoudre_hash_depuis_reference(
            reference
        )
        is not None
    )


def ext_construire_commande_clone(
    url,
    reference,
    destination
):
    commandes = [
        helper.obtenir_executable_git(),
        "-c",
        "advice.detachedHead=false",
        "clone",
        "--quiet",
    ]

    if not ext_reference_flottante(
        reference
    ):
        commandes.extend(
            [
                "--branch",
                reference,
            ]
        )

    commandes.extend(
        [
            "--depth",
            "1",
            url,
            destination,
        ]
    )

    return commandes


def ext_construire_commandes_hash(
    url,
    hash_complet,
    destination
):
    executable = (
        helper.obtenir_executable_git()
    )

    return [
        [
            executable,
            "init",
            "--quiet",
            destination,
        ],
        [
            executable,
            "-C",
            destination,
            "remote",
            "add",
            "origin",
            url,
        ],
        [
            executable,
            "-C",
            destination,
            "fetch",
            "--quiet",
            "--depth",
            "1",
            "origin",
            hash_complet,
        ],
        [
            executable,
            "-C",
            destination,
            "checkout",
            "--quiet",
            "FETCH_HEAD",
        ],
    ]


def ext_executer_commandes_capturees(
    liste_commandes,
    repertoire
):
    sortie_totale = ""

    for commande in liste_commandes:
        code, sortie = (
            helper.executer_commande_capturee(
                commande,
                repertoire,
            )
        )

        sortie_totale += sortie

        if code != 0:
            return code, sortie_totale

    return 0, sortie_totale


def ext_cloner_depot(
    nom,
    url,
    reference
):
    if ext_depot_existe(nom):
        print(
            "ext/repo/"
            + nom
            + " déjà présent"
        )
        return 0

    destination = (
        ext_obtenir_repertoire_depot(
            nom
        )
    )

    print(
        "cloning into ext/repo/"
        + nom
    )

    log.log_evenement(
        "ext",
        "clonage démarré : "
        + nom,
    )

    hash_complet = (
        ext_resoudre_hash_depuis_reference(
            reference
        )
    )

    if hash_complet is not None:
        code, sortie = (
            ext_executer_commandes_capturees(
                ext_construire_commandes_hash(
                    url,
                    hash_complet,
                    destination,
                ),
                ext_obtenir_repertoire_repo(),
            )
        )
    else:
        code, sortie = (
            helper.executer_commande_capturee(
                ext_construire_commande_clone(
                    url,
                    reference,
                    destination,
                ),
                ext_obtenir_repertoire_repo(),
            )
        )

    ext_journaliser_bloc(
        "ext",
        sortie,
    )

    if code != 0:
        print(sortie)

        log.log_evenement(
            "ext",
            "clonage échoué : "
            + nom,
        )

        return code

    log.log_evenement(
        "ext",
        "clonage terminé : "
        + nom,
    )

    return 0


def ext_installer_git(
    nom,
    cible,
    reference
):
    return ext_cloner_depot(
        nom,
        cible,
        reference,
    )


def ext_installer_xmake(
    nom,
    cible,
    reference
):
    if ext_reference_flottante(
        reference
    ):
        identifiant = cible
    else:
        identifiant = (
            cible
            if not reference
            else cible + " " + reference
        )

    commandes = [
        helper.obtenir_executable_xmake(),
        "require",
        "--yes",
        identifiant,
    ]

    print(
        "resolving "
        + nom
        + " via xmake"
    )

    log.log_evenement(
        "ext",
        "résolution xmake démarrée : "
        + nom,
    )

    code, sortie = (
        helper.executer_commande_capturee(
            commandes,
            ext_obtenir_repertoire_projet(),
        )
    )

    ext_journaliser_bloc(
        "ext",
        sortie,
    )

    if code != 0:
        print(sortie)

        log.log_evenement(
            "ext",
            "résolution xmake échouée : "
            + nom,
        )

        return code

    log.log_evenement(
        "ext",
        "résolution xmake terminée : "
        + nom,
    )

    return 0


def ext_installer_entree(
    nom,
    type_source,
    cible,
    reference
):
    if ext_entree_desactivee(nom):
        return 0

    if type_source == "git":
        return ext_installer_git(
            nom,
            cible,
            reference,
        )

    if type_source == "xmake":
        return ext_installer_xmake(
            nom,
            cible,
            reference,
        )

    print(
        "type de dépendance inconnu : "
        + type_source
    )

    log.log_evenement(
        "ext",
        "type de dépendance inconnu : "
        + nom,
    )

    return 1


def ext_installer_dependances():
    for (
        nom,
        type_source,
        cible,
        reference
    ) in init.obtenir_dependances_ext():
        code = ext_installer_entree(
            nom,
            type_source,
            cible,
            reference,
        )

        if code != 0:
            print(
                "échec installation : "
                + nom
            )

    return 0


def ext_confirmer_construction(nom):
    reponse = input(
        "construire ext/repo/"
        + nom
        + " ? [y/N] "
    ).strip().lower()

    return reponse == "y"


def ext_configurer_repertoire_construction():
    commandes = [
        helper.obtenir_executable_xmake(),
        "f",
        "-o",
        helper.obtenir_repertoire_sortie(),
    ]

    return helper.executer_commande(
        commandes,
        ext_obtenir_repertoire_projet(),
    )


def ext_construire_depot(nom):
    if ext_sortie_existe(nom):
        print(
            nom
            + " déjà construit"
        )
        return 0

    if not ext_confirmer_construction(
        nom
    ):
        return 0

    code = (
        ext_configurer_repertoire_construction()
    )

    if code != 0:
        log.log_evenement(
            "ext",
            "configuration échouée : "
            + nom,
        )
        return code

    commandes = [
        helper.obtenir_executable_xmake(),
        "build",
        nom,
    ]

    print(
        "building ext/repo/"
        + nom
    )

    log.log_evenement(
        "ext",
        "construction démarrée : "
        + nom,
    )

    code, sortie = (
        helper.executer_commande_capturee(
            commandes,
            ext_obtenir_repertoire_projet(),
        )
    )

    print(sortie)

    ext_journaliser_bloc(
        "ext",
        sortie,
    )

    if code != 0:
        log.log_evenement(
            "ext",
            "construction échouée : "
            + nom,
        )
        return code

    log.log_evenement(
        "ext",
        "construction terminée : "
        + nom,
    )

    return 0


def ext_construire_entree(
    nom,
    type_source,
    cible
):
    if ext_entree_desactivee(nom):
        return 0

    if type_source == "git":
        if not ext_depot_existe(nom):
            return 0

        code = ext_construire_depot(
            nom
        )

        if code != 0:
            print(
                "échec construction : "
                + nom
            )
            return 0

    if ext_sortie_existe(nom):
        return 0

    print(
        "organizing out/lib/"
        + nom
    )

    log.log_evenement(
        "ext",
        "organisation démarrée : "
        + nom,
    )

    code = ext_organiser_bibliotheque(
        nom,
        type_source,
        cible,
    )

    if code != 0:
        print(
            "échec organisation : "
            + nom
        )

        log.log_evenement(
            "ext",
            "organisation échouée : "
            + nom,
        )

        return 0

    log.log_evenement(
        "ext",
        "organisation terminée : "
        + nom,
    )

    return 0


def ext_nettoyer_scratch_xmake():
    return helper.supprimer_repertoire(
        ext_obtenir_repertoire_scratch_xmake()
    )


def ext_construire_dependances():
    for (
        nom,
        type_source,
        cible,
        reference
    ) in init.obtenir_dependances_ext():
        ext_construire_entree(
            nom,
            type_source,
            cible,
        )

    ext_nettoyer_scratch_xmake()

    return 0


def ext_trouver_entree(nom):
    for entree in (
        init.obtenir_dependances_ext()
    ):
        nom_entree = entree[0]

        if (
            nom_entree == nom
            or nom_entree == "#" + nom
        ):
            return entree

    return None


def ext_localiser_bibliotheque(
    nom,
    type_source,
    cible
):
    if type_source == "git":
        return ext_organiser_git_bibliotheque(
            nom
        )

    if type_source == "xmake":
        return ext_organiser_xmake_bibliotheque(
            cible
        )

    return None


def ext_localiser_licence(
    nom,
    type_source,
    cible
):
    if type_source == "git":
        return ext_organiser_git_licence(
            nom
        )

    if type_source == "xmake":
        return ext_organiser_xmake_licence(
            cible
        )

    return None


def ext_identifiant_git(nom):
    hash_commande = (
        helper.obtenir_hash_commande(
            ext_obtenir_repertoire_depot(
                nom
            ),
            6,
        )
    )

    return (
        hash_commande
        if hash_commande
        else "inconnu"
    )


def ext_identifiant_xmake(cible):
    repertoire_paquet = (
        helper.trouver_installation_paquet_xmake(
            cible
        )
    )

    if repertoire_paquet is None:
        return "inconnu"

    repertoire_version = (
        os.path.dirname(
            repertoire_paquet
        )
    )

    return os.path.basename(
        repertoire_version
    )


def ext_identifiant_archive(
    nom,
    type_source,
    cible
):
    if type_source == "git":
        return ext_identifiant_git(
            nom
        )

    if type_source == "xmake":
        return ext_identifiant_xmake(
            cible
        )

    return "inconnu"


def ext_organiser_bibliotheque(
    nom,
    type_source,
    cible
):
    chemin_bibliotheque = (
        ext_localiser_bibliotheque(
            nom,
            type_source,
            cible,
        )
    )

    if chemin_bibliotheque is None:
        print(
            "bibliothèque introuvable pour : "
            + nom
        )
        return 1

    chemin_licence = (
        ext_localiser_licence(
            nom,
            type_source,
            cible,
        )
    )

    if chemin_licence is None:
        print(
            "licence introuvable pour : "
            + nom
        )
        return 1

    repertoire_cible = (
        helper.obtenir_repertoire_lib_dependance(
            nom
        )
    )

    code = helper.supprimer_repertoire(
        repertoire_cible
    )

    if code != 0:
        return code

    code = helper.creer_repertoire(
        repertoire_cible
    )

    if code != 0:
        return code

    destination_bibliotheque = (
        os.path.join(
            repertoire_cible,
            os.path.basename(
                chemin_bibliotheque
            ),
        )
    )

    if type_source == "git":
        code = helper.deplacer_fichier(
            chemin_bibliotheque,
            destination_bibliotheque,
        )
    else:
        code = helper.copier_fichier(
            chemin_bibliotheque,
            destination_bibliotheque,
        )

    if code != 0:
        return code

    return helper.copier_fichier(
        chemin_licence,
        os.path.join(
            repertoire_cible,
            os.path.basename(
                chemin_licence
            ),
        ),
    )


def ext_archiver_entree(entree):
    (
        nom,
        type_source,
        cible,
        reference
    ) = entree

    if not ext_sortie_existe(nom):
        print(
            "construire d'abord : "
            + nom
        )
        return 1

    repertoire_zip = (
        helper.obtenir_repertoire_zip()
    )

    code = helper.creer_repertoire(
        repertoire_zip
    )

    if code != 0:
        return code

    identifiant = (
        ext_identifiant_archive(
            nom,
            type_source,
            cible,
        )
    )

    chemin_zip = os.path.join(
        repertoire_zip,
        nom
        + "_"
        + helper.obtenir_systeme()
        + "_"
        + helper.obtenir_distribution()
        + "_"
        + helper.obtenir_architecture()
        + "_"
        + identifiant
        + ".zip",
    )

    print(
        "archiving out/lib/"
        + nom
    )

    log.log_evenement(
        "ext",
        "archivage démarré : "
        + nom,
    )

    code = helper.creer_archive_zip(
        helper.obtenir_repertoire_lib_dependance(
            nom
        ),
        chemin_zip,
    )

    if code != 0:
        log.log_evenement(
            "ext",
            "archivage échoué : "
            + nom,
        )
        return code

    log.log_evenement(
        "ext",
        "archivage terminé : "
        + nom,
    )

    return 0


def ext_confirmer_archivage(nom):
    reponse = input(
        "archiver "
        + nom
        + " ? [y/N] "
    ).strip().lower()

    return reponse == "y"


def ext_archiver_dependances():
    for entree in (
        init.obtenir_dependances_ext()
    ):
        nom = entree[0]

        if ext_entree_desactivee(nom):
            continue

        if not ext_confirmer_archivage(
            nom
        ):
            continue

        code = ext_archiver_entree(
            entree
        )

        if code != 0:
            print(
                "échec archivage : "
                + nom
            )

    return 0


def ext_archiver_bibliotheque(nom):
    entree = ext_trouver_entree(
        nom
    )

    if entree is None:
        print(
            "dépendance inconnue : "
            + nom
        )
        return 1

    if ext_entree_desactivee(
        entree[0]
    ):
        print(
            "dépendance désactivée : "
            + nom
        )
        return 1

    return ext_archiver_entree(
        entree
    )


def afficher_menu_ext():
    menu.afficher_gabarit_menu(
        "run>rig>ext",
        [
            ("i", "install dependencies"),
            ("b", "build dependencies"),
            ("a", "archive dependencies"),
        ],
    )


def ext_commande_installer(args):
    if args:
        print("usage: i")
        return 0

    ext_installer_dependances()

    return 0


def ext_commande_construire(args):
    if args:
        print("usage: b")
        return 0

    ext_construire_dependances()

    return 0


def ext_commande_archiver(args):
    if args:
        print("usage: a")
        return 0

    return ext_archiver_dependances()


def ext_distribuer(
    commande,
    args
):
    if commande == "i":
        return ext_commande_installer(
            args
        )

    if commande == "b":
        return ext_commande_construire(
            args
        )

    if commande == "a":
        return ext_commande_archiver(
            args
        )

    print(
        "commande inconnue : "
        + commande
    )

    return 0


def ext_session():
    return menu.session_gabarit_menu(
        "ext> ",
        afficher_menu_ext,
        ext_distribuer,
        base.decouper_commande_base,
    )


def ext_principal():
    code = helper.creer_repertoire(
        ext_obtenir_repertoire_repo()
    )

    if code != 0:
        return 0

    return ext_session()


if __name__ == "__main__":
    ext_principal()