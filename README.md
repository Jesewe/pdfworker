# PDFWorker

PDFWorker is a desktop application built with Python and PyQt6 that provides various tools for working with PDF files. It allows users to convert PDF pages to images, extract text from PDFs, merge multiple PDFs into one, and split a PDF into individual pages.

## Features

- **Convert PDF to Images**: Extracts each page of a PDF and saves it as an image in the selected output folder.
- **Extract Text from PDF**: Extracts all text from a PDF and saves it as a text file.
- **Merge PDFs**: Combines multiple PDF files into a single PDF.
- **Split PDF**: Splits a PDF into individual pages, each saved as a separate PDF file.

## Requirements

- Python 3.7 or higher
- PyQt6
- PyPDF2
- PyMuPDF (fitz)

## Installation

1. Clone the repository or download the source code:
   ```bash
   git clone https://github.com/Jesewe/pdfworker.git
   cd pdfworker
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the application.
2. Select a PDF file using the "Browse" button under "Select PDF File."
3. Select an output folder using the "Browse" button under "Select Output Folder."
4. Choose an action:
   - **Convert PDF to Images**: Click the "Convert PDF to Images" button.
   - **Extract Text**: Click the "Extract Text" button and specify the output file.
   - **Merge PDFs**: Click the "Merge PDFs" button, select multiple PDF files, and specify the output file.
   - **Split PDF**: Click the "Split PDF" button.

## Error Handling

- If invalid paths are provided, the app will display an error message.
- Detailed error messages will be shown in case of any issues during processing.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.