# run.py

import os
import signal
import sys


sys.dont_write_bytecode = True


def run_configurer_chemins():
    repertoire_racine = os.path.dirname(
        os.path.abspath(__file__)
    )

    sys.path.insert(
        0,
        os.path.join(repertoire_racine, "rig"),
    )

    sys.path.insert(
        0,
        os.path.join(repertoire_racine, "rig", "code"),
    )


run_configurer_chemins()

import base
import git
import init
import menu
import rig


def gerer_signal_interruption(numero_signal, cadre):
    print()
    sys.exit(0)


def configurer_signaux():
    signal.signal(
        signal.SIGINT,
        gerer_signal_interruption,
    )


def afficher_menu_run():
    menu.afficher_gabarit_menu(
        "run",
        [
            ("r", "submenu rig"),
            ("g", "submenu git"),
        ],
    )


def run_rig(args):
    if args:
        print("usage: r")
        return 0

    return rig.rig_principal()


def run_git(args):
    if args:
        print("usage: g")
        return 0

    return git.git_principal()


def run_distribuer(commande, args):
    if commande == "r":
        return run_rig(args)

    if commande == "g":
        return run_git(args)

    print("commande inconnue : " + commande)
    return 0


def run_session():
    return menu.session_gabarit_menu(
        "run> ",
        afficher_menu_run,
        run_distribuer,
        base.decouper_commande_base,
    )


def run_principal():
    configurer_signaux()
    init.initialiser()

    return run_session()


if __name__ == "__main__":
    sys.exit(run_principal())