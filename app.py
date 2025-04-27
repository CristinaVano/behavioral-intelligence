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
        "none_criminal": "Ninguno",
        "personality_traits": "Rasgos de personalidad",
        "paranoid": "Paranoide",
        "antisocial": "Antisocial",
        "sadomasochistic": "Sadomasoquista",
        "impulsive": "Impulsivo",
        "unstable": "Emocionalmente inestable",
        "dependent": "Dependiente",
        "avoidant": "Evitativo",
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
        "diagnosis_list": "Lista de diagnósticos",
        "previous_therapies": "Terapias anteriores",
        "therapy_date": "Fecha inicio terapia",
        "select_date": "Seleccionar fecha",
        "alarm_date": "Fecha señales de alarma",
        "interest_profile": "Perfil de interés",
        "family_extremism": "Antecedentes familiares de extremismo",
        "upload_photo": "Subir foto del sujeto",
        "upload_button": "Subir imagen",
        "photo_requirements": "La foto debe ser tipo DNI con fondo blanco",
        "psychological_profile": "Perfil Psicológico",
        "clinical_history": "Historial Clínico",
        "additional_comments": "Comentarios Adicionales",
        "institutional_recommendations": "Recomendaciones Institucionales",
        "therapy_recommendations": "Recomendaciones Terapéuticas",
        "medical_recommendations": "Recomendaciones Médicas",
        "reintegration_therapy": "Terapia de Reinserción",
        "preventive_measures": "Medidas Preventivas",
        "emergency_measures": "Medidas de Emergencia",
        "risk_factors": "Factores de Riesgo",
        "protective_factors": "Factores de Protección",
        "intervention_plan": "Plan de Intervención",
        "monitoring_plan": "Plan de Seguimiento",
        "social_support": "Apoyo Social",
        "family_support": "Apoyo Familiar",
        "professional_support": "Apoyo Profesional",
        "observations": "Observaciones",
        "recommendations_summary": "Resumen de Recomendaciones",
        "follow_up_date": "Fecha de Seguimiento",
        "evaluator": "Evaluador",
        "evaluation_center": "Centro de Evaluación",
        "evaluation_type": "Tipo de Evaluación",
        "evaluation_context": "Contexto de la Evaluación",
        "evaluation_objective": "Objetivo de la Evaluación",
        "evaluation_methodology": "Metodología de Evaluación",
        "evaluation_tools": "Herramientas de Evaluación",
        "evaluation_limitations": "Limitaciones de la Evaluación",
        "evaluation_reliability": "Fiabilidad de la Evaluación",
        "evaluation_validity": "Validez de la Evaluación",
        "evaluation_recommendations": "Recomendaciones de la Evaluación",
        "evaluation_conclusions": "Conclusiones de la Evaluación",
        "save_evaluation": "Guardar Evaluación",
        "print_evaluation": "Imprimir Evaluación",
        "share_evaluation": "Compartir Evaluación",
        "export_evaluation": "Exportar Evaluación",
        "import_evaluation": "Importar Evaluación",
        "delete_evaluation": "Eliminar Evaluación",
        "edit_evaluation": "Editar Evaluación",
        "clone_evaluation": "Clonar Evaluación",
        "archive_evaluation": "Archivar Evaluación",
        "restore_evaluation": "Restaurar Evaluación",
        "evaluation_history": "Historial de Evaluaciones",
        "evaluation_statistics": "Estadísticas de Evaluación",
        "evaluation_trends": "Tendencias de Evaluación",
        "evaluation_comparisons": "Comparaciones de Evaluación",
        "evaluation_analytics": "Análisis de Evaluación",
        "evaluation_metrics": "Métricas de Evaluación",
        "evaluation_indicators": "Indicadores de Evaluación",
        "evaluation_outcomes": "Resultados de Evaluación",
        "evaluation_impact": "Impacto de la Evaluación",
        "evaluation_effectiveness": "Efectividad de la Evaluación",
        "evaluation_efficiency": "Eficiencia de la Evaluación",
        "evaluation_quality": "Calidad de la Evaluación",
        "evaluation_improvement": "Mejora de la Evaluación",
        "evaluation_feedback": "Retroalimentación de la Evaluación"
    }
}

