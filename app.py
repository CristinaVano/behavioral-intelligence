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

# Diccionarios para traducción (versión completa)
translations = {
    "Español": {
        # ... (todas las traducciones anteriores)
        # Nuevas entradas para antecedentes
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
        # Nuevos diagnósticos
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
        # Nuevos rasgos de personalidad
        "narcissistic": "Narcisista",
        "histrionic": "Histriónico",
        "passive_aggressive": "Pasivo-agresivo",
        "schizoid": "Esquizoide",
        "obsessive": "Obcecado con el control",
        # Campos nuevos
        "clinical_history": "Historial Clínico",
        "psychological_profile": "Perfil Psicológico",
        "additional_comments": "Comentarios Adicionales"
    },
    # Repetir mismas adiciones para otros idiomas (English, العربية, Français)
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
    st.title(translations["Español"]["app_title"])

    # Autenticación básica
    username = st.text_input(translations["Español"]["username"])
    password = st.text_input(translations["Español"]["password"], type="password")

    if st.button(translations["Español"]["login_button"]):
        if username and password:
            st.success(translations["Español"]["welcome"] + f", {username}!")

            with st.container():
                st.header(translations["Español"]["profile_section"])
                col1, col2, col3 = st.columns(3)
                
                # Columna 1
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
                
                # Columna 2
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
                
                # Columna 3
                with col3:
                    diagnosis_list = st.multiselect(
                        translations["Español"]["diagnosis_list"],
                        [translations["Español"][item] for item in additional_mental_health_traits]
                    )
                    
                    previous_therapies = st.text_input(translations["Español"]["previous_therapies"])
                    therapy_date = st.date_input(translations["Español"]["therapy_date"], datetime.now())
                    alarm_date = st.date_input(translations["Español"]["alarm_date"], datetime.now()).year
                    st.write(f"Año de señales: {alarm_date}")
                
                # Sección de información adicional
                st.header("Información Adicional")
                col4, col5, col6 = st.columns(3)
                with col4:
                    clinical_history = st.text_area(translations["Español"]["clinical_history"])
                with col5:
                    psychological_profile = st.text_area(translations["Español"]["psychological_profile"])
                with col6:
                    additional_comments = st.text_area(translations["Español"]["additional_comments"])

            if st.button(translations["Español"]["submit"]):
                # Lógica de generación de informes
                if username == "demo_bias":
                    generate_generic_report(
                        name, id_number, age, gender, education, substances,
                        criminal_record, personality_traits, diagnosis_list,
                        previous_therapies, therapy_date, alarm_date,
                        clinical_history, psychological_profile, additional_comments
                    )
                elif username in ["JuanCarlos_bias", "Cristina_bias"]:
                    generate_generic_report(...)
                    generate_director_report(
                        name, id_number, age, gender, education, substances,
                        criminal_record, personality_traits, diagnosis_list,
                        previous_therapies, therapy_date, alarm_date,
                        clinical_history, psychological_profile, additional_comments
                    )

def generate_generic_report(...):
    # Implementación completa de generación de PDF con:
    # - Todos los campos nuevos incluidos
    # - Gráficos de riesgo
    # - Explicaciones detalladas

def generate_director_report(...):
    # Implementación con:
    # - Sistema de puntuación detallado
    # - Metodología de evaluación
    # - Datos técnicos completos

if __name__ == "__main__":
    main()

