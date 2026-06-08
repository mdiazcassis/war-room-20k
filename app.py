# WAR_ROOM_UDI_V6_PUBLICACION_FINAL

import json
import unicodedata
from textwrap import dedent

import streamlit as st
import pandas as pd
import pydeck as pdk

from components.ranking import render_ranking
from components.ficha import render_ficha


# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    layout="wide",
    page_title="WAR ROOM"
)

ALTURA_PRINCIPAL = 1120
ALTURA_RANKING = 1040


# ======================================================
# HELPERS HTML
# ======================================================

def html(code):
    limpio = "\n".join(
        line.strip()
        for line in dedent(code).splitlines()
        if line.strip()
    )

    st.markdown(
        limpio,
        unsafe_allow_html=True
    )


def force_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


def actualizar_desde_selector():
    st.session_state["comuna_actual"] = st.session_state["selector_widget"]


def normalizar_comuna(texto):
    """
    Normaliza nombres de comunas para matching entre Excel y GeoJSON.
    Ejemplos:
    MAIPÚ -> MAIPU
    ÑUÑOA -> NUNOA
    PEÑALOLÉN -> PENALOLEN
    VIÑA DEL MAR -> VINA DEL MAR
    """

    if pd.isna(texto):
        return ""

    texto = str(texto).strip().upper()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    texto = (
        texto
        .replace("Ñ", "N")
        .replace("  ", " ")
        .strip()
    )

    return texto


# ======================================================
# CSS
# ======================================================

st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(90deg, #020617 0%, #001B44 100%);
    color: white;
}

div[data-baseweb="select"] > div {
    background-color: #1E1E2F;
    color: white;
    border-radius: 10px;
}

h1, h2, h3, h4 {
    color: #F5F5F5 !important;
    font-weight: 800 !important;
}

p, label {
    color: #E0E0E0;
}

.block-container {
    padding-top: 0.1rem;
    padding-bottom: 1rem;
}

/* =====================================================
   HEADER WAR ROOM
===================================================== */

.war-header-spacer {
    height: 22px;
}

.header-logo-box {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 24px;
}

.header-zone {
    padding-top: 8px;
    margin-bottom: 8px;
}

.header-glossary {
    width: 100%;
    color: #B0BEC5;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.25px;
    line-height: 1.35;
    margin-bottom: 10px;
}

