import streamlit as st

from utils.interpretacion import (
    interpretar_tipologia
)

# ======================================================
# FICHA TERRITORIAL
# ======================================================

def render_ficha(fila):

    comuna = fila["COMUNA_LIMPIA"]

    region = fila.get(
        "REGION_GEO",
        "Sin región"
    )

    tipo = fila["TIPOLOGIA_FINAL"]

    ranking = int(
        fila["RANKING_NACIONAL"]
    )

    ipl = round(
        float(fila["IPL_V3"]),
        4
    )

    mit = round(
        float(fila["MIT_LOG"]),
        1
    )

    militancia = int(
        fila["MILITANTES_UDI"]
    )

    interpretacion = interpretar_tipologia(tipo)

    # ==================================================
    # COLOR
    # ==================================================

    color = "#455A64"

    if "BASTION" in tipo.upper():
        color = "#1976D2"

    elif "RESERVA" in tipo.upper():
        color = "#EF6C00"

    elif "ENCLAVE" in tipo.upper():
        color = "#FBC02D"

    # ==================================================
    # HEADER
    # ==================================================

    st.markdown(
        f"""
<div style="margin-bottom:6px;">

<div style="
font-size:32px;
font-weight:900;
line-height:1;
color:#F5F5F5;
">
{comuna}
</div>

<div style="
font-size:14px;
color:#B0BEC5;
margin-top:2px;
">
{region}
</div>

</div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # BADGE
    # ==================================================

    st.markdown(
        f"""
<div style="
background:{color};
color:white;
padding:6px 10px;
border-radius:8px;
font-size:11px;
font-weight:700;
display:inline-block;
margin-bottom:10px;
">
{tipo}
</div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # KPIs
    # ==================================================

    st.markdown(
        f"""
<div style="
font-size:13px;
line-height:1.05;
color:#F5F5F5;
margin-bottom:12px;
">

<b>RANKING WAR ROOM</b><br>
{ranking}<br><br>

<b>IPL WAR ROOM</b><br>
{ipl}<br><br>

<b>MIT SCORE</b><br>
{mit}<br><br>

<b>MILITANTES UDI</b><br>
{militancia}

</div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # ESTRUCTURA
    # ==================================================

    st.markdown(
        """
<div style="
font-size:17px;
font-weight:800;
margin-bottom:6px;
color:#F5F5F5;
">
ESTRUCTURA OPERATIVA
</div>
        """,
        unsafe_allow_html=True
    )

    alcalde = fila.get("ALCALDE", 0)
    concejal = fila.get("CONCEJAL", 0)
    core = fila.get("CORE", 0)
    diputado = fila.get("DIPUTADO", 0)
    senador = fila.get("SENADOR", 0)
    gobernador = fila.get("GOBERNADOR", 0)

    total = (
        alcalde +
        concejal +
        core +
        diputado +
        senador +
        gobernador
    )

    st.markdown(
        f"""
<div style="
font-size:13px;
line-height:1.05;
color:#F5F5F5;
margin-bottom:12px;
">

ALCALDES: {int(alcalde)}<br>
CONCEJALES: {int(concejal)}<br>
CORES: {int(core)}<br>
DIPUTADOS: {int(diputado)}<br>
SENADORES: {int(senador)}<br>
GOBERNADOR: {int(gobernador)}<br>
TOTAL AUTORIDADES: {int(total)}

</div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # ALERTA
    # ==================================================

    alerta = "⚫ Baja presencia territorial."

    if "BASTION" in tipo.upper():
        alerta = "🔵 Alta militancia y alta capilaridad territorial."

    elif "RESERVA" in tipo.upper():
        alerta = "🟠 Alta militancia con baja estructura operativa."

    elif "ENCLAVE" in tipo.upper():
        alerta = "🟡 Alta estructura con base orgánica limitada."

    st.markdown(
        """
<div style="
font-size:17px;
font-weight:800;
margin-bottom:6px;
color:#F5F5F5;
">
LECTURA TÁCTICA
</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div style="
padding:8px;
border-radius:8px;
background:#0F1C2E;
border-left:4px solid #1E88E5;
font-size:12px;
line-height:1.15;
color:#F5F5F5;
margin-bottom:12px;
">
{alerta}
</div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # INTERPRETACION
    # ==================================================

    st.markdown(
        """
<div style="
font-size:17px;
font-weight:800;
margin-bottom:6px;
color:#F5F5F5;
">
INTERPRETACIÓN WAR ROOM
</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div style="
font-size:12px;
line-height:1.2;
color:#E0E0E0;
white-space:normal;
word-break:break-word;
overflow-wrap:break-word;
margin-bottom:18px;
">

{interpretacion}

</div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # GLOSARIO
    # ==================================================

    st.markdown(
        """
<div style="
font-size:16px;
font-weight:800;
margin-bottom:10px;
color:#F5F5F5;
">
━━━━━━━━━━━━<br>
GLOSARIO WAR ROOM<br>
━━━━━━━━━━━━
</div>

<div style="
font-size:11px;
line-height:1.35;
color:#B0BEC5;
">

<b style="font-size:13px;color:#F5F5F5;">IPL</b><br>
Índice Potencial Longueira.<br>
Capacidad potencial de activación territorial.<br><br>

<b style="font-size:13px;color:#F5F5F5;">MIT</b><br>
Modelo de Implantación Territorial.<br>
Capilaridad operativa UDI en el territorio.<br><br>

<div style="
display:flex;
align-items:center;
gap:8px;
margin-bottom:4px;
">
<div style="
width:10px;
height:10px;
border-radius:50%;
background:#1976D2;
"></div>

<b style="font-size:13px;color:#F5F5F5;">
BASTIÓN OPERATIVO
</b>
</div>

Alta militancia + alta estructura territorial.<br><br>

<div style="
display:flex;
align-items:center;
gap:8px;
margin-bottom:4px;
">
<div style="
width:10px;
height:10px;
border-radius:50%;
background:#EF6C00;
"></div>

<b style="font-size:13px;color:#F5F5F5;">
RESERVA ACTIVABLE
</b>
</div>

Alta militancia + baja capilaridad operativa.<br><br>

<div style="
display:flex;
align-items:center;
gap:8px;
margin-bottom:4px;
">
<div style="
width:10px;
height:10px;
border-radius:50%;
background:#FBC02D;
"></div>

<b style="font-size:13px;color:#F5F5F5;">
ENCLAVE OPERATIVO
</b>
</div>

Alta estructura + baja base militante.<br><br>

<div style="
display:flex;
align-items:center;
gap:8px;
margin-bottom:4px;
">
<div style="
width:10px;
height:10px;
border-radius:50%;
background:#455A64;
"></div>

<b style="font-size:13px;color:#F5F5F5;">
VACÍO TERRITORIAL
</b>
</div>

Baja presencia orgánica y baja estructura.

</div>
        """,
        unsafe_allow_html=True
    )