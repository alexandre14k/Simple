# rig/code/code.py

import os

import base
import client
import helper


code_programme_demarre = False


def afficher_menu_code():
    base.afficher_menu_base(
        "run>rig>debug>code",
        [
            ("at", "attacher"),
            ("re", "réinitialiser"),
            ("br <étiquette>", "définir un point d'arrêt"),
            ("d", "supprimer tous les points d'arrêt"),
            ("c", "continuer"),
            ("ls", "prévisualiser les lignes suivantes"),
            ("s", "entrer dans la fonction"),
            ("o", "sortir de la fonction"),
            ("n", "instruction suivante"),
            ("h", "afficher l'aide"),
            ("m", "afficher le menu"),
            ("x", "quitter"),
        ],
    )


def afficher_aide_code():
    base.afficher_aide_base(
        "code",
        [
            ("at", "attacher"),
            ("re", "réinitialiser"),
            ("br <étiquette>", "définir un point d'arrêt"),
            ("d", "supprimer tous les points d'arrêt"),
            ("c", "continuer"),
            ("ls", "prévisualiser les lignes suivantes"),
            ("s", "entrer dans la fonction"),
            ("o", "sortir de la fonction"),
            ("n", "instruction suivante"),
            ("ch <expression>", "afficher comme caractère"),
            ("str <expression>", "afficher comme chaîne"),
            ("bin <expression>", "afficher en binaire"),
            ("hex <expression>", "afficher en hexadécimal"),
            ("get addr <expression>", "obtenir l'adresse en hexadécimal"),
            ("set char <expression>", "allouer et définir un caractère"),
            ("set short <expression>", "allouer et définir un entier court"),
            ("set int <expression>", "allouer et définir un entier"),
            ("set uchar <expression>", "allouer et définir un caractère non signé"),
            ("set ushort <expression>", "allouer et définir un entier court non signé"),
            ("set uint <expression>", "allouer et définir un entier non signé"),
            ("m", "afficher le menu"),
            ("x", "quitter"),
        ],
    )


def code_executable_debug_existe():
    return helper.fichier_existe(
        helper.obtenir_chemin_application(
            "debug"
        )
    )


def code_attacher(args):
    if args:
        print("usage: at")
        return 0

    if not client.client_est_actif():
        return 1

    return 0


def code_reinitialiser(args):
    if args:
        print("usage: re")
        return 0

    return 0


def code_point_arret(args):
    if not args:
        print("usage: br <étiquette>")
        return 0

    etiquette = " ".join(args)

    return client.client_envoyer(
        "break " + etiquette
    )


def code_supprimer_points_arret(args):
    if args:
        print("usage: d")
        return 0

    return client.client_envoyer(
        "delete"
    )


def code_continuer(args):
    global code_programme_demarre

    if args:
        print("usage: c")
        return 0

    if not code_programme_demarre:
        code_programme_demarre = True

        return client.client_envoyer(
            "run"
        )

    return client.client_envoyer(
        "continue"
    )


def code_apercu_lignes(args):
    if args:
        print("usage: ls")
        return 0

    return client.client_envoyer(
        "list"
    )


def code_entrer(args):
    if args:
        print("usage: s")
        return 0

    return client.client_envoyer(
        "step"
    )


def code_sortir(args):
    if args:
        print("usage: o")
        return 0

    return client.client_envoyer(
        "finish"
    )


def code_suivant(args):
    if args:
        print("usage: n")
        return 0

    return client.client_envoyer(
        "next"
    )


def code_afficher_valeur(args, formatage, commande):
    if not args:
        print("usage: " + commande + " <expression>")
        return 0

    expression = " ".join(args)

    return client.client_envoyer(
        "print/" + formatage + " " + expression
    )


def code_afficher_caractere(args):
    return code_afficher_valeur(
        args,
        "c",
        "ch",
    )


def code_afficher_chaine(args):
    return code_afficher_valeur(
        args,
        "s",
        "str",
    )


def code_afficher_binaire(args):
    return code_afficher_valeur(
        args,
        "t",
        "bin",
    )


def code_afficher_hexadecimal(args):
    return code_afficher_valeur(
        args,
        "x",
        "hex",
    )


def code_obtenir_adresse(args):
    if not args:
        print("usage: get addr <expression>")
        return 0

    expression = " ".join(args)

    return client.client_envoyer(
        "print/x &(" + expression + ")"
    )


