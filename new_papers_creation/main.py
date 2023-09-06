from dir_findTEX import find_tex_file
from Vspace_delete import *
import os
from addRows import *
import shutil




# loop throgh the directory of the papers directories, and activete the function create_new_pdf for each directory
def loop_through_directories(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for directory in dirs:
            subdirectory_path = os.path.join(root, directory)   
            print("now in directory: --------------------------------: " ,subdirectory_path)
            try:
                create_new_pdf(subdirectory_path)
                move_changed_pdfs(subdirectory_path, "new_papers_creation/results")
            except Exception as e:
                print(f"An error occurred: {e}, the directory : {subdirectory_path} was not created")
                # move the directory to failed directory
                shutil.move(subdirectory_path, "new_papers_creation/failed_directories")
            


def create_new_pdf(directory_path):
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
            # comment the vspace lines (delete the vspace command and add a comment sign before it)
            remove_pdfinfo_commands(new_file_path)
            comment_vspace_lines(new_file_path)
            remove_small_command(new_file_path)
            # add 3 lines to the last page
            create_3Lines_page(new_file_path)
            

            
            # comment_vspace_lines(tex_file_path)

        else:
            print("No aaai format found in the .tex file")
            # raise Exception("No aaai format found in the .tex file")
            raise Exception("No aaai format found in the .tex file")
    else:
        print("No .tex file found")
        raise Exception("No .tex file found")

def move_changed_pdfs(directory_path, destination_path):
    # move directory to destination path
    shutil.move(directory_path, destination_path)

# loop_through_directories("new_papers_creation/All_Directories")
create_new_pdf("new_papers_creation/AAAI-12")

