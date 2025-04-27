import streamlit as st
from datetime import datetime
from fpdf import FPDF
import io
import os
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="BIAS - Sistema de Análisis de Riesgo",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CONFIGURACIÓN DE DATOS (SOLO ESPAÑOL)
# =============================================
OPCIONES_SUSTANCIAS = [
    "Alcohol", "Tabaco", "Drogas recreativas", 
    "Cocaína", "Heroína", "Ninguna"
]

ANTECEDENTES_PENALES = [
    "Robo", "Violencia de género", "Homicidio", "Terrorismo", "Ninguno",
    "Aislamiento social progresivo", "Justificación de la violencia",
    "Fascinación por ideologías extremistas", "Cambios drásticos en comportamiento",
    "Expresión de odio hacia grupos", "Contacto con radicalizados",
    "Consumo propaganda extremista", "Actividades sospechosas online",
    "Intento de reclutamiento", "Preparación física para combate"
]

RASGOS_PERSONALIDAD = [
    "Paranoide", "Antisocial", "Sadomasoquista", "Impulsivo", 
    "Emocionalmente inestable", "Dependiente", "Evitativo",
    "Narcisista", "Histriónico", "Pasivo-agresivo", "Esquizoide",
    "Obcecado con el control", "Ninguno significativo"
]

DIAGNOSTICOS_SALUD_MENTAL = [
    "Trastorno estrés postraumático (TEPT)", "Trastorno límite personalidad (TLP)",
    "Trastorno bipolar", "Esquizofrenia", "Depresión mayor recurrente",
    "Trastorno obsesivo-compulsivo (TOC)", "Trastorno ansiedad generalizada (TAG)",
    "Trastorno de pánico", "Fobia social", "Trastorno de la conducta"
]

