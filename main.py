import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
import fitz
import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

# Constants
DEFAULT_DPI = 500

def pdf_to_images(pdf_path, output_folder, dpi=DEFAULT_DPI):
    os.makedirs(output_folder, exist_ok=True)
    try:
        with fitz.open(pdf_path) as pdf_document:
            for page_number in range(len(pdf_document)):
                page = pdf_document[page_number]
                pix = page.get_pixmap(dpi=dpi)
                output_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
                pix.save(output_path)
        return output_folder
    except Exception as e:
        raise RuntimeError(f"Error during PDF conversion: {e}")

def extract_text_from_pdf(pdf_path, output_path):
    try:
        with fitz.open(pdf_path) as pdf_document:
            text = ""
            for page in pdf_document:
                text += page.get_text()
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)
    except Exception as e:
        raise RuntimeError(f"Error extracting text: {e}")

def merge_pdfs(pdf_paths, output_path):
    try:
        merger = PdfMerger()
        for pdf in pdf_paths:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
    except Exception as e:
        raise RuntimeError(f"Error merging PDFs: {e}")

def split_pdf(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    try:
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_file = os.path.join(output_folder, f"page_{i + 1}.pdf")
            with open(output_file, "wb") as f:
                writer.write(f)
    except Exception as e:
        raise RuntimeError(f"Error splitting PDF: {e}")

class PDFWorkerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFWorker")
        self.setFixedSize(600, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Widgets
        self.pdf_path_label = QLabel("Select PDF File:")
        self.pdf_path_input = QLineEdit()
        self.pdf_path_input.setPlaceholderText("Select a PDF file...")
        self.pdf_browse_button = QPushButton("Browse")
        self.pdf_browse_button.clicked.connect(self.select_pdf)

        self.output_folder_label = QLabel("Select Output Folder:")
        self.output_folder_input = QLineEdit()
        self.output_folder_input.setPlaceholderText("Select an output folder...")
        self.output_browse_button = QPushButton("Browse")
        self.output_browse_button.clicked.connect(self.select_output_folder)

        self.convert_button = QPushButton("Convert PDF to Images")
        self.convert_button.clicked.connect(self.convert_to_images)

        self.extract_text_button = QPushButton("Extract Text")
        self.extract_text_button.clicked.connect(self.extract_text)

        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.clicked.connect(self.merge_pdfs)

        self.split_button = QPushButton("Split PDF")
        self.split_button.clicked.connect(self.split_pdf)

        # Add widgets to layouts
        form_layout.addWidget(self.pdf_path_label)
        form_layout.addWidget(self.pdf_path_input)
        form_layout.addWidget(self.pdf_browse_button)

        form_layout.addWidget(self.output_folder_label)
        form_layout.addWidget(self.output_folder_input)
        form_layout.addWidget(self.output_browse_button)

        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.extract_text_button)
        button_layout.addWidget(self.merge_button)
        button_layout.addWidget(self.split_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QLabel { color: #d4d4d4; font-size: 14px; }
            QLineEdit { background-color: #2d2d30; color: #d4d4d4; border: 1px solid #3e3e42; border-radius: 5px; padding: 5px; }
            QPushButton { background-color: #007acc; color: #ffffff; border: none; border-radius: 5px; padding: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #005a9e; }
            QPushButton:pressed { background-color: #003f73; } """)

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.pdf_path_input.setText(file_path)

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_path:
            self.output_folder_input.setText(folder_path)

    def convert_to_images(self):
        pdf_path = self.pdf_path_input.text()
        output_folder = self.output_folder_input.text()
        if not os.path.exists(pdf_path) or not output_folder:
            QMessageBox.critical(self, "Error", "Please select a valid PDF file and output folder.")
            return
        try:
            result_folder = pdf_to_images(pdf_path, output_folder)
            QMessageBox.information(self, "Success", f"Images saved in: {result_folder}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def extract_text(self):
        pdf_path = self.pdf_path_input.text()
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Extracted Text", "", "Text Files (*.txt)")
        if not pdf_path or not output_path:
            QMessageBox.critical(self, "Error", "Please select a valid PDF file and output file.")
            return
        try:
            extract_text_from_pdf(pdf_path, output_path)
            QMessageBox.information(self, "Success", f"Text saved in: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def merge_pdfs(self):
        pdf_paths, _ = QFileDialog.getOpenFileNames(self, "Select PDFs to Merge", "", "PDF Files (*.pdf)")
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf)")
        if not pdf_paths or not output_path:
            QMessageBox.critical(self, "Error", "Please select PDF files and output file.")
            return
        try:
            merge_pdfs(pdf_paths, output_path)
            QMessageBox.information(self, "Success", f"Merged PDF saved in: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def split_pdf(self):
        pdf_path = self.pdf_path_input.text()
        output_folder = self.output_folder_input.text()
        if not os.path.exists(pdf_path) or not output_folder:
            QMessageBox.critical(self, "Error", "Please select a valid PDF file and output folder.")
            return
        try:
            split_pdf(pdf_path, output_folder)
            QMessageBox.information(self, "Success", f"PDF split into pages in: {output_folder}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFWorkerApp()
    window.show()
    sys.exit(app.exec())