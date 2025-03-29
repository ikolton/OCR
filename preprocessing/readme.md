# Preprocessing Module

The Preprocessing Module is responsible for preparing invoice images for OCR. It includes functions to enhance image quality, correct orientation, and crop regions of interest, ensuring that subsequent OCR processing is more accurate.

## Features

- **Contrast Enhancement:**  
  Improves image contrast using gamma correction and CLAHE.
  
- **Denoising:**  
  Reduces noise using non-local means denoising.

- **Sharpening:**  
  Applies an unsharp mask filter to enhance image details.

- **Edge Enhancement:**  
  Enhances image edges using morphological operations.

- **Thresholding:**  
  Applies global thresholding to convert images to binary.

- **Rotation and Deskewing:**  
  Uses Hough Transform to detect and correct skewed images, ensuring proper alignment.

- **Orientation Correction:**  
  Leverages Tesseract's OSD (Orientation and Script Detection) to adjust image orientation based on OCR feedback.

- **Resizing and Normalization:**  
  Resizes images to a target width while maintaining aspect ratio and normalizes pixel values.

- **Cropping to Text:**  
  Identifies and crops the image to regions containing text based on OCR data.

- **Custom Preprocessing Pipeline:**  
  Supports applying a custom-ordered sequence of steps. Functions include:
  - `preprocess_image`: Applies a standard sequence of preprocessing steps.
  - `preprocess_image_custom`: Applies user-defined steps in a specified order.

## Available Functions

- `enhance_contrast(gray, use_gamma=True, gamma=0.5, use_clahe=True, clipLimit=4.0, tileGridSize=(8, 8))`  
  Enhance image contrast via gamma correction and CLAHE.

- `denoise_image(gray, h=5, templateWindowSize=9, searchWindowSize=31)`  
  Reduce noise in the grayscale image.

- `sharpen_image(gray, kernel=None)`  
  Apply an unsharp mask filter to sharpen the image.

- `edge_enhancement(gray, alpha=0.2, kernel_size=3)`  
  Enhance image edges using a morphological gradient.

- `threshold_image(gray, thresh_value=80, max_value=255, invert=False)`  
  Apply global thresholding to produce a binary image.

- `rotate_bound(gray, angle)`  
  Rotate the image by a specified angle without cropping content.

- `deskew_using_hough(gray)`  
  Estimate and correct skew using edge detection and Hough Line Transform.

- `get_osd_info(gray)`  
  Retrieve orientation information using Tesseract's OSD.

- `get_ocr_text_score(gray)`  
  Compute an OCR text score based on alphanumeric content.

- `evaluate_candidate(gray, candidate_angle)`  
  Evaluate a candidate rotation based on OCR score and OSD feedback.

- `correct_orientation(gray)`  
  Determine and apply the best rotation for proper orientation.

- `resize_normalize(gray, target_width=800)`  
  Resize the image to a target width and normalize pixel values.

- `crop_to_text(gray, min_conf=60, margin=100)`  
  Crop the image to the region containing text based on OCR confidence.

- `correct_format_for_preprocessing(image)`  
  Convert input images to grayscale for preprocessing.

- `correct_format_for_ocr(image)`  
  Prepare the image for OCR by resizing and normalizing.

- `preprocess_image(...)`  
  Run a standard preprocessing pipeline with configurable steps.

- `preprocess_image_custom(image, steps, target_width=800)`  
  Run a custom preprocessing pipeline based on a user-defined list of steps.


## Configuration

- Most functions allow you to modify parameters such as gamma value, clip limits, and thresholds.  
- The default pipeline is configured in the main application and can be customized further in your own scripts.

## Logging

- The module uses Python's built-in `logging` library. Ensure that your logging configuration captures the module's log messages for debugging purposes.


