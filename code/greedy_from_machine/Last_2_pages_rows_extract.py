import pdfplumber
import re
import pdb
import PyPDF2
# import fitz
from handle_full_paper import remove_comments

NUMBER_OF_LAST_PAGES = 2

def find_first_row_in_last_page(pdf_file_path, latex_path):
    # Open the PDF file and extract the last page
    with pdfplumber.open(pdf_file_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        # Define the x-coordinate ranges for each column
        left_column = (0, 0, page.width / 2, page.height)
        # Extract text only from the left column
        text = page.within_bbox(left_column).extract_text()
        text = text.split('\n')
        iteration =0
        last_iteration = False
        return_index = 0
        while(len(text) > 1):
            if last_iteration:
                break
            
            first_line, is_start_table, is_start_figure, return_index, last_iteration = check_if_text_inside_table(pdf_file_path, text, latex_path, iteration, return_index)
            if is_start_table==False or is_start_figure==True:
                first_line, is_start_image, return_index = check_if_text_inside_image(pdf_file_path, text, latex_path, is_start_figure)
            if is_start_table or is_start_figure or is_start_image:
                #the first line is different from the first line in text and we need to check again if the first line is inside table or image
                text= text[return_index:]
                iteration+=1
            else:
                break
             
                
                
        return first_line


def check_if_text_inside_image(pdf_path, text_in_page, latex_path, is_start_figure = False):
    return_index = 0
    index = 0
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        if is_start_figure:
            #find the first line of text in page that starts with Figure
            for index, line in enumerate(text_in_page):
                if line.startswith('Figure'):
                    text_in_page = text_in_page[index:]
                    break
        if text_in_page[0].startswith('Figure'):
                text_in_page, return_index = remove_caption(text_in_page, latex_path, 'Figure')
                return text_in_page, True, return_index+index        
        return text_in_page[0], False, return_index+index
    
def convert_Latex_to_rows_list(latex_path,pdf_path):
    # list of rows to extract from the latex file
    rows_list = []
    # the first row in the page we want to start the extraction from
    first_row_to_begin = find_first_row_in_last_page(pdf_path, latex_path)
    print(first_row_to_begin)
    # clean the line to make it easier to compare
    clean_line = re.sub(r'[^a-zA-Z0-9]+', '', first_row_to_begin)
    # search the line in  the latex file
    try:
        with open(latex_path, 'r',encoding='utf-8', errors='ignore') as tex_file:
            file_content = tex_file.read()
        lines = file_content.strip().split('\n')
        # count the number of lines before the line we want to start the extraction from
        lines_before_the_line = 0
        # flag to know if we found the line we want to start the extraction from
        found_start = False
        # flag to know if we found the line we want to end the extraction from
        found_end = False
        # clean the line to make it easier to compare
        pattern = r'\\[a-zA-Z]+(?:\[[^\]]\])?(?:\{[^\}]\})?'

        for line in lines:
            # Use re.sub to replace LaTeX commands with an empty string
            clean_linePDF = re.sub(pattern, '', line)
            clean_latex_line_to_compare = re.sub(r'[^a-zA-Z0-9]+', '', clean_linePDF)
            while(not found_start and clean_line not in clean_latex_line_to_compare):
                lines_before_the_line += 1
                rows_list.append('\n')
                break
            if(not found_start and clean_line in clean_latex_line_to_compare):
                print("found the line")
                print(clean_line)
                print(clean_latex_line_to_compare)
                rows_list.append(line)
                found_start = True
                continue                

            while found_start and not line.startswith("\\end{document}"):
                if(line == ''):
                    rows_list.append('\n')
                    break
                else:
                    rows_list.append(line)
                    break
            if found_start and line.startswith("\\end{document}"):
                rows_list.append(line)
                found_end = True
                break
        rows_list = check_tables_images_last_pages_pdf(pdf_path, rows_list, latex_path, 'Figure')
        rows_list = check_tables_images_last_pages_pdf(pdf_path, rows_list, latex_path , 'Table')
        
        return rows_list
                    
    #check for missing tables and images
    except Exception as e:
            print(f"An error occurred: {e}")

def extract_text_from_tables(pdf_path, latex_path,text, iteration, return_index=0):
    is_table = False
    is_figure = False
    text = ""
    first_line = ""
    last_iteration = False
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        left_column = (0, 0, page.width / 2, page.height)
        tables = page.within_bbox(left_column).find_tables()
        if tables:
            is_table = True
            if len(tables) == iteration+1:
                last_iteration = True                
            first_table = tables[iteration]
            table_bbox = first_table.bbox
            #get the first y_coordinate of table
            first_y_coordinate = table_bbox[1]
            text_inside_table = page.extract_tables()[0]
            #get the text in the page of the left column
            left_column = (0, 0, page.width / 2, page.height)
            # Extract text only from the left column and separate by lines
            text = page.within_bbox(left_column).extract_text_lines()
            
            #check if the first line in the text is not in the table then its the first line
            if text[return_index]['top'] < first_y_coordinate and text[return_index]['bottom'] < first_y_coordinate and not text[0]['text'].startswith('Table'):
                return text[0], is_table, is_figure, 0, last_iteration
            #the table is first so we need to get the y coordinate of the last line in the table
            y_coordinate = table_bbox[3]
            #get the first line in page that is after the table
            for index, line in enumerate(text):
                if line['top'] > y_coordinate:
                    line = text[index]
                    #extract text only from after the table so from y_coordinate
                    bbox = (0, y_coordinate, page.width / 2, page.height)
                    rel_text = page.within_bbox(bbox).extract_text()
                    rel_text = rel_text.split('\n')
                    if line['text'].startswith('Table'):
                        first_line, return_index = remove_caption(rel_text, latex_path, 'Table')
                        return_index += index
                    #find images that were detected as tables
                    elif not text[0]['text'].startswith('Table'):
                        is_figure = True
                        is_table = False
                        first_line = None
                        break
                    else: 
                        first_line = rel_text[0]
                        return_index = index
                    break
        return first_line, is_table, is_figure, return_index, last_iteration
    
def check_if_text_inside_table(pdf_path, text_in_page, latex_path, iteration=0, return_index=0):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        text_after_table, is_table, is_figure, return_index, last_iteration = extract_text_from_tables(pdf_path, latex_path, text_in_page,iteration,return_index)
        return text_after_table, is_table, is_figure, return_index, last_iteration
                            
def remove_caption(text_in_page, latex_path , caption_type):
    with open(latex_path, 'r', encoding='utf-8' ) as f:
        lines = f.readlines()
    #find all lines that start with \caption
    caption_lines = []
    temp_line= ""
    pattern = r'^\s*\\caption'
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            if '}' in line:
                caption_lines.append(line)
            else:
                temp_line= line
                index=i
                while '}' not in lines[index]:
                    index+=1
                    temp_line+=lines[index]
                caption_lines.append(temp_line)
    #remove \caption from the lines
    caption_lines = [line.replace(r'\caption{', '') for line in caption_lines]
    #keep only what is before }
    caption_lines = [line.split('}')[0] for line in caption_lines]
    #leave only numbers and letters in the lines
    caption_lines = [re.sub(r'[^a-zA-Z0-9]+', '', line) for line in caption_lines]
    #find the caption that starts with text_in_page[0]
    caption_line = ''
    text_index = 0
    beginning_of_caption = text_in_page[text_index].split(':')[1]

    while len(caption_lines) >1:
        for index, line in enumerate(caption_lines):
            clean_beginning_of_caption = re.sub(r'[^a-zA-Z]+', '', beginning_of_caption)
            if clean_beginning_of_caption in line:
                continue
            else:
                caption_lines[index] = ''
        #remove the empty lines
        caption_lines = list(filter(None, caption_lines))
        text_index+=1
        beginning_of_caption = text_in_page[text_index]

    caption_line = caption_lines[0]

    clean_caption_line = re.sub(r'[^a-zA-Z]+', '', caption_line)
    for index, line in enumerate(text_in_page):
        #remove the regex Table\d: from clean_line
        if caption_type == 'Table':
            clean_line = re.sub(r'Table\d*:', '', line)
        if caption_type == 'Figure':
            clean_line = re.sub(r'Figure\s*\d*:', '', line)
        clean_line = re.sub(r'[^a-zA-Z]+', '', clean_line)
        #search for cdot in the clean_caption_line and remove
        clean_caption_line = clean_caption_line.replace('cdot', '')
        if clean_line in clean_caption_line:
            text_in_page[index] = ''
        else:
            break
    #filter out empty lines
    text_in_page = list(filter(None, text_in_page))
    return text_in_page[0], index

def check_tables_images_last_pages_pdf(pdf_path, rows_list ,latex_path , caption_type) :  
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages[-NUMBER_OF_LAST_PAGES:]
        for page in pages:
            page_text = page.extract_text()
            if caption_type == 'Figure':
                table_to_find = re.findall(r'Figure\s*\d*:', page_text)
            elif caption_type == 'Table':
                table_to_find = re.findall(r'Table\s*\d*:', page_text)
            for table in table_to_find:
                index= re.search(r'\d+', table).group()
                with open(latex_path, 'r', encoding='utf-8', errors='ignore') as tex_file:
                    file_content = tex_file.read()
                    lines = file_content.strip().split('\n')
                    table_started = False
                    table_latex= []
                    if caption_type == 'Figure':
                        begin_pattern= r'\begin{figure'
                        end_pattern= r'\end{figure' #check if it is the right pattern
                    if caption_type == 'Table':
                         begin_pattern= r'\begin{table'
                         end_pattern= r'\end{table'#check if it is the right pattern
                    index_counter = 1
                    index_in_latex = 0
                    for line in lines:
                        if begin_pattern in line and index_counter == int(index):
                            index_in_latex = lines.index(line)
                            table_started = True
                            table_latex.append(line)
                            line = ""
                        elif table_started and end_pattern not in line:
                            table_latex.append(line)
                        elif begin_pattern in line and index_counter < int(index):
                            index_counter+=1
                            # table_started = True
                            # table_latex.append(line)
                            line = ""
                        elif end_pattern in line and table_started:
                            table_latex.append(line)
                            line = ""
                            table_started = False
                            break
                    found_table = True
                    for line in table_latex:
                        if line not in rows_list:
                            found_table = False
                            break
                    if not found_table:
                        for line in table_latex:
                            rows_list[index_in_latex] = line
                            index_in_latex+=1
                       
    return rows_list





# remove_comments("code/greedy_from_machine/test_lidor/main_changed.tex")
# convert_Latex_to_rows_list("code/greedy_from_machine/test_lidor/main_changed.tex", "code/greedy_from_machine/test_lidor/main_changed.pdf")