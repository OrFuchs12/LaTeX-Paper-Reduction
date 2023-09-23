
import os
import re
import shutil
import fitz
import re


number_of_last_pages = 2

pdf_path = 'last_pages_from_full_paper\AAAI 2016\prize_changed.pdf'
  
#create a new pdf file with only last pages
def copy_last_pages(input_pdf_path, output_pdf_path, number_of_last_pages):
    
    pdf_document = fitz.open(input_pdf_path)
    total_pages = len(pdf_document)
    new_pdf_document = fitz.open()
    
    for page_num in range(total_pages - number_of_last_pages, total_pages):
        new_pdf_document.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
    
    new_pdf_document.save(output_pdf_path)
    
    pdf_document.close()
    new_pdf_document.close()
            
# copy_last_pages(pdf_path, "output.pdf", number_of_last_pages)

def remove_comments(latex_path):
    with open(latex_path, 'r') as f:
        lines = f.readlines()
    with open(latex_path, 'w') as f:
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
    
                
remove_astrik_inside_paranthases("code\\greedy_from_machine\\files\\prize_changed.tex")