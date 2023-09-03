#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import fileinput
import os
import re

def get_args():
    if len( sys.argv ) != 4:
        raise IOError("Must get: 1. Main tex input; 2. Sections output; 3. Template of the paper output;")
        
    file_main_tex_input_path    = sys.argv[1]
    print( "argument: file_main_tex_input_path  : " + file_main_tex_input_path )

    file_sections_output_path   = sys.argv[2]
    print( "argument: file_sections_output_path : " + file_sections_output_path )

    file_template_output_path   = sys.argv[3]
    print( "argument: file_template_output_path : " + file_template_output_path)
    
    if os.path.exists(file_main_tex_input_path):
        print( "found: file_main_tex_input_path     : " + file_main_tex_input_path )
        file_main_tex_input = open( file_main_tex_input_path, 'rt' )
    else:
        raise ImportError( "file_main_tex_input_path file does not exists: " + file_main_tex_input_path )

    file_sections_output = open(file_sections_output_path, 'wt')
    file_template_output = open(file_template_output_path, 'wt')

    return file_main_tex_input, file_sections_output, file_template_output


def main():
    if sys.version_info[0] < 3: # Python 2 needs utf-8
        reload(sys)
        sys.setdefaultencoding('utf-8')

    file_main_tex_input, file_sections_output, file_template_output = get_args()

    file_main_tex_input_text: str = file_main_tex_input.read()

    subsection_list = [ "PTAs", "A Formal Semantics for PLPs", "Control Graphs", "Control Graph Verifier" ]

    for subsection_name in subsection_list:
        print(" - " + subsection_name)

        section_content = re.search("\\\\subsection\{" + subsection_name + "\}" +
                                    "(.*)" +
                                    "%endsection\{" + subsection_name + "\}",
                                    file_main_tex_input_text, re.MULTILINE | re.DOTALL)

        if ( None != section_content  ):
            file_sections_output.write("\sectionStart{" + subsection_name + "}\n" +
                                       section_content[1] +
                                       "\n\sectionEnd{" + subsection_name + "}\n")

            file_main_tex_input_text = file_main_tex_input_text.replace( section_content[0],
                                                                         "\\subsection{" + subsection_name + "}" )

    file_template_output.write(file_main_tex_input_text)
    
    file_main_tex_input.close()
    file_sections_output.close()
    file_template_output.close()
    print("Done")
    
    
main()

# Run example:
# ./split_tex_to_sections_and_template.py /home/alexds9/Thesis/paper_main_tex_20180512/main.tex /home/alexds9/Thesis/paper_main_tex_20180512/splitted_sections.txt /home/alexds9/Thesis/paper_main_tex_20180512/splitted_template.tex