def code_definir_valeur(args, type_nom, commande):
    if not args:
        print(
            "usage: "
            + commande
            + " <expression>"
        )
        return 0

    expression = " ".join(args)

    commandes = [
        "set $code_memoire = ("
        + type_nom
        + " *) malloc(sizeof("
        + type_nom
        + "))",
        "set {"
        + type_nom
        + "} $code_memoire = "
        + expression,
        "print/x $code_memoire",
    ]

    for commande_debug in commandes:
        code = client.client_envoyer(
            commande_debug
        )

        if code != 0:
            return code

    return 0


def code_definir_caractere(args):
    return code_definir_valeur(
        args,
        "char",
        "set char",
    )


def code_definir_entier_court(args):
    return code_definir_valeur(
        args,
        "short",
        "set short",
    )


def code_definir_entier(args):
    return code_definir_valeur(
        args,
        "int",
        "set int",
    )


def code_definir_caractere_non_signe(args):
    return code_definir_valeur(
        args,
        "unsigned char",
        "set uchar",
    )


def code_definir_entier_court_non_signe(args):
    return code_definir_valeur(
        args,
        "unsigned short",
        "set ushort",
    )


def code_definir_entier_non_signe(args):
    return code_definir_valeur(
        args,
        "unsigned int",
        "set uint",
    )


def code_afficher_aide(args):
    if args:
        print("usage: h")
        return 0

    afficher_aide_code()
    return 0


def code_afficher_menu(args):
    if args:
        print("usage: m")
        return 0

    afficher_menu_code()
    return 0


def code_distribuer(commande, args):
    if commande == "at":
        return code_attacher(args)

    if commande == "re":
        return code_reinitialiser(args)

    if commande == "br":
        return code_point_arret(args)

    if commande == "d":
        return code_supprimer_points_arret(args)

    if commande == "c":
        return code_continuer(args)

    if commande == "ls":
        return code_apercu_lignes(args)

    if commande == "s":
        return code_entrer(args)

    if commande == "o":
        return code_sortir(args)

    if commande == "n":
        return code_suivant(args)

    if commande == "ch":
        return code_afficher_caractere(args)

    if commande == "str":
        return code_afficher_chaine(args)

    if commande == "bin":
        return code_afficher_binaire(args)

    if commande == "hex":
        return code_afficher_hexadecimal(args)

    if (
        commande == "get"
        and len(args) >= 2
        and args[0] == "addr"
    ):
        return code_obtenir_adresse(args[1:])

    if commande == "set" and len(args) >= 2:
        if args[0] == "char":
            return code_definir_caractere(args[1:])

        if args[0] == "short":
            return code_definir_entier_court(args[1:])

        if args[0] == "int":
            return code_definir_entier(args[1:])

        if args[0] == "uchar":
            return code_definir_caractere_non_signe(args[1:])

        if args[0] == "ushort":
            return code_definir_entier_court_non_signe(args[1:])

        if args[0] == "uint":
            return code_definir_entier_non_signe(args[1:])

    if commande == "h":
        return code_afficher_aide(args)

    if commande == "m":
        return code_afficher_menu(args)

    if commande == "x":
        return 1

    print("commande inconnue : " + commande)
    return 0


def code_session():
    global code_programme_demarre

    if not code_executable_debug_existe():
        print("configurer d'abord l'application en mode debug")
        return 1

    code_programme_demarre = False

    chemin_absolu = helper.obtenir_chemin_application(
        "debug"
    )

    chemin_relatif = os.path.relpath(
        chemin_absolu,
        helper.obtenir_repertoire_racine(),
    )

    commande = [
        helper.obtenir_executable_gdb(),
        "--quiet",
        chemin_relatif,
    ]

    if client.client_demarrer(
        commande,
        helper.obtenir_repertoire_racine(),
    ) != 0:
        return 1

    try:
        afficher_menu_code()

        while True:
            ligne = input("code> ").strip()
            parties = base.decouper_commande_base(ligne)

            if not parties:
                continue

            commande = parties[0]
            args = parties[1:]

            resultat = code_distribuer(
                commande,
                args,
            )

            if resultat == 1:
                return 0

            if resultat != 0:
                return resultat
    finally:
        client.client_arreter()


def code_principal():
    return code_session()


if __name__ == "__main__":
    code_principal()