import re

def has_aaai_format(tex_file_path):
    # docomantion of the function:
    # This function checks if the .tex file has the format of AAAI conference.
    # The function gets the path of the .tex file as an argument.
    # The function returns True if the .tex file has the format of AAAI conference, otherwise it returns False.
    try:
        with open(tex_file_path, 'r', encoding="utf-8") as tex_file:
            for line in tex_file:
                if find_aaai_format(line):
                    return True
    except Exception as e:
        print(f"An error occurred: {e}")
    return False

# put Vspace in comment function:
def comment_vspace_lines(tex_file_path):
    # docomantion of the function:
    # the function gets the path of the .tex file as an argument.
    # the function find a \vspace{...} in the .tex file and delete this command, and add '%removedVspace' in the end of the line.
    try:
        updated_lines = []

        with open(tex_file_path, 'r', encoding="utf-8") as tex_file:
            
            for line in tex_file:
                # check using regex if the line conatins '\vspace' and after {}
                indices= find_vspace_range(line)
                if indices:
                    # if so, delete content in the line between the indices and add '%'
                    updated_lines.append(line[:indices[0]] + line[indices[1]+1:].rstrip()+ '%removedVspace')
                else:
                    updated_lines.append(line.rstrip())

        with open(tex_file_path, 'w', encoding="utf-8") as tex_file:
            tex_file.write('\n'.join(updated_lines))
            
        
    except Exception as e:
        print(f"An error occurred: {e}")


def find_vspace_range(line):
    pattern = r'\\vspace\{.*?\}'
    match = re.search(pattern, line)
    
    if match:
        return match.start(), match.end()

    else:
        return None
    
def find_aaai_format(line):
    pattern = r'\\usepackage.*\{aaai\d*\}'
    match = re.search(pattern, line)
    return True if match else False


def remove_pdfinfo_commands(tex_file_path):
    with open(tex_file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    new_lines = []
    skip_next_brace = False

    for line in lines:
        if '\\pdfinfo{' in line:
            skip_next_brace = True
            continue

        if skip_next_brace:
            if '}' in line:
                skip_next_brace = False
            continue

        new_lines.append(line)

    with open(tex_file_path, 'w', encoding="utf-8") as file:
        file.writelines(new_lines)
    
def remove_small_command(tex_file_path):
    with open(tex_file_path, 'r', encoding='utf-8') as input_file:
        latex_content = input_file.read()

    # Define a regular expression pattern to match \small commands
    pattern = r'\\small\b'

    # Use re.sub to replace \small commands with commented versions
    modified_content = re.sub(pattern, r'% \g<0>', latex_content)

    # Save the modified content to the output file
    with open(tex_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)


def remove_new_page_command(tex_file_path):
    with open(tex_file_path, 'r', encoding='utf-8') as input_file:
        latex_content = input_file.read()

    # Define a regular expression pattern to match \newpage commands
    pattern = r'\\newpage\b'

    # Use re.sub to replace \newpage commands with commented versions
    modified_content = re.sub(pattern, r'% \g<0>', latex_content)

    with open(tex_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)
