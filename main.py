## DEPRECATED ##
# This script is deprecated and replaced by app.py.

# import argparse
# import cv2
# from preprocessing import image_preprocessing
# from ocr import ocr_engine
# from config import LANGUAGE_MAP

# def main():
#     print("Invoice OCR Test")
#     print("---------------")
#     parser = argparse.ArgumentParser(description="Invoice OCR Test")
#     parser.add_argument("image_path", help="Path to the input invoice image")
#     parser.add_argument("--engine", choices=["tesseract", "easyocr"], default="tesseract", 
#                         help="OCR engine to use (default: tesseract)")
#     parser.add_argument("--lang", choices=list(LANGUAGE_MAP.keys()), default="english",
#                         help="Language for OCR (canonical name, e.g., 'english', 'polish'; default: english)")
#     args = parser.parse_args()

#     # Preprocess the image using our image_preprocessing module.
#     image = cv2.imread(args.image_path)
#     if image is None:
#         print("Error: Invalid image path")
#         return
#     try:
#         preprocessed_image = image_preprocessing.preprocess_image(image)
#     except Exception as e:
#         print(f"Error in preprocessing image: {e}")
#         return

#     # Extract text from the preprocessed image using our OCR module.
#     extracted_text = ocr_engine.extract_text(preprocessed_image, lang=args.lang, engine=args.engine)

#     print("\nExtracted Text:")
#     print(extracted_text)

# if __name__ == "__main__":
#     main()
