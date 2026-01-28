"""Formatting detection module for identifying text properties."""
import pytesseract
from PIL import Image
import cv2
import numpy as np


class FormattingDetector:
    """Detect text formatting properties like bold, italic, alignment."""
    
    def __init__(self):
        self.config = r'--psm 6'
    
    def detect_formatting(self, image_input):
        """
        Detect formatting properties in image.
        
        Args:
            image_input: PIL Image or file path
        
        Returns:
            dict: Contains alignment, text blocks, and detected properties
        """
        if isinstance(image_input, str):
            img = Image.open(image_input)
        else:
            img = image_input
        
        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Get detailed OCR data
        data = pytesseract.image_to_data(cv_img, config=self.config, output_type=pytesseract.Output.DICT)
        
        # Analyze text blocks for alignment
        alignment = self._detect_alignment(cv_img, data)
        
        # Detect bold/italic characteristics
        formatting_info = self._detect_text_properties(cv_img, data)
        
        return {
            'alignment': alignment,
            'text_blocks': self._extract_text_blocks(data),
            'formatting': formatting_info,
            'confidence': np.mean([int(conf) for conf in data['confidence'] if int(conf) > 0])
        }
    
    def _detect_alignment(self, image, ocr_data):
        """Detect text alignment (left, center, right)."""
        width = image.shape[1]
        x_positions = [int(x) for x in ocr_data['left']]
        
        if not x_positions:
            return 'left'
        
        # Calculate average x position
        avg_x = np.mean(x_positions)
        
        # Determine alignment based on average position
        left_threshold = width * 0.25
        right_threshold = width * 0.75
        
        if avg_x < left_threshold:
            return 'left'
        elif avg_x > right_threshold:
            return 'right'
        else:
            return 'center'
    
    def _detect_text_properties(self, image, ocr_data):
        """Detect bold and italic properties."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        properties = {
            'is_bold': self._is_bold(gray, ocr_data),
            'is_italic': self._is_italic(gray, ocr_data),
            'font_size_estimate': self._estimate_font_size(ocr_data)
        }
        
        return properties
    
    def _is_bold(self, gray, ocr_data):
        """Detect if text appears bold based on stroke width."""
        heights = [int(h) for h in ocr_data['height']]
        
        if not heights:
            return False
        
        avg_height = np.mean(heights)
        
        # Bold text typically has thicker strokes
        # Use threshold based on character height
        return avg_height > 25  # Threshold for bold detection
    
    def _is_italic(self, gray, ocr_data):
        """Detect if text appears italic based on skew."""
        # Simple italic detection using skew angle
        coords = np.column_stack(np.where(gray > 128))
        
        if len(coords) < 5:
            return False
        
        ellipse = cv2.fitEllipse(cv2.convexHull(coords))
        angle = ellipse[2]
        
        return abs(angle) > 10  # Threshold for italic detection
    
    def _estimate_font_size(self, ocr_data):
        """Estimate average font size."""
        heights = [int(h) for h in ocr_data['height'] if int(h) > 0]
        
        return round(np.mean(heights)) if heights else 12
    
    def _extract_text_blocks(self, ocr_data):
        """Extract text with position information organized into blocks."""
        blocks = []
        
        for i, text in enumerate(ocr_data['text']):
            if int(ocr_data['conf'][i]) > 30:  # Confidence threshold
                block = {
                    'text': text,
                    'x': int(ocr_data['left'][i]),
                    'y': int(ocr_data['top'][i]),
                    'width': int(ocr_data['width'][i]),
                    'height': int(ocr_data['height'][i]),
                    'confidence': int(ocr_data['conf'][i])
                }
                blocks.append(block)
        
        # Group blocks into paragraphs (group by y position)
        paragraphs = self._group_into_paragraphs(blocks)
        
        return paragraphs
    
    def _group_into_paragraphs(self, blocks):
        """Group text blocks into paragraphs based on vertical spacing."""
        if not blocks:
            return []
        
        paragraphs = []
        current_paragraph = []
        prev_y = blocks[0]['y']
        
        for block in blocks:
            # If y position changes significantly, start new paragraph
            if block['y'] - prev_y > 20:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = []
            
            current_paragraph.append(block)
            prev_y = block['y']
        
        if current_paragraph:
            paragraphs.append(current_paragraph)
        
        return paragraphs
