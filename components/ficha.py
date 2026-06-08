import re
import pandas as pd
import streamlit as st
from textwrap import dedent

from utils.interpretacion import interpretar_tipologia


# ======================================================
# HELPERS
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


def safe_int(value, default=0):
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def pct(value):
    try:
        value = safe_float(value)
        return f"{round(value * 100, 1)}%"
    except Exception:
        return "0.0%"


def clean_text(value, default="Sin información"):
    try:
        if pd.isna(value):
            return default

        value = str(value).strip()

        if value == "":
            return default

        return value

    except Exception:
        return default


def construir_url_sinim(fila):

    codigo = fila.get(
        "CODIGO_SINIM",
        ""
    )

    if pd.isna(codigo) or str(codigo).strip() == "":
        url_guardada = fila.get(
            "URL_SINIM",
            ""
        )

        if pd.isna(url_guardada) or str(url_guardada).strip() == "":
            return ""

        match = re.search(
            r"municipio=([0-9]+)",
            str(url_guardada)
        )

        if not match:
            return ""

        codigo = match.group(1)

    codigo_str = str(codigo).strip()

    if codigo_str.lower() == "nan" or codigo_str == "":
        return ""

    if "." in codigo_str:
        try:
            codigo_str = str(
                int(
                    float(codigo_str)
                )
            )
        except Exception:
            codigo_str = codigo_str.split(".")[0]

    codigo_str = re.sub(
        r"[^0-9]",
        "",
        codigo_str
    )

    if codigo_str == "":
        return ""

    codigo_str = codigo_str.zfill(5)

    return (
        "https://datos.sinim.gov.cl/impresion_ficha_comunal.php"
        f"?municipio={codigo_str}&provincia=T&region=T"
    )


def construir_proximo_movimiento(tipo, militancia, total_autoridades, senior_val, sub40_val):

    tipo_upper = str(tipo).upper()

    prioridad = "Media"
    accion = "Ordenar despliegue territorial"
    canal = "Referentes locales + contacto directo"
    foco = "Activar base comunal y validar red territorial"
    riesgo = "Baja conversión entre presencia política y movilización efectiva"
    color_movimiento = "#1E88E5"

    if "BASTION" in tipo_upper:

        prioridad = "Alta / Defender y movilizar"
        accion = "Consolidar operación comunal"
        canal = "Autoridades locales + red militante activa"
        foco = "Asegurar participación, disciplina territorial y despliegue temprano"
        riesgo = "Sobreconfianza o desmovilización por ventaja estructural"
        color_movimiento = "#1976D2"

    elif "RESERVA" in tipo_upper:

        prioridad = "Alta / Activar estructura"
        accion = "Convertir militancia en operación"
        canal = "Base militante + referentes comunales"
        foco = "Levantar responsables territoriales y reforzar conducción local"
        riesgo = "Alta base sin suficiente estructura de mando"
        color_movimiento = "#EF6C00"

    elif "ENCLAVE" in tipo_upper:

        prioridad = "Media / Expandir base"
        accion = "Usar estructura existente para crecer"
        canal = "Autoridades UDI + redes comunitarias"
        foco = "Reclutar, ordenar base nueva y transformar presencia en militancia"
        riesgo = "Estructura política sin masa militante suficiente"
        color_movimiento = "#FBC02D"

    elif "VACIO" in tipo_upper or "VACÍO" in tipo_upper:

        prioridad = "Baja táctica / Monitoreo"
        accion = "Instalación territorial gradual"
        canal = "Contacto directo + redes locales"
        foco = "Identificar referentes y construir presencia comunal mínima"
        riesgo = "Baja base orgánica y dependencia de autoridades supracomunales"
        color_movimiento = "#455A64"

    if senior_val >= 0.70:
        foco = foco + " · Priorizar base 50+"
        canal = canal + " · llamados personalizados"

    if sub40_val <= 0.10:
        riesgo = riesgo + " · baja renovación Sub40"

    if militancia <= 30 and total_autoridades <= 1:
        accion = "Instalación territorial de baja intensidad"
        riesgo = "Muy baja masa crítica local"

    return {
        "prioridad": prioridad,
        "accion": accion,
        "canal": canal,
        "foco": foco,
        "riesgo": riesgo,
        "color": color_movimiento
    }


# ======================================================
# FICHA TERRITORIAL
# ======================================================

