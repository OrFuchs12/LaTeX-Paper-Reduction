import re
import pdfplumber
import subprocess
import os
import fitz
from lorem_text import lorem
# import the file code/greedy_from_machine/Last_2_pages_rows_extract.py






NUMBER_OF_LINES_ON_LAST_PAGE = 2
ESTIMATED_LINES_PER_PAGE = 10
def clean_latex_line(helpline):
    regex = re.compile('[^a-zA-Z]')
    pattern = r'\\cite\{[^\}]+\}'
    helpline = re.sub(pattern, '', helpline)
    pattern = r'\\citet\{[^\}]+\}'
    helpline = re.sub(pattern, '', helpline)
    pattern = r'\\ref\{[^\}]+\}'
    helpline = re.sub(pattern, '', helpline)
    pattern = r'\\label\{[^\}]+\}'
    helpline = re.sub(pattern, '', helpline)
    helpline = helpline.replace(r'\emph', '')
    helpline = helpline.replace(r'\textit', '')
    helpline = helpline.replace(r'\textbf', '')
    helpline = helpline.replace(r'\phi', '') 
    helpline = helpline.replace(r'\cdot', '')
    helpline = helpline.replace(r'\em', '')
    helpline = helpline.replace(r'\underline', '')
    helpline = helpline.replace(r'\protect', '')
    latex_command_pattern = re.compile(r'\\[a-zA-Z]+')
    helpline = re.sub(latex_command_pattern, '', helpline)
    helpline = regex.sub(' ', helpline)
    helpline = remove_math_patterns(helpline)
    helpline = re.sub(r'[^a-zA-Z]+', '', helpline)
    helpline= helpline.lower()

    return helpline

def remove_math_patterns(text):
    # Stage 1: Identify parts enclosed by $
    pattern = r'\$.*?\$'
    matches = re.finditer(pattern, text)

    for match in matches:
        original_match = match.group(0)
        
        # Stage 2: Replace 'something_letter' or 'something_number' with 'something_'
        replacement = re.sub(r'_(\w)', '_', original_match)
        replacement = re.sub(r'_\{.*?\}', '_', replacement)
        replacement = re.sub(r'\\mathcal', '', replacement)
        text = text.replace(original_match, replacement, 1)  # Replace only the first occurrence


    frac_pattern = re.compile(r'\\frac\{(\w+)\}\{(\d+)\} ([^\s]+) (\d+)')
    # Replace the pattern with the desired format
    text = re.sub(frac_pattern, r'{\1} \3 \4', text)
    return text


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
        bottom_area_top = page_height * (1/2)  
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

