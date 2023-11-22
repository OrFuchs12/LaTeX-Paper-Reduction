import pdfplumber
import re
import pdb
import PyPDF2
from handle_full_paper import remove_comments

NUMBER_OF_LAST_PAGES = 2

def remove_math_patterns(text):
    # Stage 1: Identify parts enclosed by $
    pattern = r'\$.*?\$'
    matches = re.finditer(pattern, text)

    for match in matches:
        original_match = match.group(0)
        
        # Stage 2: Replace 'something_letter' or 'something_number' with 'something_'
        replacement = re.sub(r'_(\w)', '_', original_match)
        text = text.replace(original_match, replacement, 1)  # Replace only the first occurrence

    return text

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
            #look for tables/figures that are at the beginning of the page in order to find first line after them 
            first_line, is_start_table, is_start_figure, return_index, last_iteration = check_if_text_inside_table(pdf_file_path, text, latex_path, iteration, return_index)
            if is_start_table==False or is_start_figure==True:
                first_line, is_start_image, return_index, last_iteration = check_if_text_inside_image(pdf_file_path, text, latex_path, is_start_figure)
            if is_start_table or is_start_figure or is_start_image:
                #incase there are more than one table/figure one after another in the beginning page
                text= text[return_index:]
                iteration+=1
            else:
                break

        return first_line

def check_if_text_inside_image(pdf_path, text_in_page, latex_path, is_start_figure = False):
    return_index = 0
    index = 0
    last_iteration = False
    with pdfplumber.open(pdf_path) as pdf:
        # page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        if is_start_figure:
            #find the first line of text in page that starts with Figure
            for index, line in enumerate(text_in_page):
                if line.startswith('Figure'):
                    text_in_page = text_in_page[index:]
                    break
        if text_in_page[0].startswith('Figure'):
                text_in_page, return_index = remove_caption(text_in_page, latex_path, 'Figure')
                if return_index == 0:
                    last_iteration = True
                return text_in_page, True, return_index+index, last_iteration
        #handling subfigures
        pattern = r'\([a-z]\)'
        if re.match(pattern, text_in_page[0]):
            #Assuming that the general caption comes after each subcaption-
            #remove lines from text in page until we find a line that starts with Figure
            for index, line in enumerate(text_in_page):
                if line.startswith('Figure'):
                    text_in_page = text_in_page[index:]
                    break
            text_in_page, return_index = remove_caption(text_in_page, latex_path, 'Figure')
            return text_in_page, True, return_index+index, last_iteration
        return text_in_page[0], False, return_index+index, last_iteration

