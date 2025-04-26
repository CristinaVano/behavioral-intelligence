import streamlit as st
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io
import os

# Configurar la app
st.set_page_config(page_title="BIAS – Prevención del Terrorismo", page_icon="🔒", layout="centered")

# Traducción de textos según el idioma
translations = {
    "Español": {
        "title": "BIAS – Prevención del Terrorismo",
        "subtitle": "Evaluación de Riesgo de Radicalización",
        "instructions": "Por favor, completa el siguiente formulario para generar el informe preliminar de riesgo.",
        "login": "Entrar",
        "username": "Usuario",
        "password": "Contraseña",
        "access_granted": "¡Acceso permitido! Bienvenido/a.",
        "access_denied": "Usuario o contraseña incorrectos.",
        "age": "Edad",
        "gender": "Género",
        "education": "Nivel de estudios",
        "substances": "Consumo de sustancias",
        "country": "País de origen",
        "city": "Ciudad de origen",
        "criminal_record": "Antecedentes penales",
        "personality_traits": "Rasgos de personalidad",
        "psychological_profile": "Perfil psicológico completo",
        "medical_history": "Historial clínico completo",
        "additional_comments": "Comentarios adicionales",
        "generate_report": "Generar Informe",
        "report_success": "Informe generado correctamente.",
        "report_header": "🔒 Informe Preliminar de Riesgo",
        "evaluation_date": "Fecha de evaluación:",
        "risk_level": "Nivel de riesgo de radicalización:",
        "preliminary_notes": "Notas preliminares:",
        "high_risk": "Se recomienda activación de protocolo de vigilancia intensiva y notificación a unidades de inteligencia.",
        "moderate_risk": "Se recomienda seguimiento regular y evaluación psicológica especializada.",
        "low_risk": "Seguimiento habitual. Reevaluar en caso de cambios de conducta.",
        "recommendations": "Recomendaciones para las instituciones",
        "therapy_recs": "Recomendaciones terapéuticas",
        "medication_recs": "Recomendaciones farmacológicas",
        "reintegration_recs": "Terapias de reinserción",
        "prevention_recs": "Medidas de prevención",
        "urgent_measures": "Medidas de urgencia",
        "download_report": "Descargar Informe PDF",
        "male": "Masculino",
        "female": "Femenino",
        "other": "Otro",
        "prefer_not_to_say": "Prefiero no decirlo",
        "secondary": "Secundaria",
        "high_school": "Bachillerato",
        "bachelor": "Grado",
        "master": "Máster",
        "phd": "Doctorado",
        "high": "ALTO",
        "moderate": "MODERADO",
        "low": "BAJO"
    },
    "Inglés": {
        "title": "BIAS – Terrorism Prevention",
        "subtitle": "Radicalization Risk Assessment",
        "instructions": "Please fill in the form below to generate the preliminary risk report.",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "access_granted": "Access granted! Welcome.",
        "access_denied": "Incorrect username or password.",
        "age": "Age",
        "gender": "Gender",
        "education": "Education Level",
        "substances": "Substance Use",
        "country": "Country of Origin",
        "city": "City of Origin",
        "criminal_record": "Criminal Record",
        "personality_traits": "Personality Traits",
        "psychological_profile": "Complete Psychological Profile",
        "medical_history": "Complete Medical History",
        "additional_comments": "Additional Comments",
        "generate_report": "Generate Report",
        "report_success": "Report successfully generated.",
        "report_header": "🔒 Preliminary Risk Report",
        "evaluation_date": "Evaluation Date:",
        "risk_level": "Radicalization Risk Level:",
        "preliminary_notes": "Preliminary Notes:",
        "high_risk": "Activation of intensive surveillance protocol and notification to intelligence units is recommended.",
        "moderate_risk": "Regular follow-up and specialized psychological evaluation is recommended.",
        "low_risk": "Routine follow-up. Reassess in case of behavioral changes.",
        "recommendations": "Recommendations for institutions",
        "therapy_recs": "Therapeutic recommendations",
        "medication_recs": "Pharmacological recommendations",
        "reintegration_recs": "Reintegration therapies",
        "prevention_recs": "Prevention measures",
        "urgent_measures": "Urgent measures",
        "download_report": "Download PDF Report",
        "male": "Male",
        "female": "Female",
        "other": "Other",
        "prefer_not_to_say": "Prefer not to say",
        "secondary": "Secondary",
        "high_school": "High School",
        "bachelor": "Bachelor's Degree",
        "master": "Master's Degree",
        "phd": "PhD",
        "high": "HIGH",
        "moderate": "MODERATE",
        "low": "LOW"
    },
    "Árabe": {
        "title": "بياس - منع الإرهاب",
        "subtitle": "تقييم مخاطر التطرف",
        "instructions": "يرجى ملء النموذج أدناه لإنشاء التقرير الأولي للمخاطر.",
        "login": "تسجيل الدخول",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "access_granted": "تم منح حق الوصول! مرحبًا.",
        "access_denied": "اسم المستخدم أو كلمة المرور غير صحيحة.",
        "age": "العمر",
        "gender": "الجنس",
        "education": "المستوى التعليمي",
        "substances": "استخدام المواد",
        "country": "بلد المنشأ",
        "city": "مدينة المنشأ",
        "criminal_record": "السجل الجنائي",
        "personality_traits": "سمات الشخصية",
        "psychological_profile": "الملف النفسي الكامل",
        "medical_history": "التاريخ الطبي الكامل",
        "additional_comments": "تعليقات إضافية",
        "generate_report": "إنشاء التقرير",
        "report_success": "تم إنشاء التقرير بنجاح.",
        "report_header": "🔒 تقرير المخاطر الأولي",
        "evaluation_date": "تاريخ التقييم:",
        "risk_level": "مستوى خطر التطرف:",
        "preliminary_notes": "ملاحظات أولية:",
        "high_risk": "يوصى بتفعيل بروتوكول المراقبة المكثفة وإخطار وحدات الاستخبارات.",
        "moderate_risk": "يوصى بالمتابعة المنتظمة والتقييم النفسي المتخصص.",
        "low_risk": "متابعة روتينية. إعادة التقييم في حالة حدوث تغييرات سلوكية.",
        "recommendations": "توصيات للمؤسسات",
        "therapy_recs": "توصيات علاجية",
        "medication_recs": "توصيات دوائية",
        "reintegration_recs": "علاجات إعادة الإدماج",
        "prevention_recs": "تدابير الوقاية",
        "urgent_measures": "تدابير عاجلة",
        "download_report": "تنزيل تقرير PDF",
        "male": "ذكر",
        "female": "أنثى",
        "other": "آخر",
        "prefer_not_to_say": "أفضل عدم القول",
        "secondary": "ثانوي",
        "high_school": "المدرسة الثانوية",
        "bachelor": "درجة البكالوريوس",
        "master": "درجة الماجستير",
        "phd": "دكتوراه",
        "high": "عالي",
        "moderate": "متوسط",
        "low": "منخفض"
    },
    "Francés": {
        "title": "BIAS - Prévention du Terrorisme",
        "subtitle": "Évaluation des risques de radicalisation",
        "instructions": "Veuillez remplir le formulaire ci-dessous pour générer le rapport préliminaire sur les risques.",
        "login": "Connexion",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "access_granted": "Accès autorisé! Bienvenue.",
        "access_denied": "Nom d'utilisateur ou mot de passe incorrect.",
        "age": "Âge",
        "gender": "Genre",
        "education": "Niveau d'éducation",
        "substances": "Consommation de substances",
        "country": "Pays d'origine",
        "city": "Ville d'origine",
        "criminal_record": "Casier judiciaire",
        "personality_traits": "Traits de personnalité",
        "psychological_profile": "Profil psychologique complet",
        "medical_history": "Historique médical complet",
        "additional_comments": "Commentaires supplémentaires",
        "generate_report": "Générer le rapport",
        "report_success": "Rapport généré avec succès.",
        "report_header": "🔒 Rapport préliminaire des risques",
        "evaluation_date": "Date d'évaluation:",
        "risk_level": "Niveau de risque de radicalisation:",
        "preliminary_notes": "Notes préliminaires:",
        "high_risk": "L'activation du protocole de surveillance intensive et la notification aux unités de renseignement sont recommandées.",
        "moderate_risk": "Un suivi régulier et une évaluation psychologique spécialisée sont recommandés.",
        "low_risk": "Suivi de routine. Réévaluer en cas de changements de comportement.",
        "recommendations": "Recommandations pour les institutions",
        "therapy_recs": "Recommandations thérapeutiques",
        "medication_recs": "Recommandations pharmacologiques",
        "reintegration_recs": "Thérapies de réinsertion",
        "prevention_recs": "Mesures de prévention",
        "urgent_measures": "Mesures d'urgence",
        "download_report": "Télécharger le rapport PDF",
        "male": "Masculin",
        "female": "Féminin",
        "other": "Autre",
        "prefer_not_to_say": "Préfère ne pas dire",
        "secondary": "Secondaire",
        "high_school": "Lycée",
        "bachelor": "Licence",
        "master": "Master",
        "phd": "Doctorat",
        "high": "ÉLEVÉ",
        "moderate": "MODÉRÉ",
        "low": "FAIBLE"
    }
}

