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
