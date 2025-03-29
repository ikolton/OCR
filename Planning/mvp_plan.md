# MVP Plan
---

### 1. Preprocessing Module

**Objective:** Prepare the input image to ensure consistency for downstream processing.

**Action Items:**
- **Library Options:**
  - [OpenCV](https://opencv.org/) – for image operations such as blurring, resizing, and deskewing.
  - [Pillow (PIL)](https://python-pillow.org/) – for basic image file manipulation.
  - [scikit-image](https://scikit-image.org/) – for advanced image processing filters and transformations.
- **Implementation Tasks:**
  - Develop functions in `preprocessing/image_preprocessing.py` to:
    - **Noise Reduction:** Apply Gaussian blur, median filtering, or similar methods.
    - **Deskewing:** Detect skew angle and rotate the image accordingly.
    - **Resizing/Normalization:** Standardize image size and scale pixel values.
    - **Sharpening**
    - **Detection and cropping**

---

### 2. OCR Module

**Objective:** Convert the extracted document image into machine-readable text.

**Action Items:**
- **Library Options:**
  - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) via [pytesseract](https://pypi.org/project/pytesseract/) – open-source, easy to integrate.
  - [EasyOCR](https://github.com/JaidedAI/EasyOCR) – supports multiple languages and fonts, deep learning-based.
  - [Google Cloud Vision](https://cloud.google.com/vision) or [AWS Textract](https://aws.amazon.com/textract/) – cloud-based OCR with high accuracy.
- **Implementation Tasks:**
  - In `ocr/ocr_engine.py`, set up:
    - **OCR Integration:** Pass the preprocessed, detected document image to the OCR engine.
    - **Configuration:** Tune parameters for language, OCR mode, and preprocessing enhancements.

---

### 3. Main Application (main.py)

**Objective:** Act as the central orchestrator that coordinates the processing pipeline and manages user interaction via the CLI.

**Action Items:**
- **Design and Implementation:**
  - Create `main.py` as the entry point of the application.
  - Implement a **central function** (e.g., `process_document(image_path)`) that:
    - Accepts an image file path as input.
    - Sequentially calls:
      - The Preprocessing Module to clean and normalize the image.
      - The Document Detection Module to isolate the invoice.
      - The OCR Module to extract text from the processed invoice.
    - Returns a structured output, including the extracted text and any key fields.
  - Implement CLI logic in `main.py` to:
    - Parse command-line arguments (using libraries like argparse or click).
    - Accept an image path as input.
    - Display the results in a user-friendly manner.
- **Advantages for Future Expansion:**
  - By isolating the core processing logic into a single function (`process_document`), transitioning to a web interface or desktop GUI will be straightforward. Both additional interfaces can simply call this function and format the results for their specific output requirements.

---

### Next Steps Post-MVP

After establishing these core functionalities and the CLI interface via main.py, the project can be extended by adding a **Data Extraction Module** (to parse and structure key fields) and, optionally, a **Document Classification Module** for differentiating invoice types. Additionally, you can build alternative interfaces (e.g., web or desktop) that reuse the same processing logic.

This plan presents multiple tool choices to allow flexibility in development and ensures a clear separation between business logic and user interaction, easing future expansions.
