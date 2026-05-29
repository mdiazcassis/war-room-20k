import unicodedata

# ======================================================
# NORMALIZAR TEXTO
# ======================================================

def normalizar_texto(texto):

    if texto is None:

        return ""

    texto = str(texto)

    texto = texto.upper()

    texto = texto.strip()

    # ==============================================
    # REMOVE ACCENTS
    # ==============================================

    texto = ''.join(

        c for c in unicodedata.normalize(
            'NFD',
            texto
        )

        if unicodedata.category(c) != 'Mn'

    )

    # ==============================================
    # Ñ
    # ==============================================

    texto = texto.replace("Ñ", "N")

    # ==============================================
    # DOUBLE SPACES
    # ==============================================

    texto = " ".join(texto.split())

    return texto