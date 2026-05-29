import pandas as pd
import numpy as np

# ======================================================
# WAR ROOM ENGINE
# ======================================================

def procesar_datos(df):

    # ==================================================
    # NORMALIZACION
    # ==================================================

    df["MILITANCIA_NORM"] = (

        df["MILITANTES_UDI"]

        /

        df["MILITANTES_UDI"].max()

    )

    df["MIT_NORM"] = (

        df["MIT_SCORE"]

        /

        df["MIT_SCORE"].max()

    )

    # ==================================================
    # MIT LOG
    # ==================================================

    df["MIT_LOG"] = np.log1p(
        df["MIT_NORM"]
    )

    # ==================================================
    # IPL WAR ROOM
    # ==================================================

    df["IPL_WR"] = (

        (df["MILITANCIA_NORM"] * 0.7)

        +

        (df["MIT_LOG"] * 0.3)

    )

    # ==================================================
    # RANKING
    # ==================================================

    df = df.sort_values(
        by="IPL_WR",
        ascending=False
    )

    df["RANKING_WR"] = range(
        1,
        len(df) + 1
    )

    # ==================================================
    # TIPOLOGIAS WAR ROOM
    # ==================================================

    mit_mediana = df["MIT_SCORE"].median()

    militancia_mediana = df["MILITANTES_UDI"].median()

    def clasificar(row):

        alta_militancia = (
            row["MILITANTES_UDI"]
            >=
            militancia_mediana
        )

        alto_mit = (
            row["MIT_SCORE"]
            >=
            mit_mediana
        )

        if alta_militancia and alto_mit:

            return "BASTION OPERATIVO"

        elif alta_militancia and not alto_mit:

            return "RESERVA ACTIVABLE"

        elif not alta_militancia and alto_mit:

            return "ENCLAVE OPERATIVO"

        else:

            return "VACIO TERRITORIAL"

    df["TIPOLOGIA_WR"] = df.apply(
        clasificar,
        axis=1
    )

    return df