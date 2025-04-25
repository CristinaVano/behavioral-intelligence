
import streamlit as st
from datetime import datetime
import pandas as pd
from fpdf import FPDF

# Configurar la app
st.set_page_config(page_title="BIAS – Prevención del Terrorismo", page_icon="🔒", layout="centered")

st.title("BIAS – Prevención del Terrorismo")
st.subheader("Evaluación de Riesgo de Radicalización")

st.write("Por favor, completa el siguiente formulario para generar el informe preliminar de riesgo.")

# Cargar registros de usuarios (desde el CSV)
usuarios = pd.read_csv('registros_perfiles.csv')

# Formulario de evaluación
with st.form(key='evaluation_form'):
    # Campo de login
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    
    submit_button = st.form_submit_button(label='Entrar')

    if submit_button:
        # Verificar usuario y contraseña
        if usuario in usuarios['Usuario'].values and contrasena == usuarios.loc[usuarios['Usuario'] == usuario, 'Contraseña'].values[0]:
            st.success("¡Acceso permitido! Bienvenido/a.")
            
            # Evaluación de radicalización
            edad = st.slider("Edad", 12, 80, 25)
            genero = st.selectbox("Género", ("Masculino", "Femenino", "Otro", "Prefiero no decirlo"))
            entorno_social = st.selectbox("Entorno social actual", ("Integrado", "Aislado", "Radicalizado", "Sin información"))
            antecedentes_penales = st.radio("Antecedentes penales por delitos violentos", ("Sí", "No"))
            antecedentes_terrorismo = st.radio("Antecedentes relacionados con terrorismo", ("Sí", "No"))
            discursos_odio = st.radio("Evidencias de discursos de odio", ("Sí", "No"))
            viajes_zonas_conflictivas = st.radio("Viajes recientes a zonas de conflicto", ("Sí", "No"))
            indicadores_psicologicos = st.radio("Indicadores psicológicos preocupantes", ("Sí", "No"))
            participacion_grupos = st.radio("Participación en grupos extremistas", ("Sí", "No"))

            submit_evaluation_button = st.form_submit_button(label='Generar Informe')

            if submit_evaluation_button:
                riesgo = 0
                if entorno_social == "Radicalizado":
                    riesgo += 2
                elif entorno_social == "Aislado":
                    riesgo += 1
                if antecedentes_penales == "Sí":
                    riesgo += 1
                if antecedentes_terrorismo == "Sí":
                    riesgo += 3
                if discursos_odio == "Sí":
                    riesgo += 2
                if viajes_zonas_conflictivas == "Sí":
                    riesgo += 2
                if indicadores_psicologicos == "Sí":
                    riesgo += 1
                if participacion_grupos == "Sí":
                    riesgo += 3

                # Evaluar nivel de riesgo
                if riesgo >= 8:
                    nivel_riesgo = "ALTO"
                elif riesgo >= 4:
                    nivel_riesgo = "MODERADO"
                else:
                    nivel_riesgo = "BAJO"

                # Mostrar informe
                st.success("Informe generado correctamente.")
                st.header("🔒 Informe Preliminar de Riesgo")
                st.write(f"**Fecha de evaluación:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                st.write(f"**Edad:** {edad}")
                st.write(f"**Género:** {genero}")
                st.write(f"**Entorno social:** {entorno_social}")
                st.write(f"**Nivel de riesgo de radicalización:** **{nivel_riesgo}**")

                st.subheader("Notas preliminares:")
                if nivel_riesgo == "ALTO":
                    st.error("Se recomienda activación de protocolo de vigilancia intensiva y notificación a unidades de inteligencia.")
                elif nivel_riesgo == "MODERADO":
                    st.warning("Se recomienda seguimiento regular y evaluación psicológica especializada.")
                else:
                    st.info("Seguimiento habitual. Reevaluar en caso de cambios de conducta.")
                
                # Generar PDF de informe
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(200, 10, txt="Informe Preliminar de Riesgo", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font('Arial', '', 12)
                pdf.cell(200, 10, txt=f"Fecha de evaluación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
                pdf.cell(200, 10, txt=f"Edad: {edad}", ln=True)
                pdf.cell(200, 10, txt=f"Género: {genero}", ln=True)
                pdf.cell(200, 10, txt=f"Entorno social: {entorno_social}", ln=True)
                pdf.cell(200, 10, txt=f"Nivel de riesgo de radicalización: {nivel_riesgo}", ln=True)
                pdf.output("Informe_BIAS.pdf")

                st.download_button(
                    label="Descargar Informe PDF",
                    data=open("Informe_BIAS.pdf", "rb").read(),
                    file_name="Informe_BIAS.pdf",
                    mime="application/pdf"
                )

        else:
            st.error("Usuario o contraseña incorrectos.")
