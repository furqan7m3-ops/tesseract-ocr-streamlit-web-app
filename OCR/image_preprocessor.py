"""Image preprocessing module for OCR enhancement."""
import cv2
import numpy as np
from PIL import Image
import io


def preprocess_image(image_input, resize_scale=2.0, denoise=True, threshold_method='adaptive'):
    """
    Preprocess image for better OCR results using adaptive thresholding.
    
    Args:
        image_input: PIL Image object or file path
        resize_scale: Scale factor for resizing (default 2.0 for better detail)
        denoise: Apply denoising filter
        threshold_method: 'adaptive', 'otsu', or 'fixed' (default 'adaptive')
    
    Returns:
        PIL Image: Preprocessed image
    """
    # Convert PIL Image to OpenCV format if needed
    if isinstance(image_input, Image.Image):
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(str(image_input))
    
    if img is None:
        raise ValueError("Could not read image")
    
    # Step 1: Resize image for better OCR
    height, width = img.shape[:2]
    new_width = int(width * resize_scale)
    new_height = int(height * resize_scale)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    # Step 2: Apply denoising
    if denoise:
        img = cv2.fastNlMeansDenoisingColored(img, None, h=10, hForColorComponents=10, 
                                               templateWindowSize=7, searchWindowSize=21)
    
    # Step 3: Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Step 4: Apply intelligent thresholding
    if threshold_method == 'adaptive':
        # Adaptive Gaussian Thresholding - adjusts per region
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, blockSize=11, C=2)
    elif threshold_method == 'otsu':
        # Otsu's thresholding - finds optimal threshold automatically
        _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        # Fixed thresholding - original method
        _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Step 5: Morphological cleanup - removes noise and connects broken text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=1)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Step 6: Convert back to PIL Image
    return Image.fromarray(cv2.cvtColor(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2RGB))


def preprocess_with_otsu(image_input, resize_scale=2.0, denoise=True):
    """
    Preprocess image using Otsu's automatic threshold detection.
    Best for documents with varying lighting.
    
    Args:
        image_input: PIL Image object or file path
        resize_scale: Scale factor for resizing
        denoise: Apply denoising filter
    
    Returns:
        PIL Image: Preprocessed image
    """
    return preprocess_image(image_input, resize_scale=resize_scale, 
                           denoise=denoise, threshold_method='otsu')


def preprocess_with_fixed_threshold(image_input, resize_scale=2.0, denoise=True, threshold_value=150):
    """
    Preprocess image using fixed threshold value.
    For consistent, predictable results.
    
    Args:
        image_input: PIL Image object or file path
        resize_scale: Scale factor for resizing
        denoise: Apply denoising filter
        threshold_value: Fixed threshold value (0-255, default 150)
    
    Returns:
        PIL Image: Preprocessed image
    """
    # Convert PIL Image to OpenCV format if needed
    if isinstance(image_input, Image.Image):
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(str(image_input))
    
    if img is None:
        raise ValueError("Could not read image")
    
    # Resize image
    height, width = img.shape[:2]
    new_width = int(width * resize_scale)
    new_height = int(height * resize_scale)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    # Apply denoising
    if denoise:
        img = cv2.fastNlMeansDenoisingColored(img, None, h=10, hForColorComponents=10, 
                                               templateWindowSize=7, searchWindowSize=21)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply fixed thresholding
    _, gray = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=1)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Convert back to PIL Image
    return Image.fromarray(cv2.cvtColor(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2RGB))


def apply_morphology(image_input, operation='close', kernel_size=3, iterations=1):
    """
    Apply morphological operations to clean up text.
    
    Args:
        image_input: PIL Image object or file path
        operation: 'close' (fill holes), 'open' (remove noise), 'dilate', 'erode'
        kernel_size: Size of the morphological kernel
        iterations: Number of times to apply operation
    
    Returns:
        PIL Image: Processed image
    """
    if isinstance(image_input, Image.Image):
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(str(image_input))
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    if operation == 'close':
        result = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    elif operation == 'open':
        result = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=iterations)
    elif operation == 'dilate':
        result = cv2.dilate(gray, kernel, iterations=iterations)
    elif operation == 'erode':
        result = cv2.erode(gray, kernel, iterations=iterations)
    else:
        result = gray
    
    return Image.fromarray(cv2.cvtColor(cv2.cvtColor(result, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2RGB))


def enhance_contrast(image_input):
    """Enhance image contrast for better OCR using CLAHE."""
    if isinstance(image_input, Image.Image):
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(str(image_input))
    
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    return Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))


def enhance_contrast_advanced(image_input, clip_limit=2.0, tile_size=8):
    """
    Advanced contrast enhancement using CLAHE with adjustable parameters.
    
    Args:
        image_input: PIL Image object or file path
        clip_limit: Contrast limiting threshold (default 2.0, higher = more contrast)
        tile_size: Size of grid tiles (default 8x8)
    
    Returns:
        PIL Image: Enhanced image
    """
    if isinstance(image_input, Image.Image):
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(str(image_input))
    
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    return Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))


def deskew_image(image_input):
    """Deskew image if text is rotated."""
    if isinstance(image_input, Image.Image):
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(str(image_input))
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(cv2.convexHull(coords))[-1]
    
    if angle < -45:
        angle = 90 + angle
    
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    return Image.fromarray(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))


def optimal_pipeline(image_input):
    """
    Best-practice pipeline for high-quality OCR.
    Combines all techniques for maximum accuracy.
    
    Order:
    1. Deskew (straighten rotated text)
    2. Enhance contrast (CLAHE)
    3. Resize (2x magnification)
    4. Denoise (remove artifacts)
    5. Adaptive threshold (intelligent B&W)
    6. Morphology cleanup (connect broken letters)
    
    Args:
        image_input: PIL Image object or file path
    
    Returns:
        PIL Image: Fully optimized image
    """
    # Step 1: Deskew
    img = deskew_image(image_input)
    
    # Step 2: Enhance contrast
    img = enhance_contrast(img)
    
    # Step 3: Preprocess with adaptive thresholding
    img = preprocess_image(img, resize_scale=2.0, denoise=True, threshold_method='adaptive')
    
    return img

