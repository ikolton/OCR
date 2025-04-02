# Extraction Module

The Extraction Module is designed to process OCR-extracted text from invoices and retrieve key information such as dates and the total amount. By using regular expressions, the module identifies and extracts relevant data points, making it easier to integrate with invoice processing systems.

## Features

- **Date Extraction:**  
  Uses regex patterns to detect date formats (e.g., `12/03/2023`, `2023-03-12`).

- **Total Amount Extraction:**  
  Identifies and extracts the total invoice amount from the text, supporting common currency symbols such as `$` and `€`.

- **Logging:**  
  Utilizes Python's built-in `logging` library to log the extracted values, aiding in debugging and monitoring.

## Available Functions

### `extract_invoice_data(text)`

- **Purpose:**  
  Extracts key invoice data (invoice date, due date, unknown dates, and total amount) from the provided OCR text.

- **Parameters:**  
  - `text` (str): The OCR-extracted text from an invoice.

- **Returns:**  
  - `dict`: A dictionary containing:
    - **Invoice Date:** The date associated with the invoice (if found, otherwise `"Not Found"`).
    - **Due Date:** The due date for the invoice payment (if found, otherwise `"Not Found"`).
    - **Unknown Dates:** A list of any additional date occurrences found in the text.
    - **Total Amount:** The total invoice amount (if found, otherwise `"Not Found"`).

