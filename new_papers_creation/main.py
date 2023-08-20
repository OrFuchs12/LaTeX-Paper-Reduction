from dir_findTEX import find_tex_file
from Vspace_delete import has_aaai_format
from Vspace_delete import comment_vspace_lines

# directory_path = "/Users/amitvitkovsky/Downloads/AAAI-12"
directory_path = "/Users/amitvitkovsky/Downloads/AAAI13-QDEC"
tex_file_path = find_tex_file(directory_path)
if tex_file_path != None :
    if has_aaai_format(tex_file_path):
        print(f"tex_file_path: {tex_file_path}")
        print(f"has_aaai_format: {has_aaai_format(tex_file_path)}")
        comment_vspace_lines(tex_file_path)

    else:
        print("No aaai format found in the .tex file")
else:
    print("No .tex file found")


