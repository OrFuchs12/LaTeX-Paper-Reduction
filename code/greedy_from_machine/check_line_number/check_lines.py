import os
import shutil

import PyPDF2
import pdfplumber

#iterate over "Paper Greedy" directory and foreach pdf file check number of lines in the last page. if it is 3 then move to the folder "3_lines" otherwise move to the folder "not_3_lines"
def count_lines_in_page(pdf_path, page_number):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]  
        text = page.extract_text()
        lines = text.strip().split('\n')
        if lines[-1] == str(page_number+1): #check if page number was added like a line
            lines.remove(lines[-1])
        line_count = len(lines)
    return line_count
    
directory = 'C:\\Users\\orfuc\\OneDrive\\שולחן העבודה\\LaTeX-Paper-Reduction-4\\code\\greedy_from_machine\\check_line_number\\Paper_Greedy'
directory2 = 'C:\\Users\\orfuc\\OneDrive\\שולחן העבודה\\LaTeX-Paper-Reduction-4\\code\\greedy_from_machine\\check_line_number'
for file in os.listdir(directory):
    if not file.endswith('.pdf'):
        continue
    file_path = os.path.join(directory, file)
    lines = count_lines_in_page(file_path, -1)
    if lines == 3:
        new_direcotry = os.path.join(directory2, '3_lines')
        shutil.move(file_path, new_direcotry)
    else:
        new_direcotry = os.path.join(directory2, 'not_3_lines')
        shutil.move(file_path, new_direcotry)