import streamlit as st
from PIL import Image
from io import BytesIO

from OCR.text_extractor import extract_text, extract_text_with_formatting
from OCR.image_preprocessor import (
    preprocess_image,
    preprocess_with_otsu,
    preprocess_with_fixed_threshold,
    optimal_pipeline,
    enhance_contrast
)
from OCR.word_generator import create_ocr_document_bytes


st.set_page_config(page_title='Tesseract Text Extractor OCR', layout='wide')
st.title('Tesseract Text Extractor OCR')

uploaded_file = st.file_uploader('Upload image', type=['png', 'jpg', 'jpeg', 'gif', 'bmp'])

if uploaded_file:
    # Load as PIL Image for preview and processing
    original_image = Image.open(uploaded_file).convert('RGB')
    st.image(original_image, caption='Original image', use_column_width=False, width=400)

    st.sidebar.header('Preprocessing')
    method = st.sidebar.selectbox('Threshold method', ['adaptive', 'otsu', 'fixed', 'none', 'optimal'])
    denoise = st.sidebar.checkbox('Denoise', value=True)
    enhance = st.sidebar.checkbox('Enhance contrast (CLAHE)', value=False)
    fixed_value = None
    if method == 'fixed':
        fixed_value = st.sidebar.slider('Fixed threshold value', 50, 220, 150)

    st.sidebar.header('OCR options')
    detect_formatting = st.sidebar.checkbox('Detect formatting (bold/italic/alignment)', value=False)

    # Preprocess actions
    if st.sidebar.button('Run Preprocess') or method == 'optimal':
        with st.spinner('Preprocessing...'):
            img = original_image
            if enhance:
                img = enhance_contrast(img)

            if method == 'adaptive':
                pre_img = preprocess_image(img, resize_scale=2.0, denoise=denoise, threshold_method='adaptive')
            elif method == 'otsu':
                pre_img = preprocess_with_otsu(img, resize_scale=2.0, denoise=denoise)
            elif method == 'fixed':
                pre_img = preprocess_with_fixed_threshold(img, resize_scale=2.0, denoise=denoise, threshold_value=fixed_value)
            elif method == 'optimal':
                pre_img = optimal_pipeline(img)
            else:
                # no thresholding, only optional denoise/resize
                pre_img = preprocess_image(img, resize_scale=2.0, denoise=denoise, threshold_method='fixed')

            # Show preprocessed preview
            buf = BytesIO()
            pre_img.save(buf, format='PNG')
            st.image(buf.getvalue(), caption='Preprocessed image', use_column_width=False, width=400)

            st.success('Preprocessing complete')

    # Extract text
    if st.button('Extract Text'):
        with st.spinner('Running OCR...'):
            try:
                # prefer formatting-aware extractor if requested
                if detect_formatting:
                    result = extract_text_with_formatting(uploaded_file)
                    text = result.get('text', '')
                    st.markdown('### Extracted Text (with formatting)')
                    st.write(text)
                    st.json({
                        'alignment': result.get('alignment'),
                        'confidence': result.get('confidence'),
                        'properties': result.get('properties')
                    })

                    # Export to Word
                    try:
                        doc_bytes = create_ocr_document_bytes(result)
                        st.download_button(
                            label='📄 Download Word (.docx)',
                            data=doc_bytes,
                            file_name='ocr_output.docx',
                            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                        )
                    except Exception as e:
                        st.error(f'Could not create Word document: {e}')
                else:
                    # pass the original file-like object or preprocessed image if available
                    text = extract_text(original_image)
                    st.markdown('### Extracted Text')
                    st.write(text)

                    # Export to Word
                    try:
                        doc_bytes = create_ocr_document_bytes(text)
                        st.download_button(
                            label='📄 Download Word (.docx)',
                            data=doc_bytes,
                            file_name='ocr_output.docx',
                            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                        )
                    except Exception as e:
                        st.error(f'Could not create Word document: {e}')

            except Exception as e:
                st.error(f'OCR failed: {e}')
    
