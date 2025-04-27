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
        "diagnosis_list": "Diagnósticos previos",
        "previous_therapies": "Terapias previas",
        "therapy_date": "Fecha de inicio de terapia",
        "select_date": "Seleccionar fecha",
        "alarm_date": "Fecha de señales de alarma",
        "interest_profile": "Motivo de interés",
        "family_extremism": "Antecedentes de extremismo familiar",
        "upload_photo": "Subir fotografía del sujeto",
        "upload_button": "Subir imagen",
        "photo_requirements": "La fotografía debe ser tipo carnet con fondo blanco"
    },
    "English": {
        "app_title": "BIAS - Behavioral Intelligence Analysis System",
        "welcome": "Welcome to the Behavioral Intelligence Analysis System",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "login_button": "Enter",
        "language": "Language",
        "logout": "Logout",
        "profile_section": "Evaluation Profile",
        "name": "Full Name",
        "id_number": "ID Number",
        "age": "Age",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "other": "Other",
        "education": "Education Level",
        "primary": "Primary",
        "secondary": "Secondary",
        "university": "University",
        "postgraduate": "Postgraduate",
        "none": "No Education",
        "substances": "Substance Use",
        "alcohol": "Alcohol",
        "tobacco": "Tobacco",
        "recreational": "Recreational Drugs",
        "cocaine": "Cocaine",
        "heroin": "Heroin",
        "none_substance": "None",
        "criminal_record": "Criminal Record",
        "theft": "Theft",
        "gender_violence": "Gender Violence",
        "homicide": "Homicide",
        "terrorism": "Terrorism",
        "none_criminal": "None",
        "personality_traits": "Personality Traits",
        "paranoid": "Paranoid",
        "antisocial": "Antisocial",
        "sadomasochistic": "Sadomasochistic",
        "impulsive": "Impulsive",
        "unstable": "Emotionally Unstable",
        "dependent": "Dependent",
        "avoidant": "Avoidant",
        "none_traits": "No Significant Traits",
        "submit": "Submit Evaluation",
        "results_section": "Evaluation Results",
        "risk_level": "Risk Level:",
        "high": "HIGH",
        "moderate": "MODERATE",
        "low": "LOW",
        "evaluation_date": "Evaluation Date:",
        "generate_report": "Generate Report",
        "download_report": "Download Report",
        "download_detailed": "Download Detailed Report",
        "login_error": "Incorrect username or password",
        "field_required": "This field is required",
        "results_info": "After submitting the evaluation, the risk analysis results will be displayed here.",
        "recommendations": "Institutional Recommendations",
        "therapy_recs": "Therapeutic Recommendations",
        "medication_recs": "Pharmacological Recommendations",
        "reintegration_recs": "Reintegration Therapies",
        "prevention_recs": "Preventive Measures",
        "urgent_measures": "Urgent Measures",
        "explanation": "Risk Level Explanation",
        "high_explanation": "The subject presents multiple significant risk factors that suggest a high probability of violent radicalization. Immediate intervention and constant monitoring are recommended.",
        "moderate_explanation": "The subject presents some relevant risk factors that require attention and follow-up. Preventive intervention and periodic evaluation are recommended.",
        "low_explanation": "The subject presents few risk factors. Routine follow-up and basic preventive measures are recommended.",
        "scoring_report": "Detailed Scoring Report",
        "detailed_scoring": "Detailed Scoring",
        "total_risk_score": "Total risk score",
        "education_score": "Education level score",
        "substances_score": "Substance use score",
        "criminal_score": "Criminal record score",
        "personality_score": "Personality traits score",
        "diagnosis_list": "Previous diagnoses",
        "previous_therapies": "Previous therapies",
        "therapy_date": "Therapy start date",
        "select_date": "Select date",
        "alarm_date": "Date of warning signs",
        "interest_profile": "Reason for interest",
        "family_extremism": "Family history of extremism",
        "upload_photo": "Upload subject photo",
        "upload_button": "Upload image",
        "photo_requirements": "Photo must be ID-type with white background"
    },
    "العربية": {
        "app_title": "BIAS - نظام تحليل الذكاء السلوكي",
        "welcome": "مرحبًا بك في نظام تحليل الذكاء السلوكي",
        "login": "تسجيل الدخول",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_button": "دخول",
        "language": "اللغة",
        "logout": "تسجيل الخروج",
        "profile_section": "ملف التقييم",
        "name": "الاسم الكامل",
        "id_number": "رقم الهوية",
        "age": "العمر",
        "gender": "الجنس",
        "male": "ذكر",
        "female": "أنثى",
        "other": "آخر",
        "education": "المستوى التعليمي",
        "primary": "ابتدائي",
        "secondary": "ثانوي",
        "university": "جامعي",
        "postgraduate": "دراسات عليا",
        "none": "بدون تعليم",
        "substances": "تعاطي المواد",
        "alcohol": "الكحول",
        "tobacco": "التبغ",
        "recreational": "المخدرات الترفيهية",
        "cocaine": "الكوكايين",
        "heroin": "الهيروين",
        "none_substance": "لا شيء",
        "criminal_record": "السجل الجنائي",
        "theft": "سرقة",
        "gender_violence": "عنف على أساس الجنس",
        "homicide": "قتل",
        "terrorism": "إرهاب",
        "none_criminal": "لا شيء",
        "personality_traits": "سمات الشخصية",
        "paranoid": "جنوني",
        "antisocial": "معادي للمجتمع",
        "sadomasochistic": "سادي مازوخي",
        "impulsive": "متهور",
        "unstable": "غير مستقر عاطفياً",
        "dependent": "اعتمادي",
        "avoidant": "تجنبي",
        "none_traits": "لا توجد سمات مهمة",
        "submit": "إرسال التقييم",
        "results_section": "نتائج التقييم",
        "risk_level": "مستوى الخطر:",
        "high": "عالي",
        "moderate": "متوسط",
        "low": "منخفض",
        "evaluation_date": "تاريخ التقييم:",
        "generate_report": "إنشاء تقرير",
        "download_report": "تنزيل التقرير",
        "download_detailed": "تنزيل التقرير المفصل",
        "login_error": "اسم المستخدم أو كلمة المرور غير صحيحة",
        "field_required": "هذا الحقل مطلوب",
        "results_info": "بعد إرسال التقييم، ستظهر هنا نتائج تحليل المخاطر.",
        "recommendations": "التوصيات المؤسسية",
        "therapy_recs": "التوصيات العلاجية",
        "medication_recs": "التوصيات الدوائية",
        "reintegration_recs": "علاجات إعادة الدمج",
        "prevention_recs": "تدابير وقائية",
        "urgent_measures": "تدابير عاجلة",
        "explanation": "شرح مستوى الخطر",
        "high_explanation": "يظهر الشخص عوامل خطر متعددة مهمة تشير إلى احتمالية عالية للتطرف العنيف. يوصى بالتدخل الفوري والمراقبة المستمرة.",
        "moderate_explanation": "يظهر الشخص بعض عوامل الخطر ذات الصلة التي تتطلب اهتمامًا ومتابعة. يوصى بالتدخل الوقائي والتقييم الدوري.",
        "low_explanation": "يظهر الشخص عدد قليل من عوامل الخطر. يوصى بالمتابعة الروتينية والتدابير الوقائية الأساسية.",
        "scoring_report": "تقرير التسجيل المفصل",
        "detailed_scoring": "التسجيل المفصل",
        "total_risk_score": "مجموع نقاط الخطر",
        "education_score": "نقاط المستوى التعليمي",
        "substances_score": "نقاط تعاطي المواد",
        "criminal_score": "نقاط السجل الجنائي",
        "personality_score": "نقاط سمات الشخصية",
        "diagnosis_list": "التشخيصات السابقة",
        "previous_therapies": "العلاجات السابقة",
        "therapy_date": "تاريخ بدء العلاج",
        "select_date": "اختر التاريخ",
        "alarm_date": "تاريخ علامات التحذير",
        "interest_profile": "سبب الاهتمام",
        "family_extremism": "التاريخ العائلي للتطرف",
        "upload_photo": "تحميل صورة الشخص",
        "upload_button": "تحميل الصورة",
        "photo_requirements": "يجب أن تكون الصورة من نوع الهوية بخلفية بيضاء"
    },
    "Français": {
        "app_title": "BIAS - Système d'Analyse de l'Intelligence Comportementale",
        "welcome": "Bienvenue au Système d'Analyse de l'Intelligence Comportementale",
        "login": "Connexion",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "login_button": "Entrer",
        "language": "Langue",
        "logout": "Déconnexion",
        "profile_section": "Profil d'évaluation",
        "name": "Nom complet",
        "id_number": "Numéro d'identification",
        "age": "Âge",
        "gender": "Genre",
        "male": "Masculin",
        "female": "Féminin",
        "other": "Autre",
        "education": "Niveau d'éducation",
        "primary": "Primaire",
        "secondary": "Secondaire",
        "university": "Universitaire",
        "postgraduate": "Postuniversitaire",
        "none": "Sans éducation",
        "substances": "Consommation de substances",
        "alcohol": "Alcool",
        "tobacco": "Tabac",
        "recreational": "Drogues récréatives",
        "cocaine": "Cocaïne",
        "heroin": "Héroïne",
        "none_substance": "Aucune",
        "criminal_record": "Antécédents criminels",
        "theft": "Vol",
        "gender_violence": "Violence basée sur le genre",
        "homicide": "Homicide",
        "terrorism": "Terrorisme",
        "none_criminal": "Aucun",
        "personality_traits": "Traits de personnalité",
        "paranoid": "Paranoïaque",
        "antisocial": "Antisocial",
        "sadomasochistic": "Sadomasochiste",
        "impulsive": "Impulsif",
        "unstable": "Émotionnellement instable",
        "dependent": "Dépendant",
        "avoidant": "Évitant",
        "none_traits": "Aucun trait significatif",
        "submit": "Soumettre l'évaluation",
        "results_section": "Résultats de l'évaluation",
        "risk_level": "Niveau de risque:",
        "high": "ÉLEVÉ",
        "moderate": "MODÉRÉ",
        "low": "FAIBLE",
        "evaluation_date": "Date d'évaluation:",
        "generate_report": "Générer le rapport",
        "download_report": "Télécharger le rapport",
        "download_detailed": "Télécharger le rapport détaillé",
        "login_error": "Nom d'utilisateur ou mot de passe incorrect",
        "field_required": "Ce champ est obligatoire",
        "results_info": "Après avoir soumis l'évaluation, les résultats de l'analyse des risques seront affichés ici.",
        "recommendations": "Recommandations institutionnelles",
        "therapy_recs": "Recommandations thérapeutiques",
        "medication_recs": "Recommandations pharmacologiques",
        "reintegration_recs": "Thérapies de réintégration",
        "prevention_recs": "Mesures préventives",
        "urgent_measures": "Mesures urgentes",
        "explanation": "Explication du niveau de risque",
        "high_explanation": "Le sujet présente de multiples facteurs de risque significatifs qui suggèrent une forte probabilité de radicalisation violente. Une intervention immédiate et une surveillance constante sont recommandées.",
        "moderate_explanation": "Le sujet présente certains facteurs de risque pertinents qui nécessitent attention et suivi. Une intervention préventive et une évaluation périodique sont recommandées.",
        "low_explanation": "Le sujet présente peu de facteurs de risque. Un suivi de routine et des mesures préventives de base sont recommandés.",
        "scoring_report": "Rapport de scoring détaillé",
        "detailed_scoring": "Scoring détaillé",
        "total_risk_score": "Score total de risque",
        "education_score": "Score de niveau d'éducation",
        "substances_score": "Score de consommation de substances",
        "criminal_score": "Score d'antécédents criminels",
        "personality_score": "Score de traits de personnalité",
        "diagnosis_list": "Diagnostics précédents",
        "previous_therapies": "Thérapies précédentes",
        "therapy_date": "Date de début de thérapie",
        "select_date": "Sélectionner la date",
        "alarm_date": "Date des signes d'alarme",
        "interest_profile": "Motif d'intérêt",
        "family_extremism": "Antécédents familiaux d'extrémisme",
        "upload_photo": "Télécharger photo du sujet",
        "upload_button": "Télécharger l'image",
        "photo_requirements": "La photo doit être de type ID avec fond blanc"
    }
}

