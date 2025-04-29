import streamlit as st
from datetime import datetime
from fpdf import FPDF
import os
from PIL import Image

st.set_page_config(page_title="BIAS", page_icon="🕵️", layout="wide")

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
        "social_isolation": "Aislamiento social progresivo",
        "violence_justification": "Justificación de la violencia",
        "extremist_fascination": "Fascinación por ideologías extremistas",
        "behavior_changes": "Cambios drásticos en el comportamiento",
        "hate_expression": "Expresión de odio hacia grupos específicos",
        "radicalized_contact": "Contacto con individuos radicalizados",
        "extremist_propaganda": "Consumo de propaganda extremista",
        "suspicious_online": "Participación en actividades sospechosas online",
        "recruitment_attempts": "Intento de reclutamiento de otros",
        "combat_preparation": "Preparación física para el combate",
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
        "therapy": "Terapias previas",
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
        "social_isolation": "Progressive social isolation",
        "violence_justification": "Justification of violence",
        "extremist_fascination": "Fascination with extremist ideologies",
        "behavior_changes": "Drastic behavioral changes",
        "hate_expression": "Expression of hatred toward specific groups",
        "radicalized_contact": "Contact with radicalized individuals",
        "extremist_propaganda": "Consumption of extremist propaganda",
        "suspicious_online": "Participation in suspicious online activities",
        "recruitment_attempts": "Attempts to recruit others",
        "combat_preparation": "Physical preparation for combat",
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
        "therapy": "Previous therapies",
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
    },
    "Deutsch": {
        "app_title": "BIAS - System für Verhaltensintelligenz-Analyse",
        "login": "Anmelden",
        "username": "Benutzername",
        "password": "Passwort",
        "logout": "Abmelden",
        "submit": "Bewertung einreichen",
        "profile_section": "Bewertungsprofil",
        "name": "Vollständiger Name",
        "id_number": "Ausweisnummer",
        "age": "Alter",
        "gender": "Geschlecht",
        "male": "Männlich",
        "female": "Weiblich",
        "other": "Andere",
        "education": "Bildungsniveau",
        "primary": "Grundschule",
        "secondary": "Sekundarschule",
        "university": "Universität",
        "postgraduate": "Postgraduiert",
        "none_edu": "Keine",
        "substances": "Substanzkonsum",
        "alcohol": "Alkohol",
        "tobacco": "Tabak",
        "recreational": "Freizeitdrogen",
        "cocaine": "Kokain",
        "heroin": "Heroin",
        "none_substance": "Keine",
        "criminal_record": "Vorstrafen",
        "theft": "Diebstahl",
        "gender_violence": "Geschlechtsspezifische Gewalt",
        "homicide": "Mord",
        "terrorism": "Terrorismus",
        "none_criminal": "Keine",
        "social_isolation": "Progressive soziale Isolation",
        "violence_justification": "Rechtfertigung von Gewalt",
        "extremist_fascination": "Faszination für extremistische Ideologien",
        "behavior_changes": "Drastische Verhaltensänderungen",
        "hate_expression": "Äußerung von Hass gegenüber bestimmten Gruppen",
        "radicalized_contact": "Kontakt mit radikalisierten Personen",
        "extremist_propaganda": "Konsum extremistischer Propaganda",
        "suspicious_online": "Teilnahme an verdächtigen Online-Aktivitäten",
        "recruitment_attempts": "Versuche, andere zu rekrutieren",
        "combat_preparation": "Körperliche Vorbereitung auf den Kampf",
        "personality_traits": "Persönlichkeitsmerkmale",
        "paranoid": "Paranoid",
        "antisocial": "Antisozial",
        "sadomasochistic": "Sadomasochistisch",
        "impulsive": "Impulsiv",
        "unstable": "Emotional instabil",
        "dependent": "Abhängig",
        "avoidant": "Vermeidend",
        "narcissistic": "Narzisstisch",
        "histrionic": "Histrionisch",
        "passive_aggressive": "Passiv-aggressiv",
        "schizoid": "Schizoid",
        "obsessive": "Zwanghaft",
        "none_traits": "Keine signifikanten Merkmale",
        "diagnosis_list": "Frühere Diagnosen",
        "therapy": "Frühere Therapien",
        "therapy_date": "Therapiebeginn",
        "alarm_date": "Jahr der Warnzeichen",
        "interest_profile": "Grund des Interesses",
        "family_extremism": "Familiengeschichte des Extremismus",
        "clinical_history": "Klinische Vorgeschichte",
        "psychological_profile": "Psychologisches Profil",
        "additional_comments": "Zusätzliche Kommentare",
        "upload_photo": "Foto des Subjekts hochladen",
        "download_report": "Allgemeinen Bericht herunterladen",
        "download_director": "Direktionsbericht herunterladen",
        "risk_level": "Risikoniveau",
        "risk_explanation": "Erklärung des Risikoniveaus",
        "recommendations": "Institutionelle Empfehlungen",
        "therapy_recs": "Therapeutische Empfehlungen",
        "medication_recs": "Pharmakologische Empfehlungen",
        "reintegration_recs": "Wiedereingliederungstherapien",
        "prevention_recs": "Präventionsmaßnahmen",
        "urgent_measures": "Dringende Maßnahmen",
        "graphics": "Grafiken und Tabellen",
        "danger_table": "Angriffsgefahr-Tabelle",
        "evolution_table": "Gefahrenentwicklungstabelle bei Nichtbehandlung",
        "confidential": "Vertraulich - Eingeschränkte Nutzung",
        "executive_summary": "Zusammenfassung",
        "date": "Erstellungsdatum",
        "analyst": "Verantwortlicher/Analyst"
    },
    "Français": {
        "app_title": "BIAS - Système d'Analyse d'Intelligence Comportementale",
        "login": "Connexion",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "logout": "Déconnexion",
        "submit": "Soumettre l'évaluation",
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
        "university": "Université",
        "postgraduate": "Post-universitaire",
        "none_edu": "Aucun",
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
        "social_isolation": "Isolement social progressif",
        "violence_justification": "Justification de la violence",
        "extremist_fascination": "Fascination pour les idéologies extrémistes",
        "behavior_changes": "Changements comportementaux drastiques",
        "hate_expression": "Expression de haine envers des groupes spécifiques",
        "radicalized_contact": "Contact avec des individus radicalisés",
        "extremist_propaganda": "Consommation de propagande extrémiste",
        "suspicious_online": "Participation à des activités suspectes en ligne",
        "recruitment_attempts": "Tentatives de recrutement d'autres personnes",
        "combat_preparation": "Préparation physique au combat",
        "personality_traits": "Traits de personnalité",
        "paranoid": "Paranoïaque",
        "antisocial": "Antisocial",
        "sadomasochistic": "Sadomasochiste",
        "impulsive": "Impulsif",
        "unstable": "Émotionnellement instable",
        "dependent": "Dépendant",
        "avoidant": "Évitant",
        "narcissistic": "Narcissique",
        "histrionic": "Histrionique",
        "passive_aggressive": "Passif-agressif",
        "schizoid": "Schizoïde",
        "obsessive": "Obsessionnel",
        "none_traits": "Aucun trait significatif",
        "diagnosis_list": "Diagnostics antérieurs",
        "therapy": "Thérapies antérieures",
        "therapy_date": "Date de début de thérapie",
        "alarm_date": "Année des signes d'alarme",
        "interest_profile": "Motif d'intérêt",
        "family_extremism": "Antécédents familiaux d'extrémisme",
        "clinical_history": "Historique clinique",
        "psychological_profile": "Profil psychologique",
        "additional_comments": "Commentaires supplémentaires",
        "upload_photo": "Télécharger la photo du sujet",
        "download_report": "Télécharger le rapport générique",
        "download_director": "Télécharger le rapport directorial",
        "risk_level": "Niveau de risque",
        "risk_explanation": "Explication du niveau de risque",
        "recommendations": "Recommandations institutionnelles",
        "therapy_recs": "Recommandations thérapeutiques",
        "medication_recs": "Recommandations pharmacologiques",
        "reintegration_recs": "Thérapies de réinsertion",
        "prevention_recs": "Mesures de prévention",
        "urgent_measures": "Mesures urgentes",
        "graphics": "Graphiques et tableaux",
        "danger_table": "Tableau de danger d'attentat",
        "evolution_table": "Tableau d'évolution du danger sans traitement",
        "confidential": "Confidentiel - Usage restreint",
        "executive_summary": "Résumé exécutif",
        "date": "Date de génération",
        "analyst": "Responsable/Analyste"
    },
    "العربية": {
        "app_title": "نظام تحليل الذكاء السلوكي - BIAS",
        "login": "تسجيل الدخول",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "logout": "تسجيل الخروج",
        "submit": "إرسال التقييم",
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
        "none_edu": "لا يوجد",
        "substances": "تعاطي المواد",
        "alcohol": "الكحول",
        "tobacco": "التبغ",
        "recreational": "المخدرات الترفيهية",
        "cocaine": "الكوكايين",
        "heroin": "الهيروين",
        "none_substance": "لا يوجد",
        "criminal_record": "السجل الجنائي",
        "theft": "سرقة",
        "gender_violence": "عنف قائم على النوع",
        "homicide": "قتل",
        "terrorism": "إرهاب",
        "none_criminal": "لا يوجد",
        "social_isolation": "العزلة الاجتماعية التدريجية",
        "violence_justification": "تبرير العنف",
        "extremist_fascination": "افتتان بالأيديولوجيات المتطرفة",
        "behavior_changes": "تغييرات سلوكية جذرية",
        "hate_expression": "التعبير عن الكراهية تجاه مجموعات محددة",
        "radicalized_contact": "الاتصال بأفراد متطرفين",
        "extremist_propaganda": "استهلاك الدعاية المتطرفة",
        "suspicious_online": "المشاركة في أنشطة مشبوهة عبر الإنترنت",
        "recruitment_attempts": "محاولات تجنيد الآخرين",
        "combat_preparation": "الإعداد البدني للقتال",
        "personality_traits": "سمات الشخصية",
        "paranoid": "جنوني",
        "antisocial": "معادي للمجتمع",
        "sadomasochistic": "سادي مازوخي",
        "impulsive": "اندفاعي",
        "unstable": "غير مستقر عاطفيا",
        "dependent": "اعتمادي",
        "avoidant": "تجنبي",
        "narcissistic": "نرجسي",
        "histrionic": "مسرحي",
        "passive_aggressive": "سلبي عدواني",
        "schizoid": "انفصامي",
        "obsessive": "وسواسي",
        "none_traits": "لا توجد سمات مهمة",
        "diagnosis_list": "التشخيصات السابقة",
        "therapy": "العلاجات السابقة",
        "therapy_date": "تاريخ بدء العلاج",
        "alarm_date": "سنة ظهور علامات الإنذار",
        "interest_profile": "سبب الاهتمام",
        "family_extremism": "تاريخ التطرف العائلي",
        "clinical_history": "التاريخ السريري",
        "psychological_profile": "الملف النفسي",
        "additional_comments": "تعليقات إضافية",
        "upload_photo": "تحميل صورة الموضوع",
        "download_report": "تنزيل التقرير العام",
        "download_director": "تنزيل تقرير المدير",
        "risk_level": "مستوى الخطر",
        "risk_explanation": "شرح مستوى الخطر",
        "recommendations": "التوصيات المؤسسية",
        "therapy_recs": "توصيات علاجية",
        "medication_recs": "توصيات دوائية",
        "reintegration_recs": "علاجات إعادة الدمج",
        "prevention_recs": "تدابير وقائية",
        "urgent_measures": "تدابير عاجلة",
        "graphics": "الرسوم البيانية والجداول",
        "danger_table": "جدول خطر الهجوم",
        "evolution_table": "جدول تطور الخطر إذا لم يعالج",
        "confidential": "سري - استخدام مقيد",
        "executive_summary": "ملخص تنفيذي",
        "date": "تاريخ الإنشاء",
        "analyst": "المسؤول/المحلل"
    }
}