.header-glossary-line {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.header-glossary b {
    color: #F5F5F5;
    font-weight: 950;
}

.header-glossary .bastion {
    color: #64B5F6;
    font-weight: 950;
}

.header-glossary .reserva {
    color: #FFB74D;
    font-weight: 950;
}

.header-glossary .enclave {
    color: #66BB6A;
    font-weight: 950;
}

.header-glossary .vacio {
    color: #B0BEC5;
    font-weight: 950;
}

.header-glossary .intensidad {
    color: #F5F5F5;
    font-weight: 950;
}

.war-strip {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 21px;
    width: 100%;
    margin-top: 48px;
    padding: 0;
    font-size: 12px;
    letter-spacing: 1.15px;
    color: #D7DEE8;
    opacity: 0.98;
    white-space: nowrap;
}

.war-strip span {
    display: inline-block;
}

.war-strip b {
    color: #FFFFFF;
    font-size: 21px;
    font-weight: 950;
    margin-right: 6px;
}

.war-separator {
    opacity: 0.32;
}

.selector-wrapper {
    margin-top: -6px;
    margin-bottom: 12px;
}

/* =====================================================
   BOTÓN / MARCA DE AGUA VERSIÓN
===================================================== */

.version-widget {
    position: fixed;
    top: 86px;
    right: 34px;
    z-index: 9999;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.version-widget details {
    position: relative;
}

.version-widget summary {
    list-style: none;
    cursor: pointer;
    user-select: none;

    background: rgba(7, 17, 31, 0.72);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 999px;

    color: rgba(245,245,245,0.88);
    font-size: 10.5px;
    font-weight: 900;
    letter-spacing: 0.45px;

    padding: 5px 10px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.24);
    backdrop-filter: blur(3px);
}

.version-widget summary::-webkit-details-marker {
    display: none;
}

.version-widget summary:hover {
    background: rgba(30, 136, 229, 0.24);
    border-color: rgba(100,181,246,0.45);
    color: #FFFFFF;
}

.version-panel {
    position: absolute;
    top: 31px;
    right: 0;
    width: 235px;

    background: rgba(7, 17, 31, 0.97);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 12px;

    padding: 11px 12px;
    color: #D7DEE8;
    box-shadow: 0 16px 44px rgba(0,0,0,0.42);
}

.version-title {
    color: #F5F5F5;
    font-size: 12px;
    font-weight: 950;
    letter-spacing: 0.7px;
    margin-bottom: 8px;
}

.version-row {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 6px;
    margin-top: 6px;
    font-size: 10.5px;
    line-height: 1.25;
}

.version-label {
    color: #90A4AE;
    font-weight: 900;
}

.version-value {
    color: #F5F5F5;
    font-weight: 850;
    text-align: right;
}

/* =====================================================
   PANEL REGIONAL
===================================================== */

.regional-panel {
    margin-top: 16px;
    background: rgba(7, 17, 31, 0.84);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 14px;
    padding: 14px 15px 15px 15px;
}

.regional-head {
    display: grid;
    grid-template-columns: 1.2fr 3.8fr;
    gap: 15px;
    align-items: stretch;
    margin-bottom: 10px;
}

.regional-title-box {
    background: rgba(2, 6, 23, 0.42);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 11px;
    padding: 12px 13px;
}

.regional-title {
    font-size: 23px;
    font-weight: 950;
    color: #F5F5F5;
    letter-spacing: 1.2px;
    line-height: 1;
    margin-bottom: 8px;
}

.regional-subtitle {
    font-size: 13px;
    color: #B0BEC5;
    font-weight: 700;
}

.regional-reading-compact {
    background: #081426;
    border: 1px solid rgba(255,255,255,0.10);
    border-left: 5px solid #1E88E5;
    border-radius: 11px;
    padding: 10px 12px;
}

.regional-reading-title {
    font-size: 13px;
    font-weight: 950;
    color: #F5F5F5;
    letter-spacing: 0.8px;
    margin-bottom: 7px;
}

.regional-reading-flow {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 9px;
}

.regional-read-mini {
    background: rgba(2, 6, 23, 0.55);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 8px 9px;
}

.regional-read-label {
    font-size: 9px;
    color: #90A4AE;
    font-weight: 950;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
}

.regional-read-text {
    font-size: 13px;
    line-height: 1.28;
    color: #F5F5F5;
    font-weight: 850;
}

.regional-kpi-strip {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
    margin-bottom: 11px;
}

.regional-kpi {
    background: #081426;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    padding: 8px 10px;
    min-height: 48px;
}

.regional-kpi-label {
    font-size: 8.5px;
    color: #B0BEC5;
    font-weight: 950;
    letter-spacing: 0.85px;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.regional-kpi-value {
    font-size: 21px;
    font-weight: 950;
    color: #F5F5F5;
    line-height: 0.95;
}

.regional-ranking-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
}

.regional-ranking-box,
.regional-ranking-box-scroll {
    background: #081426;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 11px;
    padding: 10px 11px;
    height: 205px;
    overflow-y: scroll;
}

.regional-ranking-title {
    font-size: 12.5px;
    font-weight: 950;
    color: #F5F5F5;
    letter-spacing: 0.55px;
    margin-bottom: 8px;
    position: sticky;
    top: 0;
    background: #081426;
    padding-bottom: 7px;
    z-index: 10;
}

.regional-row {
    display: grid;
    grid-template-columns: 28px 1fr 68px;
    gap: 7px;
    font-size: 11px;
    line-height: 1.18;
    color: #F5F5F5;
    margin-bottom: 6px;
}

.regional-rank {
    color: #B0BEC5;
    font-weight: 900;
}

.regional-commune {
    font-weight: 950;
}

.regional-value {
    color: #B0BEC5;
    text-align: right;
    font-weight: 900;
}

.region-current {
    background: rgba(30, 136, 229, 0.20);
    border-left: 3px solid #1E88E5;
    border-radius: 6px;
    padding: 4px 4px;
    margin-left: -4px;
    margin-right: -4px;
}

.commune-current {
    background: rgba(239, 108, 0, 0.24);
    border-left: 3px solid #EF6C00;
    border-radius: 6px;
    padding: 4px 4px;
    margin-left: -4px;
    margin-right: -4px;
}

.regional-ranking-box::-webkit-scrollbar,
.regional-ranking-box-scroll::-webkit-scrollbar {
    width: 6px;
}

.regional-ranking-box::-webkit-scrollbar-track,
.regional-ranking-box-scroll::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.04);
}

