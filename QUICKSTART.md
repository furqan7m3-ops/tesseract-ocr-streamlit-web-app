# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install Tesseract (Choose your OS)

**Windows (Recommended: Chocolatey)**
```powershell
choco install tesseract
```
Or download installer from: https://github.com/UB-Mannheim/tesseract/wiki

**Linux (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS**
```bash
brew install tesseract
```

### Step 3: Verify Installation
```bash
tesseract --version
```

---

## 📱 Running the Application

### Option A: Desktop GUI (Recommended for Most Users)
```bash
python gui.py
```
✨ Full-featured desktop application with:
- Real-time image preview
- Image preprocessing tools
- Text extraction
- Save as Word or plain text
- Copy to clipboard

### Option B: Web Interface
```bash
streamlit run app.py
```
Then open: http://localhost:8501

---

## 📖 Common Tasks

### Extract Text from Image
1. Click **"Load Image"** button
2. Select your image file
3. Click **"Extract Text"**
4. View results in text area

### Improve OCR Results
1. Load image
2. Try these buttons in order:
   - **Preprocess** - For scanned documents
   - **Enhance Contrast** - For low-quality images
   - **Deskew** - For rotated documents
3. Then extract text

### Save Results
**As Plain Text:**
- Click "Save Text"
- Choose location and filename

**As Word Document:**
- Click "Save as Word Doc"
- Includes original image + formatted text

**To Clipboard:**
- Click "Copy to Clipboard"
- Paste anywhere with Ctrl+V

---

## ⚙️ Configuration

### Change Preprocessing Settings
Edit `OCR/image_preprocessor.py`:
```python
# Increase scale for smaller text
preprocessed = preprocess_image(img, resize_scale=3.0)

# Disable denoising
preprocessed = preprocess_image(img, denoise=False)
```

### Use Different Languages
Edit `OCR/text_extractor.py` or GUI:
```python
# Spanish
text = extract_text(image_path, lang='spa')

# Multiple languages
text = extract_text(image_path, lang='eng+spa')
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Tesseract not found" | Install Tesseract and restart |
| Poor OCR accuracy | Try Preprocess → Enhance → Extract |
| GUI is slow | Wait for progress bar to complete |
| Word document won't open | Ensure python-docx is installed |

---

## 📚 Project Structure
```
Project/
├── gui.py                      ← Run this for desktop app
├── app.py                      ← Run this for web app
├── requirements.txt            ← Install these packages
├── README.md                   ← Full documentation
└── OCR/
    ├── text_extractor.py       ← Core OCR logic
    ├── image_preprocessor.py   ← Image enhancement
    ├── formatting_detector.py  ← Text formatting
    └── word_generator.py       ← Create Word docs
```

---

## 💡 Tips for Best Results

1. **Image Quality Matters**
   - Use high-quality images (300+ DPI recommended)
   - Ensure text is clearly visible
   - Good lighting/contrast is important

2. **Preprocessing Helps**
   - Always try "Preprocess" first
   - Use "Enhance Contrast" for faded text
   - Use "Deskew" for rotated documents

3. **Check Results**
   - Review extracted text for accuracy
   - Confidence score shown in status bar
   - Edit text before saving if needed

4. **Document Generation**
   - Formatting detection works best with clear formatting
   - Original image is embedded in Word document
   - Can be further edited in Microsoft Word

---

## 🎯 Next Steps

- **Read** `README.md` for complete documentation
- **Check** `IMPLEMENTATION_SUMMARY.md` for technical details
- **Explore** the code in `OCR/` directory
- **Experiment** with different preprocessing options

---

## ⚡ Performance Tips

- **Faster Processing**: Disable formatting detection if not needed
- **Better Accuracy**: Preprocess images before extraction
- **Batch Processing**: GUI handles multi-threading automatically
- **Memory**: Large images work fine, preprocessing may take a few seconds

---

## 📝 Example Workflow

```
1. Open gui.py
2. Click "Load Image"
3. (Optional) Click "Preprocess" for scanned documents
4. Click "Extract Text"
5. Review extracted text
6. Click "Save as Word Doc" to export
7. Document is ready for editing in Microsoft Word!
```

---

For detailed information, see **README.md** and **IMPLEMENTATION_SUMMARY.md**

Happy OCR-ing! 🎉