def get_translation(key):
    if 'lang' not in st.session_state:
        st.session_state.lang = "Español"
    return translations[st.session_state.lang].get(key, key)

class ProfessionalPDF(FPDF):
    def __init__(self, lang="Español"):
        super().__init__()
        self.lang = lang
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)
        self.add_font('DejaVu', 'I', 'DejaVuSans-Oblique.ttf', uni=True)
        self.add_font('DejaVu', 'BI', 'DejaVuSans-BoldOblique.ttf', uni=True)
        self.set_font('DejaVu', '', 12)

    def cover_page(self, data):
        self.add_page()
        self.set_font('DejaVu', 'B', 16)
        title = get_translation("app_title")
        self.multi_cell(0, 10, title, align='C')
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, f"{get_translation('date')}: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'R')
        self.cell(0, 10, f"{get_translation('analyst')}: {data.get('analyst', 'N/A')}", 0, 1, 'R')
        self.ln(5)
        self.set_font('DejaVu', 'I', 10)
        self.cell(0, 10, get_translation("confidential"), 0, 1, 'C')
        self.ln(10)

    def executive_summary(self, summary, photo=None):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, get_translation("executive_summary"), 0, 1, 'L')
        y_start = self.get_y()
        self.set_font('DejaVu', '', 12)
        self.multi_cell(110, 8, summary)
        self.ln(5)
        if photo is not None:
            try:
                img = Image.open(photo)
                img_path = "temp_photo.jpg"
                img.save(img_path)
                self.image(img_path, x=130, y=y_start, w=50)
                os.remove(img_path)
            except Exception as e:
                print(f"Error procesando la imagen: {e}")

    def subject_data_table(self, data):
        self.add_page()
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, get_translation("profile_section"), 0, 1, 'C')
        self.ln(5)
        self.set_fill_color(220, 220, 220)
        self.set_font('DejaVu', 'B', 12)
        fields = [
            (get_translation("name"), data.get('name', 'N/A')),
            (get_translation("id_number"), data.get('id_number', 'N/A')),
            (get_translation("age"), str(data.get('age', 'N/A'))),
            (get_translation("gender"), data.get('gender', 'N/A')),
            (get_translation("education"), data.get('education', 'N/A')),
            (get_translation("clinical_history"), data.get('clinical_history', 'N/A')),
            (get_translation("psychological_profile"), data.get('psychological_profile', 'N/A')),
            (get_translation("diagnosis_list"), data.get('diagnosis_list', 'N/A')),
            (get_translation("therapy"), data.get('therapy', 'N/A')),
            (get_translation("therapy_date"), str(data.get('therapy_date', 'N/A'))),
            (get_translation("alarm_date"), str(data.get('alarm_year', 'N/A'))),
            (get_translation("interest_profile"), data.get('interest_profile', 'N/A')),
            (get_translation("family_extremism"), data.get('family_extremism', 'N/A')),
            (get_translation("additional_comments"), data.get('additional_comments', 'N/A'))
        ]
        for i, (field, value) in enumerate(fields):
            fill = i % 2 == 0
            self.set_font('DejaVu', 'B', 11)
            self.cell(60, 10, field, 1, 0, 'L', fill)
            self.set_font('DejaVu', '', 11)
            self.multi_cell(0, 10, str(value), 1, 'L', fill)

    def risk_assessment(self, risk_level, explanation):
        self.add_page()
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, get_translation("risk_level"), 0, 1, 'C')
        self.ln(5)
        self.set_font('DejaVu', 'B', 14)
        self.cell(60, 10, f"{get_translation('risk_level')}:", 0, 0)
        if risk_level == get_translation("risk_level"):
            self.set_text_color(255, 0, 0)
        elif risk_level == "MODERADO":
            self.set_text_color(255, 128, 0)
        else:
            self.set_text_color(0, 128, 0)
        self.cell(0, 10, risk_level, 0, 1)
        self.set_text_color(0, 0, 0)
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 10, get_translation("risk_explanation"), 0, 1)
        self.set_font('DejaVu', '', 11)
        self.multi_cell(0, 8, explanation)
        self.ln(10)
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, get_translation("graphics"), 0, 1)
        risk_factors = {
            get_translation("criminal_record"): 85,
            get_translation("personality_traits"): 70,
            get_translation("substances"): 60,
            get_translation("social_isolation"): 40
        }
        self.set_font('DejaVu', '', 10)
        for factor, value in risk_factors.items():
            bar = "█" * int(value/10)
            self.cell(60, 8, f"{factor}:", 0, 0)
            self.cell(0, 8, f"{bar} {value}%", 0, 1)

    def recommendations_section(self, recs):
        self.add_page()
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, get_translation("recommendations"), 0, 1, 'C')
        self.ln(5)
        self.set_fill_color(220, 220, 220)
        for i, (title, explanation) in enumerate(recs):
            fill = i % 2 == 0
            self.set_font('DejaVu', 'B', 12)
            self.cell(0, 10, title, 1, 1, 'L', fill)
            self.set_font('DejaVu', '', 11)
            self.multi_cell(0, 8, explanation, 1, 'L', fill)
            self.ln(3)

    def graphics_section(self):
        self.add_page()
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, get_translation("graphics"), 0, 1, 'C')
        self.ln(5)
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, get_translation("evolution_table"), 0, 1)
        self.set_fill_color(220, 220, 220)
        self.set_font('DejaVu', 'B', 9)
        self.cell(40, 8, get_translation("date"), 1, 0, 'C', True)
        self.cell(40, 8, get_translation("risk_level"), 1, 0, 'C', True)
        self.cell(40, 8, get_translation("recommendations"), 1, 0, 'C', True)
        self.cell(0, 8, get_translation("risk_explanation"), 1, 1, 'C', True)
        data = [
            ("3 meses", "Alto", "Alto+", "Aislamiento social, radicalización online"),
            ("6 meses", "Alto+", "Extremo", "Contacto con extremistas, pérdida de anclajes sociales"),
            ("12 meses", "Extremo", "Crítico", "Preparación potencial para acción violenta")
        ]
        self.set_font('DejaVu', '', 6)
        for i, (period, initial, projection, factors) in enumerate(data):
            fill = i % 2 == 1
            self.cell(40, 8, period, 1, 0, 'C', fill)
            self.cell(40, 8, initial, 1, 0, 'C', fill)
            self.cell(40, 8, projection, 1, 0, 'C', fill)
            self.cell(0, 8, factors, 1, 1, 'L', fill)
        self.ln(10)
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 10, get_translation("danger_table"), 0, 1)
        self.set_font('DejaVu', '', 10)
        self.cell(0, 10, get_translation("confidential"), 0, 1)

    def director_report_extension(self):
        self.add_page()
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, get_translation("download_director"), 0, 1, 'C')
        self.ln(5)
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, get_translation("risk_level"), 0, 1)
        self.set_fill_color(220, 220, 220)
        self.set_font('DejaVu', 'B', 11)
        self.cell(60, 10, get_translation("criminal_record"), 1, 0, 'L', True)
        self.cell(40, 10, "Puntuación", 1, 0, 'C', True)
        self.cell(0, 10, get_translation("risk_explanation"), 1, 1, 'L', True)
        data = [
            (get_translation("criminal_record"), "85/100", get_translation("risk_explanation")),
            (get_translation("personality_traits"), "70/100", get_translation("risk_explanation")),
            (get_translation("substances"), "60/100", get_translation("risk_explanation")),
            (get_translation("social_isolation"), "40/100", get_translation("risk_explanation")),
            ("PUNTUACIÓN GLOBAL", "73/100", get_translation("risk_explanation"))
        ]
        self.set_font('DejaVu', '', 10)
        for i, (factor, score, method) in enumerate(data):
            fill = i % 2 == 1
            if factor == "PUNTUACIÓN GLOBAL":
                self.set_font('DejaVu', 'B', 10)
            self.cell(60, 10, factor, 1, 0, 'L', fill)
            self.cell(40, 10, score, 1, 0, 'C', fill)
            self.multi_cell(0, 10, method, 1, 'L', fill)
            self.set_font('DejaVu', '', 10)
        self.ln(10)
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, get_translation("executive_summary"), 0, 1)
        self.set_font('DejaVu', '', 11)
        self.multi_cell(0, 8, get_translation("risk_explanation"))

