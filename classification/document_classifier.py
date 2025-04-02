from transformers import pipeline
from config import DOCUMENT_LABELS

# Initialize the zero-shot classification pipeline with a model like facebook/bart-large-mnli.
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_document(text):
    """
    Classify the OCR-extracted text as 'invoice' or 'non-invoice' using zero-shot classification.
    The function returns a list formatted as:
      [ "Classified as: <winning label>",
        "<label1> : <score>",
        "<label2> : <score>" ]
    
    Parameters:
        text (str): The OCR-extracted text.
    
    Returns:
        list: Formatted classification results.
    """
    candidate_labels = list(DOCUMENT_LABELS)
    result = classifier(text, candidate_labels)
    
    # Determine the winning label based on the highest score.
    max_score_index = result['scores'].index(max(result['scores']))
    winning_label = result['labels'][max_score_index]
    
    # Build the formatted result list.
    formatted_result = [f"Classified as: {winning_label}"]
    for label, score in zip(result['labels'], result['scores']):
        formatted_result.append(f"{label}'s score: {score:.2f}")
    
    return formatted_result

# if __name__ == "__main__":
#     # Example usage with sample text.
#     sample_text = "Invoice Number: 123456\nDate: 2023-06-30\nVendor: ABC Supplies\nTotal: $450.00"
#     classification_result = classify_document(sample_text)
#     print("Classification Result:", classification_result)