# Verificar si el archivo CSV de usuarios existe
if not os.path.exists('registros_perfiles.csv'):
    # Crear un DataFrame vacío con las columnas necesarias
    usuarios_df = pd.DataFrame({
        'Usuario': ['admin', 'usuario1', 'usuario2'],
        'Contraseña': ['admin123', 'password1', 'password2'],
        'Rol': ['administrador', 'evaluador', 'analista']
    })
    # Guardar el DataFrame en un archivo CSV
    usuarios_df.to_csv('registros_perfiles.csv', index=False)

# Inicialización de variables de sesión
if 'idioma' not in st.session_state:
    st.session_state['idioma'] = "Español"
if 'usuario_autenticado' not in st.session_state:
    st.session_state['usuario_autenticado'] = False
if 'usuario_actual' not in st.session_state:
    st.session_state['usuario_actual'] = None
if 'rol_usuario' not in st.session_state:
    st.session_state['rol_usuario'] = None  
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False
    st.session_state['form_data'] = {}

# Selección de idioma
idioma = st.selectbox("Selecciona tu idioma / Select your language / اختر لغتك / Sélectionnez votre langue", 
                    ("Español", "Inglés", "Árabe", "Francés"), 
                    index=list(["Español", "Inglés", "Árabe", "Francés"]).index(st.session_state['idioma']))