.regional-ranking-box::-webkit-scrollbar-thumb,
.regional-ranking-box-scroll::-webkit-scrollbar-thumb {
    background: rgba(176,190,197,0.35);
    border-radius: 10px;
}
</style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# DATA
# ======================================================

@st.cache_data
def load_data():
    return pd.read_excel("data/WAR_ROOM_CORE_V6_OFICIAL.xlsx")


@st.cache_data
def load_geojson():
    with open("data/chile_comunas.geojson", "r", encoding="utf-8") as f:
        return json.load(f)


df = load_data()
geojson = load_geojson()

df["COMUNA_LIMPIA"] = df["COMUNA_LIMPIA"].astype(str).str.upper()
df["COMUNA_KEY"] = df["COMUNA_LIMPIA"].apply(normalizar_comuna)


# ======================================================
# MOTOR ESTRATÉGICO V6 / IPL_V4
# ======================================================

if "IPL_V4" in df.columns:
    df["IPL_V3"] = df["IPL_V4"]

if "TIPOLOGIA_V4" in df.columns:
    df["TIPOLOGIA_FINAL"] = df["TIPOLOGIA_V4"]

if "RANKING_IPL_V4" in df.columns:
    df["RANKING_IPL_DASH"] = df["RANKING_IPL_V4"].astype(int)


# ======================================================
# RANGOS DE INTENSIDAD — 3 TRAMOS CLAROS
# ======================================================

IPL_Q1 = float(
    df["IPL_V3"].quantile(0.33)
)

IPL_Q2 = float(
    df["IPL_V3"].quantile(0.66)
)


# ======================================================
# RANKINGS DASHBOARD
# ======================================================

if "RANKING_IPL_DASH" not in df.columns:
    df["RANKING_IPL_DASH"] = (
        df["IPL_V3"]
        .rank(
            ascending=False,
            method="min"
        )
        .astype(int)
    )

