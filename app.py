# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from fpdf import FPDF # Usar FPDF2: pip install fpdf2
import shap
import lime
import lime.lime_tabular
import numpy as np
import matplotlib.pyplot as plt # Necesario si se descomentan las gráficas SHAP/LIME
import base64
from datetime import datetime
import os # Para verificar existencia de archivos de fuentes
import traceback # Para mostrar tracebacks completos

# --- Configuración de la Página de Streamlit ---
st.set_page_config(layout="wide", page_title="Behavioral Intelligence Platform")

# --- Traducciones ---
translations = {
    "es": {
        "title": "Plataforma de Inteligencia Conductual",
        "form_title": "Formulario de Evaluación",
        "user_id": "ID de Sujeto",
        "age": "Edad",
        "income": "Ingresos Anuales (€)",
        "education_level": "Nivel Educativo",
        "high_school": "Secundaria",
        "college": "Universidad",
        "graduate": "Postgrado",
        "previous_incidents": "Incidentes Previos",
        "therapy_date": "Fecha Última Terapia",
        "alarm_year": "Año de Alarma",
        "interest_profile": "Perfil de Intereses",
        "family_extremism": "Extremismo Familiar",
        "additional_comments": "Comentarios Adicionales",
        "yes": "Sí",
        "no": "No",
        "submit": "Evaluar y Generar Informes",
        "download_report": "Descargar Informe PDF",
        "error_processing": "Error al procesar los datos:",
        "report_generated": "Informe generado.",
        "prediction": "Predicción de Riesgo",
        "confidence": "Confianza",
        "recommendations": "Recomendaciones",
        "data_summary": "Resumen de Datos del Sujeto",
        "cover_page_title": "Informe Confidencial de Inteligencia Conductual",
        "subject_id": "ID del Sujeto", 
        "report_date": "Fecha del Informe",
        "lime_report_title": "Informe de Explicaciones LIME",
        "shap_report_title": "Informe de Valores SHAP",
        "xai_explanations_title": "Explicaciones de IA (LIME & SHAP)",
        "risk_level_low": "Bajo",
        "risk_level_medium": "Medio", 
        "risk_level_high": "Alto",
        "page": "Página",
        "confidential_footer": "CONFIDENCIAL",
        "model_not_trained_warning": "Advertencia: El modelo predictivo no está entrenado o no hay suficientes datos. Usando lógica de placeholder.",
        "xai_skipped_warning": "Explicaciones XAI omitidas (modelo o datos de prueba no disponibles).",
        "error_prediction": "Error durante la predicción:",
        "error_xai": "Error durante el procesamiento XAI:",
        "error_pdf": "Error durante la generación del PDF:",
        "input_user_id_warning": "Por favor, ingrese un ID de Sujeto.",
    }
}
current_lang = "es"

def get_translation(key, lang=current_lang):
    return translations.get(lang, {}).get(key, key.replace("_", " ").title())

# --- Modelo y Datos (Placeholder/Ejemplo) ---
FEATURE_NAMES = ['age', 'income', 'education_level', 'previous_incidents']
CLASS_NAMES = [get_translation("risk_level_low"), get_translation("risk_level_high")] 

@st.cache_data
def load_example_data():
    data = {
        'age': [25, 30, 35, 22, 45, 50, 29, 33, 40, 37] * 2,
        'income': [50000, 60000, 80000, 45000, 90000, 120000, 55000, 70000, 85000, 75000] * 2,
        'education_level': [1, 2, 3, 1, 2, 3, 1, 2, 3, 2] * 2,
        'previous_incidents': [0, 1, 0, 0, 2, 1, 0, 1, 0, 1] * 2,
        'risk_score_continuous': [0.1, 0.3, 0.2, 0.1, 0.6, 0.4, 0.15, 0.35, 0.25, 0.33] * 2
    }
    df = pd.DataFrame(data)
    df['risk_target'] = (df['risk_score_continuous'] > 0.3).astype(int)
    return df

@st.cache_resource
def train_model(df_train):
    if df_train.empty or len(df_train) < 10: 
        # st.warning(get_translation("model_not_trained_warning")) # Ya no es necesario mostrarlo aquí si se maneja en la UI
        return None, pd.DataFrame(columns=FEATURE_NAMES) 

    X = df_train[FEATURE_NAMES]
    y = df_train['risk_target']
    
    model = RandomForestClassifier(random_state=42, class_weight='balanced')
    try:
        model.fit(X, y)
        return model, X 
    except ValueError as e: 
        st.error(f"Error al entrenar el modelo: {e}. Usando placeholder.")
        return None, pd.DataFrame(columns=FEATURE_NAMES)

