from dir_findTEX import find_tex_file
from Vspace_delete import has_aaai_format
from Vspace_delete import comment_vspace_lines
import os

# directory_path = "/Users/amitvitkovsky/Downloads/AAAI-12"
# directory_path = "/Users/amitvitkovsky/Downloads/AAAI13-QDEC"
directory_path = "new_papers_creation\AAAI13-QDEC"
tex_file_path = find_tex_file(directory_path)
if tex_file_path != None :
    if has_aaai_format(tex_file_path):
        # create a new file with the same name as the original file, but with the suffix '_changed' and the same content as the original file.
        new_file_name = os.path.splitext(os.path.basename(tex_file_path))[0] + "_changed.tex"
        new_file_path = os.path.join(directory_path, new_file_name)

        with open(tex_file_path, 'r') as original_file:
            content = original_file.read()

        with open(new_file_path, 'w') as new_file:
            new_file.write(content)

        print(f"New file created: {new_file_path}")
        print(f"tex_file_path: {tex_file_path}")
        print(f"has_aaai_format: {has_aaai_format(tex_file_path)}")
        comment_vspace_lines(new_file_path)
        

        
        # comment_vspace_lines(tex_file_path)

    else:
        print("No aaai format found in the .tex file")
else:
    print("No .tex file found")