def calcular_nivel_riesgo(data, lang):
    # Sistema de puntuación para factores de riesgo
    puntuacion = 0
    
    # Antecedentes penales (0-5 puntos)
    antecedentes_graves = ["Homicidio", "Terrorismo", "Violencia de género"]
    for antecedente in data['antecedentes_penales']:
        if antecedente in antecedentes_graves:
            puntuacion += 5
        elif antecedente != "Ninguno":
            puntuacion += 2

    # Consumo de sustancias (0-3 puntos)
    sustancias_graves = ["Cocaína", "Heroína"]
    for sustancia in data['consumo_sustancias']:
        if sustancia in sustancias_graves:
            puntuacion += 3
        elif sustancia != "Ninguna":
            puntuacion += 1

    # Rasgos de personalidad (0-5 puntos)
    rasgos_peligrosos = ["Antisocial", "Paranoide", "Impulsivo"]
    for rasgo in data['rasgos_personalidad']:
        if rasgo in rasgos_peligrosos:
            puntuacion += 2
        elif rasgo != "Ninguno significativo":
            puntuacion += 1

    # Nivel educativo (factor protector, -2 a 0 puntos)
    niveles_educativos = {
        "Sin estudios": 0,
        "Primaria": -0.5,
        "Secundaria": -1,
        "Universidad": -1.5,
        "Postgrado": -2
    }
    puntuacion += niveles_educativos.get(data['nivel_estudios'], 0)

    # Determinar nivel de riesgo según puntuación total
    if puntuacion > 10:
        return lang["high"]
    elif puntuacion > 5:
        return lang["moderate"]
    else:
        return lang["low"]

def generar_recomendaciones(nivel_riesgo, data, lang):
    recomendaciones = {
        "terapeuticas": [],
        "farmacologicas": [],
        "reinsercion": [],
        "prevencion": [],
        "urgencia": []
    }

    # Recomendaciones según nivel de riesgo
    if nivel_riesgo == lang["high"]:
        recomendaciones["terapeuticas"] = [
            "Terapia individual intensiva (2-3 sesiones/semana)",
            "Terapia grupal focalizada en control de impulsos",
            "Intervención familiar sistémica"
        ]
        recomendaciones["farmacologicas"] = [
            "Evaluación psiquiátrica urgente",
            "Considerar medicación estabilizadora"
        ]
        recomendaciones["urgencia"] = [
            "Monitoreo constante",
            "Plan de contención de crisis",
            "Coordinación con fuerzas de seguridad"
        ]
    elif nivel_riesgo == lang["moderate"]:
        recomendaciones["terapeuticas"] = [
            "Terapia individual semanal",
            "Grupos de apoyo"
        ]
        recomendaciones["prevencion"] = [
            "Seguimiento quincenal",
            "Plan de prevención de recaídas"
        ]
    else:
        recomendaciones["prevencion"] = [
            "Seguimiento mensual",
            "Actividades de integración social"
        ]

    # Recomendaciones específicas según factores de riesgo
    if "Alcohol" in data['consumo_sustancias'] or "Drogas recreativas" in data['consumo_sustancias']:
        recomendaciones["reinsercion"].append("Programa de rehabilitación de adicciones")

    if "Antisocial" in data['rasgos_personalidad'] or "Paranoide" in data['rasgos_personalidad']:
        recomendaciones["terapeuticas"].append("Terapia cognitivo-conductual especializada")

    return recomendaciones

def generar_pdf(data, nivel_riesgo, recomendaciones, lang):
    pdf = FPDF()
    pdf.add_page()

    # Configuración de estilos
    pdf.set_font('Arial', 'B', 16)
    pdf.set_fill_color(200, 220, 255)

    # Encabezado
    pdf.cell(0, 10, 'INFORME DE EVALUACIÓN DE RIESGO BIAS', 0, 1, 'C', True)
    pdf.ln(10)

    # Información básica
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'DATOS PERSONALES', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 12)

    datos_basicos = [
        ('Nombre', data['nombre']),
        ('ID', data['numero_identificacion']),
        ('Edad', str(data['edad'])),
        ('Género', data['genero']),
        ('Nivel Educativo', data['nivel_estudios'])
    ]

    for etiqueta, valor in datos_basicos:
        pdf.cell(50, 10, etiqueta + ':', 0)
        pdf.cell(0, 10, valor, 0, 1)

    # Nivel de riesgo
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'EVALUACIÓN DE RIESGO', 0, 1, 'L', True)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f'Nivel de Riesgo: {nivel_riesgo}', 0, 1)

    # Factores de riesgo
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'FACTORES DE RIESGO IDENTIFICADOS', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 12)

    factores = [
        ('Consumo de Sustancias', ', '.join(data['consumo_sustancias'])),
        ('Antecedentes Penales', ', '.join(data['antecedentes_penales'])),
        ('Rasgos de Personalidad', ', '.join(data['rasgos_personalidad']))
    ]

    for categoria, items in factores:
        pdf.cell(0, 10, f'{categoria}:', 0, 1)
        pdf.multi_cell(0, 10, items)

    # Recomendaciones
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'RECOMENDACIONES', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 12)

    for categoria, recs in recomendaciones.items():
        if recs:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, categoria.capitalize() + ':', 0, 1)
            pdf.set_font('Arial', '', 11)
            for rec in recs:
                pdf.cell(10, 10, '•', 0)
                pdf.multi_cell(0, 10, rec)

    # Fecha y firma
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f'Fecha de evaluación: {datetime.now().strftime("%d/%m/%Y")}', 0, 1)
    pdf.cell(0, 10, 'Evaluador: ________________________________', 0, 1)

    # Generar PDF en memoria
    pdf_output = pdf.output(dest='S').encode('latin1')
    return base64.b64encode(pdf_output).decode()

