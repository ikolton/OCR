# OCR Module

The OCR Module handles the extraction of text from images using different OCR engines. It integrates both Tesseract and EasyOCR to provide flexible, multi-language support for text extraction.

## Features

- **Tesseract OCR Integration:**  
  Uses Tesseract to extract text with configurable parameters, leveraging its built-in orientation and script detection.

- **EasyOCR Integration:**  
  Provides an alternative deep learning-based OCR engine that supports multiple languages.

- **Language Mapping:**  
  Automatically maps canonical language names to the specific language codes required by each OCR engine.

- **Text Statistics:**  
  Computes basic statistics (word count, character count, line count, average word length) on the extracted text.

## Available Functions

- `get_engine_language(canonical_lang, engine)`  
  Maps a canonical language name (e.g., "english") to the appropriate language code for Tesseract or EasyOCR.

- `extract_text_tesseract(image, lang, config=DEFAULT_CONFIG)`  
  Extracts text from an image using Tesseract OCR with configurable parameters.

- `extract_text_easyocr(image, lang)`  
  Extracts text from an image using EasyOCR.

- `extract_text(image, lang, engine='tesseract', config=DEFAULT_CONFIG)`  
  A unified function that calls either Tesseract or EasyOCR based on the provided engine argument.

- `get_text_stats(text)`  
  Computes and returns statistics about the extracted text including word count, character count, line count, and average word length.

## Configuration

- **Default Configurations:**  
  - The OCR extraction uses a default configuration (`DEFAULT_CONFIG`) for Tesseract that can be modified if needed.
  - Language mappings are defined in the configuration file, ensuring correct language codes for Tesseract and EasyOCR.

- **Engine Selection:**  
  - Choose between Tesseract and EasyOCR based on your requirements. Tesseract is well-suited for many cases, while EasyOCR offers robust multi-language support.

## Logging

- The module employs Python's `logging` library to log information and errors during OCR processing.  
- Make sure your logging configuration captures these log messages for effective debugging and monitoring.
