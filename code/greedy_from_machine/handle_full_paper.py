
import os
import re
import shutil
import fitz
import re


NUMBER_OF_LAST_PAGES = 2

# pdf_path = 'last_pages_from_full_paper\AAAI 2016\prize_changed.pdf'
  
#create a new pdf file with only last pages
def copy_last_pages(input_pdf_path, NUMBER_OF_LAST_PAGES):
    output_pdf_path = input_pdf_path[:-4] + "_last_pages.pdf"
    pdf_document = fitz.open(input_pdf_path)
    total_pages = len(pdf_document)
    new_pdf_document = fitz.open()
    
    for page_num in range(total_pages - NUMBER_OF_LAST_PAGES, total_pages):
        new_pdf_document.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
    
    new_pdf_document.save(output_pdf_path)
    
    pdf_document.close()
    new_pdf_document.close()
    return output_pdf_path
            
# copy_last_pages("code/greedy_from_machine/files/samd_changed.pdf", "output.pdf", NUMBER_OF_LAST_PAGES)

def remove_comments(latex_path):
    with open(latex_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(latex_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if not re.match(r'^\s*%', line):
                f.write(line)

#things like \begin{figure*} become \begin{figure}
def remove_astrik_inside_paranthases(latex_path):
    with open(latex_path, 'r') as f:
        lines = f.readlines()
    with open(latex_path, 'w') as f:
        for line in lines:
            line = re.sub(r'\\begin{(\w+)\*}', r'\\begin{\1}', line)
            line = re.sub(r'\\end{(\w+)\*}', r'\\end{\1}', line)
            f.write(line)
    
# copy_last_pages("code/greedy_from_machine/files/Keller_changed.pdf", "updated_keller.pdf", NUMBER_OF_LAST_PAGES)