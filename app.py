import streamlit as st
import pandas as pd
from datetime import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
import base64

st.set_page_config(page_title="Behavioral Intelligence", layout="centered")

st.title("Behavioral Intelligence")
st.subheader("Evaluación de Riesgo y Reintegración Asistida por IA")

st.markdown("Este sistema permite valorar perfiles de forma integral y generar análisis éticos, humanos y contextualizados, con especial atención a procesos de libertad condicional y reinserción.")

# === Formulario ===
nombre = st.text_input("Nombre del caso evaluado:")
edad = st.slider("Edad", 10, 80, 30)
empatia = st.slider("Empatía percibida (0–10)", 0, 10, 5)

antecedentes = st.radio("¿Ha habido antecedentes violentos?", ["Sí", "No"])
impulsividad = st.slider("Nivel de impulsividad (0–10)", 0, 10, 5)
apoyo = st.radio("¿Tiene red de apoyo?", ["Sí", "No"])
sustancias = st.radio("¿Consumo de sustancias?", ["Sí", "No"])
introspeccion = st.slider("Capacidad de introspección (0–10)", 0, 10, 5)
diagnostico = st.text_input("Diagnóstico psiquiátrico actual (si lo hay):")

sesiones = st.slider("Sesiones terapéuticas por mes", 0, 12, 2)
situacion_familiar = st.selectbox(
    "Situación familiar actual",
    ["Vive con familia", "Vive solo/a", "Situación conflictiva"]
)
acceso_armas = st.radio("¿Acceso a armas?", ["Sí", "No"])
autolitico = st.radio("¿Historial de intentos autolíticos?", ["Sí", "No"])
motivacion = st.slider("Motivación al cambio (0–10)", 0, 10, 5)
juicios = st.radio("¿Juicios en curso o medidas legales activas?", ["Sí", "No"])
contexto = st.text_input("Contexto laboral o educativo:")

tipo_delito = st.selectbox(
    "Tipo de delito principal",
    [
        "Violencia de género",
        "Violencia familiar no pareja",
        "Delito sexual",
        "Delito contra la propiedad",
        "Delito contra la vida",
        "Amenazas o coacciones",
        "Tráfico o tenencia de drogas",
        "Otro / sin especificar"
    ]
)

# === Evaluación del perfil ===
if st.button("Evaluar perfil"):
    st.success(f"Perfil de {nombre} evaluado con éxito.")
    st.write("Resumen de datos ingresados:")
    st.write(f"- Edad: {edad}")
    st.write(f"- Empatía: {empatia}")
    st.write(f"- Impulsividad: {impulsividad}")
    st.write(f"- Red de apoyo: {apoyo}")
    st.write(f"- Consumo de sustancias: {sustancias}")
    st.write(f"- Capacidad de introspección: {introspeccion}")
    st.write(f"- Antecedentes violentos: {antecedentes}")
    st.write(f"- Diagnóstico: {diagnostico}")
    st.write(f"- Sesiones/mes: {sesiones}")
    st.write(f"- Situación familiar: {situacion_familiar}")
    st.write(f"- Acceso a armas: {acceso_armas}")
    st.write(f"- Intentos autolíticos: {autolitico}")
    st.write(f"- Motivación al cambio: {motivacion}")
    st.write(f"- Juicios o medidas legales: {juicios}")
    st.write(f"- Contexto laboral/educativo: {contexto}")
    st.write(f"- Tipo de delito: {tipo_delito}")

    # === Análisis de riesgo ===
    riesgo = "Bajo"

    if antecedentes == "Sí" or autolitico == "Sí":
        riesgo = "Moderado"

    if (
        antecedentes == "Sí"
        and empatia < 4
        and impulsividad > 7
        and sustancias == "Sí"
        and apoyo == "No"
        and motivacion < 5
    ):
        riesgo = "Alto"

    if tipo_delito == "Delito sexual" and empatia < 4 and introspeccion < 4:
        riesgo = "Alto"

    if tipo_delito == "Violencia de género" and motivacion < 5 and impulsividad > 7:
        riesgo = "Alto"

    if tipo_delito == "Tráfico o tenencia de drogas" and sustancias == "Sí" and motivacion < 4:
        riesgo = "Moderado"

    st.write("---")
    st.subheader("Análisis del perfil")
    st.info(f"Nivel de riesgo estimado: **{riesgo}**")

    st.markdown("Este nivel de riesgo se ha calculado con base en las respuestas proporcionadas. Pronto estará disponible una evaluación explicable mediante SHAP y LIME.")

    # === Registro de datos en CSV ===
    datos = {
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre": nombre,
        "edad": edad,
        "empatia": empatia,
        "antecedentes": antecedentes,
        "impulsividad": impulsividad,
        "apoyo": apoyo,
        "sustancias": sustancias,
        "introspeccion": introspeccion,
        "diagnostico": diagnostico,
        "sesiones": sesiones,
        "situacion_familiar": situacion_familiar,
        "acceso_armas": acceso_armas,
        "autolitico": autolitico,
        "motivacion": motivacion,
        "juicios": juicios,
        "contexto": contexto,
        "tipo_delito": tipo_delito,
        "riesgo_estimado": riesgo
    }

    df_nuevo = pd.DataFrame([datos])
    ruta_archivo = "registros_perfiles.csv"

    if os.path.exists(ruta_archivo):
        df_existente = pd.read_csv(ruta_archivo)
        df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
        df_actualizado.to_csv(ruta_archivo, index=False)
    else:
        df_nuevo.to_csv(ruta_archivo, index=False)

    st.success("✅ Datos guardados correctamente en 'registros_perfiles.csv'")

    # === Generar informe PDF ===
    nombre_archivo = f"informe_{nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    line_height = 20
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Informe de Evaluación Conductual Asistida por IA")
    y -= 30

    c.setFont("Helvetica", 12)
    for clave, valor in datos.items():
        c.drawString(50, y, f"{clave.replace('_', ' ').capitalize()}: {valor}")
        y -= line_height
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

    c.showPage()
    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()

    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{nombre_archivo}">📥 Descargar informe PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
