"""Text extraction module using Tesseract OCR."""
import pytesseract
from PIL import Image
import io
from .formatting_detector import FormattingDetector


def extract_text(image_input, lang='eng'):
    """
    Extract text from image using Tesseract OCR.
    
    Args:
        image_input: PIL Image object, file path, or file-like object (Streamlit UploadedFile, BytesIO, etc.)
        lang: Language code (default 'eng' for English)
    
    Returns:
        str: Extracted text
    """
    try:
        # Handle string file paths
        if isinstance(image_input, str):
            img = Image.open(image_input)
        # Handle file-like objects (Streamlit UploadedFile, BytesIO, etc.)
        elif hasattr(image_input, 'read'):
            img = Image.open(image_input)
        # Handle PIL Image objects
        else:
            img = image_input
        
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except Exception as e:
        raise Exception(f"OCR extraction failed: {str(e)}")


def extract_text_with_formatting(image_input, lang='eng'):
    """
    Extract text with formatting detection.
    
    Args:
        image_input: PIL Image object, file path, or file-like object (Streamlit UploadedFile, BytesIO, etc.)
        lang: Language code (default 'eng' for English)
    
    Returns:
        dict: Contains extracted text and formatting information
    """
    try:
        # Handle string file paths
        if isinstance(image_input, str):
            img = Image.open(image_input)
        # Handle file-like objects (Streamlit UploadedFile, BytesIO, etc.)
        elif hasattr(image_input, 'read'):
            img = Image.open(image_input)
        # Handle PIL Image objects
        else:
            img = image_input
    except Exception as e:
        raise Exception(f"Failed to load image: {str(e)}")
    
    # Extract plain text
    text = extract_text(img, lang=lang)
    
    # Detect formatting
    try:
        detector = FormattingDetector()
        formatting_data = detector.detect_formatting(img)
        
        return {
            'text': text,
            'formatting_data': formatting_data,
            'alignment': formatting_data.get('alignment', 'left'),
            'text_blocks': formatting_data.get('text_blocks', []),
            'confidence': formatting_data.get('confidence', 0),
            'properties': formatting_data.get('formatting', {})
        }
    
    except Exception as e:
        # Return with basic info if formatting detection fails
        return {
            'text': text,
            'error': str(e),
            'alignment': 'left'
        }


def extract_text_with_confidence(image_input, lang='eng'):
    """
    Extract text and confidence scores for each word.
    
    Args:
        image_input: PIL Image object, file path, or file-like object (Streamlit UploadedFile, BytesIO, etc.)
        lang: Language code (default 'eng' for English)
    
    Returns:
        dict: Contains text and per-word confidence scores
    """
    import cv2
    import numpy as np
    
    try:
        # Handle string file paths
        if isinstance(image_input, str):
            img = Image.open(image_input)
        # Handle file-like objects (Streamlit UploadedFile, BytesIO, etc.)
        elif hasattr(image_input, 'read'):
            img = Image.open(image_input)
        # Handle PIL Image objects
        else:
            img = image_input
    except Exception as e:
        raise Exception(f"Failed to load image: {str(e)}")
    
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Get detailed OCR data with confidence
    data = pytesseract.image_to_data(cv_img, lang=lang, output_type=pytesseract.Output.DICT)
    
    words_with_confidence = []
    for i, text in enumerate(data['text']):
        if int(data['conf'][i]) > 30:  # Confidence threshold
            words_with_confidence.append({
                'word': text,
                'confidence': int(data['conf'][i]),
                'position': (int(data['left'][i]), int(data['top'][i]))
            })
    
    full_text = ' '.join([w['word'] for w in words_with_confidence])
    avg_confidence = np.mean([w['confidence'] for w in words_with_confidence]) if words_with_confidence else 0
    
    return {
        'text': full_text,
        'words_with_confidence': words_with_confidence,
        'average_confidence': float(avg_confidence)
    }