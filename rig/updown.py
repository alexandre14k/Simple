# rig/updown.py

import os
import sys


def updown_effacer_ligne(
    invite,
    ligne,
    position
):
    sys.stdout.write(
        "\r"
        + " " * (
            len(invite)
            + len(ligne)
            + 2
        )
        + "\r"
        + invite
        + ligne
    )

    deplacement = len(ligne) - position

    if deplacement > 0:
        sys.stdout.write(
            "\b" * deplacement
        )

    sys.stdout.flush()


def updown_lire_posix():
    import termios
    import tty

    entree = sys.stdin
    ancien = termios.tcgetattr(
        entree
    )

    try:
        tty.setraw(
            entree.fileno()
        )

        while True:
            caractere = entree.read(1)

            if caractere == "\r" or caractere == "\n":
                return "enter"

            if caractere == "\x03":
                raise KeyboardInterrupt

            if caractere == "\x7f":
                return "backspace"

            if caractere == "\x1b":
                second = entree.read(1)

                if second != "[":
                    continue

                troisieme = entree.read(1)

                if troisieme == "A":
                    return "up"

                if troisieme == "B":
                    return "down"

                if troisieme == "C":
                    return "right"

                if troisieme == "D":
                    return "left"

                continue

            if caractere == "\x04":
                return "delete"

            return caractere

    finally:
        termios.tcsetattr(
            entree,
            termios.TCSADRAIN,
            ancien
        )


def updown_lire_windows():
    import msvcrt

    caractere = msvcrt.getwch()

    if caractere in ("\r", "\n"):
        return "enter"

    if caractere == "\x03":
        raise KeyboardInterrupt

    if caractere == "\b":
        return "backspace"

    if caractere == "\x00" or caractere == "\xe0":
        touche = msvcrt.getwch()

        if touche == "H":
            return "up"

        if touche == "P":
            return "down"

        if touche == "M":
            return "right"

        if touche == "K":
            return "left"

        if touche == "S":
            return "delete"

        return ""

    if caractere == "\x04":
        return "delete"

    return caractere


def updown_lire_caractere():
    if os.name == "nt":
        return updown_lire_windows()

    return updown_lire_posix()


def updown_lire(
    invite,
    historique
):
    ligne = ""
    position = 0
    index_historique = None

    sys.stdout.write(
        invite
    )

    sys.stdout.flush()

    while True:
        touche = updown_lire_caractere()

        if touche == "enter":
            sys.stdout.write(
                "\n"
            )
            sys.stdout.flush()
            return ligne

        if touche == "up":
            if historique:
                if index_historique is None:
                    index_historique = (
                        len(historique) - 1
                    )
                else:
                    index_historique = (
                        index_historique - 1
                    ) % len(historique)

                ligne = historique[
                    index_historique
                ]

                position = len(ligne)

                updown_effacer_ligne(
                    invite,
                    ligne,
                    position
                )

            continue

        if touche == "down":
            if historique:
                if index_historique is None:
                    index_historique = 0
                else:
                    index_historique = (
                        index_historique + 1
                    ) % len(historique)

                ligne = historique[
                    index_historique
                ]

                position = len(ligne)

                updown_effacer_ligne(
                    invite,
                    ligne,
                    position
                )

            continue

        if touche == "left":
            if position > 0:
                sys.stdout.write(
                    "\b"
                )

                position -= 1

                sys.stdout.flush()

            continue

        if touche == "right":
            if position < len(ligne):
                sys.stdout.write(
                    ligne[position]
                )

                position += 1

                sys.stdout.flush()

            continue

        if touche == "backspace":
            if position == 0:
                continue

            ligne = (
                ligne[:position - 1]
                + ligne[position:]
            )

            position -= 1

            updown_effacer_ligne(
                invite,
                ligne,
                position
            )

            continue

        if touche == "delete":
            if position >= len(ligne):
                continue

            ligne = (
                ligne[:position]
                + ligne[position + 1:]
            )

            updown_effacer_ligne(
                invite,
                ligne,
                position
            )

            continue

        if not touche:
            continue

        ligne = (
            ligne[:position]
            + touche
            + ligne[position:]
        )

        position += 1

        updown_effacer_ligne(
            invite,
            ligne,
            position
        )