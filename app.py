import streamlit as st
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io

# Configurar la app
st.set_page_config(page_title="BIAS – Prevención del Terrorismo", page_icon="🔒", layout="centered")

# Cambiar el fondo a blanco
st.markdown("""
    <style>
        .css-18e3th9 {
            background-color: white;
        }
        .css-1v0mbdj {
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Selección de idioma
idioma = st.selectbox("Selecciona tu idioma", ("Español", "Inglés", "Árabe", "Francés"))

# Cambiar idioma según elección
if idioma == "Español":
    st.title("BIAS – Prevención del Terrorismo")
    st.subheader("Evaluación de Riesgo de Radicalización")
    instrucciones = "Por favor, completa el siguiente formulario para generar el informe preliminar de riesgo."
elif idioma == "Inglés":
    st.title("BIAS – Terrorism Prevention")
    st.subheader("Radicalization Risk Assessment")
    instrucciones = "Please fill in the form below to generate the preliminary risk report."
elif idioma == "Árabe":
    st.title("بياس - منع الإرهاب")
    st.subheader("تقييم مخاطر التطرف")
    instrucciones = "يرجى ملء النموذج أدناه لإنشاء التقرير الأولي للمخاطر."
elif idioma == "Francés":
    st.title("BIAS - Prévention du Terrorisme")
    st.subheader("Évaluation des risques de radicalisation")
    instrucciones = "Veuillez remplir le formulaire ci-dessous pour générer le rapport préliminaire sur les risques."

st.write(instrucciones)

# Cargar registros de usuarios (desde el CSV)
usuarios = pd.read_csv('registros_perfiles.csv')

# Verificar si el usuario ya está autenticado
if 'usuario_autenticado' not in st.session_state:
    st.session_state['usuario_autenticado'] = False

# Formulario de login
if not st.session_state['usuario_autenticado']:
    with st.form(key='login_form'):
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        submit_login_button = st.form_submit_button(label="Entrar")

        if submit_login_button:
            # Validar el usuario y contraseña
            if usuario in usuarios['Usuario'].values:
                contrasena_correcta = usuarios.loc[usuarios['Usuario'] == usuario, 'Contraseña'].values[0]
                if contrasena == contrasena_correcta:
                    st.session_state['usuario_autenticado'] = True
                    st.success("¡Acceso permitido! Bienvenido/a.")
                else:
                    st.error("Usuario o contraseña incorrectos.")
            else:
                st.error("Usuario o contraseña incorrectos.")

# Si ya está autenticado, mostrar el formulario de evaluación
if st.session_state['usuario_autenticado']:
    # Formulario de evaluación
    with st.form(key='evaluation_form'):
        # Campos de la evaluación
        edad = st.slider("Edad", 12, 80, 25)
        genero = st.selectbox("Género", ("Masculino", "Femenino", "Otro", "Prefiero no decirlo"))
        nivel_estudios = st.selectbox("Nivel de estudios", ("Secundaria", "Bachillerato", "Grado", "Máster", "Doctorado"))
        consumo_sustancias = st.multiselect("Consumo de sustancias", ("Alcohol", "Tabaco", "Drogas recreativas", "Cocaína", "Heroína"))
        pais_origen = st.text_input("País de origen")
        ciudad_origen = st.text_input("Ciudad de origen")
        antecedentes_penales = st.multiselect("Antecedentes penales", 
            ["Robo", "Homicidio", "Fraude", "Extorsión", "Violencia de género", "Delitos informáticos", 
            "Vandalismo", "Acusaciones falsas", "Amenazas", "Violación", "Terrorismo", "Tráfico de drogas", 
            "Secuestro", "Delitos fiscales", "Blanqueo de dinero"])
        rasgos_personalidad = st.multiselect("Rasgos de personalidad", 
            ["Paranoide", "Antisocial", "Sadomasoquista", "Impulsivo", "Emocionalmente inestable", 
            "Dependiente", "Evitativo"])

        # Sección de comentarios adicionales
        st.subheader("Comentarios adicionales")
        perfil_psicologico = st.text_area("Perfil psicológico completo")
        historial_clinico = st.text_area("Historial clínico completo")
        comentarios_adicionales = st.text_area("Comentarios adicionales")

        submit_evaluation_button = st.form_submit_button(label='Generar Informe')

        if submit_evaluation_button:
            # Aquí se hace el cálculo del riesgo
            riesgo = 0
            if nivel_estudios == "Secundaria":
                riesgo += 1
            elif nivel_estudios == "Bachillerato":
                riesgo += 2
            elif nivel_estudios == "Grado":
                riesgo += 3
            elif nivel_estudios == "Máster":
                riesgo += 4
            elif nivel_estudios == "Doctorado":
                riesgo += 5

            if "Alcohol" in consumo_sustancias:
                riesgo += 1
            if "Tabaco" in consumo_sustancias:
                riesgo += 1
            if "Drogas recreativas" in consumo_sustancias:
                riesgo += 2
            if "Cocaína" in consumo_sustancias or "Heroína" in consumo_sustancias:
                riesgo += 3

            if "Robo" in antecedentes_penales:
                riesgo += 2
            if "Homicidio" in antecedentes_penales:
                riesgo += 3
            if "Violencia de género" in antecedentes_penales:
                riesgo += 3

            if "Paranoide" in rasgos_personalidad:
                riesgo += 2
            if "Antisocial" in rasgos_personalidad:
                riesgo += 3
            if "Sadomasoquista" in rasgos_personalidad:
                riesgo += 1
            if "Impulsivo" in rasgos_personalidad:
                riesgo += 2
            if "Emocionalmente inestable" in rasgos_personalidad:
                riesgo += 3
            if "Dependiente" in rasgos_personalidad or "Evitativo" in rasgos_personalidad:
                riesgo += 2

            # Evaluar nivel de riesgo
            if riesgo >= 15:
                nivel_riesgo = "ALTO"
            elif riesgo >= 10:
                nivel_riesgo = "MODERADO"
            else:
                nivel_riesgo = "BAJO"

            # Mostrar informe
            st.success("Informe generado correctamente.")
            st.header("🔒 Informe Preliminar de Riesgo")
            st.write(f"**Fecha de evaluación:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            st.write(f"**Edad:** {edad}")
            st.write(f"**Género:** {genero}")
            st.write(f"**Nivel de estudios:** {nivel_estudios}")
            st.write(f"**Consumo de sustancias:** {', '.join(consumo_sustancias)}")
            st.write(f"**País de origen:** {pais_origen}")
            st.write(f"**Ciudad de origen:** {ciudad_origen}")
            st.write(f"**Nivel de riesgo de radicalización:** **{nivel_riesgo}**")
            st.write(f"**Perfil psicológico:** {perfil_psicologico}")
            st.write(f"**Historial clínico:** {historial_clinico}")
            st.write(f"**Comentarios adicionales:** {comentarios_adicionales}")

            st.subheader("Notas preliminares:")
            if nivel_riesgo == "ALTO":
                st.error("Se recomienda activación de protocolo de vigilancia intensiva y notificación a unidades de inteligencia.")
            elif nivel_riesgo == "MODERADO":
                st.warning("Se recomienda seguimiento regular y evaluación psicológica especializada.")
            else:
                st.info("Seguimiento habitual. Reevaluar en caso de cambios de conducta.")
            
            # Crear el PDF usando ReportLab en memoria
            pdf_output = io.BytesIO()
            
            # Crear PDF con ReportLab
            c = canvas.Canvas(pdf_output, pagesize=letter)
            c.setFont("Helvetica", 12)

            # Agregar texto al PDF
            c.drawString(100, 750, f"Fecha de evaluación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.drawString(100, 730, f"Edad: {edad}")
            c.drawString(100, 710, f"Género: {genero}")
            c.drawString(100, 690, f"Nivel de estudios: {nivel_estudios}")
            c.drawString(100, 670, f"Consumo de sustancias: {', '.join(consumo_sustancias)}")
            c.drawString(100, 650, f"País de origen: {pais_origen}")
            c.drawString(100, 630, f"Ciudad de origen: {ciudad_origen}")
            c.drawString(100, 610, f"Nivel de riesgo de radicalización: {nivel_riesgo}")
            c.drawString(100, 590, f"Perfil psicológico: {perfil_psicologico}")
            c.drawString(100, 570, f"Historial clínico: {historial_clinico}")
            c.drawString(100, 550, f"Comentarios adicionales: {comentarios_adicionales}")

            # Guardar PDF en memoria
            c.save()

            # Asegurarse de que se pueda descargar
            pdf_output.seek(0)  # Resetear el puntero del archivo
            st.download_button(
                label="Descargar Informe PDF",
                data=pdf_output,
                file_name="Informe_BIAS.pdf",
                mime="application/pdf"
            )
