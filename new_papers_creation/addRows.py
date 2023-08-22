import re
import pdfplumber
import subprocess
import os
import fitz

# def get_number_of_footnotes(latex_file_path):
#     with open(latex_file_path, 'r', encoding='utf-8') as latex_file:
#         latex_content = latex_file.read()
#     pattern = r'\\footnote{.*?}'
#     footnotes = re.findall(pattern, latex_content)
#     total_lines = 0
#     for footnote in footnotes:
#         lines = footnote.split('\n')
#         total_lines += len(lines)
#     return total_lines
    
def add_to_latex(tex_file_path, lines):
        with open(tex_file_path, "r") as input_file:
            file_content = input_file.read()
        pattern = r"\\clearpage\s*\\bibliography\{(.*?)\}"
        match = re.search(pattern, file_content)
        if match:
            modified = (
            file_content[:match.start()]
            + lines
            +'\n'
            + file_content[match.start():]
            )
            with open(tex_file_path, "w") as output_file:
                output_file.write(modified)
                
def remove_from_latex(tex_file_path, lines):
    pass           

def find_bibliography_format(line):
    pattern = r'\\bibliography\{(.*?)\}'
    match = re.search(pattern, line)
    return True if match else False

def count_lines_in_page(pdf_path, page_number):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]  
        text = page.extract_text()
        lines = text.strip().split('\n')
        for line in lines: #check if page number is considered a line
            if line == str(page_number+1): #page number starts from 0
                lines.remove(line)
                print("removed page number", page_number+1)
        print(lines)
        line_count = len(lines)
    return line_count

def find_page_number_before_bibliography(pdf_path, bibliography_keyword):
    pdf_document = fitz.open(pdf_path)
    found_page_number = None
    found = False
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        page_text = page.get_text()
        
        if bibliography_keyword in page_text:
            found_page_number = page_number  # Page numbering starts from 0
            found = True
            break
    pdf_document.close()
    
    if found:
        return found_page_number-1
    else:
        return None

#find bibliography format and add /clearpage before it
def add_clearpage_before_bibliography(tex_file_path):
    try: 
        if not os.path.exists(tex_file_path):
            print("File path {} does not exist. Exiting...".format(tex_file_path))
            return
        with open(tex_file_path, "r") as input_file:
            file_content = input_file.read()
        pattern = r'\\bibliography\{(.*?)\}'
         
        match = re.search(pattern, file_content)
        if match:
            print("found bibliography format on line", match)
            modified_content = re.sub(
            pattern,
            r"\\clearpage\n\\bibliography{\1}",
            file_content,
            count=1,
            )
            with open(tex_file_path, "w") as output_file:
                output_file.write(modified_content)
    except Exception as e:
        print(f"An error occurred: {e}")
        

def compile_latex_to_pdf(latex_file_path):
    try:
        dir_path = os.path.dirname(latex_file_path)
        base_name = os.path.splitext(os.path.basename(latex_file_path))[0]
        
        subprocess.run(["tectonic", latex_file_path])
        pdf_file_path = os.path.join(dir_path, base_name + ".pdf")
        return pdf_file_path
        
    except subprocess.CalledProcessError as e:
        print("Error during LaTeX to PDF conversion:", e)
 
 
text_to_add = "We consider a multi-level jury problem in which experts are" 
        
def main():
    # tex_file_path = "new_papers_creation\\AAAI-12\\aaai12-29 copy.tex"
    tex_file_path = "new_papers_creation\Who Reviews The Reviewers_ A Multi-Level Jury Problem\AAAI2024\example2lines.tex"
    add_clearpage_before_bibliography(tex_file_path)
    pdf_file_path = compile_latex_to_pdf(tex_file_path)
    keyword = "References"
    line_threshold = 66
    lines = 0
    while (lines != 3):
        text_to_add = "We consider a multi-level jury problem in which experts are\n" 
        page_number = find_page_number_before_bibliography(pdf_file_path, keyword)
        print("page number before bibliography is", page_number)
        lines = count_lines_in_page(pdf_file_path, page_number)
        print("lines in page", lines)
        if lines == 3:
            print("paper is all ready with 3 lines on the last page")
            return
        if lines < 3: 
            add_to_latex(tex_file_path, text_to_add)
        elif lines > line_threshold:
            add_to_latex(tex_file_path, text_to_add*(132-lines))
        else:
            remove_from_latex(tex_file_path, lines)
            print("lines are more than 3 but less than threshold")
            return
        pdf_file_path = compile_latex_to_pdf(tex_file_path)
        
    
main()

# pdf_file = "new_papers_creation\\AAAI13-QDEC\\QDEC-POMDP.8.pdf"
# pdf_file = "new_papers_creation\\AAAI-12\\aaai12-29 copy.pdf"
