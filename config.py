LANGUAGE_MAP = {
    "english": {"tesseract": "eng", "easyocr": "en"},
    "french":  {"tesseract": "fra", "easyocr": "fr"},
    "german":  {"tesseract": "deu", "easyocr": "de"},
    "polish":  {"tesseract": "pol", "easyocr": "pl"},
}

# List of available preprocessing steps.
AVAILABLE_STEPS = [
    "contrast", "denoise", "edge_enhancement", "sharpen",
    "threshold", "deskew", "orientation", "crop"
]

# Default pipeline order.
DEFAULT_PIPELINE = ["contrast", "deskew", "orientation", "crop"]

DOCUMENT_LABELS = {"invoice", "receipt", "contract", "report", "letter", "memo", "form", "other"}