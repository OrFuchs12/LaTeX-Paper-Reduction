import os
import subprocess
import csv
import pdfplumber
from collections import defaultdict
import fitz
import re

def extract_pages_pdf(pdf_path, output_path):
    pdf_document = fitz.open(pdf_path)
    last_page_number = len(pdf_document)

    # Create a new PDF document
    new_pdf = fitz.open()

    # Add the last two pages to the new document
    new_pdf.insert_pdf(pdf_document, from_page=last_page_number-2, to_page=last_page_number-1)

    # Save the new PDF with only the last two pages
    new_pdf.save(output_path)
    new_pdf.close()
    
    
def extract_preamble(input_tex, output_tex):
    with open(input_tex, 'r', encoding='utf-8') as file:
        latex_content = file.read()

        # Find the index of \begin{document}
        begin_document_index = latex_content.find("\\begin{document}")

        # Extract everything before \begin{document}
        preamble = latex_content[:begin_document_index + len("\\begin{document}")]

        # Write the preamble to a new LaTeX file
        with open(output_tex, 'w', encoding='utf-8') as output_file:
            output_file.write(preamble)
    
# pdf_path = "new_papers_creation/test_pdf/Formatting-Instructions-LaTeX-2024_changed.pdf"
# output_path = "new_papers_creation/test_pdf/Formatting-Instructions-LaTeX-2024_2_pages.pdf"

# extract_pages_pdf(pdf_path, output_path)

# Paths to the input LaTeX file and the output preamble file
input_tex = "new_papers_creation/test_latex/Formatting-Instructions-LaTeX-2024_changed.tex"
output_tex = "new_papers_creation/test_latex/new_latex.tex"

extract_preamble(input_tex, output_tex)