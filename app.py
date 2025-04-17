import streamlit as st
import pandas as pd
import datetime
from fpdf2 import FPDF
import os

st.set_page_config(page_title="Behavioral Intelligence", layout="centered")

st.title("Sistema BIAS – Evaluación Conductual")

# Crear formulario
with st.form(key="formulario"):
    nombre = st.text_input("Nombre del evaluado")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
    delito = st.selectbox("Tipo de delito", [
        "Violencia de género", "Delito sexual", "Tráfico", "Agresión física",
        "Robo", "Vandalismo", "Violencia filioparental", "Otro"
    ])
    reincidencia = st.checkbox("¿Tiene antecedentes o reincidencia?")
    impulsividad = st.checkbox("¿Se observan conductas impulsivas?")
    conciencia_dano = st.selectbox("Conciencia sobre el daño causado", [
        "Alta", "Media", "Baja", "Nula"
    ])
    red_apoyo = st.selectbox("Red de apoyo actual", [
        "Familiar estable", "Parcial", "Inexistente"
    ])
    estabilidad = st.selectbox("Estabilidad residencial", [
        "Alta", "Media", "Baja"
    ])
    empleo = st.selectbox("Situación laboral", [
        "Trabajo estable", "Trabajo precario", "Desempleado", "Estudiante"
    ])
    consumo = st.selectbox("Consumo de sustancias", [
        "No", "Ocasional", "Habitual", "Desconocido"
    ])
    fecha = st.date_input("Fecha de evaluación", value=datetime.date.today())
    observaciones = st.text_area("Observaciones adicionales")

    submit = st.form_submit_button("Generar informe")

# Función para estimar nivel de riesgo
def calcular_riesgo():
    puntuacion = 0
    if reincidencia:
        puntuacion += 2
    if impulsividad:
        puntuacion += 1
    if conciencia_dano in ["Baja", "Nula"]:
        puntuacion += 2
    if red_apoyo == "Inexistente":
        puntuacion += 2
    if estabilidad == "Baja":
        puntuacion += 1
    if consumo in ["Habitual"]:
        puntuacion += 1

    if puntuacion >= 6:
        return "ALTO"
    elif puntuacion >= 3:
        return "MEDIO"
    elif puntuacion >= 1:
        return "BAJO"
    else:
        return "NO CONCLUYENTE"

# Función para sugerir programa
def sugerir_programa(riesgo, delito):
    if riesgo == "ALTO":
        return "Intervención intensiva con seguimiento clínico y social"
    elif riesgo == "MEDIO":
        if "género" in delito.lower():
            return "PRIA-MA – Programa de Reeducación para Agresores"
        elif "sexual" in delito.lower():
            return "Grupo terapéutico para delitos sexuales con evaluación continua"
        elif "tráfico" in delito.lower():
            return "Programa de deshabituación y orientación laboral"
        else:
            return "Programa general de regulación emocional y control de impulsos"
    elif riesgo == "BAJO":
        return "Reinserción sociolaboral con seguimiento puntual"
    else:
        return "Evaluación no concluyente – se requiere revisión profesional"

# Función para generar PDF
def generar_pdf(nombre, riesgo, programa, evaluador, privado=False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if privado:
        pdf.set_title("Informe Privado BIAS")
        pdf.cell(200, 10, txt="Informe de puntuación – Uso interno", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Nivel de riesgo estimado: {riesgo}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {datetime.date.today()}", ln=True)
        pdf.cell(200, 10, txt=f"Evaluador: {evaluador}", ln=True)
        pdf.cell(200, 10, txt="Este documento no debe compartirse fuera del equipo técnico.", ln=True)
        nombre_archivo = f"informe_privado_{nombre}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    else:
        pdf.set_title("Informe Conductual BIAS")
        pdf.cell(200, 10, txt="Informe conductual y programa sugerido", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Nivel de riesgo: {riesgo}", ln=True)
        pdf.cell(200, 10, txt=f"Programa recomendado: {programa}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {datetime.date.today()}", ln=True)
        pdf.cell(200, 10, txt="Este informe debe ser validado por el equipo profesional antes de enviarse.", ln=True)
        nombre_archivo = f"informe_conductual_{nombre}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    ruta = os.path.join(os.getcwd(), nombre_archivo)
    pdf.output(ruta)
    return ruta

# Acción al enviar
if submit:
    riesgo = calcular_riesgo()
    programa = sugerir_programa(riesgo, delito)

    st.success(f"Nivel de riesgo: {riesgo}")
    st.info(f"Programa sugerido: {programa}")

    # Generar PDFs
    path_privado = generar_pdf(nombre, riesgo, programa, "Analista BIAS", privado=True)
    path_publico = generar_pdf(nombre, riesgo, programa, "Analista BIAS", privado=False)

    with open(path_privado, "rb") as file:
        st.download_button("Descargar informe privado", file, file_name=os.path.basename(path_privado))

    with open(path_publico, "rb") as file:
        st.download_button("Descargar informe genérico", file, file_name=os.path.basename(path_publico))
