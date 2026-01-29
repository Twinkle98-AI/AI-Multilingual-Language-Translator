import streamlit as st
from mtranslate import translate
import pandas as pd
from gtts import gTTS
import base64

# -------------------- LOAD DATA --------------------
df = pd.read_csv("C:/Users/Twinkele/OneDrive/Desktop/lang_translate/language.csv")
df.dropna(inplace=True)

# Convert to dict
lang_dict = dict(zip(df['name'], df['iso']))

# Force add missing languages
extra_langs = {
    "Sanskrit": "sa",
    "Malayalam": "ml",
    "Odia": "or",
    "Konkani": "kok"
}

lang_dict.update(extra_langs)
lang_names = sorted(lang_dict.keys())

# -------------------- SPEECH SUPPORTED LANGS --------------------
speech_langs = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "mr": "Marathi",
    "kn": "Kannada",
    "gu": "Gujarati",
    "bn": "Bengali",
    "ur": "Urdu",
    "sa": "Sanskrit",
    "or": "Odia"
}

# -------------------- UTILITY --------------------
def get_download_link(file):
    with open(file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="{file}">Download Audio</a>'

# -------------------- UI --------------------
st.title("🌍 AI Language Translator")

input_text = st.text_area("Enter text to translate", height=120)
choice = st.selectbox("Select Target Language", lang_names)

col1, col2 = st.columns(2)

# -------------------- LOGIC --------------------
if input_text:
    try:
        selected_code = lang_dict[choice]

        # Konkani fallback
        if selected_code == "kok":
            st.warning("Konkani speech not supported. Using Marathi.")
            selected_code = "mr"

        # Odia warning
        if selected_code == "or":
            st.warning("Odia translation is limited in mtranslate.")

        translated_text = translate(input_text, selected_code)

        with col1:
            st.text_area("Translated Text", translated_text, height=200)

        if selected_code in speech_langs:
            tts = gTTS(text=translated_text, lang=selected_code)
            tts.save("audio.mp3")

            with col2:
                st.audio("audio.mp3")
                st.markdown(get_download_link("audio.mp3"), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")

