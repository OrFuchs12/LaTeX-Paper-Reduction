import pdfplumber
import re
import pdb
import PyPDF2


NUMBER_OF_LAST_PAGES = 2

def find_first_row_in_last_page(pdf_file_path):
    # Open the PDF file and extract the last page
    with pdfplumber.open(pdf_file_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]

        # Define the x-coordinate ranges for each column
        left_column = (0, 0, page.width / 2, page.height)

        # Extract text only from the left column
        text = page.within_bbox(left_column).extract_text()

        # extract the coordinates of the first obejct in the page, text, image or table
        
        # Find the first row of text that is not inside a table
        tables_coordinates = get_tables_coordinates(pdf_file_path, -NUMBER_OF_LAST_PAGES)
        if tables_coordinates:
            first_table = tables_coordinates[0]
            rows = text.split('\n')
            for index, row in enumerate(rows):
                # Calculate the bounding box for the current row
                # ########### this part is not working well, need to fix it #############
                # the problem is i cant get the coordinates of the first row in the page
                # if we can get the coordinates of the first row in the page we can check if the row is inside the table
                row_bbox = {
                    "x0": left_column[0],
                    "y0": left_column[1] + index * 10,  # Adjust the '10' based on font size and spacing
                    "x1": left_column[2],
                    "y1": left_column[1] + (index + 1) * 10  # Adjust as needed
                }
                print(row_bbox)
                
                if not is_row_inside_table(row_bbox, first_table):
                    return row
        else:
            return text.split('\n')[0]
            

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


def is_row_inside_table(row, table):
    """
    Returns True if the specified row is inside the specified table, False otherwise.
    """
    row_x1, _, row_x2, row_y = row.values()
    table_x1, _, table_x2, table_y = table
    return table_x1 <= row_x1 <= row_x2 <= table_x2 and table_y <= row_y



def convert_Latex_to_rows_list(latex_path,pdf_path):
    # list of rows to extract from the latex file
    rows_list = []
    # the first row in the page we want to start the extraction from
    first_row_to_begin = find_first_Row_in_last_page(pdf_path)
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
                    
                

    except Exception as e:
            print(f"An error occurred: {e}")

                    
                




        


print(get_tables_coordinates('test_for_last_page_files/samd_changed.pdf', - NUMBER_OF_LAST_PAGES))
print(find_first_row_in_last_page('test_for_last_page_files/samd_changed.pdf'))
# list= convert_Latex_to_rows_list('test_for_last_page_files/samd_changed.tex','test_for_last_page_files/samd_changed.pdf')      
# print(list)