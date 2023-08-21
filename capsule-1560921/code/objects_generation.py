from objects_for_adding import *

initial_document_path = "initial_doc.tex"
picture_path = '../visualization.png'
documents_path = ""

picture_width_options = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
picture_height_options = [0.1, 0.125, 0.15, 0.175, 0.2]
caption_length_options = [x for x in range(50, 130, 10)]
caption_options = [True]
position_pram_options = ['h', 't', 'b', 'H', '']
algorithm_length_options = [x for x in range(5, 16, 2)]
text_length_options = [x for x in range(100, 600, 10)]
table_rows_options = [3, 4, 5]
table_cols_options = [3, 4, 5]
table_col_width_options = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
enum_length_options = [3, 4, 5]
enum_iterations_num = 3
definition_length_options = [x for x in range(40, 120, 10)]
equations_version_options = [x for x in range(0, 10, 1)]
# sub_figures_options = [2, 3, 4]
# sub_figures_vertical_options = [True, False]
# matrices_rows_options = [3, 4, 5]
# matrices_cols_options = [3, 4, 5]


latex_dict = {}
idx = 0


def __create_object(function, params):
    picture = function(*params)
    return picture


def __create_all_texts():
    global idx
    texts = []
    for text_length in text_length_options:
        latex_dict[idx] = __create_object(text, (text_length, True,))
        texts.append(idx)
        idx += 1
    return texts


def __create_all_section_headers():
    global idx
    sections = []
    latex_dict[idx] = __create_object(section, ())
    sections.append(idx)
    idx += 1
    return sections


def __create_all_sub_section_headers():
    global idx
    subsections = []
    latex_dict[idx] = __create_object(sub_section, ())
    subsections.append(idx)
    idx += 1
    return subsections


def __create_all_paragraphs():
    global idx
    paragraphs = []
    for text_length in text_length_options:
        latex_dict[idx] = __create_object(paragraph, (text_length,))
        paragraphs.append(idx)
        idx += 1
    return paragraphs


def __create_all_pictures():
    global idx
    pictures = [[],[],[],[],[]]

    d = {}
    for w in picture_width_options:
        for h in picture_height_options:
            val = w / h
            d[val] = (w, h)

    for key, value in d.items():
        for label_length in caption_length_options:
            for param in position_pram_options:
                for cap in caption_options:
                    latex_dict[idx] = __create_object(figure,
                                                      (picture_path, value[0], value[1], label_length, cap, param,))
                    if param=="":
                        pictures[0].append(idx)
                    elif param=="h":
                        pictures[1].append(idx)
                    elif param=="H":
                        pictures[2].append(idx)
                    elif param=="t":
                        pictures[3].append(idx)
                    elif param=="b":
                        pictures[4].append(idx)
                    #pictures.append(idx)
                    idx += 1
    return pictures


def __create_tables():
    global idx
    tables = [[],[],[],[],[]]
    for n_rows in table_rows_options:
        for n_cols in table_cols_options:
            for col_width in table_col_width_options:
                for label in caption_length_options:
                    for cap in caption_options:
                        for param in position_pram_options:
                            latex_dict[idx] = __create_object(table, (n_rows, n_cols, col_width, label, cap, param,))

                            if param == "":
                                tables[0].append(idx)
                            elif param == "h":
                                tables[1].append(idx)
                            elif param == "H":
                                tables[2].append(idx)
                            elif param == "t":
                                tables[3].append(idx)
                            elif param == "b":
                                tables[4].append(idx)
                            #tables.append(idx)
                            idx += 1
    return tables


def __create_algorithms():
    global idx
    algorithms = [[],[],[],[],[]]
    for len in algorithm_length_options:
        for param in position_pram_options:
            latex_dict[idx] = __create_object(algorithm, (len, param,))
            #algorithms.append(idx)
            if param == "":
                algorithms[0].append(idx)
            elif param == "h":
                algorithms[1].append(idx)
            elif param == "H":
                algorithms[2].append(idx)
            elif param == "t":
                algorithms[3].append(idx)
            elif param == "b":
                algorithms[4].append(idx)
            idx += 1
    return algorithms


def __create_equations():
    global idx
    equations = []
    for i in equations_version_options:
        latex_dict[idx] = __create_object(equation, (i,))
        equations.append(idx)
        idx += 1
    return equations


def __create_enums():
    global idx
    enums = []
    for i in range(enum_iterations_num):
        for len in enum_length_options:
            latex_dict[idx] = __create_object(enum, (len,))
            enums.append(idx)
            idx += 1
    return enums


def __create_definitions():
    global idx
    definitions = []
    for i in definition_length_options:
        latex_dict[idx] = __create_object(definition, (i,))
        definitions.append(idx)
        idx += 1
    return definitions


def getDict():
    global idx
    idx=0
    texts = __create_all_texts()
    sections = __create_all_section_headers()
    subsections = __create_all_sub_section_headers()
    paragraphs = __create_all_paragraphs()
    pictures = __create_all_pictures()
    tables = __create_tables()
    algorithms = __create_algorithms()
    equations = __create_equations()
    enums = __create_enums()
    definitions = __create_definitions()
    return latex_dict


def getAllLists():
    """
    :return: list of all possible tex elements
    """
    global idx
    idx=0
    newlst = [__create_all_texts(), __create_all_section_headers(), __create_all_sub_section_headers(),
              __create_all_paragraphs(),
              __create_all_pictures(), __create_tables(), __create_algorithms(), __create_equations(), __create_enums(),
              __create_definitions()]

    return newlst



