import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
import os

st.set_page_config(page_title="Behavioral Intelligence", layout="centered")
st.title("Sistema BIAS – Evaluación Conductual")

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
    libertad = st.selectbox("¿Está en libertad o cumpliendo condena?", [
        "Libertad", "Condena"
    ])
    medicacion = st.selectbox("Tipo de medicación (si procede)", [
        "Ninguna", "Antipsicóticos", "Antidepresivos", "Estabilizadores del ánimo", "Ansiolíticos", "Otro"
    ])
    observaciones = st.text_area("Observaciones adicionales")
    fecha = st.date_input("Fecha de evaluación", value=datetime.date.today())

    
# BASE DE DATOS CLÍNICA Y SOCIAL
bias_interventions_clinicas = [
    {"nombre": "Terapia Dialéctico-Conductual (DBT)", "grupo_destinatario": "Adolescentes y adultos", "diagnostico": "Trastorno Límite de la Personalidad (TLP)", "modalidad": "Individual + grupal", "duracion_estimada": "Mínimo 6 meses", "medicacion": "ISRS, estabilizadores, antipsicóticos", "observaciones": "Evaluar riesgo suicida, requiere vínculo fuerte"},
    {"nombre": "Terapia de exposición (TOC)", "grupo_destinatario": "Adultos", "diagnostico": "Trastorno Obsesivo-Compulsivo", "modalidad": "Individual", "duracion_estimada": "12-20 sesiones", "medicacion": "ISRS, clomipramina", "observaciones": "No iniciar sin motivación adecuada"}
]

bias_interventions_sociales = [
    {"nombre": "Grupos de empoderamiento y autonomía", "grupo_destinatario": "Mujeres adultas", "contexto": "Libertad", "modalidad": "Grupal", "duracion_estimada": "Variable", "observaciones": "Refuerzo de autoestima y toma de decisiones"},
    {"nombre": "Terapia familiar estructurada", "grupo_destinatario": "Adolescentes varones", "contexto": "Libertad", "modalidad": "Familiar", "duracion_estimada": "3-6 meses", "observaciones": "Rediseño de roles parentales y regulación emocional"}
]

def filtrar_intervenciones_clinicas(medicacion):
    return [i for i in bias_interventions_clinicas if medicacion.lower() in i["medicacion"].lower() or medicacion == "Otro"]

def filtrar_intervenciones_sociales(grupo, contexto):
    return [i for i in bias_interventions_sociales if i["grupo_destinatario"] == grupo and i["contexto"] == contexto]

def generar_texto_intervenciones_clinicas(medicacion):
    intervenciones = filtrar_intervenciones_clinicas(medicacion)
    if not intervenciones:
        return "No se identificaron intervenciones clínicas relevantes."
    texto = "Intervenciones clínicas sugeridas:\n\n"
    for i in intervenciones:
        texto += f"{i['nombre']}\n- Modalidad: {i['modalidad']}\n- Duración: {i['duracion_estimada']}\n- Observaciones: {i['observaciones']}\n\n"
    return texto.strip()

def generar_texto_intervenciones_sociales(grupo, contexto):
    intervenciones = filtrar_intervenciones_sociales(grupo, contexto)
    if not intervenciones:
        return "No se identificaron intervenciones sociales relevantes."
    texto = "Intervenciones sociales sugeridas:\n\n"
    for i in intervenciones:
        texto += f"{i['nombre']}\n- Modalidad: {i['modalidad']}\n- Duración: {i['duracion_estimada']}\n- Observaciones: {i['observaciones']}\n\n"
    return texto.strip()

    submit = st.form_submit_button("Generar informe")

if submit:
    # Informe público
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Informe de Evaluación Conductual – BIAS", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"Edad: {edad}", ln=True)
    pdf.cell(200, 10, txt=f"Sexo: {sexo}", ln=True)
    pdf.cell(200, 10, txt=f"Tipo de delito: {delito}", ln=True)
    pdf.cell(200, 10, txt=f"Reincidencia: {'Sí' if reincidencia else 'No'}", ln=True)
    pdf.cell(200, 10, txt=f"Impulsividad: {'Sí' if impulsividad else 'No'}", ln=True)
    pdf.cell(200, 10, txt=f"Conciencia sobre el daño: {conciencia_dano}", ln=True)
    pdf.cell(200, 10, txt=f"Red de apoyo: {red_apoyo}", ln=True)
    pdf.cell(200, 10, txt=f"Estabilidad residencial: {estabilidad}", ln=True)
    pdf.cell(200, 10, txt=f"Situación laboral: {empleo}", ln=True)
    pdf.cell(200, 10, txt=f"Consumo de sustancias: {consumo}", ln=True)
    pdf.cell(200, 10, txt=f"Situación legal: {libertad}", ln=True)
    pdf.cell(200, 10, txt=f"Tipo de medicación: {medicacion}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha de evaluación: {fecha}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Observaciones: {observaciones}")
    nombre_archivo = f"informe_{nombre.replace(' ', '_')}.pdf"
    pdf.ln(10)
pdf.set_font("Arial", style="B", size=12)
pdf.cell(200, 10, txt="Recomendaciones del sistema BIAS", ln=True)
pdf.set_font("Arial", style="", size=11)
texto_clinico = generar_texto_intervenciones_clinicas(medicacion)
pdf.multi_cell(0, 10, txt=texto_clinico)

texto_social = generar_texto_intervenciones_sociales(grupo, libertad)
pdf.multi_cell(0, 10, txt=texto_social)

pdf.output(nombre_archivo)

    # Informe privado (para uso interno)
pdf_privado = FPDF()
    pdf_privado.add_page()
    pdf_privado.set_font("Arial", size=12)
    pdf_privado.cell(200, 10, txt="Informe Privado – Uso Interno (Análisis Codificado)", ln=True, align="C")
    pdf_privado.ln(10)
    pdf_privado.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
    pdf_privado.cell(200, 10, txt=f"Código: {edad}-{sexo[:1]}-{delito[:3]}-{fecha}", ln=True)
    pdf_privado.multi_cell(0, 10, txt=f"Análisis interno: {observaciones}")
    nombre_privado = f"privado_{nombre.replace(' ', '_')}.pdf"
    pdf_privado.output(nombre_privado)

    st.success("¡Informe generado correctamente!")

    # Botones de descarga
    with open(nombre_archivo, "rb") as file:
        st.download_button(
            label="Descargar informe público (PDF)",
            data=file,
            file_name=nombre_archivo,
            mime="application/pdf"
        )

    with open(nombre_privado, "rb") as file_priv:
        st.download_button(
            label="Descargar informe privado (PDF)",
            data=file_priv,
            file_name=nombre_privado,
            mime="application/pdf"
        )
