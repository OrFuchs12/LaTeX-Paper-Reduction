import pdfplumber

def is_text_only(pdf_path):
    """Check if a PDF page contains only text."""
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        # Check for images
        if page.images:
            return False
        # Check for tables
        if page.extract_tables():
            return False

    return True

def check_paper(folder):
    """Check the second last page of a PDF paper."""
    with pdfplumber.open(folder) as pdf:
        page = pdf.pages[-2]
        return is_text_only(page)