import streamlit as st
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io
import os
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="BIAS - Sistema de Análisis de Inteligencia Conductual",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Diccionarios para traducción
translations = {
    "Español": {
        "app_title": "BIAS - Sistema de Análisis de Inteligencia Conductual",
        # ... (mantener todas las traducciones del archivo paste-2.txt)
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

def generar_pdf_generico(datos):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="INFORME GENÉRICO BIAS", ln=True, align='C')
    pdf.ln(10)
    
    # Sección de Datos Básicos
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, txt="Datos del Sujeto", ln=True)
    pdf.set_font('Arial', '', 12)
    
    info_basica = [
        ("Nombre completo", datos['nombre']),
        ("Número de identificación", datos['id_number']),
        ("Edad", str(datos['edad'])),
        ("Género", datos['genero']),
        ("Nivel educativo", datos['education']),
        ("Año de señales de alarma", str(datos['alarm_date']))
    ]
    
    for campo, valor in info_basica:
        pdf.cell(90, 10, txt=campo + ":", ln=0)
        pdf.cell(100, 10, txt=valor, ln=1)
    
    # Sección de Riesgos
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, txt="Factores de Riesgo", ln=True)
    
    factores = [
        ("Consumo de sustancias", ", ".join(datos['substances'])),
        ("Antecedentes penales", ", ".join(datos['criminal_record'])),
        ("Rasgos de personalidad", ", ".join(datos['personality_traits'])),
        ("Diagnósticos previos", ", ".join(datos['diagnosis_list']))
    ]
    
    for factor, valor in factores:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(95, 10, txt=factor + ":", ln=0)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(95, 10, txt=valor)
    
    # Sección Adicional
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, txt="Información Adicional", ln=True)
    
    adicionales = [
        ("Historial Clínico", datos['clinical_history']),
        ("Perfil Psicológico", datos['psychological_profile']),
        ("Comentarios", datos['additional_comments'])
    ]
    
    for titulo, contenido in adicionales:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 10, txt=titulo + ":", ln=1)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, txt=contenido)
    
    # Gráficos simulados
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Gráficos de Riesgo", ln=True, align='C')
    pdf.image("grafico_placeholder.png", x=30, y=40, w=150)  # Necesitarías tener una imagen
    
    return pdf.output(dest='S').encode('latin-1')

def generar_pdf_direccion(datos):
    pdf = FPDF()
    # ... (similar al anterior pero con sección de puntuación)
    return pdf.output(dest='S').encode('latin-1')

def main():
    # Configuración inicial de sesión
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
        st.session_state.datos_formulario = {}
    
    # Barra lateral de login
    with st.sidebar:
        if not st.session_state.autenticado:
            st.header("Autenticación")
            usuario = st.text_input("Usuario")
            contrasena = st.text_input("Contraseña", type="password")
            
            if st.button("Ingresar"):
                if usuario in ["demo_bias", "JuanCarlos_bias", "Cristina_bias"] and contrasena == "biasdemo2025":
                    st.session_state.autenticado = True
                    st.session_state.usuario = usuario
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        else:
            st.header(f"Bienvenido, {st.session_state.usuario}")
            if st.button("Cerrar sesión"):
                st.session_state.autenticado = False
                st.rerun()
    
    # Contenido principal
    if st.session_state.autenticado:
        with st.form("formulario_principal"):
            st.header("Perfil de Evaluación")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre completo")
                id_number = st.text_input("Número de identificación")
                edad = st.number_input("Edad", min_value=12, max_value=100)
                genero = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
                educacion = st.selectbox("Nivel educativo", ["Primaria", "Secundaria", "Universidad", "Postgrado", "Ninguno"])
                
                # Fecha de señales solo año
                ano_alarma = st.selectbox("Año de señales de alarma", list(range(2000, datetime.now().year + 1)))
            
            with col2:
                sustancias = st.multiselect("Consumo de sustancias", ["Alcohol", "Tabaco", "Drogas recreativas", "Cocaína", "Heroína"])
                antecedentes = st.multiselect("Antecedentes penales", ["Robo", "Violencia de género", "Homicidio", "Terrorismo"] + additional_terrorism_antecedents)
                rasgos = st.multiselect("Rasgos de personalidad", ["Paranoide", "Antisocial", "Impulsivo"] + additional_personality_traits)
                diagnosticos = st.multiselect("Diagnósticos previos", additional_mental_health_traits)
                
                # Terapia condicional
                terapia = st.selectbox("Terapias previas", ["Ninguna", "Psicoterapia", "Farmacológica"])
                fecha_terapia = st.date_input("Fecha inicio terapia", disabled=(terapia == "Ninguna"))
            
            # Sección adicional
            st.subheader("Información Adicional")
            hist_clinico = st.text_area("Historial Clínico")
            perfil_psico = st.text_area("Perfil Psicológico")
            comentarios = st.text_area("Comentarios")
            
            # Foto del sujeto
            foto = st.file_uploader("Subir foto (formato carnet)", type=["jpg", "png"])
            
            if st.form_submit_button("Generar Informe"):
                datos = {
                    'nombre': nombre,
                    'id_number': id_number,
                    'edad': edad,
                    'genero': genero,
                    'education': educacion,
                    'alarm_date': ano_alarma,
                    'substances': sustancias,
                    'criminal_record': antecedentes,
                    'personality_traits': rasgos,
                    'diagnosis_list': diagnosticos,
                    'clinical_history': hist_clinico,
                    'psychological_profile': perfil_psico,
                    'additional_comments': comentarios
                }
                
                # Generar PDF
                pdf_bytes = generar_pdf_generico(datos)
                st.session_state.pdf_generico = pdf_bytes
                
                if st.session_state.usuario in ["JuanCarlos_bias", "Cristina_bias"]:
                    pdf_dir_bytes = generar_pdf_direccion(datos)
                    st.session_state.pdf_direccion = pdf_dir_bytes
        
        # Descargas después del formulario
        if 'pdf_generico' in st.session_state:
            st.download_button(
                label="Descargar Informe Genérico",
                data=st.session_state.pdf_generico,
                file_name="informe_generico.pdf",
                mime="application/pdf"
            )
            
            if 'pdf_direccion' in st.session_state:
                st.download_button(
                    label="Descargar Informe Dirección",
                    data=st.session_state.pdf_direccion,
                    file_name="informe_direccion.pdf",
                    mime="application/pdf"
                )
    else:
        st.info("Por favor inicie sesión para acceder al sistema")

if __name__ == "__main__":
    main()
