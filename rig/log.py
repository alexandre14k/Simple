# rig/log.py

import inspect
import os
import queue
import threading
import time

import helper


log_file_attente = queue.Queue()
log_thread_ecriture = None
log_execution = False
log_domaines_separes = set()
log_actif_app = False
log_actif_ext = False
log_actif_git = False


def log_definir_actif(domaine, actif):
    global log_actif_app
    global log_actif_ext
    global log_actif_git

    if domaine == "app":
        log_actif_app = actif
        return 0

    if domaine == "ext":
        log_actif_ext = actif
        return 0

    if domaine == "git":
        log_actif_git = actif
        return 0

    return 1


def log_domaine_actif(domaine):
    if domaine == "app":
        return log_actif_app

    if domaine == "ext":
        return log_actif_ext

    if domaine == "git":
        return log_actif_git

    return True


def log_obtenir_chemin_fichier(domaine):
    return os.path.join(
        helper.obtenir_repertoire_racine(),
        domaine + ".log",
    )


def log_obtenir_horodatage():
    return time.strftime("%Y%m%d-%H%M%S")


def log_obtenir_origine():
    cadre = inspect.stack()[2]

    chemin = os.path.relpath(
        cadre.filename,
        helper.obtenir_repertoire_racine(),
    )

    return (
        chemin.replace(os.sep, "/")
        + ":"
        + str(cadre.lineno)
    )


def log_formater_ligne(origine, message):
    return (
        log_obtenir_horodatage()
        + " -- "
        + origine
        + " -- "
        + message
    )


def log_fichier_non_vide(chemin):
    if not helper.fichier_existe(chemin):
        return False

    try:
        return os.path.getsize(chemin) > 0
    except OSError:
        return False


def log_ecrire_brute(domaine, ligne):
    try:
        with open(log_obtenir_chemin_fichier(domaine), "a") as flux:
            flux.write(ligne + "\n")
    except OSError:
        pass


def log_assurer_separation(domaine):
    if domaine in log_domaines_separes:
        return

    log_domaines_separes.add(domaine)

    if log_fichier_non_vide(log_obtenir_chemin_fichier(domaine)):
        log_ecrire_brute(domaine, "----")


def log_ecrire_ligne(domaine, ligne):
    log_assurer_separation(domaine)
    log_ecrire_brute(domaine, ligne)


def log_boucle_ecriture():
    while log_execution or not log_file_attente.empty():
        try:
            domaine, ligne = log_file_attente.get(timeout=0.1)
        except queue.Empty:
            continue

        if domaine is None:
            return

        log_ecrire_ligne(domaine, ligne)


def log_demarrer():
    global log_thread_ecriture
    global log_execution

    if log_execution:
        return 0

    log_execution = True

    log_thread_ecriture = threading.Thread(
        target=log_boucle_ecriture,
        daemon=True,
    )

    log_thread_ecriture.start()

    return 0


def log_arreter():
    global log_thread_ecriture
    global log_execution

    if not log_execution:
        return 0

    log_execution = False
    log_file_attente.put((None, None))

    if log_thread_ecriture is not None:
        log_thread_ecriture.join(
            timeout=2.0,
        )

    log_thread_ecriture = None

    return 0


def log_evenement(domaine, message):
    if not log_domaine_actif(domaine):
        return 0

    if not log_execution:
        log_demarrer()

    origine = log_obtenir_origine()
    ligne = log_formater_ligne(origine, message)

    log_file_attente.put((domaine, ligne))

    return 0


if __name__ == "__main__":
    log_demarrer()
    log_evenement("app", "test")
    log_arreter()
