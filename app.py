import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from fpdf import FPDF
import io
import base64
import re
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(
    page_title="Sistema Escolar Interactivo",
    page_icon="🏫",
    layout="wide"
)

# ============================================
# DATOS DE ESTUDIANTES - BASE
# ============================================
data_carlos_giraldo = [
    ["Alejandro Vargas", 13579246, "Matemáticas", 4.5, 8], 
    ["Alejandro Vargas", 13579246, "Español", 7.2, 9],
    ["Alejandro Vargas", 13579246, "Inglés", 6.8, 7], 
    ["Alejandro Vargas", 13579246, "Ciencias", 5.9, 8],
    ["Beatriz Morales", 24681357, "Matemáticas", 8.1, 10], 
    ["Beatriz Morales", 24681357, "Español", 9.0, 10],
    ["Beatriz Morales", 24681357, "Inglés", 7.5, 9], 
    ["Beatriz Morales", 24681357, "Ciencias", 8.8, 10],
    ["Carlos Mendoza", 35792468, "Matemáticas", 6.4, 7], 
    ["Carlos Mendoza", 35792468, "Español", 5.8, 6],
    ["Carlos Mendoza", 35792468, "Inglés", 8.2, 9], 
    ["Carlos Mendoza", 35792468, "Ciencias", 7.0, 8],
    ["Daniela Ortiz", 46813579, "Matemáticas", 3.8, 5], 
    ["Daniela Ortiz", 46813579, "Español", 6.5, 8],
    ["Daniela Ortiz", 46813579, "Inglés", 5.0, 6], 
    ["Daniela Ortiz", 46813579, "Ciencias", 4.2, 4],
    ["Eduardo Navarro", 57924680, "Matemáticas", 9.2, 10], 
    ["Eduardo Navarro", 57924680, "Español", 8.7, 9],
    ["Eduardo Navarro", 57924680, "Inglés", 9.5, 10], 
    ["Eduardo Navarro", 57924680, "Ciencias", 8.9, 10],
]

data_olga_santamaria = [
    ["Fernanda Pérez", 68035791, "Matemáticas", 7.9, 9], 
    ["Fernanda Pérez", 68035791, "Español", 8.8, 10],
    ["Fernanda Pérez", 68035791, "Inglés", 9.0, 10], 
    ["Fernanda Pérez", 68035791, "Ciencias", 8.5, 9],
    ["Gabriel Quintana", 79146802, "Matemáticas", 5.3, 7], 
    ["Gabriel Quintana", 79146802, "Español", 7.6, 9],
    ["Gabriel Quintana", 79146802, "Inglés", 6.1, 8], 
    ["Gabriel Quintana", 79146802, "Ciencias", 6.8, 7],
    ["Helena Ruiz", 80257913, "Matemáticas", 8.5, 10], 
    ["Helena Ruiz", 80257913, "Español", 7.3, 8],
    ["Helena Ruiz", 80257913, "Inglés", 8.9, 10], 
    ["Helena Ruiz", 80257913, "Ciencias", 7.7, 9],
    ["Ignacio Salazar", 91368024, "Matemáticas", 6.7, 8], 
    ["Ignacio Salazar", 91368024, "Español", 5.5, 6],
    ["Ignacio Salazar", 91368024, "Inglés", 7.4, 9], 
    ["Ignacio Salazar", 91368024, "Ciencias", 6.9, 8],
    ["Juliana Torres", 2479135, "Matemáticas", 9.0, 10], 
    ["Juliana Torres", 2479135, "Español", 8.6, 9],
    ["Juliana Torres", 2479135, "Inglés", 9.3, 10], 
    ["Juliana Torres", 2479135, "Ciencias", 8.8, 10],
]

# ============================================
# CREAR DATOS PARA AMBOS DEPARTAMENTOS
# ============================================
columns = ["Nombre", "Cedula", "Asignatura", "Nota_Parcial", "Nota_Final"]

# Colegio Carlos Giraldo - Boyacá
df_carlos_giraldo_boyaca = pd.DataFrame(data_carlos_giraldo, columns=columns)
df_carlos_giraldo_boyaca["Departamento"] = "Boyacá"
df_carlos_giraldo_boyaca["Colegio"] = "Colegio Departamental Carlos Giraldo - Boyacá"
df_carlos_giraldo_boyaca["Asistencia"] = 0

# Colegio Carlos Giraldo - Cundinamarca
df_carlos_giraldo_cundinamarca = pd.DataFrame(data_carlos_giraldo, columns=columns)
df_carlos_giraldo_cundinamarca["Departamento"] = "Cundinamarca"
df_carlos_giraldo_cundinamarca["Colegio"] = "Colegio Departamental Carlos Giraldo - Cundinamarca"
df_carlos_giraldo_cundinamarca["Asistencia"] = 0

# Instituto Olga Santamaría - Boyacá
df_olga_santamaria_boyaca = pd.DataFrame(data_olga_santamaria, columns=columns)
df_olga_santamaria_boyaca["Departamento"] = "Boyacá"
df_olga_santamaria_boyaca["Colegio"] = "Instituto Técnico Olga Santamaría - Boyacá"
df_olga_santamaria_boyaca["Asistencia"] = 0

# Instituto Olga Santamaría - Cundinamarca
df_olga_santamaria_cundinamarca = pd.DataFrame(data_olga_santamaria, columns=columns)
df_olga_santamaria_cundinamarca["Departamento"] = "Cundinamarca"
df_olga_santamaria_cundinamarca["Colegio"] = "Instituto Técnico Olga Santamaría - Cundinamarca"
df_olga_santamaria_cundinamarca["Asistencia"] = 0

# DataFrame combinado (todos los departamentos e instituciones)
df_all_students = pd.concat([
    df_carlos_giraldo_boyaca,
    df_carlos_giraldo_cundinamarca,
    df_olga_santamaria_boyaca,
    df_olga_santamaria_cundinamarca
], ignore_index=True)

# ============================================
# DATOS DE PROFESORES - AGREGADOS PARA AMBOS DEPARTAMENTOS
# ============================================
profesores_data = {
    "Colegio Departamental Carlos Giraldo - Boyacá": [
        {"nombre": "Prof. María García", "cedula": 11111111, "asignatura": "Matemáticas"},
        {"nombre": "Prof. Juan López", "cedula": 22222222, "asignatura": "Español"},
        {"nombre": "Prof. Ana Martínez", "cedula": 33333333, "asignatura": "Inglés"},
        {"nombre": "Prof. Pedro Sánchez", "cedula": 44444444, "asignatura": "Ciencias"},
    ],
    "Instituto Técnico Olga Santamaría - Boyacá": [
        {"nombre": "Prof. Laura Rodríguez", "cedula": 55555555, "asignatura": "Matemáticas"},
        {"nombre": "Prof. Carlos Hernández", "cedula": 66666666, "asignatura": "Español"},
        {"nombre": "Prof. Diana Gómez", "cedula": 77777777, "asignatura": "Inglés"},
        {"nombre": "Prof. Roberto Díaz", "cedula": 88888888, "asignatura": "Ciencias"},
    ],
    "Colegio Departamental Carlos Giraldo - Cundinamarca": [
        {"nombre": "Prof. María García", "cedula": 11111111, "asignatura": "Matemáticas"},
        {"nombre": "Prof. Juan López", "cedula": 22222222, "asignatura": "Español"},
        {"nombre": "Prof. Ana Martínez", "cedula": 33333333, "asignatura": "Inglés"},
        {"nombre": "Prof. Pedro Sánchez", "cedula": 44444444, "asignatura": "Ciencias"},
    ],
    "Instituto Técnico Olga Santamaría - Cundinamarca": [
        {"nombre": "Prof. Laura Rodríguez", "cedula": 55555555, "asignatura": "Matemáticas"},
        {"nombre": "Prof. Carlos Hernández", "cedula": 66666666, "asignatura": "Español"},
        {"nombre": "Prof. Diana Gómez", "cedula": 77777777, "asignatura": "Inglés"},
        {"nombre": "Prof. Roberto Díaz", "cedula": 88888888, "asignatura": "Ciencias"},
    ]
}

