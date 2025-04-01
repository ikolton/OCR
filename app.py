import streamlit as st
import cv2
import numpy as np
from preprocessing import image_preprocessing
from ocr import ocr_engine
from config import LANGUAGE_MAP, AVAILABLE_STEPS, DEFAULT_PIPELINE
import logging
from PIL import Image as PILImage
import io
import re

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

st.set_page_config(layout="wide")


def extract_invoice_data(text):
    """Extracts dates, place, and total sum from OCR text using regex patterns."""

    # Regular Expression Patterns
    date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"  # Matches dates like 12/03/2023, 2023-03-12
    total_pattern = r"(Total\s*[:\s]*[\$€]?\s*([\d,]+\.\d{2}))"  # Matches 'Total: 123.45' or 'Total $123.45'

    # Extracting values
    date_matches = re.findall(date_pattern, text)
    logging.info(f"Found dates: {date_matches}")

    total_match = re.search(total_pattern, text)
    logging.info(f"Found total: {total_match.group(1) if total_match else 'Not Found'}")


    invoice_date, due_date = "Not Found", "Not Found"
    for date in date_matches:
        if "invoice date" in text.lower() and invoice_date == "Not Found":
            invoice_date = date
        elif "due date" in text.lower() and due_date == "Not Found":
            due_date = date

    date_matches = [date for date in date_matches if date != invoice_date and date != due_date]

    extracted_data = {
        "Invoice Date": invoice_date,
        "Due Date": due_date,
        "Unknown Dates": date_matches,
        "Total Amount": total_match.group(2) if total_match else "Not Found"
    }

    return extracted_data


# Set a default pipeline on start if not already defined.
if 'pipeline_steps' not in st.session_state:
    st.session_state.pipeline_steps = DEFAULT_PIPELINE.copy()

# We'll use session state to store the preprocessed image.
if 'preprocessed_image' not in st.session_state:
    st.session_state.preprocessed_image = None

if 'ocr_text' not in st.session_state:
    st.session_state.ocr_text = None


def pipeline_ordering_ui():
    st.write("### Configure Preprocessing Pipeline")
    col_reset = st.container()
    col1, col2 = st.columns(2)

    # Reset button
    with col_reset:
        if st.button("Reset to Default"):
            st.session_state.pipeline_steps = DEFAULT_PIPELINE.copy()
            st.rerun()

    with col1:
        st.write("**Available Steps**")
        for step in AVAILABLE_STEPS:
            # Button to add a step if not already selected.
            if st.button(f"{step}", key=f"add_{step}"):
                if step not in st.session_state.pipeline_steps:
                    st.session_state.pipeline_steps.append(step)
                    st.rerun()

    with col2:
        st.write("**Selected Steps (in order)**")
        for i, step in enumerate(st.session_state.pipeline_steps):
            col_step, col_up, col_down, col_remove = st.columns([3, 1, 1, 1])
            col_step.write(step)
            # Button to move the step up.
            if col_up.button("↑", key=f"up_{step}_{i}"):
                if i > 0:
                    st.session_state.pipeline_steps[i], st.session_state.pipeline_steps[i - 1] = (
                        st.session_state.pipeline_steps[i - 1],
                        st.session_state.pipeline_steps[i]
                    )
                st.rerun()
            # Button to move the step down.
            if col_down.button("↓", key=f"down_{step}_{i}"):
                if i < len(st.session_state.pipeline_steps) - 1:
                    st.session_state.pipeline_steps[i], st.session_state.pipeline_steps[i + 1] = (
                        st.session_state.pipeline_steps[i + 1],
                        st.session_state.pipeline_steps[i]
                    )
                st.rerun()
            # Button to remove the step.
            if col_remove.button("delete", key=f"remove_{step}_{i}"):
                st.session_state.pipeline_steps.remove(step)
                st.rerun()

    st.write("Current pipeline order:", st.session_state.pipeline_steps)
    return st.session_state.pipeline_steps


def main():
    st.title("Invoice OCR Scanner")
    st.write("Upload an invoice image and configure your preprocessing pipeline.")

    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
    ocr_engine_choice = st.selectbox("Choose OCR Engine", ["easyocr", "tesseract"])
    language_choice = st.selectbox("Choose Language", list(LANGUAGE_MAP.keys()))

    # Display the interactive ordering UI.
    steps = pipeline_ordering_ui()

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            st.error("Error: Could not read the image.")
        else:
            st.image(image, channels="BGR", caption="Original Image")

            # Separate button for preprocessing.
            if st.button("Detect and preprocess image"):
                try:
                    preprocessed_image = image_preprocessing.preprocess_image_custom(image, steps)
                    st.session_state.preprocessed_image = preprocessed_image
                except Exception as e:
                    st.error(f"Error during preprocessing: {e}")
                    return

        # Display the preprocessed image (if it exists) before extracting OCR
        if st.session_state.preprocessed_image is not None:
            st.image(st.session_state.preprocessed_image, caption="Preprocessed Image", channels="GRAY")

            pil_image = PILImage.fromarray(st.session_state.preprocessed_image)

            # Save the PIL Image to a BytesIO object for downloading.
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='PNG')  # Save as PNG (you can change to JPEG if needed)
            img_byte_arr.seek(0)

            # Trigger the download
            st.download_button(
                label="Download Preprocessed Image",
                data=img_byte_arr,
                file_name="preprocessed_image.png",
                mime="image/png"
            )

            # Separate button for OCR extraction.
        if st.session_state.preprocessed_image is not None and st.button("Extract OCR"):
            try:
                extracted_text = ocr_engine.extract_text(
                    st.session_state.preprocessed_image,
                    lang=language_choice,
                    engine=ocr_engine_choice
                )
                st.session_state.ocr_text = extracted_text

            except Exception as e:
                st.error(f"Error during OCR extraction: {e}")

        if st.session_state.ocr_text is not None:
            st.subheader("Extracted Text")
            st.text_area("OCR Output", st.session_state.ocr_text, height=300)

            invoice_data = extract_invoice_data(st.session_state.ocr_text)
            st.write("### Extracted Invoice Data")
            st.json(invoice_data)

            # Compute and display text statistics.
            text_stats = ocr_engine.get_text_stats(st.session_state.ocr_text)
            st.write("### Text Statistics")
            st.json(text_stats)

            st.download_button(
                label="Download OCR text",
                data=st.session_state.ocr_text,
                file_name="text.txt",
            )


if __name__ == '__main__':
    main()
