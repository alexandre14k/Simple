# rig/git.py

import base
import helper
import log
import menu
import strip


def git_obtenir_repertoire():
    return helper.obtenir_repertoire_racine()


def git_construire_commande(args):
    commande = [helper.obtenir_executable_git()]
    commande.extend(args)
    return commande


def git_executer(args_git):
    return helper.executer_commande_capturee(
        git_construire_commande(args_git),
        git_obtenir_repertoire(),
    )


def git_journaliser_bloc(bloc):
    for ligne in strip.strip_nettoyer_bloc(bloc):
        log.log_evenement("git", ligne)


def git_afficher_resultat(sortie):
    for ligne in strip.strip_nettoyer_bloc(sortie):
        print(ligne)


def git_hash_obtenir_fichiers(hash_commit):
    code, sortie = git_executer(
        [
            "diff-tree",
            "--no-commit-id",
            "--name-status",
            "-r",
            hash_commit,
        ]
    )

    if code != 0:
        return None

    fichiers = []

    for ligne in sortie.splitlines():
        parties = ligne.split(
            "\t",
            1,
        )

        if len(parties) != 2:
            continue

        statut = parties[0][0]
        chemin = parties[1]

        if statut == "M":
            fichiers.append(
                "#m:" + chemin + " +++++++"
            )

        elif statut == "A":
            fichiers.append(
                "#a:" + chemin
            )

        elif statut == "D":
            fichiers.append(
                "#d:" + chemin
            )

    return fichiers


def git_hash_existe(hash_commit):
    code, sortie = git_executer(
        [
            "cat-file",
            "-t",
            hash_commit,
        ]
    )

    return (
        code == 0
        and sortie.strip() == "commit"
    )


def git_hash(args):
    if args:
        print("usage: h")
        return 0

    hash_commit = input(
        "hash : "
    ).strip()

    if not git_hash_existe(hash_commit):
        print("inconnu")
        return 0

    fichiers = git_hash_obtenir_fichiers(
        hash_commit
    )

    if fichiers is None:
        print("inconnu")
        return 0

    for fichier in fichiers:
        print(fichier)

    return 0


def git_inspecter_obtenir_diff(hash_commit):
    code, sortie = git_executer(
        [
            "show",
            "--format=%ad -- %h | %ae | %s",
            "--date=format:%Y%m%d-%H%M%S",
            "--no-ext-diff",
            "--unified=0",
            "--no-renames",
            hash_commit,
        ]
    )

    if code != 0:
        return None

    return sortie


def git_inspecter_afficher_diff(sortie):
    for ligne in sortie.splitlines():
        if ligne.startswith("+++ b/"):
            continue

        if ligne.startswith("--- a/"):
            continue

        if ligne.startswith("@@"):
            continue

        if ligne.startswith("+"):
            print(
                "+++ "
                + ligne[1:]
            )
            continue

        if ligne.startswith("-"):
            print(
                "--- "
                + ligne[1:]
            )


def git_inspecter(args):
    if args:
        print("usage: i")
        return 0

    hash_commit = input(
        "hash : "
    ).strip()

    if not git_hash_existe(hash_commit):
        print("inconnu")
        return 0

    sortie = git_inspecter_obtenir_diff(
        hash_commit
    )

    if sortie is None:
        print("inconnu")
        return 0

    git_inspecter_afficher_diff(
        sortie
    )

    return 0


def afficher_menu_git():
    menu.afficher_gabarit_menu(
        "run>git",
        [
            ("s", "statut"),
            ("r", "réinitialiser"),
            ("a", "rajouter"),
            ("c", "commiter"),
            ("l", "journal"),
            ("h", "hash"),
            ("i", "inspecter"),
            ("f", "récupérer"),
            ("d", "télécharger"),
            ("u", "téléverser"),
        ],
    )



def git_statut(args):
    if args:
        print("usage: s")
        return 0

    code, sortie = git_executer(["status"])

    git_afficher_resultat(sortie)
    git_journaliser_bloc(sortie)

    return 0