def render_ficha(fila):

    comuna = fila["COMUNA_LIMPIA"]
    region = fila.get("REGION_GEO", "Sin región")
    tipo = fila["TIPOLOGIA_FINAL"]

    ranking_ipl = safe_int(fila.get("RANKING_IPL_DASH", 0))
    ranking_mit = safe_int(fila.get("RANKING_MIT_DASH", 0))
    ranking_militancia = safe_int(fila.get("RANKING_MILITANCIA_DASH", 0))

    militancia = safe_int(fila.get("MILITANTES_UDI", 0))

    url_sinim = construir_url_sinim(fila)

    interpretacion = interpretar_tipologia(tipo)

    color = "#455A64"

    if "BASTION" in tipo.upper():
        color = "#1976D2"
    elif "RESERVA" in tipo.upper():
        color = "#EF6C00"
    elif "ENCLAVE" in tipo.upper():
        color = "#FBC02D"

    # ==================================================
    # DATOS ESTRUCTURA
    # ==================================================

    alcalde = safe_int(fila.get("ALCALDE", 0))
    concejal = safe_int(fila.get("CONCEJAL", 0))
    core = safe_int(fila.get("CORE", 0))
    diputado = safe_int(fila.get("DIPUTADO", 0))
    senador = safe_int(fila.get("SENADOR", 0))
    gobernador = safe_int(fila.get("GOBERNADOR", 0))

    total_autoridades = (
        alcalde
        + concejal
        + core
        + diputado
        + senador
        + gobernador
    )

    # ==================================================
    # DATOS PERFIL
    # ==================================================

    perfil_total = safe_int(
        fila.get(
            "MILITANTES_PERFIL_TOTAL",
            militancia
        )
    )

    mujeres_pct = pct(fila.get("MUJERES_PCT", 0))
    hombres_pct = pct(fila.get("HOMBRES_PCT", 0))

    tramo_dominante = clean_text(
        fila.get(
            "TRAMO_DOMINANTE",
            "Sin información"
        )
    )

    tramo_pct = pct(
        fila.get(
            "TRAMO_DOMINANTE_PCT",
            0
        )
    )

    edad_promedio = round(
        safe_float(
            fila.get(
                "EDAD_PROMEDIO_APROX",
                0
            )
        ),
        1
    )

    sub40_val = safe_float(
        fila.get(
            "SUB40_PCT",
            0
        )
    )

    senior_val = safe_float(
        fila.get(
            "SENIOR_50MAS_PCT",
            0
        )
    )

    sub40_pct = pct(sub40_val)
    senior_pct = pct(senior_val)

    lectura_activacion = clean_text(
        fila.get(
            "LECTURA_ACTIVACION",
            "Sin lectura de activación disponible."
        )
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

    # ==================================================
    # PRÓXIMO MOVIMIENTO
    # ==================================================

    movimiento = construir_proximo_movimiento(
        tipo=tipo,
        militancia=militancia,
        total_autoridades=total_autoridades,
        senior_val=senior_val,
        sub40_val=sub40_val
    )

    prioridad = movimiento["prioridad"]
    accion = movimiento["accion"]
    canal = movimiento["canal"]
    foco = movimiento["foco"]
    riesgo = movimiento["riesgo"]
    color_movimiento = movimiento["color"]

    # ==================================================
    # HEADER
    # ==================================================

    html(
        f"""
        <div style="margin-bottom:8px;">
            <div style="font-size:32px;font-weight:900;line-height:0.95;color:#F5F5F5;letter-spacing:0.5px;">
                {comuna}
            </div>
            <div style="font-size:13px;color:#B0BEC5;margin-top:5px;">
                {region}
            </div>
        </div>

        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
            <div style="background:{color};color:white;padding:7px 12px;border-radius:9px;font-size:11px;font-weight:900;display:inline-block;">
                {tipo}
            </div>
        """
    )

    if url_sinim:

        html(
            f"""
            <a href="{url_sinim}" target="_blank" style="
                display:inline-block;
                text-decoration:none;
                background:#0B1728;
                border:1px solid rgba(255,255,255,0.18);
                color:#F5F5F5;
                padding:7px 12px;
                border-radius:9px;
                font-size:11px;
                font-weight:900;
                letter-spacing:0.4px;
            ">
                FICHA SINIM ↗
            </a>
            </div>
            """
        )

    else:

        html(
            """
            <div style="
                display:inline-block;
                background:#111827;
                border:1px solid rgba(255,255,255,0.08);
                color:#78909C;
                padding:7px 12px;
                border-radius:9px;
                font-size:11px;
                font-weight:800;
                letter-spacing:0.4px;
            ">
                SINIM NO DISPONIBLE
            </div>
            </div>
            """
        )

    # ==================================================
    # KPI PANEL COMPACTO
    # ==================================================

    html(
        f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:13px;">
            <div style="background:#07111F;border:1px solid rgba(255,255,255,0.10);border-radius:9px;padding:9px 9px 8px 9px;">
                <div style="font-size:9px;letter-spacing:0.8px;color:#B0BEC5;font-weight:900;">RANK IPL</div>
                <div style="font-size:20px;font-weight:900;color:#F5F5F5;line-height:1.05;margin-top:3px;">{ranking_ipl}</div>
            </div>

            <div style="background:#07111F;border:1px solid rgba(255,255,255,0.10);border-radius:9px;padding:9px 9px 8px 9px;">
                <div style="font-size:9px;letter-spacing:0.8px;color:#B0BEC5;font-weight:900;">RANK MIT</div>
                <div style="font-size:20px;font-weight:900;color:#F5F5F5;line-height:1.05;margin-top:3px;">{ranking_mit}</div>
            </div>

            <div style="background:#07111F;border:1px solid rgba(255,255,255,0.10);border-radius:9px;padding:9px 9px 8px 9px;">
                <div style="font-size:9px;letter-spacing:0.8px;color:#B0BEC5;font-weight:900;">RANK MIL.</div>
                <div style="font-size:20px;font-weight:900;color:#F5F5F5;line-height:1.05;margin-top:3px;">{ranking_militancia}</div>
            </div>

            <div style="background:#07111F;border:1px solid rgba(255,255,255,0.10);border-radius:9px;padding:9px 9px 8px 9px;">
                <div style="font-size:9px;letter-spacing:0.8px;color:#B0BEC5;font-weight:900;">MILITANTES</div>
                <div style="font-size:20px;font-weight:900;color:#F5F5F5;line-height:1.05;margin-top:3px;">{militancia}</div>
            </div>
        </div>
        """
    )

    # ==================================================
    # RADIOGRAFÍA OPERATIVA COMPACTA
    # Reemplaza las dos cajas grandes:
    # - Estructura Operativa
    # - Perfil Militante
    # ==================================================

    html(
        f"""
        <div style="font-size:15px;font-weight:900;margin-bottom:7px;color:#F5F5F5;letter-spacing:0.5px;">
            RADIOGRAFÍA OPERATIVA
        </div>

        <div style="
            background:#07111F;
            border:1px solid rgba(255,255,255,0.10);
            border-radius:10px;
            padding:11px 12px 10px 12px;
            margin-bottom:14px;
            color:#F5F5F5;
        ">

            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                gap:8px;
                padding-bottom:9px;
                margin-bottom:9px;
                border-bottom:1px solid rgba(255,255,255,0.10);
            ">
                <div style="font-size:11px;color:#B0BEC5;font-weight:900;letter-spacing:0.7px;">
                    AUTORIDADES
                </div>

                <div style="font-size:18px;font-weight:900;color:#F5F5F5;">
                    {total_autoridades}
                </div>

                <div style="font-size:11px;color:#B0BEC5;font-weight:900;letter-spacing:0.7px;">
                    BASE 50+
                </div>

                <div style="font-size:18px;font-weight:900;color:#F5F5F5;">
                    {senior_pct}
                </div>

                <div style="font-size:11px;color:#B0BEC5;font-weight:900;letter-spacing:0.7px;">
                    SUB40
                </div>

                <div style="font-size:18px;font-weight:900;color:#F5F5F5;">
                    {sub40_pct}
                </div>
            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(6,1fr);
                gap:6px;
                margin-bottom:9px;
            ">

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">ALC</div>
                    <div style="font-size:15px;font-weight:900;">{alcalde}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">CON</div>
                    <div style="font-size:15px;font-weight:900;">{concejal}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">CORE</div>
                    <div style="font-size:15px;font-weight:900;">{core}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">DIP</div>
                    <div style="font-size:15px;font-weight:900;">{diputado}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">SEN</div>
                    <div style="font-size:15px;font-weight:900;">{senador}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">GOB</div>
                    <div style="font-size:15px;font-weight:900;">{gobernador}</div>
                </div>

            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(5,1fr);
                gap:6px;
            ">

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">TOTAL</div>
                    <div style="font-size:15px;font-weight:900;">{perfil_total}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">EDAD</div>
                    <div style="font-size:15px;font-weight:900;">{edad_promedio}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">TRAMO</div>
                    <div style="font-size:14px;font-weight:900;">{tramo_dominante}</div>
                    <div style="font-size:9px;color:#B0BEC5;margin-top:1px;">{tramo_pct}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">MUJ.</div>
                    <div style="font-size:15px;font-weight:900;">{mujeres_pct}</div>
                </div>

                <div style="background:#0B1728;border-radius:7px;padding:6px 5px;text-align:center;">
                    <div style="font-size:9px;color:#B0BEC5;font-weight:900;">HOM.</div>
                    <div style="font-size:15px;font-weight:900;">{hombres_pct}</div>
                </div>

            </div>

        </div>
        """
    )

    # ==================================================
    # LECTURAS
    # ==================================================

    html(
        f"""
        <div style="font-size:16px;font-weight:900;margin-bottom:8px;color:#F5F5F5;letter-spacing:0.4px;">
            LECTURA TÁCTICA
        </div>

        <div style="padding:10px 13px;border-radius:9px;background:#0F1C2E;border-left:5px solid #1E88E5;font-size:14px;line-height:1.40;color:#F5F5F5;margin-bottom:14px;">
            {alerta}
        </div>

        <div style="font-size:16px;font-weight:900;margin-bottom:8px;color:#F5F5F5;letter-spacing:0.4px;">
            LECTURA DE ACTIVACIÓN
        </div>

        <div style="padding:13px 15px;border-radius:9px;background:#111D2F;border-left:5px solid #EF6C00;font-size:14px;line-height:1.48;color:#E8EEF5;white-space:normal;word-break:normal;overflow-wrap:break-word;margin-bottom:16px;">
            {lectura_activacion}
        </div>

        <div style="font-size:16px;font-weight:900;margin-bottom:8px;color:#F5F5F5;letter-spacing:0.4px;">
            INTERPRETACIÓN WAR ROOM
        </div>

        <div style="font-size:14px;line-height:1.48;color:#E8EEF5;white-space:normal;word-break:normal;overflow-wrap:break-word;margin-bottom:16px;">
            {interpretacion}
        </div>
        """
    )

    # ==================================================
    # PRÓXIMO MOVIMIENTO
    # ==================================================

    html(
        f"""
        <div style="height:1px;background:rgba(255,255,255,0.28);width:38%;margin:12px 0 11px 0;"></div>

        <div style="font-size:16px;font-weight:900;margin-bottom:8px;color:#F5F5F5;letter-spacing:0.4px;">
            PRÓXIMO MOVIMIENTO
        </div>

        <div style="
            background:#07111F;
            border:1px solid rgba(255,255,255,0.10);
            border-left:5px solid {color_movimiento};
            border-radius:9px;
            padding:12px 13px;
            color:#E8EEF5;
            margin-bottom:4px;
        ">

            <div style="display:grid;grid-template-columns:84px 1fr;gap:6px 10px;font-size:12.5px;line-height:1.34;">

                <div style="color:#B0BEC5;font-weight:900;letter-spacing:0.5px;">
                    PRIORIDAD
                </div>
                <div style="font-weight:900;color:#F5F5F5;">
                    {prioridad}
                </div>

                <div style="color:#B0BEC5;font-weight:900;letter-spacing:0.5px;">
                    ACCIÓN
                </div>
                <div>
                    {accion}
                </div>

                <div style="color:#B0BEC5;font-weight:900;letter-spacing:0.5px;">
                    CANAL
                </div>
                <div>
                    {canal}
                </div>

                <div style="color:#B0BEC5;font-weight:900;letter-spacing:0.5px;">
                    FOCO
                </div>
                <div>
                    {foco}
                </div>

                <div style="color:#B0BEC5;font-weight:900;letter-spacing:0.5px;">
                    RIESGO
                </div>
                <div>
                    {riesgo}
                </div>

            </div>
        </div>
        """
    )