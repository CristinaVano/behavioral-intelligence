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
    libertad = st.selectbox("Situación judicial", [
        "En libertad", "Cumpliendo condena"
    ])
    medicacion = st.selectbox("Tratamiento farmacológico actual", [
        "Ninguno", "Estabilizadores del estado de ánimo", "Antipsicóticos",
        "Ansiolíticos", "Antidepresivos", "Desconocido"
    ])
    observaciones = st.text_area("Observaciones adicionales")
    fecha = st.date_input("Fecha de evaluación", value=datetime.date.today())

    submit = st.form_submit_button("Generar informe")

if submit:
    riesgo = "Alto" if reincidencia and impulsividad else "Medio" if impulsividad else "Bajo"

    if riesgo == "Alto":
        recomendacion = "Intervención clínica prioritaria"
    elif riesgo == "Medio":
        recomendacion = "Programa mixto de regulación e inserción"
    else:
        recomendacion = "Derivación a programas sociales"

    data = {
        "Nombre": nombre,
        "Edad": edad,
        "Sexo": sexo,
        "Delito": delito,
        "Riesgo": riesgo,
        "Red de apoyo": red_apoyo,
        "Empleo": empleo,
        "Estabilidad": estabilidad,
        "Consumo": consumo,
        "Conciencia": conciencia_dano,
        "Observaciones": observaciones,
        "Recomendación": recomendacion,
        "Situación judicial": libertad,
        "Tratamiento actual": medicacion,
        "Fecha": fecha.strftime("%Y-%m-%d")
    }

    df = pd.DataFrame([data])
    if not os.path.exists("registros_perfiles.csv"):
        df.to_csv("registros_perfiles.csv", index=False)
    else:
        df.to_csv("registros_perfiles.csv", mode="a", header=False, index=False)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Informe de Evaluación Conductual - BIAS", ln=True)
    pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"Edad: {edad}", ln=True)
    pdf.cell(200, 10, txt=f"Delito: {delito}", ln=True)
    pdf.cell(200, 10, txt=f"Nivel de riesgo: {riesgo}", ln=True)
    pdf.cell(200, 10, txt=f"Recomendación: {recomendacion}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha de evaluación: {fecha.strftime('%Y-%m-%d')}", ln=True)
    pdf.output(f"informe_{nombre.replace(' ', '_')}.pdf")

    pdf_priv = FPDF()
    pdf_priv.add_page()
    pdf_priv.set_font("Arial", size=12)
    pdf_priv.cell(200, 10, txt="INFORME PRIVADO - SISTEMA BIAS", ln=True)
    for key, value in data.items():
        pdf_priv.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf_priv.output(f"privado_{nombre.replace(' ', '_')}.pdf")

    st.success("¡Informe generado correctamente!")
    with open(f"informe_{nombre.replace(' ', '_')}.pdf", "rb") as file:
    st.download_button(
        label="Descargar informe público (PDF)",
        data=file,
        file_name=f"informe_{nombre.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

with open(f"privado_{nombre.replace(' ', '_')}.pdf", "rb") as file_priv:
    st.download_button(
        label="Descargar informe privado (PDF)",
        data=file_priv,
        file_name=f"privado_{nombre.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
