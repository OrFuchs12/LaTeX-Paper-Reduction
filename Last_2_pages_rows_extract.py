import pdfplumber
import re
import pdb



NUMBER_OF_LAST_PAGES = 3

def find_first_Row_in_last_page(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        page = pdf.pages[-NUMBER_OF_LAST_PAGES]
        # Define the x-coordinate ranges for each columnc

        # Extract text from the left column
        left_column = (0, 0, page.width / 2, page.height)

        # Extract text only from the left column
        text = page.within_bbox(left_column).extract_text()
        return text.split('\n')[0]

   
def convert_Latex_to_rows_list(latex_path,pdf_path):
    # list of rows to extract from the latex file
    rows_list = []
    # the first row in the page we want to start the extraction from
    first_row_to_begin = find_first_Row_in_last_page(pdf_path)
    # clean the line to make it easier to compare
    clean_line = re.sub(r'[^a-zA-Z]+', '', first_row_to_begin)
    # search the line in  the latex file
    try:
        with open(latex_path, 'r') as tex_file:
            file_content = tex_file.read()
        lines = file_content.strip().split('\n')
        # count the number of lines before the line we want to start the extraction from
        lines_before_the_line = 0
        # flag to know if we found the line we want to start the extraction from
        found_start = False
        # flag to know if we found the line we want to end the extraction from
        found_end = False
        for line in lines:
            # clean the line to make it easier to compare
            pattern = r'\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\{[^\}]*\})?'

            # Use re.sub to replace LaTeX commands with an empty string
            clean_linePDF = re.sub(pattern, '', line)
            clean_latex_line_to_compare = re.sub(r'[^a-zA-Z]+', '', clean_linePDF)
            if not found_start:
                if clean_line in clean_latex_line_to_compare:
                    print("found the line")
                    print(clean_line)
                    print(clean_latex_line_to_compare)
                    rows_list.append(line)
                    found_start = True
                else:
                    lines_before_the_line += 1
                    rows_list.append('\n')
            elif found_start and not found_end:
                if line.startswith("\\end{document}"):
                    found_end = True
                    break
                else:
                    if(line == ''):
                        rows_list.append('\n')
                    else:
                        rows_list.append(line)
        return rows_list
                    
                

    except Exception as e:
            print(f"An error occurred: {e}")


# print(find_first_Row_in_last_page('code/greedy_from_machine/temp/Keller_changed.pdf'))
list= convert_Latex_to_rows_list('test_for_last_page_files/samd_changed.tex','test_for_last_page_files/samd_changed.pdf')      
print(list)