# =============================================
# FUNCIONES PARA GENERAR PDF
# =============================================
def generar_informe_generico(datos):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "INFORME GENÉRICO BIAS", 0, 1, 'C')
    pdf.ln(10)
    
    # Sección 1: Datos del sujeto
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Datos del sujeto", 0, 1)
    pdf.set_font('Arial', '', 12)
    
    campos = [
        ("Nombre completo", datos['nombre']),
        ("ID", datos['id']),
        ("Edad", str(datos['edad'])),
        ("Género", datos['genero']),
        ("Nivel educativo", datos['educacion']),
        ("Consumo sustancias", ", ".join(datos['sustancias'])),
        ("Antecedentes penales", ", ".join(datos['antecedentes'])),
        ("Rasgos personalidad", ", ".join(datos['rasgos'])),
        ("Diagnósticos", ", ".join(datos['diagnosticos'])),
        ("Terapias previas", datos['terapias']),
        ("Año señales alarma", str(datos['ano_alarma'])),
        ("Motivo interés", datos['motivo_interes']),
        ("Antecedentes extremismo", datos['antecedentes_extremismo']),
        ("Historial clínico", datos['historial_clinico']),
        ("Perfil psicológico", datos['perfil_psicologico']),
        ("Comentarios", datos['comentarios'])
    ]
    
    for campo, valor in campos:
        pdf.cell(90, 8, f"{campo}:", 0, 0)
        pdf.multi_cell(0, 8, valor)
        pdf.ln(2)
    
    # Foto
    if datos['foto']:
        img_path = "temp_foto.jpg"
        Image.open(datos['foto']).save(img_path)
        pdf.image(img_path, x=160, y=20, w=30)
        os.remove(img_path)
    
    # Sección 2: Riesgo y recomendaciones
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Nivel de riesgo y recomendaciones", 0, 1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 8, "Nivel de riesgo:", 0, 0)
    pdf.set_text_color(255, 0, 0)  # Rojo para alto riesgo
    pdf.cell(0, 8, "ALTO", 0, 1)
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 8, "Explicación: El sujeto presenta múltiples factores de riesgo que indican alta probabilidad de radicalización violenta. Se recomienda intervención inmediata.")
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Recomendaciones:", 0, 1)
    recomendaciones = [
        "1. Terapia intensiva con especialista en radicalización",
        "2. Monitorización constante de actividades online",
        "3. Restricción de acceso a material extremista",
        "4. Programa de reinserción social supervisado"
    ]
    for rec in recomendaciones:
        pdf.cell(0, 8, rec, 0, 1)
    
    # Sección 3: Gráficos (placeholders)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Análisis gráfico", 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, "Gráfico 1: Urgencia de actuación (ver plataforma)", 0, 1)
    pdf.cell(0, 8, "Gráfico 2: Probabilidad de radicalización (ver plataforma)", 0, 1)
    pdf.cell(0, 8, "Tabla 1: Evolución del riesgo sin intervención", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

def generar_informe_direccion(datos):
    # Similar al anterior pero con sección de puntuación
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "INFORME DIRECCIÓN BIAS", 0, 1, 'C')
    pdf.ln(10)
    
    # Sistema de puntuación
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Sistema de puntuación técnico", 0, 1)
    pdf.set_font('Arial', '', 12)
    
    puntuaciones = [
        ("Antecedentes penales", "15/20 puntos"),
        ("Rasgos personalidad", "12/15 puntos"),
        ("Consumo sustancias", "8/10 puntos"),
        ("Diagnósticos", "10/15 puntos")
    ]
    
    for categoria, puntos in puntuaciones:
        pdf.cell(90, 8, f"{categoria}:", 0, 0)
        pdf.cell(0, 8, puntos, 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

# =============================================
# INTERFAZ PRINCIPAL
# =============================================
def main():
    # Gestión de autenticación
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
        st.session_state.usuario = ""
        st.session_state.datos = {}
    
    # Barra lateral de login
    with st.sidebar:
        if not st.session_state.autenticado:
            st.header("🔐 Autenticación")
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
            st.header(f"👤 {st.session_state.usuario}")
            if st.button("🚪 Cerrar sesión"):
                st.session_state.autenticado = False
                st.session_state.datos = {}
                st.rerun()
    
    # Contenido principal
    if st.session_state.autenticado:
        st.title("📋 Formulario de Evaluación BIAS")
        
        with st.form("form_evaluacion"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre completo")
                id_num = st.text_input("Número de identificación")
                edad = st.number_input("Edad", 10, 100, 18)
                genero = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
                educacion = st.selectbox("Nivel educativo", ["Primaria", "Secundaria", "Universidad", "Postgrado", "Ninguno"])
                sustancias = st.multiselect("Consumo de sustancias", OPCIONES_SUSTANCIAS)
                antecedentes = st.multiselect("Antecedentes penales", ANTECEDENTES_PENALES)
                rasgos = st.multiselect("Rasgos de personalidad", RASGOS_PERSONALIDAD)
            
            with col2:
                diagnosticos = st.multiselect("Diagnósticos previos", DIAGNOSTICOS_SALUD_MENTAL)
                terapias = st.text_input("Terapias previas (especificar)")
                terapia_fecha = st.date_input("Fecha inicio terapia", disabled=("Ninguna" in terapias))
                ano_alarma = st.selectbox("Año de señales de alarma", list(range(2000, datetime.now().year + 1)))
                motivo_interes = st.text_area("Motivo de interés/investigación")
                antecedentes_extremismo = st.text_area("Antecedentes de extremismo familiar")
                historial_clinico = st.text_area("Historial clínico completo")
                perfil_psicologico = st.text_area("Perfil psicológico detallado")
                comentarios = st.text_area("Comentarios adicionales")
                foto = st.file_uploader("Subir foto del sujeto (formato carnet)", type=["jpg", "png"])
            
            if st.form_submit_button("📤 Generar informes"):
                datos = {
                    'nombre': nombre,
                    'id': id_num,
                    'edad': edad,
                    'genero': genero,
                    'educacion': educacion,
                    'sustancias': sustancias,
                    'antecedentes': antecedentes,
                    'rasgos': rasgos,
                    'diagnosticos': diagnosticos,
                    'terapias': terapias,
                    'ano_alarma': ano_alarma,
                    'motivo_interes': motivo_interes,
                    'antecedentes_extremismo': antecedentes_extremismo,
                    'historial_clinico': historial_clinico,
                    'perfil_psicologico': perfil_psicologico,
                    'comentarios': comentarios,
                    'foto': foto
                }
                st.session_state.datos = datos
                st.success("✅ Datos guardados correctamente")
        
        # Generación de informes
        if st.session_state.datos:
            st.divider()
            st.header("📄 Informes Generados")
            
            # Generar PDF genérico
            pdf_bytes = generar_informe_generico(st.session_state.datos)
            st.download_button(
                label="⬇️ Descargar Informe Genérico (PDF)",
                data=pdf_bytes,
                file_name="informe_generico_bias.pdf",
                mime="application/pdf"
            )
            
            # Informe adicional para directores
            if st.session_state.usuario in ["JuanCarlos_bias", "Cristina_bias"]:
                st.divider()
                pdf_dir_bytes = generar_informe_direccion(st.session_state.datos)
                st.download_button(
                    label="⬇️ Descargar Informe Dirección (PDF)",
                    data=pdf_dir_bytes,
                    file_name="informe_direccion_bias.pdf",
                    mime="application/pdf"
                )
    else:
        st.info("🔒 Por favor inicie sesión para acceder al sistema")

if __name__ == "__main__":
    main()
