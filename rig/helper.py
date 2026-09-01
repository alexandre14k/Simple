# rig/helper.py

import os
import platform
import shutil
import signal
import subprocess
import zipfile


def obtenir_repertoire_racine():
    repertoire = os.environ.get("RIG_RACINE")

    if repertoire:
        return os.path.abspath(repertoire)

    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
        )
    )


def obtenir_repertoire_sortie():
    return os.path.join(
        obtenir_repertoire_racine(),
        "out",
    )


def obtenir_repertoire_construction(mode):
    return os.path.join(
        obtenir_repertoire_sortie(),
        mode,
    )


def obtenir_repertoire_lib():
    return os.path.join(
        obtenir_repertoire_sortie(),
        "lib",
    )


def obtenir_repertoire_zip():
    return os.path.join(
        obtenir_repertoire_sortie(),
        "zip",
    )


def obtenir_repertoire_lib_dependance(nom):
    return os.path.join(
        obtenir_repertoire_lib(),
        nom,
    )


def obtenir_chemin_bibliotheque_dependance(nom):
    return trouver_bibliotheque_statique(
        obtenir_repertoire_lib_dependance(nom)
    )


def obtenir_repertoire_includes_xmake(cible):
    repertoire_paquet = trouver_installation_paquet_xmake(
        cible
    )

    if repertoire_paquet is None:
        return None

    return os.path.join(
        repertoire_paquet,
        "include",
    )


def obtenir_repertoire_construction_repli():
    return os.path.join(
        obtenir_repertoire_racine(),
        "rig",
        "build",
    )


def obtenir_repertoire_globale_xmake():
    racine = os.environ.get(
        "XMAKE_GLOBALDIR",
        os.path.expanduser("~"),
    )

    return os.path.join(
        racine,
        ".xmake",
    )


def obtenir_repertoire_paquets_xmake():
    return os.path.join(
        obtenir_repertoire_globale_xmake(),
        "packages",
    )


def obtenir_repertoire_paquet_xmake(cible):
    return os.path.join(
        obtenir_repertoire_paquets_xmake(),
        cible[0].lower(),
        cible,
    )


def obtenir_nom_executable(mode):
    nom = (
        "app"
        if mode == "release"
        else "app_" + mode
    )

    return nom + obtenir_extension_executable()


def obtenir_chemin_application(mode):
    return os.path.join(
        obtenir_repertoire_sortie(),
        obtenir_nom_executable(mode),
    )


def obtenir_compilateur_cxx():
    compilateur = os.environ.get("CXX")

    if compilateur:
        return compilateur

    compilateur = shutil.which("g++")

    if compilateur:
        return compilateur

    return "g++"


def obtenir_commande_compilation(mode):
    commande = [
        obtenir_compilateur_cxx(),
        "-std=c++20",
        "-ffunction-sections",
        "-fdata-sections",
    ]

    if mode == "release":
        commande.extend(
            [
                "-O2",
            ]
        )

    if mode == "debug":
        commande.append("-g")

    return commande


def fichier_est_bibliotheque_partagee(nom_fichier):
    extension = os.path.splitext(
        nom_fichier
    )[1].lower()

    return extension in (
        ".so",
        ".dll",
        ".dylib",
    )


def trouver_bibliotheque_partagee(repertoire):
    return rechercher_fichier(
        repertoire,
        fichier_est_bibliotheque_partagee,
    )


def fichier_existe(chemin):
    return os.path.isfile(chemin)


def repertoire_existe(chemin):
    return os.path.isdir(chemin)


def creer_repertoire(chemin):
    try:
        os.makedirs(
            chemin,
            exist_ok=True,
        )
    except OSError:
        return 1

    return 0


def supprimer_repertoire(chemin):
    if not repertoire_existe(chemin):
        return 0

    try:
        shutil.rmtree(chemin)
    except OSError:
        return 1

    return 0


def executer_commande(commande, repertoire=None):
    try:
        resultat = subprocess.run(
            commande,
            cwd=repertoire,
            check=False,
        )
    except OSError:
        return 1

    return resultat.returncode


