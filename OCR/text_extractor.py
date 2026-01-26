import pytesseract
from PIL import Image
def extract_text(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    return text