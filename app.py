import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import playsound

# Set your OpenAI API key here
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to transcribe audio to text
def transcribe_audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        st.success("Audio captured!")
        try:
            st.info("Transcribing audio...")
            text = recognizer.recognize_google(audio)
            st.success(f"Transcription: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Could not request results from the speech recognition service.")
            return None

# Function to generate a response from OpenAI
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response['choices'][0]['message']['content'].strip()
    return reply

# Function to convert text to speech and play it
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        playsound.playsound(tmp_file.name)
        os.remove(tmp_file.name)

# Streamlit app interface
st.title("Voice Assistant GPT Interface")

# Button to record and process audio
if st.button("Speak and Get Response"):
    user_input = transcribe_audio_to_text()
    if user_input:
        response = get_openai_response(user_input)
        st.text_area("Assistant's Response:", response)
        speak_text(response)

st.markdown("Developed with ❤️ using Streamlit and OpenAI API")
