import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
import os

st.set_page_config(page_title="Behavioral Intelligence", layout="centered")
st.title("Sistema BIAS - Evaluacion Conductual")

# Crear formulario
with st.form(key="formulario"):
    nombre = st.text_input("Nombre del evaluado")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
    delito = st.selectbox("Tipo de delito", [
        "Violencia de genero", "Delito sexual", "Trafico", "Agresion fisica",
        "Robo", "Vandalismo", "Violencia filioparental", "Otro"
    ])
    reincidencia = st.checkbox("¿Tiene antecedentes o reincidencia?")
    impulsividad = st.checkbox("¿Se observan conductas impulsivas?")
    conciencia_dano = st.selectbox("Conciencia sobre el dano causado", [
        "Alta", "Media", "Baja", "Nula"
    ])
    red_apoyo = st.selectbox("Red de apoyo actual", [
        "Familiar estable", "Parcial", "Inexistente"
    ])
    estabilidad = st.selectbox("Estabilidad residencial", [
        "Alta", "Media", "Baja"
    ])
    empleo = st.selectbox("Situacion laboral", [
        "Trabajo estable", "Trabajo precario", "Desempleado", "Estudiante"
    ])
    consumo = st.selectbox("Consumo de sustancias", [
        "No", "Ocasional", "Habitual", "Desconocido"
    ])
    fecha = st.date_input("Fecha de evaluacion", value=datetime.date.today())
    observaciones = st.text_area("Observaciones adicionales")

    submit = st.form_submit_button("Generar informe")

if submit:
    df = pd.read_csv("registros_perfiles.csv")

    nuevo_registro = pd.DataFrame([{
        "Nombre": nombre,
        "Edad": edad,
        "Sexo": sexo,
        "Delito": delito,
        "Reincidencia": reincidencia,
        "Impulsividad": impulsividad,
        "Conciencia_dano": conciencia_dano,
        "Red_apoyo": red_apoyo,
        "Estabilidad": estabilidad,
        "Empleo": empleo,
        "Consumo": consumo,
        "Fecha": fecha,
        "Observaciones": observaciones
    }])

    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_csv("registros_perfiles.csv", index=False)

    # Informe privado PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Informe de Evaluacion Conductual - BIAS", ln=True)

    for columna, valor in nuevo_registro.iloc[0].items():
        pdf.cell(200, 10, txt=f"{columna}: {valor}", ln=True)

    nombre_archivo = f"informe_{nombre}_{fecha}.pdf".replace(" ", "_")
    pdf.output(nombre_archivo)

    st.success("Informe generado correctamente.")
    with open(nombre_archivo, "rb") as file:
        st.download_button(
            label="Descargar informe en PDF",
            data=file,
            file_name=nombre_archivo,
            mime="application/pdf"
        )