# Actualizar el idioma si ha cambiado
if idioma != st.session_state['idioma']:
    st.session_state['idioma'] = idioma
    st.rerun()

# Añadir traducciones para el informe detallado
if "scoring_report" not in translations["Español"]:
    translations["Español"]["scoring_report"] = "Informe Detallado de Puntuación"
    translations["Español"]["detailed_scoring"] = "Desglose detallado de la puntuación"
    translations["Español"]["total_risk_score"] = "Puntuación total de riesgo"
    translations["Español"]["education_score"] = "Puntuación por nivel educativo"
    translations["Español"]["substances_score"] = "Puntuación por consumo de sustancias"
    translations["Español"]["criminal_score"] = "Puntuación por antecedentes penales"
    translations["Español"]["personality_score"] = "Puntuación por rasgos de personalidad"
    translations["Español"]["download_detailed"] = "Descargar Informe Detallado"
    translations["Español"]["diagnosis_list"] = "Lista de diagnósticos previos"
    translations["Español"]["previous_therapies"] = "Terapias previas"
    translations["Español"]["therapy_yes"] = "Sí, ha recibido terapia"
    translations["Español"]["therapy_no"] = "No ha recibido terapia"
    translations["Español"]["therapy_date"] = "Fecha de inicio de terapia"
    translations["Español"]["alarm_signals"] = "Primeras señales de alarma"
    translations["Español"]["alarm_date"] = "Fecha de primeras señales"
    translations["Español"]["interest_profile"] = "Motivo de interés"
    translations["Español"]["upload_photo"] = "Subir fotografía"
    translations["Español"]["family_extremism"] = "Antecedentes familiares de extremismo"
    
    translations["Inglés"]["scoring_report"] = "Detailed Scoring Report"
    translations["Inglés"]["detailed_scoring"] = "Detailed score breakdown"
    translations["Inglés"]["total_risk_score"] = "Total risk score"
    translations["Inglés"]["education_score"] = "Education level score"
    translations["Inglés"]["substances_score"] = "Substance use score"
    translations["Inglés"]["criminal_score"] = "Criminal record score"
    translations["Inglés"]["personality_score"] = "Personality traits score"
    translations["Inglés"]["download_detailed"] = "Download Detailed Report"
    translations["Inglés"]["diagnosis_list"] = "Previous diagnosis list"
    translations["Inglés"]["previous_therapies"] = "Previous therapies"
    translations["Inglés"]["therapy_yes"] = "Yes, received therapy"
    translations["Inglés"]["therapy_no"] = "No therapy received"
    translations["Inglés"]["therapy_date"] = "Therapy start date"
    translations["Inglés"]["alarm_signals"] = "First alarm signals"
    translations["Inglés"]["alarm_date"] = "Date of first signals"
    translations["Inglés"]["interest_profile"] = "Reason for interest"
    translations["Inglés"]["upload_photo"] = "Upload photo"
    translations["Inglés"]["family_extremism"] = "Family history of extremism"
    
    translations["Árabe"]["scoring_report"] = "تقرير التسجيل المفصل"
    translations["Árabe"]["detailed_scoring"] = "تفصيل تفصيلي للنتيجة"
    translations["Árabe"]["total_risk_score"] = "مجموع نقاط الخطر"
    translations["Árabe"]["education_score"] = "درجة المستوى التعليمي"
    translations["Árabe"]["substances_score"] = "درجة تعاطي المواد"
    translations["Árabe"]["criminal_score"] = "درجة السجل الجنائي"
    translations["Árabe"]["personality_score"] = "درجة سمات الشخصية"
    translations["Árabe"]["download_detailed"] = "تنزيل التقرير المفصل"
    translations["Árabe"]["diagnosis_list"] = "قائمة التشخيصات السابقة"
    translations["Árabe"]["previous_therapies"] = "العلاجات السابقة"
    translations["Árabe"]["therapy_yes"] = "نعم، تلقى العلاج"
    translations["Árabe"]["therapy_no"] = "لم يتلق العلاج"
    translations["Árabe"]["therapy_date"] = "تاريخ بدء العلاج"
    translations["Árabe"]["alarm_signals"] = "إشارات الإنذار الأولى"
    translations["Árabe"]["alarm_date"] = "تاريخ الإشارات الأولى"
    translations["Árabe"]["interest_profile"] = "سبب الاهتمام"
    translations["Árabe"]["upload_photo"] = "تحميل الصورة"
    translations["Árabe"]["family_extremism"] = "تاريخ عائلي للتطرف"
    
    translations["Francés"]["scoring_report"] = "Rapport de Notation Détaillé"
    translations["Francés"]["detailed_scoring"] = "Répartition détaillée des scores"
    translations["Francés"]["total_risk_score"] = "Score de risque total"
    translations["Francés"]["education_score"] = "Score de niveau d'éducation"
    translations["Francés"]["substances_score"] = "Score de consommation de substances"
    translations["Francés"]["criminal_score"] = "Score de casier judiciaire"
    translations["Francés"]["personality_score"] = "Score de traits de personnalité"
    translations["Francés"]["download_detailed"] = "Télécharger le Rapport Détaillé"
    translations["Francés"]["diagnosis_list"] = "Liste des diagnostics antérieurs"
    translations["Francés"]["previous_therapies"] = "Thérapies antérieures"
    translations["Francés"]["therapy_yes"] = "Oui, a reçu une thérapie"
    translations["Francés"]["therapy_no"] = "Pas de thérapie reçue"
    translations["Francés"]["therapy_date"] = "Date de début de la thérapie"
    translations["Francés"]["alarm_signals"] = "Premiers signaux d'alarme"
    translations["Francés"]["alarm_date"] = "Date des premiers signaux"
    translations["Francés"]["interest_profile"] = "Raison de l'intérêt"
    translations["Francés"]["upload_photo"] = "Télécharger une photo"
    translations["Francés"]["family_extremism"] = "Antécédents familiaux d'extrémisme"

