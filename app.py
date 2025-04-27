import streamlit as st
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

st.set_page_config(page_title="BIAS", page_icon="🕵️", layout="wide")

# Traducciones completas
translations = {
    "Español": {
        "app_title": "BIAS - Sistema de Análisis de Inteligencia Conductual",
        "login": "Iniciar Sesión",
        "username": "Usuario",
        "password": "Contraseña",
        "logout": "Cerrar Sesión",
        "submit": "Enviar evaluación",
        "profile_section": "Perfil de Evaluación",
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
        "none_edu": "Ninguno",
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
        "narcissistic": "Narcisista",
        "histrionic": "Histriónico",
        "passive_aggressive": "Pasivo-agresivo",
        "schizoid": "Esquizoide",
        "obsessive": "Obcecado con el control",
        "none_traits": "Ninguno significativo",
        "diagnosis_list": "Diagnósticos previos",
        "therapy": "Terapias previas",
        "therapy_date": "Fecha de inicio de terapia",
        "alarm_date": "Año de señales de alarma",
        "interest_profile": "Motivo de interés",
        "family_extremism": "Antecedentes de extremismo familiar",
        "clinical_history": "Historial clínico",
        "psychological_profile": "Perfil psicológico",
        "additional_comments": "Comentarios adicionales",
        "upload_photo": "Subir foto del sujeto",
        "download_report": "Descargar Informe Genérico",
        "download_director": "Descargar Informe Dirección",
        "risk_level": "Nivel de riesgo",
        "risk_explanation": "Explicación del nivel de riesgo",
        "recommendations": "Recomendaciones institucionales",
        "therapy_recs": "Recomendaciones terapéuticas",
        "medication_recs": "Recomendaciones farmacológicas",
        "reintegration_recs": "Terapias de reinserción",
        "prevention_recs": "Medidas de prevención",
        "urgent_measures": "Medidas de urgencia",
        "graphics": "Gráficos y Tablas",
        "danger_table": "Tabla de peligro de atentado",
        "evolution_table": "Tabla de evolución del peligro si no se trata",
        "confidential": "Confidencial - Uso restringido",
        "executive_summary": "Resumen Ejecutivo",
        "date": "Fecha de generación",
        "analyst": "Responsable/Analista"
    },
    "English": {
        "app_title": "BIAS - Behavioral Intelligence Analysis System",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "logout": "Logout",
        "submit": "Submit evaluation",
        "profile_section": "Evaluation Profile",
        "name": "Full name",
        "id_number": "ID number",
        "age": "Age",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "other": "Other",
        "education": "Education level",
        "primary": "Primary",
        "secondary": "Secondary",
        "university": "University",
        "postgraduate": "Postgraduate",
        "none_edu": "None",
        "substances": "Substance use",
        "alcohol": "Alcohol",
        "tobacco": "Tobacco",
        "recreational": "Recreational drugs",
        "cocaine": "Cocaine",
        "heroin": "Heroin",
        "none_substance": "None",
        "criminal_record": "Criminal record",
        "theft": "Theft",
        "gender_violence": "Gender violence",
        "homicide": "Homicide",
        "terrorism": "Terrorism",
        "none_criminal": "None",
        "personality_traits": "Personality traits",
        "paranoid": "Paranoid",
        "antisocial": "Antisocial",
        "sadomasochistic": "Sadomasochistic",
        "impulsive": "Impulsive",
        "unstable": "Emotionally unstable",
        "dependent": "Dependent",
        "avoidant": "Avoidant",
        "narcissistic": "Narcissistic",
        "histrionic": "Histrionic",
        "passive_aggressive": "Passive-aggressive",
        "schizoid": "Schizoid",
        "obsessive": "Obsessive",
        "none_traits": "No significant traits",
        "diagnosis_list": "Previous diagnoses",
        "therapy": "Previous therapies",
        "therapy_date": "Therapy start date",
        "alarm_date": "Year of warning signs",
        "interest_profile": "Reason for interest",
        "family_extremism": "Family history of extremism",
        "clinical_history": "Clinical history",
        "psychological_profile": "Psychological profile",
        "additional_comments": "Additional comments",
        "upload_photo": "Upload subject photo",
        "download_report": "Download Generic Report",
        "download_director": "Download Director Report",
        "risk_level": "Risk level",
        "risk_explanation": "Risk level explanation",
        "recommendations": "Institutional recommendations",
        "therapy_recs": "Therapeutic recommendations",
        "medication_recs": "Pharmacological recommendations",
        "reintegration_recs": "Reintegration therapies",
        "prevention_recs": "Prevention measures",
        "urgent_measures": "Urgent measures",
        "graphics": "Graphics and Tables",
        "danger_table": "Attack danger table",
        "evolution_table": "Danger evolution table if untreated",
        "confidential": "Confidential - Restricted use",
        "executive_summary": "Executive Summary",
        "date": "Generation date",
        "analyst": "Responsible/Analyst"
    },
    "Français": {
        "therapy_date": "Date de début de la thérapie",
        # ... añade el resto de claves igual ...
    },
    "العربية": {
        "therapy_date": "تاريخ بدء العلاج",
        # ... añade el resto de claves igual ...
    }
}

def get_translation(key):
    if 'lang' not in st.session_state:
        st.session_state.lang = "Español"
    return translations[st.session_state.lang].get(key, key)

class ProfessionalPDF(FPDF):
    def __init__(self, lang="Español"):
        super().__init__()
        self.lang = lang
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        self.set_font('DejaVu', '', 12)
    # ... el resto de métodos igual ...

def main():
    if 'lang' not in st.session_state:
        st.session_state.lang = "Español"
    st.sidebar.title("🌍 Idioma / Language")
    lang_options = list(translations.keys())
    selected_lang = st.sidebar.selectbox(
        "Idioma", 
        lang_options,
        index=lang_options.index(st.session_state.lang) if st.session_state.lang in lang_options else 0
    )
    st.session_state.lang = selected_lang
    if 'auth' not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        st.title(get_translation("app_title"))
        user = st.text_input(get_translation("username"))
        pwd = st.text_input(get_translation("password"), type="password")
        if st.button(get_translation("login")):
            if user in ["demo_bias", "JuanCarlos_bias", "Cristina_bias"] and pwd == "biasdemo2025":
                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        return
    if st.sidebar.button(get_translation("logout")):
        st.session_state.auth = False
        st.rerun()
    st.title(get_translation("app_title"))
    with st.form(key="main_form"):
        # ... todos tus campos ...
        therapy = st.text_input(get_translation("therapy"))
        therapy_date = st.date_input(get_translation("therapy_date")) if therapy else None
        # ... el resto de campos ...
        submitted = st.form_submit_button(get_translation("submit"))
    if submitted:
        # ... tu lógica de generación de PDF ...
        pass

if __name__ == "__main__":
    main()

