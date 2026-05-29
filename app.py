import json
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

# ======================================================
# CSS
# ======================================================

st.markdown(
    dedent(
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
            padding-top: 0.4rem;
            padding-bottom: 1rem;
        }

        .war-title {
            font-size: 58px;
            font-weight: 900;
            color: #F5F5F5;
            letter-spacing: -2px;
            line-height: 1;
            margin-top: 72px;
            white-space: nowrap;
        }

        .war-strip {
            display: flex;
            align-items: center;
            gap: 24px;
            width: 100%;
            margin-top: -8px;
            margin-bottom: 8px;
            padding: 8px 0 4px 0;
            font-size: 12px;
            letter-spacing: 1.1px;
            color: #D7DEE8;
            opacity: 0.95;
            white-space: nowrap;
        }

        .war-strip span {
            display: inline-block;
        }

        .war-strip b {
            color: #FFFFFF;
            font-size: 18px;
            font-weight: 900;
            margin-right: 4px;
        }

        .war-separator {
            opacity: 0.35;
        }
        </style>
        """
    ),
    unsafe_allow_html=True
)

# ======================================================
# DATA
# ======================================================

@st.cache_data
def load_data():
    return pd.read_excel("data/WAR_ROOM_CORE_V3.xlsx")


@st.cache_data
def load_geojson():
    with open("data/chile_comunas.geojson", "r", encoding="utf-8") as f:
        return json.load(f)


df = load_data()
geojson = load_geojson()

df["COMUNA_LIMPIA"] = df["COMUNA_LIMPIA"].astype(str).str.upper()

# ======================================================
# METRICAS HEADER MANUALES
# ======================================================

TOTAL_MUNICIPIOS = 345
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

logo_col, title_col = st.columns(
    [1.55, 5.45]
)

with logo_col:
    st.image(
        "assets/logo_20k.png",
        width=285
    )

with title_col:
    st.markdown(
        dedent(
            """
            <div class="war-title">
                WAR ROOM
            </div>
            """
        ),
        unsafe_allow_html=True
    )

# ======================================================
# INDICADORES SUPERIORES
# ======================================================

st.markdown(
    dedent(
        f"""
        <div class="war-strip">
            <span><b>{TOTAL_MUNICIPIOS}</b> MUNICIPIOS</span>
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
        """
    ),
    unsafe_allow_html=True
)

# ======================================================
# SELECTOR
# ======================================================

comuna = st.selectbox(
    "Seleccionar comuna",
    sorted(df["COMUNA_LIMPIA"].unique())
)

fila = df[df["COMUNA_LIMPIA"] == comuna].iloc[0]

# ======================================================
# COLOR FUNCTION
# ======================================================

def color_tipologia(tipo):
    tipo = str(tipo).upper()

    if "BASTION" in tipo:
        return [25, 118, 210]
    elif "RESERVA" in tipo:
        return [239, 108, 0]
    elif "ENCLAVE" in tipo:
        return [251, 192, 45]
    else:
        return [69, 90, 100]


# ======================================================
# LOOKUP
# ======================================================

lookup = df.set_index("COMUNA_LIMPIA").to_dict("index")

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

    comuna_geo = str(props.get("Comuna", "")).upper()

    feature["properties"]["COMUNA_LIMPIA"] = comuna_geo

    if comuna_geo in lookup:

        row = lookup[comuna_geo]

        tipo = row["TIPOLOGIA_FINAL"]
        ipl = row["IPL_V3"]

        feature["properties"]["TIPOLOGIA_WR"] = tipo
        feature["properties"]["IPL_WR"] = round(float(ipl), 2)
        feature["properties"]["fill_color"] = color_tipologia(tipo)

    else:

        feature["properties"]["TIPOLOGIA_WR"] = "SIN DATA"
        feature["properties"]["IPL_WR"] = 0
        feature["properties"]["fill_color"] = [69, 90, 100]

    if comuna_geo == comuna:

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
    opacity=0.30,
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
    opacity=0.95,
    get_fill_color="properties.fill_color",
    get_line_color=[255, 255, 255],
    line_width_min_pixels=4
)

# ======================================================
# VIEW STATE
# ======================================================

view_state = pdk.ViewState(
    latitude=-35.5,
    longitude=-71.0,
    zoom=3.4,
    pitch=0
)

# ======================================================
# TOOLTIP
# ======================================================

tooltip = {
    "html": """
    <b>Comuna:</b> {COMUNA_LIMPIA}<br/>
    <b>Tipología:</b> {TIPOLOGIA_WR}<br/>
    <b>IPL:</b> {IPL_WR}
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
    tooltip=tooltip
)

# ======================================================
# LAYOUT
# ======================================================

left, center, right = st.columns(
    [1.3, 4.2, 1.4]
)

with left:

    render_ranking(df)

with center:

    st.pydeck_chart(
        deck,
        use_container_width=True,
        height=1450
    )

with right:

    render_ficha(fila)

# ======================================================
# WATERMARK
# ======================================================

st.markdown(
    dedent(
        """
        <div style="
            position:fixed;
            bottom:10px;
            right:18px;
            opacity:0.12;
            font-size:14px;
            font-weight:700;
            color:white;
            z-index:9999;
            letter-spacing:1px;
        ">
            MDiazCassis
        </div>
        """
    ),
    unsafe_allow_html=True
)