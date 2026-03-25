import streamlit as st
import google.generativeai as genai
import PyPDF2
import tempfile
import os

st.set_page_config(page_title="الباحث الذكي", page_icon="📚")
st.title("📚 الباحث الذكي")

api_key = st.sidebar.text_input("مفتاح Gemini API", type="password")
if not api_key:
    st.sidebar.warning("أدخل مفتاح API")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    
    with open(tmp_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    
    os.unlink(tmp_path)
    
    st.success(f"تم استخراج {len(text)} حرفاً")
    
    question = st.text_input("سؤالك:")
    if question:
        with st.spinner("جاري الإجابة..."):
            prompt = f"أجب بناءً على النص: {text[:3000]}\n\nالسؤال: {question}"
            response = model.generate_content(prompt)
            st.write(response.text)
