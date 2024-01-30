from dir_findTEX import find_tex_file
from Vspace_delete import *
import os
from addRows import *
import shutil
import time
import func_timeout


def create(sub_path, destination_path):
    create_new_pdf(sub_path)
    move_changed_pdfs(sub_path, destination_path)
    
    
# loop throgh the directory of the papers directories, and activete the function create_new_pdf for each directory
def loop_through_directories(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for directory in dirs:
            subdirectory_path = os.path.join(root, directory)   
            print("now in directory: --------------------------------: " ,subdirectory_path)
            
            try:
                func_timeout.func_timeout(timeout=120,func=create, args=[subdirectory_path,"new_papers_creation/results"])
            
            except func_timeout.exceptions.FunctionTimedOut:
                # Handle timeout exception by logging and continue to the next iteration
                print("Timeout occurred while executing create.")
                shutil.move(subdirectory_path, "new_papers_creation/failed_directories")
                pass   
            except Exception as e:
                print(f"An error occurred: {e}, the directory : {subdirectory_path} was not created")
                # move the directory to failed directory
                shutil.move(subdirectory_path, "new_papers_creation/failed_directories")
                pass
    

def create_new_pdf(directory_path):
    tex_file_path = find_tex_file(directory_path)
    if tex_file_path != None :
        if has_aaai_format(tex_file_path):
            # create a new file with the same name as the original file, but with the suffix '_changed' and the same content as the original file.
            new_file_name = os.path.splitext(os.path.basename(tex_file_path))[0] + "_changed.tex"
            new_file_path = os.path.join(directory_path, new_file_name)
            with open(tex_file_path, 'r', encoding="utf-8") as original_file:
                content = original_file.read()
            with open(new_file_path, 'w', encoding="utf-8") as new_file:
                new_file.write(content)        
            # comment the vspace lines (delete the vspace command and add a comment sign before it)
            remove_pdfinfo_commands(new_file_path)
            comment_vspace_lines(new_file_path)
            remove_new_page_command(new_file_path)
            # remove_small_command(new_file_path)
            # add 3 lines to the last page
            create_extra_line_page(new_file_path)
            

            
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


import os
import tarfile
import shutil
import glob

# def rename_directories(base_directory):
#     for folder in os.listdir(base_directory):
#         folder_path = os.path.join(base_directory, folder)

#         if os.path.isdir(folder_path):
#             # Look for a LaTeX file with "_changed" in its name
#             latex_files = glob.glob(os.path.join(folder_path, '*_changed.tex'))

#             if latex_files:
#                 latex_path = latex_files[0]
#                 paper_title = extract_title_from_latex(latex_path)

#                 if paper_title:
#                     # Extract the first word of the title
#                     first_word = paper_title.split()[0]

#                     # Rename the directory
#                     new_folder_name = os.path.join(base_directory, first_word)
#                     os.rename(folder_path, new_folder_name)
#                     print(f'Renamed directory: {folder} to {first_word}')
#                 else:
#                     print(f'Error: Unable to extract title from LaTeX in {folder}')
def extract_tar(tar_file, extract_path):
    with tarfile.open(tar_file, 'r') as tar:
        tar.extractall(extract_path)

# def run_custom_function(directory_path):
#     # Replace this with your custom function
#     print(f"Running custom function on directory: {directory_path}")

def process_tar_files(input_directory, output_directory):
        # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Get a list of all files with the pattern "xxxx.xxxxx" in the input directory
    tar_files = glob.glob(os.path.join(input_directory, '[0-9]*.[0-9]*'))

    # Set to keep track of encountered base names
    # encountered_base_names = set()
    # encountered_base_names.add("2312")
    index=2
    for tar_file in tar_files:
        # Create a directory with a unique name
        
        
        directory_name = f"newdir_{index}"
        index+=1
        # tex_file_path = find_tex_file(tar_file)
        # if tex_file_path != None :
        # base_name, extension = os.path.splitext(os.path.basename(tar_file))
        
        # # Check if the base name has been encountered before
        # if base_name in encountered_base_names:
        #     index = 1
        #     while f"{base_name}_{index}" in encountered_base_names:
        #         index += 1
        #     directory_name = f"{base_name}_{index}"
        # else:
        #     directory_name = base_name

        # encountered_base_names.add(directory_name)

        extract_path = os.path.join(output_directory, directory_name)
        os.makedirs(extract_path, exist_ok=True)

        # Extract tar file into the created directory
        extract_tar(tar_file, extract_path)

        # Delete the tar file after extraction
        os.remove(tar_file)

    # Run the custom function on the output directory
    # rename_directories(output_directory)
    
    loop_through_directories(output_directory)

if __name__ == "__main__":
    # List of gzipped tar files
    
    input_directory = "new_papers_creation\\tar_files"
    # Output directory where all the extracted directories will be placed
    output_directory = "new_papers_creation\\All_Directories"

    # Process the tar files and run the custom function
    # process_tar_files(input_directory, output_directory)
    loop_through_directories(output_directory)







    

# loop_through_directories("new_papers_creation\\All_Directories")

# import os
# import glob
# import re

# def extract_title_from_latex(latex_path):
#     title_pattern = re.compile(r'\\title{([^}]*)}')

#     with open(latex_path, 'r', encoding='utf-8') as file:
#         content = file.read()
#         match = title_pattern.search(content)
#         if match:
#             title = match.group(1).strip().replace(':', '')
#             return title
#         else:
#             return None

# def rename_directories(base_directory):
#     for folder in os.listdir(base_directory):
#         folder_path = os.path.join(base_directory, folder)

#         if os.path.isdir(folder_path):
#             # Look for a LaTeX file with "_changed" in its name
#             latex_files = glob.glob(os.path.join(folder_path, '*_changed.tex'))

#             if latex_files:
#                 latex_path = latex_files[0]
#                 paper_title = extract_title_from_latex(latex_path)

#                 if paper_title:
#                     # Extract the first word of the title
#                     first_word = paper_title.split()[0]

#                     # Rename the directory
#                     new_folder_name = os.path.join(base_directory, first_word)
#                     os.rename(folder_path, new_folder_name)
#                     print(f'Renamed directory: {folder} to {first_word}')
#                 else:
#                     print(f'Error: Unable to extract title from LaTeX in {folder}')

                
                
                
# rename_directories("new_papers_creation\\results")
# create_new_pdf("new_papers_creation\\AAAI 2016")
# create_new_pdf('new_papers_creation\\aaai_docs')
# str = "hello yosi my name is or"
# clean_str = "helloyosimynameisor"
# substring = "my name"
# clean_substring = "myname"

# # Find the index of the substring in the cleaned string
# clean_index = clean_str.find(clean_substring)

# if clean_index != -1:
#     # Calculate the corresponding index in the original string
#     original_index = clean_index + str[:clean_index + 1 ].count(" ")
#     print(f"The substring '{substring}' was found at index {original_index} in the original string.")
# else:
#     print(f"The substring '{substring}' was not found in the original string.")