# Inicializar las variables de estado de la sesión si no existen
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['username'] = ""
    st.session_state['rol_usuario'] = ""

if 'idioma' not in st.session_state:
    st.session_state['idioma'] = "Español"

# Función para cambiar el idioma
def change_language():
    st.session_state['idioma'] = st.session_state['language_selector']

# Obtener el diccionario del idioma seleccionado
lang = translations[st.session_state['idioma']]

# Leer el CSV de usuarios (o crearlo si no existe)
def load_users():
    try:
        if os.path.exists('registros_perfiles.csv'):
            df = pd.read_csv('registros_perfiles.csv')
            # Asegurarse de que tiene las columnas correctas
            if 'Usuario' in df.columns and 'Contraseña' in df.columns and 'Rol' in df.columns:
                print("Columnas después de ajustes:", df.columns.tolist())
                print("Contenido final del DataFrame:")
                print(df)
                return df
            else:
                # Crear un dataframe con las columnas correctas
                df = pd.DataFrame({
                    'Usuario': ['demo_bias', 'JuanCarlos_bias', 'Cristina_bias'],
                    'Contraseña': ['biasdemo2025', 'admin_bias', 'admin_bias'],
                    'Rol': ['evaluador', 'director', 'director']
                })
                df.to_csv('registros_perfiles.csv', index=False)
                return df
        else:
            # Crear un dataframe con usuarios predeterminados
            df = pd.DataFrame({
                'Usuario': ['demo_bias', 'JuanCarlos_bias', 'Cristina_bias'],
                'Contraseña': ['biasdemo2025', 'admin_bias', 'admin_bias'],
                'Rol': ['evaluador', 'director', 'director']
            })
            df.to_csv('registros_perfiles.csv', index=False)
            return df
    except Exception as e:
        st.error(f"Error al cargar usuarios: {e}")
        # Crear un dataframe con usuarios predeterminados en caso de error
        df = pd.DataFrame({
            'Usuario': ['demo_bias', 'JuanCarlos_bias', 'Cristina_bias'],
            'Contraseña': ['biasdemo2025', 'admin_bias', 'admin_bias'],
            'Rol': ['evaluador', 'director', 'director']
        })
        df.to_csv('registros_perfiles.csv', index=False)
        return df

# Cargar usuarios
users_df = load_users()

