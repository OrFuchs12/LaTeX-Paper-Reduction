

def has_aaai_format(tex_file_path):
    # docomantion of the function:
    # This function checks if the .tex file has the format of AAAI conference.
    # The function gets the path of the .tex file as an argument.
    # The function returns True if the .tex file has the format of AAAI conference, otherwise it returns False.
    try:
        with open(tex_file_path, 'r') as tex_file:
            for line in tex_file:
                if 'usepackage{aaai}' in line:
                    return True
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return False

# put Vspace in comment function:
def comment_vspace_lines(tex_file_path):
    try:
        updated_lines = []

        with open(tex_file_path, 'r') as tex_file:
            for line in tex_file:
                if 'vspace' in line:
                    updated_lines.append('% ' + line.rstrip())
                else:
                    updated_lines.append(line.rstrip())

        with open(tex_file_path, 'w') as tex_file:
            tex_file.write('\n'.join(updated_lines))
            
        print("vspace lines commented successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

