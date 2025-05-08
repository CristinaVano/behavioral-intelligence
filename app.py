# -*- coding: utf-8 -*-
# --- Versión con Secciones Cualitativas y Recomendaciones Detalladas ---
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from fpdf import FPDF
import shap
import lime
import lime.lime_tabular
import numpy as np
# import matplotlib.pyplot as plt # Comentado si no se usan gráficas en PDF
import base64
from datetime import datetime
import os 
import traceback
import re # Para búsqueda simple de palabras clave (opcional)

# --- Configuración de la Página de Streamlit ---
st.set_page_config(layout="wide", page_title="Behavioral Intelligence Platform")

# --- Credenciales de Usuario (NO SEGURO PARA PRODUCCIÓN) ---
USER_CREDENTIALS = {
    "demo_bias": "biasdemo2025", "JuanCarlos_bias": "direccionbias",
    "Cristina_bias": "direccionbias", "Teresa_bias": "coordinacionbias",
    "Pau_bias": "coordinacionbias"
}

# --- Traducciones Completas (con títulos para nuevas secciones) ---
translations = {
    "es": {
        "app_title": "Plataforma de Inteligencia Conductual", "login_title": "Acceso a la Plataforma",
        "username": "Usuario", "password": "Contraseña", "login_button": "Iniciar Sesión",
        "logout_button": "Cerrar Sesión", "wrong_credentials": "Usuario o contraseña incorrectos.",
        "select_language": "Seleccionar Idioma", "language_en": "Inglés (English)", "language_es": "Español",
        "form_title": "Formulario de Evaluación de Sujeto", "user_id": "ID de Sujeto", "age": "Edad",
        "income": "Ingresos Anuales (Opcional)", 
        "education_level_new": "Nivel de Estudios",
        "substance_use": "Consumo de Sustancias", "country_origin": "País de Origen", "city_origin": "Ciudad de Origen",
        "criminal_record": "Antecedentes Penales", "personality_traits": "Rasgos de Personalidad",
        "previous_diagnoses": "Diagnósticos Previos", "reason_interest": "Motivo de Interés/Caso",
        "family_terrorism_history": "Antecedentes Familiares Terrorismo/Extremismo", 
        "psychological_profile_notes": "Perfil Psicológico (Notas)", # Cambiado ligeramente
        "clinical_history_summary": "Historial Clínico (Resumen)", # Cambiado ligeramente
        # --- Nuevos Títulos de Sección para PDF ---
        "section_reason_interest": "Motivo de Interés / Contexto del Caso",
        "section_family_history": "Antecedentes Familiares Relevantes",
        "section_psychological_profile": "Notas sobre el Perfil Psicológico",
        "section_clinical_history": "Resumen del Historial Clínico",
        "section_detailed_recommendations": "Recomendaciones Detalladas (Intervención)",
        # --- Fin Nuevos Títulos ---
        "studies_none": "Ninguno", "studies_primary": "Primaria", "studies_secondary": "Secundaria",
        "studies_vocational": "FP", "studies_bachelor": "Grado", "studies_master": "Máster", 
        "studies_phd": "Doctorado", "studies_other": "Otro",
        "substance_none": "Ninguno", "substance_alcohol": "Alcohol", "substance_cannabis": "Cannabis", "substance_cocaine": "Cocaína",
        "substance_amphetamines": "Anfetaminas", "substance_opiates": "Opiáceos", "substance_benzodiazepines": "Benzodiacepinas",
        "substance_hallucinogens": "Alucinógenos", "substance_tobacco": "Tabaco", "substance_new_psychoactive": "NSP", "substance_other": "Otra",
        "crime_none": "Ninguno", "crime_theft": "Robo/Hurto", "crime_assault": "Lesiones",
        "crime_drug_trafficking": "Tráfico Drogas", "crime_fraud": "Fraude", "crime_public_order": "Desórden Público",
        "crime_domestic_violence": "Violencia Domést.", "crime_terrorism_related": "Rel. Terrorismo",
        "crime_cybercrime": "Ciberdelincuencia", "crime_homicide": "Homicidio", "crime_other": "Otro",
        "trait_responsible": "Responsable", "trait_impulsive": "Impulsivo", "trait_introverted": "Introvertido",
        "trait_extroverted": "Extrovertido", "trait_anxious": "Ansioso", "trait_aggressive": "Agresivo",
        "trait_empathetic": "Empático", "trait_narcissistic": "Narcisista", "trait_conscientious": "Concienzudo",
        "trait_open_experience": "Abierto Exper.", "trait_neurotic": "Neurótico", "trait_agreeable": "Amable",
        "trait_psychoticism": "Psicoticismo", "trait_manipulative": "Manipulador", "trait_other": "Otro",
        "diag_none": "Ninguno", "diag_depression": "Depresión", "diag_anxiety": "Ansiedad",
        "diag_bipolar": "Bipolar", "diag_schizophrenia": "Esquizofrenia", "diag_ptsd": "TEPT",
        "diag_personality_disorder": "Trast. Personalidad", "diag_adhd": "TDAH",
        "diag_substance_use_disorder": "Trast. Uso Sust.", "diag_eating_disorder": "Trast. Alimentario", "diag_other": "Otro",
        "yes": "Sí", "no": "No", "submit": "Evaluar y Generar Informes",
        "download_report": "Descargar Informe PDF", "error_processing": "Error procesando datos:", 
        "report_generated": "Informe generado.", "prediction": "Predicción Riesgo", "confidence": "Confianza", 
        "recommendations": "Recomendaciones Generales", # Cambiado a "Generales"
        "data_summary": "Resumen Datos Sujeto", 
        "cover_page_title": "Informe Confidencial Inteligencia Conductual", 
        "subject_id_pdf": "ID Sujeto (Informe)", 
        "report_date": "Fecha Informe", "lime_report_title": "Informe LIME", "shap_report_title": "Informe SHAP", 
        "xai_explanations_title": "Explicaciones IA (Omitido)", # Actualizado para indicar omisión
        "risk_level_low": "Bajo", "risk_level_medium": "Medio", "risk_level_high": "Alto", 
        "page": "Página", "confidential_footer": "CONFIDENCIAL",
        "model_not_trained_warning": "Advertencia: Modelo no entrenado. Usando datos placeholder.", 
        "xai_skipped_warning": "XAI omitido (modelo/datos no disponibles).", 
        "error_prediction": "Error predicción:", "error_xai": "Error XAI:", "error_pdf": "Error PDF:", 
        "input_user_id_warning": "Ingrese ID Sujeto.", 
    },
    "en": { # Traducciones al inglés actualizadas
        "app_title": "Behavioral Intelligence Platform", "login_title": "Platform Access",
        "username": "Username", "password": "Password", "login_button": "Login",
        "logout_button": "Logout", "wrong_credentials": "Incorrect username or password.",
        "select_language": "Select Language", "language_en": "English", "language_es": "Spanish (Español)",
        "form_title": "Subject Evaluation Form", "user_id": "Subject ID", "age": "Age",
        "income": "Annual Income (Optional)", 
        "education_level_new": "Education Level",
        "substance_use": "Substance Use", "country_origin": "Country of Origin", "city_origin": "City of Origin",
        "criminal_record": "Criminal Record", "personality_traits": "Personality Traits",
        "previous_diagnoses": "Previous Diagnoses", "reason_interest": "Reason for Interest/Case",
        "family_terrorism_history": "Family History Terrorism/Extremism",
        "psychological_profile_notes": "Psychological Profile (Notes)", 
        "clinical_history_summary": "Clinical History (Summary)", 
        "section_reason_interest": "Reason for Interest / Case Context",
        "section_family_history": "Relevant Family History",
        "section_psychological_profile": "Notes on Psychological Profile",
        "section_clinical_history": "Clinical History Summary",
        "section_detailed_recommendations": "Detailed Recommendations (Intervention)",
        "studies_none": "None", "studies_primary": "Primary", "studies_secondary": "Secondary",
        "studies_vocational": "Vocational", "studies_bachelor": "Bachelor's", "studies_master": "Master's",
        "studies_phd": "PhD", "studies_other": "Other",
        "substance_none": "None", "substance_alcohol": "Alcohol", "substance_cannabis": "Cannabis", "substance_cocaine": "Cocaine",
        "substance_amphetamines": "Amphetamines", "substance_opiates": "Opiates", "substance_benzodiazepines": "Benzodiazepines",
        "substance_hallucinogens": "Hallucinogens", "substance_tobacco": "Tobacco", "substance_new_psychoactive": "NPS", "substance_other": "Other",
        "crime_none": "None", "crime_theft": "Theft", "crime_assault": "Assault",
        "crime_drug_trafficking": "Drug Trafficking", "crime_fraud": "Fraud", "crime_public_order": "Public Order",
        "crime_domestic_violence": "Domestic Viol.", "crime_terrorism_related": "Terrorism Rel.",
        "crime_cybercrime": "Cybercrime", "crime_homicide": "Homicide", "crime_other": "Other",
        "trait_responsible": "Responsible", "trait_impulsive": "Impulsive", "trait_introverted": "Introverted",
        "trait_extroverted": "Extroverted", "trait_anxious": "Anxious", "trait_aggressive": "Aggressive",
        "trait_empathetic": "Empathetic", "trait_narcissistic": "Narcissistic", "trait_conscientious": "Conscientious",
        "trait_open_experience": "Open to Exp.", "trait_neurotic": "Neurotic", "trait_agreeable": "Agreeable",
        "trait_psychoticism": "Psychoticism", "trait_manipulative": "Manipulative", "trait_other": "Other",
        "diag_none": "None", "diag_depression": "Depression", "diag_anxiety": "Anxiety",
        "diag_bipolar": "Bipolar", "diag_schizophrenia": "Schizophrenia", "diag_ptsd": "PTSD",
        "diag_personality_disorder": "Personality Dis.", "diag_adhd": "ADHD",
        "diag_substance_use_disorder": "Substance Use Dis.", "diag_eating_disorder": "Eating Dis.", "diag_other": "Other",
        "yes": "Yes", "no": "No", "submit": "Evaluate & Generate Reports",
        "download_report": "Download PDF Report", "error_processing": "Error processing data:",
        "report_generated": "Report generated.", "prediction": "Risk Prediction", "confidence": "Confidence",
        "recommendations": "General Recommendations", # Changed to General
        "data_summary": "Subject Data Summary",
        "cover_page_title": "Confidential Behavioral Intelligence Report", "subject_id_pdf": "Subject ID (Report)",
        "report_date": "Report Date", "lime_report_title": "LIME Report", "shap_report_title": "SHAP Report",
        "xai_explanations_title": "AI Explanations (Omitted)", # Updated
        "risk_level_low": "Low", "risk_level_medium": "Medium", "risk_level_high": "High", 
        "page": "Page", "confidential_footer": "CONFIDENTIAL",
        "model_not_trained_warning": "Warning: Model not trained. Using placeholder data.",
        "xai_skipped_warning": "XAI skipped (model/data unavailable).",
        "error_prediction": "Prediction error:", "error_xai": "XAI error:", "error_pdf": "PDF error:",
        "input_user_id_warning": "Enter Subject ID.",
    }
}