df["RANKING_MIT_DASH"] = (
    df["MIT_LOG"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)

df["RANKING_MILITANCIA_DASH"] = (
    df["MILITANTES_UDI"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)


# ======================================================
# MÉTRICAS HEADER MANUALES
# ======================================================

TOTAL_MUNICIPIOS_LABEL = "310/345"
TOTAL_MILITANTES_LABEL = "30.7K"

TOTAL_ALCALDES = 33
TOTAL_CONCEJALES = 267
TOTAL_CORES = 76
TOTAL_DIPUTADOS = 17
TOTAL_SENADORES = 5
TOTAL_GOBERNADORES = 3


# ======================================================
# HEADER
# ======================================================

st.markdown(
    '<div class="war-header-spacer"></div>',
    unsafe_allow_html=True
)

logo_col, metrics_col = st.columns(
    [1.25, 5.60]
)

with logo_col:
    st.markdown(
        '<div class="header-logo-box">',
        unsafe_allow_html=True
    )

    st.image(
        "assets/logo_20k.png",
        width=168
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

with metrics_col:
    html(
        f"""
        <div class="header-zone">

            <div class="header-glossary">
                <div class="header-glossary-line">
                    <b>IPL</b>: Índice Potencial Longueira · prioridad de activación · 
                    <b>MIT</b>: matriz de influencia territorial · 
                    <b>Militancia</b>: base movilizable
                </div>
                <div class="header-glossary-line">
                    <span class="bastion">BASTIÓN</span>: base alta + estructura alta · 
                    <span class="reserva">RESERVA</span>: base activable + estructura baja · 
                    <span class="enclave">ENCLAVE</span>: estructura alta + base baja · 
                    <span class="vacio">VACÍO</span>: baja base + baja estructura · 
                    <span class="intensidad">Intensidad</span>: IPL alto / medio / bajo
                </div>
            </div>

            <div class="war-strip">
                <span><b>{TOTAL_MUNICIPIOS_LABEL}</b> MUNICIPIOS</span>
                <span class="war-separator">|</span>
                <span><b>{TOTAL_MILITANTES_LABEL}</b> MILITANTES</span>
                <span class="war-separator">|</span>
                <span><b>{TOTAL_ALCALDES}</b> ALC</span>
                <span><b>{TOTAL_CONCEJALES}</b> CON</span>
                <span><b>{TOTAL_CORES}</b> CORE</span>
                <span><b>{TOTAL_DIPUTADOS}</b> DIP</span>
                <span><b>{TOTAL_SENADORES}</b> SEN</span>
                <span><b>{TOTAL_GOBERNADORES}</b> GOB</span>
            </div>

        </div>
        """
    )


# ======================================================
# BOTÓN MARCA DE AGUA / VERSIONES
# ======================================================

html(
    """
    <div class="version-widget">
        <details>
            <summary>MDiazCassis · V6</summary>
            <div class="version-panel">
                <div class="version-title">WAR ROOM UDI · V6</div>

                <div class="version-row">
                    <div class="version-label">Autor</div>
                    <div class="version-value">MDiazCassis</div>
                </div>

                <div class="version-row">
                    <div class="version-label">Motor</div>
                    <div class="version-value">IPL V4</div>
                </div>

                <div class="version-row">
                    <div class="version-label">Cobertura</div>
                    <div class="version-value">345 comunas</div>
                </div>

                <div class="version-row">
                    <div class="version-label">Ranking</div>
                    <div class="version-value">prioridad interna</div>
                </div>

                <div class="version-row">
                    <div class="version-label">Color</div>
                    <div class="version-value">tipología territorial</div>
                </div>

                <div class="version-row">
                    <div class="version-label">Tono</div>
                    <div class="version-value">IPL alto / medio / bajo</div>
                </div>

                <div class="version-row">
                    <div class="version-label">Variables</div>
                    <div class="version-value">militancia + MIT + reserva + balance</div>
                </div>
            </div>
        </details>
    </div>
    """
)


# ======================================================
# SELECTOR CON SESSION STATE
# ======================================================

comunas = sorted(
    df["COMUNA_LIMPIA"].unique()
)

if "comuna_actual" not in st.session_state:
    st.session_state["comuna_actual"] = comunas[0]

if st.session_state["comuna_actual"] not in comunas:
    st.session_state["comuna_actual"] = comunas[0]

if (
    "selector_widget" not in st.session_state
    or st.session_state["selector_widget"] != st.session_state["comuna_actual"]
):
    st.session_state["selector_widget"] = st.session_state["comuna_actual"]

st.markdown(
    '<div class="selector-wrapper">',
    unsafe_allow_html=True
)

st.selectbox(
    "Seleccionar comuna",
    comunas,
    key="selector_widget",
    on_change=actualizar_desde_selector
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

comuna = st.session_state["comuna_actual"]

fila = df[
    df["COMUNA_LIMPIA"] == comuna
].iloc[0]


# ======================================================
# FUNCIONES DE COLOR MAPA
# ======================================================

def normalizar_tipo(tipo):

    tipo_norm = (
        str(tipo)
        .upper()
        .replace("Á", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
        .replace(" ", "_")
        .replace("-", "_")
    )

    return tipo_norm


def nivel_intensidad_ipl(ipl):

    try:
        valor = float(ipl)
    except Exception:
        valor = 0.0

    if valor >= IPL_Q2:
        return "ALTA"
    elif valor >= IPL_Q1:
        return "MEDIA"
    else:
        return "BAJA"


def color_tipologia_bandeado(tipo, ipl):

    tipo_norm = normalizar_tipo(tipo)
    nivel = nivel_intensidad_ipl(ipl)

    if "BASTION" in tipo_norm:

        if nivel == "ALTA":
            return [64, 156, 255]
        elif nivel == "MEDIA":
            return [31, 119, 214]
        else:
            return [19, 80, 156]

    elif "RESERVA" in tipo_norm:

        if nivel == "ALTA":
            return [255, 149, 64]
        elif nivel == "MEDIA":
            return [230, 114, 23]
        else:
            return [161, 75, 12]

    elif "ENCLAVE" in tipo_norm:

        if nivel == "ALTA":
            return [72, 192, 104]
        elif nivel == "MEDIA":
            return [40, 145, 72]
        else:
            return [23, 101, 49]

    elif "VACIO" in tipo_norm:

        if nivel == "ALTA":
            return [108, 129, 150]
        elif nivel == "MEDIA":
            return [79, 98, 117]
        else:
            return [53, 68, 84]

    else:
        return [53, 68, 84]


# ======================================================
# LOOKUP ROBUSTO EXCEL ↔ GEOJSON
# ======================================================

lookup = df.set_index(
    "COMUNA_KEY"
).to_dict(
    "index"
)


# ======================================================
# GEOJSON SELECCIONADO
# ======================================================

selected_geojson = {
    "type": "FeatureCollection",
    "features": []
}


# ======================================================
# MAP DATA
# ======================================================

for feature in geojson["features"]:

    props = feature["properties"]

    comuna_geo_original = str(
        props.get(
            "Comuna",
            ""
        )
    ).upper()

    comuna_geo_key = normalizar_comuna(
        comuna_geo_original
    )

    if comuna_geo_key in lookup:

        row = lookup[comuna_geo_key]

        comuna_base = str(
            row.get(
                "COMUNA_LIMPIA",
                comuna_geo_original
            )
        ).upper()

        tipo = row["TIPOLOGIA_FINAL"]
        ipl = row["IPL_V3"]
        mit = row.get(
            "MIT_LOG",
            0
        )
        ranking_ipl = int(
            row.get(
                "RANKING_IPL_DASH",
                0
            )
        )
        nivel = nivel_intensidad_ipl(ipl)
        militantes = int(
            row.get(
                "MILITANTES_UDI",
                0
            )
        )

        feature["properties"]["COMUNA_LIMPIA"] = comuna_base
        feature["properties"]["TIPOLOGIA_WR"] = tipo
        feature["properties"]["COMUNA_TIPO_WR"] = f"{comuna_base} · {tipo}"
        feature["properties"]["IPL_NIVEL_WR"] = f"{round(float(ipl), 2)} · {nivel}"
        feature["properties"]["MIT_WR"] = round(
            float(mit),
            2
        )
        feature["properties"]["RANK_IPL_WR"] = f"#{ranking_ipl}"
        feature["properties"]["IPL_WR"] = round(
            float(ipl),
            2
        )
        feature["properties"]["NIVEL_IPL_WR"] = nivel
        feature["properties"]["MILITANTES_WR"] = militantes
        feature["properties"]["fill_color"] = color_tipologia_bandeado(
            tipo=tipo,
            ipl=ipl
        )

    else:

        feature["properties"]["COMUNA_LIMPIA"] = comuna_geo_original
        feature["properties"]["TIPOLOGIA_WR"] = "SIN DATA"
        feature["properties"]["COMUNA_TIPO_WR"] = f"{comuna_geo_original} · SIN DATA"
        feature["properties"]["IPL_NIVEL_WR"] = "0 · SIN DATA"
        feature["properties"]["MIT_WR"] = 0
        feature["properties"]["RANK_IPL_WR"] = "#0"
        feature["properties"]["IPL_WR"] = 0
        feature["properties"]["NIVEL_IPL_WR"] = "SIN DATA"
        feature["properties"]["MILITANTES_WR"] = 0
        feature["properties"]["fill_color"] = [42, 54, 66]

    if comuna_geo_key == normalizar_comuna(comuna):

        selected_geojson["features"].append(feature)


# ======================================================
# MAP LAYERS
# ======================================================

main_layer = pdk.Layer(
    "GeoJsonLayer",
    geojson,
    pickable=True,
    stroked=True,
    filled=True,
    opacity=0.78,
    get_fill_color="properties.fill_color",
    get_line_color=[15, 15, 15],
    line_width_min_pixels=1
)

highlight_layer = pdk.Layer(
    "GeoJsonLayer",
    selected_geojson,
    pickable=True,
    stroked=True,
    filled=True,
    opacity=0.98,
    get_fill_color="properties.fill_color",
    get_line_color=[255, 255, 255],
    line_width_min_pixels=4
)


# ======================================================
# VIEW STATE MAPA
# Encuadre inicial nacional estable
# ======================================================

view_state = pdk.ViewState(
    latitude=-37.2,
    longitude=-71.35,
    zoom=3.45,
    pitch=0,
    bearing=0
)


# ======================================================
# TOOLTIP
# ======================================================

tooltip = {
    "html": """
    <b>Comuna:</b> {COMUNA_TIPO_WR}<br/>
    <b>IPL:</b> {IPL_NIVEL_WR}<br/>
    <b>Militantes:</b> {MILITANTES_WR}<br/>
    <b>MIT:</b> {MIT_WR}<br/>
    <b>Rank IPL:</b> {RANK_IPL_WR}
    """,
    "style": {
        "backgroundColor": "#07111F",
        "color": "white",
        "fontSize": "13px"
    }
}


# ======================================================
# DECK
# ======================================================

deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v11",
    initial_view_state=view_state,
    layers=[
        main_layer,
        highlight_layer
    ],
    tooltip=tooltip,
    views=[
        pdk.View(
            type="MapView",
            controller={
                "dragPan": True,
                "scrollZoom": False,
                "touchZoom": True,
                "dragRotate": False,
                "touchRotate": False,
                "doubleClickZoom": True
            }
        )
    ]
)


# ======================================================
# LAYOUT PRINCIPAL
# ======================================================

left, center, right = st.columns(
    [1.25, 3.25, 2.35]
)


with left:

    comuna_click = render_ranking(
        df,
        comuna_actual=comuna,
        altura=ALTURA_RANKING
    )

    if comuna_click:

        st.session_state["comuna_actual"] = comuna_click
        force_rerun()


with center:

    with st.container(
        height=ALTURA_PRINCIPAL,
        border=False
    ):

        st.pydeck_chart(
            deck,
            use_container_width=True,
            height=ALTURA_PRINCIPAL
        )


with right:

    with st.container(
        height=ALTURA_PRINCIPAL,
        border=False
    ):

        render_ficha(fila)


# ======================================================
# PANEL REGIONAL
# ======================================================

region_actual = fila.get(
    "REGION_GEO",
    ""
)

df_region = df[
    df["REGION_GEO"] == region_actual
].copy()

total_comunas_region = len(
    df_region
)

total_militantes_region = int(
    df_region["MILITANTES_UDI"]
    .fillna(0)
    .sum()
)

ipl_promedio_region = round(
    df_region["IPL_V3"]
    .fillna(0)
    .mean(),
    2
)

mit_promedio_region = round(
    df_region["MIT_LOG"]
    .fillna(0)
    .mean(),
    2
)

bastiones_region = int(
    df_region["TIPOLOGIA_FINAL"]
    .astype(str)
    .str.contains(
        "BASTION",
        case=False,
        na=False
    )
    .sum()
)

reservas_region = int(
    df_region["TIPOLOGIA_FINAL"]
    .astype(str)
    .str.contains(
        "RESERVA",
        case=False,
        na=False
    )
    .sum()
)

enclaves_region = int(
    df_region["TIPOLOGIA_FINAL"]
    .astype(str)
    .str.contains(
        "ENCLAVE",
        case=False,
        na=False
    )
    .sum()
)

vacios_region = (
    total_comunas_region
    - bastiones_region
    - reservas_region
    - enclaves_region
)

top_ipl = df_region.sort_values(
    "IPL_V3",
    ascending=False
)

top_militancia = df_region.sort_values(
    "MILITANTES_UDI",
    ascending=False
)

ranking_regiones = (
    df
    .groupby(
        "REGION_GEO",
        as_index=False
    )
    .agg(
        IPL_PROM=("IPL_V3", "mean"),
        MIT_PROM=("MIT_LOG", "mean"),
        MILITANTES=("MILITANTES_UDI", "sum"),
        COMUNAS=("COMUNA_LIMPIA", "count")
    )
)

ranking_regiones["IPL_PROM"] = ranking_regiones["IPL_PROM"].round(2)
ranking_regiones["MIT_PROM"] = ranking_regiones["MIT_PROM"].round(2)

ranking_regiones["MILITANTES"] = (
    ranking_regiones["MILITANTES"]
    .fillna(0)
    .astype(int)
)

ranking_regiones = (
    ranking_regiones
    .sort_values(
        "MILITANTES",
        ascending=False
    )
    .reset_index(drop=True)
)


# ======================================================
# LECTURA REGIONAL COMPACTA
# ======================================================

def construir_lectura_regional(
    total_militantes,
    total_comunas,
    ipl_promedio,
    mit_promedio,
    bastiones,
    reservas,
    vacios,
    enclaves
):

    diagnostico = "Presencia UDI relevante con mezcla de comunas fuertes y zonas débiles."
    movimiento = "Priorizar comunas con mayor retorno y ordenar despliegue operativo."
    riesgo = "Dispersión territorial y baja conversión de base en estructura."

    if total_militantes >= 8000:

        diagnostico = "Bloque principal UDI: alta masa militante y peso nacional."
        movimiento = "Defender bastiones y convertir reservas en operación."
        riesgo = "Saturación en polos fuertes y baja eficiencia periférica."

    elif total_militantes >= 1800:

        diagnostico = "Región competitiva: buena base y margen de activación."
        movimiento = "Concentrar operación en bastiones y reservas."
        riesgo = "Militancia disponible sin conducción comunal suficiente."

    elif total_militantes >= 900:

        diagnostico = "Región media: presencia visible con brechas operativas."
        movimiento = "Construir polos comunales y responsables locales."
        riesgo = "Fragmentación y dependencia de liderazgos aislados."

    else:

        diagnostico = "Región de baja escala: requiere instalación selectiva."
        movimiento = "Elegir pocas comunas objetivo y levantar referentes."
        riesgo = "Baja masa crítica para sostener despliegue amplio."

    if reservas > bastiones:
        movimiento = movimiento + " Foco: reservas activables."

    if vacios + enclaves > bastiones + reservas:
        riesgo = riesgo + " Alto peso de vacíos/enclaves."

    if mit_promedio < 1.5 and total_militantes >= 1000:
        diagnostico = diagnostico + " Base mayor que capilaridad."

    return diagnostico, movimiento, riesgo


diagnostico_regional, movimiento_regional, riesgo_regional = construir_lectura_regional(
    total_militantes=total_militantes_region,
    total_comunas=total_comunas_region,
    ipl_promedio=ipl_promedio_region,
    mit_promedio=mit_promedio_region,
    bastiones=bastiones_region,
    reservas=reservas_region,
    vacios=vacios_region,
    enclaves=enclaves_region
)


# ======================================================
# FUNCIONES PANEL REGIONAL
# ======================================================

def construir_rows(tabla, columna, comuna_actual, decimales=2):

    html_rows = ""

    for i, (_, row) in enumerate(
        tabla.iterrows(),
        start=1
    ):

        comuna_row = row["COMUNA_LIMPIA"]
        valor = row[columna]

        if columna == "MILITANTES_UDI":
            valor_fmt = f"{int(valor)}"
        else:
            valor_fmt = f"{round(float(valor), decimales)}"

        clase_extra = ""

        if str(comuna_row).upper() == str(comuna_actual).upper():
            clase_extra = "commune-current"

        html_rows += f"""
        <div class="regional-row {clase_extra}">
            <div class="regional-rank">{i}</div>
            <div class="regional-commune">{comuna_row}</div>
            <div class="regional-value">{valor_fmt}</div>
        </div>
        """

    return html_rows


def construir_rows_regiones(tabla, region_actual):

    html_rows = ""

    for i, (_, row) in enumerate(
        tabla.iterrows(),
        start=1
    ):

        region = row["REGION_GEO"]
        valor = int(row["MILITANTES"])

        clase_extra = "region-current" if region == region_actual else ""

        html_rows += f"""
        <div class="regional-row {clase_extra}">
            <div class="regional-rank">{i}</div>
            <div class="regional-commune">{region}</div>
            <div class="regional-value">{valor}</div>
        </div>
        """

    return html_rows


rows_ipl = construir_rows(
    top_ipl,
    "IPL_V3",
    comuna_actual=comuna
)

rows_militancia = construir_rows(
    top_militancia,
    "MILITANTES_UDI",
    comuna_actual=comuna,
    decimales=0
)

rows_regiones = construir_rows_regiones(
    ranking_regiones,
    region_actual
)


# ======================================================
# RENDER PANEL REGIONAL
# ======================================================

html(
    f"""
    <div class="regional-panel">

        <div class="regional-head">

            <div class="regional-title-box">
                <div class="regional-title">
                    PANEL REGIONAL
                </div>

                <div class="regional-subtitle">
                    {region_actual}
                </div>
            </div>

            <div class="regional-reading-compact">

                <div class="regional-reading-title">
                    LECTURA ESTRATÉGICA REGIONAL
                </div>

                <div class="regional-reading-flow">

                    <div class="regional-read-mini">
                        <div class="regional-read-label">DIAGNÓSTICO</div>
                        <div class="regional-read-text">{diagnostico_regional}</div>
                    </div>

                    <div class="regional-read-mini">
                        <div class="regional-read-label">MOVIMIENTO</div>
                        <div class="regional-read-text">{movimiento_regional}</div>
                    </div>

                    <div class="regional-read-mini">
                        <div class="regional-read-label">RIESGO</div>
                        <div class="regional-read-text">{riesgo_regional}</div>
                    </div>

                </div>

            </div>

        </div>

        <div class="regional-kpi-strip">

            <div class="regional-kpi">
                <div class="regional-kpi-label">COMUNAS</div>
                <div class="regional-kpi-value">{total_comunas_region}</div>
            </div>

            <div class="regional-kpi">
                <div class="regional-kpi-label">MILITANTES</div>
                <div class="regional-kpi-value">{total_militantes_region}</div>
            </div>

            <div class="regional-kpi">
                <div class="regional-kpi-label">IPL PROM.</div>
                <div class="regional-kpi-value">{ipl_promedio_region}</div>
            </div>

            <div class="regional-kpi">
                <div class="regional-kpi-label">MIT PROM.</div>
                <div class="regional-kpi-value">{mit_promedio_region}</div>
            </div>

            <div class="regional-kpi">
                <div class="regional-kpi-label">BASTIONES</div>
                <div class="regional-kpi-value">{bastiones_region}</div>
            </div>

            <div class="regional-kpi">
                <div class="regional-kpi-label">RESERVAS</div>
                <div class="regional-kpi-value">{reservas_region}</div>
            </div>

            <div class="regional-kpi">
                <div class="regional-kpi-label">VAC / ENC</div>
                <div class="regional-kpi-value">{vacios_region} / {enclaves_region}</div>
            </div>

        </div>

        <div class="regional-ranking-grid">

            <div class="regional-ranking-box">
                <div class="regional-ranking-title">
                    TOP COMUNAS REGIÓN POR IPL
                </div>
                {rows_ipl}
            </div>

            <div class="regional-ranking-box">
                <div class="regional-ranking-title">
                    TOP COMUNAS REGIÓN POR MILITANCIA
                </div>
                {rows_militancia}
            </div>

            <div class="regional-ranking-box-scroll">
                <div class="regional-ranking-title">
                    RANKING REGIONES POR MILITANTES UDI
                </div>
                {rows_regiones}
            </div>

        </div>

    </div>
    """
)