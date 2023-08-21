
**Main File**:
1. generation_of_file.py - creates a paper given specific combination of objects. Creates 3 variants of the file, while making sure
there are two pages and on the second page there are few objects.
Calls the feature extraction process for each variant.

**Objects tex files**:

1. objects_generation - creates a dictionary of tex objects' IDs (key) and their Tex code
2. get_dictionary - getDict function returns a dictionary of tex objects' IDs (key) and their probable height (value).


**Dealing with PDFs**:

1. pdf_miner_new & pdf_miner_new_checking_length - returns textual objects from PDF
2. pdf_extraction - returns tables & figures from PDF
3. read_single_file - returns a "workable" combination of the above two returned values, for comparison with the tex file.


***Feature Extraction Process***:

**Tex Parsing Files:**


We didn't do much documentation of this part. This parsing is specific to our needs, and is not a general parser for latex documents:
1. latex elements must be separated by \n.
2. Only latex elements types are included.
3. You should remove comments and replace private commands in their corresponding tex.

There are 3 python files creating the parsing and tokenizing of the latex files. 
No need to change this part, unless you want to analyze more latex elements, or to change the design of aaai.

The main file is main_parsing, with the function "parse". This file calls other two files.
1. Connector - recursive file to build tree
2. latex_parsing
3. main_parsing - main file. The function 'receive_lines_version_1' creates a list of tex object, with attributes.


**Comparison Tex to PDF:**
1. combining_tex_by_content_comparison_functions
2. mapping_latex_to_pdf : a wrapper calls the tex parsing, pdf elements analysis, and combining_tex_by_contnet_comparison_functions

**Feature Extraction**:
1. features_extraction_single_paper - using this file, given a pdf and a latex doc, we can preform feature extraction.
                                        output: csv with the doc name and his features.



***Tex Compilation Instructions***:

Use 'tectonic' package for compiling the file. Use conda-forge in order to install the package.
Command to insert in cmd: 'tectonic -X compile path_for_tex_file'
While the path_for_tex_file will be where the pdf will be compiled to (just with .pdf ending instead of .tex).
The compiler is xelatex. Note there is different from the default compiler in overleaf.