# ============================================
# INFORMACIÓN ESCOLAR (SIN CAMBIOS)
# ============================================
info_escolar = {
    "calendario_academico": """
📅 **CALENDARIO ACADÉMICO 2024-2025**

**Primer Semestre:**
- Inicio de clases: 22 de Enero 2024
- Semana de receso: 25-29 de Marzo (Semana Santa)
- Fin primer período: 12 de Abril
- Entrega de boletines: 19 de Abril
- Fin segundo período: 14 de Junio
- Vacaciones mitad de año: 17 Junio - 7 Julio

**Segundo Semestre:**
- Inicio segundo semestre: 8 de Julio
- Semana de receso: 7-11 de Octubre
- Fin tercer período: 13 de Septiembre
- Fin cuarto período: 22 de Noviembre
- Clausura: 29 de Noviembre
    """,
    
    "matriculas": """
📋 **INFORMACIÓN DE MATRÍCULAS**

**Fechas de matrícula 2025:**
- Estudiantes antiguos: 1-15 de Noviembre 2024
- Estudiantes nuevos: 18-30 de Noviembre 2024

**Requisitos:**
1. Fotocopia documento de identidad
2. Certificado de estudios anteriores
3. Fotos 3x4 fondo azul (2 unidades)
4. Certificado médico
5. Paz y salvo año anterior

**Costos:**
- Matrícula: $150.000
- Pensión mensual: $180.000
- Seguro estudiantil: $45.000/año
    """,
    
    "actividades_escolares": """
🎭 **ACTIVIDADES ESCOLARES 2024**

**Próximos eventos:**
- 15 Feb: Día del Amor y la Amistad
- 8 Mar: Día de la Mujer
- 23 Abr: Día del Idioma
- 30 Abr: Día del Niño
- 15 May: Día del Maestro
- 20 Jul: Izadas de bandera - Independencia
- 7 Ago: Batalla de Boyacá
- 12 Oct: Día de la Raza
- 31 Oct: Halloween escolar
- 11 Nov: Festival de talentos
- 29 Nov: Clausura y grados
    """,
    
    "rutas_escolares": """
🚌 **RUTAS ESCOLARES**

**Rutas disponibles:**

**Ruta 1 - Norte:**
- Salida: 6:00 AM
- Paradas: Centro, La Estación, Barrio Norte
- Costo: $120.000/mes

**Ruta 2 - Sur:**
- Salida: 6:15 AM
- Paradas: Terminal, Barrio Sur, La Esperanza
- Costo: $120.000/mes

**Ruta 3 - Oriente:**
- Salida: 6:00 AM
- Paradas: Comuneros, San José, El Prado
- Costo: $130.000/mes

**Contacto transporte:** 310-555-1234
    """,
    
    "horarios": """
⏰ **HORARIOS DE CLASE**

**Jornada Mañana:**
- Entrada: 6:30 AM
- Primera hora: 6:45 - 7:35 AM
- Segunda hora: 7:35 - 8:25 AM
- Descanso: 8:25 - 8:50 AM
- Tercera hora: 8:50 - 9:40 AM
- Cuarta hora: 9:40 - 10:30 AM
- Descanso: 10:30 - 10:50 AM
- Quinta hora: 10:50 - 11:40 AM
- Sexta hora: 11:40 AM - 12:30 PM

**Jornada Tarde:**
- Entrada: 12:30 PM
- Salida: 6:30 PM
    """,
    
    "asignaturas": """
📚 **ASIGNATURAS**

**Áreas Fundamentales:**
- Matemáticas (5 horas/semana)
- Español y Literatura (5 horas/semana)
- Inglés (4 horas/semana)
- Ciencias Naturales (4 horas/semana)
- Ciencias Sociales (3 horas/semana)

**Áreas Complementarias:**
- Educación Física (2 horas/semana)
- Artística (2 horas/semana)
- Tecnología e Informática (2 horas/semana)
- Ética y Valores (1 hora/semana)
- Religión (1 hora/semana)
    """,
    
    "reuniones": """
👥 **REUNIONES DE PADRES**

**Próximas reuniones:**

📌 **Entrega de boletines 1er período:**
- Fecha: 19 de Abril 2024
- Hora: 7:00 AM - 12:00 PM
- Lugar: Salones de clase

📌 **Asamblea general de padres:**
- Fecha: 10 de Mayo 2024
- Hora: 8:00 AM
- Lugar: Auditorio principal

📌 **Escuela de padres:**
- Fechas: Último viernes de cada mes
- Hora: 6:00 PM
- Tema Mayo: "Acompañamiento escolar"
    """,
    
    "fechas_entrega": """
📝 **FECHAS DE ENTREGA**

**Período actual - Abril 2024:**

| Asignatura | Trabajo | Fecha |
|------------|---------|-------|
| Matemáticas | Taller álgebra | 15 Abril |
| Español | Ensayo literario | 18 Abril |
| Inglés | Presentación oral | 20 Abril |
| Ciencias | Proyecto ecosistemas | 22 Abril |
| Sociales | Línea de tiempo | 25 Abril |

**Exámenes finales período:**
- 8-12 de Abril 2024
    """,
    
    "actividades": """
📋 **ACTIVIDADES PENDIENTES**

**Esta semana:**
- Lunes: Quiz de matemáticas
- Martes: Exposición de inglés
- Miércoles: Laboratorio de ciencias
- Jueves: Entrega taller español
- Viernes: Evaluación sociales

**Próxima semana:**
- Preparación día del idioma
- Ensayos grupo de danzas
- Inicio proyecto de feria científica
    """,
    
    "tutoria": f"""
📖 **TUTORÍAS Y REFUERZOS ACADÉMICOS**

¡Excelente que busques apoyo académico! Aquí tienes un recurso de refuerzo:

🎥 **Video de refuerzo recomendado:**
https://www.youtube.com/watch?v=0d5VWxcSUIk

**Horarios de tutorías presenciales:**
- Lunes y Miércoles: 2:00 PM - 4:00 PM (Matemáticas)
- Martes y Jueves: 2:00 PM - 4:00 PM (Español e Inglés)
- Viernes: 2:00 PM - 4:00 PM (Ciencias)

**Para agendar tutoría:**
1. Habla con tu director de grupo
2. Inscríbete en coordinación académica
3. Las tutorías son gratuitas

**Contacto:** coordinacion@colegio.edu.co
    """
}

