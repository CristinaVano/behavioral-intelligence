import streamlit as st
from datetime import datetime
from fpdf import FPDF
import io
import os
from PIL import Image

# ============ TRADUCCIONES =============
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
        "therapy": "Terapias previas y fecha de inicio",
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
        "therapy": "Previous therapies and start date",
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
    }
    # Añade aquí Francés y Árabe siguiendo el mismo patrón, incluyendo "therapy_date"
}

def get_translation(key):
    return translations[st.session_state.lang][key]

class ProfessionalPDF(FPDF):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font('Helvetica', '', 12)

    def cover(self, data):
        self.add_page()
        self.set_font('Helvetica', 'B', 22)
        self.cell(0, 15, get_translation("app_title"), 0, 1, 'C')
        self.ln(12)
        self.set_font('Helvetica', 'B', 18)
        self.cell(0, 12, get_translation("profile_section"), 0, 1, 'C')
        self.ln(10)
        self.set_font('Helvetica', '', 12)
        self.cell(0, 10, f"{get_translation('date')}: {datetime.now().strftime('%d/%m/%Y')}", 0, 1)
        self.cell(0, 10, f"{get_translation('analyst')}: {data['analyst']}", 0, 1)
        self.ln(10)
        self.set_font('Helvetica', 'I', 10)
        self.multi_cell(0, 8, get_translation("confidential"))
        self.ln(10)

    def executive_summary(self, summary):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, get_translation("executive_summary"), 0, 1)
        self.set_font('Helvetica', '', 12)
        self.multi_cell(0, 8, summary)
        self.ln(5)

    def subject_data(self, data):
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, get_translation("profile_section"), 0, 1)
        self.set_font('Helvetica', '', 11)
        for k, v in data.items():
            if k == "photo" or k == "analyst":
                continue
            self.cell(60, 8, f"{get_translation(k)}:", 1)
            self.cell(0, 8, str(v), 1, 1)
        if data.get("photo"):
            img = Image.open(data["photo"])
            img_path = "temp_photo.jpg"
            img.save(img_path)
            self.image(img_path, x=170, y=self.get_y()-50, w=30)
            os.remove(img_path)
        self.ln(4)

    def risk_section(self, risk_level, explanation):
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, get_translation("risk_level"), 0, 1)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 8, f"{get_translation('risk_level')}: {risk_level}", 0, 1)
        self.set_font('Helvetica', '', 11)
        self.multi_cell(0, 8, f"{get_translation('risk_explanation')}: {explanation}")
        self.ln(5)

    def recommendations_section(self, recs):
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, get_translation("recommendations"), 0, 1)
        self.set_font('Helvetica', '', 11)
        for title, text in recs:
            self.set_font('Helvetica', 'B', 11)
            self.cell(0, 8, f"- {title}:", 0, 1)
            self.set_font('Helvetica', '', 11)
            self.multi_cell(0, 7, text)
        self.ln(5)

    def graphics_section(self):
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, get_translation("graphics"), 0, 1)
        self.set_font('Helvetica', '', 11)
        self.cell(0, 8, get_translation("danger_table"), 0, 1)
        self.cell(0, 8, get_translation("evolution_table"), 0, 1)
        self.cell(0, 8, "(Gráficos y tablas disponibles en plataforma digital)", 0, 1)
        self.ln(5)

