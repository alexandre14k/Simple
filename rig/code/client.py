# rig/code/client.py

import queue
import threading

import filter
import helper


client_file_commandes = queue.Queue()
client_evenement_reponse = threading.Event()

client_processus = None
client_thread_commandes = None
client_thread_sortie = None

client_execution = False
client_reactif = False


def client_est_actif():
    return (
        client_execution
        and client_processus is not None
        and helper.processus_actif(client_processus)
    )


def client_est_reactif():
    return (
        client_est_actif()
        and client_reactif
    )


def client_afficher_sortie(sortie):
    filter.afficher_sortie_code(sortie)


def client_traiter_tampon(tampon):
    if not tampon:
        return ""

    client_afficher_sortie(tampon)

    return ""


def client_attendre_reponse():
    if not client_evenement_reponse.wait(
        timeout=10.0,
    ):
        return 1

    return 0


def client_boucle_sortie():
    global client_reactif

    processus = client_processus

    if processus is None:
        return

    tampon = ""

    while client_execution:
        caractere = processus.stdout.read(1)

        if not caractere:
            if tampon:
                tampon = client_traiter_tampon(
                    tampon
                )

            if processus.poll() is not None:
                client_reactif = True
                client_evenement_reponse.set()
                return

            continue

        tampon += caractere

        if tampon.endswith("(gdb) "):
            contenu = tampon[
                :-len("(gdb) ")
            ]

            client_afficher_sortie(
                contenu
            )

            tampon = ""
            client_reactif = True
            client_evenement_reponse.set()


def client_boucle_commandes():
    while client_execution:
        try:
            commande = client_file_commandes.get(
                timeout=0.1,
            )
        except queue.Empty:
            continue

        if commande is None:
            return

        processus = client_processus

        if processus is None:
            continue

        try:
            processus.stdin.write(
                commande + "\n"
            )
            processus.stdin.flush()
        except (BrokenPipeError, OSError):
            return


def client_demarrer(commande, repertoire=None):
    global client_processus
    global client_thread_commandes
    global client_thread_sortie
    global client_execution
    global client_reactif

    client_arreter()

    client_processus = helper.lancer_processus(
        commande,
        repertoire,
    )

    if client_processus is None:
        return 1

    client_execution = True
    client_reactif = False
    client_evenement_reponse.clear()

    client_thread_sortie = threading.Thread(
        target=client_boucle_sortie,
        daemon=True,
    )

    client_thread_commandes = threading.Thread(
        target=client_boucle_commandes,
        daemon=True,
    )

    client_thread_sortie.start()
    client_thread_commandes.start()

    code = client_attendre_reponse()

    if code != 0:
        client_arreter()
        return code

    return 0


def client_envoyer(commande):
    global client_reactif

    if not client_est_actif():
        return 1

    client_reactif = False
    client_evenement_reponse.clear()

    client_file_commandes.put(commande)

    return client_attendre_reponse()


def client_arreter():
    global client_processus
    global client_thread_commandes
    global client_thread_sortie
    global client_execution
    global client_reactif

    client_execution = False
    client_reactif = False
    client_evenement_reponse.clear()

    while True:
        try:
            client_file_commandes.get_nowait()
        except queue.Empty:
            break

    processus = client_processus

    if processus is not None:
        try:
            if processus.stdin is not None:
                processus.stdin.close()
        except (BrokenPipeError, OSError):
            pass

        helper.terminer_processus(processus)

    if client_thread_commandes is not None:
        client_thread_commandes.join(
            timeout=1.0,
        )

    if client_thread_sortie is not None:
        client_thread_sortie.join(
            timeout=1.0,
        )

    client_processus = None
    client_thread_commandes = None
    client_thread_sortie = None

    return 0