def git_reinitialiser(args):
    if args:
        print("usage: r")
        return 0

    code, sortie = git_executer(["reset"])

    git_afficher_resultat(sortie)
    git_journaliser_bloc(sortie)

    return 0


def git_analyser_ligne_statut(ligne):
    if not ligne:
        return None

    if ligne.startswith("##"):
        return None

    if len(ligne) < 4:
        return None

    return ligne[:2], ligne[3:]


def git_obtenir_fichiers_modifies():
    code, sortie = git_executer(["status", "-sb"])

    if code != 0:
        return []

    fichiers = []

    for ligne in sortie.splitlines():
        resultat = git_analyser_ligne_statut(ligne)

        if resultat is not None:
            fichiers.append(resultat)

    return fichiers


def git_confirmer_ajout(chemin):
    reponse = input(
        "ajouter " + chemin + " ? [y/N] "
    ).strip().lower()

    return reponse == "y"


def git_ajouter(args):
    if args:
        print("usage: a")
        return 0

    fichiers = git_obtenir_fichiers_modifies()

    if not fichiers:
        print("rien à ajouter")
        return 0

    for statut, chemin in fichiers:
        print(statut + " " + chemin)

        if not git_confirmer_ajout(chemin):
            continue

        code, sortie = git_executer(["add", "--", chemin])

        git_afficher_resultat(sortie)
        git_journaliser_bloc(sortie)

    return 0


def git_confirmer_commit(message):
    reponse = input(
        "commit \"" + message + "\" ? [y/N] "
    ).strip().lower()

    return reponse == "y"


def git_commiter(args):
    if args:
        print("usage: c")
        return 0

    message = input("message : ").strip()

    if not message:
        print("message vide")
        return 0

    if not git_confirmer_commit(message):
        return 0

    code, sortie = git_executer(["commit", "-m", message])

    git_afficher_resultat(sortie)
    git_journaliser_bloc(sortie)

    return 0


def git_journal(args):
    if args:
        print("usage: l")
        return 0

    code, sortie = git_executer(
        [
            "log",
            "-n",
            "10",
            "--format=%ad -- %h | %ae | %s",
            "--date=format:%Y%m%d-%H%M%S",
        ]
    )

    git_afficher_resultat(sortie)
    git_journaliser_bloc(sortie)

    return 0


def git_recuperer(args):
    if args:
        print("usage: f")
        return 0

    code, sortie = git_executer(["fetch"])

    git_afficher_resultat(sortie)
    git_journaliser_bloc(sortie)

    return 0


def git_telecharger(args):
    if args:
        print("usage: d")
        return 0

    code, sortie = git_executer(["pull"])

    git_afficher_resultat(sortie)
    git_journaliser_bloc(sortie)

    if code != 0:
        print("merge first")
        return 0

    return 0


def git_envoyer(args):
    if args:
        print("usage: u")
        return 0

    code, sortie = git_executer(["push"])

    git_afficher_resultat(sortie)
    git_journaliser_bloc(sortie)

    return 0


def git_distribuer(commande, args):
    if commande == "s":
        return git_statut(args)

    if commande == "r":
        return git_reinitialiser(args)

    if commande == "a":
        return git_ajouter(args)

    if commande == "c":
        return git_commiter(args)

    if commande == "l":
        return git_journal(args)

    if commande == "h":
        return git_hash(args)

    if commande == "i":
        return git_inspecter(args)

    if commande == "f":
        return git_recuperer(args)

    if commande == "d":
        return git_telecharger(args)

    if commande == "u":
        return git_envoyer(args)

    print("commande inconnue : " + commande)
    return 0


def git_session():
    return menu.session_gabarit_menu(
        "git> ",
        afficher_menu_git,
        git_distribuer,
        base.decouper_commande_base,
    )


def git_principal():
    return git_session()


if __name__ == "__main__":
    git_principal()