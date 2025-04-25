import streamlit as st
from datetime import datetime

# Configurar la app
st.set_page_config(page_title="BIAS - Prevención del Terrorismo", page_icon="🔒", layout="centered")

st.title("BIAS – Prevención del Terrorismo")
st.subheader("Evaluación de Riesgo de Radicalización")

st.write("Por favor, completa el siguiente formulario para generar el informe preliminar de riesgo.")

# Formulario de evaluación
with st.form(key='evaluation_form'):
    edad = st.slider("Edad", 12, 80, 25)
    genero = st.selectbox("Género", ("Masculino", "Femenino", "Otro", "Prefiero no decirlo"))
    entorno_social = st.selectbox("Entorno social actual", ("Integrado", "Aislado", "Radicalizado", "Sin información"))
    antecedentes_penales = st.radio("Antecedentes penales por delitos violentos", ("Sí", "No"))
    antecedentes_terrorismo = st.radio("Antecedentes relacionados con terrorismo", ("Sí", "No"))
    discursos_odio = st.radio("Evidencias de discursos de odio", ("Sí", "No"))
    viajes_zonas_conflictivas = st.radio("Viajes recientes a zonas de conflicto", ("Sí", "No"))
    indicadores_psicologicos = st.radio("Indicadores psicológicos preocupantes", ("Sí", "No"))
    participacion_grupos = st.radio("Participación en grupos extremistas", ("Sí", "No"))

    submit_button = st.form_submit_button(label='Generar Informe')

# Procesamiento de datos
if submit_button:
    riesgo = 0

    if entorno_social == "Radicalizado":
        riesgo += 2
    elif entorno_social == "Aislado":
        riesgo += 1

    if antecedentes_penales == "Sí":
        riesgo += 1
    if antecedentes_terrorismo == "Sí":
        riesgo += 3
    if discursos_odio == "Sí":
        riesgo += 2
    if viajes_zonas_conflictivas == "Sí":
        riesgo += 2
    if indicadores_psicologicos == "Sí":
        riesgo += 1
    if participacion_grupos == "Sí":
        riesgo += 3

    # Evaluar nivel de riesgo
    if riesgo >= 8:
        nivel_riesgo = "ALTO"
    elif riesgo >= 4:
        nivel_riesgo = "MODERADO"
    else:
        nivel_riesgo = "BAJO"

    # Mostrar informe
    st.success("Informe generado correctamente.")

    st.header("\ud83d\udd22 Informe Preliminar de Riesgo")
    st.write(f"**Fecha de evaluación:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.write(f"**Edad:** {edad}")
    st.write(f"**Género:** {genero}")
    st.write(f"**Entorno social:** {entorno_social}")
    st.write(f"**Nivel de riesgo de radicalización:** **{nivel_riesgo}**")

    st.subheader("Notas preliminares:")
    if nivel_riesgo == "ALTO":
        st.error("Se recomienda activación de protocolo de vigilancia intensiva y notificación a unidades de inteligencia.")
    elif nivel_riesgo == "MODERADO":
        st.warning("Se recomienda seguimiento regular y evaluación psicológica especializada.")
    else:
        st.info("Seguimiento habitual. Reevaluar en caso de cambios de conducta.")

    st.write("\nEste informe es preliminar y debe ser validado por un profesional especializado antes de cualquier actuación.")
