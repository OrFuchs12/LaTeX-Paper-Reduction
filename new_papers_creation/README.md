addRows : 
    1. we add \clearpage to the latex file right before the \bibliography using "add_clearpage_before_bibliography"
    2. we compile the latex file with the clear page using "compile_latex_to_pdf"
    3. while the number of lines is not 3 we:
       1. find the page number that is right before the bibliography using "find_page_number_before_bibliography" (IMPORTANT: the page number starts from 0)
       2. we count the lines in the page (IMPORTANT: use pdfplumber and not fitz) using "count_lines_in_page"
       3. according to number of lines we will add or remove lines
          1. if the number is 3 exit
          2. if we have more than 66 lines then the right column has text and we would like to add until we have 3 lines in a new page, in order to compile as less as possible we will add lines 132-number of lines because 132 is the number of lines in a full pdf page
          3. if we have less than 3 lines we need to add one line 
          4. if we have less than 66 than we need to remove the number of lines -3 
       4. compile again to check changes 

TODO: 
1. fix add_to_latex and implement remove_from_latex
2. check with all papers 


edge cases for page number to check: 
    1. page number 
    2. footnotes 