import streamlit as st
import datetime
from fpdf import FPDF

st.set_page_config(page_title="Behavioral Intelligence", layout="centered")
st.title("Sistema BIAS – Evaluación Conductual")

with st.form("formulario"):
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

import streamlit as st
import datetime
from fpdf import FPDF

# Bases clínicas y sociales ya incluidas (no modificamos esa parte en este paso)

st.set_page_config(page_title="Behavioral Intelligence", layout="centered")
st.title("Sistema BIAS – Evaluación Conductual")

with st.form("formulario"):
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

# Este archivo será construido con todo lo que Nara pidió, paso a paso, sin omitir nada.


import streamlit as st
import datetime
from fpdf import FPDF

st.set_page_config(page_title="Behavioral Intelligence", layout="centered")
st.title("Sistema BIAS – Evaluación Conductual")

with st.form("formulario"):
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

# ========================
# INTERVENCIONES CLÍNICAS
# ========================

bias_interventions_clinicas = [
    {
        "nombre": "Terapia Dialéctico-Conductual (DBT)",
        "grupo_destinatario": "Adolescentes y adultos",
        "diagnostico": "Trastorno Límite de la Personalidad (TLP)",
        "modalidad": "Individual + grupal",
        "duracion_estimada": "Mínimo 6 meses",
        "medicacion": "ISRS, estabilizadores, antipsicóticos",
        "observaciones": "Evaluar riesgo suicida. Vínculo terapéutico fuerte es esencial."
    },
    {
        "nombre": "Terapia de exposición con prevención de respuesta (EPR)",
        "grupo_destinatario": "Adultos y adolescentes",
        "diagnostico": "Trastorno Obsesivo-Compulsivo (TOC)",
        "modalidad": "Individual",
        "duracion_estimada": "10-20 sesiones",
        "medicacion": "ISRS en dosis altas, clomipramina",
        "observaciones": "Supervisar adherencia. Combinar con reestructuración cognitiva si hay resistencia."
    },
    {
        "nombre": "Psicoterapia emocional + contrato de seguridad",
        "grupo_destinatario": "Adolescentes",
        "diagnostico": "Autolesión o ideación suicida",
        "modalidad": "Individual",
        "duracion_estimada": "8-12 sesiones + seguimiento",
        "medicacion": "ISRS, estabilizadores",
        "observaciones": "Validación emocional sin dramatización. Detectar función de la autolesión."
    }
]

def filtrar_intervenciones_clinicas(medicacion):
    return [
        interv for interv in bias_interventions_clinicas
        if medicacion.lower() in interv["medicacion"].lower() or medicacion == "Otro"
    ]

def generar_texto_intervenciones_clinicas(medicacion):
    intervenciones = filtrar_intervenciones_clinicas(medicacion)
    if not intervenciones:
        return "No se identificaron intervenciones clínicas relevantes asociadas al tipo de medicación indicada."
    texto = "INTERVENCIONES CLÍNICAS SUGERIDAS:\n\n"
    for i in intervenciones:
        texto += f"{i['nombre']}\n"
        texto += f"- Modalidad: {i['modalidad']}\n"
        texto += f"- Duración: {i['duracion_estimada']}\n"
        texto += f"- Observaciones clínicas: {i['observaciones']}\n\n"
    return texto.strip()

# ========================
# INTERVENCIONES SOCIALES
# ========================

bias_interventions_sociales = [
    {
        "nombre": "Programa de empoderamiento femenino",
        "grupo_destinatario": "Mujeres adultas",
        "contexto": "Libertad",
        "modalidad": "Grupal",
        "duracion_estimada": "Variable",
        "observaciones": "Fortalece autoestima, autonomía y toma de decisiones desde una perspectiva de género."
    },
    {
        "nombre": "Terapia familiar estructurada",
        "grupo_destinatario": "Adolescentes varones",
        "contexto": "Libertad",
        "modalidad": "Familiar",
        "duracion_estimada": "3-6 meses",
        "observaciones": "Reestructura dinámicas familiares conflictivas sin culpabilizar al menor."
    },
    {
        "nombre": "Grupos de habilidades sociales",
        "grupo_destinatario": "Hombres adultos",
        "contexto": "Libertad",
        "modalidad": "Grupal",
        "duracion_estimada": "10-12 sesiones",
        "observaciones": "Refuerza habilidades de comunicación, empatía y resolución de conflictos."
    }
]

