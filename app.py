import streamlit as st
import cv2
import numpy as np
from preprocessing import image_preprocessing
from ocr import ocr_engine
from config import LANGUAGE_MAP, AVAILABLE_STEPS, DEFAULT_PIPELINE
import logging

# Configure global logging so that all modules using logging will follow these settings.
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

st.set_page_config(layout="wide")

# Set a default pipeline on start if not already defined.
if 'pipeline_steps' not in st.session_state:
    st.session_state.pipeline_steps = DEFAULT_PIPELINE.copy()

# We'll use session state to store the preprocessed image.
if 'preprocessed_image' not in st.session_state:
    st.session_state.preprocessed_image = None

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
                    st.session_state.pipeline_steps[i], st.session_state.pipeline_steps[i-1] = (
                        st.session_state.pipeline_steps[i-1],
                        st.session_state.pipeline_steps[i]
                    )
                st.rerun()
            # Button to move the step down.
            if col_down.button("↓", key=f"down_{step}_{i}"):
                if i < len(st.session_state.pipeline_steps) - 1:
                    st.session_state.pipeline_steps[i], st.session_state.pipeline_steps[i+1] = (
                        st.session_state.pipeline_steps[i+1],
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
    ocr_engine_choice = st.selectbox("Choose OCR Engine", ["tesseract", "easyocr"])
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
            if st.button("Preprocess Image"):
                try:
                    preprocessed_image = image_preprocessing.preprocess_image_custom(image, steps)
                    st.session_state.preprocessed_image = preprocessed_image
                    st.image(preprocessed_image, caption="Preprocessed Image", channels="GRAY")
                except Exception as e:
                    st.error(f"Error during preprocessing: {e}")
                    return

            # Separate button for OCR extraction.
            if st.session_state.preprocessed_image is not None and st.button("Extract OCR"):
                try:
                    extracted_text = ocr_engine.extract_text(
                        st.session_state.preprocessed_image,
                        lang=language_choice,
                        engine=ocr_engine_choice
                    )
                    st.subheader("Extracted Text")
                    st.text_area("OCR Output", extracted_text, height=300)

                    # Compute and display text statistics.
                    text_stats = ocr_engine.get_text_stats(extracted_text)
                    st.write("### Text Statistics")
                    st.json(text_stats)
                except Exception as e:
                    st.error(f"Error during OCR extraction: {e}")

if __name__ == '__main__':
    main()
