# rig/code/server.py

import threading

import helper


server_processus = None
server_thread = None
server_execution = False


def server_est_actif():
    return (
        server_execution
        and server_processus is not None
        and helper.processus_actif(server_processus)
    )


def server_boucle_sortie():
    processus = server_processus

    if processus is None:
        return

    while server_execution:
        ligne = processus.stdout.readline()

        if not ligne:
            if processus.poll() is not None:
                return

            continue

        print(ligne.rstrip())


def server_demarrer(commande, repertoire=None):
    global server_processus
    global server_thread
    global server_execution

    server_arreter()

    server_processus = helper.lancer_processus(
        commande,
        repertoire,
    )

    if server_processus is None:
        return 1

    server_execution = True

    server_thread = threading.Thread(
        target=server_boucle_sortie,
        daemon=True,
    )

    server_thread.start()

    return 0


def server_arreter():
    global server_processus
    global server_thread
    global server_execution

    server_execution = False

    processus = server_processus

    if processus is not None:
        helper.terminer_processus(processus)

    if server_thread is not None:
        server_thread.join(
            timeout=1.0,
        )

    server_processus = None
    server_thread = None

    return 0


def server_reinitialiser(commande, repertoire=None):
    server_arreter()

    return server_demarrer(
        commande,
        repertoire,
    )