# Barra lateral para el selector de idioma y login/logout
with st.sidebar:
    # Selector de idioma en la parte superior de la barra lateral
    st.selectbox(
        label=lang["language"],
        options=["Español", "English", "العربية", "Français"],
        key="language_selector",
        on_change=change_language,
        index=["Español", "English", "العربية", "Français"].index(st.session_state['idioma'])
    )
    
    # Separador
    st.markdown("---")
    
    # Formulario de login si no está autenticado
    if not st.session_state['authenticated']:
        st.subheader(lang["login"])
        username = st.text_input(lang["username"])
        password = st.text_input(lang["password"], type="password")
        
        if st.button(lang["login_button"]):
            # Verificar las credenciales
            user_row = users_df[(users_df['Usuario'] == username) & (users_df['Contraseña'] == password)]
            if not user_row.empty:
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['rol_usuario'] = user_row.iloc[0]['Rol']
                st.rerun()
            else:
                st.error(lang["login_error"])
    else:
        # Mostrar el nombre de usuario y botón de logout
        st.subheader(f"{lang['welcome']}, {st.session_state['username']}")
        if st.button(lang["logout"]):
            st.session_state['authenticated'] = False
            st.session_state['username'] = ""
            st.session_state['rol_usuario'] = ""
            st.rerun()

# Título principal de la aplicación
st.title(lang["app_title"])

