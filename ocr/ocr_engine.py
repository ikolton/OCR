import cv2
import pytesseract
import logging
from config import LANGUAGE_MAP

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# Default configuration parameters for OCR
DEFAULT_CONFIG = '--psm 6'


def get_engine_language(canonical_lang, engine):
    """
    Retrieve the engine-specific language code given a canonical language name.
    
    Parameters:
        canonical_lang (str): The canonical language identifier (e.g., "english").
        engine (str): The OCR engine ('tesseract' or 'easyocr').
    
    Returns:
        str: The corresponding language code for the given engine.
    """
    canonical_lang = canonical_lang.lower()
    if canonical_lang in LANGUAGE_MAP:
        return LANGUAGE_MAP[canonical_lang].get(engine, canonical_lang)
    return canonical_lang

def extract_text_tesseract(image, lang, config=DEFAULT_CONFIG):
    """
    Extract text from an image using Tesseract OCR.
    
    Parameters:
        image (numpy.array): The input image (BGR or grayscale).
        lang (str): The language for OCR.
        config (str): Additional Tesseract configuration options.
        
    Returns:
        str: The text extracted from the image.
    """
    try:
        text = pytesseract.image_to_string(image, lang, config=config)
        logger.info("Tesseract OCR extraction completed successfully.")
        return text
    except Exception as e:
        logger.error("Error during Tesseract OCR extraction: %s", e)
        return ""


def extract_text_easyocr(image, lang):
    """
    Extract text from an image using EasyOCR.
    
    Parameters:
        image (numpy.array): The input image.
        lang (str): The language code for OCR.
        
    Returns:
        str: The text extracted from the image.
    """
    try:
        import easyocr
    except ImportError as e:
        logger.error("EasyOCR is not installed. Please install it via 'pip install easyocr'.")
        return ""
    
    try:
        reader = easyocr.Reader([lang], gpu=False)
        results = reader.readtext(image)
        text = " ".join([result[1] for result in results])
        logger.info("EasyOCR extraction completed successfully.")
        return text
    except Exception as e:
        logger.error("Error during EasyOCR extraction: %s", e)
        return ""

def extract_text(image, lang, engine='tesseract', config=DEFAULT_CONFIG):
    """
    Extract text from an image using the specified OCR engine.
    
    Parameters:
        image (numpy.array): The input image.
        engine (str): The OCR engine to use ('tesseract' or 'easyocr').
        lang (str): The language for OCR.
        config (str): Additional Tesseract configuration (ignored for EasyOCR).
        
    Returns:
        str: The extracted text.
    """
    lang = get_engine_language(lang, engine.lower())
    if engine.lower() == 'tesseract':
        return extract_text_tesseract(image, lang=lang, config=config)
    elif engine.lower() == 'easyocr':
        return extract_text_easyocr(image, lang=lang)
    else:
        logger.error("Unsupported OCR engine: %s", engine)
        raise ValueError(f"Unsupported OCR engine: {engine}")

def get_text_stats(text):
    """
    Compute basic statistics on the extracted text.

    Parameters:
        text (str): The OCR-extracted text.

    Returns:
        dict: A dictionary with word count, character count, line count,
              and average word length.
    """
    words = text.split()
    word_count = len(words)
    character_count = len(text)
    line_count = len(text.splitlines())
    average_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0

    return {
        "word_count": word_count,
        "character_count": character_count,
        "line_count": line_count,
        "average_word_length": average_word_length
    }
