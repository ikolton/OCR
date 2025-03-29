import cv2
import numpy as np
import pytesseract
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def enhance_contrast(gray, use_gamma=True, gamma=0.5, use_clahe=True, clipLimit=4.0, tileGridSize=(8, 8)):
    """
    Enhance the contrast of the input grayscale image using gamma correction and CLAHE.
    
    Parameters:
        gray (np.array): Input grayscale image.
        use_gamma (bool): Whether to apply gamma correction.
        gamma (float): Gamma correction value.
        use_clahe (bool): Whether to apply CLAHE.
        clipLimit (float): CLAHE clip limit.
        tileGridSize (tuple): Grid size for CLAHE.
        
    Returns:
        np.array: Contrast-enhanced grayscale image.
    """
    if use_gamma:
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(256)]).astype("uint8")
        gray = cv2.LUT(gray, table)
    if use_clahe:
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
        gray = clahe.apply(gray)
    return gray


def denoise_image(gray, h=5, templateWindowSize=9, searchWindowSize=31):
    """
    Denoise the input grayscale image using non-local means denoising.
    
    Parameters:
        gray (np.array): Input grayscale image.
        h (float): Filter strength.
        templateWindowSize (int): Size of template patch.
        searchWindowSize (int): Size of search window.
        
    Returns:
        np.array: Denoised grayscale image.
    """
    return cv2.fastNlMeansDenoising(gray, None, h, templateWindowSize, searchWindowSize)


def sharpen_image(gray, kernel=None):
    """
    Sharpen the input grayscale image using an unsharp mask filter.
    
    Parameters:
        gray (np.array): Input grayscale image.
        kernel (np.array, optional): Custom sharpening kernel. If None, a default kernel is used.
        
    Returns:
        np.array: Sharpened grayscale image.
    """
    if kernel is None:
        kernel = np.array([[0, -0.5, 0],
                           [-0.5, 3, -0.5],
                           [0, -0.5, 0]])
    return cv2.filter2D(gray, -1, kernel)


