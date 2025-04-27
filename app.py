import streamlit as st
from datetime import datetime
from fpdf import FPDF
import io
import os
import base64
from PIL import Image

# =============================================
# CONFIGURACIÓN MULTI-IDIOMA (COMPLETA)
# =============================================
translations = {
    "Español": {
        "app_title": "BIAS - Sistema de Análisis de Inteligencia Conductual",
        "login": "Iniciar Sesión",
        "username": "Usuario",
        "password": "Contraseña",
        "logout": "Cerrar Sesión",
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
        "obsessive": "Obcecado",
        "none_traits": "Ninguno significativo",
        "submit": "Enviar evaluación",
        "results_section": "Resultados de la evaluación",
        "risk_level": "Nivel de riesgo",
        "high": "ALTO",
        "moderate": "MODERADO",
        "low": "BAJO",
        "therapy": "Terapias previas",
        "therapy_date": "Fecha de inicio",
        "alarm_date": "Año de señales",
        "interest_profile": "Motivo de interés",
        "family_extremism": "Antecedentes de extremismo familiar",
        "upload_photo": "Subir foto del sujeto",
        "photo_requirements": "Formato carnet con fondo blanco",
        "clinical_history": "Historial clínico",
        "psychological_profile": "Perfil psicológico",
        "additional_comments": "Comentarios adicionales",
        "download_report": "Descargar Informe",
        "download_director": "Informe para Dirección"
    },
    "English": {
        "app_title": "BIAS - Behavioral Intelligence Analysis System",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "logout": "Logout",
        "profile_section": "Evaluation Profile",
        # ... (completar todas las traducciones)
    },
    "Français": {
        "app_title": "BIAS - Système d'Analyse de l'Intelligence Comportementale",
        "login": "Connexion",
        # ... (completar todas las traducciones)
    },
    "العربية": {
        "app_title": "بياس - نظام تحليل الذكاء السلوكي",
        "login": "تسجيل الدخول",
        # ... (completar todas las traducciones)
    }
}

# =============================================
# CLASE PARA GENERACIÓN DE PDF
# =============================================
class BIASPDF(FPDF):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        if lang == "العربية":
            self.set_rtl(True)
            self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
            self.set_font('DejaVu', '', 12)
        else:
            self.set_font('Helvetica', '', 12)
    
    def header(self):
        self.set_font('Helvetica', 'B', 16) if self.lang != "العربية" else self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, translations[self.lang]["app_title"], 0, 1, 'C')
        self.ln(10)
    
    def add_section(self, title, content):
        self.set_font('Helvetica', 'B', 14) if self.lang != "العربية" else self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, title, 0, 1)
        self.set_font('Helvetica', '', 12) if self.lang != "العربية" else self.set_font('DejaVu', '', 12)
        self.multi_cell(0, 8, content)
        self.ln(5)

# =============================================
# FUNCIONES PRINCIPALES
# =============================================
def get_translation(key):
    return translations[st.session_state.current_lang][key]

def generate_pdf(data, report_type):
    lang = st.session_state.current_lang
    pdf = BIASPDF(lang)
    pdf.add_page()
    
    # Encabezado
    pdf.header()
    
    # Sección de datos básicos
    basic_data = f"""
    {get_translation('name')}: {data['name']}
    {get_translation('id_number')}: {data['id_number']}
    {get_translation('age')}: {data['age']}
    {get_translation('gender')}: {data['gender']}
    {get_translation('education')}: {data['education']}
    """
    pdf.add_section(get_translation('profile_section'), basic_data)
    
    # Sección de riesgos
    risk_data = f"""
    {get_translation('substances')}: {', '.join(data['substances'])}
    {get_translation('criminal_record')}: {', '.join(data['criminal_record'])}
    {get_translation('personality_traits')}: {', '.join(data['personality_traits'])}
    """
    pdf.add_section(get_translation('risk_level'), risk_data)
    
    # Sección adicional para directores
    if report_type == "director":
        pdf.add_page()
        pdf.add_section(get_translation('download_director'), "Sistema de puntuación detallado...")
    
    return pdf.output(dest='S').encode('latin-1')

