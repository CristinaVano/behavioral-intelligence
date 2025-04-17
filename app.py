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
    conciencia_dano = st.selectbox("Conciencia sobre el daño causado", ["Alta", "Media", "Baja", "Nula"])
    red_apoyo = st.selectbox("Red de apoyo actual", ["Familiar estable", "Parcial", "Inexistente"])
    estabilidad = st.selectbox("Estabilidad residencial", ["Alta", "Media", "Baja"])
    empleo = st.selectbox("Situación laboral", ["Trabajo estable", "Trabajo precario", "Desempleado", "Estudiante"])
    consumo = st.selectbox("Consumo de sustancias", ["No", "Ocasional", "Habitual", "Desconocido"])
    fecha = st.date_input("Fecha de evaluación", value=datetime.date.today())
    observaciones = st.text_area("Observaciones adicionales")

    submit = st.form_submit_button("Generar informe")

if submit:
    df = pd.DataFrame([{
        "Nombre": nombre,
        "Edad": edad,
        "Sexo": sexo,
        "Delito": delito,
        "Reincidencia": reincidencia,
        "Impulsividad": impulsividad,
        "Conciencia del daño": conciencia_dano,
        "Red de apoyo": red_apoyo,
        "Estabilidad residencial": estabilidad,
        "Situación laboral": empleo,
        "Consumo de sustancias": consumo,
        "Fecha": fecha,
        "Observaciones": observaciones
    }])

    df.to_csv("registros_perfiles.csv", index=False)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Informe de Evaluación Conductual – BIAS", ln=True, align="C")
    pdf.ln(10)

    for columna, valor in df.iloc[0].items():
        pdf.cell(200, 10, txt=f"{columna}: {valor}", ln=True)

    nombre_archivo = f"informe_{nombre.replace(' ', '_')}.pdf"
    pdf.output(nombre_archivo)

    st.success(f"Informe generado: {nombre_archivo}")
    with open(nombre_archivo, "rb") as file:
        st.download_button("Descargar informe", file, file_name=nombre_archivo)
    with open(path_privado, "rb") as file:
        st.download_button("Descargar informe privado", file, file_name=os.path.basename(path_privado))

    with open(path_publico, "rb") as file:
        st.download_button("Descargar informe genérico", file, file_name=os.path.basename(path_publico))
