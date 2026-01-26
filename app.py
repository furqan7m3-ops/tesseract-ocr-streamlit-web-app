import streamlit as st
from OCR.text_extractor import extract_text


st.title('Tesseract Text Extractor OCR')
uploaded_img=st.file_uploader('Upload File', type=['png','jpg','jpeg','gif','bmp'])
if uploaded_img:
    button = st.button("Extract Text")
    if button:
        with st.spinner("Processing image..."):
            text = extract_text(uploaded_img)
        st.markdown('### Extracted Text')
        st.write(text)
    
