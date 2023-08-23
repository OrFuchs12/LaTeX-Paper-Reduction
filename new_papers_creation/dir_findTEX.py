import os

def find_tex_file(directory_path):
    tex_file_path = None
    
    for root, dirs, files in os.walk(directory_path):
        tex_files = [file for file in os.listdir(directory_path) if file.endswith(".tex")]
        if len(tex_files) > 1:
            for file in tex_files:
                # if file has the name main.tex, then return it
                if file == "main.tex":
                    tex_file_path = os.path.join(root, file)
                    break
                # else, open the file and search for the string "\begin{document}"
                else:
                    with open(os.path.join(root, file), 'r') as f:
                        file_content = f.read()
                    if "\\begin{document}" in file_content:
                        tex_file_path = os.path.join(root, file)
                        break
                
            if tex_file_path:
                break  # No need to continue searching if the .tex file is found
        # if there is only one .tex file, return it
        else:
            tex_file_path = os.path.join(root, tex_files[0])
            break
    
    return tex_file_path


