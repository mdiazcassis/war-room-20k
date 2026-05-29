# ======================================================
# INTERPRETACION WAR ROOM
# ======================================================

def interpretar_tipologia(tipo):

    tipo = str(tipo).upper()

    # ==================================================
    # BASTION
    # ==================================================

    if "BASTION" in tipo:

        return (
            "Territorio consolidado con alta capacidad "
            "de movilización política y fuerte presencia "
            "operativa UDI. "
            "Requiere estrategia de mantención, "
            "protección electoral y expansión de "
            "influencia hacia comunas adyacentes."
        )

    # ==================================================
    # RESERVA
    # ==================================================

    elif "RESERVA" in tipo:

        return (
            "Comuna con base orgánica relevante, "
            "pero con estructura política insuficiente. "
            "Existe potencial claro de activación "
            "territorial mediante fortalecimiento "
            "operacional y despliegue de autoridades."
        )

    # ==================================================
    # ENCLAVE
    # ==================================================

    elif "ENCLAVE" in tipo:

        return (
            "Territorio sostenido principalmente "
            "por estructura política o presencia "
            "de autoridades, con menor respaldo "
            "orgánico territorial. "
            "Existe riesgo de fragilidad operacional "
            "si disminuye la capilaridad institucional."
        )

    # ==================================================
    # VACIO
    # ==================================================

    else:

        return (
            "Territorio con baja penetración política, "
            "escasa militancia y limitada estructura "
            "operacional. "
            "Requiere estrategia de instalación, "
            "crecimiento gradual y construcción "
            "de presencia territorial."
        )