def edge_enhancement(gray, alpha=0.2, kernel_size=3):
    """
    Enhance edges in the input grayscale image using a morphological gradient and blend it with the original.
    
    Parameters:
        gray (np.array): Input grayscale image.
        alpha (float): Weight of the edge map.
        kernel_size (int): Size of the structuring element.
    
    Returns:
        np.array: Grayscale image with enhanced edges.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    grad = cv2.convertScaleAbs(grad)
    enhanced = cv2.addWeighted(gray, 1.0, grad, alpha, 0)
    return enhanced


def threshold_image(gray, thresh_value=80, max_value=255, invert=False):
    """
    Apply global thresholding to the input grayscale image.
    
    Parameters:
        gray (np.array): Input grayscale image.
        thresh_value (int): Threshold value.
        max_value (int): Maximum value for thresholded pixels.
        invert (bool): If True, use binary inverse thresholding.
        
    Returns:
        np.array: Binary (thresholded) grayscale image.
    """
    threshold_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    ret, thresh_img = cv2.threshold(gray, thresh_value, max_value, threshold_type)
    return thresh_img


def rotate_bound(gray, angle):
    """
    Rotate the input grayscale image by the specified angle without cropping.
    
    Parameters:
        gray (np.array): Input grayscale image.
        angle (float): Rotation angle in degrees.
        
    Returns:
        np.array: Rotated grayscale image with black borders.
    """
    (h, w) = gray.shape[:2] if len(gray.shape) == 3 else gray.shape
    cX, cY = w // 2, h // 2
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(gray, M, (nW, nH), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def deskew_using_hough(gray):
    """
    Estimate and correct the skew of the input grayscale image using edge detection and Hough Line Transform.
    
    Parameters:
        gray (np.array): Input grayscale image.
        
    Returns:
        np.array: Deskewed grayscale image.
    """
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    if lines is None:
        logger.debug("No lines detected using Hough; skipping deskew.")
        return gray
    angles = [np.degrees(np.arctan2((line[0][3] - line[0][1]), (line[0][2] - line[0][0])))
              for line in lines]
    if not angles:
        return gray
    median_angle = np.median(angles)
    logger.debug("Hough-based deskew: median angle = %.2f°", median_angle)
    return rotate_bound(gray, median_angle)


def get_osd_info(gray):
    """
    Retrieve orientation information from Tesseract's OSD for a grayscale image.
    
    Parameters:
        gray (np.array): Input grayscale image.
        
    Returns:
        tuple: (rotate_value, orientation_confidence)
    """
    try:
        osd_output = pytesseract.image_to_osd(gray)
        rotate_value = 0
        orientation_confidence = 0.0
        for line in osd_output.split('\n'):
            if "Rotate:" in line:
                rotate_value = int(line.split(":")[1].strip())
            if "Orientation confidence:" in line:
                orientation_confidence = float(line.split(":")[1].strip())
        return rotate_value, orientation_confidence
    except Exception as e:
        logger.error("OSD detection failed: %s", e)
        return None, None


def get_ocr_text_score(gray):
    """
    Compute an OCR-based score by counting alphanumeric characters in the text extracted from the grayscale image.
    
    Parameters:
        gray (np.array): Input grayscale image.
        
    Returns:
        int: OCR text score.
    """
    text = pytesseract.image_to_string(gray)
    return sum(c.isalnum() for c in text)


def evaluate_candidate(gray, candidate_angle):
    """
    Evaluate a candidate rotation by computing its OCR text score and OSD penalty.
    
    Parameters:
        gray (np.array): Input grayscale image.
        candidate_angle (float): Candidate rotation angle.
        
    Returns:
        tuple: (combined_score, candidate_image, osd_rotate)
    """
    candidate_image = rotate_bound(gray, -candidate_angle)
    osd_rotate, confidence = get_osd_info(candidate_image)
    if osd_rotate is None:
        osd_rotate = 360
    ocr_score = get_ocr_text_score(candidate_image)
    penalty = 50 * abs(osd_rotate)
    combined_score = ocr_score - penalty
    logger.debug("Candidate %d° -> OSD Rotate: %d (conf: %.2f), OCR: %d, Score: %d",
                 candidate_angle, osd_rotate, confidence, ocr_score, combined_score)
    return combined_score, candidate_image, osd_rotate


def correct_orientation(gray):
    """
    Determine and apply the optimal rotation for the grayscale image based on OCR and OSD feedback.
    
    Parameters:
        gray (np.array): Input grayscale image.
        
    Returns:
        np.array: Grayscale image with corrected orientation.
    """
    candidates = [0, 90, 180, 270]
    best_score = -float('inf')
    best_image = gray
    best_angle = None
    for angle in candidates:
        score, candidate_image, _ = evaluate_candidate(gray, angle)
        if score > best_score:
            best_score = score
            best_image = candidate_image
            best_angle = angle
    logger.info("Best candidate: %d° with score %d", best_angle, best_score)
    return best_image


def resize_normalize(gray, target_width=800):
    """
    Resize the grayscale image to the specified width while preserving aspect ratio and normalize pixel values.
    
    Parameters:
        gray (np.array): Input grayscale image.
        target_width (int): Desired width.
        
    Returns:
        np.array: Resized and normalized grayscale image.
    """
    if len(gray.shape) == 2:
        h, w = gray.shape
    else:
        h, w = gray.shape[:2]
    ratio = target_width / float(w)
    new_dimensions = (target_width, int(h * ratio))
    resized = cv2.resize(gray, new_dimensions, interpolation=cv2.INTER_AREA)
    normalized = resized.astype("float32") / 255.0
    return normalized


def crop_to_text(gray, min_conf=60, margin=100):
    """
    Crop the grayscale image to the region containing text based on OCR data.
    
    Parameters:
        gray (np.array): Input grayscale image.
        min_conf (float): Minimum OCR confidence threshold.
        margin (int): Margin to add around the detected text region.
        
    Returns:
        np.array: Cropped grayscale image.
    """
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
    boxes = []
    for i in range(len(data['text'])):
        try:
            conf = float(data['conf'][i])
        except:
            conf = 0
        if conf > min_conf and data['text'][i].strip():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            boxes.append((x, y, x + w, y + h))
    if boxes:
        x_min = max(min(b[0] for b in boxes) - margin, 0)
        y_min = max(min(b[1] for b in boxes) - margin, 0)
        x_max = min(max(b[2] for b in boxes) + margin, gray.shape[1])
        y_max = min(max(b[3] for b in boxes) + margin, gray.shape[0])
        logger.debug("Cropped to text region: (%d, %d, %d, %d)", x_min, y_min, x_max, y_max)
        return gray[y_min:y_max, x_min:x_max]
    logger.debug("No text detected for cropping; returning original image.")
    return gray

def correct_format_for_preprocessing(image):
    """
    Ensure the input image is in the correct format for preprocessing.

    Parameters:
        image (np.array): Input image.

    Returns:
        np.array: Grayscale image.
    """

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def correct_format_for_ocr(image):
    """
    Ensure the input image is in the correct format for OCR.

    Parameters:
        image (np.array): Input image.
    Returns:
        np.array: Grayscale image.
    """

    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = resize_normalize(image)
    if image.dtype == 'float32' or image.dtype == 'float64':
            image = (image * 255).astype('uint8')
    return image


def preprocess_image(image,
                     apply_contrast=True,
                     apply_denoise=False,
                     apply_edge_enhancement=False,
                     apply_sharpen=True,
                     apply_threshold=False,
                     apply_deskew=True,
                     apply_orientation=True,
                     apply_crop=True,
                     apply_resize=True,
                     target_width=800):
    """
    Preprocess an image by applying a configurable sequence of steps on a grayscale image.
    
    The image is first converted to grayscale and then processed according to the flags provided.
    
    Parameters:
        image_path (str): Path to the input image.
        apply_contrast (bool): Apply contrast enhancement.
        apply_denoise (bool): Apply denoising.
        apply_edge_enhancement (bool): Apply edge enhancement.
        apply_sharpen (bool): Apply sharpening.
        apply_threshold (bool): Apply global thresholding.
        apply_deskew (bool): Apply Hough-based deskewing.
        apply_orientation (bool): Correct orientation via OCR and OSD.
        apply_crop (bool): Crop to text region.
        apply_resize (bool): Resize and normalize the image.
        target_width (int): Target width for resizing.
        
    Returns:
        np.array: Preprocessed grayscale image.
    """
    image = correct_format_for_preprocessing(image)
    
    if apply_contrast:
        image = enhance_contrast(image)
    if apply_denoise:
        image = denoise_image(image)
    if apply_edge_enhancement:
        image = edge_enhancement(image)
    if apply_sharpen:
        image = sharpen_image(image)
    if apply_threshold:
        image = threshold_image(image)
    if apply_deskew:
        image = deskew_using_hough(image)
    if apply_orientation:
        image = correct_orientation(image)
    if apply_crop:
        image = crop_to_text(image)
    if apply_resize:
        image = resize_normalize(image, target_width=target_width)

    # if image.dtype == 'float32' or image.dtype == 'float64':
    #         image = (image * 255).astype('uint8')
    return correct_format_for_ocr(image)

def preprocess_image_custom(image, steps, target_width=800):
    """
    Preprocess an image using a custom ordered pipeline of steps.
    
    The function always applies:
      - correct_format_for_preprocessing at the start.
      - correct_format_for_ocr at the end.
    
    Between these, it applies the functions specified in 'steps' in order.
    
    Parameters:
        image (np.array): Input image (BGR).
        steps (list of str): Ordered list of preprocessing step names. Allowed values:
                             "contrast", "denoise", "edge_enhancement", "sharpen",
                             "threshold", "deskew", "orientation", "crop".
        target_width (int): Target width for the resizing.
    
    Returns:
        np.array: The preprocessed image ready for OCR.
    """
    # Always start with converting to grayscale (mandatory step)
    image = correct_format_for_preprocessing(image)
    
    # Mapping of step names to functions
    step_functions = {
        "contrast": enhance_contrast,
        "denoise": denoise_image,
        "edge_enhancement": edge_enhancement,
        "sharpen": sharpen_image,
        "threshold": threshold_image,
        "deskew": deskew_using_hough,
        "orientation": correct_orientation,
        "crop": crop_to_text
    }
    
    # Apply the steps in the order specified by the user
    for step in steps:
        func = step_functions.get(step)
        if func:
            logger.debug("Applying step: %s", step)
            image = func(image)
        else:
            logger.warning("Unknown preprocessing step: %s", step)
    
    # Always end with converting the image to the correct format for OCR
    image = correct_format_for_ocr(image)
    return image




# # Inline testing code
# if __name__ == '__main__':
#     test_image_path = 'test/test5.jpeg'
#     # test_image_path = 'test/test7.png'
#     try:
#         # processed_image = preprocess_image(test_image_path, apply_denoise=True, apply_sharpen=True, apply_edge_enhancement=True, apply_contrast=True, apply_threshold=True)
#         processed_image = preprocess_image(test_image_path)
#         display_image = (processed_image * 255).astype("uint8")
#         cv2.imshow("Preprocessed Image", display_image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     except Exception as e:
#         print(f"Error during preprocessing: {e}")
