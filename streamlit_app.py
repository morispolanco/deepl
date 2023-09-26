import streamlit as st
import requests
import docx2txt
from docx import Document
from io import BytesIO

# Cambiar el título en la pestaña del navegador
st.set_page_config(page_title="DeepLTranslate", layout="centered")

# URL base de la API de DeepL
BASE_URL = "https://api-free.deepl.com/v2/translate"

# Función para traducir texto
def translate_text(text, target_lang, auth_key):
    url = f"{BASE_URL}"
    headers = {'Authorization': f'DeepL-Auth-Key {auth_key}'}
    data = {
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        translation = response.json()["translations"][0]["text"]
        detected_source_language = response.json()["translations"][0]["detected_source_language"]
        return translation, detected_source_language
    else:
        return None, None

# Título de la aplicación
st.title("DeepLTranslate")

# Agregar título y texto en la parte superior
st.markdown("## La mejor traducción automática del mundo")
st.markdown("Las redes neuronales de DeepLTranslate son capaces de captar hasta los más mínimos matices y reproducirlos en la traducción a diferencia de cualquier otro servicio. Para evaluar la calidad de nuestros modelos de traducción automática, realizamos regularmente pruebas a ciegas. En las pruebas a ciegas, los traductores profesionales seleccionan la traducción más precisa sin saber qué empresa la produjo. DeepLTranslate supera a la competencia por un factor de 3:1.")

# Cargar archivo DOCX
uploaded_file = st.file_uploader("Cargar archivo DOCX", type=["docx"])

# Selección de idioma de destino
target_lang = st.selectbox("Seleccione el idioma de destino:", ["DE", "ES", "IT", "EN", "FR"])

# Clave de autenticación de DeepL
auth_key = st.text_input("Ingrese su clave de autenticación de DeepL:")

# Botón para traducir
if st.button("Traducir"):
    if auth_key and uploaded_file is not None:
        # Leer el contenido del archivo DOCX
        text = docx2txt.process(uploaded_file)

        translation, detected_source_language = translate_text(text, target_lang, auth_key)
        if translation:
            # Crear un nuevo documento DOCX con la traducción
            translated_docx = Document()
            translated_docx.add_paragraph(translation)

            # Guardar el documento DOCX en un objeto BytesIO
            docx_buffer = BytesIO()
            translated_docx.save(docx_buffer)
            docx_buffer.seek(0)

            # Descargar el archivo DOCX
            st.download_button("Descargar traducción", data=docx_buffer, file_name="traduccion.docx")
        else:
            st.error("Error al traducir el texto. Verifique su clave de autenticación o intente nuevamente.")
    else:
        st.error("Por favor, cargue un archivo DOCX y ingrese una clave de autenticación de DeepL válida.")
