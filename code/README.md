
**Main File**:
1. main.py - receives directory of tex&pdf files and their feature extraction' csv file. 
For each such document, by calling the script Using_operators.py, various tex files are created (each file is created by activation of an operator).
In the main.py we will compile each variant and calculate the height of elements on the 2nd page (if exists).
The labels are added to the current row in the df.


**Dealing with PDFs**:

Same as in documents generation. Explained in documents generation' README file.

***Feature Extraction Process***:
1. feature_extracion_single_paper.py - features_extraction_single_paper - using this file, given a pdf and a latex doc, we can preform feature extraction. output: csv with the doc name and his features.

**Tex Parsing Files:**

This is a bit different code from the parsing in documents generation. The difference is in main_parsing function.
The main file is main_parsing, with the function "parse2". This file calls other two files.
1. Connector - recursive file to build tree
2. latex_parsing
3. main_parsing - main file. The function 'receive_lines_version_1' creates a list of tex object, with attributes.


***Performing Operators***:

using_operators.py - this is a function that main.py calls to perform the operators. 

The first half of the file is the way we perform each operator and then saving the results in the operator respective dict. 

In the second half of the file we take each change that was done the first half (when performing each operator) and actually putting the change (for example, for the vspace operator, in the first half we generated all the values that the tag should get and in the second half we actually created a new .tex file with the addition of the vspace tag with the right value that we got in the first half of the file)

They way we run the first half of the file is that we go through all the objects in the doc, and then if we identify a specific object we will perform all the available operators we can perform on this specific operator, and then we will save what we got.

After finishing with the using_operator.py we return a list of .tex files that we created and now we need to compile in order to get where the new doc ends (to get the label, if we managed to reduce the length or no)