import re
import pdfplumber
import subprocess
import os
import fitz
from lorem_text import lorem


NUMBER_OF_LINES_ON_LAST_PAGE = 2
ESTIMATED_LINES_PER_PAGE = 10

#TODO: maybe add a check for tables 
def check_content_on_second_column(pdf_path, page_number=0):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        
        text_blocks = page.extract_words()
        images = page.images
        tables = page.extract_tables()
        
        page_width = page.width
        second_column_left = page_width * (1 / 2)  
        second_column_right = page_width

        page_height = page.height
        bottom_area_top = page_height * (2 / 3)  
        bottom_area_bottom = page_height 
        
        text_on_bottom_right = any(
            block for block in text_blocks if 
            second_column_left <= block['x0'] <= second_column_right and
            bottom_area_top <= block['bottom'] <= bottom_area_bottom
        )

        images_on_bottom_right = any(
            image for image in images if
            second_column_left <= image['x0'] <= second_column_right and
            bottom_area_top <= image['y0'] <= bottom_area_bottom
        )
                
        return text_on_bottom_right or images_on_bottom_right 

def add_to_latex(tex_file_path, lines):
        lorem_ipsum_text = lorem.sentence()
        with open(tex_file_path, "r") as input_file:
            file_content = input_file.read()
        pattern = r"\\clearpage\s*\\bibliography\{(.*?)\}"
        match = re.search(pattern, file_content)
        if match:
            modified = (
            file_content[:match.start()]
            + lorem_ipsum_text
            + file_content[match.start():]
            )
            with open(tex_file_path, "w") as output_file:
                output_file.write(modified)
        pdf_file_path = compile_latex_to_pdf(tex_file_path)
        page_number = find_page_number_before_bibliography(pdf_file_path, "References")
        lines=count_lines_in_page(pdf_file_path, page_number)
        return lines


                
def remove_from_latex(tex_file_path, chars):
    with open(tex_file_path, "r") as input_file:
        file_content = input_file.read()
    pattern = r"\\clearpage\s*\\bibliography\{(.*?)\}"
    match = re.search(pattern, file_content)
    if match:
        modified = (
        file_content[:match.start()-chars]
        + file_content[match.start():]
        )
        with open(tex_file_path, "w") as output_file:
            output_file.write(modified)

def count_lines_in_page(pdf_path, page_number):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]  
        text = page.extract_text()
        lines = text.strip().split('\n')
        if lines[-1] == str(page_number+1): #check if page number was added like a line
            lines.remove(lines[-1])
        line_count = len(lines)
    return line_count

def getLines(pdf_path, page_number, next=False):
     with pdfplumber.open(pdf_path) as pdf:
        try:
            if next ==True:
                page_number = page_number-1
            page = pdf.pages[page_number]  
            text = page.extract_text()
            lines = text.strip().split('\n')
            return lines
        except:
            print("error in getLines")
            return None
    
def find_last_line_text(lines, last_index=-1):
        return lines[last_index]
    
def search_last_line(tex_file_path, last_line_to_remove):
    with open(tex_file_path, "r") as input_file:
        file_content = input_file.read()
    if last_line_to_remove[-1] == "-":
        last_line_to_remove = last_line_to_remove[:-1]
    pattern = r"{}".format(last_line_to_remove)
    try:
        match = re.search(pattern, file_content)    
        if match:
            modified = (
            file_content[:match.start()]
            + file_content[match.end():]
            )
            with open(tex_file_path, "w") as output_file:
                output_file.write(modified)
            return True
        else:
            print("last line not found")
            return False
    except:
        print("error in search_last_line")
        return False

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
 
def check_only_text(pdf_path, page_number):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]  
        text = page.extract_text()
        images = page.images
        tables = page.extract_tables()
        return bool(text) and not bool(images) and not bool(tables)

def remove_lines(pdf_file_path, latex_path, page_number, lines_on_last_page, next=False):
    last_line_to_remove = find_last_line_text(lines_on_last_page, -1)
    while not search_last_line(latex_path, last_line_to_remove):
        lines_on_last_page.remove(lines_on_last_page[-1])
        if len(lines_on_last_page) != 0:
            last_line_to_remove = find_last_line_text(lines_on_last_page, -1)
    print("removing the lines: ", last_line_to_remove)
    pdf_file_path = compile_latex_to_pdf(latex_path)
    page_number = find_page_number_before_bibliography(pdf_file_path, "References")
    lines=count_lines_in_page(pdf_file_path, page_number)
    return lines

def create_extra_line_page(new_file_path):
    add_clearpage_before_bibliography(new_file_path)
    pdf_file_path = compile_latex_to_pdf(new_file_path)
    keyword = "References"
    lines = 0
    page_number = find_page_number_before_bibliography(pdf_file_path, keyword)
    print("page number before bibliography is", page_number)
    lines = count_lines_in_page(pdf_file_path, page_number)
    lines_on_last_page = getLines(pdf_file_path, page_number, next)

    while (lines != NUMBER_OF_LINES_ON_LAST_PAGE):
        text_to_add = "We consider a multi-level jury problem in which experts\n" 
        if lines == NUMBER_OF_LINES_ON_LAST_PAGE:
            print("paper is allready with 3 lines on the last page")
            return
        #TODO: text to add should be also lorem ipsum
        if lines < NUMBER_OF_LINES_ON_LAST_PAGE: 
            lines = add_to_latex(new_file_path, (NUMBER_OF_LINES_ON_LAST_PAGE-lines)*text_to_add)
            
        elif check_content_on_second_column(pdf_file_path, page_number):
            print("there is content on the second column on the bottom")
            lines = add_to_latex(new_file_path, ESTIMATED_LINES_PER_PAGE)
        #TODO: not add text but delete sections until image/table goes up a page, maybe need to  
        #add a check if there is an algorithm 
        elif not check_only_text(pdf_file_path, page_number):
            print("not only text on the last page")
            lines = add_to_latex(new_file_path, ESTIMATED_LINES_PER_PAGE)
        else:
            lines = remove_lines(pdf_file_path, new_file_path, page_number, lines_on_last_page)
            if len(lines_on_last_page) == 0:
                lines_on_last_page = getLines(pdf_file_path, page_number-1)



        



