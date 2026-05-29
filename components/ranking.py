import streamlit as st

# ======================================================
# RANKING
# ======================================================

def render_ranking(df):

    # ==================================================
    # TITULO
    # ==================================================

    st.markdown(
        """
<div style="
font-size:32px;
font-weight:900;
line-height:1;
margin-bottom:20px;
color:#F5F5F5;
">
RANKING<br>TÁCTICO
</div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # SELECTOR
    # ==================================================

    opciones = {
        "IPL": "IPL_V3",
        "MIT": "MIT_LOG",
        "MILITANCIA": "MILITANTES_UDI"
    }

    seleccion = st.selectbox(
        "Ordenar por",
        list(opciones.keys())
    )

    columna = opciones[seleccion]

    # ==================================================
    # SORT
    # ==================================================

    ranking = df.sort_values(
        columna,
        ascending=False
    )

    # ==================================================
    # CONTENEDOR
    # ==================================================

    html = """
<div style="
height:1200px;
overflow-y:scroll;
background:#081426;
border:1px solid rgba(255,255,255,0.12);
border-radius:10px;
padding:12px;
">
"""

    # ==================================================
    # FILAS
    # ==================================================

    for i, (_, row) in enumerate(
        ranking.iterrows(),
        start=1
    ):

        comuna = row["COMUNA_LIMPIA"]

        valor = row[columna]

        if columna != "MILITANTES_UDI":
            valor = round(float(valor), 3)
        else:
            valor = int(valor)

        html += f"""
<div style="
font-size:12px;
line-height:1.15;
margin-bottom:6px;
color:#F5F5F5;
">

<b>{i}. {comuna}</b>

<span style="
color:#B0BEC5;
margin-left:6px;
">
{seleccion}: {valor}
</span>

</div>
"""

    # ==================================================
    # CIERRE
    # ==================================================

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )