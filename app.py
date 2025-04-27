import streamlit as st
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io
import base64
from PIL import Image
import os

# Configuración de la página
st.set_page_config(
    page_title="BIAS - Behavioral Intelligence Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Diccionarios para traducción
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
        "hate_speech": "Discurso de odio",
        "online_radicalization": "Radicalización en línea",
        "travel_attempts": "Intentos de viaje a zonas de conflicto",
        "financial_support": "Apoyo financiero a grupos extremistas",
        "possession_weapons": "Posesión de armas",
        "attack_planning": "Planificación de ataques",
        "recruitment": "Reclutamiento de nuevos miembros",
        "propaganda_consumption": "Consumo de propaganda extremista",
        "isolation": "Aislamiento social",
        "identity_crisis": "Crisis de identidad",
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
        "ptsd": "Trastorno de estrés postraumático (TEPT)",
        "bpd": "Trastorno límite de la personalidad (TLP)",
        "bipolar": "Trastorno bipolar",
        "schizophrenia": "Esquizofrenia",
        "major_depression": "Depresión mayor recurrente",
        "ocd": "Trastorno obsesivo-compulsivo (TOC)",
        "gad": "Trastorno de ansiedad generalizada (TAG)",
        "panic_disorder": "Trastorno de pánico",
        "social_phobia": "Fobia social",
        "conduct_disorder": "Trastorno de la conducta",
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
additional_terrorism_antecedents = [
    "hate_speech", "online_radicalization", "travel_attempts",
    "financial_support", "possession_weapons", "attack_planning",
    "recruitment", "propaganda_consumption", "isolation", "identity_crisis"
]

additional_mental_health_traits = [
    "ptsd", "bpd", "bipolar", "schizophrenia", "major_depression",
    "ocd", "gad", "panic_disorder", "social_phobia", "conduct_disorder"
]

additional_personality_traits = [
    "narcissistic", "histrionic", "passive_aggressive", "schizoid", "obsessive"
]

def main():
    # Configuración inicial del estado de la sesión
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.user_data = {}

    st.title(translations["Español"]["app_title"])

    # Barra lateral para login/logout
    with st.sidebar:
        if not st.session_state.authenticated:
            st.header("Autenticación")
            username = st.text_input(translations["Español"]["username"])
            password = st.text_input(translations["Español"]["password"], type="password")
            
            if st.button(translations["Español"]["login_button"]):
                # Validación básica (usuarios demo)
                if username in ["demo_bias", "JuanCarlos_bias", "Cristina_bias"] and password == "biasdemo2025":
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error(translations["Español"]["login_error"])
        else:
            st.header(f"Bienvenido, {st.session_state.username}")
            if st.button(translations["Español"]["logout"]):
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.rerun()

    if st.session_state.authenticated:
        with st.container():
            st.header(translations["Español"]["profile_section"])
            
            with st.form(key="main_form"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    name = st.text_input(translations["Español"]["name"])
                    id_number = st.text_input(translations["Español"]["id_number"])
                    age = st.number_input(translations["Español"]["age"], min_value=0, max_value=120, value=18)
                    gender = st.selectbox(translations["Español"]["gender"], 
                                       [translations["Español"]["male"], 
                                        translations["Español"]["female"], 
                                        translations["Español"]["other"]])
                    education = st.selectbox(translations["Español"]["education"], 
                                          [translations["Español"]["primary"], 
                                           translations["Español"]["secondary"], 
                                           translations["Español"]["university"], 
                                           translations["Español"]["postgraduate"], 
                                           translations["Español"]["none"]])
                
                with col2:
                    substances = st.multiselect(
                        translations["Español"]["substances"],
                        [translations["Español"]["alcohol"], 
                         translations["Español"]["tobacco"],
                         translations["Español"]["recreational"],
                         translations["Español"]["cocaine"],
                         translations["Español"]["heroin"],
                         translations["Español"]["none_substance"]]
                    )
                    
                    criminal_record = st.multiselect(
                        translations["Español"]["criminal_record"],
                        [translations["Español"]["theft"],
                         translations["Español"]["gender_violence"],
                         translations["Español"]["homicide"],
                         translations["Español"]["terrorism"],
                         translations["Español"]["none_criminal"]] +
                        [translations["Español"][item] for item in additional_terrorism_antecedents]
                    )
                    
                    personality_traits = st.multiselect(
                        translations["Español"]["personality_traits"],
                        [translations["Español"]["paranoid"],
                         translations["Español"]["antisocial"],
                         translations["Español"]["sadomasochistic"],
                         translations["Español"]["impulsive"],
                         translations["Español"]["unstable"],
                         translations["Español"]["dependent"],
                         translations["Español"]["avoidant"],
                         translations["Español"]["none_traits"]] +
                        [translations["Español"][item] for item in additional_personality_traits]
                    )
                
                with col3:
                    diagnosis_list = st.multiselect(
                        translations["Español"]["diagnosis_list"], 
                        [translations["Español"][item] for item in additional_mental_health_traits]
                    )
                    
                    previous_therapies = st.selectbox(
                        translations["Español"]["previous_therapies"],
                        ["Ninguna", "Psicoterapia", "Farmacológica", "Mixta"]
                    )
                    
                    therapy_date = st.date_input(
                        translations["Español"]["therapy_date"],
                        disabled=(previous_therapies == "Ninguna")
                    )
                    
                    alarm_year = st.selectbox(
                        "Año de señales de alarma",
                        options=list(range(2000, datetime.now().year + 1)),
                        index=datetime.now().year - 2000
                    )
                
                # Nueva sección de información adicional
                st.header("Información Adicional")
                col4, col5 = st.columns(2)
                with col4:
                    interest_reason = st.text_area(translations["Español"]["interest_profile"])
                    family_extremism = st.text_area(translations["Español"]["family_extremism"])
                with col5:
                    clinical_history = st.text_area(translations["Español"]["clinical_history"])
                    psychological_profile = st.text_area(translations["Español"]["psychological_profile"])
                    additional_comments = st.text_area(translations["Español"]["additional_comments"])
                
                # Subida de foto
                uploaded_photo = st.file_uploader(
                    translations["Español"]["upload_photo"],
                    type=["jpg", "png", "jpeg"]
                )
                
                submitted = st.form_submit_button(translations["Español"]["submit"])

                if submitted:
                    # Guardar datos en el estado de la sesión
                    st.session_state.user_data = {
                        'name': name,
                        'id_number': id_number,
                        'age': age,
                        'gender': gender,
                        'education': education,
                        'substances': substances,
                        'criminal_record': criminal_record,
                        'personality_traits': personality_traits,
                        'diagnosis_list': diagnosis_list,
                        'previous_therapies': previous_therapies,
                        'therapy_date': therapy_date,
                        'alarm_year': alarm_year,
                        'interest_reason': interest_reason,
                        'family_extremism': family_extremism,
                        'clinical_history': clinical_history,
                        'psychological_profile': psychological_profile,
                        'additional_comments': additional_comments,
                        'photo': uploaded_photo
                    }

        # Generación de informes después del envío
        if submitted and st.session_state.user_data:
            generate_report(st.session_state.user_data)
            if st.session_state.username in ["JuanCarlos_bias", "Cristina_bias"]:
                generate_detailed_report(st.session_state.user_data)

def generate_report(user_data):
    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Configuración básica del PDF
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Informe BIAS", ln=True, align='C')
    pdf.ln(10)
    
    # Datos básicos
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Nombre: {user_data['name']}", ln=True)
    pdf.cell(200, 10, txt=f"ID: {user_data['id_number']}", ln=True)
    pdf.cell(200, 10, txt=f"Edad: {user_data['age']}", ln=True)
    pdf.cell(200, 10, txt=f"Género: {user_data['gender']}", ln=True)
    
    # Añadir más datos según necesidad...
    
    # Guardar PDF en bytes
    pdf_output = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
    
    # Botón de descarga
    st.download_button(
        label=translations["Español"]["download_report"],
        data=pdf_output,
        file_name="informe_bias.pdf",
        mime="application/pdf"
    )

def generate_detailed_report(user_data):
    # Similar a generate_report pero con más detalles
    pass

if __name__ == "__main__":
    main()
