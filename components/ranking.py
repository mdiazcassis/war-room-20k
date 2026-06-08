import streamlit as st

# ======================================================
# RANKING CLICKEABLE / LISTADO COMPLETO
# ======================================================

def render_ranking(df, comuna_actual=None, altura=1120):

    # ==================================================
    # CSS
    # ==================================================

    st.markdown(
        """
<style>

/* Label del selector */
div[data-testid="stSelectbox"] label {
    font-size: 15px !important;
    font-weight: 850 !important;
    color: #F5F5F5 !important;
    letter-spacing: 0.2px !important;
}

/* Texto selector */
div[data-baseweb="select"] div {
    font-size: 15px !important;
    font-weight: 850 !important;
}

/* Caja ranking */
.ranking-shell {
    background: rgba(7, 17, 31, 0.45);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    padding: 8px;
    height: 100%;
    overflow-y: auto;
}

/* Header ranking */
.ranking-header-line {
    font-family: "SFMono-Regular", Consolas, Menlo, monospace !important;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 0.6px;
    color: #90A4AE;
    padding: 4px 6px 7px 6px;
    margin-bottom: 5px;
    border-bottom: 1px solid rgba(255,255,255,0.10);
    white-space: pre;
}

/* Radio container */
div[role="radiogroup"] {
    gap: 2px !important;
    width: 100% !important;
}

/* Cada opción */
div[role="radiogroup"] label {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;

    background: #07111F !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 5px !important;

    padding: 4px 6px !important;
    margin-bottom: 4px !important;
    min-height: 29px !important;

    display: flex !important;
    align-items: center !important;
}

/* Hover fila */
div[role="radiogroup"] label:hover {
    background: rgba(30, 136, 229, 0.20) !important;
    border: 1px solid rgba(100,181,246,0.35) !important;
}

/* Ocultar círculo radio */
div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* Contenedor interno */
div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
    width: 100% !important;
    max-width: 100% !important;
}

/* Texto opción */
div[role="radiogroup"] label p {
    color: #F5F5F5 !important;
    font-size: 12.2px !important;
    font-weight: 900 !important;
    line-height: 1.05 !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;

    white-space: pre !important;
    overflow: hidden !important;
    text-overflow: clip !important;

    font-family: "SFMono-Regular", Consolas, Menlo, monospace !important;
}

/* Opción activa */
div[role="radiogroup"] label:has(input:checked) {
    background: rgba(239, 108, 0, 0.30) !important;
    border: 1px solid rgba(239, 108, 0, 0.95) !important;
    box-shadow: 0 0 0 1px rgba(239, 108, 0, 0.25) inset !important;
}

/* Compactar vertical */
div[data-testid="stVerticalBlock"] {
    gap: 0.45rem !important;
}

</style>
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
        list(opciones.keys()),
        key="ranking_order"
    )

    columna = opciones[seleccion]

    # ==================================================
    # DATA COMPLETA
    # ==================================================

    ranking_full = (
        df
        .sort_values(
            columna,
            ascending=False
        )
        .reset_index(drop=True)
        .copy()
    )

    ranking_full["RANK_POS"] = ranking_full.index + 1

    # ==================================================
    # LABELS
    # ==================================================

    labels = []
    mapa_label_comuna = {}

    for _, row in ranking_full.iterrows():

        i = int(row["RANK_POS"])
        comuna = str(row["COMUNA_LIMPIA"])
        valor = row[columna]

        if columna != "MILITANTES_UDI":
            valor = round(float(valor), 2)
            valor_txt = f"{valor:.2f}".rstrip("0").rstrip(".")
        else:
            valor = int(valor)
            valor_txt = f"{valor}"

        comuna_txt = comuna[:13]
        label = f"{i:>2}. {comuna_txt:<13} {valor_txt:>5}"

        labels.append(label)
        mapa_label_comuna[label] = comuna

    # ==================================================
    # LABEL ACTUAL
    # ==================================================

    label_actual = None

    if comuna_actual is not None:

        comuna_actual_upper = str(comuna_actual).upper()

        for label, comuna in mapa_label_comuna.items():
            if comuna.upper() == comuna_actual_upper:
                label_actual = label
                break

    if label_actual is None and labels:
        label_actual = labels[0]

    index_actual = 0

    if label_actual in labels:
        index_actual = labels.index(label_actual)

    key_radio = f"ranking_radio_{seleccion}_{str(comuna_actual).replace(' ', '_')}"

    # ==================================================
    # CONTENEDOR
    # ==================================================

    clicked = None

    with st.container(
        height=altura,
        border=False
    ):

        st.markdown(
            """
<div class="ranking-shell">
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="ranking-header-line"> #  COMUNA          {seleccion[:5]}</div>
            """,
            unsafe_allow_html=True
        )

        seleccionado = st.radio(
            "Ranking táctico",
            labels,
            index=index_actual,
            key=key_radio,
            label_visibility="collapsed"
        )

        st.markdown(
            """
</div>
            """,
            unsafe_allow_html=True
        )

    comuna_seleccionada = mapa_label_comuna.get(
        seleccionado,
        None
    )

    if (
        comuna_seleccionada
        and comuna_actual is not None
        and comuna_seleccionada.upper() != str(comuna_actual).upper()
    ):
        clicked = comuna_seleccionada

    return clicked