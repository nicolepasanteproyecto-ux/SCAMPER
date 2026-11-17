# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 10:48:27 2026

@author: practicante-im
"""

import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import random
import time
import math

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==============================================================================
st.set_page_config(
    page_title="Ruleta SCAMPER - Innovación",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f8f9fa;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}
.titulo-scamper {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: #212529;
    letter-spacing: 3px;
    margin-bottom: 2px;
}
.subtitulo-estado {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    font-weight: 500;
    color: #6c757d;
    margin-bottom: 10px;
}
.barra-vidas {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin: 8px 0 18px 0;
}
.chip-vida {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 20px;
    padding: 5px 12px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.panel-historial {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 18px 15px;
    min-height: 340px;
    max-height: 360px;
    overflow-y: auto;
    margin-bottom: 14px;
}
.panel-qr {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 16px 15px;
    text-align: center;
}
.titulo-historial {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #343a40;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
}
.item-historial {
    background-color: #f1f3f5;
    color: #212529;
    padding: 9px 12px;
    margin-bottom: 8px;
    border-radius: 8px;
    border-left: 5px solid #0d6efd;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    font-weight: 700;
}
div.stButton > button {
    border-radius: 10px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
    font-size: 16px;
    padding: 14px 20px;
    border: none;
}
div.stButton > button[kind="primary"] {
    background-color: #0d6efd;
    color: white;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #0b5ed7;
}
div.stButton > button[kind="secondary"] {
    background-color: #e9ecef;
    color: #495057;
}
div.stButton > button[kind="secondary"]:hover {
    background-color: #dee2e6;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BANCO OFICIAL DE PREGUNTAS DETONADORAS SCAMPER (GRUPO PURDY)
# ==============================================================================
DATOS_SCAMPER = [
    {
        "letra": "S", "nombre": "SUSTITUIR", "color": "#dc3545", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué parte del proceso de [área / producto] que hace una persona podríamos cambiar para que lo haga directamente el cliente?",
            "¿Qué hábito o vicio de trabajo antiguo en [área / equipo] podemos cambiar por una regla simple de agilidad?",
            "¿Qué canal tradicional de atención o comunicación en [área] podemos sustituir por una alternativa digital o automatizada?",
            "¿Qué insumo o recurso de un solo uso en [proceso / área] podemos cambiar por una opción reutilizable o digital?",
            "¿Qué métrica tradicional en [área] podemos sustituir por un indicador que realmente mida el valor entregado?",
            "¿Qué trámite o burocracia interna en [área] podemos sustituir por un flujo de aprobación inmediato y transparente?",
            "¿Qué paso del proceso de [área] que genera estrés podemos sustituir por una experiencia guiada y amable?",
            "¿Qué capacitación o instructivo extenso en [área / proceso] podemos sustituir por un formato interactivo o una guía rápida paso a paso?"
        ]
    },
    {
        "letra": "C", "nombre": "COMBINAR", "color": "#fd7e14", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué dos pasos o trámites consecutivos en [área / proceso] podemos combinar en una sola acción de un clic?",
            "¿Qué datos o información que hoy pedimos por separado en [proceso] podemos recolectar en un único formulario o punto de contacto?",
            "¿Qué beneficio o incentivo de bienestar podemos combinar con una meta u objetivo de trabajo en [área]?",
            "¿Qué dos indicadores o métricas de [área] podemos combinar para medir el impacto real en una sola mirada?",
            "¿Qué tarea de [área A] podemos combinar con el flujo de [área B] para evitar que el cliente explique su caso dos veces?",
            "¿Qué base de conocimientos estática y chat de consultas frecuentes en [área] podemos integrar en una sola plataforma inteligente?",
            "¿Qué evaluación de desempeño y revisión de clima laboral en [área] podemos combinar en una sola conversación de acompañamiento?",
            "¿Qué reunión de traspaso de proyectos entre [área A] y [área B] podemos combinar con un espacio informal de integración para el equipo?"
        ]
    },
    {
        "letra": "A", "nombre": "ADAPTAR", "color": "#ffc107", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué herramienta o función digital que ya usamos individualmente podemos adaptar como estándar oficial en [área/proceso] para automatizar tareas repetitivas?",
            "Adaptemos un estándar externo: Identifiquen un proceso, plantilla o regla ágil que otra área de la empresa o industria ejecute en pocos minutos y adáptalo hoy mismo a [área/proceso].",
            "¿Qué solución aplicada temporalmente durante una emergencia o contingencia operativa podemos adaptar para convertirla en un estándar permanente en [área]?",
            "Si adaptamos la lógica de notificaciones automáticas o alertas de una app de uso diario, ¿en qué parte de [proceso] la pondremos para avisar únicamente cuando se requiere intervenir?",
            "Para evitar cuellos de botella por firmas o aprobaciones, ¿qué criterio de autorización directa o montos límite de otro proceso exitoso podemos adaptar aquí?",
            "¿Qué experiencia de autogestión o autoservicio de otra plataforma podemos adaptar para que los requerimientos internos se resuelvan sin depender de intermediarios?",
            "Desarrollemos un formato de guía visual rápida o lista de verificación (checklist) de un solo paso a paso que permita ejecutar [proceso] sin margen de error ni curvas de aprendizaje largas.",
            "Si adaptamos un tablero visual transparente de prioridades (donde todo el equipo ve el estado real de las tareas sin mandar correos), ¿cuáles 3 indicadores clave podríamos ahí?"
        ]
    },
    {
        "letra": "M", "nombre": "MODIFICAR", "color": "#28a745", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "Modifiquemos la escala: Si simplificamos x10 la visibilidad del trabajo de [área], ¿qué tablero o panel deberíamos instalar para que toda la empresa entienda nuestro impacto?",
            "Si modificamos la secuencia de [proceso] invirtiendo el orden de los pasos (por ejemplo, validar primero antes de solicitar insumos), ¿qué error o retrabajo evitaríamos?",
            "¿Qué nivel de detalle o precisión innecesaria en los reportes de [proceso] podemos minimizar para enfocarnos solo en los datos que mueven la toma de decisiones?",
            "¿Qué parámetro o criterio de decisión en [proyecto] podemos modificar para que el equipo apruebe o descarte una prueba piloto en menos de 24 horas?",
            "Modifiquemos la escala del piloto: Si redujeramos el alcance de [propuesta] a su versión más mínima y rápida de probar (PMV), ¿qué datos reales necesitaríamos para decidir en la mesa si escalarla o descartarla?",
            "Si modificamos la asignación de recursos para que el equipo de innovación tenga un \"fondo ciego\" o presupuesto preapropiado para micro-pilotos de 48 horas, ¿qué tantas pruebas más podríamos ejecutar este mes?",
            "Modifiquemos la estructura del pitch: Tomen la presentación de [proyecto / idea] y modifiquen para que dure máximo 3 minutos: 1 minuto para el problema, 1 minuto para la hipótesis de solución y 1 minuto para la decisión exacta que necesita el equipo.",
            "¿Qué parámetro o tolerancia de riesgo en [proyecto / idea] podemos modificar para tomar la decisión de lanzar una prueba piloto con un 70% de certeza en lugar de esperar datos completos?"
        ]
    },
    {
        "letra": "P", "nombre": "PONER OTROS USOS", "color": "#17a2b8", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "Si pusiéramos en otro uso el canal de comunicación o retroalimentación que hoy usamos para quejas de clientes, ¿cómo podríamos adaptarlo para capturar ideas rápidas de innovación de los colaboradores?",
            "¿Qué herramienta, recurso o proceso que ya funciona muy bien en otra área de la empresa podemos poner en otro uso para resolver [el reto de hoy] sin inventar nada desde cero?",
            "¿Qué prototipo, idea archivada o proyecto que no se concretó en [área / año pasado] podemos poner en otro uso adaptándolo para resolver el reto de hoy?",
            "¿Qué soporte de comunicación corporativa que ya existe (como las pantallas de los pasillos, los tótems informativos o la intranet) podemos desviar de su propósito original y poner en otro uso, usándolo como un canal interactivo para exhibir [la idea] y recopilar reacciones del personal que pasa por ahí?",
            "¿Qué métrica de rendimiento que el equipo ya revisa en [proceso] podemos poner en otro uso como el indicador para saber si la idea tuvo éxito?",
            "¿Qué hábito o costumbre diaria del equipo en [área] podemos poner en otro uso para asegurar que esta nueva idea se vuelva una rutina natural?",
            "¿Qué acuerdo de nivel de servicio o tiempo máximo de respuesta que ya respetamos en [trámite] podemos poner en otro uso como nuestro compromiso de velocidad para este piloto?",
            "¿Qué evento, feria o actividad grupal que ya se realiza en [área / empresa] podemos poner en otro uso como el escenario para lanzar la prueba de esta idea?"
        ]
    },
    {
        "letra": "E", "nombre": "ELIMINAR", "color": "#007bff", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué paso, requisito o documento en [área / proceso] podemos eliminar hoy mismo para que la idea principal pase del papel a la prueba piloto sin trabas burocráticas?",
            "¿Qué alternativa o de opción extra en [propuesta] podemos eliminar para dejar solo una ruta clara y tomar la decisión sin dudar?",
            "¿Qué paso del alcance inicial de la idea en [área / proyecto] podemos eliminar temporalmente para tener la primera versión probada esta misma semana?",
            "¿Qué datos, campos o requisitos innecesarios en el formulario o plan de [proceso] podemos eliminar para simplificar la propuesta a su mínima expresión viable?",
            "¿Qué punto de fricción o complicación técnica que frena al usuario en [área] podemos eliminar para que la solución sea simple y directa de implementar?",
            "¿Qué reunión de revisión o comité innecesario podemos eliminar para sustituirlo por una decisión directa del equipo en esta misma sesión?",
            "¿Qué supuesto o duda sobre el usuario en [área] podemos eliminar de la discusión y darlo por válido para tomar hoy la decisión de avanzar?",
            "¿Qué funcionalidad o beneficio secundario en [propuesta] podemos eliminar para enfocar el 100% de los recursos únicamente en el problema principal?"
        ]
    },
    {
        "letra": "R", "nombre": "REORGANIZAR", "color": "#6610f2", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué pasaría si invertimos el orden en [proceso] y entregamos primero la solución o beneficio al usuario antes de pedirle requisitos o formularios?",
            "¿Qué pasó que normalmente dejamos para el final de [proyecto] podemos mover al puro inicio para saber hoy mismo si la idea va a funcionar?",
            "¿Qué pasaría si en lugar de esperar a que el usuario venga con un problema en [proceso], nos adelantamos y le enviamos la solución antes de que la pida?",
            "¿Cómo cambiaría el trabajo en [equipo] si en lugar de buscar la información manualmente, reordenar el sistema para que la información le llegue sola al colaborador?",
            "En lugar de hacer las revisiones de [trámite] una por una en fila, ¿cómo podemos reordenarlas para que varias personas las aprueben al mismo tiempo?",
            "¿Qué pasaría si probamos esta idea primero en [área / sucursal] durante una sola semana antes de aplicarla a toda la empresa?",
            "¿Cómo podemos reordenar el orden de las tareas en [proceso] para resolver primero lo que genera más valor y dejar lo secundario para después?",
            "¿Qué pasaría si en lugar de explicar primero todo el proceso en [área], mostramos directamente el resultado final para captar el interés inmediato del usuario?"
        ]
    }
]

URL_APP_DESTINO_DEFAULT = ""

def inicializar_estado():
    if "opciones" not in st.session_state:
        st.session_state.opciones = [{**item, "salidas_actuales": 0} for item in DATOS_SCAMPER]
    if "historial" not in st.session_state:
        st.session_state.historial = []
    if "angulo_actual" not in st.session_state:
        st.session_state.angulo_actual = 0
    if "estado_texto" not in st.session_state:
        st.session_state.estado_texto = "Opciones activas: 7 (máx. 3 salidas c/u)"
    if "mostrar_dialogo" not in st.session_state:
        st.session_state.mostrar_dialogo = False
    if "ganador_actual" not in st.session_state:
        st.session_state.ganador_actual = None
    if "pregunta_actual" not in st.session_state:
        st.session_state.pregunta_actual = ""
    if "tiempo_restante" not in st.session_state:
        st.session_state.tiempo_restante = 90
    if "cronometro_activo" not in st.session_state:
        st.session_state.cronometro_activo = False
    if "sonar_campana" not in st.session_state:
        st.session_state.sonar_campana = False
    if "url_qr" not in st.session_state:
        st.session_state.url_qr = URL_APP_DESTINO_DEFAULT

inicializar_estado()

# ==============================================================================
# 3. SONIDO DE CAMPANA
# ==============================================================================
def reproducir_campana():
    components.html(
        """
        <script>
        (function() {
            try {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                const ctx = new AudioCtx();
                const ahora = ctx.currentTime;

                function tocarNota(freq, inicio, duracion) {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, inicio);
                    gain.gain.setValueAtTime(0.35, inicio);
                    gain.gain.exponentialRampToValueAtTime(0.001, inicio + duracion);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(inicio);
                    osc.stop(inicio + duracion);
                }

                tocarNota(880, ahora, 0.9);
                tocarNota(1318.5, ahora + 0.18, 1.1);
            } catch (e) {}
        })();
        </script>
        """,
        height=0,
        width=0
    )

# ==============================================================================
# 4. DIBUJO DE LA RULETA CIRCULAR E INDICADOR DE VIDAS
# ==============================================================================
def generar_svg_ruleta(opciones, angulo_actual):
    size = 440
    cx = size / 2
    cy = size / 2
    r = 190
    num = len(opciones)

    if num == 0:
        return (
            f'<div style="display:flex;justify-content:center;align-items:center;margin:6px 0;">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f8f9fa" stroke="#dee2e6" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy}" fill="#495057" font-family="Segoe UI, sans-serif" '
            f'font-size="22" font-weight="bold" text-anchor="middle" dominant-baseline="middle">'
            f'¡CICLO COMPLETADO!</text></svg></div>'
        )

    paso = 360.0 / num
    partes = []

    for i, opt in enumerate(opciones):
        start_deg = (angulo_actual + i * paso) % 360
        end_deg = start_deg + paso

        start_rad = math.radians(start_deg - 90)
        end_rad = math.radians(end_deg - 90)

        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)

        large_arc = 1 if paso > 180 else 0

        if num == 1:
            partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{opt["color"]}" stroke="white" stroke-width="3"/>')
        else:
            d = f"M {cx},{cy} L {x1:.2f},{y1:.2f} A {r},{r} 0 {large_arc},1 {x2:.2f},{y2:.2f} Z"
            partes.append(f'<path d="{d}" fill="{opt["color"]}" stroke="white" stroke-width="3"/>')

        mid_deg = start_deg + (paso / 2.0)
        rot_texto = mid_deg - 90
        mid_rad = math.radians(rot_texto)
        tx = cx + (r * 0.56) * math.cos(mid_rad)
        ty = cy + (r * 0.56) * math.sin(mid_rad)

        font_size = 11 if len(opt["nombre"]) > 12 else 12
        partes.append(
            f'<text x="{tx:.2f}" y="{ty:.2f}" fill="#ffffff" font-family="Segoe UI, sans-serif" '
            f'font-size="{font_size}" font-weight="bold" text-anchor="middle" dominant-baseline="middle" '
            f'transform="rotate({rot_texto:.2f}, {tx:.2f}, {ty:.2f})">{opt["nombre"]}</text>'
        )

    centro_y_flecha = (
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.16:.1f}" fill="#ffffff" stroke="#c8c8c8" stroke-width="3"/>'
        f'<polygon points="{cx},{cy - r - 16} {cx - 14},{cy - r + 4} {cx + 14},{cy - r + 4}" fill="#212529"/>'
    )

    return (
        f'<div style="display:flex;justify-content:center;align-items:center;margin:4px 0 6px 0;">'
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'{"".join(partes)}{centro_y_flecha}'
        f'</svg></div>'
    )

def generar_barra_vidas(todas_opciones):
    chips = []
    for opt in todas_opciones:
        restantes = opt["max_salidas"] - opt["salidas_actuales"]
        puntos = ("● " * restantes + "○ " * opt["salidas_actuales"]).strip()
        opacidad = "1" if restantes > 0 else "0.45"
        color_letra = opt["color"] if restantes > 0 else "#6c757d"
        chips.append(
            f'<div class="chip-vida" style="opacity:{opacidad};">'
            f'<span style="color:{color_letra};font-size:15px;">{opt["letra"]}</span>'
            f'<span style="color:{color_letra};letter-spacing:1px;">{puntos}</span>'
            f'</div>'
        )
    return f'<div class="barra-vidas">{"".join(chips)}</div>'

# ==============================================================================
# 5. VENTANA EMERGENTE DEL RETO (CON PREGUNTAS OFICIALES)
# ==============================================================================
@st.dialog("Reto SCAMPER", width="small")
def dialogo_reto():
    ganador = st.session_state.ganador_actual
    if not ganador:
        return

    if st.session_state.sonar_campana:
        reproducir_campana()
        st.session_state.sonar_campana = False

    st.markdown(
        f'<div style="text-align:center;font-family:Segoe UI,sans-serif;font-size:52px;'
        f'font-weight:800;color:{ganador["color"]};line-height:1.1;">{ganador["letra"]} - {ganador["nombre"]}</div>'
        f'<div style="text-align:center;font-family:Segoe UI,sans-serif;font-size:13px;'
        f'color:#6c757d;margin-bottom:12px;">Salida #{ganador["salidas_actuales"]} de {ganador["max_salidas"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div style="background-color:#f1f3f5;border-left:5px solid {ganador["color"]};'
        f'padding:12px 15px;border-radius:8px;margin-bottom:14px;font-family:Segoe UI,sans-serif;'
        f'font-size:15px;font-weight:600;color:#212529;text-align:center;">'
        f'💡 "{st.session_state.pregunta_actual}"'
        f'</div>',
        unsafe_allow_html=True
    )

    if st.button("🔄 Cambiar pregunta", use_container_width=True):
        st.session_state.pregunta_actual = random.choice(ganador["preguntas"])
        st.rerun()

    mins = st.session_state.tiempo_restante // 60
    segs = st.session_state.tiempo_restante % 60
    color_reloj = "#dc3545" if st.session_state.tiempo_restante == 0 else "#0d6efd"
    texto_reloj = "¡TIEMPO!" if st.session_state.tiempo_restante == 0 else f"{mins:02d}:{segs:02d}"

    st.markdown(
        f'<div style="text-align:center;font-family:Segoe UI,sans-serif;font-size:38px;'
        f'font-weight:800;color:{color_reloj};background:#f8f9fa;border-radius:10px;padding:10px;'
        f'margin:12px 0;">{texto_reloj}</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶ Iniciar", use_container_width=True, disabled=(st.session_state.tiempo_restante == 0)):
            st.session_state.cronometro_activo = True
            st.rerun()
    with c2:
        if st.button("⏸ Pausar", use_container_width=True, disabled=(st.session_state.tiempo_restante == 0)):
            st.session_state.cronometro_activo = False
            st.rerun()

    if st.button("⏹ Terminar", type="primary", use_container_width=True):
        st.session_state.cronometro_activo = False
        st.session_state.sonar_campana = False
        transcurrido = ganador["tiempo_inicial"] - st.session_state.tiempo_restante
        m_t = transcurrido // 60
        s_t = transcurrido % 60
        duracion = f"{m_t:02d}:{s_t:02d}"

        st.session_state.historial.append(
            f"{ganador['letra']} - {ganador['nombre']} (#{ganador['salidas_actuales']}) [{duracion}]"
        )
        activas = [o for o in st.session_state.opciones if o["salidas_actuales"] < o["max_salidas"]]
        if len(activas) == 0:
            st.session_state.estado_texto = "¡Todas las categorías completaron sus 3 salidas!"
        else:
            st.session_state.estado_texto = f"Última: {ganador['nombre']} (#{ganador['salidas_actuales']}/3) | Activas: {len(activas)}"

        st.session_state.mostrar_dialogo = False
        st.rerun()

    if st.session_state.cronometro_activo and st.session_state.tiempo_restante > 0:
        time.sleep(1)
        st.session_state.tiempo_restante -= 1
        if st.session_state.tiempo_restante == 0:
            st.session_state.cronometro_activo = False
            st.session_state.sonar_campana = True
        st.rerun()

# ==============================================================================
# 6. INTERFAZ PRINCIPAL
# ==============================================================================
col_izq, col_der = st.columns([3.1, 1.3], gap="large")

with col_izq:
    st.markdown('<div class="titulo-scamper">SCAMPER</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitulo-estado">{st.session_state.estado_texto}</div>', unsafe_allow_html=True)

    opciones_activas = [o for o in st.session_state.opciones if o["salidas_actuales"] < o["max_salidas"]]
    placeholder_ruleta = st.empty()
    placeholder_ruleta.markdown(generar_svg_ruleta(opciones_activas, st.session_state.angulo_actual), unsafe_allow_html=True)

    st.markdown(generar_barra_vidas(st.session_state.opciones), unsafe_allow_html=True)

    b1, b2 = st.columns(2, gap="medium")
    with b1:
        girar = st.button("🎯 GIRAR RULETA", type="primary", use_container_width=True, disabled=(len(opciones_activas) == 0))
    with b2:
        reiniciar = st.button("🔄 Reiniciar", type="secondary", use_container_width=True)

    if reiniciar:
        st.session_state.opciones = [{**item, "salidas_actuales": 0} for item in DATOS_SCAMPER]
        st.session_state.historial = []
        st.session_state.angulo_actual = 0
        st.session_state.estado_texto = "Opciones activas: 7 (máx. 3 salidas c/u)"
        st.session_state.mostrar_dialogo = False
        st.session_state.cronometro_activo = False
        st.session_state.sonar_campana = False
        st.rerun()

    if girar and len(opciones_activas) > 0:
        velocidad = random.uniform(38, 52)
        while velocidad > 1.2:
            st.session_state.angulo_actual = (st.session_state.angulo_actual + velocidad) % 360
            placeholder_ruleta.markdown(
                generar_svg_ruleta(opciones_activas, st.session_state.angulo_actual),
                unsafe_allow_html=True
            )
            velocidad *= 0.88
            time.sleep(0.04)

        paso = 360.0 / len(opciones_activas)
        angulo_flecha = (360.0 - st.session_state.angulo_actual) % 360.0
        indice_ganador = int(angulo_flecha / paso) % len(opciones_activas)
        ganador = opciones_activas[indice_ganador]

        ganador["salidas_actuales"] += 1
        st.session_state.ganador_actual = ganador
        st.session_state.pregunta_actual = random.choice(ganador["preguntas"])
        st.session_state.tiempo_restante = ganador["tiempo_inicial"]
        st.session_state.cronometro_activo = False
        st.session_state.sonar_campana = False
        st.session_state.mostrar_dialogo = True
        st.rerun()

with col_der:
    items_html = ""
    for entry in st.session_state.historial:
        items_html += f'<div class="item-historial">{entry}</div>'

    html_panel = (
        '<div class="panel-historial">'
        '<div class="titulo-historial">HISTORIAL DE SALIDAS</div>'
        f'{items_html}'
        '</div>'
    )
    st.markdown(html_panel, unsafe_allow_html=True)

    if st.session_state.url_qr.strip():
        url_codificada = urllib.parse.quote(st.session_state.url_qr.strip(), safe="")
        qr_contenido = f'<img src="https://api.qrserver.com/v1/create-qr-code/?size=165x165&data={url_codificada}" width="155" height="155" style="border-radius:8px;margin:4px 0 8px 0;" />'
    else:
        qr_contenido = (
            '<div style="width:155px;height:155px;margin:4px auto 8px auto;border:2px dashed #ced4da;'
            'border-radius:8px;display:flex;align-items:center;justify-content:center;color:#adb5bd;'
            'font-family:Segoe UI,sans-serif;font-size:12px;padding:10px;">Espacio reservado para tu QR</div>'
        )

    html_qr = (
        '<div class="panel-qr">'
        '<div class="titulo-historial" style="margin-bottom:8px;">📱 SIGUIENTE PASO</div>'
        f'{qr_contenido}'
        '<div style="font-family:Segoe UI,sans-serif;font-size:12px;color:#6c757d;">'
        'Escanea para ingresar tu idea'
        '</div>'
        '</div>'
    )
    st.markdown(html_qr, unsafe_allow_html=True)

    with st.expander("🔗 Configurar enlace del QR", expanded=False):
        nueva_url = st.text_input("Pega aquí el link de tu app:", value=st.session_state.url_qr, label_visibility="collapsed", placeholder="https://...")
        if nueva_url != st.session_state.url_qr:
            st.session_state.url_qr = nueva_url
            st.rerun()

if st.session_state.mostrar_dialogo:
    dialogo_reto()