# Verificar si el usuario está autenticado para mostrar el contenido
if st.session_state['authenticated']:
    # Contenedor para el formulario de evaluación
    with st.container():
        st.header(lang["profile_section"])
        
        # Crear formulario
        with st.form(key="evaluation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input(lang["name"], key="nombre")
                numero_id = st.text_input(lang["id_number"], key="numero_id")
                edad = st.number_input(lang["age"], min_value=14, max_value=100, value=25, key="edad")
                genero = st.selectbox(
                    lang["gender"],
                    [lang["male"], lang["female"], lang["other"]],
                    key="genero"
                )
            
            with col2:
                education_options = [lang["primary"], lang["secondary"], lang["university"], lang["postgraduate"], lang["none"]]
                nivel_estudios = st.selectbox(
                    lang["education"],
                    education_options,
                    key="nivel_estudios"
                )
                
                sustancias_opciones = [lang["alcohol"], lang["tobacco"], lang["recreational"], 
                                     lang["cocaine"], lang["heroin"], lang["none_substance"]]
                consumo_sustancias = st.multiselect(
                    lang["substances"],
                    sustancias_opciones,
                    default=[lang["none_substance"]],
                    key="consumo_sustancias"
                )
                
                antecedentes_opciones = [lang["theft"], lang["gender_violence"], 
                                        lang["homicide"], lang["terrorism"], lang["none_criminal"]]
                antecedentes_penales = st.multiselect(
                    lang["criminal_record"],
                    antecedentes_opciones,
                    default=[lang["none_criminal"]],
                    key="antecedentes_penales"
                )
                
                personalidad_opciones = [lang["paranoid"], lang["antisocial"], lang["sadomasochistic"],
                                        lang["impulsive"], lang["unstable"], lang["dependent"],
                                        lang["avoidant"], lang["none_traits"]]
                rasgos_personalidad = st.multiselect(
                    lang["personality_traits"],
                    personalidad_opciones,
                    default=[lang["none_traits"]],
                    key="rasgos_personalidad"
                )
            
            # Agregar campos adicionales
            col3, col4 = st.columns(2)
            
            with col3:
                diagnosticos_opciones = ["Trastorno de personalidad", "Depresión", "Trastorno bipolar", 
                                       "Esquizofrenia", "Trastorno de ansiedad", "TEPT", "Trastorno obsesivo-compulsivo"]
                diagnosticos_previos = st.multiselect(
                    lang["diagnosis_list"],
                    diagnosticos_opciones,
                    key="diagnosticos_previos"
                )
                
                terapia_previa = st.selectbox(
                    lang["previous_therapies"],
                    ["Ninguna", "Psicoterapia individual", "Terapia grupal", "Rehabilitación por adicciones", 
                     "Terapia familiar", "Intervención psiquiátrica"],
                    key="terapia_previa"
                )
                
                fecha_inicio_terapia = st.date_input(
                    lang["therapy_date"],
                    value=None,
                    key="fecha_inicio_terapia",
                    disabled=(terapia_previa == "Ninguna")
                )
            
            with col4:
                fecha_alarma = st.date_input(
                    lang["alarm_date"],
                    key="fecha_alarma"
                )
                
                motivo_interes = st.text_area(
                    lang["interest_profile"],
                    height=100,
                    max_chars=500,
                    key="motivo_interes"
                )
                
                antecedentes_extremismo = st.text_area(
                    lang["family_extremism"],
                    height=100,
                    max_chars=500,
                    key="antecedentes_extremismo"
                )
            
            # Subida de fotografía
            st.subheader(lang["upload_photo"])
            st.caption(lang["photo_requirements"])
            foto_subida = st.file_uploader(lang["upload_button"], type=["jpg", "jpeg", "png"], key="foto_subida")
            
            # Botón de envío
            submitted = st.form_submit_button(lang["submit"])

    # Contenedor para los resultados y PDF
    with st.container():
        st.header(lang["results_section"])
        
        if 'results_displayed' not in st.session_state:
            st.session_state['results_displayed'] = False
            st.info(lang["results_info"])
        
        # Procesar el formulario cuando se envía
        if submitted:
            # Validar campos obligatorios
            if not nombre or not numero_id:
                st.error(lang["field_required"])
            else:
                # Calcular puntuación de riesgo
                riesgo = 0
                
                # Puntuación por nivel educativo (invertido: menos educación, más riesgo)
                educacion_puntuacion = education_options.index(nivel_estudios) + 1
                if nivel_estudios == lang["none"]:
                    riesgo += 5
                elif nivel_estudios == lang["primary"]:
                    riesgo += 4
                elif nivel_estudios == lang["secondary"]:
                    riesgo += 3
                elif nivel_estudios == lang["university"]:
                    riesgo += 2
                elif nivel_estudios == lang["postgraduate"]:
                    riesgo += 1
                
                # Puntuación por consumo de sustancias (múltiples opciones)
                if lang["none_substance"] not in consumo_sustancias:
                    if lang["alcohol"] in consumo_sustancias:
                        riesgo += 1
                    if lang["tobacco"] in consumo_sustancias:
                        riesgo += 1
                    if lang["recreational"] in consumo_sustancias:
                        riesgo += 2
                    if lang["cocaine"] in consumo_sustancias or lang["heroin"] in consumo_sustancias:
                        riesgo += 3
                
                # Puntuación por antecedentes penales (múltiples opciones)
                if lang["none_criminal"] not in antecedentes_penales:
                    if lang["theft"] in antecedentes_penales:
                        riesgo += 2
                    if lang["homicide"] in antecedentes_penales:
                        riesgo += 3
                    if lang["gender_violence"] in antecedentes_penales:
                        riesgo += 3
                    if lang["terrorism"] in antecedentes_penales:
                        riesgo += 5
                
                # Puntuación por rasgos de personalidad (múltiples opciones)
                if lang["none_traits"] not in rasgos_personalidad:
                    if lang["paranoid"] in rasgos_personalidad:
                        riesgo += 2
                    if lang["antisocial"] in rasgos_personalidad:
                        riesgo += 3
                    if lang["sadomasochistic"] in rasgos_personalidad:
                        riesgo += 1
                    if lang["impulsive"] in rasgos_personalidad:
                        riesgo += 2
                    if lang["unstable"] in rasgos_personalidad:
                        riesgo += 3
                    if lang["dependent"] in rasgos_personalidad or lang["avoidant"] in rasgos_personalidad:
                        riesgo += 2
                
                # Determinar nivel de riesgo
                if riesgo >= 15:
                    nivel_riesgo = lang["high"]
                    color_riesgo = "red"
                    explicacion_riesgo = lang["high_explanation"]
                elif riesgo >= 8:
                    nivel_riesgo = lang["moderate"]
                    color_riesgo = "orange"
                    explicacion_riesgo = lang["moderate_explanation"]
                else:
                    nivel_riesgo = lang["low"]
                    color_riesgo = "green"
                    explicacion_riesgo = lang["low_explanation"]
                
                # Mostrar resultados
                st.subheader(f"{lang['risk_level']} ", anchor=False)
                st.markdown(f"<h3 style='color:{color_riesgo};'>{nivel_riesgo}</h3>", unsafe_allow_html=True)
                st.markdown(f"**{lang['explanation']}**: {explicacion_riesgo}")
                st.markdown(f"**{lang['evaluation_date']}** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                
                # Mostrar foto subida si existe
                if foto_subida is not None:
                    st.image(foto_subida, width=200, caption=nombre)
                
                # Mostrar recomendaciones según nivel de riesgo
                st.subheader(lang["recommendations"])
                
                # Recomendaciones terapéuticas
                st.markdown(f"**{lang['therapy_recs']}**:")
                if nivel_riesgo == lang["high"]:
                    st.markdown("- Terapia cognitivo-conductual intensiva (3 sesiones semanales)")
                    st.markdown("- Intervención psicosocial multidimensional")
                    st.markdown("- Terapia familiar sistémica")
                    st.markdown("- Tratamiento de trauma y estrés postraumático")
                elif nivel_riesgo == lang["moderate"]:
                    st.markdown("- Terapia cognitivo-conductual (1-2 sesiones semanales)")
                    st.markdown("- Terapia de grupo para manejo de ira y frustración")
                    st.markdown("- Entrenamiento en habilidades sociales")
                else:
                    st.markdown("- Terapia de apoyo (1 sesión quincenal)")
                    st.markdown("- Orientación vocacional")
                    st.markdown("- Desarrollo de habilidades de afrontamiento")
                
                # Recomendaciones farmacológicas
                st.markdown(f"**{lang['medication_recs']}**:")
                if nivel_riesgo == lang["high"]:
                    st.markdown("- Evaluación psiquiátrica urgente para valoración de tratamiento")
                    st.markdown("- Considerar antipsicóticos atípicos bajo estricta supervisión")
                    st.markdown("- Estabilizadores del ánimo según evaluación psiquiátrica")
                    st.markdown("- Tratamiento para adicciones si corresponde")
                elif nivel_riesgo == lang["moderate"]:
                    st.markdown("- Evaluación psiquiátrica para valoración")
                    st.markdown("- Considerar ansiolíticos de baja potencia para periodos cortos")
                    st.markdown("- Tratamiento para depresión o ansiedad si corresponde")
                else:
                    st.markdown("- No se recomienda medicación psiquiátrica salvo síntomas específicos")
                    st.markdown("- Evaluación de seguimiento cada 3 meses")
                
                # Terapias de reinserción
                st.markdown(f"**{lang['reintegration_recs']}**:")
                if nivel_riesgo == lang["high"]:
                    st.markdown("- Programa intensivo de desradicalización")
                    st.markdown("- Reinserción gradual con supervisión continua")
                    st.markdown("- Formación educativa o laboral en entorno controlado")
                    st.markdown("- Mentores especializados en desradicalización")
                elif nivel_riesgo == lang["moderate"]:
                    st.markdown("- Programa de integración comunitaria supervisada")
                    st.markdown("- Formación laboral y educativa")
                    st.markdown("- Desarrollo de red social positiva")
                else:
                    st.markdown("- Fomento de participación comunitaria")
                    st.markdown("- Programas de voluntariado")
                    st.markdown("- Apoyo en educación o empleo")
                
                # Medidas de prevención
                st.markdown(f"**{lang['prevention_recs']}**:")
                if nivel_riesgo == lang["high"]:
                    st.markdown("- Monitoreo constante por servicios de inteligencia")
                    st.markdown("- Restricción de acceso a internet y redes sociales")
                    st.markdown("- Control de desplazamientos y contactos")
                    st.markdown("- Evaluaciones de riesgo periódicas (semanal)")
                elif nivel_riesgo == lang["moderate"]:
                    st.markdown("- Seguimiento regular por servicios sociales")
                    st.markdown("- Monitoreo de actividad online")
                    st.markdown("- Evaluaciones de riesgo periódicas (mensual)")
                else:
                    st.markdown("- Seguimiento comunitario")
                    st.markdown("- Evaluación trimestral")
                
                # Medidas de urgencia (solo para riesgo alto)
                if nivel_riesgo == lang["high"]:
                    st.markdown(f"**{lang['urgent_measures']}**:")
                    st.markdown("- Notificación inmediata a unidades antiterroristas")
                    st.markdown("- Intervención psiquiátrica de urgencia si hay signos de crisis")
                    st.markdown("- Protocolo de contención en caso de riesgo inminente")
                
                # Actualizar el estado
                st.session_state['results_displayed'] = True
                
                # Botón para generar informe PDF
                if st.button(lang["generate_report"]):
                    try:
                        # Generar PDF utilizando FPDF
                        pdf_output = io.BytesIO()
                        pdf = FPDF()
                        pdf.add_page()
                        
                        # Título del documento
                        pdf.set_font('Arial', 'B', 16)
                        pdf.cell(200, 10, txt="BIAS - Behavioral Intelligence Analysis System", ln=True, align='C')
                        pdf.ln(10)
                        
                        # Información básica
                        pdf.set_font('Arial', '', 12)
                        pdf.cell(200, 10, txt=f"{lang['name']}: {nombre}", ln=True)
                        pdf.cell(200, 10, txt=f"{lang['id_number']}: {numero_id}", ln=True)
                        pdf.cell(200, 10, txt=f"{lang['age']}: {edad}", ln=True)
                        pdf.cell(200, 10, txt=f"{lang['gender']}: {genero}", ln=True)
                        pdf.cell(200, 10, txt=f"{lang['education']}: {nivel_estudios}", ln=True)
                        pdf.ln(5)
                        
                        # Resultados de la evaluación
                        pdf.set_font('Arial', 'B', 14)
                        pdf.cell(200, 10, txt=lang["results_section"], ln=True)
                        pdf.set_font('Arial', '', 12)
                        
                        # Nivel de riesgo
                        pdf.cell(200, 10, txt=f"{lang['risk_level']} {nivel_riesgo}", ln=True)
                        pdf.cell(200, 10, txt=f"{lang['evaluation_date']} {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
                        pdf.multi_cell(0, 10, txt=f"{lang['explanation']}: {explicacion_riesgo}")
                        pdf.ln(5)
                        
                        # Recomendaciones institucionales
                        pdf.set_font('Arial', 'B', 14)
                        pdf.cell(200, 10, txt=lang["recommendations"], ln=True)
                        
                        # Recomendaciones terapéuticas
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(200, 10, txt=f"{lang['therapy_recs']}", ln=True)
                        pdf.set_font('Arial', '', 11)
                        if nivel_riesgo == lang["high"]:
                            pdf.cell(200, 8, txt="- Terapia cognitivo-conductual intensiva (3 sesiones semanales)", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Ayuda a reestructurar patrones de pensamiento extremistas y facilita el desarrollo de nuevas formas de interpretación de la realidad.", align='L')
                            
                            pdf.cell(200, 8, txt="- Intervención psicosocial multidimensional", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Aborda factores familiares, sociales y personales que contribuyen a la radicalización, proporcionando apoyo integral.", align='L')
                            
                            pdf.cell(200, 8, txt="- Terapia familiar sistémica", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Trabaja con el entorno familiar para modificar dinámicas disfuncionales que pueden reforzar comportamientos extremistas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Tratamiento de trauma y estrés postraumático", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: El trauma no resuelto es un factor significativo en procesos de radicalización; su tratamiento reduce vulnerabilidad.", align='L')
                        elif nivel_riesgo == lang["moderate"]:
                            pdf.cell(200, 8, txt="- Terapia cognitivo-conductual (1-2 sesiones semanales)", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Permite identificar y modificar pensamientos distorsionados que predisponen a la radicalización, desarrollando estrategias adaptativas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Terapia de grupo para manejo de ira y frustración", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: La ira mal gestionada es precursora de comportamientos violentos; el abordaje grupal proporciona modelos positivos de regulación emocional.", align='L')
                            
                            pdf.cell(200, 8, txt="- Entrenamiento en habilidades sociales", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Fortalece competencias para integrarse en grupos sociales positivos, reduciendo la búsqueda de pertenencia en grupos extremistas.", align='L')
                        else:
                            pdf.cell(200, 8, txt="- Terapia de apoyo (1 sesión quincenal)", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Brinda espacio de escucha y acompañamiento, fortaleciendo factores protectores y previniendo escalada de factores de riesgo.", align='L')
                            
                            pdf.cell(200, 8, txt="- Orientación vocacional", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: La falta de propósito vital puede ser factor de riesgo; la orientación proporciona objetivos constructivos y sentido de pertenencia social.", align='L')
                            
                            pdf.cell(200, 8, txt="- Desarrollo de habilidades de afrontamiento", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Mejora la gestión del estrés y frustración, evitando respuestas impulsivas frente a situaciones adversas.", align='L')
                        
                        # Recomendaciones farmacológicas
                        pdf.ln(5)
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(200, 10, txt=f"{lang['medication_recs']}", ln=True)
                        pdf.set_font('Arial', '', 11)
                        if nivel_riesgo == lang["high"]:
                            pdf.cell(200, 8, txt="- Evaluación psiquiátrica urgente para valoración de tratamiento", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Permite identificar condiciones psiquiátricas que pueden exacerbar ideación extremista y determinar necesidades farmacológicas específicas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Considerar antipsicóticos atípicos bajo estricta supervisión", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: En casos de pensamiento paranoide o psicótico, estos fármacos pueden estabilizar el pensamiento y reducir la interpretación distorsionada de la realidad.", align='L')
                            
                            pdf.cell(200, 8, txt="- Estabilizadores del ánimo según evaluación psiquiátrica", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: La inestabilidad emocional puede precipitar actos impulsivos violentos; estos medicamentos ayudan a regular las fluctuaciones anímicas extremas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Tratamiento para adicciones si corresponde", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: El consumo de sustancias reduce el autocontrol y puede catalizar comportamientos extremistas; su tratamiento mejora la estabilidad general.", align='L')
                        elif nivel_riesgo == lang["moderate"]:
                            pdf.cell(200, 8, txt="- Evaluación psiquiátrica para valoración", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Permite descartar trastornos psiquiátricos subyacentes que podrían intensificar la vulnerabilidad a ideologías extremistas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Considerar ansiolíticos de baja potencia para periodos cortos", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: La ansiedad elevada puede aumentar la rigidez cognitiva y la polarización; su manejo farmacológico puede facilitar la apertura a intervenciones psicoterapéuticas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Tratamiento para depresión o ansiedad si corresponde", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Estos trastornos pueden intensificar sentimientos de desesperanza o injusticia que facilitan la radicalización ideológica.", align='L')
                        else:
                            pdf.cell(200, 8, txt="- No se recomienda medicación psiquiátrica salvo síntomas específicos", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: En casos de bajo riesgo, los efectos secundarios de medicaciones pueden superar los beneficios; las intervenciones psicosociales suelen ser suficientes.", align='L')
                            
                            pdf.cell(200, 8, txt="- Evaluación de seguimiento cada 3 meses", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Permite monitorizar la evolución y detectar precozmente cualquier signo de empeoramiento que requiera intervención farmacológica.", align='L')
                        
                        # Terapias de reinserción
                        pdf.ln(5)
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(200, 10, txt=f"{lang['reintegration_recs']}", ln=True)
                        pdf.set_font('Arial', '', 11)
                        if nivel_riesgo == lang["high"]:
                            pdf.cell(200, 8, txt="- Programa intensivo de desradicalización", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Los programas específicos de desradicalización abordan directamente las creencias extremistas y proporcionan alternativas ideológicas coherentes.", align='L')
                            
                            pdf.cell(200, 8, txt="- Reinserción gradual con supervisión continua", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: El proceso escalonado permite la adaptación progresiva, reduciendo el riesgo de recaída mientras se mantiene control sobre factores de riesgo.", align='L')
                            
                            pdf.cell(200, 8, txt="- Formación educativa o laboral en entorno controlado", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Proporciona estructuración diaria, desarrollo de competencias y sentido de propósito, elementos protectores contra la radicalización.", align='L')
                            
                            pdf.cell(200, 8, txt="- Mentores especializados en desradicalización", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: La figura del mentor ofrece modelo alternativo de identificación y acompañamiento personalizado, crucial en procesos de cambio ideológico.", align='L')
                        elif nivel_riesgo == lang["moderate"]:
                            pdf.cell(200, 8, txt="- Programa de integración comunitaria supervisada", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Facilita la conexión con la comunidad general, diluyendo la influencia de grupos extremistas y ofreciendo sentido de pertenencia alternativo.", align='L')
                            
                            pdf.cell(200, 8, txt="- Formación laboral y educativa", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Incrementa oportunidades de desarrollo personal y profesional, reduciendo la vulnerabilidad a narrativas extremistas basadas en la marginación.", align='L')
                            
                            pdf.cell(200, 8, txt="- Desarrollo de red social positiva", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Las relaciones sociales saludables constituyen un factor protector fundamental contra la influencia de grupos extremistas.", align='L')
                        else:
                            pdf.cell(200, 8, txt="- Fomento de participación comunitaria", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Fortalece el sentido de pertenencia social y la identificación con valores compartidos, reduciendo la probabilidad de aislamiento.", align='L')
                            
                            pdf.cell(200, 8, txt="- Programas de voluntariado", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Promueve la empatía y conexión con otros, desarrollando perspectivas incompatibles con ideologías extremistas y violentas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Apoyo en educación o empleo", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Facilita integración social normalizada y desarrollo de proyecto vital constructivo que reduce vulnerabilidad a radicalización.", align='L')
                        
                        # Medidas de prevención
                        pdf.ln(5)
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(200, 10, txt=f"{lang['prevention_recs']}", ln=True)
                        pdf.set_font('Arial', '', 11)
                        if nivel_riesgo == lang["high"]:
                            pdf.cell(200, 8, txt="- Monitoreo constante por servicios de inteligencia", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: La supervisión especializada permite detectar comunicaciones o comportamientos indicativos de preparación para actos violentos.", align='L')
                            
                            pdf.cell(200, 8, txt="- Restricción de acceso a internet y redes sociales", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Limita la exposición a propaganda extremista y reduce posibilidades de contacto con agentes radicalizadores online.", align='L')
                            
                            pdf.cell(200, 8, txt="- Control de desplazamientos y contactos", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Evita el acceso a zonas de riesgo y el contacto con individuos vinculados a grupos extremistas que pueden reforzar la ideología violenta.", align='L')
                            
                            pdf.cell(200, 8, txt="- Evaluaciones de riesgo periódicas (semanal)", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Permite ajustar intervenciones según evolución del caso y detectar precozmente señales de escalada en la radicalización.", align='L')
                        elif nivel_riesgo == lang["moderate"]:
                            pdf.cell(200, 8, txt="- Seguimiento regular por servicios sociales", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Proporciona apoyo profesional continuado y detección temprana de factores de vulnerabilidad social que pueden intensificar el riesgo.", align='L')
                            
                            pdf.cell(200, 8, txt="- Monitoreo de actividad online", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Permite identificar búsquedas o interacciones relacionadas con contenido extremista que indicarían progresión en el proceso de radicalización.", align='L')
                            
                            pdf.cell(200, 8, txt="- Evaluaciones de riesgo periódicas (mensual)", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Facilita el seguimiento sistemático y ajuste de intervenciones según evolución, manteniendo continuidad en la evaluación.", align='L')
                        else:
                            pdf.cell(200, 8, txt="- Seguimiento comunitario", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Aprovecha los recursos naturales del entorno social para mantener niveles básicos de supervisión no intrusiva.", align='L')
                            
                            pdf.cell(200, 8, txt="- Evaluación trimestral", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Permite mantener contacto profesional periódico para valorar estabilidad y detectar cambios significativos antes de que escalen.", align='L')
                        
                        # Medidas de urgencia (solo para riesgo alto)
                        if nivel_riesgo == lang["high"]:
                            pdf.ln(5)
                            pdf.set_font('Arial', 'B', 12)
                            pdf.cell(200, 10, txt=f"{lang['urgent_measures']}", ln=True)
                            pdf.set_font('Arial', '', 11)
                            pdf.cell(200, 8, txt="- Notificación inmediata a unidades antiterroristas", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Activa protocolos de seguridad nacional ante riesgo inminente, asegurando intervención coordinada de fuerzas especializadas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Intervención psiquiátrica de urgencia si hay signos de crisis", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Los estados de descompensación psiquiátrica pueden precipitar actos violentos impulsivos; la intervención rápida puede prevenir escaladas críticas.", align='L')
                            
                            pdf.cell(200, 8, txt="- Protocolo de contención en caso de riesgo inminente", ln=True)
                            pdf.multi_cell(0, 8, txt="  Justificación: Establece procedimientos estandarizados de respuesta inmediata que minimizan riesgos para el sujeto y la comunidad en situaciones críticas.", align='L')
                        
                        # Valor total de riesgo (para usarse en los gráficos)
                        riesgo_total = riesgo
                        
                        # Añadir gráficos de puntuación
                        pdf.ln(10)
                        pdf.set_font('Arial', 'B', 14)
                        pdf.cell(200, 10, txt="Gráficos de Riesgo", ln=True, align='C')
                        pdf.ln(5)
                        
                        # Gráfico 1: Probabilidad de Radicalización
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(200, 10, txt="Probabilidad de Radicalización", ln=True)
                        
                        # Crear escala visual para probabilidad de radicalización
                        pdf.set_fill_color(255, 255, 255)  # Fondo blanco
                        pdf.rect(20, pdf.get_y(), 170, 20, style='DF')
                        
                        # Calcular probabilidad en base al riesgo total (0-100%)
                        probabilidad_radicalizacion = min(100, (riesgo_total / 30) * 100)
                        ancho_barra = (probabilidad_radicalizacion / 100) * 170
                        
                        # Determinar color según nivel de probabilidad
                        if probabilidad_radicalizacion >= 70:
                            pdf.set_fill_color(255, 0, 0)  # Rojo para alta probabilidad
                        elif probabilidad_radicalizacion >= 40:
                            pdf.set_fill_color(255, 165, 0)  # Naranja para probabilidad media
                        else:
                            pdf.set_fill_color(0, 128, 0)  # Verde para baja probabilidad
                        
                        # Dibujar la barra de probabilidad
                        pdf.rect(20, pdf.get_y(), ancho_barra, 20, style='F')
                        
                        # Añadir porcentaje
                        pdf.set_xy(20, pdf.get_y())
                        pdf.set_text_color(0, 0, 0)  # Texto negro
                        pdf.set_font('Arial', 'B', 10)
                        pdf.cell(170, 20, txt=f"{probabilidad_radicalizacion:.1f}%", align='C')
                        
                        # Mover abajo para el siguiente gráfico
                        pdf.ln(25)
                        
                        # Gráfico 2: Nivel de Peligro
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(200, 10, txt="Nivel de Peligro", ln=True)
                        
                        # Calcular puntuación de sustancias para el PDF
                        puntuacion_sustancias = 0
                        if "Alcohol" in consumo_sustancias:
                            puntuacion_sustancias += 1
                        if "Tabaco" in consumo_sustancias:
                            puntuacion_sustancias += 1
                        if "Drogas recreativas" in consumo_sustancias:
                            puntuacion_sustancias += 2
                        if "Cocaína" in consumo_sustancias or "Heroína" in consumo_sustancias:
                            puntuacion_sustancias += 3
                        
                        # Calcular puntuación de antecedentes para el PDF
                        puntuacion_antecedentes = 0
                        if "Robo" in antecedentes_penales:
                            puntuacion_antecedentes += 2
                        if "Homicidio" in antecedentes_penales:
                            puntuacion_antecedentes += 3
                        if "Violencia de género" in antecedentes_penales:
                            puntuacion_antecedentes += 3
                        if "Terrorismo" in antecedentes_penales:
                            puntuacion_antecedentes += 5
                        
                        # Calcular puntuación de personalidad para el PDF
                        puntuacion_personalidad = 0
                        if "Paranoide" in rasgos_personalidad:
                            puntuacion_personalidad += 2
                        if "Antisocial" in rasgos_personalidad:
                            puntuacion_personalidad += 3
                        if "Sadomasoquista" in rasgos_personalidad:
                            puntuacion_personalidad += 1
                        if "Impulsivo" in rasgos_personalidad:
                            puntuacion_personalidad += 2
                        if "Emocionalmente inestable" in rasgos_personalidad:
                            puntuacion_personalidad += 3
                        if "Dependiente" in rasgos_personalidad or "Evitativo" in rasgos_personalidad:
                            puntuacion_personalidad += 2
                        
                        # El valor total de riesgo ya fue definido anteriormente
                            
                        # Determinar nivel de peligro según puntuación de rasgos de personalidad y antecedentes
                        nivel_peligro = (puntuacion_personalidad + puntuacion_antecedentes) / 2
                        max_peligro = 10  # Valor máximo posible para la escala
                        porcentaje_peligro = min(100, (nivel_peligro / max_peligro) * 100)
                        
                        # Dibujar escala de peligro
                        pdf.set_fill_color(255, 255, 255)  # Fondo blanco
                        pdf.rect(20, pdf.get_y(), 170, 20, style='DF')
                        
                        # Determinar color según nivel de peligro
                        if porcentaje_peligro >= 70:
                            pdf.set_fill_color(255, 0, 0)  # Rojo para alto peligro
                        elif porcentaje_peligro >= 40:
                            pdf.set_fill_color(255, 165, 0)  # Naranja para peligro medio
                        else:
                            pdf.set_fill_color(0, 128, 0)  # Verde para bajo peligro
                        
                        # Dibujar la barra de peligro
                        ancho_barra_peligro = (porcentaje_peligro / 100) * 170
                        pdf.rect(20, pdf.get_y(), ancho_barra_peligro, 20, style='F')
                        
                        # Añadir etiqueta de nivel
                        pdf.set_xy(20, pdf.get_y())
                        pdf.set_text_color(0, 0, 0)  # Texto negro
                        pdf.set_font('Arial', 'B', 10)
                        
                        if porcentaje_peligro >= 70:
                            etiqueta_peligro = "ALTO"
                        elif porcentaje_peligro >= 40:
                            etiqueta_peligro = "MEDIO"
                        else:
                            etiqueta_peligro = "BAJO"
                            
                        pdf.cell(170, 20, txt=f"{etiqueta_peligro} ({porcentaje_peligro:.1f}%)", align='C')
                        
                        pdf.ln(25)
                        
                        # Guardar el PDF en memoria usando BytesIO
                        pdf_data = pdf.output(dest='S').encode('latin-1')  # 'S' means return as string
                        pdf_output.write(pdf_data)
                        
                        # Hacer que el archivo esté disponible para descargar
                        pdf_output.seek(0)  # Resetear el puntero del archivo
                        st.download_button(
                            label=lang["download_report"],
                            data=pdf_output,
                            file_name="Informe_BIAS.pdf",
                            mime="application/pdf"
                        )
                        
                        # Si el usuario es director, generar el informe detallado
                        if st.session_state['rol_usuario'] == 'director':
                            pdf_detallado = io.BytesIO()
                            pdf_det = FPDF()
                            pdf_det.add_page()
                            
                            # Título del informe detallado
                            pdf_det.set_font('Arial', 'B', 16)
                            pdf_det.cell(200, 10, txt=lang["scoring_report"], ln=True, align='C')
                            pdf_det.ln(10)
                            
                            # Información básica
                            pdf_det.set_font('Arial', '', 12)
                            pdf_det.cell(200, 10, txt=f"{lang['evaluation_date']} {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
                            pdf_det.cell(200, 10, txt=f"{lang['age']}: {edad}", ln=True)
                            pdf_det.cell(200, 10, txt=f"{lang['gender']}: {genero}", ln=True)
                            
                            # Añadir nuevos campos al informe detallado
                            if diagnosticos_previos:
                                pdf_det.cell(200, 10, txt=f"{lang['diagnosis_list']}: {', '.join(diagnosticos_previos)}", ln=True)
                            
                            pdf_det.cell(200, 10, txt=f"{lang['previous_therapies']}: {terapia_previa}", ln=True)
                            if fecha_inicio_terapia:
                                pdf_det.cell(200, 10, txt=f"{lang['therapy_date']}: {fecha_inicio_terapia}", ln=True)
                            
                            pdf_det.cell(200, 10, txt=f"{lang['alarm_date']}: {fecha_alarma}", ln=True)
                            
                            if motivo_interes:
                                pdf_det.multi_cell(0, 10, txt=f"{lang['interest_profile']}: {motivo_interes}")
                            
                            if antecedentes_extremismo:
                                pdf_det.multi_cell(0, 10, txt=f"{lang['family_extremism']}: {antecedentes_extremismo}")
                            
                            pdf_det.ln(5)
                            
                            # Sección de puntuación detallada
                            pdf_det.set_font('Arial', 'B', 14)
                            pdf_det.cell(200, 10, txt=lang["detailed_scoring"], ln=True)
                            pdf_det.set_font('Arial', '', 12)
                            
                            # Desglose de puntuación
                            pdf_det.cell(200, 10, txt=f"{lang['total_risk_score']}: {riesgo_total}", ln=True)
                            pdf_det.cell(200, 10, txt=f"{lang['education_score']}: {education_options.index(nivel_estudios) + 1}", ln=True)
                            
                            # Las puntuaciones ya se calcularon anteriormente para los gráficos
                            
                            pdf_det.cell(200, 10, txt=f"{lang['substances_score']}: {puntuacion_sustancias}", ln=True)
                            pdf_det.cell(200, 10, txt=f"{lang['criminal_score']}: {puntuacion_antecedentes}", ln=True)
                            pdf_det.cell(200, 10, txt=f"{lang['personality_score']}: {puntuacion_personalidad}", ln=True)
                            
                            # Detalles específicos de cada categoría
                            pdf_det.ln(5)
                            pdf_det.set_font('Arial', 'B', 12)
                            pdf_det.cell(200, 10, txt=f"{lang['substances']}: ", ln=True)
                            pdf_det.set_font('Arial', '', 11)
                            for sustancia in consumo_sustancias:
                                puntos = 0
                                if sustancia == "Alcohol" or sustancia == "Tabaco":
                                    puntos = 1
                                elif sustancia == "Drogas recreativas":
                                    puntos = 2
                                elif sustancia == "Cocaína" or sustancia == "Heroína":
                                    puntos = 3
                                pdf_det.cell(200, 8, txt=f"- {sustancia}: {puntos} puntos", ln=True)
                            
                            pdf_det.ln(5)
                            pdf_det.set_font('Arial', 'B', 12)
                            pdf_det.cell(200, 10, txt=f"{lang['criminal_record']}: ", ln=True)
                            pdf_det.set_font('Arial', '', 11)
                            for antecedente in antecedentes_penales:
                                puntos = 0
                                if antecedente == "Robo":
                                    puntos = 2
                                elif antecedente == "Homicidio" or antecedente == "Violencia de género":
                                    puntos = 3
                                elif antecedente == "Terrorismo":
                                    puntos = 5
                                pdf_det.cell(200, 8, txt=f"- {antecedente}: {puntos} puntos", ln=True)
                            
                            pdf_det.ln(5)
                            pdf_det.set_font('Arial', 'B', 12)
                            pdf_det.cell(200, 10, txt=f"{lang['personality_traits']}: ", ln=True)
                            pdf_det.set_font('Arial', '', 11)
                            for rasgo in rasgos_personalidad:
                                puntos = 0
                                if rasgo == "Paranoide" or rasgo == "Impulsivo":
                                    puntos = 2
                                elif rasgo == "Antisocial" or rasgo == "Emocionalmente inestable":
                                    puntos = 3
                                elif rasgo == "Sadomasoquista":
                                    puntos = 1
                                elif rasgo == "Dependiente" or rasgo == "Evitativo":
                                    puntos = 2
                                pdf_det.cell(200, 8, txt=f"- {rasgo}: {puntos} puntos", ln=True)
                            
                            # Añadir la sección de recomendaciones al informe detallado
                            pdf_det.ln(5)
                            pdf_det.set_font('Arial', 'B', 14)
                            pdf_det.cell(200, 10, txt=lang["recommendations"], ln=True)
                            
                            # Recomendaciones terapéuticas
                            pdf_det.set_font('Arial', 'B', 12)
                            pdf_det.cell(200, 10, txt=f"{lang['therapy_recs']}", ln=True)
                            pdf_det.set_font('Arial', '', 11)
                            if nivel_riesgo == lang["high"]:
                                pdf_det.cell(200, 8, txt="- Terapia cognitivo-conductual intensiva (3 sesiones semanales)", ln=True)
                                pdf_det.cell(200, 8, txt="- Intervención psicosocial multidimensional", ln=True)
                                pdf_det.cell(200, 8, txt="- Terapia familiar sistémica", ln=True)
                                pdf_det.cell(200, 8, txt="- Tratamiento de trauma y estrés postraumático", ln=True)
                            elif nivel_riesgo == lang["moderate"]:
                                pdf_det.cell(200, 8, txt="- Terapia cognitivo-conductual (1-2 sesiones semanales)", ln=True)
                                pdf_det.cell(200, 8, txt="- Terapia de grupo para manejo de ira y frustración", ln=True)
                                pdf_det.cell(200, 8, txt="- Entrenamiento en habilidades sociales", ln=True)
                            else:
                                pdf_det.cell(200, 8, txt="- Terapia de apoyo (1 sesión quincenal)", ln=True)
                                pdf_det.cell(200, 8, txt="- Orientación vocacional", ln=True)
                                pdf_det.cell(200, 8, txt="- Desarrollo de habilidades de afrontamiento", ln=True)
                            
                            # Recomendaciones farmacológicas
                            pdf_det.ln(5)
                            pdf_det.set_font('Arial', 'B', 12)
                            pdf_det.cell(200, 10, txt=f"{lang['medication_recs']}", ln=True)
                            pdf_det.set_font('Arial', '', 11)
                            if nivel_riesgo == lang["high"]:
                                pdf_det.cell(200, 8, txt="- Evaluación psiquiátrica urgente para valoración de tratamiento", ln=True)
                                pdf_det.cell(200, 8, txt="- Considerar antipsicóticos atípicos bajo estricta supervisión", ln=True)
                                pdf_det.cell(200, 8, txt="- Estabilizadores del ánimo según evaluación psiquiátrica", ln=True)
                                pdf_det.cell(200, 8, txt="- Tratamiento para adicciones si corresponde", ln=True)
                            elif nivel_riesgo == lang["moderate"]:
                                pdf_det.cell(200, 8, txt="- Evaluación psiquiátrica para valoración", ln=True)
                                pdf_det.cell(200, 8, txt="- Considerar ansiolíticos de baja potencia para periodos cortos", ln=True)
                                pdf_det.cell(200, 8, txt="- Tratamiento para depresión o ansiedad si corresponde", ln=True)
                            else:
                                pdf_det.cell(200, 8, txt="- No se recomienda medicación psiquiátrica salvo síntomas específicos", ln=True)
                                pdf_det.cell(200, 8, txt="- Evaluación de seguimiento cada 3 meses", ln=True)
                            
                            # Terapias de reinserción
                            pdf_det.ln(5)
                            pdf_det.set_font('Arial', 'B', 12)
                            pdf_det.cell(200, 10, txt=f"{lang['reintegration_recs']}", ln=True)
                            pdf_det.set_font('Arial', '', 11)
                            if nivel_riesgo == lang["high"]:
                                pdf_det.cell(200, 8, txt="- Programa intensivo de desradicalización", ln=True)
                                pdf_det.cell(200, 8, txt="- Reinserción gradual con supervisión continua", ln=True)
                                pdf_det.cell(200, 8, txt="- Formación educativa o laboral en entorno controlado", ln=True)
                                pdf_det.cell(200, 8, txt="- Mentores especializados en desradicalización", ln=True)
                            elif nivel_riesgo == lang["moderate"]:
                                pdf_det.cell(200, 8, txt="- Programa de integración comunitaria supervisada", ln=True)
                                pdf_det.cell(200, 8, txt="- Formación laboral y educativa", ln=True)
                                pdf_det.cell(200, 8, txt="- Desarrollo de red social positiva", ln=True)
                            else:
                                pdf_det.cell(200, 8, txt="- Fomento de participación comunitaria", ln=True)
                                pdf_det.cell(200, 8, txt="- Programas de voluntariado", ln=True)
                                pdf_det.cell(200, 8, txt="- Apoyo en educación o empleo", ln=True)
                            
                            # Medidas de prevención
                            pdf_det.ln(5)
                            pdf_det.set_font('Arial', 'B', 12)
                            pdf_det.cell(200, 10, txt=f"{lang['prevention_recs']}", ln=True)
                            pdf_det.set_font('Arial', '', 11)
                            if nivel_riesgo == lang["high"]:
                                pdf_det.cell(200, 8, txt="- Monitoreo constante por servicios de inteligencia", ln=True)
                                pdf_det.cell(200, 8, txt="- Restricción de acceso a internet y redes sociales", ln=True)
                                pdf_det.cell(200, 8, txt="- Control de desplazamientos y contactos", ln=True)
                                pdf_det.cell(200, 8, txt="- Evaluaciones de riesgo periódicas (semanal)", ln=True)
                            elif nivel_riesgo == lang["moderate"]:
                                pdf_det.cell(200, 8, txt="- Seguimiento regular por servicios sociales", ln=True)
                                pdf_det.cell(200, 8, txt="- Monitoreo de actividad online", ln=True)
                                pdf_det.cell(200, 8, txt="- Evaluaciones de riesgo periódicas (mensual)", ln=True)
                            else:
                                pdf_det.cell(200, 8, txt="- Seguimiento comunitario", ln=True)
                                pdf_det.cell(200, 8, txt="- Evaluación trimestral", ln=True)
                            
                            # Medidas de urgencia (solo para riesgo alto)
                            if nivel_riesgo == lang["high"]:
                                pdf_det.ln(5)
                                pdf_det.set_font('Arial', 'B', 12)
                                pdf_det.cell(200, 10, txt=f"{lang['urgent_measures']}", ln=True)
                                pdf_det.set_font('Arial', '', 11)
                                pdf_det.cell(200, 8, txt="- Notificación inmediata a unidades antiterroristas", ln=True)
                                pdf_det.cell(200, 8, txt="- Intervención psiquiátrica de urgencia si hay signos de crisis", ln=True)
                                pdf_det.cell(200, 8, txt="- Protocolo de contención en caso de riesgo inminente", ln=True)
                            
                            # Guardar el PDF detallado en memoria
                            pdf_det_data = pdf_det.output(dest='S').encode('latin-1')
                            pdf_detallado.write(pdf_det_data)
                            
                            # Hacer que el archivo detallado esté disponible para descargar
                            pdf_detallado.seek(0)
                            st.download_button(
                                label=lang["download_detailed"],
                                data=pdf_detallado,
                                file_name="Informe_Detallado_BIAS.pdf",
                                mime="application/pdf",
                                key="download_detailed"
                            )
                    except Exception as e:
                        st.error(f"Error al generar el PDF: {e}")
                        
                        # Mensaje informativo sobre la limitación de caracteres no latinos
                        if st.session_state['idioma'] == "Árabe":
                            st.info("Nota: La generación de PDFs con caracteres árabes puede requerir configuración adicional. El PDF generado podría no mostrar correctamente todos los caracteres.")
else:
    # Mostrar mensaje de bienvenida cuando no se ha iniciado sesión
    st.markdown(f"### {lang['welcome']}")
    st.info(f"{lang['login']} para acceder al sistema.")