# --- Estado de Sesión ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'lang' not in st.session_state: st.session_state.lang = "es"

def get_translation(key):
    return translations.get(st.session_state.lang, translations.get("es", {})).get(key, key.replace("_", " ").title())

# --- Login y Selección de Idioma ---
if not st.session_state.logged_in:
    language_options_map = {"es": get_translation("language_es"), "en": get_translation("language_en")}
    selected_lang_key = st.radio(get_translation("select_language"), list(language_options_map.keys()),
                                 format_func=lambda x: language_options_map[x], key="lang_sel_main", horizontal=True)
    if selected_lang_key != st.session_state.lang:
        st.session_state.lang = selected_lang_key
        st.rerun() 
    st.title(get_translation("login_title"))
    with st.form("login_form"):
        username_input = st.text_input(get_translation("username"))
        password_input = st.text_input(get_translation("password"), type="password")
        if st.form_submit_button(get_translation("login_button")):
            if username_input in USER_CREDENTIALS and USER_CREDENTIALS[username_input] == password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.rerun() 
            else: st.error(get_translation("wrong_credentials"))
    st.stop()

# --- App Principal ---
st.sidebar.title(get_translation("app_title"))
st.sidebar.subheader(f"{get_translation('username')}: {st.session_state.username}")
if st.sidebar.button(get_translation("logout_button")):
    st.session_state.logged_in = False; st.session_state.username = ""
    st.rerun() 