# =============================================
# INTERFAZ PRINCIPAL
# =============================================
def main():
    # Configuración inicial
    if 'current_lang' not in st.session_state:
        st.session_state.current_lang = "Español"
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Barra lateral
    with st.sidebar:
        # Selector de idioma
        lang = st.selectbox("🌍", options=list(translations.keys()))
        st.session_state.current_lang = lang
        
        # Autenticación
        if not st.session_state.authenticated:
            st.header(get_translation("login"))
            username = st.text_input(get_translation("username"))
            password = st.text_input(get_translation("password"), type="password")
            
            if st.button(get_translation("login")):
                if username in ["demo_bias", "JuanCarlos_bias", "Cristina_bias"] and password == "biasdemo2025":
                    st.session_state.authenticated = True
                    st.session_state.user = username
                    st.rerun()
        else:
            if st.button(get_translation("logout")):
                st.session_state.authenticated = False
                st.rerun()
    
    if st.session_state.authenticated:
        # Formulario principal
        with st.form("main_form"):
            st.title(get_translation("app_title"))
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(get_translation("name"))
                id_number = st.text_input(get_translation("id_number"))
                age = st.number_input(get_translation("age"), 12, 100)
                gender = st.selectbox(get_translation("gender"), [
                    get_translation("male"),
                    get_translation("female"),
                    get_translation("other")
                ])
                education = st.selectbox(get_translation("education"), [
                    get_translation("primary"),
                    get_translation("secondary"),
                    get_translation("university"),
                    get_translation("postgraduate"),
                    get_translation("none_edu")
                ])
                substances = st.multiselect(get_translation("substances"), [
                    get_translation("alcohol"),
                    get_translation("tobacco"),
                    get_translation("recreational"),
                    get_translation("cocaine"),
                    get_translation("heroin"),
                    get_translation("none_substance")
                ])
            
            with col2:
                criminal_record = st.multiselect(get_translation("criminal_record"), [
                    get_translation("theft"),
                    get_translation("gender_violence"),
                    get_translation("homicide"),
                    get_translation("terrorism"),
                    get_translation("none_criminal"),
                    "Aislamiento social progresivo",
                    "Justificación de la violencia",
                    "Fascinación por ideologías extremistas"
                ])
                personality_traits = st.multiselect(get_translation("personality_traits"), [
                    get_translation("paranoid"),
                    get_translation("antisocial"),
                    get_translation("sadomasochistic"),
                    get_translation("impulsive"),
                    get_translation("unstable"),
                    get_translation("dependent"),
                    get_translation("avoidant"),
                    get_translation("narcissistic"),
                    get_translation("histrionic"),
                    get_translation("passive_aggressive"),
                    get_translation("schizoid"),
                    get_translation("obsessive"),
                    get_translation("none_traits")
                ])
                therapy = st.text_input(get_translation("therapy"))
                therapy_date = st.date_input(get_translation("therapy_date"), disabled=(therapy == ""))
                alarm_year = st.selectbox(get_translation("alarm_date"), list(range(2000, datetime.now().year + 1)))
                interest_profile = st.text_area(get_translation("interest_profile"))
                family_extremism = st.text_area(get_translation("family_extremism"))
                clinical_history = st.text_area(get_translation("clinical_history"))
                psychological_profile = st.text_area(get_translation("psychological_profile"))
                additional_comments = st.text_area(get_translation("additional_comments"))
                uploaded_photo = st.file_uploader(get_translation("upload_photo"), type=["jpg", "png"])
            
            if st.form_submit_button(get_translation("submit")):
                data = {
                    'name': name,
                    'id_number': id_number,
                    'age': age,
                    'gender': gender,
                    'education': education,
                    'substances': substances,
                    'criminal_record': criminal_record,
                    'personality_traits': personality_traits,
                    'therapy': therapy,
                    'therapy_date': therapy_date,
                    'alarm_year': alarm_year,
                    'interest_profile': interest_profile,
                    'family_extremism': family_extremism,
                    'clinical_history': clinical_history,
                    'psychological_profile': psychological_profile,
                    'additional_comments': additional_comments,
                    'photo': uploaded_photo
                }
                
                # Generar PDF genérico
                pdf_bytes = generate_pdf(data, "generic")
                st.session_state.pdf_generic = pdf_bytes
                
                # Generar PDF para dirección
                if st.session_state.user in ["JuanCarlos_bias", "Cristina_bias"]:
                    pdf_dir_bytes = generate_pdf(data, "director")
                    st.session_state.pdf_director = pdf_dir_bytes
        
        # Descargas
        if 'pdf_generic' in st.session_state:
            st.download_button(
                label=get_translation("download_report"),
                data=st.session_state.pdf_generic,
                file_name="bias_report.pdf",
                mime="application/pdf"
            )
            if 'pdf_director' in st.session_state:
                st.download_button(
                    label=get_translation("download_director"),
                    data=st.session_state.pdf_director,
                    file_name="bias_director_report.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
