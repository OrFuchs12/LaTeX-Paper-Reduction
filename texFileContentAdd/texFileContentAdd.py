
# because some tex files include another tex files, we should probably use this function in a while loop
# untill it returns false, thats when it dosent find a match of an include command.
import os
import re

def replace_input_include_with_content(directory, main_file):
    main_file_path = os.path.join(directory, main_file)

    if not os.path.exists(main_file_path):
        print(f"Main file '{main_file}' not found in directory '{directory}'.")
        return False

    with open(main_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Use regular expressions to find and replace \input and \include commands
    content, replaced = replace_commands(directory, content)

    if not replaced:
        print("No \\input or \\include commands found in the code.")
        return False

    # Create the output file with "_include" suffix
    output_file = os.path.join(directory, os.path.splitext(main_file)[0] + "_include.tex")

    # Write the modified content to the new output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Replacement completed. The modified content has been saved to '{os.path.splitext(main_file)[0] + '_include.tex'}'.")
    return True

def replace_commands(directory, content):
    replaced = False

    # Use regular expressions to find and replace \input and \include commands
    content = re.sub(r'\\input{([^}]+)}', lambda match: replace_input(directory, match.group(1)), content)
    content = re.sub(r'\\include{([^}]+)}', lambda match: replace_input(directory, match.group(1)), content)

    if re.search(r'\\input{([^}]+)}|\\include{([^}]+)}', content):
        replaced = True

    return content, replaced

def replace_input(directory, referenced_file):
    referenced_file_path = os.path.join(directory, referenced_file)

    if not os.path.exists(referenced_file_path):
        print(f"Referenced file '{referenced_file}' not found in directory '{directory}'.")
        return ""

    with open(referenced_file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main(directory, main_file): 
    print(replace_input_include_with_content(directory, main_file))

main('texFileContentAdd/Commonsense_AAAI21','main_changed.tex')