# --- Modelo y Features (Actualizado) ---
NEW_FEATURE_NAMES = [ 
    'age', 'income', 'education_level_numeric', 'substance_use_numeric',
    'criminal_record_numeric', 'personality_traits_numeric', 'previous_diagnoses_numeric'
]
CLASS_NAMES = [get_translation("risk_level_low"), get_translation("risk_level_high")]

@st.cache_data
def load_example_data_for_new_model(): 
    num_samples = 40 
    data = {
        'age': np.random.randint(18, 70, num_samples),
        'income': np.random.randint(15000, 120000, num_samples),
        'education_level_numeric': np.random.randint(0, 7, num_samples), 
        'substance_use_numeric': np.random.randint(0, 10, num_samples), 
        'criminal_record_numeric': np.random.randint(0, 10, num_samples),
        'personality_traits_numeric': np.random.randint(0, 14, num_samples),
        'previous_diagnoses_numeric': np.random.randint(0, 10, num_samples),
        'risk_target': np.random.randint(0, 2, num_samples) 
    }
    return pd.DataFrame(data)

@st.cache_resource 
def train_new_model(df_train):
    if df_train.empty or len(df_train) < 20: 
        return None, pd.DataFrame(columns=NEW_FEATURE_NAMES) 
    
    features_present = [f for f in NEW_FEATURE_NAMES if f in df_train.columns]
    if len(features_present) < len(NEW_FEATURE_NAMES):
        st.error(f"Faltan columnas para entrenar el modelo. Esperadas: {NEW_FEATURE_NAMES}, Encontradas: {features_present}")
        return None, pd.DataFrame(columns=NEW_FEATURE_NAMES)

    X = df_train[features_present] 
    y = df_train['risk_target']
    
    if len(np.unique(y)) < 2 : 
         st.warning("Target con una sola clase. El modelo no puede entrenar.")
         return None, X 
         
    model = RandomForestClassifier(random_state=42, class_weight='balanced', n_estimators=50, max_depth=10)
    try:
        model.fit(X, y)
        model.feature_names_in_ = features_present 
        return model, X
    except Exception as e:
        st.error(f"Error al entrenar modelo: {e}")
        return None, X

df_training_data_new = load_example_data_for_new_model()
trained_model_new, X_test_df_global_new = train_new_model(df_training_data_new.copy()) 
if trained_model_new is None and st.session_state.logged_in:
    st.warning(get_translation("model_not_trained_warning"))

