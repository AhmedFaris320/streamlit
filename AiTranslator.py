import streamlit as st
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key="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",  # or rely on environment variable
    model="llama-3.3-70b-versatile"         # example model, you can change
)
st.title("AI Translator App")
st.divider()
st.subheader("Enter text to translate") 
user_input = st.text_area("Enter text here", height=200)
source_lang = st.selectbox("Select source language", ["English", "Spanish", "French", "German", "Chinese"])
target_lang = st.selectbox("Select target language", ["English", "Spanish", "French", "German", "Chinese"])

def translate_text(text, source_lang, target_lang):
    prompt = f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}\n\nTranslation:"
    response = llm.predict(prompt)
    return response

if st.button("Translate"):
        if user_input:
            translation = translate_text(user_input, source_lang, target_lang)
            st.subheader("Translation")
            st.write(translation)
