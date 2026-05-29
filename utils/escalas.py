# ======================================================
# ESCALA IPL
# ======================================================

def escala_ipl(valor):

    if valor >= 0.80:

        return "DOMINANTE"

    elif valor >= 0.60:

        return "ALTO"

    elif valor >= 0.40:

        return "MEDIO"

    elif valor >= 0.20:

        return "BAJO"

    else:

        return "CRITICO"


# ======================================================
# ESCALA MIT
# ======================================================

def escala_mit(valor):

    if valor >= 8:

        return "CAPILAR"

    elif valor >= 5:

        return "FUERTE"

    elif valor >= 2:

        return "OPERATIVO"

    else:

        return "DEBIL"


# ======================================================
# ESCALA MILITANCIA
# ======================================================

def escala_militancia(valor):

    if valor >= 1500:

        return "BASTION"

    elif valor >= 700:

        return "ALTA"

    elif valor >= 250:

        return "MEDIA"

    else:

        return "BAJA"