# --- Clase PDF Profesional con Helvetica (Simplificada) ---
class ProfessionalPDF(FPDF):
    PDF_FONT_FAMILY = 'Helvetica' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font(self.PDF_FONT_FAMILY, "", 12) 
        self.alias_nb_pages()

    def header(self):
        if self.page_no() == 1: return 
        self.set_font(self.PDF_FONT_FAMILY, 'B', 10)
        self.cell(0, 10, get_translation("app_title"), 0, 0, 'C') 
        self.ln(10)
        self.set_font(self.PDF_FONT_FAMILY, '', 8)
        self.cell(0, 10, f'{get_translation("report_date")}: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'L')
        self.cell(0, 10, f'{get_translation("page")} {self.page_no()}/{{nb}}', 0, 0, 'R')
        self.ln(10)
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def footer(self):
        if self.page_no() == 1: return 
        self.set_y(-15)
        self.set_font(self.PDF_FONT_FAMILY, 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, get_translation("confidential_footer"), 0, 0, 'C')
        self.set_text_color(0)

    def chapter_title(self, title_key):
        self.set_font(self.PDF_FONT_FAMILY, 'B', 14)
        self.set_fill_color(220, 220, 220) 
        self.cell(0, 10, get_translation(title_key), 0, 1, 'L', True)
        self.ln(5)

    def chapter_body(self, body_text):
        if body_text and str(body_text).strip() != "N/A":
            self.set_font(self.PDF_FONT_FAMILY, '', 11)
            self.multi_cell(0, 7, str(body_text)) 
            self.ln(5)
        # else: # Opcional: indicar si no hay texto
        #     self.set_font(self.PDF_FONT_FAMILY, 'I', 10)
        #     self.multi_cell(0, 7, "(No especificado)")
        #     self.ln(5)


    def cover_page(self, report_data):
        self.add_page()
        self.set_font(self.PDF_FONT_FAMILY, 'B', 22) 
        self.set_y(70)
        self.multi_cell(0, 12, get_translation("cover_page_title"), 0, 'C')
        self.ln(20)
        self.set_font(self.PDF_FONT_FAMILY, '', 14)
        self.cell(0, 10, f'{get_translation("subject_id_pdf")}: {report_data.get("user_id", "N/A")}', 0, 1, 'C')
        self.cell(0, 10, f'{get_translation("report_date")}: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
        self.ln(10)
        self.set_y(self.h - 40)
        self.set_font(self.PDF_FONT_FAMILY, 'I', 10)
        self.cell(0, 10, get_translation("confidential_footer").upper() + " - SOLO PARA USO AUTORIZADO", 0, 0, 'C')
    
    def create_data_summary_section(self, report_data): 
        self.chapter_title("data_summary")
        fields_to_display_keys = [
            "user_id", "prediction", "confidence", "age", "education_level_new", "substance_use",
            "country_origin", "city_origin", "criminal_record", "personality_traits",
            "previous_diagnoses" # Quitamos los campos largos de aquí, irán en secciones propias
            # "reason_interest", "family_terrorism_history", 
            # "psychological_profile_notes", "clinical_history_summary", "income" 
        ]
        # Añadir income al final si quieres mantenerlo en el resumen
        if report_data.get("income"):
             fields_to_display_keys.append("income")

        key_map = { 
            "user_id": "user_id", "prediction": "prediction_label", "confidence": "confidence_str",
            "education_level_new": "education_level_str_new",
            "substance_use": "substance_use_str", "criminal_record": "criminal_record_str",
            "personality_traits": "personality_traits_str", "previous_diagnoses": "previous_diagnoses_str"
            # Asegúrate que 'income' esté en report_data si lo incluyes arriba
        }
        for i, label_key in enumerate(fields_to_display_keys):
            data_key_actual = key_map.get(label_key, label_key)
            field_label = get_translation(label_key)
            field_value = str(report_data.get(data_key_actual, "N/A"))
            fill = i % 2 == 0
            page_height_available = self.h - self.b_margin
            if self.get_y() > page_height_available - 20: self.add_page()
            current_y_pos = self.get_y()
            self.set_font(self.PDF_FONT_FAMILY, 'B', 10)
            self.multi_cell(70, 7, field_label, border=0, align='L', fill=fill, new_x="RIGHT", new_y="TOP") 
            # Mover X a la posición correcta para el valor, manteniendo la Y original de la fila
            self.set_xy(self.l_margin + 70, current_y_pos) 
            self.set_font(self.PDF_FONT_FAMILY, '', 10)
            self.multi_cell(0, 7, field_value, border=0, align='L', fill=fill, new_x="LMARGIN", new_y="NEXT")
        self.ln(5) 

    def recommendations_section(self, recommendations_list): # Recomendaciones GENERALES basadas en predicción
        self.chapter_title("recommendations") # El título ahora dice "Recomendaciones Generales"
        current_font = self.PDF_FONT_FAMILY
        if recommendations_list and isinstance(recommendations_list, list):
            available_width = self.w - self.l_margin - self.r_margin 
            for i, rec in enumerate(recommendations_list):
                self.set_x(self.l_margin) 
                self.set_font(current_font, 'B', 10)
                self.multi_cell(available_width, 7, f"{i+1}. {rec.get('title', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
                self.set_x(self.l_margin) 
                self.set_font(current_font, '', 10)
                self.multi_cell(available_width, 7, rec.get('description', 'N/A'), new_x="LMARGIN", new_y="NEXT") 
                self.ln(3) 
        else:
            self.chapter_body("No recommendations available.")
        self.ln(5)

    # --- NUEVOS MÉTODOS PARA SECCIONES CUALITATIVAS ---
    def reason_interest_section(self, report_data):
        text = report_data.get("reason_interest", "")
        if text and text != "N/A":
            self.chapter_title("section_reason_interest")
            self.chapter_body(text)

    def family_terrorism_history_section(self, report_data):
        text = report_data.get("family_terrorism_history", "")
        if text and text != "N/A":
            self.chapter_title("section_family_history")
            self.chapter_body(text)

    def psychological_profile_notes_section(self, report_data):
        text = report_data.get("psychological_profile_notes", "")
        if text and text != "N/A":
            self.chapter_title("section_psychological_profile")
            self.chapter_body(text)

    def clinical_history_summary_section(self, report_data):
        text = report_data.get("clinical_history_summary", "")
        if text and text != "N/A":
            self.chapter_title("section_clinical_history")
            self.chapter_body(text)
            
    def detailed_recommendations_section(self, detailed_recs_list):
        self.chapter_title("section_detailed_recommendations")
        current_font = self.PDF_FONT_FAMILY
        if detailed_recs_list and isinstance(detailed_recs_list, list):
            available_width = self.w - self.l_margin - self.r_margin
            for i, rec in enumerate(detailed_recs_list):
                 self.set_x(self.l_margin)
                 self.set_font(current_font, 'B', 11) # Un poco más grande para el tipo/nombre
                 rec_title = f"{i+1}. {rec.get('type', 'Recomendación')}: {rec.get('name', 'N/A')}"
                 self.multi_cell(available_width, 7, rec_title, new_x="LMARGIN", new_y="NEXT")

                 self.set_x(self.l_margin)
                 self.set_font(current_font, '', 10) # Fuente normal para la explicación
                 self.multi_cell(available_width, 6, rec.get('explanation', 'N/A'), new_x="LMARGIN", new_y="NEXT")
                 self.ln(4) # Espacio entre recomendaciones detalladas
        else:
             self.chapter_body("No detailed recommendations available based on provided data.") # Mensaje en inglés si no hay traducción
        self.ln(5)


    # --- MÉTODO XAI VACÍO ---
    def xai_explanations_section(self, report_data, lime_expl, shap_vals, x_instance_df):
        """Sección de explicaciones XAI omitida."""
        pass 

    # --- MÉTODO generate_full_report ACTUALIZADO ---
    def generate_full_report(self, report_data, recommendations, detailed_recommendations, lime_expl, shap_vals, x_instance_df):
        self.cover_page(report_data)
        self.create_data_summary_section(report_data)
        # Añadir secciones cualitativas
        self.reason_interest_section(report_data)
        self.family_terrorism_history_section(report_data)
        self.psychological_profile_notes_section(report_data)
        self.clinical_history_summary_section(report_data)
        # Añadir recomendaciones (ambos tipos)
        self.recommendations_section(recommendations) # Generales basadas en riesgo
        self.detailed_recommendations_section(detailed_recommendations) # Específicas
        # --- LLAMADA A SECCIÓN XAI SIGUE COMENTADA ---
        # if lime_expl or (shap_vals is not None): 
        #     self.xai_explanations_section(report_data, lime_expl, shap_vals, x_instance_df)
# --- Fin de la Clase PDF ---


# --- Lógica App Streamlit ---

# --- Base de Conocimiento para Recomendaciones Detalladas (EJEMPLO) ---
THERAPY_RECOMMENDATIONS = {
    "diag_depression": [
        {"type": "Terapia", "name": "Terapia Cognitivo-Conductual (TCC)", 
         "explanation": "La TCC ayuda a identificar y modificar patrones de pensamiento y comportamiento negativos asociados a la depresión. Se centra en el presente y en la resolución de problemas. Sesiones semanales suelen ser efectivas, enfocándose en la reestructuración cognitiva y la activación conductual."},
        {"type": "Medicación", "name": "ISRS (Inhibidores Selectivos de la Recaptación de Serotonina)", 
         "explanation": "Fármacos como Fluoxetina, Sertralina o Escitalopram son comúnmente prescritos. Aumentan los niveles de serotonina en el cerebro. Requieren evaluación médica para dosis y seguimiento de efectos secundarios. Su efecto completo puede tardar varias semanas."}
    ],
    "diag_anxiety": [
        {"type": "Terapia", "name": "Terapia Cognitivo-Conductual (TCC)", 
         "explanation": "Eficaz para diversos trastornos de ansiedad (TAG, pánico, fobias). Incluye técnicas de exposición gradual, reestructuración cognitiva para manejar preocupaciones y miedos irracionales, y entrenamiento en relajación."},
        {"type": "Terapia", "name": "Terapia de Aceptación y Compromiso (ACT)",
         "explanation": "Enfocada en aceptar pensamientos y sensaciones difíciles sin luchar contra ellos, y comprometerse con acciones alineadas a los valores personales, incluso en presencia de ansiedad."},
         {"type": "Medicación", "name": "ISRS / IRSN / Benzodiacepinas", 
         "explanation": "Los ISRS o IRSN suelen ser la primera línea farmacológica a largo plazo. Las Benzodiacepinas (ej. Diazepam, Lorazepam) pueden usarse puntualmente para alivio rápido pero con riesgo de dependencia. Requiere prescripción y supervisión médica estricta."}
    ],
     "diag_ptsd": [
        {"type": "Terapia", "name": "EMDR (Desensibilización y Reprocesamiento por Movimientos Oculares)", 
         "explanation": "Terapia especializada para procesar recuerdos traumáticos. Utiliza estimulación bilateral (movimientos oculares, sonidos o toques) para ayudar al cerebro a integrar la experiencia traumática de forma adaptativa."},
        {"type": "Terapia", "name": "Terapia de Exposición Prolongada (TEP)",
         "explanation": "Consiste en enfrentar gradualmente los recuerdos y situaciones temidas relacionadas con el trauma en un entorno seguro, ayudando a reducir la evitación y la intensidad emocional asociada."},
         {"type": "Medicación", "name": "ISRS (Sertralina, Paroxetina)", 
         "explanation": "Aprobados específicamente para TEPT, pueden ayudar a manejar síntomas de ansiedad, depresión e intrusión. La Prazosina se usa a veces para pesadillas. Requiere evaluación médica."}
    ],
    "diag_substance_use_disorder": [
        {"type": "Terapia", "name": "Entrevista Motivacional", 
         "explanation": "Enfoque centrado en el cliente para explorar y resolver la ambivalencia hacia el cambio. Ayuda a aumentar la motivación interna para reducir o detener el consumo."},
        {"type": "Terapia", "name": "Terapia Grupal / Grupos de Apoyo (ej. AA/NA)",
         "explanation": "Proporciona apoyo entre pares, reduce el aislamiento y ofrece estrategias compartidas para mantener la sobriedad. La asistencia regular es clave."},
        {"type": "Medicación", "name": "Tratamiento Asistido por Medicación (TAM/MAT)", 
         "explanation": "Dependiendo de la sustancia (ej. Naltrexona para alcohol/opiáceos, Buprenorfina/Metadona para opiáceos, Acamprosato para alcohol). Reduce el 'craving' y los síntomas de abstinencia. Requiere un programa médico especializado."}
    ],
    # Añadir más mapeos para otros diagnósticos si es necesario
}

def predict_risk_level(df_input, model, feature_list): # CORREGIDO
    if model is None: return CLASS_NAMES[0], 0.10
    if not isinstance(df_input, pd.DataFrame): return CLASS_NAMES[0], 0.05
    if df_input.shape[0] == 0: return CLASS_NAMES[0], 0.05
    try:
        input_df_ordered = df_input[feature_list] 
        print(f"DEBUG Predict: Shape of data passed to model.predict_proba: {input_df_ordered.shape}") 
        if input_df_ordered.shape[1] != len(feature_list):
             st.error(f"Error: Discrepancia features. Modelo: {len(feature_list)}, Datos: {input_df_ordered.shape[1]}.")
             return CLASS_NAMES[0], 0.05
        pred_proba = model.predict_proba(input_df_ordered) 
        pred_proba_instance = pred_proba[0] 
        pred_idx = np.argmax(pred_proba_instance)
        confidence = pred_proba_instance[pred_idx]
        pred_label = CLASS_NAMES[pred_idx]
        print(f"DEBUG Predict: Prediction Label: {pred_label}, Confidence: {confidence:.3f}")
        return pred_label, confidence
    except Exception as e:
        st.error(f"{get_translation('error_prediction')} {e}")
        print(f"Predict Error Details: {traceback.format_exc()}") 
        return CLASS_NAMES[0], 0.05

def generate_general_recommendations(pred_label, conf): # Renombrada
    recs = []
    if pred_label == CLASS_NAMES[1]: # Alto Riesgo
        recs.append({"title": get_translation("recommendations") + " - Prioritaria", "description": "Evaluación exhaustiva y apoyo intensivo."})
        if conf > 0.75: recs.append({"title": "Alerta Elevada", "description": "Protocolos de seguimiento cercano."})
    elif pred_label == get_translation("risk_level_medium"): # Si existiera riesgo medio
         recs.append({"title": "Monitorización Activa", "description": "Seguimiento regular y apoyo preventivo."})
    else: # Bajo Riesgo
        recs.append({"title": "Mantenimiento Preventivo", "description": "Continuar buenas prácticas."})
    return recs

def generate_detailed_recommendations(report_data):
    """Genera recomendaciones detalladas basadas en diagnóstico y keywords (simple)."""
    recommendations = []
    diagnosis_key = report_data.get("previous_diagnoses_key", "diag_none") # Necesitamos la CLAVE del diagnóstico
    
    # 1. Recomendaciones basadas en diagnóstico principal
    if diagnosis_key in THERAPY_RECOMMENDATIONS:
        recommendations.extend(THERAPY_RECOMMENDATIONS[diagnosis_key])

    # 2. (Opcional) Búsqueda MUY simple de keywords en notas psicológicas
    # profile_notes = report_data.get("psychological_profile_notes", "").lower()
    # if "agresividad" in profile_notes or "impulsividad" in profile_notes:
    #     if not any(rec['name'] == "Terapia Dialéctico-Conductual (TDC) - Habilidades" for rec in recommendations):
    #          recommendations.append({
    #              "type": "Terapia", "name": "Terapia Dialéctico-Conductual (TDC) - Habilidades",
    #              "explanation": "La TDC ofrece entrenamiento en habilidades de regulación emocional, tolerancia al malestar, mindfulness y efectividad interpersonal, útiles para manejar impulsividad y reactividad emocional intensa."
    #          })
          
    # Asegurarse de no tener duplicados (por si una terapia aplica a varias condiciones)
    unique_recs = []
    seen_names = set()
    for rec in recommendations:
        if rec['name'] not in seen_names:
            unique_recs.append(rec)
            seen_names.add(rec['name'])
            
    return unique_recs


st.title(get_translation("app_title"))

def get_options_dict(prefix, keys):
    return {f"{prefix}_{key}": get_translation(f"{prefix}_{key}") for key in keys}

# --- Definiciones de opciones y mapeos numéricos (como antes) ---
education_keys = ["none", "primary", "secondary", "vocational", "bachelor", "master", "phd", "other"]
substance_keys = ["none", "alcohol", "cannabis", "cocaine", "amphetamines", "opiates", "benzodiazepines", "hallucinogens", "tobacco", "new_psychoactive", "other"]
crime_keys = ["none", "theft", "assault", "drug_trafficking", "fraud", "public_order", "domestic_violence", "terrorism_related", "cybercrime", "homicide", "other"]
trait_keys = ["responsible", "impulsive", "introverted", "extroverted", "anxious", "aggressive", "empathetic", "narcissistic", "conscientious", "open_experience", "neurotic", "agreeable", "psychoticism", "manipulative", "other"]
diag_keys = ["none", "depression", "anxiety", "bipolar", "schizophrenia", "ptsd", "personality_disorder", "adhd", "substance_use_disorder", "eating_disorder", "other"]

education_options_new = get_options_dict("studies", education_keys)
substance_options = get_options_dict("substance", substance_keys)
criminal_record_options = get_options_dict("crime", crime_keys)
personality_trait_options = get_options_dict("trait", trait_keys)
diagnosis_options = get_options_dict("diag", diag_keys)

def create_numeric_map(option_keys_list):
    return {key: i for i, key in enumerate(sorted(option_keys_list))} 

education_numeric_map = create_numeric_map(education_options_new.keys())
substance_numeric_map = create_numeric_map(substance_options.keys())
criminal_record_numeric_map = create_numeric_map(criminal_record_options.keys())
personality_trait_numeric_map = create_numeric_map(personality_trait_options.keys())
diagnosis_numeric_map = create_numeric_map(diagnosis_options.keys())
# --- Fin Definiciones ---


with st.form(key="evaluation_form_final"):
    st.header(get_translation("form_title"))
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### {get_translation('Información Básica y Contexto')}")
        age_form = st.number_input(get_translation("age"), 18, 100, 30)
        income_form = st.number_input(get_translation("income"), 0, 250000, 30000, 1000, help="Este campo es opcional.")
        education_key_selected = st.selectbox(get_translation("education_level_new"), list(education_options_new.keys()), format_func=lambda x: education_options_new[x])
        substance_key_selected = st.selectbox(get_translation("substance_use"), list(substance_options.keys()), format_func=lambda x: substance_options[x])
        country_origin_form = st.text_input(get_translation("country_origin"))
        city_origin_form = st.text_input(get_translation("city_origin"))
    with col2:
        st.markdown(f"#### {get_translation('Historial y Diagnósticos')}")
        crime_key_selected = st.selectbox(get_translation("criminal_record"), list(criminal_record_options.keys()), format_func=lambda x: criminal_record_options[x])
        trait_key_selected = st.selectbox(get_translation("personality_traits"), list(personality_trait_options.keys()), format_func=lambda x: personality_trait_options[x])
        # Guardamos la CLAVE seleccionada del diagnóstico para usarla en las recomendaciones
        diag_key_selected = st.selectbox(get_translation("previous_diagnoses"), list(diagnosis_options.keys()), format_func=lambda x: diagnosis_options[x])
    
    st.markdown(f"#### {get_translation('Información Cualitativa Detallada')}")
    reason_interest_form = st.text_area(get_translation("reason_interest"), height=75, placeholder="Describa el motivo del análisis...")
    family_terrorism_history_form = st.text_area(get_translation("family_terrorism_history"), height=75, placeholder="Detalles sobre antecedentes familiares...")
    psychological_profile_notes_form = st.text_area(get_translation("psychological_profile_notes"), height=100, placeholder="Observaciones, evaluaciones previas...")
    clinical_history_summary_form = st.text_area(get_translation("clinical_history_summary"), height=100, placeholder="Resumen del historial clínico...")
    
    submit_button_final = st.form_submit_button(label=get_translation("submit"))

if submit_button_final:
    subject_id_generated = f"SID_{st.session_state.username.upper()}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    form_data_for_model_dict = {
        "age": age_form, "income": income_form,
        "education_level_numeric": education_numeric_map.get(education_key_selected, 0),
        "substance_use_numeric": substance_numeric_map.get(substance_key_selected, 0),
        "criminal_record_numeric": criminal_record_numeric_map.get(crime_key_selected, 0),
        "personality_traits_numeric": personality_trait_numeric_map.get(trait_key_selected, 0),
        "previous_diagnoses_numeric": diagnosis_numeric_map.get(diag_key_selected, 0),
    }
    report_data_payload = {
        "user_id": subject_id_generated, "age": age_form, "income": income_form,
        "education_level_str_new": education_options_new.get(education_key_selected, "N/A"),
        "substance_use_str": substance_options.get(substance_key_selected, "N/A"),
        "country_origin": country_origin_form or "N/A", "city_origin": city_origin_form or "N/A",
        "criminal_record_str": criminal_record_options.get(crime_key_selected, "N/A"),
        "personality_traits_str": personality_trait_options.get(trait_key_selected, "N/A"),
        "previous_diagnoses_str": diagnosis_options.get(diag_key_selected, "N/A"), # Texto del diagnóstico
        "previous_diagnoses_key": diag_key_selected, # CLAVE del diagnóstico para lógica interna
        "reason_interest": reason_interest_form or "N/A",
        "family_terrorism_history": family_terrorism_history_form or "N/A",
        "psychological_profile_notes": psychological_profile_notes_form or "N/A",
        "clinical_history_summary": clinical_history_summary_form or "N/A",
    }
    
    # --- Predicción ---
    try:
        df_for_prediction = pd.DataFrame([form_data_for_model_dict], columns=NEW_FEATURE_NAMES)
        prediction, confidence = predict_risk_level(df_for_prediction, trained_model_new, NEW_FEATURE_NAMES) 
    except KeyError as e:
         st.error(f"Error: Falta la columna '{e}' requerida por el modelo.")
         print(f"DEBUG Predict Keys: Keys in dict: {list(form_data_for_model_dict.keys())}")
         print(f"DEBUG Predict Keys: Expected features: {NEW_FEATURE_NAMES}")
         st.stop() 
    except Exception as e:
         st.error(f"Error inesperado durante preparación datos predicción: {e}")
         st.stop()

    report_data_payload["prediction_label"] = prediction
    report_data_payload["confidence_str"] = f"{confidence*100:.1f}%"
    st.subheader(f"{get_translation('prediction')}: {prediction} ({get_translation('confidence')}: {report_data_payload['confidence_str']})")
    
    # --- Recomendaciones ---
    general_recommendations_list = generate_general_recommendations(prediction, confidence) # Renombrada
    detailed_recommendations_list = generate_detailed_recommendations(report_data_payload) # Nueva función
    
    st.subheader(get_translation("recommendations")) # Título para recomendaciones generales
    for r in general_recommendations_list: st.write(f"**{r['title']}**: {r['description']}")
        
    if detailed_recommendations_list:
        st.subheader(get_translation("section_detailed_recommendations")) # Título para detalladas
        for r_det in detailed_recommendations_list:
            st.markdown(f"**{r_det['type']}: {r_det['name']}**")
            st.write(r_det['explanation'])
    
    # --- Cálculo XAI (se ejecuta pero no se añade al PDF) ---
    lime_expl_obj, shap_vals_pred_class = None, None
    instance_df_for_xai = df_for_prediction.copy() 
    
    if trained_model_new and X_test_df_global_new is not None and not X_test_df_global_new.empty:
        try:
            lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                X_test_df_global_new[NEW_FEATURE_NAMES].values, 
                feature_names=NEW_FEATURE_NAMES,
                class_names=CLASS_NAMES, mode='classification', discretize_continuous=True
            )
            lime_expl_obj = lime_explainer.explain_instance(
                instance_df_for_xai.iloc[0].values, 
                trained_model_new.predict_proba, num_features=len(NEW_FEATURE_NAMES)
            )
            
            if isinstance(trained_model_new, RandomForestClassifier):
                shap_explainer = shap.TreeExplainer(trained_model_new, X_test_df_global_new[NEW_FEATURE_NAMES]) 
                shap_values_all = shap_explainer.shap_values(instance_df_for_xai) 
            else:
                X_test_summary = shap.kmeans(X_test_df_global_new[NEW_FEATURE_NAMES], min(50, len(X_test_df_global_new)))
                shap_explainer = shap.KernelExplainer(trained_model_new.predict_proba, X_test_summary)
                shap_values_all = shap_explainer.shap_values(instance_df_for_xai)
            
            pred_idx = CLASS_NAMES.index(prediction) if prediction in CLASS_NAMES else 0
            if isinstance(shap_values_all, list) and len(shap_values_all) == len(CLASS_NAMES):
                 shap_vals_pred_class = shap_values_all[pred_idx][0]
            elif isinstance(shap_values_all, np.ndarray) and shap_values_all.ndim == 2:
                 shap_vals_pred_class = shap_values_all[0] if pred_idx == 1 else -shap_values_all[0]
            else: shap_vals_pred_class = np.zeros(len(NEW_FEATURE_NAMES))
        except Exception as e: st.error(f"{get_translation('error_xai')} {e}\n{traceback.format_exc()}")
    else: st.info(get_translation("xai_skipped_warning"))
    # --- Fin Cálculo XAI ---

    # --- Generación del PDF (SIN sección XAI activa, CON nuevas secciones cualitativas y recomendaciones detalladas) ---
    try:
        pdf = ProfessionalPDF()
        pdf.generate_full_report( 
            report_data_payload, 
            general_recommendations_list, # Pasar las recomendaciones generales
            detailed_recommendations_list,# Pasar las recomendaciones detalladas
            lime_expl_obj, 
            shap_vals_pred_class, 
            instance_df_for_xai 
        )
        pdf_file_name = f"Informe_{report_data_payload['user_id']}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf_bytes = bytes(pdf.output(dest='S')) # Convertir a bytes
        st.download_button(get_translation("download_report"), pdf_bytes, pdf_file_name, "application/pdf")
        st.success(get_translation("report_generated"))
    except Exception as e: st.error(f"{get_translation('error_pdf')} {e}\n{traceback.format_exc()}")
