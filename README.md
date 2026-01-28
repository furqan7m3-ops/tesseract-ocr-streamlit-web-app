# Tesseract OCR Text Extractor

A comprehensive OCR application that extracts text from images with advanced preprocessing, formatting detection, and Word document generation capabilities. Includes both Streamlit web interface and Tkinter desktop GUI.

## Features

✅ **Image Preprocessing**
- Automatic image resizing and scaling
- Denoising filters for improved OCR accuracy
- Binary thresholding for clear text separation
- Contrast enhancement using CLAHE
- Image deskewing for rotated text

✅ **Advanced OCR**
- Tesseract OCR integration for multiple languages
- Confidence scores for extracted text
- Detailed word-level position tracking
- Support for English and Spanish languages

✅ **Formatting Detection**
- Text alignment detection (left, center, right, justify)
- Bold text detection based on stroke width
- Italic text detection based on skew angle
- Font size estimation
- Paragraph organization

✅ **Document Generation**
- Export to Word documents (.docx) with formatting
- Preserve original image in document
- Metadata support (title, author, subject)
- Professional document structure

✅ **User Interface Options**
- **Desktop GUI**: Tkinter-based interface with real-time preview
  - Image loading and preprocessing tools
  - Real-time text extraction with progress indicator
  - Copy to clipboard functionality
  - Text and document export options

- **Web Interface**: Streamlit-based web application
  - Simple file upload interface
  - Real-time processing

## Project Structure

```
Terserract OCR Web App/
├── app.py                      # Streamlit web application
├── gui.py                      # Tkinter desktop GUI application
├── requirements.txt            # Python dependencies
├── packages.txt               # System packages (Tesseract)
├── images/                    # Sample images directory
└── OCR/
    ├── __init__.py
    ├── text_extractor.py      # Core OCR extraction functions
    ├── image_preprocessor.py  # Image preprocessing utilities
    ├── formatting_detector.py # Text formatting analysis
    └── word_generator.py      # Word document generation
```

## Installation

### 1. System Dependencies

#### Windows (via Chocolatey):
```powershell
choco install tesseract
```

#### Ubuntu/Debian:
```bash
sudo apt-get install tesseract-ocr
```

#### macOS:
```bash
brew install tesseract
```

### 2. Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Tesseract Installation

```bash
tesseract --version
```

## Usage

### Desktop GUI (Recommended)

```bash
python gui.py
```

**Features:**
- Load image files (PNG, JPG, JPEG, GIF, BMP)
- Apply preprocessing: resize, denoise, threshold
- Enhance contrast with CLAHE algorithm
- Correct image skew/rotation
- Extract text with optional formatting detection
- Save as plain text (.txt) or Word document (.docx)
- Copy extracted text to clipboard

### Web Interface

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## API Usage

### Basic Text Extraction

```python
from OCR.text_extractor import extract_text

text = extract_text("image.png")
print(text)
```

### Extract Text with Formatting

```python
from OCR.text_extractor import extract_text_with_formatting

result = extract_text_with_formatting("image.png")
print(result['text'])
print(f"Alignment: {result['alignment']}")
print(f"Confidence: {result['confidence']}%")
```

### Image Preprocessing

```python
from OCR.image_preprocessor import preprocess_image, enhance_contrast
from PIL import Image

img = Image.open("image.png")
preprocessed = preprocess_image(img, resize_scale=2, denoise=True)
preprocessed.save("preprocessed.png")
```

### Generate Word Document

```python
from OCR.word_generator import create_ocr_document

create_ocr_document(
    text="Extracted text here...",
    image_path="original.png",
    output_path="output.docx"
)
```

## Configuration

### Preprocessing Options

In `image_preprocessor.py`, customize preprocessing parameters:
- `resize_scale`: Image magnification factor (default: 1.5)
- `denoise`: Apply denoising filter (default: True)
- `threshold`: Apply binary threshold (default: True)

### OCR Languages

Supported languages are configured in `text_extractor.py`:
- `eng`: English (default)
- `spa`: Spanish
- Custom: Add more Tesseract language codes as needed

### Formatting Detection Thresholds

In `formatting_detector.py`, adjust detection sensitivity:
- Bold detection height threshold (line ~155)
- Italic skew angle threshold (line ~175)
- Paragraph spacing threshold (line ~225)

## Troubleshooting

### "Tesseract is not installed" Error
- Ensure Tesseract OCR is installed system-wide
- On Windows, add Tesseract to your PATH or specify its location:
  ```python
  import pytesseract
  pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### Poor OCR Accuracy
- Try image preprocessing options in the GUI:
  - Increase resize scale
  - Apply contrast enhancement
  - Use deskew feature for rotated images
- Ensure image quality is high (minimum 300 DPI recommended)

### Word Document Generation Fails
- Verify `python-docx` is installed: `pip install python-docx`
- Ensure write permissions in output directory

## Performance Tips

1. **Resize Images**: Larger images (2x-3x) often produce better OCR results
2. **Preprocessing**: Apply denoising for scanned documents
3. **Contrast**: Use contrast enhancement for low-quality images
4. **Batch Processing**: For multiple images, consider using threading (already implemented in GUI)

## Dependencies

| Package | Purpose |
|---------|---------|
| pytesseract | Tesseract OCR Python wrapper |
| pillow | Image processing |
| opencv-python | Advanced image preprocessing |
| numpy | Numerical operations |
| python-docx | Word document generation |
| streamlit | Web interface framework |

## License

This project is part of the PPIT curriculum at FAST-NUCES.

## Support

For issues or questions, check the error messages in the status bar of the GUI application. The application provides detailed feedback for all operations.

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Author**: PPIT Student Project Team
