# rig/combine.py


def combine_decouper(ligne):
    if "+" not in ligne:
        return [ligne]

    parties = ligne.split(
        "+"
    )

    resultat = []

    for partie in parties:
        partie = partie.strip()

        if partie:
            resultat.append(
                partie
            )

    return resultat