# rig/init.py

import os


DEPENDANCES_EXT = (
    ("sdl3", "xmake", "libsdl3", ""),
    ("imgui",
     "git",
      "https://github.com/ocornut/imgui.git",
      "https://github.com/ocornut/imgui/commit/"+
      "f1cc2ae15e53a861a874c3034aae6798fde194ab"),
)


def initialiser_environnement():
    repertoire_racine = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
        )
    )

    os.environ["RIG_RACINE"] = repertoire_racine

    return 0


def charger_environnement():
    if "RIG_RACINE" in os.environ:
        return 0

    return initialiser_environnement()


def obtenir_variable_environnement(nom, valeur_par_defaut=None):
    return os.environ.get(
        nom,
        valeur_par_defaut,
    )


def definir_variable_environnement(nom, valeur):
    os.environ[nom] = valeur


def obtenir_dependances_ext():
    return DEPENDANCES_EXT


def initialiser():
    return charger_environnement()


if __name__ == "__main__":
    initialiser()