
import streamlit as st
import datetime
from fpdf import FPDF

st.set_page_config(page_title="Behavioral Intelligence", layout="centered")
st.title("Sistema BIAS - Evaluacion Conductual")

with st.form("formulario"):
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
    libertad = st.selectbox("¿Esta en libertad o cumpliendo condena?", [
        "Libertad", "Condena"
    ])
    medicacion = st.selectbox("Tipo de medicacion (si procede)", [
        "Ninguna", "Antipsicoticos", "Antidepresivos", "Estabilizadores del animo", "Ansioliticos", "Otro"
    ])
    observaciones = st.text_area("Observaciones adicionales")
    fecha = st.date_input("Fecha de evaluacion", value=datetime.date.today())
    submit = st.form_submit_button("Generar informe")

# ========================
# INTERVENCIONES CLINICAS
# ========================

bias_interventions_clinicas = [
    {
        "nombre": "Terapia Dialectico-Conductual (DBT)",
        "grupo_destinatario": "Adolescentes y adultos",
        "diagnostico": "Trastorno Limite de la Personalidad (TLP)",
        "modalidad": "Individual + grupal",
        "duracion_estimada": "Minimo 6 meses",
        "medicacion": "ISRS, estabilizadores, antipsicoticos",
        "observaciones": "Evaluar riesgo suicida. Vinculo terapeutico fuerte es esencial."
    },
    {
        "nombre": "Terapia de exposicion con prevencion de respuesta (EPR)",
        "grupo_destinatario": "Adultos y adolescentes",
        "diagnostico": "Trastorno Obsesivo-Compulsivo (TOC)",
        "modalidad": "Individual",
        "duracion_estimada": "10-20 sesiones",
        "medicacion": "ISRS en dosis altas, clomipramina",
        "observaciones": "Supervisar adherencia. Combinar con reestructuracion cognitiva si hay resistencia."
    },
    {
        "nombre": "Psicoterapia emocional + contrato de seguridad",
        "grupo_destinatario": "Adolescentes",
        "diagnostico": "Autolesion o ideacion suicida",
        "modalidad": "Individual",
        "duracion_estimada": "8-12 sesiones + seguimiento",
        "medicacion": "ISRS, estabilizadores",
        "observaciones": "Validacion emocional sin dramatizacion. Detectar funcion de la autolesion."
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
        return "No se identificaron intervenciones clinicas relevantes asociadas al tipo de medicacion indicada."
    texto = "INTERVENCIONES CLINICAS SUGERIDAS:\n\n"
    for i in intervenciones:
        texto += f"{i['nombre']}\n"
        texto += f"- Modalidad: {i['modalidad']}\n"
        texto += f"- Duracion: {i['duracion_estimada']}\n"
        texto += f"- Observaciones clinicas: {i['observaciones']}\n\n"
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
        "observaciones": "Fortalece autoestima, autonomia y toma de decisiones desde una perspectiva de genero."
    },
    {
        "nombre": "Terapia familiar estructurada",
        "grupo_destinatario": "Adolescentes varones",
        "contexto": "Libertad",
        "modalidad": "Familiar",
        "duracion_estimada": "3-6 meses",
        "observaciones": "Reestructura dinamicas familiares conflictivas sin culpabilizar al menor."
    },
    {
        "nombre": "Grupos de habilidades sociales",
        "grupo_destinatario": "Hombres adultos",
        "contexto": "Libertad",
        "modalidad": "Grupal",
        "duracion_estimada": "10-12 sesiones",
        "observaciones": "Refuerza habilidades de comunicacion, empatia y resolucion de conflictos."
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
        texto += f"- Duracion: {i['duracion_estimada']}\n"
        texto += f"- Observaciones: {i['observaciones']}\n\n"
    return texto.strip()

# Generacion del informe
if submit:
    grupo = "Adolescentes varones" if edad < 18 and sexo == "Masculino" else             "Adolescentes mujeres" if edad < 18 else             "Hombres adultos" if sexo == "Masculino" else "Mujeres adultas"
    contexto = "Libertad" if libertad == "Libertad" else "Prision"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Informe de Evaluacion Conductual - BIAS", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"Edad: {edad}", ln=True)
    pdf.cell(200, 10, txt=f"Sexo: {sexo}", ln=True)
    pdf.cell(200, 10, txt=f"Tipo de delito: {delito}", ln=True)
    pdf.cell(200, 10, txt=f"Reincidencia: {'Si' if reincidencia else 'No'}", ln=True)
    pdf.cell(200, 10, txt=f"Impulsividad: {'Si' if impulsividad else 'No'}", ln=True)
    pdf.cell(200, 10, txt=f"Conciencia sobre el dano: {conciencia_dano}", ln=True)
    pdf.cell(200, 10, txt=f"Red de apoyo: {red_apoyo}", ln=True)
    pdf.cell(200, 10, txt=f"Estabilidad residencial: {estabilidad}", ln=True)
    pdf.cell(200, 10, txt=f"Situacion laboral: {empleo}", ln=True)
    pdf.cell(200, 10, txt=f"Consumo de sustancias: {consumo}", ln=True)
    pdf.cell(200, 10, txt=f"Situacion legal: {libertad}", ln=True)
    pdf.cell(200, 10, txt=f"Tipo de medicacion: {medicacion}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha de evaluacion: {fecha}", ln=True)
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

    with open(nombre_archivo, "rb") as file:
        st.download_button(
            label="Descargar informe completo (PDF)",
            data=file,
            file_name=nombre_archivo,
            mime="application/pdf"
        )
