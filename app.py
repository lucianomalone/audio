import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment

# Função para converter áudio para texto
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()

    # Verifica o tipo de arquivo e converte para .wav se necessário
    if audio_file.name.endswith('.ogg') or audio_file.name.endswith('.mp3'):
        audio = AudioSegment.from_file(audio_file)
        audio = audio.set_channels(1)  # Converter para mono se for estéreo
        audio.export("temp.wav", format="wav")
        audio_file = "temp.wav"

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='pt-BR')
            return text
        except sr.UnknownValueError:
            return "Não foi possível entender o áudio."
        except sr.RequestError:
            return "Não foi possível completar a requisição. Verifique sua conexão com a internet."

# Configuração da interface do Streamlit
st.title("Conversor de Áudio para Texto")

st.write("Selecione um arquivo de áudio no formato .ogg ou .mp3 para convertê-lo em texto.")

uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["ogg", "mp3"])

if uploaded_file is not None:
    st.write(f"Arquivo carregado: {uploaded_file.name}")
    st.write("Realizando a conversão, por favor, aguarde...")
    
    text_output = audio_to_text(uploaded_file)
    
    st.write("Texto extraído:")
    st.text_area("Resultado", value=text_output, height=200)
