import streamlit as st
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io
import os

# Configuración de la página
st.set_page_config(
    page_title="BIAS - Behavioral Intelligence Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Traducción y listas ampliadas (solo Español para ejemplo)
translations = {
    "Español": {
        "app_title": "BIAS - Sistema de Análisis de Inteligencia Conductual",
        "welcome": "Bienvenido/a al Sistema de Análisis de Inteligencia Conductual",
        "login": "Iniciar Sesión",
        "username": "Usuario",
        "password": "Contraseña",
        "login_button": "Entrar",
        "language": "Idioma",
        "logout": "Cerrar Sesión",
        "profile_section": "Perfil de evaluación",
        "name": "Nombre completo",
        "id_number": "Número de identificación",
        "age": "Edad",
        "gender": "Género",
        "male": "Masculino",
        "female": "Femenino",
        "other": "Otro",
        "education": "Nivel educativo",
        "primary": "Primaria",
        "secondary": "Secundaria",
        "university": "Universidad",
        "postgraduate": "Postgrado",
        "none": "Sin estudios",
        "substances": "Consumo de sustancias",
        "alcohol": "Alcohol",
        "tobacco": "Tabaco",
        "recreational": "Drogas recreativas",
        "cocaine": "Cocaína",
        "heroin": "Heroína",
        "none_substance": "Ninguna",
        "criminal_record": "Antecedentes penales",
        "theft": "Robo",
        "gender_violence": "Violencia de género",
        "homicide": "Homicidio",
        "terrorism": "Terrorismo",
        "none_criminal": "Ninguno",
        "personality_traits": "Rasgos de personalidad",
        "paranoid": "Paranoide",
        "antisocial": "Antisocial",
        "sadomasochistic": "Sadomasoquista",
        "impulsive": "Impulsivo",
        "unstable": "Emocionalmente inestable",
        "dependent": "Dependiente",
        "avoidant": "Evitativo",
        "none_traits": "Ninguno significativo",
        "submit": "Enviar evaluación",
        "results_section": "Resultados de la evaluación",
        "risk_level": "Nivel de riesgo:",
        "high": "ALTO",
        "moderate": "MODERADO",
        "low": "BAJO",
        "evaluation_date": "Fecha de evaluación:",
        "generate_report": "Generar informe",
        "download_report": "Descargar Informe",
        "download_detailed": "Descargar Informe Detallado",
        "login_error": "Usuario o contraseña incorrectos",
        "field_required": "Este campo es obligatorio",
        "results_info": "Tras enviar la evaluación, aquí se mostrarán los resultados del análisis de riesgo.",
        "recommendations": "Recomendaciones institucionales",
        "therapy_recs": "Recomendaciones Terapéuticas",
        "medication_recs": "Recomendaciones Farmacológicas",
        "reintegration_recs": "Terapias de Reinserción",
        "prevention_recs": "Medidas de Prevención",
        "urgent_measures": "Medidas de Urgencia",
        "explanation": "Explicación del Nivel de Riesgo",
        "high_explanation": "El sujeto presenta múltiples factores de riesgo significativos que sugieren una alta probabilidad de radicalización violenta. Se recomienda intervención inmediata y monitoreo constante.",
        "moderate_explanation": "El sujeto presenta algunos factores de riesgo relevantes que requieren atención y seguimiento. Se recomienda intervención preventiva y evaluación periódica.",
        "low_explanation": "El sujeto presenta pocos factores de riesgo. Se recomienda seguimiento rutinario y medidas preventivas básicas.",
        "scoring_report": "Informe Detallado de Puntuación",
        "detailed_scoring": "Puntuación Detallada",
        "total_risk_score": "Puntuación total de riesgo",
        "education_score": "Puntuación nivel educativo",
        "substances_score": "Puntuación consumo de sustancias",
        "criminal_score": "Puntuación antecedentes penales",
        "personality_score": "Puntuación rasgos de personalidad",
        "diagnosis_list": "Diagnósticos previos",
        "previous_therapies": "Terapias previas",
        "therapy_date": "Fecha de inicio de terapia",
        "select_date": "Seleccionar fecha",
        "alarm_date": "Fecha de señales de alarma",
        "interest_profile": "Motivo de interés",
        "family_extremism": "Antecedentes de extremismo familiar",
        "upload_photo": "Subir fotografía del sujeto",
        "upload_button": "Subir imagen",
        "photo_requirements": "La fotografía debe ser tipo carnet con fondo blanco",
        "clinical_history": "Historial Clínico",
        "psychological_profile": "Perfil Psicológico",
        "additional_comments": "Comentarios Adicionales"
    }
}

# Listas ampliadas
antecedentes_extra = [
    "Aislamiento social progresivo", "Justificación de la violencia", "Fascinación por ideologías extremistas",
    "Cambios drásticos en el comportamiento", "Expresión de odio hacia grupos específicos",
    "Contacto con individuos radicalizados", "Consumo de propaganda extremista",
    "Participación en actividades sospechosas online", "Intento de reclutamiento de otros",
    "Preparación física para el combate"
]
diagnosticos_extra = [
    "Trastorno de estrés postraumático (TEPT)", "Trastorno límite de la personalidad (TLP)",
    "Trastorno bipolar", "Esquizofrenia", "Depresión mayor recurrente",
    "Trastorno obsesivo-compulsivo (TOC)", "Trastorno de ansiedad generalizada (TAG)",
    "Trastorno de pánico", "Fobia social", "Trastorno de la conducta"
]
rasgos_extra = [
    "Narcisista", "Histriónico", "Pasivo-agresivo", "Esquizoide", "Obcecado con el control"
]

def generate_generic_report(*args):
    st.success("Informe genérico generado (aquí iría la lógica PDF y gráficos).")
    st.write(args)

def generate_director_report(*args):
    st.success("Informe de dirección generado (aquí iría la lógica PDF, gráficos y sistema de puntuación).")
    st.write(args)

def main():
    st.title(translations["Español"]["app_title"])
    username = st.text_input(translations["Español"]["username"])
    password = st.text_input(translations["Español"]["password"], type="password")

    if st.button(translations["Español"]["login_button"]):
        if username and password:
            st.success(translations["Español"]["welcome"] + f", {username}!")
            with st.form("formulario_bias"):
                st.header(translations["Español"]["profile_section"])
                col1, col2, col3 = st.columns(3)
                with col1:
                    name = st.text_input(translations["Español"]["name"])
                    id_number = st.text_input(translations["Español"]["id_number"])
                    age = st.number_input(translations["Español"]["age"], min_value=0, max_value=120, value=18)
                    gender = st.selectbox(translations["Español"]["gender"], [translations["Español"]["male"], translations["Español"]["female"], translations["Español"]["other"]])
                    education = st.selectbox(translations["Español"]["education"], [translations["Español"]["primary"], translations["Español"]["secondary"], translations["Español"]["university"], translations["Español"]["postgraduate"], translations["Español"]["none"]])
                with col2:
                    substances = st.multiselect(translations["Español"]["substances"], [translations["Español"]["alcohol"], translations["Español"]["tobacco"], translations["Español"]["recreational"], translations["Español"]["cocaine"], translations["Español"]["heroin"], translations["Español"]["none_substance"]])
                    criminal_record = st.multiselect(translations["Español"]["criminal_record"], [translations["Español"]["theft"], translations["Español"]["gender_violence"], translations["Español"]["homicide"], translations["Español"]["terrorism"], translations["Español"]["none_criminal"]] + antecedentes_extra)
                    personality_traits = st.multiselect(translations["Español"]["personality_traits"], [translations["Español"]["paranoid"], translations["Español"]["antisocial"], translations["Español"]["sadomasochistic"], translations["Español"]["impulsive"], translations["Español"]["unstable"], translations["Español"]["dependent"], translations["Español"]["avoidant"], translations["Español"]["none_traits"]] + rasgos_extra)
                with col3:
                    diagnosis_list = st.multiselect(translations["Español"]["diagnosis_list"], diagnosticos_extra)
                    previous_therapies = st.text_input(translations["Español"]["previous_therapies"])
                    therapy_date = st.date_input(translations["Español"]["therapy_date"], datetime.now())
                    alarm_date = st.date_input(translations["Español"]["alarm_date"], datetime.now()).year
                    st.write(f"Año de señales de alarma: {alarm_date}")
                st.header("Información Adicional")
                col4, col5, col6 = st.columns(3)
                with col4:
                    clinical_history = st.text_area(translations["Español"]["clinical_history"])
                with col5:
                    psychological_profile = st.text_area(translations["Español"]["psychological_profile"])
                with col6:
                    additional_comments = st.text_area(translations["Español"]["additional_comments"])
                enviado = st.form_submit_button(translations["Español"]["submit"])

            if enviado:
                if username == "demo_bias":
                    generate_generic_report(name, id_number, age, gender, education, substances, criminal_record, personality_traits, diagnosis_list, previous_therapies, therapy_date, alarm_date, clinical_history, psychological_profile, additional_comments)
                elif username in ["JuanCarlos_bias", "Cristina_bias"]:
                    generate_generic_report(name, id_number, age, gender, education, substances, criminal_record, personality_traits, diagnosis_list, previous_therapies, therapy_date, alarm_date, clinical_history, psychological_profile, additional_comments)
                    generate_director_report(name, id_number, age, gender, education, substances, criminal_record, personality_traits, diagnosis_list, previous_therapies, therapy_date, alarm_date, clinical_history, psychological_profile, additional_comments)
                else:
                    st.warning("No se puede generar el informe para este usuario.")
        else:
            st.error(translations["Español"]["login_error"])

if __name__ == "__main__":
    main()
