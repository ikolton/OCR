# Invoice OCR Scanner

Invoice OCR Scanner is an automated system that extracts key information from invoice images. By combining robust image preprocessing techniques with advanced Optical Character Recognition (OCR), this project converts scanned invoices into machine-readable text for easier data extraction and analysis.

## Table of Contents

- [Invoice OCR Scanner](#invoice-ocr-scanner)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Using Conda](#using-conda)
    - [Using pip](#using-pip)
  - [Usage](#usage)
    - [Command Line](#command-line)
    - [Streamlit Interface](#streamlit-interface)
  - [Development](#development)
  - [Future Enhancements](#future-enhancements)
  - [License](#license)

## Features

- **Image Preprocessing:**  
  Enhance images with contrast adjustment, noise reduction, deskewing, sharpening, and cropping to focus on text regions.
  
- **Optical Character Recognition (OCR):**  
  Extract text using:
  - **Tesseract OCR:** A widely-used, open-source OCR engine.
  - **EasyOCR:** A deep learning-based OCR alternative that supports multiple languages.
  
- **Modular Design:**  
  Structured into separate modules for preprocessing, OCR, (planned) data extraction, and (optional) document classification.

- **User Interfaces:**  
  - ~~A CLI-based application for streamlined processing.~~
  - An interactive Streamlit web interface for real-time invoice scanning.

## Architecture

The (planned) project structure is as follows:
```
invoice_scanner/
├── app.py                  # Entry point: coordinates the overall workflow.
├── config.py                # Configuration settings and language mappings.
├── README.md                # Project documentation.
├── requirements.txt         # Python dependencies.
├── environment.yml          # Conda environment configuration.
├── preprocessing/           # Image preprocessing module.
│   ├── __init__.py
│   └── image_preprocessing.py  # Functions for image enhancement, deskewing, cropping, etc.
├── ocr/                     # OCR module.
│   ├── __init__.py
│   └── ocr_engine.py           # Integration with Tesseract and EasyOCR.
├── extraction/              # (Planned) Data extraction module.
│   ├── __init__.py
│   └── data_extractor.py       # Parsing OCR results to extract key invoice fields.
├── classification/          # (Optional) Document classification module.
│   ├── __init__.py
│   └── invoice_classifier.py   # (Future) Classify invoice types and validate layouts.
└── utils/                   # Utility functions and helpers.
    ├── __init__.py
    └── helper_functions.py     # Logging, error handling, etc.
```

## Installation

### Prerequisites

- Python 3.7+
- Tesseract OCR: Install https://github.com/tesseract-ocr/tesseract and make sure it's in your system path.
- Conda (optional but recommended)

### Using Conda

1. Clone the repository:
```sh
git clone https://github.com/ikolton/OCR.git
cd invoice_scanner
```
2. Create the environment:
```sh
conda env create -f environment.yml
```
3. Activate it:
```sh
conda activate invoice_scanner
```
### Using pip

1. Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
2. Install dependencies:
```sh
pip install -r requirements.txt
```
## Usage

### Command Line - *deprecated*
```sh
python main.py --image path/to/invoice.jpg --ocr_engine tesseract --language english
```
### Streamlit Interface

```sh
streamlit run app.py
```

Upload an invoice, tweak the pipeline, and extract text via OCR.

## Development

- Preprocessing in `preprocessing/image_preprocessing.py`
- OCR logic in `ocr/ocr_engine.py`
- Configurable pipeline and language map in `config.py`

## Future Enhancements

- Data field extraction (dates, totals, invoice numbers)
- Document classification
- Smarter Streamlit UI and PDF/CSV export

## License

MIT License — see LICENSE file for details.
