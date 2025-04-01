import re
import logging

logger = logging.getLogger(__name__)

def extract_invoice_data(text):
    """
    Extracts dates and the total amount from OCR text using regex patterns.
    """
    # Regular Expression Patterns
    date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})" # Matches dates like 12/03/2023, 2023-03-12
    total_pattern = r"(Total\s*[:\s]*[\$€]?\s*([\d,]+\.\d{2}))" # Matches 'Total: 123.45' or 'Total $123.45'

    
    # Extract values
    date_matches = re.findall(date_pattern, text)
    logger.info(f"Found dates: {date_matches}")
    
    total_match = re.search(total_pattern, text)
    logger.info(f"Found total: {total_match.group(1) if total_match else 'Not Found'}")
    
    invoice_date, due_date = "Not Found", "Not Found"
    for date in date_matches:
        if "invoice date" in text.lower() and invoice_date == "Not Found":
            invoice_date = date
        elif "due date" in text.lower() and due_date == "Not Found":
            due_date = date

    # Remove identified dates from the list.
    date_matches = [date for date in date_matches if date != invoice_date and date != due_date]

    extracted_data = {
        "Invoice Date": invoice_date,
        "Due Date": due_date,
        "Unknown Dates": date_matches,
        "Total Amount": total_match.group(2) if total_match else "Not Found"
    }
    
    return extracted_data
