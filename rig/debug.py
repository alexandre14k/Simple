# rig/debug.py

import trace
import helper


def debug_executable_existe():
    return helper.fichier_existe(
        helper.obtenir_chemin_application(
            "debug"
        )
    )


def debug_principal():
    if not debug_executable_existe():
        print("first build debug")
        return 0

    return trace.trace_main()


if __name__ == "__main__":
    debug_principal()