# ============================================
# INICIALIZAR SESSION STATE
# ============================================
if 'df_all_students' not in st.session_state:
    st.session_state.df_all_students = df_all_students.copy()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'departamento' not in st.session_state:
    st.session_state.departamento = None
if 'colegio' not in st.session_state:
    st.session_state.colegio = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'consultas' not in st.session_state:
    st.session_state.consultas = {
        "calendario": 0, "matriculas": 0, "actividades": 0,
        "rutas": 0, "horarios": 0, "asignaturas": 0,
        "reuniones": 0, "fechas_entrega": 0, "tutoria": 0, 
        "notas": 0, "asistencia": 0, "certificado": 0
    }
if 'privacy_accepted' not in st.session_state:
    st.session_state.privacy_accepted = False

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def generar_certificado_pdf(nombre, cedula, colegio, promedio):
    """Genera un certificado de estudios en PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 20, 'CERTIFICADO DE ESTUDIOS', 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, colegio.upper(), 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_draw_color(0, 0, 128)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(15)
    
    pdf.set_font('Arial', '', 12)
    
    texto = f"""
    El/La rector(a) del {colegio}, 
    
    CERTIFICA QUE:
    
    El/La estudiante {nombre}, identificado(a) con documento 
    de identidad No. {cedula}, se encuentra matriculado(a) 
    y cursando estudios en esta institución educativa durante 
    el año lectivo 2024.
    
    El estudiante presenta un promedio académico de: {promedio:.2f}
    
    Este certificado se expide a solicitud del interesado(a) 
    en la ciudad de Bogotá, a los {datetime.now().day} días 
    del mes de {datetime.now().strftime('%B')} de {datetime.now().year}.
    """
    
    pdf.multi_cell(0, 8, texto)
    pdf.ln(20)
    
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, 'RECTOR(A)', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, colegio, 0, 1, 'C')
    
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, f'Documento generado el {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
    pdf.cell(0, 5, 'Este documento es válido sin firma ni sello para trámites internos', 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

def procesar_pregunta(pregunta):
    """Procesa la pregunta del chatbot y retorna la respuesta apropiada"""
    pregunta_lower = pregunta.lower()
    
    if any(palabra in pregunta_lower for palabra in ['calendario', 'fechas', 'cuando empiezan', 'vacaciones']):
        st.session_state.consultas["calendario"] += 1
        return info_escolar["calendario_academico"]
    
    elif any(palabra in pregunta_lower for palabra in ['matricula', 'inscripción', 'inscribir', 'requisitos matricula']):
        st.session_state.consultas["matriculas"] += 1
        return info_escolar["matriculas"]
    
    elif any(palabra in pregunta_lower for palabra in ['actividad', 'evento', 'celebración', 'festival']):
        st.session_state.consultas["actividades"] += 1
        return info_escolar["actividades_escolares"]
    
    elif any(palabra in pregunta_lower for palabra in ['ruta', 'transporte', 'bus', 'recorrido']):
        st.session_state.consultas["rutas"] += 1
        return info_escolar["rutas_escolares"]
    
    elif any(palabra in pregunta_lower for palabra in ['horario', 'hora', 'jornada', 'entrada', 'salida']):
        st.session_state.consultas["horarios"] += 1
        return info_escolar["horarios"]
    
    elif any(palabra in pregunta_lower for palabra in ['asignatura', 'materia', 'clase', 'área']):
        st.session_state.consultas["asignaturas"] += 1
        return info_escolar["asignaturas"]
    
    elif any(palabra in pregunta_lower for palabra in ['reunión', 'padres', 'citación', 'asamblea']):
        st.session_state.consultas["reuniones"] += 1
        return info_escolar["reuniones"]
    
    elif any(palabra in pregunta_lower for palabra in ['entrega', 'tarea', 'trabajo', 'examen', 'quiz']):
        st.session_state.consultas["fechas_entrega"] += 1
        return info_escolar["fechas_entrega"]
    
    elif any(palabra in pregunta_lower for palabra in ['tutoria', 'tutoría', 'refuerzo', 'ayuda', 'apoyo', 'no entiendo']):
        st.session_state.consultas["tutoria"] += 1
        return info_escolar["tutoria"]
    
    elif any(palabra in pregunta_lower for palabra in ['nota', 'calificación', 'promedio', 'boletin']):
        st.session_state.consultas["notas"] += 1
        
        cedula = st.session_state.user_data['cedula']
        colegio = st.session_state.colegio
        departamento = st.session_state.departamento
        
        df_estudiante = st.session_state.df_all_students[
            (st.session_state.df_all_students['Departamento'] == departamento) &
            (st.session_state.df_all_students['Colegio'] == colegio) &
            (st.session_state.df_all_students['Cedula'] == cedula)
        ]
        
        if not df_estudiante.empty:
            nombre = df_estudiante['Nombre'].iloc[0]
            notas = df_estudiante[['Asignatura', 'Nota_Parcial', 'Nota_Final']]
            promedio_final = df_estudiante['Nota_Final'].mean()
            
            respuesta = f"📊 **Notas de {nombre}**\n\n"
            respuesta += "| Asignatura | Nota Parcial | Nota Final |\n"
            respuesta += "|------------------|-----------|----------|\n"
            
            for _, row in notas.iterrows():
                respuesta += f"| {row['Asignatura']} | {row['Nota_Parcial']} | {row['Nota_Final']} |\n"
            
            respuesta += f"\n📈 **Promedio Final:** {promedio_final:.2f}"
            return respuesta
        else:
            return "❌ No se encontraron notas para tu cédula."
    
    elif any(palabra in pregunta_lower for palabra in ['asistencia', 'clases asistidas']):
        st.session_state.consultas["asistencia"] += 1
        
        cedula = st.session_state.user_data['cedula']
        colegio = st.session_state.colegio
        departamento = st.session_state.departamento
        
        df_estudiante = st.session_state.df_all_students[
            (st.session_state.df_all_students['Departamento'] == departamento) &
            (st.session_state.df_all_students['Colegio'] == colegio) &
            (st.session_state.df_all_students['Cedula'] == cedula)
        ]
        
        if not df_estudiante.empty:
            asistencia_total = df_estudiante['Asistencia'].sum()
            return f"📅 **Asistencia:** Has asistido a **{asistencia_total}** clases en total."
        else:
            return "❌ No se encontró información de asistencia."
    
    elif any(palabra in pregunta_lower for palabra in ['certificado']):
        st.session_state.consultas["certificado"] += 1
        
        cedula = st.session_state.user_data['cedula']
        nombre = st.session_state.user_data['nombre']
        colegio = st.session_state.colegio
        
        df_estudiante = st.session_state.df_all_students[
            (st.session_state.df_all_students['Departamento'] == st.session_state.departamento) &
            (st.session_state.df_all_students['Colegio'] == colegio) &
            (st.session_state.df_all_students['Cedula'] == cedula)
        ]
        
        if not df_estudiante.empty:
            promedio = df_estudiante['Nota_Final'].mean()
            pdf_bytes = generar_certificado_pdf(nombre, cedula, colegio, promedio)
            b64 = base64.b64encode(pdf_bytes).decode()
            return f'<a href="data:application/pdf;base64,{b64}" download="certificado.pdf">📥 Descargar Certificado de Estudios</a>'
        else:
            return "❌ No se pudo generar el certificado."
    
    elif any(palabra in pregunta_lower for palabra in ['dashboard', 'estadísticas', 'resumen']):
        st.session_state.consultas["notas"] += 1
        
        cedula = st.session_state.user_data['cedula']
        colegio = st.session_state.colegio
        departamento = st.session_state.departamento
        
        df_estudiante = st.session_state.df_all_students[
            (st.session_state.df_all_students['Departamento'] == departamento) &
            (st.session_state.df_all_students['Colegio'] == colegio) &
            (st.session_state.df_all_students['Cedula'] == cedula)
        ]
        
        if not df_estudiante.empty:
            nombre = df_estudiante['Nombre'].iloc[0]
            promedio_final = df_estudiante['Nota_Final'].mean()
            asistencia_total = df_estudiante['Asistencia'].sum()
            
            respuesta = f"📊 **Resumen Académico de {nombre}**\n\n"
            respuesta += f"📍 **Departamento:** {departamento}\n"
            respuesta += f"🏫 **Colegio:** {colegio}\n"
            respuesta += f"🆔 **Cédula:** {cedula}\n"
            respuesta += f"📈 **Promedio Final:** {promedio_final:.2f}\n"
            respuesta += f"📅 **Asistencia Total:** {asistencia_total} clases\n\n"
            
            respuesta += "### Próximas Actividades:\n"
            respuesta += "- 📅 15 Abril: Taller de álgebra (Matemáticas)\n"
            respuesta += "- 📅 18 Abril: Ensayo literario (Español)\n"
            respuesta += "- 📅 20 Abril: Presentación oral (Inglés)\n\n"
            
            respuesta += "### Horario de Clases:\n"
            respuesta += "- 📚 6:45 - 7:35 AM: Matemáticas\n"
            respuesta += "- 📚 7:35 - 8:25 AM: Español\n"
            respuesta += "- 📚 8:50 - 9:40 AM: Inglés\n"
            respuesta += "- 📚 9:40 - 10:30 AM: Ciencias\n"
            
            return respuesta
        else:
            return "❌ No se encontró información para generar el dashboard."
    
    elif any(palabra in pregunta_lower for palabra in ['hola', 'buenos dias', 'buenas tardes', 'hey']):
        return f"👋 ¡Hola {st.session_state.user_data['nombre']}! ¿En qué puedo ayudarte hoy? Puedo:\n\n• Ver tus notas y promedios\n• Consultar tu asistencia\n• Generar tu certificado\n• Mostrar un resumen de tu rendimiento\n• Informarte sobre el calendario y actividades\n• Ayudarte con horarios y entregas"
    
    elif any(palabra in pregunta_lower for palabra in ['gracias', 'thank', 'genial']):
        return "😊 ¡Con gusto! Si necesitas más ayuda, solo pregúntame."

    else:
        # RESPUESTAS INTELIGENTES A MÁS PREGUNTAS
        pregunta_lower = pregunta_lower.replace("?", "").replace(".", "").replace("!", "")

        respuestas = {
            # MATRÍCULAS Y COSTOS
            "cuanto cuesta": info_escolar["matriculas"],
            "costo": info_escolar["matriculas"],
            "precio": info_escolar["matriculas"],
            "valor matricula": info_escolar["matriculas"],
            "pago": "💰 Los pagos se realizan en el banco o por PSE. Tienes hasta el 15 de noviembre para estudiantes antiguos. Más detalles:\n\n" + info_escolar["matriculas"],
            "inscribir": info_escolar["matriculas"],
            "requisitos": info_escolar["matriculas"],
            "paz y salvo": "📄 Para paz y salvo debes estar al día en pagos y devolver libros de biblioteca. Acércate a secretaría de 7:00 AM a 12:00 PM.",

            # CALENDARIO Y FESTIVOS
            "dia del idioma": "🗣️ El Día del Idioma se celebra el **23 de abril**. Habrá concurso de poesía y declamación. ¡Prepárate!",
            "halloween": "🎃 ¡Sí! El 31 de octubre celebramos Halloween escolar con desfile de disfraces y actividades divertidas.",
            "dia del niño": "🎈 El Día del Niño es el **30 de abril**. Habrá juegos, refrigerio y sorpresas para todos.",
            "dia de la mujer": "🌸 El 8 de marzo celebramos el Día de la Mujer con actividades especiales.",
            "festivo": "Los festivos nacionales NO hay clases. El próximo es el **Batalla de Boyacá - 7 de agosto** (puente).",
            "vacaciones": info_escolar["calendario_academico"],

            # TRANSPORTE Y RUTAS
            "transporte": info_escolar["rutas_escolares"],
            "bus": info_escolar["rutas_escolares"],
            "ruta": info_escolar["rutas_escolares"],
            "recogerme": "Sí, tenemos 3 rutas escolares. Contáctanos al 310-555-1234 para inscribirte:\n\n" + info_escolar["rutas_escolares"],

            # HORARIOS Y JORNADA
            "a que hora entro": info_escolar["horarios"],
            "a que hora salgo": info_escolar["horarios"],
            "jornada": info_escolar["horarios"],
            "recreo": "🥪 El descanso es de 8:25 a 8:50 AM y de 10:30 a 10:50 AM. ¡Aprovecha para comer algo!",

            # ENTREGAS Y RECUPERACIÓN
            "recuperar": "Sí puedes recuperar notas. Habla con tu profesor para programar una evaluación de recuperación antes del 20 de cada período.",
            "boletines": info_escolar["reuniones"],
            "cuando entregan boletines": info_escolar["reuniones"],
            "tareas pendientes": info_escolar["fechas_entrega"],

            # UBICACIÓN Y CONTACTO
            "direccion": "📍 Estamos ubicados en la carrera 10 # 15-20, centro de la ciudad. ¡Te esperamos!",
            "telefono": "📞 Secretaría: 601-555-0123\nTransporte: 310-555-1234\nCoordinación: coordinacion@colegio.edu.co",
            "donde queda": "Estamos en el centro, cerca de la plaza principal. Carrera 10 # 15-20.",

            # ACTIVIDADES
            "festival": "🎭 El Festival de Talentos es el **11 de noviembre**. ¡Inscribe tu acto en coordinación!",
            "feria de la ciencia": "🔬 La feria científica será en la tercera semana de octubre. ¡Empieza tu proyecto!",
            "clausura": "🎓 La clausura y grados serán el **29 de noviembre**. ¡Los esperamos a todos!",

            # GENERAL
            "hola": f"👋 ¡Hola {st.session_state.user_data['nombre']}! 😊 Soy tu asistente virtual. Pregúntame lo que necesites.",
            "como estas": "¡Excelente! Listo para ayudarte 😄 ¿En qué te colaboro hoy?",
            "gracias": "¡De nada! 😊 Siempre aquí para ayudarte. ¡Que tengas un lindo día!",
        }

        for clave, respuesta in respuestas.items():
            if clave in pregunta_lower:
                # Contar la consulta
                tema = clave.split()[0] if " " in clave else clave
                st.session_state.consultas["otras"] = st.session_state.consultas.get("otras", 0) + 1
                return respuesta

        # Si no entiende nada
        return """🤔 Mmm, esa pregunta aún no la tengo aprendida, ¡pero estoy aprendiendo rápido! 😄