df_training_data = load_example_data()
trained_model, X_test_df_global = train_model(df_training_data.copy())
if trained_model is None: # Muestra advertencia una vez si el modelo no se entrena
    st.warning(get_translation("model_not_trained_warning"))


# --- Clase PDF Profesional con Helvetica ---
class ProfessionalPDF(FPDF):
    PDF_FONT_FAMILY = 'Helvetica' # Usar Helvetica como base

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=15)
        self.setup_fonts() # Llama a setup_fonts que ahora usa Helvetica
        self.alias_nb_pages()

    def setup_fonts(self):
        # FPDF usa 'helvetica', 'times', 'courier' como nombres de fuentes base
        # No necesitamos add_font para estas, solo set_font
        # Para estilos (B, I, BI), FPDF los maneja internamente para fuentes base
        self.set_font(self.PDF_FONT_FAMILY, "", 12)

    def header(self):
        if self.page_no() == 1: return 
        self.set_font(self.PDF_FONT_FAMILY, 'B', 10)
        self.cell(0, 10, get_translation("title"), 0, 0, 'C')
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
        self.set_text_color(0) # Reset text color

    def chapter_title(self, title_key):
        self.set_font(self.PDF_FONT_FAMILY, 'B', 14)
        self.set_fill_color(220, 220, 220) 
        self.cell(0, 10, get_translation(title_key), 0, 1, 'L', True)
        self.ln(5)

    def chapter_body(self, body_text):
        self.set_font(self.PDF_FONT_FAMILY, '', 11)
        self.multi_cell(0, 7, str(body_text)) 
        self.ln(5)

    def cover_page(self, report_data):
        self.add_page()
        self.set_font(self.PDF_FONT_FAMILY, 'B', 22) 
        self.set_y(70)
        self.multi_cell(0, 12, get_translation("cover_page_title"), 0, 'C')
        self.ln(20)
        self.set_font(self.PDF_FONT_FAMILY, '', 14)
        self.cell(0, 10, f'{get_translation("subject_id")}: {report_data.get("user_id", "N/A")}', 0, 1, 'C')
        self.cell(0, 10, f'{get_translation("report_date")}: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
        self.ln(10)
        self.set_y(self.h - 40)
        self.set_font(self.PDF_FONT_FAMILY, 'I', 10)
        self.cell(0, 10, get_translation("confidential_footer").upper() + " - SOLO PARA USO AUTORIZADO", 0, 0, 'C')

    def create_data_summary_section(self, report_data):
        self.chapter_title("data_summary")
        
        fields_to_map = {
            "user_id": "user_id", "prediction": "prediction_label", "confidence": "confidence_str",
            "age": "age", "income": "income", "education_level": "education_level_str",
            "previous_incidents": "previous_incidents", "therapy_date": "therapy_date",
            "alarm_year": "alarm_year", "interest_profile": "interest_profile",
            "family_extremism": "family_extremism_str", "additional_comments": "additional_comments"
        }
        
        for i, (label_key, data_key) in enumerate(fields_to_map.items()):
            field_label = get_translation(label_key)
            field_value = str(report_data.get(data_key, "N/A"))
            fill = i % 2 == 0
            current_y = self.get_y()
            
            self.set_font(self.PDF_FONT_FAMILY, 'B', 10)
            self.multi_cell(60, 7, field_label, border=0, align='L', fill=fill, ln=0)
            
            self.set_xy(self.l_margin + 60, current_y)
            self.set_font(self.PDF_FONT_FAMILY, '', 10)
            self.multi_cell(0, 7, field_value, border=0, align='L', fill=fill, ln=1)
        self.ln(5)

    def recommendations_section(self, recommendations_list):
        self.chapter_title("recommendations")
        if recommendations_list and isinstance(recommendations_list, list):
            for i, rec in enumerate(recommendations_list):
                self.set_font(self.PDF_FONT_FAMILY, 'B', 10)
                self.multi_cell(0, 7, f"{i+1}. {rec.get('title', 'N/A')}")
                self.set_font(self.PDF_FONT_FAMILY, '', 10)
                self.multi_cell(0, 7, rec.get('description', 'N/A'))
                self.ln(3)
        else:
            self.chapter_body("No recommendations available.")
        self.ln(5)

    def xai_explanations_section(self, report_data, lime_expl, shap_vals, x_instance_df):
        self.chapter_title("xai_explanations_title")

        self.set_font(self.PDF_FONT_FAMILY, 'B', 12)
        self.cell(0, 10, get_translation("lime_report_title"), 0, 1, 'L')
        self.set_font(self.PDF_FONT_FAMILY, '', 10)
        if lime_expl:
            try:
                pred_label = report_data.get('prediction_label', CLASS_NAMES[0])
                pred_idx = CLASS_NAMES.index(pred_label) if pred_label in CLASS_NAMES else 0
                explanation_list = lime_expl.as_list(label=pred_idx)
                self.multi_cell(0, 7, f"LIME (Predicted: {pred_label}):")
                for feature_idx_str, weight in explanation_list:
                    try: 
                        feature_name = FEATURE_NAMES[int(feature_idx_str)]
                    except (ValueError, IndexError):
                        feature_name = feature_idx_str 
                    self.multi_cell(0, 7, f"- {feature_name}: {weight:.3f}")
            except Exception as e:
                self.multi_cell(0, 7, f"Error LIME: {e}")
        else:
            self.multi_cell(0, 7, "LIME explanation not available.")
        self.ln(5)

        self.set_font(self.PDF_FONT_FAMILY, 'B', 12)
        self.cell(0, 10, get_translation("shap_report_title"), 0, 1, 'L')
        self.set_font(self.PDF_FONT_FAMILY, '', 10)
        if shap_vals is not None and x_instance_df is not None:
            try:
                self.multi_cell(0, 7, f"SHAP (Predicted: {report_data.get('prediction_label', 'N/A')}):")
                for i, feature_name in enumerate(FEATURE_NAMES):
                    if i < len(shap_vals):
                        self.multi_cell(0, 7, f"- {feature_name}: {shap_vals[i]:.3f}")
            except Exception as e:
                self.multi_cell(0, 7, f"Error SHAP: {e}")
        else:
            self.multi_cell(0, 7, "SHAP values not available.")
        self.ln(5)

    def generate_full_report(self, report_data, recommendations, lime_expl, shap_vals, x_instance_df):
        self.cover_page(report_data)
        self.create_data_summary_section(report_data)
        self.recommendations_section(recommendations)
        if lime_expl or (shap_vals is not None):
            self.xai_explanations_section(report_data, lime_expl, shap_vals, x_instance_df)
# --- Fin de la Clase PDF ---


# --- Lógica de la Aplicación Streamlit ---
def predict_risk_level(form_input_data, model, feature_list):
    if model is None:
        return CLASS_NAMES[0], 0.10 

    try:
        input_df = pd.DataFrame([form_input_data])[feature_list]
        pred_proba = model.predict_proba(input_df)[0]
        pred_idx = np.argmax(pred_proba)
        confidence = pred_proba[pred_idx]
        pred_label = CLASS_NAMES[pred_idx]
        return pred_label, confidence
    except Exception as e:
        st.error(f"{get_translation('error_prediction')} {e}")
        return CLASS_NAMES[0], 0.05


def generate_behavioral_recommendations(pred_label, conf):
    recs = []
    if pred_label == CLASS_NAMES[1]: 
        recs.append({"title": "Intervención Prioritaria", "description": "Evaluación exhaustiva y apoyo intensivo."})
        if conf > 0.75:
            recs.append({"title": "Alerta Elevada", "description": "Protocolos de seguimiento cercano."})
    elif pred_label == get_translation("risk_level_medium"): 
         recs.append({"title": "Monitorización Activa", "description": "Seguimiento regular y apoyo preventivo."})
    else: 
        recs.append({"title": "Mantenimiento Preventivo", "description": "Continuar buenas prácticas y bienestar general."})
    return recs


# --- Interfaz de Usuario Streamlit ---
st.title(get_translation("title"))

education_map = {1: get_translation("high_school"), 2: get_translation("college"), 3: get_translation("graduate")}
yes_no_map = {0: get_translation("no"), 1: get_translation("yes")}

with st.form(key="evaluation_form"):
    st.header(get_translation("form_title"))
    
    c1, c2 = st.columns(2)
    with c1:
        user_id = st.text_input(get_translation("user_id"), f"SUBJ_{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}")
        age = st.number_input(get_translation("age"), 18, 100, 30)
        income = st.number_input(get_translation("income"), 0, 1000000, 50000, 1000)
        education_level_val = st.selectbox(get_translation("education_level"), list(education_map.keys()), format_func=lambda x: education_map[x])
        previous_incidents_val = st.number_input(get_translation("previous_incidents"), 0, 50, 0)

    with c2:
        therapy_date_in = st.date_input(get_translation("therapy_date"), value=None)
        alarm_year_in = st.number_input(get_translation("alarm_year"), 1950, datetime.now().year + 1, datetime.now().year)
        interest_profile_in = st.text_area(get_translation("interest_profile"), height=75, placeholder="Ej: armas, ideología X, grupos Y...")
        family_extremism_val = st.radio(get_translation("family_extremism"), list(yes_no_map.keys()), format_func=lambda x: yes_no_map[x])
        additional_comments_in = st.text_area(get_translation("additional_comments"), height=75, placeholder="Observaciones relevantes...")

    submit_button = st.form_submit_button(label=get_translation("submit"))

if submit_button:
    if not user_id.strip():
        st.warning(get_translation("input_user_id_warning"))
    else:
        form_data_for_model = {
            "age": age, "income": income,
            "education_level": education_level_val,
            "previous_incidents": previous_incidents_val,
        }

        report_data_payload = {
            **form_data_for_model, 
            "user_id": user_id,
            "education_level_str": education_map.get(education_level_val, "N/A"),
            "therapy_date": therapy_date_in.strftime("%Y-%m-%d") if therapy_date_in else "N/A",
            "alarm_year": str(alarm_year_in),
            "interest_profile": interest_profile_in or "N/A",
            "family_extremism_str": yes_no_map.get(family_extremism_val, "N/A"),
            "additional_comments": additional_comments_in or "N/A",
        }

        prediction, confidence = predict_risk_level(form_data_for_model, trained_model, FEATURE_NAMES)
        report_data_payload["prediction_label"] = prediction
        report_data_payload["confidence_val"] = confidence 
        report_data_payload["confidence_str"] = f"{confidence*100:.1f}%"

        st.subheader(f"{get_translation('prediction')}: {prediction} ({get_translation('confidence')}: {report_data_payload['confidence_str']})")

        recommendations_list = generate_behavioral_recommendations(prediction, confidence)
        st.subheader(get_translation("recommendations"))
        for r in recommendations_list: st.write(f"**{r['title']}**: {r['description']}")

        lime_explanation_obj = None
        shap_values_for_pred_class = None
        instance_df_for_xai = pd.DataFrame([form_data_for_model])[FEATURE_NAMES]

        if trained_model and X_test_df_global is not None and not X_test_df_global.empty:
            try:
                lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                    training_data=X_test_df_global.values, feature_names=FEATURE_NAMES,
                    class_names=CLASS_NAMES, mode='classification', discretize_continuous=True
                )
                lime_explanation_obj = lime_explainer.explain_instance(
                    data_row=instance_df_for_xai.iloc[0].values,
                    predict_fn=trained_model.predict_proba, num_features=len(FEATURE_NAMES)
                )
                
                if isinstance(trained_model, RandomForestClassifier): # TreeExplainer es más eficiente para modelos de árbol
                    shap_explainer = shap.TreeExplainer(trained_model, X_test_df_global) 
                    shap_values_all = shap_explainer.shap_values(instance_df_for_xai) # Devuelve lista de arrays (uno por clase)
                else: # Fallback a KernelExplainer (más lento, pero más general)
                    # KernelExplainer necesita un resumen de los datos de fondo
                    X_test_summary = shap.kmeans(X_test_df_global, 50) # K-Means para resumir datos de fondo
                    shap_explainer = shap.KernelExplainer(trained_model.predict_proba, X_test_summary)
                    shap_values_all = shap_explainer.shap_values(instance_df_for_xai) # Devuelve lista de arrays
                    st.info("Usando KernelExplainer para SHAP (puede ser más lento).")

                pred_idx = CLASS_NAMES.index(prediction) if prediction in CLASS_NAMES else 0
                if isinstance(shap_values_all, list) and len(shap_values_all) == len(CLASS_NAMES):
                     shap_values_for_pred_class = shap_values_all[pred_idx][0] 
                elif isinstance(shap_values_all, np.ndarray) and shap_values_all.ndim == 2 : 
                     shap_values_for_pred_class = shap_values_all[0] if pred_idx == 1 else -shap_values_all[0]
                else: 
                     shap_values_for_pred_class = np.zeros(len(FEATURE_NAMES))
            except Exception as e:
                st.error(f"{get_translation('error_xai')} {e}")
                st.error(traceback.format_exc())
        else:
            st.info(get_translation("xai_skipped_warning"))

        try:
            pdf = ProfessionalPDF()
            pdf.generate_full_report(
                report_data_payload, recommendations_list,
                lime_explanation_obj, shap_values_for_pred_class, instance_df_for_xai
            )
            pdf_file_name = f"Informe_{user_id.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            pdf_bytes = pdf.output(dest='S').encode('latin-1')

            st.download_button(
                label=get_translation("download_report"), data=pdf_bytes,
                file_name=pdf_file_name, mime="application/pdf"
            )
            st.success(get_translation("report_generated"))
        except Exception as e:
            st.error(f"{get_translation('error_pdf')} {e}")
            st.error(traceback.format_exc())