def guardar_registro(data, nivel_riesgo):
    try:
        # Crear DataFrame con los datos
        registro = {
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'nombre': data['nombre'],
            'id': data['numero_identificacion'],
            'nivel_riesgo': nivel_riesgo,
            'edad': data['edad'],
            'genero': data['genero'],
            'nivel_estudios': data['nivel_estudios'],
            'consumo_sustancias': ','.join(data['consumo_sustancias']) if data['consumo_sustancias'] else '',
            'antecedentes_penales': ','.join(data['antecedentes_penales']) if data['antecedentes_penales'] else '',
            'rasgos_personalidad': ','.join(data['rasgos_personalidad']) if data['rasgos_personalidad'] else ''
        }

        # Crear DataFrame con un solo registro
        df_nuevo = pd.DataFrame([registro])

        # Guardar en CSV
        if os.path.exists('registros_perfiles.csv'):
            df_existente = pd.read_csv('registros_perfiles.csv')
            df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_actualizado = df_nuevo

        df_actualizado.to_csv('registros_perfiles.csv', index=False)
        return True
    except Exception as e:
        st.error(f"Error al guardar el registro: {str(e)}")
        return False

def main():
    # Selección de idioma (por ahora solo español)
    language = "Español"
    lang = translations[language]

    st.title(lang["app_title"])

    # Sistema de autenticación
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            username = st.text_input(lang["username"])
            password = st.text_input(lang["password"], type="password")
            submit = st.form_submit_button(lang["login_button"])

            if submit:
                if username == "admin" and password == "password":
                    st.session_state.authenticated = True
                    st.success(lang["welcome"])
                    st.rerun()
                else:
                    st.error(lang["login_error"])

    else:
        # Botón de cierre de sesión en la barra lateral
        if st.sidebar.button(lang["logout"]):
            st.session_state.authenticated = False
            st.rerun()

        # Formulario principal
        with st.form("evaluation_form"):
            st.header(lang["profile_section"])

            # División en columnas para mejor organización
            col1, col2 = st.columns(2)

            with col1:
                nombre = st.text_input(lang["name"], key='nombre')
                numero_identificacion = st.text_input(lang["id_number"], key='numero_identificacion')
                edad = st.number_input(lang["age"], min_value=18, max_value=100, key='edad')
                genero = st.radio(lang["gender"], 
                                [lang["male"], lang["female"], lang["other"]], 
                                key='genero')
                nivel_estudios = st.selectbox(lang["education"],
                                            [lang["none"], lang["primary"], lang["secondary"],
                                             lang["university"], lang["postgraduate"]],
                                            key='nivel_estudios')

            with col2:
                consumo_sustancias = st.multiselect(lang["substances"],
                                                  [lang["alcohol"], lang["tobacco"], 
                                                   lang["recreational"], lang["cocaine"],
                                                   lang["heroin"], lang["none_substance"]],
                                                  key='consumo_sustancias')

                antecedentes_penales = st.multiselect(lang["criminal_record"],
                                                    [lang["theft"], lang["gender_violence"],
                                                     lang["homicide"], lang["terrorism"],
                                                     lang["none_criminal"]],
                                                    key='antecedentes_penales')

                rasgos_personalidad = st.multiselect(lang["personality_traits"],
                                                   [lang["paranoid"], lang["antisocial"],
                                                    lang["sadomasochistic"], lang["impulsive"],
                                                    lang["unstable"], lang["dependent"],
                                                    lang["avoidant"], lang["none_traits"]],
                                                   key='rasgos_personalidad')

            # Campos adicionales
            st.subheader(lang["psychological_profile"])
            perfil_psicologico = st.text_area("", key='perfil_psicologico')

            st.subheader(lang["clinical_history"])
            historial_clinico = st.text_area("", key='historial_clinico')

            col3, col4 = st.columns(2)
            with col3:
                fecha_inicio_terapia = st.date_input(lang["therapy_date"], key='fecha_terapia')
            with col4:
                fecha_alarma = st.date_input(lang["alarm_date"], key='fecha_alarma')

            st.subheader(lang["interest_profile"])
            motivo_interes = st.text_area("", key='motivo_interes')

            st.subheader(lang["family_extremism"])
            antecedentes_extremismo = st.text_area("", key='antecedentes_extremismo')

            # Subida de foto
            uploaded_file = st.file_uploader(lang["upload_photo"], 
                                           type=["jpg", "jpeg", "png"],
                                           key='foto')
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption=lang["photo_requirements"])

            # Botón de envío
            submit_button = st.form_submit_button(lang["submit"])

            if submit_button:
                # Validación de campos obligatorios
                required_fields = {
                    'nombre': nombre,
                    'numero_identificacion': numero_identificacion,
                    'edad': edad,
                    'genero': genero,
                    'nivel_estudios': nivel_estudios
                }

                missing_fields = [key for key, value in required_fields.items() if not value]

                if missing_fields:
                    st.error(f"{lang['field_required']}: {', '.join(missing_fields)}")
                else:
                    # Recopilar datos
                    data = {
                        'nombre': nombre,
                        'numero_identificacion': numero_identificacion,
                        'edad': edad,
                        'genero': genero,
                        'nivel_estudios': nivel_estudios,
                        'consumo_sustancias': consumo_sustancias,
                        'antecedentes_penales': antecedentes_penales,
                        'rasgos_personalidad': rasgos_personalidad,
                        'perfil_psicologico': perfil_psicologico,
                        'historial_clinico': historial_clinico,
                        'fecha_inicio_terapia': fecha_inicio_terapia,
                        'fecha_alarma': fecha_alarma,
                        'motivo_interes': motivo_interes,
                        'antecedentes_extremismo': antecedentes_extremismo
                    }

                    def calcular_nivel_riesgo(data, lang):
    puntuacion = 0
    # Modifica estos valores según necesites
    if puntuacion > 10:  # Cambia este umbral
        return lang["high"]
    elif puntuacion > 5:  # Cambia este umbral
        return lang["moderate"]
    else:
        return lang["low"]

                    # Generar recomendaciones
                    recomendaciones = generar_recomendaciones(nivel_riesgo, data, lang)

                    # Guardar registro
                    if guardar_registro(data, nivel_riesgo):
                        # Mostrar resultados
                        st.success(lang["results_section"])

                        # Sección de resultados
                        st.header(lang["results_section"])

                        # Mostrar nivel de riesgo con formato
                        st.subheader(lang["risk_level"])
                        if nivel_riesgo == lang["high"]:
                            st.error(nivel_riesgo)
                            st.write(lang["high_explanation"])
                        elif nivel_riesgo == lang["moderate"]:
                            st.warning(nivel_riesgo)
                            st.write(lang["moderate_explanation"])
                        else:
                            st.success(nivel_riesgo)
                            st.write(lang["low_explanation"])

                        # Mostrar recomendaciones
                        st.subheader(lang["recommendations"])

                        col5, col6 = st.columns(2)
                        with col5:
                            if recomendaciones["terapeuticas"]:
                                st.write(lang["therapy_recs"])
                                for rec in recomendaciones["terapeuticas"]:
                                    st.write(f"• {rec}")

                            if recomendaciones["farmacologicas"]:
                                st.write(lang["medication_recs"])
                                for rec in recomendaciones["farmacologicas"]:
                                    st.write(f"• {rec}")

                        with col6:
                            if recomendaciones["reinsercion"]:
                                st.write(lang["reintegration_recs"])
                                for rec in recomendaciones["reinsercion"]:
                                    st.write(f"• {rec}")

                            if recomendaciones["prevencion"]:
                                st.write(lang["prevention_recs"])
                                for rec in recomendaciones["prevencion"]:
                                    st.write(f"• {rec}")

                        if recomendaciones["urgencia"]:
                            st.error(lang["urgent_measures"])
                            for rec in recomendaciones["urgencia"]:
                                st.write(f"• {rec}")

                        # Generar y ofrecer descarga del informe
                        pdf_b64 = generar_pdf(data, nivel_riesgo, recomendaciones, lang)
                        href = f'<a href="data:application/pdf;base64,{pdf_b64}" download="informe_BIAS_{data["numero_identificacion"]}.pdf">{lang["download_detailed"]}</a>'
                        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