def main():
    st.set_page_config(page_title="BIAS", page_icon="🕵️", layout="wide")
    if 'lang' not in st.session_state:
        st.session_state.lang = "Español"
    st.sidebar.title("🌍 Idioma / Language")
    st.session_state.lang = st.sidebar.selectbox("Idioma", list(translations.keys()), index=0)
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
        return
    else:
        if st.sidebar.button(get_translation("logout")):
            st.session_state.auth = False
            st.rerun()
    st.title(get_translation("app_title"))
    with st.form("main_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(get_translation("name"))
            id_number = st.text_input(get_translation("id_number"))
            age = st.number_input(get_translation("age"), 12, 100)
            gender = st.selectbox(get_translation("gender"), [
                get_translation("male"), get_translation("female"), get_translation("other")
            ])
            education = st.selectbox(get_translation("education"), [
                get_translation("primary"), get_translation("secondary"), get_translation("university"),
                get_translation("postgraduate"), get_translation("none_edu")
            ])
            substances = st.multiselect(get_translation("substances"), [
                get_translation("alcohol"), get_translation("tobacco"), get_translation("recreational"),
                get_translation("cocaine"), get_translation("heroin"), get_translation("none_substance")
            ])
            criminal_record = st.multiselect(get_translation("criminal_record"), [
                get_translation("theft"), get_translation("gender_violence"), get_translation("homicide"),
                get_translation("terrorism"), get_translation("none_criminal"),
                "Aislamiento social progresivo", "Justificación de la violencia", "Fascinación por ideologías extremistas",
                "Cambios drásticos en el comportamiento", "Expresión de odio hacia grupos específicos",
                "Contacto con individuos radicalizados", "Consumo de propaganda extremista",
                "Participación en actividades sospechosas online", "Intento de reclutamiento de otros",
                "Preparación física para el combate"
            ])
        with col2:
            personality_traits = st.multiselect(get_translation("personality_traits"), [
                get_translation("paranoid"), get_translation("antisocial"), get_translation("sadomasochistic"),
                get_translation("impulsive"), get_translation("unstable"), get_translation("dependent"),
                get_translation("avoidant"), get_translation("narcissistic"), get_translation("histrionic"),
                get_translation("passive_aggressive"), get_translation("schizoid"), get_translation("obsessive"),
                get_translation("none_traits")
            ])
            diagnosis_list = st.text_area(get_translation("diagnosis_list"))
            therapy = st.text_input(get_translation("therapy"))
            therapy_date = st.date_input(get_translation("therapy_date"), disabled=(therapy == ""))
            alarm_year = st.selectbox(get_translation("alarm_date"), list(range(2000, datetime.now().year + 1)))
            interest_profile = st.text_area(get_translation("interest_profile"))
            family_extremism = st.text_area(get_translation("family_extremism"))
            clinical_history = st.text_area(get_translation("clinical_history"))
            psychological_profile = st.text_area(get_translation("psychological_profile"))
            additional_comments = st.text_area(get_translation("additional_comments"))
            uploaded_photo = st.file_uploader(get_translation("upload_photo"), type=["jpg", "png"])
        analyst = st.text_input(get_translation("analyst"), value=st.session_state.user)
        enviado = st.form_submit_button(get_translation("submit"))
    if enviado:
        executive_summary = "El sujeto presenta un perfil de riesgo elevado por la concurrencia de factores penales, consumo de sustancias y antecedentes familiares."
        risk_level = "ALTO"
        risk_explanation = "Factores acumulados de riesgo penal, consumo y rasgos de personalidad."
        recommendations = [
            (get_translation("therapy_recs"), "Intervención intensiva por especialista en radicalización."),
            (get_translation("medication_recs"), "Evaluación psiquiátrica para control farmacológico."),
            (get_translation("reintegration_recs"), "Programa de reinserción social supervisado."),
            (get_translation("prevention_recs"), "Medidas de prevención comunitaria."),
            (get_translation("urgent_measures"), "Monitorización inmediata y restricción de movimientos.")
        ]
        pdf = ProfessionalPDF(st.session_state.lang)
        pdf.cover({"analyst": analyst})
        pdf.executive_summary(executive_summary)
        pdf.subject_data({
            "name": name, "id_number": id_number, "age": age, "gender": gender,
            "education": education, "substances": ", ".join(substances),
            "criminal_record": ", ".join(criminal_record),
            "personality_traits": ", ".join(personality_traits),
            "diagnosis_list": diagnosis_list,
            "therapy": therapy, "therapy_date": therapy_date,
            "alarm_year": alarm_year, "interest_profile": interest_profile,
            "family_extremism": family_extremism,
            "clinical_history": clinical_history,
            "psychological_profile": psychological_profile,
            "additional_comments": additional_comments,
            "photo": uploaded_photo,
            "analyst": analyst
        })
        pdf.risk_section(risk_level, risk_explanation)
        pdf.recommendations_section(recommendations)
        pdf.graphics_section()
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button(get_translation("download_report"), pdf_bytes, file_name="bias_report.pdf", mime="application/pdf")
        if st.session_state.user in ["JuanCarlos_bias", "Cristina_bias"]:
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 14)
            pdf.cell(0, 10, "Sistema de puntuación y justificación técnica", 0, 1)
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 8, "Desglose de puntuaciones por área/factor y justificación técnica de cada decisión.")
            pdf_dir_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button(get_translation("download_director"), pdf_dir_bytes, file_name="bias_director_report.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