def main():
    if 'lang' not in st.session_state:
        st.session_state.lang = "Español"

    st.sidebar.title("🌍 " + get_translation("language"))
    lang_options = list(translations.keys())
    selected_lang = st.sidebar.selectbox(
        get_translation("language"),
        lang_options,
        index=lang_options.index(st.session_state.lang) if st.session_state.lang in lang_options else 0,
        key="lang_selector"
    )
    st.session_state.lang = selected_lang

    if 'auth' not in st.session_state:
        st.session_state.auth = False

    if not st.session_state.auth:
        st.title(get_translation("app_title"))
        user = st.text_input(get_translation("username"), key="login_user")
        pwd = st.text_input(get_translation("password"), type="password", key="login_pwd")
        if st.button(get_translation("login"), key="login_btn"):
            if user in ["demo_bias", "JuanCarlos_bias", "Cristina_bias"] and pwd in ["biasdemo2025", "admin_bias"]:
                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error(get_translation("login_error"))
        return

    if st.sidebar.button(get_translation("logout"), key="logout_btn"):
        st.session_state.auth = False
        st.rerun()

    st.title(get_translation("app_title"))
    with st.form(key="main_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(get_translation("name"), key="name_input")
            id_number = st.text_input(get_translation("id_number"), key="id_input")
            age = st.number_input(get_translation("age"), 12, 100, 25, key="age_input")
            gender = st.selectbox(
                get_translation("gender"),
                [get_translation("male"), get_translation("female"), get_translation("other")],
                key="gender_select"
            )
            education = st.selectbox(
                get_translation("education"),
                [
                    get_translation("primary"),
                    get_translation("secondary"),
                    get_translation("university"),
                    get_translation("postgraduate"),
                    get_translation("none_edu")
                ],
                key="education_select"
            )
            substances = st.multiselect(
                get_translation("substances"),
                [
                    get_translation("alcohol"),
                    get_translation("tobacco"),
                    get_translation("recreational"),
                    get_translation("cocaine"),
                    get_translation("heroin"),
                    get_translation("none_substance")
                ],
                key="substances_select"
            )
            criminal_record = st.multiselect(
                get_translation("criminal_record"),
                [
                    get_translation("theft"),
                    get_translation("gender_violence"),
                    get_translation("homicide"),
                    get_translation("terrorism"),
                    get_translation("none_criminal"),
                    get_translation("social_isolation"),
                    get_translation("violence_justification"),
                    get_translation("extremist_fascination"),
                    get_translation("behavior_changes"),
                    get_translation("hate_expression"),
                    get_translation("radicalized_contact"),
                    get_translation("extremist_propaganda"),
                    get_translation("suspicious_online"),
                    get_translation("recruitment_attempts"),
                    get_translation("combat_preparation")
                ],
                key="criminal_select"
            )
        with col2:
            personality_traits = st.multiselect(
                get_translation("personality_traits"),
                [
                    get_translation("paranoid"),
                    get_translation("antisocial"),
                    get_translation("sadomasochistic"),
                    get_translation("impulsive"),
                    get_translation("unstable"),
                    get_translation("dependent"),
                    get_translation("avoidant"),
                    get_translation("narcissistic"),
                    get_translation("histrionic"),
                    get_translation("passive_aggressive"),
                    get_translation("schizoid"),
                    get_translation("obsessive"),
                    get_translation("none_traits")
                ],
                key="personality_select"
            )
            diagnosis_list = st.text_area(get_translation("diagnosis_list"), key="diagnosis_area")
            therapy = st.text_input(get_translation("therapy"), key="therapy_input")
            therapy_date = st.date_input(get_translation("therapy_date"), key="therapy_date") if therapy else None
            alarm_year = st.selectbox(
                get_translation("alarm_date"),
                list(range(2000, datetime.now().year + 1)),
                key="alarm_year_select"
            )
            interest_profile = st.text_area(get_translation("interest_profile"), key="interest_area")
            family_extremism = st.text_area(get_translation("family_extremism"), key="family_extremism_area")
            clinical_history = st.text_area(get_translation("clinical_history"), key="clinical_area")
            psychological_profile = st.text_area(get_translation("psychological_profile"), key="psychological_area")
            additional_comments = st.text_area(get_translation("additional_comments"), key="comments_area")
            uploaded_photo = st.file_uploader(get_translation("upload_photo"), type=["jpg", "png"], key="photo_uploader")

        analyst = st.text_input(get_translation("analyst"), value=st.session_state.user, key="analyst_input")
        submitted = st.form_submit_button(get_translation("submit"), key="submit_btn")

    if submitted:
        executive_summary = get_translation("executive_summary")
        risk_level = "ALTO"
        risk_explanation = get_translation("risk_explanation")
        recommendations = [
            (get_translation("therapy_recs"), get_translation("therapy_recs_details")),
            (get_translation("medication_recs"), get_translation("medication_recs_details")),
            (get_translation("reintegration_recs"), get_translation("reintegration_recs_details")),
            (get_translation("prevention_recs"), get_translation("prevention_recs_details"))
        ]
        try:
            pdf = ProfessionalPDF(st.session_state.lang)
            pdf.cover_page({"analyst": analyst})
            pdf.executive_summary(executive_summary, uploaded_photo)
            subject_data = {
                "name": name,
                "id_number": id_number,
                "age": age,
                "gender": gender,
                "education": education,
                "substances": substances,
                "criminal_record": criminal_record,
                "personality_traits": personality_traits,
                "diagnosis_list": diagnosis_list,
                "therapy": therapy,
                "therapy_date": therapy_date,
                "alarm_year": alarm_year,
                "interest_profile": interest_profile,
                "family_extremism": family_extremism,
                "clinical_history": clinical_history,
                "psychological_profile": psychological_profile,
                "additional_comments": additional_comments,
                "analyst": analyst
            }
            pdf.subject_data_table(subject_data)
            pdf.risk_assessment(risk_level, risk_explanation)
            pdf.recommendations_section(recommendations)
            pdf.graphics_section()
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                get_translation("download_report"),
                pdf_bytes,
                file_name="bias_report.pdf",
                mime="application/pdf",
                key="report_btn"
            )
            if st.session_state.user in ["JuanCarlos_bias", "Cristina_bias"]:
                dir_pdf = ProfessionalPDF(st.session_state.lang)
                dir_pdf.director_report_extension()
                pdf_dir_bytes = dir_pdf.output(dest='S').encode('latin-1')
                st.download_button(
                    get_translation("download_director"),
                    pdf_dir_bytes,
                    file_name="bias_director_report.pdf",
                    mime="application/pdf",
                    key="director_btn"
                )
        except Exception as e:
            st.error(f"{get_translation('error')}: {str(e)}")

if __name__ == "__main__":
    main()
