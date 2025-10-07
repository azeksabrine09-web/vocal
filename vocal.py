import streamlit as st
import speech_recognition as sr
import threading
import time

st.set_page_config(page_title="Reconnaissance vocale", page_icon="🎙️", layout="centered")


paused = False
transcription = ""


def toggle_pause():
    global paused
    paused = not paused
    return "⏸️ En pause" if paused else "▶️ Reprise"

def transcribe_speech(language='fr-FR'):
    global transcription
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    st.info(f"Reconnaissance vocale démarrée ({language}) — Parlez maintenant...")
    transcription = ""

    try:
        while not paused:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            try:
                text = recognizer.recognize_google(audio, language=language)
                st.write(f"🗣️ Vous avez dit : **{text}**")
                transcription += text + "\n"
            except sr.UnknownValueError:
                st.warning("⚠️ Je n’ai pas compris, essayez de répéter.")
            except sr.RequestError as e:
                st.error(f"❌ Erreur API : {e}")
                break

    except Exception as e:
        st.error(f"Erreur inattendue : {e}")

def save_text():
    global transcription
    filename = st.text_input("Nom du fichier pour enregistrer :", "transcription.txt")
    if st.button("💾 Enregistrer le texte"):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(transcription)
            st.success(f"✅ Transcription enregistrée dans `{filename}`")
        except Exception as e:
            st.error(f"Erreur lors de l'enregistrement : {e}")

# --- Interface Streamlit ---
st.title("🎙️ Application de reconnaissance vocale")
st.write("Cette application vous permet de **parler** et de voir votre **texte transcrit en direct**.")

language = st.selectbox("Choisissez la langue :", ["fr-FR", "en-US", "es-ES", "de-DE", "it-IT"])

col1, col2, col3 = st.columns(3)

if col1.button("▶️ Démarrer"):
    threading.Thread(target=transcribe_speech, args=(language,), daemon=True).start()

if col2.button("⏸️ Pause / Reprise"):
    st.info(toggle_pause())

if col3.button("🛑 Arrêter"):
    paused = True
    st.warning("Reconnaissance arrêtée.")

st.divider()
save_text()