def executer_commande_capturee(
    commande,
    repertoire=None
):
    try:
        resultat = subprocess.run(
            commande,
            cwd=repertoire,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except OSError:
        return 1, ""

    return (
        resultat.returncode,
        resultat.stdout,
    )


def lancer_processus(commande, repertoire=None):
    try:
        return subprocess.Popen(
            commande,
            cwd=repertoire,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except OSError:
        return None


def processus_actif(processus):
    if processus is None:
        return False

    return processus.poll() is None


def terminer_processus(processus):
    if not processus_actif(processus):
        return 0

    try:
        processus.terminate()
        processus.wait(timeout=1.0)
    except subprocess.TimeoutExpired:
        try:
            processus.kill()
            processus.wait()
        except OSError:
            return 1
    except OSError:
        return 1

    return 0


def envoyer_signal_processus(
    processus,
    signal_systeme
):
    if not processus_actif(processus):
        return 1

    try:
        processus.send_signal(
            signal_systeme
        )
    except OSError:
        return 1

    return 0


def obtenir_systeme():
    if os.name == "nt":
        return "windows"

    if os.uname().sysname == "Darwin":
        return "macos"

    return "linux"


def obtenir_information_os_linux():
    chemin = "/etc/os-release"

    if not fichier_existe(chemin):
        return "", ""

    identifiant = ""
    version = ""

    try:
        with open(chemin) as flux:
            for ligne in flux:
                ligne = ligne.strip()

                if ligne.startswith("ID="):
                    identifiant = ligne.split(
                        "=",
                        1
                    )[1].strip('"')

                if ligne.startswith("VERSION_ID="):
                    version = ligne.split(
                        "=",
                        1
                    )[1].strip('"')
    except OSError:
        return "", ""

    return identifiant, version


def obtenir_distribution():
    if os.name == "nt":
        return platform.release()

    if os.uname().sysname == "Darwin":
        return platform.mac_ver()[0]

    identifiant, version = obtenir_information_os_linux()

    if identifiant and version:
        return (
            identifiant
            + "_"
            + version
        )

    return "inconnu"


def obtenir_architecture():
    machine = platform.machine().lower()

    correspondances = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "i386": "x86",
        "i686": "x86",
    }

    return correspondances.get(
        machine,
        machine,
    )


def obtenir_extension_executable():
    if os.name == "nt":
        return ".exe"

    return ""


def obtenir_nom_bibliotheque_statique(nom):
    if os.name == "nt":
        return nom + ".lib"

    return "lib" + nom + ".a"


def obtenir_repertoire_bin():
    return os.path.join(
        obtenir_repertoire_racine(),
        "bin",
    )


def effacer_ecran():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    return 0


def copier_fichier(
    source,
    destination
):
    try:
        shutil.copy2(
            source,
            destination
        )
    except OSError:
        return 1

    return 0


def deplacer_fichier(
    source,
    destination
):
    try:
        shutil.move(
            source,
            destination
        )
    except OSError:
        return 1

    return 0


def ecrire_fichier(
    chemin,
    contenu
):
    try:
        with open(chemin, "w") as flux:
            flux.write(contenu)
    except OSError:
        return 1

    return 0


def lister_fichiers_extension(
    repertoire,
    extension
):
    if not repertoire_existe(repertoire):
        return []

    resultat = []

    for nom in os.listdir(repertoire):
        if nom.endswith(extension):
            resultat.append(
                os.path.join(
                    repertoire,
                    nom,
                )
            )

    return resultat


def lister_sous_repertoires(chemin):
    if not repertoire_existe(chemin):
        return []

    resultat = []

    for nom in os.listdir(chemin):
        chemin_complet = os.path.join(
            chemin,
            nom,
        )

        if repertoire_existe(
            chemin_complet
        ):
            resultat.append(
                chemin_complet
            )

    return resultat


def obtenir_horodatage_modification(chemin):
    try:
        return os.path.getmtime(chemin)
    except OSError:
        return 0


def trouver_installation_paquet_xmake(cible):
    racine = obtenir_repertoire_paquet_xmake(
        cible
    )

    candidats = []

    for repertoire_version in lister_sous_repertoires(
        racine
    ):
        candidats.extend(
            lister_sous_repertoires(
                repertoire_version
            )
        )

    if not candidats:
        return None

    candidats.sort(
        key=obtenir_horodatage_modification,
        reverse=True,
    )

    return candidats[0]


def trouver_installation_paquet_xmake_partagee(
    cible
):
    racine = obtenir_repertoire_paquet_xmake(
        cible
    )

    candidats = []

    for repertoire_version in lister_sous_repertoires(
        racine
    ):
        for repertoire_paquet in lister_sous_repertoires(
            repertoire_version
        ):
            repertoire_lib = os.path.join(
                repertoire_paquet,
                "lib",
            )

            if trouver_bibliotheque_partagee(
                repertoire_lib
            ) is not None:
                candidats.append(
                    repertoire_paquet
                )

    if not candidats:
        return None

    candidats.sort(
        key=obtenir_horodatage_modification,
        reverse=True,
    )

    return candidats[0]


def fichier_est_bibliotheque_statique(
    nom_fichier
):
    extension = os.path.splitext(
        nom_fichier
    )[1].lower()

    return extension in (
        ".a",
        ".lib",
    )


def fichier_est_licence(nom_fichier):
    base, extension = os.path.splitext(
        nom_fichier
    )

    base = base.lower()
    extension = extension.lower()

    if extension not in (
        "",
        ".txt",
        ".md",
        ".rst",
    ):
        return False

    return base.startswith(
        (
            "license",
            "licence",
            "copying",
        )
    )


def fichier_correspond_nom(nom_cible):
    def predicat(nom_fichier):
        return nom_fichier == nom_cible

    return predicat


def rechercher_fichier_plat(
    repertoire,
    predicat
):
    if not repertoire_existe(repertoire):
        return None

    for nom in sorted(
        os.listdir(repertoire)
    ):
        chemin = os.path.join(
            repertoire,
            nom,
        )

        if (
            os.path.isfile(chemin)
            and predicat(nom)
        ):
            return chemin

    return None


def rechercher_fichier(
    repertoire,
    predicat
):
    if not repertoire_existe(repertoire):
        return None

    for racine, dossiers, fichiers in os.walk(
        repertoire
    ):
        for fichier in sorted(fichiers):
            if predicat(fichier):
                return os.path.join(
                    racine,
                    fichier,
                )

    return None


def trouver_bibliotheque_statique(
    repertoire
):
    return rechercher_fichier(
        repertoire,
        fichier_est_bibliotheque_statique,
    )


def trouver_fichier_licence(
    repertoire
):
    return rechercher_fichier(
        repertoire,
        fichier_est_licence,
    )


def obtenir_executable_xmake():
    executable = shutil.which("xmake")

    if executable:
        return executable

    return "xmake"


def obtenir_executable_git():
    executable = shutil.which("git")

    if executable:
        return executable

    return "git"


def obtenir_executable_gdb():
    executable = shutil.which("gdb")

    if executable:
        return executable

    return "gdb"


def obtenir_hash_commande(
    repertoire,
    longueur=6
):
    commandes = [
        obtenir_executable_git(),
        "rev-parse",
        "--short=" + str(longueur),
        "HEAD",
    ]

    code, sortie = (
        executer_commande_capturee(
            commandes,
            repertoire,
        )
    )

    if code != 0:
        return ""

    return sortie.strip()


def creer_archive_zip(
    repertoire_source,
    chemin_zip
):
    if not repertoire_existe(
        repertoire_source
    ):
        return 1

    try:
        with zipfile.ZipFile(
            chemin_zip,
            "w",
            zipfile.ZIP_DEFLATED,
        ) as archive:
            for (
                racine,
                dossiers,
                fichiers
            ) in os.walk(
                repertoire_source
            ):
                for fichier in fichiers:
                    chemin_complet = os.path.join(
                        racine,
                        fichier,
                    )

                    chemin_relatif = os.path.relpath(
                        chemin_complet,
                        repertoire_source,
                    )

                    archive.write(
                        chemin_complet,
                        chemin_relatif,
                    )
    except OSError:
        return 1

    return 0


def obtenir_chemins_applications():
    return [
        os.path.join(
            obtenir_repertoire_sortie(),
            "app",
        ),
        os.path.join(
            obtenir_repertoire_sortie(),
            "app_debug",
        ),
        os.path.join(
            obtenir_repertoire_sortie(),
            "app.exe",
        ),
        os.path.join(
            obtenir_repertoire_sortie(),
            "app_debug.exe",
        ),
    ]


def obtenir_applications_existantes():
    return [
        chemin
        for chemin in obtenir_chemins_applications()
        if fichier_existe(chemin)
    ]


def obtenir_taille_fichier_kiloctets(
    chemin
):
    try:
        return (
            os.path.getsize(chemin)
            / 1024.0
        )
    except OSError:
        return 0.0


def verifier_liaison_statique_linux(
    chemin
):
    code, sortie = (
        executer_commande_capturee(
            [
                "ldd",
                chemin,
            ]
        )
    )

    if "not a dynamic executable" in sortie:
        return True

    if "statically linked" in sortie:
        return True

    if code == 0:
        return False

    return None