Puedo ayudarte con:
• Notas, promedio y boletines  
• Certificado de estudios  
• Calendario, festivos y vacaciones  
• Matrícula y costos  
• Transporte escolar  
• Horarios y recreos  
• Actividades y eventos  
• Tutorías y recuperación de notas  
• Dirección y teléfonos del colegio  

Escribe tu pregunta de nuevo o elige uno de los botones rápidos 👆 ¡Estoy aquí para ayudarte!"""
    

# ============================================
# PÁGINA DE PRIVACIDAD
# ============================================
def mostrar_aviso_privacidad():
    # Estilos CSS mejorados
    st.markdown("""
    <style>
    /* Fondo degradado más suave y profesional */
    .stApp {
        background: linear-gradient(135deg, #5e60ce 0%, #8f94fb 100%);
    }
    
    /* Contenedor principal */
    .privacy-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
    }
    
    /* Título principal */
    .privacy-title {
        color: white !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Subtítulo */
    .privacy-subtitle {
        color: #e6e6ff !important;
        font-size: 1.3rem !important;
        text-align: center !important;
        margin-bottom: 3rem !important;
        font-weight: 500;
    }
    
    /* Tarjeta de contenido */
    .privacy-card {
        background: white;
        padding: 2.5rem;
        border-radius: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        color: #333;
        position: relative;
        overflow: hidden;
    }
    
    /* Efecto de línea superior en la tarjeta */
    .privacy-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 1.5rem 1.5rem 0 0;
    }
    
    /* Texto de la política */
    .privacy-text {
        text-align: justify;
        line-height: 1.7 !important;
        font-size: 1.1rem !important;
        color: #444;
        margin-bottom: 2rem;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Lista de puntos */
    .privacy-list {
        list-style-type: none;
        padding: 0;
        margin: 1.5rem 0;
    }
    
    .privacy-list li {
        margin: 0.8rem 0;
        padding-left: 2rem;
        position: relative;
        color: #555;
    }
    
    .privacy-list li::before {
        content: "•";
        color: #764ba2;
        font-weight: bold;
        position: absolute;
        left: 0;
    }
    
    /* Contenedor del checkbox */
    .checkbox-container {
        display: flex;
        align-items: center;
        margin: 2.5rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 1rem;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .checkbox-container:hover {
        border-color: #764ba2;
        background: #fff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Label del checkbox */
    .checkbox-label {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #2d3748;
        margin-left: 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Botón mejorado */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem !important;
        border-radius: 0.8rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(102, 110, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 110, 234, 0.4) !important;
    }
    
    .stButton > button:disabled {
        background: #cbd5e0 !important;
        box-shadow: none !important;
        transform: none !important;
    }
    
    /* Icono de privacidad */
    .privacy-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1.5rem;
        color: #fff;
    }
    
    /* Animación para el título */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-title {
        animation: fadeIn 1s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)

    # Contenedor principal
    st.markdown('<div class="privacy-container">', unsafe_allow_html=True)

    # Título con icono
    st.markdown('<div class="privacy-icon">🔒</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="privacy-title animate-title">Aviso de Privacidad</h1>', unsafe_allow_html=True)
    st.markdown('<p class="privacy-subtitle">Protección de tus datos personales</p>', unsafe_allow_html=True)

    # Tarjeta de contenido
    st.markdown('<div class="privacy-card">', unsafe_allow_html=True)

    # Texto principal con mejor formato
    st.markdown("""
    <div class="privacy-text">
        <p style="font-weight: 600; font-size: 1.2rem; margin-bottom: 1.5rem; color: #2d3748;">
            🎯 <strong>PROPÓSITO DEL TRATAMIENTO</strong>
        </p>
        Con el fin de brindarte un servicio educativo de calidad y cumplir con las normativas 
        vigentes, necesitamos que aceptes nuestra política de tratamiento de datos personales 
        conforme a la <strong>Ley 1581 de 2012</strong> de Colombia.
        
        <p style="margin-top: 1.5rem; font-weight: 600; font-size: 1.2rem; color: #2d3748;">
            📌 <strong>DATOS QUE RECOPILAMOS</strong>
        </p>
        Los datos personales que tratamos incluyen:
        
        <ul class="privacy-list">
            <li>Nombre completo</li>
            <li>Número de identificación (cédula)</li>
            <li>Información académica (notas, asignaturas, asistencia)</li>
            <li>Historial de consultas en el sistema</li>
        </ul>
        
        <p style="margin-top: 1.5rem; font-weight: 600; font-size: 1.2rem; color: #2d3748;">
            🛡️ <strong>CÓMO PROTEGEMOS TUS DATOS</strong>
        </p>
        <p>Implementamos medidas técnicas y organizativas de seguridad para proteger tus datos 
        contra la pérdida, destrucción, alteración, revelación o acceso no autorizado.</p>
        
        <p style="margin-top: 1.5rem; font-weight: 600; font-size: 1.2rem; color: #2d3748;">
            📜 <strong>TUS DERECHOS</strong>
        </p>
        <p>En todo momento puedes ejercer tus derechos de:</p>
        
        <ul class="privacy-list">
            <li>Acceso a tus datos</li>
            <li>Rectificación de datos inexactos</li>
            <li>Eliminación de datos</li>
            <li>Limitación del tratamiento</li>
            <li>Revocación del consentimiento</li>
        </ul>
        
        <p style="margin-top: 1.5rem; font-weight: 600; font-size: 1.2rem; color: #2d3748;">
            📞 <strong>CONTACTO</strong>
        </p>
        <p>Para cualquier consulta sobre el tratamiento de tus datos:</p>
        <p style="background: #f0f7ff; padding: 1rem; border-radius: 0.8rem; margin-top: 0.5rem;">
            ✉️ <strong>Correo:</strong> protecciondatos@colegio.edu.co<br>
            📞 <strong>Teléfono:</strong> (601) 555-0123
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Checkbox y botón en columnas
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    
    with col2:
        st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
        checkbox = st.checkbox("", key="privacy_checkbox", label_visibility="collapsed")
        st.markdown('<label class="checkbox-label">He leído y acepto la política de privacidad y protección de datos personales</label>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Botón con condición
        if checkbox:
            if st.button("🚀 Entrar al Sistema", type="primary", use_container_width=True):
                st.session_state.privacy_accepted = True
                st.rerun()
        else:
            st.button("🚀 Entrar al Sistema", type="primary", use_container_width=True, disabled=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Cierre de privacy-card
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre de privacy-container

# ============================================
# USO EN TU APLICACIÓN
# ============================================
# Simplemente llama a la función donde necesites mostrar el aviso
# mostrar_aviso_privacidad()
# ============================================
# PÁGINA DE LOGIN
# ============================================
def mostrar_login():
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .school-card {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        transition: transform 0.3s;
        color: #333;
    }
    .school-card:hover {
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>🏫 Sistema Escolar Interactivo</h1><p>Bienvenido al portal estudiantil</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 📍 Paso 1: Selecciona tu Departamento")
    
    departamento = st.radio(
        "Departamento",
        ["Boyacá", "Cundinamarca"],
        horizontal=True
    )
    
    st.session_state.departamento = departamento
    
    st.markdown("---")
    st.markdown("### 🏫 Paso 2: Selecciona tu Institución")
    
    if departamento == "Boyacá":
        instituciones = ["Colegio Departamental Carlos Giraldo - Boyacá", "Instituto Técnico Olga Santamaría - Boyacá"]
    else:
        instituciones = ["Colegio Departamental Carlos Giraldo - Cundinamarca", "Instituto Técnico Olga Santamaría - Cundinamarca"]
    
    institucion = st.radio(
        "Institución",
        instituciones,
        horizontal=True
    )
    
    st.session_state.colegio = institucion
    
    st.success(f"✅ Departamento e institución seleccionados")
    
    st.markdown("---")
    st.markdown("### 👤 Paso 3: Selecciona tu rol")
    
    user_type = st.radio(
        "¿Eres estudiante, profesor o padre de familia?",
        ["Estudiante", "Profesor", "Padre de familia"],
        horizontal=True
    )
    
    st.markdown("---")
    st.markdown("### 🔐 Paso 4: Ingresa tu número de cédula")
    
    if user_type == "Padre de familia":
        st.info("📌 Ingresa la cédula de **tu hijo** para acceder a su información")
        cedula = st.text_input("Número de cédula del hijo:", placeholder="Ej: 12345678")
    else:
        cedula = st.text_input("Número de cédula:", placeholder="Ej: 12345678")
    
    if st.button("🚀 Ingresar al Sistema", type="primary", use_container_width=True):
        if cedula:
            try:
                cedula_num = int(cedula)
                
                # Filtrar por departamento y institución seleccionada
                df_buscar = st.session_state.df_all_students[
                    (st.session_state.df_all_students['Departamento'] == st.session_state.departamento) & 
                    (st.session_state.df_all_students['Colegio'] == st.session_state.colegio)
                ]
                
                if user_type == "Estudiante" or user_type == "Padre de familia":
                    estudiante = df_buscar[df_buscar['Cedula'] == cedula_num]
                    
                    if not estudiante.empty:
                        st.session_state.logged_in = True
                        st.session_state.user_type = "estudiante" if user_type == "Estudiante" else "padre"
                        st.session_state.user_data = {
                            "nombre": estudiante['Nombre'].iloc[0],
                            "cedula": cedula_num,
                            "colegio": st.session_state.colegio,
                            "departamento": st.session_state.departamento
                        }
                        st.rerun()
                    else:
                        st.error("❌ Cédula no encontrada en esta institución.")
                else:  # Profesor
                    profesores = profesores_data.get(st.session_state.colegio, [])
                    profesor = next((p for p in profesores if p['cedula'] == cedula_num), None)
                    
                    if profesor:
                        st.session_state.logged_in = True
                        st.session_state.user_type = "profesor"
                        st.session_state.user_data = {
                            "nombre": profesor['nombre'],
                            "cedula": cedula_num,
                            "asignatura": profesor['asignatura'],
                            "colegio": st.session_state.colegio,
                            "departamento": st.session_state.departamento
                        }
                        st.rerun()
                    else:
                        st.error("❌ Cédula de profesor no encontrada en esta institución.")
                        
            except ValueError:
                st.error("❌ Por favor ingresa un número de cédula válido.")
        else:
            st.warning("⚠️ Por favor ingresa tu número de cédula.")

# ============================================
# DASHBOARD ESTUDIANTE
# ============================================
def mostrar_dashboard_estudiante():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/student-male--v1.png", width=80)
        if st.session_state.user_type == "padre":
            st.markdown(f"### 👨 👩 👧 👦 Accediendo como Padre de Familia")
            st.markdown(f"📌 Información de tu hijo")
        else:
            st.markdown(f"### 👋 ¡Hola, {st.session_state.user_data['nombre']}!")
        
        st.markdown(f"📍 {st.session_state.departamento} | {st.session_state.colegio}")
        if st.session_state.user_type != "padre":
            st.markdown(f"🆔 C.C. {st.session_state.user_data['cedula']}")
        st.markdown("---")
        
        menu = st.radio(
            "📌 Menú",
            ["💬 Chat Bot", "📊 Mis Notas", "📜 Certificado", "📈 Dashboard", "🔒 Privacidad"]
        )
        
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_data = None
            st.session_state.chat_history = []
            st.rerun()
    
    if menu == "💬 Chat Bot":
        mostrar_chatbot()
    elif menu == "📊 Mis Notas":
        mostrar_notas()
    elif menu == "📜 Certificado":
        mostrar_certificado()
    elif menu == "📈 Dashboard":
        mostrar_dashboard_stats()
    elif menu == "🔒 Privacidad":
        mostrar_info_privacidad()

def mostrar_chatbot():
    st.title("Asistente Virtual Escolar")
    st.markdown("Pregúntame sobre notas, asistencias, certificados, calendario y más.")

    # Contenedor del historial del chat
    chat_container = st.container()

    with chat_container:
        for mensaje in st.session_state.chat_history:
            if mensaje["role"] == "user":
                # Mensaje del usuario → derecha, verde tipo WhatsApp
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #25d366, #128c7e);
                    color: white;
                    padding: 12px 18px;
                    border-radius: 20px;
                    margin: 12px 0;
                    max-width: 75%;
                    margin-left: auto;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                    font-size: 15px;
                ">
                    <strong>Tú:</strong> {mensaje["content"]}
                </div>
                """, unsafe_allow_html=True)

            else:
                # Mensaje del asistente → izquierda
                if isinstance(mensaje["content"], str) and "download=" in mensaje["content"]:
                    # Caso especial: enlace de descarga del certificado
                    st.markdown(f"""
                    <div style="
                        background-color: #2c3e50;
                        color: #ecf0f1;
                        padding: 16px 20px;
                        border-radius: 20px;
                        margin: 12px 0;
                        max-width: 85%;
                        border-left: 5px solid #3498db;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                    ">
                        <strong style="color:#3498db;">Asistente:</strong><br><br>
                        {mensaje["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Mensaje normal del asistente
                    st.markdown(f"""
                    <div style="
                        background-color: #2c3e50;
                        color: #ecf0f1;
                        padding: 14px 18px;
                        border-radius: 20px;
                        margin: 12px 0;
                        max-width: 85%;
                        border-left: 5px solid #2ecc71;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                        line-height: 1.5;
                        font-size: 15px;
                    ">
                        <strong style="color:#2ecc71;">Asistente:</strong><br><br>
                        {mensaje["content"]}
                    </div>
                    """, unsafe_allow_html=True)

        # Scroll automático al final (opcional pero muy útil)
        js = '''
        <script>
            const container = window.parent.document.querySelector(".main");
            container.scrollTop = container.scrollHeight;
        </script>
        '''
        st.components.v1.html(js, height=0)

    st.markdown("---")

    # Botones rápidos
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Calendario", use_container_width=True):
            pregunta = "calendario académico"
            respuesta = procesar_pregunta(pregunta)
            st.session_state.chat_history.append({"role": "user", "content": "Mostrar calendario"})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.rerun()

    with col2:
        if st.button("Horarios", use_container_width=True):
            pregunta = "horarios"
            respuesta = procesar_pregunta(pregunta)
            st.session_state.chat_history.append({"role": "user", "content": "Mostrar horarios"})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.rerun()

    with col3:
        if st.button("Tutorías", use_container_width=True):
            pregunta = "tutoria refuerzo"
            respuesta = procesar_pregunta(pregunta)
            st.session_state.chat_history.append({"role": "user", "content": "Información de tutorías"})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.rerun()

    with col4:
        if st.button("Dashboard", use_container_width=True):
            pregunta = "dashboard resumen"
            respuesta = procesar_pregunta(pregunta)
            st.session_state.chat_history.append({"role": "user", "content": "Mostrar mi dashboard"})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.rerun()

    # === CHAT CON ENTER AUTOMÁTICO ===
    pregunta = st.chat_input("Escribe tu mensaje aquí y presiona Enter para enviar")

    if pregunta:
        respuesta = procesar_pregunta(pregunta)
        st.session_state.chat_history.append({"role": "user", "content": pregunta})
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        st.rerun()

    # Botón limpiar conversación
    if st.button("Limpiar conversación", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

def mostrar_notas():
    st.title("📊 Mis Notas y Calificaciones")
    
    cedula = st.session_state.user_data['cedula']
    colegio = st.session_state.colegio
    departamento = st.session_state.departamento
    
    df_estudiante = st.session_state.df_all_students[
        (st.session_state.df_all_students['Departamento'] == departamento) & 
        (st.session_state.df_all_students['Colegio'] == colegio) & 
        (st.session_state.df_all_students['Cedula'] == cedula)
    ]
    
    if not df_estudiante.empty:
        st.markdown(f"### 👤 Estudiante: {df_estudiante['Nombre'].iloc[0]}")
        st.markdown(f"📍 {departamento} | {colegio}")
        
        st.markdown("---")
        
        notas_display = df_estudiante[['Asignatura', 'Nota_Parcial', 'Nota_Final']].copy()
        notas_display.columns = ['Asignatura', 'Nota Parcial', 'Nota Final']
        
        st.dataframe(notas_display, hide_index=True, use_container_width=True)
        
        promedio_parcial = df_estudiante['Nota_Parcial'].mean()
        promedio_final = df_estudiante['Nota_Final'].mean()
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Promedio Parcial", f"{promedio_parcial:.2f}")
        
        with col2:
            st.metric("📈 Promedio Final", f"{promedio_final:.2f}")
        
        with col3:
            estado = "✅ Aprobado" if promedio_final >= 6 else "⚠️ En riesgo"
            st.metric("📋 Estado", estado)
        
        st.markdown("---")
        
        st.markdown("#### 📈 Gráfico de Rendimiento")
        
        
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Nota Parcial',
            x=df_estudiante['Asignatura'],
            y=df_estudiante['Nota_Parcial'],
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            name='Nota Final',
            x=df_estudiante['Asignatura'],
            y=df_estudiante['Nota_Final'],
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            barmode='group',
            title='Comparación de Notas por Asignatura',
            xaxis_title='Asignatura',
            yaxis_title='Nota',
            yaxis_range=[0, 10]
        )
        
        st.plotly_chart(fig, use_container_width=True)

def mostrar_certificado():
    st.title("📜 Certificado de Estudios")
    
    st.markdown("""
    Genera y descarga tu certificado de estudios oficial. Este documento certifica 
    tu matrícula activa en la institución educativa.
    """)
    
    cedula = st.session_state.user_data['cedula']
    nombre = st.session_state.user_data['nombre']
    colegio = st.session_state.colegio
    departamento = st.session_state.departamento
    
    df_estudiante = st.session_state.df_all_students[
        (st.session_state.df_all_students['Departamento'] == departamento) & 
        (st.session_state.df_all_students['Colegio'] == colegio) & 
        (st.session_state.df_all_students['Cedula'] == cedula)
    ]
    
    promedio = df_estudiante['Nota_Final'].mean()
    
    st.markdown("---")
    
    st.markdown("### 📄 Vista Previa del Certificado")
    
    st.markdown(f"""
    <div style="background-color: #fffbf0; padding: 30px; border: 2px solid #d4a574; border-radius: 10px;">
        <h2 style="text-align: center; color: #1a3a5c;">CERTIFICADO DE ESTUDIOS</h2>
        <h3 style="text-align: center; color: #2c5282;">{colegio.upper()}</h3>
        <hr style="border-color: #d4a574;">
        <p style="text-align: justify; font-size: 14px;">
            El/La rector(a) del {colegio}, 
            <strong>CERTIFICA QUE:</strong>
        </p>
        <p style="text-align: center; font-size: 16px;">
            El/La estudiante <strong>{nombre}</strong>, identificado(a) con documento 
            de identidad No. <strong>{cedula}</strong>, se encuentra matriculado(a) 
            y cursando estudios en esta institución educativa durante el año lectivo 2024.
        </p>
        <p style="text-align: center; font-size: 14px;">
            Promedio académico actual: <strong>{promedio:.2f}</strong>
        </p>
        <p style="text-align: center; font-size: 12px; color: #666;">
            Expedido el {datetime.now().strftime('%d de %B de %Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("📥 Descargar Certificado PDF", type="primary", use_container_width=True):
        pdf_bytes = generar_certificado_pdf(nombre, cedula, colegio, promedio)
        
        st.download_button(
            label="💾 Guardar PDF",
            data=pdf_bytes,
            file_name=f"certificado_{nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        st.success("✅ ¡Certificado generado exitosamente!")

def mostrar_dashboard_stats():
    st.title("📈 Dashboard de Estadísticas")
    
    st.markdown("### 📊 Temas Más Consultados")
    
    consultas_df = pd.DataFrame({
        'Tema': list(st.session_state.consultas.keys()),
        'Consultas': list(st.session_state.consultas.values())
    })
    
    
    fig = px.bar(consultas_df, x='Tema', y='Consultas', 
                 title='Frecuencia de Consultas por Tema',
                 color='Consultas',
                 color_continuous_scale='Blues')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📚 Promedios por Asignatura (Todos los Estudiantes)")
    
    promedios_asignatura = st.session_state.df_all_students.groupby(['Departamento', 'Colegio', 'Asignatura'])['Nota_Final'].mean().reset_index()
    
    fig2 = px.bar(promedios_asignatura, x='Asignatura', y='Nota_Final', 
                  color='Colegio', 
                  title='Distribución de Promedios por Asignatura y Colegio',
                  labels={'Nota_Final': 'Promedio Final', 'Asignatura': 'Asignatura'})
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 👥 Ranking de Estudiantes")
    
    ranking = st.session_state.df_all_students.groupby(['Departamento', 'Colegio', 'Nombre', 'Cedula'])['Nota_Final'].mean().reset_index()
    ranking = ranking.sort_values('Nota_Final', ascending=False)
    ranking.columns = ['Departamento', 'Colegio', 'Nombre', 'Cédula', 'Promedio']
    ranking['Posición'] = range(1, len(ranking) + 1)
    
    st.dataframe(ranking[['Posición', 'Departamento', 'Colegio', 'Nombre', 'Promedio']], hide_index=True, use_container_width=True)

def mostrar_info_privacidad():
    st.title("🔒 Política de Privacidad")
    
    st.markdown("""
    ### Tus Datos Están Protegidos

    En nuestra institución nos tomamos muy en serio la protección de tus datos personales.
    
    #### 📋 Datos que manejamos:
    - Nombre completo
    - Número de identificación (cédula)
    - Calificaciones académicas
    - Historial de consultas
    
    #### 🛡️ Cómo protegemos tu información:
    - Acceso solo con autenticación
    - Datos encriptados
    - No compartimos con terceros
    - Cumplimiento de Ley 1581 de 2012
    
    #### ✅ Tus derechos:
    - Acceder a tu información
    - Corregir datos incorrectos
    - Solicitar eliminación
    - Revocar autorización
    
    #### 📞 Contacto:
    Para ejercer tus derechos o consultas sobre esta política:
    - Email: protecciondatos@colegio.edu.co
    - Teléfono: (601) 555-0123
    """)

# ============================================
# DASHBOARD PROFESOR
# ============================================
def mostrar_dashboard_profesor():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/teacher.png", width=80)
        st.markdown(f"### 👋 ¡Hola, {st.session_state.user_data['nombre']}!")
        st.markdown(f"📚 {st.session_state.user_data['asignatura']}")
        st.markdown(f"📍 {st.session_state.departamento} | {st.session_state.colegio}")
        st.markdown("---")
        
        menu = st.radio(
            "📌 Menú",
            ["📊 Ver Estudiantes", "📈 Estadísticas", "🔒 Privacidad"]
        )
        
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_data = None
            st.rerun()
    
    if menu == "📊 Ver Estudiantes":
        st.title("📊 Lista de Estudiantes")
        
        df_mostrar = st.session_state.df_all_students[
            (st.session_state.df_all_students['Departamento'] == st.session_state.departamento) & 
            (st.session_state.df_all_students['Colegio'] == st.session_state.colegio)
        ]
        
        asignatura = st.session_state.user_data['asignatura']
        df_asignatura = df_mostrar[df_mostrar['Asignatura'] == asignatura].copy()
        
        edited_df = st.data_editor(
            df_asignatura[['Nombre', 'Cedula', 'Nota_Parcial', 'Nota_Final', 'Asistencia']],
            key="editor",
            use_container_width=True,
            num_rows="fixed"
        )
        
        if st.button("💾 Guardar Cambios", type="primary", use_container_width=True):
            for index, row in edited_df.iterrows():
                mask = (df_mostrar['Cedula'] == row['Cedula']) & (df_mostrar['Asignatura'] == asignatura)
                df_mostrar.loc[mask, ['Nota_Parcial', 'Nota_Final', 'Asistencia']] = row[['Nota_Parcial', 'Nota_Final', 'Asistencia']]
            
            st.session_state.df_all_students = df_mostrar[
                (df_mostrar['Departamento'] == st.session_state.departamento) & 
                (df_mostrar['Colegio'] == st.session_state.colegio)
            ]
                
            st.success("✅ Cambios guardados exitosamente.")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📈 Resumen de la Clase")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Promedio", f"{df_asignatura['Nota_Final'].mean():.2f}")
        with col2:
            st.metric("📈 Mejor Nota", f"{df_asignatura['Nota_Final'].max():.2f}")
        with col3:
            st.metric("📉 Peor Nota", f"{df_asignatura['Nota_Final'].min():.2f}")
            
    elif menu == "📈 Estadísticas":
        st.title("📈 Estadísticas de la Clase")
        
        df_mostrar = st.session_state.df_all_students[
            (st.session_state.df_all_students['Departamento'] == st.session_state.departamento) & 
            (st.session_state.df_all_students['Colegio'] == st.session_state.colegio)
        ]
        
        asignatura = st.session_state.user_data['asignatura']
        df_asignatura = df_mostrar[df_mostrar['Asignatura'] == asignatura]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Promedio Clase", f"{df_asignatura['Nota_Final'].mean():.2f}")
        with col2:
            st.metric("📈 Nota Máxima", f"{df_asignatura['Nota_Final'].max():.2f}")
        with col3:
            st.metric("📉 Nota Mínima", f"{df_asignatura['Nota_Final'].min():.2f}")
            
        st.markdown("---")
        
        import plotly.express as px
        fig = px.histogram(df_asignatura, x="Nota_Final", nbins=10, 
                          title="Distribución de Notas Finales",
                          labels={"Nota_Final": "Nota Final"},
                          color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig, use_container_width=True)
        
    elif menu == "🔒 Privacidad":
        mostrar_info_privacidad()

# ============================================
# MAIN APP
# ============================================
def main():
    if not st.session_state.privacy_accepted:
        mostrar_aviso_privacidad()
    elif not st.session_state.logged_in:
        mostrar_login()
    elif st.session_state.user_type == "estudiante":
        mostrar_dashboard_estudiante()
    elif st.session_state.user_type == "padre":
        mostrar_dashboard_estudiante()  # Usamos la misma función, pero con mensaje de padre
    elif st.session_state.user_type == "profesor":
        mostrar_dashboard_profesor()

# ============================================
# BOTÓN FLOTANTE WHATSAPP - VERSIÓN CORREGIDA Y BONITA
# ============================================
def whatsapp_flotante():
    if not st.session_state.get('logged_in', False):
        return
        
    numero_whatsapp = "573102223334"  # ← Cambia por el número real del colegio
    nombre = st.session_state.user_data.get('nombre', 'un estudiante')
    colegio = st.session_state.get('colegio', 'la institución')
    
    mensaje = f"Hola, soy {nombre} del {colegio}. Necesito ayuda con:"
    enlace = f"https://wa.me/{numero_whatsapp}?text={mensaje.replace(' ', '%20')}"

    st.markdown(f"""
    <style>
    .whatsapp-flotante {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
    }}
    .whatsapp-btn {{
        width: 60px;
        height: 60px;
        background-color: #25D366;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    .whatsapp-btn:hover {{
        transform: scale(1.2);
        box-shadow: 0 8px 25px rgba(37,211,102,0.6);
    }}
    .tooltip {{
        position: absolute;
        bottom: 80px;
        right: 0;
        background-color: #128C7E;
        color: white;
        padding: 12px 16px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: bold;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        transform: translateY(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }}
    .whatsapp-btn:hover + .tooltip {{
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }}
    </style>

    <div class="whatsapp-flotante">
        <a href="{enlace}" target="_blank">
            <div class="whatsapp-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="38">
            </div>
        </a>
        <div class="tooltip">
            ¿Deseas hablar con la línea de atención al estudiante?
        </div>
    </div>
    """, unsafe_allow_html=True)

# Llamar al botón solo cuando esté logueado
if st.session_state.get('logged_in', False):
    whatsapp_flotante()

if __name__ == "__main__":
    main()
