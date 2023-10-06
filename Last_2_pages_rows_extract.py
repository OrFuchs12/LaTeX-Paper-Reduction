import pdfplumber
import re
import pdb
import PyPDF2


NUMBER_OF_LAST_PAGES = 2

def find_first_row_in_last_page(pdf_file_path, latex_path):
    # Open the PDF file and extract the last page
    with pdfplumber.open(pdf_file_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]

        # Define the x-coordinate ranges for each column
        left_column = (0, 0, page.width / 2, page.height)

        # Extract text only from the left column
        text = page.within_bbox(left_column).extract_text()
        #TODO: check for tbale works, need to add image and algorithm... 
        text, is_start_table = check_if_text_inside_table(pdf_file_path, text.split('\n'), latex_path)
        if is_start_table==False:
            #image
            text, is_start_image = check_if_text_inside_image(pdf_file_path, text, latex_path)
        #add a check if the table lines are in index 0 and only then delete 
        #add indication about figures/tables/algorithms
        return text[0]

            

def get_tables_coordinates(pdf_path, page_number):
    """
    Returns a list of the coordinates of all tables on the specified page of the PDF file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]

        # Get the tables coordinates in the page using pdfplumber
        tables = page.find_tables()

        # Get the coordinates of the tables in the wanted page
        tables_coordinates = [table.bbox for table in tables]

        return tables_coordinates


# def is_row_inside_table(row, table):
#     """
#     Returns True if the specified row is inside the specified table, False otherwise.
#     """
#     row_x1, _, row_x2, row_y = row.values()
#     table_x1, _, table_x2, table_y = table
#     return table_x1 <= row_x1 <= row_x2 <= table_x2 and table_y <= row_y



def check_if_text_inside_image(pdf_path, text_in_page, latex_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        if text_in_page[0].startswith('Figure'):
                text_in_page = remove_caption(text_in_page, latex_path, 'Figure')
                return text_in_page, True        
        return text_in_page, False
    
    
def convert_Latex_to_rows_list(latex_path,pdf_path):
    # list of rows to extract from the latex file
    rows_list = []
    # the first row in the page we want to start the extraction from
    first_row_to_begin = find_first_row_in_last_page(pdf_path, latex_path)
    print(first_row_to_begin)
    # clean the line to make it easier to compare
    clean_line = re.sub(r'[^a-zA-Z]+', '', first_row_to_begin)
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
            clean_latex_line_to_compare = re.sub(r'[^a-zA-Z]+', '', clean_linePDF)
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

        return rows_list
                    
                
    #check for missing tables and images
    except Exception as e:
            print(f"An error occurred: {e}")

                    
                
def extract_text_from_tables(pdf_path):
    table_settings = {
    "vertical_strategy": "text",
    "horizontal_strategy": "lines"
    }
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        #get the text inside the tables 
        text_in_first_table = page.extract_tables(table_settings)[0]
        return text_in_first_table
    
def check_if_text_inside_table(pdf_path, text_in_page, latex_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        text_in_table = extract_text_from_tables(pdf_path)
        #loop through nested list and remove None values
        text_in_table = [[cell for cell in row if cell is not None] for row in text_in_table]
        #concat all items in a row to one string
        text_in_table = [' '.join(row) for row in text_in_table]
        caption_line = None
        removed_caption = False
        #find the line of the caption of the table
        if text_in_table:
            #search for regex Table\d*: in the text of the page
            for index, line in enumerate(text_in_page):
                if re.search(r'Table\d*:', line):
                    caption_line = index
                    if caption_line == 0:
                        text_in_page = remove_caption(text_in_page, latex_path , 'Table')
                        removed_caption = True
                    break
            #for each line until caption line check if the line is in the table
            is_start_page = False
            for index, line in enumerate(text_in_page):
                if caption_line == None:
                    return text_in_page, is_start_page
                if removed_caption or (not removed_caption and index < caption_line):
                    for row in text_in_table:
                        clean_line = re.sub(r'[^a-zA-Z]+', '', line)
                        clean_row = re.sub(r'[^a-zA-Z]+', '', row)
                        if clean_line in clean_row:
                            if index==0:
                                is_start_page = True
                                text_in_page[index] = ''
                                break
                            elif index > 0 and is_start_page:
                                text_in_page[index] = ''
                                break
                            else:
                                return text_in_page, is_start_page
            #remove empty lines from the list
            text_in_page = list(filter(None, text_in_page))
            if re.search(r'Table\d*:', text_in_page[0]):
                text_in_page = remove_caption(text_in_page, latex_path , 'Table'  )
        return text_in_page, is_start_page

                            
def remove_caption(text_in_page, latex_path , caption_type):
    
    with open(latex_path, 'r', encoding='utf-8' ) as f:
        lines = f.readlines()
    #find all lines that start with \caption
    caption_lines = []
    temp_line= ""
    pattern = r'^\s*\\caption'
    for line in lines:
        if re.match(pattern, line):
            if '}' in line:
                caption_lines.append(line)
            else:
                temp_line= line
                index=lines.index(line)
                while '}' not in lines[index]:
                    index+=1
                    temp_line+=lines[index]
                temp_line+=lines[index]
                caption_lines.append(temp_line)
    #remove \caption from the lines
    caption_lines = [line.replace(r'\caption{', '') for line in caption_lines]
    #keep only what is before }
    caption_lines = [line.split('}')[0] for line in caption_lines]
    #leave only numbers and letters in the lines
    caption_lines = [re.sub(r'[^a-zA-Z]+', '', line) for line in caption_lines]
    #find the caption that starts with text_in_page[0]
    caption_line = ''
    for line in caption_lines:
        beginning_of_caption = text_in_page[0].split(':')[1]
        clean_beginning_of_caption = re.sub(r'[^a-zA-Z]+', '', beginning_of_caption)
        if clean_beginning_of_caption in line:
            caption_line = line
            break
    clean_caption_line = re.sub(r'[^a-zA-Z]+', '', caption_line)
    for index, line in enumerate(text_in_page):
        #remove the regex Table\d: from clean_line
        if caption_type == 'Table':
            clean_line = re.sub(r'Table\d*:', '', line)
        if caption_type == 'Figure':
            clean_line = re.sub(r'Figure\s\d*:', '', line)
        clean_line = re.sub(r'[^a-zA-Z]+', '', clean_line)
        #search for cdot in the clean_caption_line and remove
        clean_caption_line = clean_caption_line.replace('cdot', '')
        if clean_line in clean_caption_line:
            text_in_page[index] = ''
        else:
            break
    #filter out empty lines
    text_in_page = list(filter(None, text_in_page))
    return text_in_page

        


# print(get_tables_coordinates('test_for_last_page_files/samd_changed.pdf', - NUMBER_OF_LAST_PAGES))
# print(find_first_row_in_last_page('test_for_last_page_files/samd_changed.pdf'))
list= convert_Latex_to_rows_list('test_for_last_page_files/aiide2023_changed.tex','test_for_last_page_files/aiide2023_changed.pdf')      
# print(list)

# print(check_if_text_inside_table('test_for_last_page_files/samd_changed.pdf'))
