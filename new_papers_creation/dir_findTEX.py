import os

def find_tex_file(directory_path):
    print(directory_path)
    tex_files = [file for file in os.listdir(directory_path) if file.endswith('.tex')]

    if len(tex_files) == 1:
        return os.path.join(directory_path, tex_files[0])

    main_tex_candidates = []
    for tex_file in tex_files:
        with open(os.path.join(directory_path, tex_file), 'r', encoding="utf-8") as f:
            content = f.read()
            # file dont end with _changed.tex
            if '\\begin{document}' in content and not tex_file.endswith('_changed.tex') :
                main_tex_candidates.append(tex_file)

    if len(main_tex_candidates) == 1:
        return os.path.join(directory_path, main_tex_candidates[0])
    # if main in the name of the file
    elif len(main_tex_candidates) > 1:
        for tex_file in main_tex_candidates:
            if 'main' in tex_file:
                return os.path.join(directory_path, tex_file)
    elif 'main.tex' in tex_files:
        return os.path.join(directory_path, 'main.tex')
    
    else:
        return None
    