def convert_Latex_to_rows_list(latex_path,pdf_path):
    remove_comments(latex_path)
    rows_list = []
    # the first row in the page we want to start the extraction from
    first_row_to_begin = find_first_row_in_last_page(pdf_path, latex_path)
    print(first_row_to_begin)
    # clean the line to make it easier to compare
    clean_line = re.sub(r'[^a-zA-Z0-9]+', '', first_row_to_begin)
    clean_line = clean_line.lower()
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
        match_was_in_second_line = False
        for i in range(len(lines)):
            if match_was_in_second_line:
                match_was_in_second_line = False
                continue
            first_line = lines[i]
            if i == 326:
                pass
            # Use re.sub to replace LaTeX commands with an empty string
            if i < len(lines) - 1:
                next_line= lines[i + 1]
                line = first_line + next_line
            else:
                line = lines[i]
            line = remove_math_patterns(line)
            # Define the pattern using regular expression
            frac_pattern = re.compile(r'\\frac\{(\w+)\}\{(\d+)\} ([^\s]+) (\d+)')
            # Replace the pattern with the desired format
            clean_line_latex = re.sub(frac_pattern, r'{\1} \3 \4', line)
            clean_line_latex = re.sub(pattern, '', clean_line_latex)
            clean_latex_line_to_compare = re.sub(r'[^a-zA-Z0-9]+', '', clean_line_latex)
            
            clean_next_line = remove_math_patterns(next_line)
            clean_next_line = re.sub(frac_pattern, r'{\1} \3 \4', clean_next_line)
            clean_next_line = re.sub(pattern, '', clean_next_line)
            clean_next_line = re.sub(r'[^a-zA-Z0-9]+', '', clean_next_line)
            clean_next_line = clean_next_line.lower()
            
            clean_line = clean_line.lower()
            clean_latex_line_to_compare = clean_latex_line_to_compare.lower()
            clean_next_line = clean_next_line.lower()
            
            while(not found_start and clean_line not in clean_latex_line_to_compare):
                lines_before_the_line += 1
                rows_list.append('\n')
                break
            
            if(not found_start and clean_line in clean_latex_line_to_compare):
                print("found the line")
                print(clean_line)
                print(clean_latex_line_to_compare)
                print(next_line)
                match_started_in_next_line = clean_line in clean_next_line
                if match_started_in_next_line:
                    rows_list.append('\n')
                    rows_list.append(next_line)
                    found_start = True
                    match_was_in_second_line = True
                else:
                    rows_list.append(first_line)
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
        #check that we found all the tables and images in the last pages
        rows_list = check_tables_images_last_pages_pdf(pdf_path, rows_list, latex_path, 'Figure')
        rows_list = check_tables_images_last_pages_pdf(pdf_path, rows_list, latex_path , 'Table')
        
        return rows_list
                    
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
        tt_table_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "text",
            
        }
        lt_table_settings = {
            "vertical_strategy": "text",
            "horizontal_strategy": "lines",
        }
        tt_tables = page.within_bbox(left_column).find_tables(tt_table_settings)
        if tt_tables:
            tables = tt_tables
        else:
            lt_tables = page.within_bbox(left_column).find_tables(lt_table_settings)
            if lt_tables:
                tables = lt_tables
        if tables and len(tables) > iteration:
            is_table = True
            if len(tables) == iteration+1:
                last_iteration = True                
            first_table = tables[iteration]
            table_bbox = first_table.bbox
            #get the first y_coordinate of table
            first_y_coordinate = table_bbox[1]
            table_text = ""
            left_column = (0, 0, page.width / 2, page.height)
            if tt_tables:
                tt_text_inside_table = page.extract_tables(tt_table_settings)[iteration][0]
                #make the list filter all None values
                tt_text_inside_table = list(filter(None, tt_text_inside_table))
                #make a string out of the list
                tt_text_inside_table = ''.join(tt_text_inside_table)
                #leave only letters and numbers
                tt_text_inside_table = re.sub(r'[^a-zA-Z0-9]+', '', tt_text_inside_table)
                table_text = tt_text_inside_table
            else:
                lt_text_inside_table = page.extract_tables(lt_table_settings)[iteration][0]
                #make the list filter all None values
                lt_text_inside_table = list(filter(None, lt_text_inside_table))
                #make a string out of the list
                lt_text_inside_table = ''.join(lt_text_inside_table)
                #leave only letters and numbers
                lt_text_inside_table = re.sub(r'[^a-zA-Z0-9]+', '', lt_text_inside_table)
                table_text = lt_text_inside_table
            #get the text in the page of the left column
            
            # Extract text only from the left column and separate by lines
            text = page.within_bbox(left_column).extract_text_lines()
            #extract text only from after the table so from y_coordinate
            y_coordinate = table_bbox[3]
            bbox = (0, y_coordinate, page.width / 2, page.height)
            rel_text = page.within_bbox(bbox).extract_text()
            rel_text = rel_text.split('\n')
            #check if the first line in the text is not in the table then its the first line
            if text[return_index]['top'] < first_y_coordinate and text[return_index]['bottom'] < first_y_coordinate and not text[0]['text'].startswith('Table'):
                #check if text[return_index] is inside text_inside_table
                clean_table_line = re.sub(r'[^a-zA-Z0-9]+', '', text[return_index]['text'])
                if clean_table_line in table_text:
                    text = text[return_index:]
                return text[0]["text"], is_table, is_figure, 0, last_iteration
            #the table is first so we need to get the y coordinate of the last line in the table
            
            
            
            #get the first line in page that is after the table
            for index, line in enumerate(text):
                if line['top'] > y_coordinate:
                    line = text[index]

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
            brace_count = line.count('{') - line.count('}')
            temp_line= line
            if brace_count > 0:
                index=i
                while brace_count > 0:
                    index+=1
                    temp_line+=lines[index]
                    brace_count += lines[index].count('{') - lines[index].count('}')
                caption_lines.append(temp_line)
            else:
                caption_lines.append(temp_line)
    #replace any \emph in the lines
    caption_lines = [line.replace(r'\emph', '') for line in caption_lines]
    #replace any \textit in the lines
    caption_lines = [line.replace(r'\textit', '') for line in caption_lines]
    caption_lines = [line.replace(r'\textbf', '') for line in caption_lines]
    #remove \caption from the lines
    caption_lines = [line.replace(r'\caption{', '') for line in caption_lines]
    #keep only what is before }
    caption_lines = [line.rsplit('}', 1)[0] for line in caption_lines]
    #leave only numbers and letters in the lines
    caption_lines = [re.sub(r'[^a-zA-Z0-9]+', '', line) for line in caption_lines]
    #find the caption that starts with text_in_page[0]
    caption_line = ''
    text_index = 0
    try :
        beginning_of_caption = text_in_page[text_index].split(':')[1]
    except IndexError:
        print("not a real caption")
        return text_in_page[0], 0

    while len(caption_lines) >1:
        for index, line in enumerate(caption_lines):
            clean_beginning_of_caption = re.sub(r'[^a-zA-Z0-9]+', '', beginning_of_caption)
            if clean_beginning_of_caption in line:
                continue
            else:
                caption_lines[index] = ''
        #remove the empty lines
        caption_lines = list(filter(None, caption_lines))
        text_index+=1
        beginning_of_caption = text_in_page[text_index]
    if (len(caption_lines) == 0):
        raise Exception("No caption found")
    caption_line = caption_lines[0]

    clean_caption_line = re.sub(r'[^a-zA-Z0-9]+', '', caption_line)
    clean_caption_line = clean_caption_line.lower()
    for index, line in enumerate(text_in_page):
        #remove the regex Table\d: from clean_line
        if caption_type == 'Table':
            clean_line = re.sub(r'Table\d*:', '', line)
        if caption_type == 'Figure':
            clean_line = re.sub(r'Figure\s*\d*:', '', line)
        clean_line = re.sub(r'[^a-zA-Z0-9]+', '', clean_line)
        clean_line = clean_line.lower()
        
        #edge cases
        clean_caption_line = clean_caption_line.replace('cdot', '')
        clean_caption_line = clean_caption_line.replace('phi', '')
        
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
                    # index_in_latex = 0
                    for index_in_latex, line in enumerate(lines):
                        if begin_pattern in line and index_counter == int(index):
                            beginning_index = index_in_latex
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
                            rows_list[beginning_index] = line
                            beginning_index+=1
                       
    return rows_list

lidor = convert_Latex_to_rows_list("code/greedy_from_machine/lidor_test/AAAI_changed.tex", "code/greedy_from_machine/lidor_test/AAAI_changed.pdf")
print(lidor)