def filtrar_intervenciones_sociales(grupo, contexto):
    return [
        i for i in bias_interventions_sociales
        if i["grupo_destinatario"] == grupo and i["contexto"] == contexto
    ]

def generar_texto_intervenciones_sociales(grupo, contexto):
    intervenciones = filtrar_intervenciones_sociales(grupo, contexto)
    if not intervenciones:
        return "No se identificaron intervenciones sociales relevantes para este perfil."
    texto = "INTERVENCIONES SOCIALES SUGERIDAS:\n\n"
    for i in intervenciones:
        texto += f"{i['nombre']}\n"
        texto += f"- Modalidad: {i['modalidad']}\n"
        texto += f"- Duración: {i['duracion_estimada']}\n"
        texto += f"- Observaciones: {i['observaciones']}\n\n"
    return texto.strip()

if submit:
    grupo = "Adolescentes varones" if edad < 18 and sexo == "Masculino" else \
            "Adolescentes mujeres" if edad < 18 else \
            "Hombres adultos" if sexo == "Masculino" else "Mujeres adultas"
    contexto = "Libertad" if libertad == "Libertad" else "Prisión"

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
    pdf.multi_cell(0, 10, txt=f"Observaciones adicionales: {observaciones}")
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="RECOMENDACIONES DEL SISTEMA", ln=True)
    pdf.set_font("Arial", style="", size=11)
    pdf.multi_cell(0, 10, txt=generar_texto_intervenciones_clinicas(medicacion))
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=generar_texto_intervenciones_sociales(grupo, contexto))

    nombre_archivo = f"informe_{nombre.replace(' ', '_')}.pdf"
    pdf.output(nombre_archivo)

    
    
    
    # Informe privado (uso interno)
    pdf_privado = FPDF()
    pdf_privado.add_page()
    pdf_privado.set_font("Arial", size=12)
    pdf_privado.cell(200, 10, txt="Informe Privado – Análisis Interno BIAS", ln=True, align="C")
    pdf_privado.ln(10)
    pdf_privado.cell(200, 10, txt=f"Nombre del evaluado: {nombre}", ln=True)
    pdf_privado.cell(200, 10, txt=f"Código generado: {edad}-{sexo[:1]}-{delito[:3]}-{fecha}", ln=True)
    pdf_privado.ln(10)
    pdf_privado.set_font("Arial", style="B", size=12)
    pdf_privado.cell(200, 10, txt="Resumen de Observaciones", ln=True)
    pdf_privado.set_font("Arial", style="", size=11)
    pdf_privado.multi_cell(0, 10, txt=observaciones)
    pdf_privado.ln(10)
    pdf_privado.multi_cell(0, 10, txt=generar_texto_intervenciones_clinicas(medicacion))
    pdf_privado.ln(5)
    pdf_privado.multi_cell(0, 10, txt=generar_texto_intervenciones_sociales(grupo, contexto))


    nombre_privado = f"privado_{nombre.replace(' ', '_')}.pdf"
    pdf_privado.output(nombre_privado)
    
    
    
    
    with open(nombre_privado, "rb") as file_priv:
    st.download_button(
        label="Descargar informe privado (PDF)",
        data=file_priv,
        file_name=nombre_privado,
        mime="application/pdf"
    )




     st.download_button(
            label="Descargar informe completo (PDF)",
            data=file,
            file_name=nombre_archivo,
            mime="application/pdf"
        )
