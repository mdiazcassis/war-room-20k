import streamlit as st

# ======================================================
# SELECTOR COMUNAL
# ======================================================

def selector_comuna(df):

    comunas = sorted(
        df["COMUNA_LIMPIA"].unique()
    )

    comuna = st.selectbox(

        "Seleccionar comuna",

        comunas

    )

    fila = df[
        df["COMUNA_LIMPIA"]
        ==
        comuna
    ]

    return fila.iloc[0]