def add_to_latex(tex_file_path):
        lorem_ipsum_text = lorem.sentence()
        with open(tex_file_path, "r", encoding="utf-8") as input_file:
            file_content = input_file.read()
        pattern = r"\\clearpage\s*\\bibliography\{(.*?)\}"
        match = re.search(pattern, file_content)
        if match:
            modified = (
            file_content[:match.start()]
            + lorem_ipsum_text
            + file_content[match.start():]
            )
            with open(tex_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(modified)
        pdf_file_path = compile_latex_to_pdf(tex_file_path)
        page_number = find_page_number_before_bibliography(pdf_file_path, "References")
        lines=count_lines_in_page(pdf_file_path, page_number)
        return lines, page_number


                
def remove_from_latex(tex_file_path, chars):
    with open(tex_file_path, "r", encoding="utf-8") as input_file:
        file_content = input_file.read()
    pattern = r"\\clearpage\s*\\bibliography\{(.*?)\}"
    match = re.search(pattern, file_content)
    if match:
        modified = (
        file_content[:match.start()-chars]
        + file_content[match.start():]
        )
        with open(tex_file_path, "w", encoding="utf-8") as output_file:
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
            text = page.extract_text(strip=False, join_tolerance=10)
            lines = text.strip().split('\n')
            return lines
        except:
            print("error in getLines")
            return None
    
def find_last_line_text(lines, last_index=-1):
        return lines[last_index]
    


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
    
    if found:
        num = found_page_number-1
    else:
        num = page_number
    pdf_document.close()
    return num

#find bibliography format and add /clearpage before it
def add_clearpage_before_bibliography(tex_file_path):
    try: 
        if not os.path.exists(tex_file_path):
            print("File path {} does not exist. Exiting...".format(tex_file_path))
            return
        with open(tex_file_path, "r", encoding="utf-8") as input_file:
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
        pattern = r"\\clearpage\s*\\bibliography\{(.*?)\}"
        match = re.search(pattern, modified_content)
        
        #check if \clearpage\n\bibliography has a % before it and if so remove it
        if modified_content[match.start()] == "%":
            modified_content = modified_content[:match.start()-1] + modified_content[match.start():]
            
        with open(tex_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(modified_content)
    except Exception as e:
        print(f"An error occurred: {e}")
        
def compile_latex_to_pdf(latex_file_path):
    try:
        dir_path = os.path.dirname(latex_file_path)
        print(dir_path)
        print(latex_file_path)
        base_name = os.path.basename(latex_file_path)
        subprocess.run(['pdflatex', base_name], cwd=dir_path)
        base_name = os.path.splitext(os.path.basename(latex_file_path))[0]

        pdf_file_path = os.path.join(dir_path, base_name + ".pdf")
        return pdf_file_path
        
    except subprocess.CalledProcessError as e:
        print("Error during LaTeX to PDF conversion:", e)
 
def check_only_text(pdf_path, page_number, lines_on_last_page, latex_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]  
        text = page.extract_text()
        images = page.images
        tables = page.find_tables()
        # other = get_tables_and_images(lines_on_last_page, latex_path)
        return bool(text) and not bool(images) and not bool(tables) #and not bool(other)
    
    
def remove_line(latex_file_path, pdf_line):
    removed = False
    # clean the pdf line
    clean_pdf_line = re.sub(r'[^a-zA-Z0-9]+', '', pdf_line)
    clean_pdf_line = clean_pdf_line.lower()

    
    # loop throgh the lines in the latex file backwards
    with open(latex_file_path, "r", encoding="utf-8") as input_file:
        file_content = input_file.read()
    lines = file_content.strip().split('\n')
    for line in reversed(lines):
        #if line starts with \ it is a commands and sould be skipped
        if line.startswith("%"):
            continue
        # clean the line 
        cleaned_latex_line = clean_latex_line(line)
        # check if clean_pdf_line is a substring of cleaned_latex_line
        if clean_pdf_line in cleaned_latex_line:
            try:
                if (line.startswith("\\")):
                    new_line = ""
                else: 
                    space_count = 0
                    index = len(line)
                    while space_count < 5:
                        index = line.rfind(' ', 0, index - 1)
                        if index == -1:
                            break
                        space_count += 1

                    new_line = line[:index]
                #if in the line[:index+1] there is { and  not } then find the next } and delete until there
                while new_line.count("{") > new_line.count("}"):
                    # find the index of the last {
                    index = new_line.rfind('{')
                    new_line = new_line[:index]
                # switch the line with the new line in the lines list
                lines[lines.index(line)] = new_line
                
                
            except ValueError:
            # remove the line from the latex file
                lines.remove(line)
            print("removed the line: ", line[:index+1])
            removed = True
            break
    if removed:
    # write the new latex file
        with open(latex_file_path, "w", encoding="utf-8") as output_file:
            output_file.write('\n'.join(lines))
        return True
    else:
        print("line not found")
        return False

def remove_lines(pdf_file_path, latex_path, page_number, lines_on_last_page):
    if (len(lines_on_last_page) == 0):
        lines_on_last_page = getLines(pdf_file_path, page_number-1)
    last_line_to_remove = find_last_line_text(lines_on_last_page)
    while not remove_line(latex_path, last_line_to_remove):
        if len(lines_on_last_page) != 0:
            lines_on_last_page.pop()
            if (len(lines_on_last_page) == 0):
                lines_on_last_page = getLines(pdf_file_path, page_number-1)
            last_line_to_remove = find_last_line_text(lines_on_last_page, -1)
        else:
            lines_on_last_page = getLines(pdf_file_path, page_number-1)
            last_line_to_remove = find_last_line_text(lines_on_last_page, -1)
    lines_on_last_page.pop()
    pdf_file_path = compile_latex_to_pdf(latex_path)
    page_number = find_page_number_before_bibliography(pdf_file_path, "References")
    lines=count_lines_in_page(pdf_file_path, page_number)
    return lines, page_number, lines_on_last_page


# main function
def create_extra_line_page(new_file_path):
    add_clearpage_before_bibliography(new_file_path)
    remove_appendix_content(new_file_path)
    pdf_file_path = compile_latex_to_pdf(new_file_path)
    keyword = "References"
    lines = 0
    page_number = find_page_number_before_bibliography(pdf_file_path, keyword)
    print("page number before bibliography is", page_number)
    lines = count_lines_in_page(pdf_file_path, page_number)
    lines_on_last_page = getLines(pdf_file_path, page_number, next)

    while (lines != NUMBER_OF_LINES_ON_LAST_PAGE):
        #TODO: text to add should be also lorem ipsum
        if lines < NUMBER_OF_LINES_ON_LAST_PAGE: 
            lines, page_number = add_to_latex(new_file_path)
            lines_on_last_page = getLines(pdf_file_path, page_number)
        elif check_content_on_second_column(pdf_file_path, page_number):
            print("there is content on the second column on the bottom")
            lines, page_number = add_to_latex(new_file_path)
            lines_on_last_page = getLines(pdf_file_path, page_number)
        #TODO: not add text but delete sections until image/table goes up a page, maybe need to  
        #add a check if there is an algorithm 
        elif not check_only_text(pdf_file_path, page_number, lines_on_last_page, new_file_path):
            print("not only text on the last page")
            lines, page_number = add_to_latex(new_file_path)
            lines_on_last_page = getLines(pdf_file_path, page_number)
        else:
            lines, new_page_number, lines_on_last_page = remove_lines(pdf_file_path, new_file_path, page_number, lines_on_last_page)
            if new_page_number != page_number:
                page_number = new_page_number
                lines_on_last_page = getLines(pdf_file_path, page_number)
            if len(lines_on_last_page) == 0:
                lines_on_last_page = getLines(pdf_file_path, page_number-1)
    
    

def get_tables_and_images(lines_on_last_page, latex_file_path):
    #get all the senstences that begin with \caption{ and end with }
    pattern = r"\\caption\{(.*?)\}"
    with open(latex_file_path, "r", encoding="utf-8") as input_file:
        file_content = input_file.read()
    matches = re.findall(pattern, file_content)
    #check if any of the matches are in lines on last page, but first leave only numbers and letters for both lines
    clean_lines_on_last_page = [re.sub(r'[^a-zA-Z0-9]+', '', line) for line in lines_on_last_page]
    clean_matches = [re.sub(r'[^a-zA-Z0-9]+', '', match) for match in matches]
    latex_match = clean_matches[-1]
    for pdf_match in clean_lines_on_last_page:
            if latex_match in pdf_match:
                return True
    return False



def remove_appendix_content(latex_file_path):
    # find \\appendix command
    with open(latex_file_path, "r", encoding="utf-8") as input_file:
        file_content = input_file.read()
    pattern_start = r"\\appendix"
    match_start = re.search(pattern_start, file_content)
    # remove all the content after the command untill \\clearpage
    pattern_end = r"\\clearpage"
    pattern_second_end = r"\\end{document}"
    match_end = re.search(pattern_end, file_content)
    if match_start and match_end:
        if match_end.start() < match_start.start():
            match_end = re.search(pattern_second_end, file_content)
        modified_content = (
        file_content[:match_start.start()]
        + file_content[match_end.start():]
        )
        with open(latex_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(modified_content)
    else:
        print("no appendix found")
        return False
    



def brace_count_check(line):
    if line.count("{") < line.count("}"):
        return True
    else:
        return False