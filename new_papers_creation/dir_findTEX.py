import os

def find_tex_file(directory_path):
    tex_file_path = None
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".tex"):
                tex_file_path = os.path.join(root, file)
                break  # Break the loop once the first .tex file is found
        if tex_file_path:
            break  # No need to continue searching if the .tex file is found
    
    return tex_file_path


