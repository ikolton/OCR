# Classification Module

The Classification Module uses zero-shot classification to determine whether OCR-extracted text belongs to an invoice or non-invoice category. It leverages a pre-trained model from the Hugging Face Transformers library, such as `facebook/bart-large-mnli`, and relies on a configurable set of candidate document labels.

## Features

- **Zero-Shot Classification:**  
  Classifies text without additional training by using a model that supports zero-shot learning.

- **Document Labeling:**  
  Uses a predefined set of labels from the configuration (`DOCUMENT_LABELS`) to assess the document type.

- **Formatted Results:**  
  Returns classification results in a user-friendly list format, indicating the winning label and corresponding scores.

## Available Functions

### `classify_document(text)`

- **Purpose:**  
  Classifies the OCR-extracted text into one of the candidate labels (e.g., 'invoice' or 'non-invoice') using zero-shot classification.

- **Parameters:**  
  - `text` (str): The OCR-extracted text to classify.

- **Returns:**  
  - `list`: A list containing:
    - A summary of the winning label in the format `"Classified as: <winning label>"`.
    - Detailed scores for each candidate label, formatted as `"<label>'s score: <score>"`.