# Obtener traducciones para el idioma seleccionado
lang = translations[st.session_state['idioma']]

# Mostrar título y subtítulo según el idioma
st.title(lang["title"])
st.subheader(lang["subtitle"])
st.write(lang["instructions"])

# Cargar registros de usuarios
try:
    usuarios = pd.read_csv('registros_perfiles.csv')
except Exception as e:
    st.error(f"Error al cargar el archivo de usuarios: {e}")
    usuarios = pd.DataFrame({'Usuario': ['admin'], 'Contraseña': ['admin123'], 'Rol': ['administrador']})

# Formulario de login
if not st.session_state['usuario_autenticado']:
    with st.form(key='login_form'):
        usuario = st.text_input(lang["username"])
        contrasena = st.text_input(lang["password"], type="password")
        submit_login_button = st.form_submit_button(label=lang["login"])

        if submit_login_button:
            # Validar el usuario y contraseña
            if usuario in usuarios['Usuario'].values:
                contrasena_correcta = usuarios.loc[usuarios['Usuario'] == usuario, 'Contraseña'].values[0]
                if contrasena == contrasena_correcta:
                    st.session_state['usuario_autenticado'] = True
                    st.session_state['usuario_actual'] = usuario
                    # Obtener el rol del usuario actual
                    st.session_state['rol_usuario'] = usuarios.loc[usuarios['Usuario'] == usuario, 'Rol'].values[0]
                    st.success(lang["access_granted"])
                    st.rerun()
                else:
                    st.error(lang["access_denied"])
            else:
                st.error(lang["access_denied"])

# Si ya está autenticado, mostrar el formulario de evaluación
if st.session_state['usuario_autenticado']:
    # Mostrar información del usuario y rol
    st.sidebar.write(f"**Usuario:** {st.session_state['usuario_actual']}")
    st.sidebar.write(f"**Rol:** {st.session_state['rol_usuario']}")
    
    # Añadir botón de cierre de sesión
    if st.sidebar.button("Cerrar sesión"):
        for key in ['usuario_autenticado', 'usuario_actual', 'rol_usuario', 'form_submitted', 'form_data']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    # Formulario de evaluación
    with st.form(key='evaluation_form'):
        # Campos de la evaluación
        edad = st.slider(lang["age"], 12, 80, 25)
        
        genero_options = [lang["male"], lang["female"], lang["other"], lang["prefer_not_to_say"]]
        genero = st.selectbox(lang["gender"], genero_options)
        
        education_options = [lang["secondary"], lang["high_school"], lang["bachelor"], lang["master"], lang["phd"]]
        nivel_estudios = st.selectbox(lang["education"], education_options)
        
        consumo_sustancias = st.multiselect(lang["substances"], ("Alcohol", "Tabaco", "Drogas recreativas", "Cocaína", "Heroína"))
        
        pais_origen = st.text_input(lang["country"])
        ciudad_origen = st.text_input(lang["city"])
        
        antecedentes_penales = st.multiselect(lang["criminal_record"], 
            ["Robo", "Homicidio", "Fraude", "Extorsión", "Violencia de género", "Delitos informáticos", 
            "Vandalismo", "Acusaciones falsas", "Amenazas", "Violación", "Terrorismo", "Tráfico de drogas", 
            "Secuestro", "Delitos fiscales", "Blanqueo de dinero"])
        
        rasgos_personalidad = st.multiselect(lang["personality_traits"], 
            ["Paranoide", "Antisocial", "Sadomasoquista", "Impulsivo", "Emocionalmente inestable", 
            "Dependiente", "Evitativo"])

        # Lista de diagnósticos previos
        st.subheader(lang["diagnosis_list"])
        diagnosticos_previos = st.multiselect(lang["diagnosis_list"], 
            ["Esquizofrenia", "Trastorno bipolar", "Depresión mayor", "Trastorno límite de personalidad", 
            "Trastorno antisocial", "Ansiedad", "Paranoia", "Psicosis", "Trastorno obsesivo-compulsivo", 
            "Trastorno por estrés postraumático", "Adicción"])
        
        # Información sobre terapias previas
        st.subheader(lang["previous_therapies"])
        therapy_options = [lang["therapy_yes"], lang["therapy_no"]]
        terapia_previa = st.radio(lang["previous_therapies"], therapy_options)
        
        if terapia_previa == lang["therapy_yes"]:
            fecha_inicio_terapia = st.date_input(lang["therapy_date"], datetime.now() - pd.Timedelta(days=180))
        else:
            fecha_inicio_terapia = None
        
        # Fecha de primeras señales de alarma
        st.subheader(lang["alarm_signals"])
        fecha_alarma = st.date_input(lang["alarm_date"], datetime.now() - pd.Timedelta(days=90))
        
        # Motivo por el que es un perfil de interés
        motivo_interes = st.text_area(lang["interest_profile"])
        
        # Antecedentes familiares de extremismo
        antecedentes_extremismo = st.text_area(lang["family_extremism"])
        
        # Sección para subir una fotografía
        foto_sujeto = st.file_uploader(lang["upload_photo"], type=["jpg", "jpeg", "png"])
        
        # Sección de comentarios adicionales
        st.subheader(lang["additional_comments"])
        perfil_psicologico = st.text_area(lang["psychological_profile"])
        historial_clinico = st.text_area(lang["medical_history"])
        comentarios_adicionales = st.text_area(lang["additional_comments"])

        submit_evaluation_button = st.form_submit_button(label=lang["generate_report"])

        if submit_evaluation_button:
            # Cálculo del riesgo
            riesgo = 0
            
            # Por nivel de estudios
            education_index = education_options.index(nivel_estudios)
            riesgo += education_index + 1
            
            # Por consumo de sustancias
            if "Alcohol" in consumo_sustancias:
                riesgo += 1
            if "Tabaco" in consumo_sustancias:
                riesgo += 1
            if "Drogas recreativas" in consumo_sustancias:
                riesgo += 2
            if "Cocaína" in consumo_sustancias or "Heroína" in consumo_sustancias:
                riesgo += 3
            
            # Por antecedentes penales
            if "Robo" in antecedentes_penales:
                riesgo += 2
            if "Homicidio" in antecedentes_penales:
                riesgo += 3
            if "Violencia de género" in antecedentes_penales:
                riesgo += 3
            if "Terrorismo" in antecedentes_penales:
                riesgo += 5
            
            # Por rasgos de personalidad
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
                nivel_riesgo = lang["high"]
            elif riesgo >= 10:
                nivel_riesgo = lang["moderate"]
            else:
                nivel_riesgo = lang["low"]
                
            # Convertir fecha a string si existe
            fecha_terapia_str = None
            if fecha_inicio_terapia:
                fecha_terapia_str = fecha_inicio_terapia.strftime('%d/%m/%Y')
                
            # Guardar los datos en session_state para usarlos fuera del formulario
            st.session_state['form_data'] = {
                'edad': edad,
                'genero': genero,
                'nivel_estudios': nivel_estudios,
                'consumo_sustancias': consumo_sustancias,
                'pais_origen': pais_origen,
                'ciudad_origen': ciudad_origen,
                'perfil_psicologico': perfil_psicologico,
                'historial_clinico': historial_clinico,
                'comentarios_adicionales': comentarios_adicionales,
                'nivel_riesgo': nivel_riesgo,
                'riesgo_total': riesgo,
                'antecedentes_penales': antecedentes_penales,
                'rasgos_personalidad': rasgos_personalidad,
                'diagnosticos_previos': diagnosticos_previos,
                'terapia_previa': terapia_previa,
                'fecha_inicio_terapia': fecha_terapia_str,
                'fecha_alarma': fecha_alarma.strftime('%d/%m/%Y'),
                'motivo_interes': motivo_interes,
                'antecedentes_extremismo': antecedentes_extremismo,
                'foto_sujeto': foto_sujeto.name if foto_sujeto else None
            }
            st.session_state['form_submitted'] = True
            st.rerun()  # Forzar recarga para mostrar resultados fuera del formulario

    # Si el formulario ha sido enviado, mostrar los resultados fuera del formulario
    if st.session_state['form_submitted']:
        # Extraer datos del session_state
        data = st.session_state['form_data']
        edad = data['edad']
        genero = data['genero']
        nivel_estudios = data['nivel_estudios']
        consumo_sustancias = data['consumo_sustancias']
        pais_origen = data['pais_origen']
        ciudad_origen = data['ciudad_origen']
        perfil_psicologico = data['perfil_psicologico']
        historial_clinico = data['historial_clinico']
        comentarios_adicionales = data['comentarios_adicionales']
        nivel_riesgo = data['nivel_riesgo']
        riesgo_total = data['riesgo_total']
        antecedentes_penales = data['antecedentes_penales']
        rasgos_personalidad = data['rasgos_personalidad']
        diagnosticos_previos = data['diagnosticos_previos']
        terapia_previa = data['terapia_previa']
        fecha_inicio_terapia = data['fecha_inicio_terapia']
        fecha_alarma = data['fecha_alarma']
        motivo_interes = data['motivo_interes']
        antecedentes_extremismo = data['antecedentes_extremismo']
        foto_sujeto = data['foto_sujeto']
        
        # Mostrar informe
        st.success(lang["report_success"])
        st.header(lang["report_header"])
        st.write(f"**{lang['evaluation_date']}** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.write(f"**{lang['age']}:** {edad}")
        st.write(f"**{lang['gender']}:** {genero}")
        st.write(f"**{lang['education']}:** {nivel_estudios}")
        st.write(f"**{lang['substances']}:** {', '.join(consumo_sustancias) if consumo_sustancias else 'N/A'}")
        st.write(f"**{lang['country']}:** {pais_origen}")
        st.write(f"**{lang['city']}:** {ciudad_origen}")
        st.write(f"**{lang['risk_level']}** **{nivel_riesgo}**")
        
        # Mostrar nuevos campos
        if diagnosticos_previos:
            st.write(f"**{lang['diagnosis_list']}:** {', '.join(diagnosticos_previos)}")
        
        st.write(f"**{lang['previous_therapies']}:** {terapia_previa}")
        if fecha_inicio_terapia:
            st.write(f"**{lang['therapy_date']}:** {fecha_inicio_terapia}")
        
        st.write(f"**{lang['alarm_date']}:** {fecha_alarma}")
        
        if motivo_interes:
            st.write(f"**{lang['interest_profile']}:** {motivo_interes}")
        
        if antecedentes_extremismo:
            st.write(f"**{lang['family_extremism']}:** {antecedentes_extremismo}")
        
        if foto_sujeto:
            st.write(f"**{lang['upload_photo']}:** {foto_sujeto}")
        
        if perfil_psicologico:
            st.write(f"**{lang['psychological_profile']}:** {perfil_psicologico}")
        if historial_clinico:
            st.write(f"**{lang['medical_history']}:** {historial_clinico}")
        if comentarios_adicionales:
            st.write(f"**{lang['additional_comments']}:** {comentarios_adicionales}")

        st.subheader(lang["preliminary_notes"])
        if nivel_riesgo == lang["high"]:
            st.error(lang["high_risk"])
        elif nivel_riesgo == lang["moderate"]:
            st.warning(lang["moderate_risk"])
        else:
            st.info(lang["low_risk"])
            
        # Añadir sección de recomendaciones para las instituciones
        st.subheader(lang["recommendations"])
        
        # Recomendaciones terapéuticas
        st.write(f"**{lang['therapy_recs']}:**")
        if nivel_riesgo == lang["high"]:
            st.write("- Terapia cognitivo-conductual intensiva (3 sesiones semanales)")
            st.write("- Intervención psicosocial multidimensional")
            st.write("- Terapia familiar sistémica")
            st.write("- Tratamiento de trauma y estrés postraumático")
        elif nivel_riesgo == lang["moderate"]:
            st.write("- Terapia cognitivo-conductual (1-2 sesiones semanales)")
            st.write("- Terapia de grupo para manejo de ira y frustración")
            st.write("- Entrenamiento en habilidades sociales")
        else:
            st.write("- Terapia de apoyo (1 sesión quincenal)")
            st.write("- Orientación vocacional")
            st.write("- Desarrollo de habilidades de afrontamiento")
            
        # Recomendaciones farmacológicas
        st.write(f"**{lang['medication_recs']}:**")
        if nivel_riesgo == lang["high"]:
            st.write("- Evaluación psiquiátrica urgente para valoración de tratamiento")
            st.write("- Considerar antipsicóticos atípicos bajo estricta supervisión")
            st.write("- Estabilizadores del ánimo según evaluación psiquiátrica")
            st.write("- Tratamiento para adicciones si corresponde")
        elif nivel_riesgo == lang["moderate"]:
            st.write("- Evaluación psiquiátrica para valoración")
            st.write("- Considerar ansiolíticos de baja potencia para periodos cortos")
            st.write("- Tratamiento para depresión o ansiedad si corresponde")
        else:
            st.write("- No se recomienda medicación psiquiátrica salvo síntomas específicos")
            st.write("- Evaluación de seguimiento cada 3 meses")
            
        # Terapias de reinserción
        st.write(f"**{lang['reintegration_recs']}:**")
        if nivel_riesgo == lang["high"]:
            st.write("- Programa intensivo de desradicalización")
            st.write("- Reinserción gradual con supervisión continua")
            st.write("- Formación educativa o laboral en entorno controlado")
            st.write("- Mentores especializados en desradicalización")
        elif nivel_riesgo == lang["moderate"]:
            st.write("- Programa de integración comunitaria supervisada")
            st.write("- Formación laboral y educativa")
            st.write("- Desarrollo de red social positiva")
        else:
            st.write("- Fomento de participación comunitaria")
            st.write("- Programas de voluntariado")
            st.write("- Apoyo en educación o empleo")
            
        # Medidas de prevención
        st.write(f"**{lang['prevention_recs']}:**")
        if nivel_riesgo == lang["high"]:
            st.write("- Monitoreo constante por servicios de inteligencia")
            st.write("- Restricción de acceso a internet y redes sociales")
            st.write("- Control de desplazamientos y contactos")
            st.write("- Evaluaciones de riesgo periódicas (semanal)")
        elif nivel_riesgo == lang["moderate"]:
            st.write("- Seguimiento regular por servicios sociales")
            st.write("- Monitoreo de actividad online")
            st.write("- Evaluaciones de riesgo periódicas (mensual)")
        else:
            st.write("- Seguimiento comunitario")
            st.write("- Evaluación trimestral")
            
        # Medidas de urgencia (solo para riesgo alto)
        if nivel_riesgo == lang["high"]:
            st.write(f"**{lang['urgent_measures']}:**")
            st.write("- Notificación inmediata a unidades antiterroristas")
            st.write("- Intervención psiquiátrica de urgencia si hay signos de crisis")
            st.write("- Protocolo de contención en caso de riesgo inminente")
        
        # Mostrar informe detallado para directores
        if st.session_state['rol_usuario'] == 'director':
            st.subheader(lang["scoring_report"])
            st.write(lang["detailed_scoring"])
            
            # Calcular puntuaciones por categoría
            puntuacion_educacion = education_options.index(nivel_estudios) + 1
            
            puntuacion_sustancias = 0
            if "Alcohol" in consumo_sustancias:
                puntuacion_sustancias += 1
            if "Tabaco" in consumo_sustancias:
                puntuacion_sustancias += 1
            if "Drogas recreativas" in consumo_sustancias:
                puntuacion_sustancias += 2
            if "Cocaína" in consumo_sustancias or "Heroína" in consumo_sustancias:
                puntuacion_sustancias += 3
            
            puntuacion_antecedentes = 0
            if "Robo" in antecedentes_penales:
                puntuacion_antecedentes += 2
            if "Homicidio" in antecedentes_penales:
                puntuacion_antecedentes += 3
            if "Violencia de género" in antecedentes_penales:
                puntuacion_antecedentes += 3
            if "Terrorismo" in antecedentes_penales:
                puntuacion_antecedentes += 5
            
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
                
            # Mostrar el desglose de puntuación
            st.write(f"**{lang['total_risk_score']}:** {riesgo_total}")
            st.write(f"**{lang['education_score']}:** {puntuacion_educacion}")
            st.write(f"**{lang['substances_score']}:** {puntuacion_sustancias}")
            st.write(f"**{lang['criminal_score']}:** {puntuacion_antecedentes}")
            st.write(f"**{lang['personality_score']}:** {puntuacion_personalidad}")
            
            # Crear un gráfico de barras para visualizar las puntuaciones
            categorias = [lang['education_score'], lang['substances_score'], lang['criminal_score'], lang['personality_score']]
            valores = [puntuacion_educacion, puntuacion_sustancias, puntuacion_antecedentes, puntuacion_personalidad]
            
            # Crear un DataFrame para el gráfico
            chart_data = pd.DataFrame({
                'Categoría': categorias,
                'Puntuación': valores
            })
            
            # Mostrar gráfico de barras
            st.bar_chart(chart_data.set_index('Categoría'))
        
        # Generar PDF de informe usando FPDF en memoria (fuera del formulario)
        try:
            pdf_output = io.BytesIO()
            pdf = FPDF()
            pdf.add_page()
            
            # Configurar fuentes
            # Usar la fuente estándar Arial que viene con FPDF
            pdf.set_font('Arial', '', 12)
            
            # Título
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(200, 10, txt=lang["report_header"].replace('🔒 ', ''), ln=True, align='C')
            pdf.ln(10)
            
            # Información del informe
            pdf.set_font('Arial', '', 12)
            pdf.cell(200, 10, txt=f"{lang['evaluation_date']} {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
            pdf.cell(200, 10, txt=f"{lang['age']}: {edad}", ln=True)
            pdf.cell(200, 10, txt=f"{lang['gender']}: {genero}", ln=True)
            pdf.cell(200, 10, txt=f"{lang['education']}: {nivel_estudios}", ln=True)
            pdf.cell(200, 10, txt=f"{lang['substances']}: {', '.join(consumo_sustancias) if consumo_sustancias else 'N/A'}", ln=True)
            pdf.cell(200, 10, txt=f"{lang['country']}: {pais_origen}", ln=True)
            pdf.cell(200, 10, txt=f"{lang['city']}: {ciudad_origen}", ln=True)
            pdf.cell(200, 10, txt=f"{lang['risk_level']} {nivel_riesgo}", ln=True)
            
            # Añadir los nuevos campos al PDF
            if diagnosticos_previos:
                pdf.cell(200, 10, txt=f"{lang['diagnosis_list']}: {', '.join(diagnosticos_previos)}", ln=True)
            
            pdf.cell(200, 10, txt=f"{lang['previous_therapies']}: {terapia_previa}", ln=True)
            if fecha_inicio_terapia:
                pdf.cell(200, 10, txt=f"{lang['therapy_date']}: {fecha_inicio_terapia}", ln=True)
            
            pdf.cell(200, 10, txt=f"{lang['alarm_date']}: {fecha_alarma}", ln=True)
            
            if motivo_interes:
                pdf.multi_cell(0, 10, txt=f"{lang['interest_profile']}: {motivo_interes}")
            
            if antecedentes_extremismo:
                pdf.multi_cell(0, 10, txt=f"{lang['family_extremism']}: {antecedentes_extremismo}")
            
            if foto_sujeto:
                pdf.cell(200, 10, txt=f"{lang['upload_photo']}: {foto_sujeto}", ln=True)
            
            if perfil_psicologico:
                pdf.multi_cell(0, 10, txt=f"{lang['psychological_profile']}: {perfil_psicologico}")
            if historial_clinico:
                pdf.multi_cell(0, 10, txt=f"{lang['medical_history']}: {historial_clinico}")
            if comentarios_adicionales:
                pdf.multi_cell(0, 10, txt=f"{lang['additional_comments']}: {comentarios_adicionales}")
            
            # Agregar sección de recomendaciones
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(200, 10, txt=lang["recommendations"], ln=True)
            
            # Recomendaciones terapéuticas
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(200, 10, txt=f"{lang['therapy_recs']}", ln=True)
            pdf.set_font('Arial', '', 11)
            if nivel_riesgo == lang["high"]:
                pdf.cell(200, 8, txt="- Terapia cognitivo-conductual intensiva (3 sesiones semanales)", ln=True)
                pdf.cell(200, 8, txt="- Intervención psicosocial multidimensional", ln=True)
                pdf.cell(200, 8, txt="- Terapia familiar sistémica", ln=True)
                pdf.cell(200, 8, txt="- Tratamiento de trauma y estrés postraumático", ln=True)
            elif nivel_riesgo == lang["moderate"]:
                pdf.cell(200, 8, txt="- Terapia cognitivo-conductual (1-2 sesiones semanales)", ln=True)
                pdf.cell(200, 8, txt="- Terapia de grupo para manejo de ira y frustración", ln=True)
                pdf.cell(200, 8, txt="- Entrenamiento en habilidades sociales", ln=True)
            else:
                pdf.cell(200, 8, txt="- Terapia de apoyo (1 sesión quincenal)", ln=True)
                pdf.cell(200, 8, txt="- Orientación vocacional", ln=True)
                pdf.cell(200, 8, txt="- Desarrollo de habilidades de afrontamiento", ln=True)
            
            # Recomendaciones farmacológicas
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(200, 10, txt=f"{lang['medication_recs']}", ln=True)
            pdf.set_font('Arial', '', 11)
            if nivel_riesgo == lang["high"]:
                pdf.cell(200, 8, txt="- Evaluación psiquiátrica urgente para valoración de tratamiento", ln=True)
                pdf.cell(200, 8, txt="- Considerar antipsicóticos atípicos bajo estricta supervisión", ln=True)
                pdf.cell(200, 8, txt="- Estabilizadores del ánimo según evaluación psiquiátrica", ln=True)
                pdf.cell(200, 8, txt="- Tratamiento para adicciones si corresponde", ln=True)
            elif nivel_riesgo == lang["moderate"]:
                pdf.cell(200, 8, txt="- Evaluación psiquiátrica para valoración", ln=True)
                pdf.cell(200, 8, txt="- Considerar ansiolíticos de baja potencia para periodos cortos", ln=True)
                pdf.cell(200, 8, txt="- Tratamiento para depresión o ansiedad si corresponde", ln=True)
            else:
                pdf.cell(200, 8, txt="- No se recomienda medicación psiquiátrica salvo síntomas específicos", ln=True)
                pdf.cell(200, 8, txt="- Evaluación de seguimiento cada 3 meses", ln=True)
            
            # Terapias de reinserción
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(200, 10, txt=f"{lang['reintegration_recs']}", ln=True)
            pdf.set_font('Arial', '', 11)
            if nivel_riesgo == lang["high"]:
                pdf.cell(200, 8, txt="- Programa intensivo de desradicalización", ln=True)
                pdf.cell(200, 8, txt="- Reinserción gradual con supervisión continua", ln=True)
                pdf.cell(200, 8, txt="- Formación educativa o laboral en entorno controlado", ln=True)
                pdf.cell(200, 8, txt="- Mentores especializados en desradicalización", ln=True)
            elif nivel_riesgo == lang["moderate"]:
                pdf.cell(200, 8, txt="- Programa de integración comunitaria supervisada", ln=True)
                pdf.cell(200, 8, txt="- Formación laboral y educativa", ln=True)
                pdf.cell(200, 8, txt="- Desarrollo de red social positiva", ln=True)
            else:
                pdf.cell(200, 8, txt="- Fomento de participación comunitaria", ln=True)
                pdf.cell(200, 8, txt="- Programas de voluntariado", ln=True)
                pdf.cell(200, 8, txt="- Apoyo en educación o empleo", ln=True)
            
            # Medidas de prevención
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(200, 10, txt=f"{lang['prevention_recs']}", ln=True)
            pdf.set_font('Arial', '', 11)
            if nivel_riesgo == lang["high"]:
                pdf.cell(200, 8, txt="- Monitoreo constante por servicios de inteligencia", ln=True)
                pdf.cell(200, 8, txt="- Restricción de acceso a internet y redes sociales", ln=True)
                pdf.cell(200, 8, txt="- Control de desplazamientos y contactos", ln=True)
                pdf.cell(200, 8, txt="- Evaluaciones de riesgo periódicas (semanal)", ln=True)
            elif nivel_riesgo == lang["moderate"]:
                pdf.cell(200, 8, txt="- Seguimiento regular por servicios sociales", ln=True)
                pdf.cell(200, 8, txt="- Monitoreo de actividad online", ln=True)
                pdf.cell(200, 8, txt="- Evaluaciones de riesgo periódicas (mensual)", ln=True)
            else:
                pdf.cell(200, 8, txt="- Seguimiento comunitario", ln=True)
                pdf.cell(200, 8, txt="- Evaluación trimestral", ln=True)
            
            # Medidas de urgencia (solo para riesgo alto)
            if nivel_riesgo == lang["high"]:
                pdf.ln(5)
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(200, 10, txt=f"{lang['urgent_measures']}", ln=True)
                pdf.set_font('Arial', '', 11)
                pdf.cell(200, 8, txt="- Notificación inmediata a unidades antiterroristas", ln=True)
                pdf.cell(200, 8, txt="- Intervención psiquiátrica de urgencia si hay signos de crisis", ln=True)
                pdf.cell(200, 8, txt="- Protocolo de contención en caso de riesgo inminente", ln=True)
            
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
