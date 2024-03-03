import os
import pickle
import subprocess
import time
import shutil
from catboost import CatBoostRegressor
import pdfplumber
import perry
import perry2
import PyPDF2
import sys
from itertools import islice
import copy
import re
import feature_extraction
import features_single
import pandas as pd
import time
import xgboost as xg
from Last_2_pages_rows_extract import convert_Latex_to_rows_list
from handle_full_paper import copy_last_pages
from handle_full_paper import remove_comments
from handle_full_paper import remove_astrik_inside_paranthases
import cv2
from pdf2image import convert_from_path
import numpy as np
NUMBER_OF_LAST_PAGES = 2
THRESHOLD = 5

Model_Classification_Path = "code/greedy_from_machine/classification_models"
Model_Regressor_Path = "code/greedy_from_machine/regression_models"

allowed_operators = [('1', '1', '10', '1'), ('1', '1', '10', '2'),
('1', '1', '10', '3'),
('1', '1', '10', '4'),
('1', '1', '10', '5'),
('1', '1', '11', '1'),
('1', '1', '11', '2'),
('1', '1', '1', '1'),
('1', '1', '1', '2'),
('1', '1', '1', '3'),
('1', '1', '1', '4'),
('1', '1', '1', '5'),
('1', '1', '1', '6'),
('1', '1', '1', '7'),
('1', '1', '1', '8'),
('1', '1', '2', '1'),
('1', '1', '2', '2'),
('1', '1', '2', '3'),
('1', '1', '2', '4'),
('1', '1', '4', '1'),
('1', '1', '4', '2'),
('1', '1', '5', '1'),
('1', '1', '5', '2'),
('1', '1', '6', '1'),
('1', '1', '6', '2'),
('1', '1', '7', '1'),
('1', '1', '7', '2'),
('1', '1', '7', '3'),
('1', '1', '9', '1'),
('1', '2', '10', '1'),
('1', '2', '10', '2'),
('1', '2', '10', '3'),
('1', '2', '10', '4'),
('1', '2', '10', '5'),
('1', '2', '11', '1'),
('1', '2', '11', '2'),
('1', '2', '1', '1'),
('1', '2', '1', '2'),
('1', '2', '1', '3'),
('1', '2', '1', '4'),
('1', '2', '1', '5'),
('1', '2', '1', '6'),
('1', '2', '1', '7'),
('1', '2', '1', '8'),
('1', '2', '2', '1'),
('1', '2', '2', '2'),
('1', '2', '2', '3'),
('1', '2', '2', '4'),
('1', '2', '4', '1'),
('1', '2', '4', '2'),
('1', '2', '5', '1'),
('1', '2', '5', '2'),
('1', '2', '6', '1'),
('1', '2', '6', '2'),
('1', '2', '7', '1'),
('1', '2', '7', '2'),
('1', '2', '7', '3'),
('1', '2', '9', '1'),
('1', '3', '10', '1'),
('1', '3', '10', '2'),
('1', '3', '10', '3'),
('1', '3', '10', '4'),
('1', '3', '1', '2'),
('1', '3', '1', '3'),
('1', '3', '1', '4'),
('1', '3', '1', '5'),
('1', '3', '1', '6'),
('1', '3', '1', '7'),
('1', '3', '1', '8'),
('1', '3', '2', '1'),
('1', '3', '2', '2'),
('1', '3', '2', '3'),
('1', '3', '2', '4'),
('1', '3', '4', '1'),
('1', '3', '4', '2'),
('1', '3', '5', '1'),
('1', '3', '5', '2'),
('1', '3', '6', '1'),
('1', '3', '6', '2'),
('1', '3', '7', '1'),
('1', '3', '7', '2'),
('1', '3', '7', '3'),
('1', '3', '9', '1'),
('1', '4', '10', '1'),
('1', '4', '10', '2'),
('1', '4', '10', '3'),
('1', '4', '10', '4'),
('1', '4', '10', '5'),
('1', '4', '11', '1'),
('1', '4', '11', '2'),
('1', '4', '1', '1'),
('1', '4', '1', '2'),
('1', '4', '1', '3'),
('1', '4', '1', '4'),
('1', '4', '1', '5'),
('1', '4', '1', '6'),
('1', '4', '1', '7'),
('1', '4', '1', '8'),
('1', '4', '2', '1'),
('1', '4', '2', '2'),
('1', '4', '2', '3'),
('1', '4', '2', '4'),
('1', '4', '4', '1'),
('1', '4', '4', '2'),
('1', '4', '5', '1'),
('1', '4', '5', '2'),
('1', '4', '6', '1'),
('1', '4', '6', '2'),
('1', '4', '7', '1'),
('1', '4', '7', '2'),
('1', '4', '7', '3'),
('1', '4', '9', '1'),
('2', '0.5', '1'),
('2', '0.5', '2'),
('2', '0.5', '3'),
('2', '0.5', '4'),
('2', '0.6', '1'),
('2', '0.6', '2'),
('2', '0.6', '3'),
('2', '0.6', '4'),
('2', '0.7', '1'),
('2', '0.7', '2'),
('2', '0.7', '3'),
('2', '0.7', '4'),
('2', '0.8', '1'),
('2', '0.8', '2'),
('2', '0.8', '3'),
('2', '0.8', '4'),
('2', '0.9', '1'),
('2', '0.9', '2'),
('2', '0.9', '3'),
('2', '0.9', '4'),
('3', '1', '1'),
('3', '1', '2'),
('4', '1', '1'),
('5', '1', '1'),
('5', '1', '2'),
('6', '1', '2'),
('6', '1', '3'),
('6', '1', '4'),
('6', '1', '5'),
('6', '1', '6'),
('6', '1', '7'),
('6', '1', '8'),
('7', '0.6', '1'),
('7', '0.6', '2'),
('7', '0.7', '1'),
('7', '0.7', '2'),
('7', '0.8', '1'),
('7', '0.8', '2'),
('7', '0.9', '1'),
('7', '0.9', '2'),
('8', '1', '1'),
('8', '1', '2'),
('8', '1', '3'),
('8', '1', '4')]


"""
    This function load the models and stores them in dictionary, parameters:
    models_path - path to the models directory (string)
"""
def load_models():
    # Load models
    models = {}
    directory = Model_Classification_Path
    for file in os.scandir(directory):
        if file.is_file():
            n = re.findall('\d+\.?\d*', file.name)
            if n[0] == '1':
                i = (n[0], n[4], n[5], n[6]) # key for vspace
            else:
                i = (n[0], n[4], n[5]) # key for other operators

            file_path = directory + '/' + file.name
            clf = xg.XGBClassifier() # in this case we used the XGBClassifier models
            booster = xg.Booster()
            booster.load_model(file_path)
            clf._Booster = booster
            print(i)
            models[i] = clf

    return models


def load_regression_models_cat():
    #Load models
    models = {}
    directory = Model_Regressor_Path
    #print(directory)
    for file in os.scandir(directory):
        if file.is_file():
            n = re.findall('\d+\.?\d*', file.name)
            if n[0] == '1':
                i = (n[0], n[4], n[5], n[6])
            else:
                i = (n[0], n[4], n[5])
            
            file_path = directory + '/' + file.name
            clf = CatBoostRegressor()
            clf.load_model(file_path)
            print(i)
            #print(file_path)
            models[i] = clf

            
    print("total models in memory:", len(models))
    return models

def get_closest_operators(operators):
    """ Get the closest operators by cost to the  first operator in the list"""
    threshold = THRESHOLD
    cost_index = 0
    closest_opartors = [operators[0]]
    for i in range(1, len(operators)):
        current_operator = operators[i]
        if (abs(current_operator[cost_index] - closest_opartors[0][cost_index]) < threshold):
            closest_opartors.append(current_operator)
        else:
            break
    return closest_opartors


def get_prediction(operator,operators_done, models,df1):
    if str(operator[2]) == '1':
        model_to_predict = (str(operator[2]), str(operator[3]), str(operator[4]), operator[5])
                
    else:
        model_to_predict = (str(operator[2]), str(operator[3]), operator[5])
    # whether we applied the operator before
    if model_to_predict in operators_done:
        return -1, model_to_predict

    print("model_to_predict:", model_to_predict)
    
    try:
        # get the prediction from the model
        prediction = models[model_to_predict].predict(df1.to_numpy())[0]

    except Exception as e:
        print("not found model:", e)
        return -1, model_to_predict
    return prediction, model_to_predict


def get_new_height(img_path, new_width):
    try:
        if img_path.lower().endswith('.pdf'):
            images = convert_from_path(img_path, first_page=1, last_page=1)
            if images:
                image = images[0]
                # Convert PIL image to OpenCV format
                im = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                height, width, channel = im.shape
                new_height = round((height * new_width / width), 2)
                return new_height
        elif img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            im = cv2.imread(img_path)
            if im is not None:
                height, width, channel = im.shape
                new_height = round((height * new_width / width), 2)
                return new_height
        else:
            print("Unsupported file format or invalid path.")
    except Exception as e:
        print("Error:", e)
    return None

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def omit(list1, word, n1):
    # for counting the occurrence of word
    count = 0
    # for counting the index number
    # where we are at present
    index = 0
    for i in list1:
        index += 1
        if i == word:
            count += 1
            if count == n1:
                # (index-1) because in list
                # indexing start from 0th position
                list1.pop(index - 1)
    return list1


def is_par(lst, index):
    for i in reversed(range(index + 1)):
        if '\\paragraph' in lst[i]:
            return True
        elif lst[i] == '\n':
            continue
        else:
            return False


def combine_two_paragraphs(lst, index_1, index_2):
    # lst[index_1] = lst[index_1].replace("\n", " ") + lst.pop(index_2)
    # return lst
    # Start removing newlines from index_2 backward until a non-newline is found above it
    orig_2 = index_2
    while index_2 > index_1 + 1 and lst[index_2 - 1] == '\n':
        del lst[index_2 - 1]
        index_2 -= 1
    #remove \n from lst[index_2 - 1]
    lst[index_2 - 1] = lst[index_2 - 1].replace("\n", " ")
    
    # Combine the paragraphs by replacing the newline with a space
    lst[index_2 - 1] += " " + lst.pop(index_2)
    
    return lst

def extract_resizebox_width(latex_command):
    empty_resizebox = False
    missing_number_index = None
    # Regular expression pattern to match the width value in the LaTeX command
    pattern = r'\\resizebox{([0-9.]*)\\+[a-zA-Z]+}'
    match = re.search(pattern, latex_command)
    if match:
        width_value = match.group(1)
        if width_value == '':
            width_value = 1
            empty_resizebox = True
            missing_number_index = match.start(1)
        try:
            return float(width_value), empty_resizebox, missing_number_index
        except ValueError:
            return None, None, None
    else:
        return None, None, None

def perform_operators(objects, doc_index, latex_path, pdf_path,path_to_file, paper_name,lidor):  # ,path_to_file):

    latex_clean_lines = []
    with open(latex_path, encoding='UTF-8') as f:
        file = f.read()
        file = file.split("\n")
       
        for line in file:
            line = line.lstrip()
            line += "\n"
            latex_clean_lines.append(line)
           


  
    list_of_starts, tags = perry2.parse2_lidor(latex_path, lidor)  # perry.parse2_lidor(latex_path, lidor)
    index_for_object = {'Par': 1, 'Figure': 2, 'CaptionFigure': 3, 'Table': 4, 'CaptionTable': 5, 'Section': 6,
                        'SubSection': 7, 'Matrix': 8, 'Enum': 9, 'Formula': 10, 'Algorithm': 11}
    # mapping:
    mapping_dict = {}
    par_index = 0
    caption_index = 0
    matrix_index = 0
    title_index = 0
    abstractsec_index = 0
    abstractpar_index = 0
    section_index = 0
    subsection_index = 0
    subsubsection_index = 0
    enum_index = 0
    algo_index = 0
    undetected_index = 0
    formula_index = 0
    caption_table_index = 0
    paragraph_index = 0
    figure_index = 0
    table_index = 0
    
    for i in range(len(list_of_starts)):
        if (tags[i][0][0] == 'Par'):
            par_index += 1
            index = par_index
        elif (tags[i][0][0] == 'Title'):
            title_index += 1
            index = title_index
        elif (tags[i][0][0] == 'AbstractSection'):
            abstractsec_index += 1
            index = abstractsec_index
        elif (tags[i][0][0] == 'AbstractPar'):
            abstractpar_index += 1
            index = abstractpar_index
        elif (tags[i][0][0] == 'Section'):
            section_index += 1
            index = section_index
        elif (tags[i][0][0] == 'SubSection'):
            subsection_index += 1
            index = subsection_index
        elif (tags[i][0][0] == 'SubSubSection'):
            subsubsection_index += 1
            index = subsubsection_index
        elif (tags[i][0][0] == 'Enum'):
            enum_index += 1
            index = enum_index
        elif (tags[i][0][0] == 'Algorithm'):
            algo_index += 1
            index = algo_index
        elif (tags[i][0][0] == 'CaptionFigure'):
            caption_index += 1
            index = caption_index
        elif (tags[i][0][0] == 'CaptionTable'):
            caption_table_index += 1
            index = caption_table_index
        elif (tags[i][0][0] == 'Formula'):
            formula_index += 1
            index = formula_index
        elif (tags[i][0][0] == 'Paragraph'):
            paragraph_index += 1
            index = paragraph_index
        else:
            undetected_index += 1
            index = undetected_index
        if (tags[i][0][0] == 'Figure'):
            mapping_dict[tags[i][0][0] + str(tags[i][0][1])] = (list_of_starts[i], latex_clean_lines[list_of_starts[i]])
        elif (tags[i][0][0] == 'Table'):
            mapping_dict[tags[i][0][0] + str(int(tags[i][0][1]) + 1)] = (
                list_of_starts[i], latex_clean_lines[list_of_starts[i]])
        else:
            mapping_dict[tags[i][0][0] + str(index)] = (list_of_starts[i], latex_clean_lines[list_of_starts[i]])

   
    # we are taking into a account that latex and pdf may be ordered differently
    indexer = 0
    object_to_add_vspace_behind = 0
   
    arr_of_places_and_vspace_to_add = []
    figure_name_key_new_latex_list_value = {}
    table_name_key_new_latex_list_value = {}
    object_name_key_new_latex_list_value = {}  # for removing special positioning chars
    dict_for_removing_last_2_words_operator = {}
    offset = 0

    combined_paragraphs_list = []
    par_remove_list = []
    algorithm_list = []
    enum_list = []
    items_seen = []
    item_num = 1
    occurrence_num = 1
    seen_paragraph = False

    pdf_order = list(objects.keys())
    latex_order = list(mapping_dict.keys())
    pdf_pairs = [(pdf_order[i], pdf_order[i + 1]) for i in range(len(pdf_order) - 1)]
    latex_pairs = [(latex_order[i], latex_order[i + 1]) for i in range(len(latex_order) - 1)]
    pair_to_check = []
    
    height = 0
    width = 0

    for key, value in objects.items():  # in this loop we will make all the operators

        if (key.startswith('CaptionTable')):
            if (value['last_line_length_words'] == 1):
                # remove last 2 words
                chosen_index_to_insert = mapping_dict[key][0]
                new_list_2 = copy.deepcopy(latex_clean_lines)
                if (new_list_2[chosen_index_to_insert][-1] == '\n'):  # remember that the par ends that way
                    new_part_last = new_list_2[chosen_index_to_insert][:len(new_list_2[chosen_index_to_insert]) - 1]
                    new_part_last_2 = new_part_last.rsplit(' ', 2)[0]  # remove last 2 words
                    new_part_last_2 = new_part_last_2 + "\n"
                    new_list_2[chosen_index_to_insert] = new_part_last_2
                    dict_for_removing_last_2_words_operator[key] = (new_list_2, 5, 10)

        if (key.startswith('CaptionFigure')):
            if (value['last_line_length_words'] == 1):
                # remove last 2 words
                chosen_index_to_insert = mapping_dict[key][0]
                new_list_2 = copy.deepcopy(latex_clean_lines)
                if (new_list_2[chosen_index_to_insert][-1] == '\n'):  # remember that the par ends that way
                    new_part_last = new_list_2[chosen_index_to_insert][:len(new_list_2[chosen_index_to_insert]) - 1]
                    new_part_last_2 = new_part_last.rsplit(' ', 2)[0]  # remove last 2 words
                    new_part_last_2 = new_part_last_2 + "\n"
                    new_list_2[chosen_index_to_insert] = new_part_last_2
                    dict_for_removing_last_2_words_operator[key] = (new_list_2, 3, 10)

        if (key.startswith('Paragraph')):
            chosen_index_to_insert = mapping_dict[key][0]
            new_list = copy.deepcopy(latex_clean_lines)
            if is_par(new_list, chosen_index_to_insert):  # remove tag of paragraph operator
                seen_paragraph = False
                for i in reversed(range(chosen_index_to_insert + 1)):
                    if '\\paragraph' in new_list[i]:
                        tag = new_list.pop(i)
                        temp = tag[tag.find("{") + 1:tag.find("}")]
                        temp = "\\textbf{" + temp + "} "
                        new_list[i] = temp + new_list[i]
                        break
                if (value['last_line_length_words'] == 1):
                    par_remove_list.append((new_list, key, 10))
                else:
                    par_remove_list.append((new_list, key, 0))

        new_key_for_par = ''.join(i for i in key if not i.isdigit())
        if (new_key_for_par == 'Par'):
            chosen_index_to_insert = mapping_dict[key][0]
            new_list = copy.deepcopy(latex_clean_lines)
            # combine two paragraphs operator
            if seen_paragraph:  # if the previous object was paragraph
                pair_to_check.append(key)
                if tuple(pair_to_check) in pdf_pairs and tuple(
                        pair_to_check) in latex_pairs:  # check if the 2 objects adjacent in pdf and latex
                    new_list = combine_two_paragraphs(new_list, previous_par_index, chosen_index_to_insert)
                    combined_paragraphs_list.append((new_list, key, 10))
                    pair_to_check.clear()
                    pair_to_check.append(key)
                    previous_par_index = chosen_index_to_insert
            else:
                seen_paragraph = True
                pair_to_check.append(key)
                previous_par_index = chosen_index_to_insert

            # remove last 2 words if the sentence end with 1 word
            if (value['last_line_length_words'] == 1):
                # remove last 2 words
                chosen_index_to_insert = mapping_dict[key][0]
                new_list_2 = copy.deepcopy(latex_clean_lines)
                if (new_list_2[chosen_index_to_insert][-1] == '\n'):  # remember that the par ends that way
                    new_part_last = new_list_2[chosen_index_to_insert][:len(new_list_2[chosen_index_to_insert]) - 1]
                    new_part_last_2 = new_part_last.rsplit(' ', 2)[0]  # remove last 2 words
                    new_part_last_2 = new_part_last_2 + "\n"
                    new_list_2[chosen_index_to_insert] = new_part_last_2
                    dict_for_removing_last_2_words_operator[key] = (new_list_2, 1, 10)
        else:
            seen_paragraph = False
            pair_to_check.clear()

        if (key.startswith('Enum')):  # convert enum to paragraph operator
            if (int(key[4:]) not in items_seen):
                chosen_index_to_insert = mapping_dict[key][0]
                new_list = copy.deepcopy(latex_clean_lines)
                number = 1
                for i in range(chosen_index_to_insert, len(new_list)):
                    if new_list[i] == '\\end{enumerate}\n':
                        break
                    if "\\item" in new_list[i]:
                        new_list[i] = new_list[i].replace("\\item", f"{number}.")
                        items_seen.append(item_num)
                        item_num += 1
                        number += 1
                new_list = omit(new_list, "\\begin{enumerate}\n", occurrence_num)
                new_list = omit(new_list, "\\end{enumerate}\n", occurrence_num)
                occurrence_num += 1
                heuristic = number - 2
                heuristic = heuristic * 3.3
                enum_list.append((new_list, key, heuristic))

            if (value['last_line_length_words'] == 1):
                # remove last 2 words
                chosen_index_to_insert = mapping_dict[key][0]
                new_list_2 = copy.deepcopy(latex_clean_lines)
                if (new_list_2[chosen_index_to_insert][-1] == '\n'):  # remember that the par ends that way
                    new_part_last = new_list_2[chosen_index_to_insert][:len(new_list_2[chosen_index_to_insert]) - 1]
                    new_part_last_2 = new_part_last.rsplit(' ', 2)[0]  # remove last 2 words
                    new_part_last_2 = new_part_last_2 + "\n"
                    new_list_2[chosen_index_to_insert] = new_part_last_2
                    dict_for_removing_last_2_words_operator[key] = (new_list_2, 9, 10)

        if (key.startswith('Algorithm')):  # change size of algorithm operator
            chosen_index_to_insert = mapping_dict[key][0]
            new_list = copy.deepcopy(latex_clean_lines)
            # find number of lines in algorithmic:
            counter_lines = 0
            start_counting = False
            for i in range(chosen_index_to_insert, len(new_list)):
                if (new_list[i].startswith('\\end{algorithmic}')):
                    start_counting = False
                    break
                if (start_counting):
                    counter_lines += 1
                if (new_list[i].startswith('\\begin{algorithmic}')):
                    start_counting = True

            new_list.insert(chosen_index_to_insert + 1, "\\small\n")
            heuristic = counter_lines * 0.77
            algorithm_list.append((new_list, key, heuristic))

            # another operator for algorithm, remove special postion letter:
            new_list_2 = copy.deepcopy(latex_clean_lines)
            string_to_edit = new_list_2[chosen_index_to_insert]
            index_to_edit = string_to_edit.find('[')
            if (index_to_edit != -1):  # there is a special positional char
                new_string_to_edit = re.sub("[\(\[].*?[\)\]]", "", string_to_edit)
                new_list_2[chosen_index_to_insert] = new_string_to_edit
                object_name_key_new_latex_list_value[key] = (new_list_2, 11, 5) #TODO!!!! check cost 

        if (key.startswith('Table')):
            chosen_index_to_insert = mapping_dict[key][0]  # index where the figure starts
            flag = False
            index_to_go_through = chosen_index_to_insert
            while (flag != True):
                if (index_to_go_through > len(latex_clean_lines)):
                    break
                if (latex_clean_lines[index_to_go_through].startswith(
                        '\\begin{adjustbox}')) or latex_clean_lines[index_to_go_through].startswith('\\resizebox'):  # finding the line where we can change the scale of the figure
                    found_index = index_to_go_through
                    flag = True                    

                else:
                    index_to_go_through += 1
            if (flag == False):
                continue
            # now we will shrink the figure to the 5 options of shrinking:
            # we will first find the places and then add the values based on the scale
            string_to_edit = latex_clean_lines[
                found_index]  # the line that we need to edit in order to change the scale
            width, empty_resizebox, resize_index = extract_resizebox_width(string_to_edit)
            # we will look for width and if it exists we will change it
            empty_number = False
            start_index = string_to_edit.find('width')
            running_index = 0
            if (start_index != -1) and width == None:  # find the number for width
                running_index = start_index
                while (running_index < len(string_to_edit)):
                    if (string_to_edit[running_index] == '='):
                        running_index += 1  # now we will find the number and change it
                        end_number = False
                        number = ''
                        while (end_number != True):
                            if (string_to_edit[running_index] == '\\'):
                                end_number = True
                            else:
                                number += string_to_edit[running_index]
                                running_index += 1
                        if number == '':
                            number = 1
                            empty_number = True
                        width = float(number)
                        break
                    running_index += 1
            options = [0.9, 0.8, 0.7, 0.6]  # scale options
            table_name_key_new_latex_list_value[
                key] = []  # this dict will have the key as the table name and then value will be the lists of the new latex content for the new file
            string_to_edit = latex_clean_lines[found_index]  # the string to edit
            heuristic = 0
            for i in range(4):
                if (i == 0):
                    heuristic = value['height'] * 0.1
                elif (i == 1):
                    heuristic = value['height'] * 0.2
                elif (i == 2):
                    heuristic = value['height'] * 0.3
                elif (i == 3):
                    heuristic = value['height'] * 0.4
                new_width = options[i] 
                if width == 0:
                    #  in the begin adjust box there is no width. we have begin{adjubox}{}, we need to find the index of the second {
                    index_of_second_bracket = string_to_edit.find('{', string_to_edit.find('{') + 1)
                    new_str = string_to_edit[:index_of_second_bracket + 1] + "width=" + str(new_width) + "\columnwidth" + string_to_edit[index_of_second_bracket+1:]
                else:
                    if empty_number:
                       #add the new_width after =
                        new_str = string_to_edit.replace('=', '=' + str(new_width)) 
                    elif empty_resizebox:
                        #add the new_width to the resize_index
                        new_str = string_to_edit[:resize_index] + str(new_width) + string_to_edit[resize_index:]
                    elif width == 2: 
                        new_str = string_to_edit.replace(str(int(width)), str(2 * new_width))
                    elif width == 1:
                        new_str = string_to_edit.replace(str(int(width)), str(new_width))                        
                    else:
                        new_str = string_to_edit.replace(str(width), str(round(new_width * width, 2)))
                copy_list = copy.deepcopy(latex_clean_lines)
                copy_list[found_index] = new_str
                table_name_key_new_latex_list_value[key].append(
                    (copy_list, heuristic))  # changing the string and adding the new latex list into the dict

            # another operator for Table, remove special postion letter:
            new_list_2 = copy.deepcopy(latex_clean_lines)
            string_to_edit = new_list_2[chosen_index_to_insert]
            index_to_edit = string_to_edit.find('[')
            if (index_to_edit != -1):  # there is a special positional char
                new_string_to_edit = re.sub("[\(\[].*?[\)\]]", "", string_to_edit)
                new_list_2[chosen_index_to_insert] = new_string_to_edit
                object_name_key_new_latex_list_value[key] = (new_list_2, 4, 5)

        if (key.startswith('Figure')):  # changing size of figure
            chosen_index_to_insert = mapping_dict[key][0]  # index where the figure starts
            flag = False
            index_to_go_through = chosen_index_to_insert
            while (flag != True):
                if (index_to_go_through > len(latex_clean_lines)):
                    break
                if (latex_clean_lines[index_to_go_through].startswith(
                        '\\includegraphics')):  # finding the line where we can change the scale of the figure
                    found_index = index_to_go_through
                    flag = True
                else:
                    index_to_go_through += 1
            if (flag == False):
                continue
            # now we will shrink the figure to the 5 options of shrinking:
            # we will first find the places and then add the values based on the scale
            string_to_edit = latex_clean_lines[
                found_index]  # the line that we need to edit in order to change the scale
            # we will look for width and if it exists we will change it
            start_index = string_to_edit.find('width')
            running_index = 0
            if (start_index != -1):  # find the number for width
                running_index = start_index
                while (running_index < len(string_to_edit)):
                    if (string_to_edit[running_index] == '='):
                        running_index += 1  # now we will find the number and change it
                        end_number = False
                        number = ''
                        while (end_number != True):
                            if (string_to_edit[running_index] == '\\'):
                                end_number = True
                            else:
                                number += string_to_edit[running_index]
                                running_index += 1
                        if number == '':
                            number= 1
                        width = float(number)
                        break
                    running_index += 1
            given_height = False
            start_index = string_to_edit.find('height')
            running_index = 0
            if (start_index != -1):  # find the number for height
                running_index = start_index
                given_height = True
                while (running_index < len(string_to_edit)):
                    if (string_to_edit[running_index] == '='):
                        running_index += 1  # now we will find the number and change it
                        end_number = False
                        number = ''
                        while (end_number != True):
                            if (string_to_edit[running_index].isdigit() == False and string_to_edit[running_index] not in ['.', ',']):
                                end_number = True
                            else:
                                number += string_to_edit[running_index]
                                running_index += 1
                        
                        height = float(number)
                        break
                    running_index += 1
            else: #no height declared in latex, we will find the height using proportion of width 
                #get height in point and convert to inches
                height = round(value['height']/72, 2)

               
                
                
            # create 5 options:
            options = [0.9, 0.8, 0.7, 0.6, 0.5]  # scale options
            figure_name_key_new_latex_list_value[
                key] = []  # this dict will have the key as the figure name and then value will be the lists of the new latex content for the new file
            string_to_edit = latex_clean_lines[found_index]  # the string to edit
            if not given_height:
                index_for_height = string_to_edit.find(']')
                string_to_edit = string_to_edit[:index_for_height] + ",height=" + str(height) +"in "+ string_to_edit[index_for_height:]
            heuristic = 0
            for i in range(5):
                if (i == 0):
                    heuristic = value['height'] - (value['height'] * 0.9)
                elif (i == 1):
                    heuristic = value['height'] - (value['height'] * 0.8)
                elif (i == 2):
                    heuristic = value['height'] - (value['height'] * 0.7)
                elif (i == 3):
                    heuristic = value['height'] - (value['height'] * 0.6)
                elif (i == 4):
                    heuristic = value['height'] - (value['height'] * 0.5)
                new_width = width * options[i]
                new_height = height * options[i]
                new_str = string_to_edit.replace(str(width), str(new_width))
                new_str = new_str.replace(str(height), str(new_height))

                    
                copy_list = copy.deepcopy(latex_clean_lines)
                copy_list[found_index] = new_str
                figure_name_key_new_latex_list_value[key].append(
                    (copy_list, heuristic))  # changing the string and adding the new latex list into the dict

            # another operator for Table, remove special postion letter:
            new_list_2 = copy.deepcopy(latex_clean_lines)
            string_to_edit = new_list_2[chosen_index_to_insert]
            index_to_edit = string_to_edit.find('[')
            if (index_to_edit != -1):  # there is a special positional char
                new_string_to_edit = re.sub("[\(\[].*?[\)\]]", "", string_to_edit)
                new_list_2[chosen_index_to_insert] = new_string_to_edit
                object_name_key_new_latex_list_value[key] = (new_list_2, 2, 5)

        if (
                indexer == 0):  # in this if we wanted to skip the first object for the vspace but we need the first element for the other operators.
            indexer += 1
            continue
        else:
            if (value['space_between_this_object_and_last_object'] > 10):  # candidate to add vspace
                chosen_index_to_insert = mapping_dict[key][0]
                if ('Formula' in key):
                    # we will make 3 partitions:
                    vspace_size_max = value['space_between_this_object_and_last_object'] / 7
                    herustica = 0
                    vspace_size_part = vspace_size_max / 4
                    for i in range(1, 5):
                        herustica = (value['space_between_this_object_and_last_object'] * i) / 4
                        vspace_size = "{:.2f}".format(vspace_size_part * i)
                        for j in index_for_object.keys():
                            if (key.startswith(j)):
                                num = index_for_object[j]
                        arr_of_places_and_vspace_to_add.append((chosen_index_to_insert,
                                                                '\\vspace{-' + str(vspace_size) + 'mm}\n', num,
                                                                vspace_size, key, herustica, i))
                        offset += 1
                else:
                    vspace_size_max = value['space_between_this_object_and_last_object'] / 3.5
                    vspace_size_part = vspace_size_max / 4
                    for i in range(1, 5):
                        herustica = (value['space_between_this_object_and_last_object'] * i) / 4
                        vspace_size = "{:.2f}".format(vspace_size_part * i)
                        for j in index_for_object.keys():
                            if (key.startswith(j)):
                                num = index_for_object[j]

                        arr_of_places_and_vspace_to_add.append((chosen_index_to_insert,
                                                                '\\vspace{-' + str(vspace_size) + 'mm}\n', num,
                                                                vspace_size, key, herustica, i))
                        offset += 1

    # we will create a new doc with each vspace addition:
    new_clean_latex_to_remember = copy.deepcopy(latex_clean_lines)
    # we will make changes to latex_clean_lines and then clean it with new_clean_latex_to_remember
    files_created = []
    operators_dict = []
    index_for_all_operators = 1

    for i in range(len(arr_of_places_and_vspace_to_add)):
        latex_clean_lines = []
        latex_clean_lines = copy.deepcopy(new_clean_latex_to_remember)
        chosen_index_to_insert = arr_of_places_and_vspace_to_add[i][0]
        str__ = arr_of_places_and_vspace_to_add[i][1]
        latex_clean_lines.insert(chosen_index_to_insert, str__)
        latex_clean_lines = latex_clean_lines  # [1:]
        latex_string = ''.join(latex_clean_lines) #todo find why putting all the latexstring
        num_of_object = re.findall('\d+', arr_of_places_and_vspace_to_add[i][4])[0]
        operators_dict.append((arr_of_places_and_vspace_to_add[i][5], latex_string, 1,
                               arr_of_places_and_vspace_to_add[i][6], arr_of_places_and_vspace_to_add[i][2],
                               num_of_object))  # type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    # here we will create the new files for figure changes
    options = [0.9, 0.8, 0.7, 0.6, 0.5]
    for key, value in figure_name_key_new_latex_list_value.items():
        for i in range(5):
            x_list = value[i][0]  # [1:]
            latex_string = ''.join(x_list)
            num_of_object = re.findall('\d+', key)[0]
            operators_dict.append((value[i][1], latex_string, 2, options[i], 2,
                                   num_of_object))  # type, value, object_used_on, num_of_object

            index_for_all_operators += 1

    # create new files for table changes
    options = [0.9, 0.8, 0.7, 0.6]
    for key, value in table_name_key_new_latex_list_value.items():
        for i in range(4):
            x_list = value[i][0]  # [1:]
            latex_string = ''.join(x_list)
            num_of_object = re.findall('\d+', key)[0]

            operators_dict.append((value[i][1], latex_string, 7, options[i], 4,
                                   num_of_object))  # type, value, object_used_on, num_of_object

            index_for_all_operators += 1

    for al in algorithm_list:
        x_list = al[0]  # [1:]
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', al[1])[0]

        operators_dict.append(
            (al[2], latex_string, 3, 1, 11, num_of_object))  # type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for enum in enum_list:
        x_list = enum[0]  # [1:]
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', enum[1])[0]
        operators_dict.append(
            (enum[2], latex_string, 4, 1, 9, num_of_object))  # type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for par in par_remove_list:
        x_list = par[0]  # [1:]
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', par[1])[0]
        operators_dict.append(
            (par[2], latex_string, 5, 1, 1, num_of_object))  # type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for par in combined_paragraphs_list:
        x_list = par[0]  # [1:]
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', par[1])[0]
        operators_dict.append(
            (par[2], latex_string, 6, 1, 1, num_of_object))  # type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    # for key, value in object_name_key_new_latex_list_value.items():
    #     x_list = value[0]
    #     latex_string = ''.join(x_list)
    #     num_of_object = re.findall('\d+', key)[0]
    #     operators_dict.append(
    #         (value[2], latex_string, 8, 1, value[1], num_of_object))  # type, value, object_used_on, num_of_object
    #     index_for_all_operators += 1

    for key, value in dict_for_removing_last_2_words_operator.items():
        x_list = value[0]
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', key)[0]
        operators_dict.append(
            (value[2], latex_string, 9, 1, value[1], num_of_object))  # type, value, object_used_on, num_of_object
        index_for_all_operators += 1


    return sorted(operators_dict, key=lambda x: x[0])  # , reverse=True) #remove reversedd



""" 
    This function return the number of lines in the last page of pdf file and the number of pages, parameters:
    file_path - path to the pdf file 
"""
def check_lines(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        # Get the number of pages in the PDF
        pages = len(pdf.pages)
        # Get the last page
        last_page = pdf.pages[pages - 1]
        # Extract the text from the last page
        text = last_page.extract_text()
        # Split the text into lines
        lines = text.split('\n')
        return len(lines), pages


""" 
    This is a simple algorithm with no condition for applying operator, parameters:
    path_to_pdf - path to the pdf file 
    path_to_latex - path to the latex file 
"""

def feature_extract_and_validate_paper(path_to_pdf, path_to_latex, paper_name):
    df, lidor = features_single.run_feature_extraction(path_to_latex, path_to_pdf, '/code/greedy_from_machine/bibliography.bib',
                                                    "code/~/results/dct0",
                                                    "code/~/results/new_files/dct0", "test", pd.DataFrame())
    lines, pages = check_lines(path_to_pdf)
    #check whether the file is not good for the algorithm:
    if lines < 2:
        print("Less then 2 lines")
        return df, lidor, lines, pages, False
    if pages < 2:
        print("Less then 2 pages")
        return df, lidor, lines, pages, False
    
    return df, lidor, lines, pages, True


def handle_new_operator_and_check_reduced(latex_after_operator, paper_name,iteration,target,previous_num_of_pages,algorithm_number):
    # write the file after operator to file
            reduced = False
            after_path = os.path.join("code/~/results/new_files/", paper_name)
            after_path = os.path.join(after_path, f"after_operator{algorithm_number}.tex")
            f = open(after_path, "w")
            f.write(latex_after_operator)
            f.close()

            # compile the file
            # cmd_line_act = 'tectonic -X compile ' + "code/~/results/new_files/after_operator1.tex"
            dir_path = os.path.join("code/~/results/new_files", paper_name)
            base_name = os.path.basename(after_path)
            # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
            subprocess.run(['pdflatex', '-interaction=nonstopmode', base_name], cwd=dir_path) #On mac
            after_pdf = os.path.join("code/~/results/new_files/", paper_name)
            after_pdf = os.path.join(after_pdf, f"after_operator{algorithm_number}.pdf")
            last_pages_pdf = copy_last_pages(after_pdf, NUMBER_OF_LAST_PAGES, iteration)
            
            
            # os.system(cmd_line_act)
            new_number_of_pages = check_lines(after_pdf)[1]
            # check the new current number of lines
            lines, pages = check_lines(last_pages_pdf)
            fullLines , fullPages = check_lines(after_pdf)
            print("current lines:", lines)
            print("current pages:", pages)

            path_to_latex = after_path

            if (pages < 2 or new_number_of_pages < previous_num_of_pages): # lines > starting_lines is for the case that we get the last 2 pages after we made it shoreter
                reduced = True

            return reduced, path_to_latex, last_pages_pdf

def get_operator(res, index):
    if str(res[index][2]) == '1':
        oper = (str(res[index][2]), str(res[index][3]), str(res[index][4]), res[index][5])
    else:
        oper = (str(res[index][2]), str(res[index][3]), res[index][5])
    
    return oper

def simple_greedy(path_to_pdf, path_to_latex, num_of_pages,paper_name ):
    reduced = False
    try:
        operators_done = []
        iteration = 0
        total_cost = 0
        index = 0
        reduced = False
        count_operators = 0

        #perform feature extraction to the file
        df, lidor, lines, pages, valid = feature_extract_and_validate_paper(path_to_pdf, path_to_latex, paper_name)
        if not valid:
            return -1, -1, False, -1   
             
        # define stop condition and some variables
        target = lines - 2
        starting_lines = lines
        print("begin lines:", lines)
        print("begin pages:", pages)
        print("target lines:", target)
        not_allowed = []

        start = time.time()
        while ( not reduced ): # if we manage to short the paper
            print("lines : --------------", lines, "pages: --------------", pages)
            # get the dictionary of the file
            with open('code/~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file) #dict of dicts: for each object in file what are the features

            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, path_to_pdf ,"code/~/results/new_files/", paper_name,lidor)
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)):
                print("Out of operators")
                break

            oper = get_operator(res, index)

            # whether we applied the operator before
            if oper in operators_done or oper not in allowed_operators:
                index += 1
                if oper not in allowed_operators:
                    not_allowed.append(oper)
                continue
            else:
                operators_done.append(oper)

            latex_after_operator = res[index][1]
            
            reduced, path_to_latex, last_pages_pdf = handle_new_operator_and_check_reduced(latex_after_operator, paper_name,iteration,target,num_of_pages,0)

            if not reduced:
                df, lidor = features_single.run_feature_extraction(path_to_latex, 
                        last_pages_pdf, 'code/~/results/bibliography.bib',
                        "code/~/results/dct0", "code/~/results/new_files/dct0", "test", pd.DataFrame())

            total_cost += res[index][0]
            index = 0 
            iteration += 1

        end = time.time()
        print("RESULTS: simple, ", paper_name, ": ", iteration, " iterations, ", end - start, " seconds, ", reduced, " reduced, ", total_cost, " total cost")
        count_operators = iteration
        print("not allowed operators:", not_allowed)
        print("operators done:", operators_done)
        return iteration, end - start, reduced, total_cost,count_operators
    except Exception as e:
        print(e)
        if iteration > 0:
            end = time.time()
            return iteration, end - start, reduced, total_cost,count_operators
        return -1, -1, reduced, -1,-1


""" 
    This is a heuristic algorithm based on the heuristic, parameters:
    path_to_pdf - path to the pdf file 
    path_to_latex - path to the latex file 
"""
def heuristic_greedy(path_to_pdf, path_to_latex,num_of_pages, paper_name):
    reduced = False
    try:
        operators_done = []
        index = 0
        reduced = False
        iteration = 0
        count_operators = 0
        LINE_WIDTH = 10
        total_cost = 0
        #perform feature extraction to the file
        
        df, lidor, lines, pages, valid = feature_extract_and_validate_paper(path_to_pdf, path_to_latex, paper_name)
        if not valid:
            return -1, -1, False, -1
        

        # define stop condition and some variables
        target = lines - 2
        starting_lines = lines
        print("begin lines:", lines)
        print("begin pages:", pages)


        start = time.time()
        while (not reduced):            
            # get the dictionary of the file
            with open('code/~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)
            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, path_to_pdf, "code/~/results/new_files/", paper_name, lidor)
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)):
                print("Out of operators")
                break

            oper = get_operator(res, index)

            # whether we applied the operator before
            if oper in operators_done or oper not in allowed_operators:
                index += 1
                continue
            else:
                operators_done.append(oper)

            # condition to apply the operator
            if res[index][0] >= LINE_WIDTH:
                count_operators += 1
                latex_after_operator = res[index][1]
                
                reduced, path_to_latex, last_pages_pdf = handle_new_operator_and_check_reduced(latex_after_operator, paper_name,iteration,target,num_of_pages,1)

                if not reduced:
                    df , lidor = features_single.run_feature_extraction(path_to_latex, 
                    last_pages_pdf, 'code/~/results/bibliography.bib',
                    "code/~/results/dct0", "code/~/results/new_files/dct0", "test", pd.DataFrame())

                iteration += 1
                total_cost += res[index][0]
                index = 0
            else:
                index += 1
                count_operators += 1

        end = time.time()
        print("RESULTS: heuristic, ", paper_name, ": ", iteration, " iterations, ", end - start, " seconds, ", reduced, " reduced, ", total_cost, " total cost")
        return iteration, end - start, reduced, total_cost,count_operators
    except Exception as e:
        print(e)
        if iteration > 0:
            end = time.time()
            return iteration, end - start, reduced, total_cost,count_operators
        return -1, -1, reduced, -1,-1
    
    
def non_stop_heuristic_greedy(path_to_pdf, path_to_latex,num_of_pages, paper_name):
    reduced = False
    try:
        operators_done = []
        index = 0
        count_operators = 0
        reduced = False
        iteration = 0
        LINE_WIDTH = 10
        total_cost = 0
        start_check_operators_that_faild = False
        #perform feature extraction to the file
        df, lidor, lines, pages, valid = feature_extract_and_validate_paper(path_to_pdf, path_to_latex, paper_name)
        if not valid:
            return -1, -1, False, -1
        
        # define stop condition and some variables
        target = lines - 2
        starting_lines = lines
        print("begin lines:", lines)
        print("begin pages:", pages)

        start = time.time()
        while (not reduced):
            print("index:", index)
            
            # get the dictionary of the file
            with open('code/~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)
            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, path_to_pdf, "code/~/results/new_files/", paper_name, lidor)
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)) and not start_check_operators_that_faild:
                print("Out of operators, starts checking operators again.")
                start_check_operators_that_faild = True
                index = 0
            elif index >= (len(res)) and start_check_operators_that_faild:
                print("Out of operators, also out of operators that failed.")
                break

            oper = get_operator(res, index)

            # whether we applied the operator before
            if oper in operators_done or oper not in allowed_operators:
                index += 1
                continue
            

            # condition to apply the operator
            if res[index][0] >= LINE_WIDTH or start_check_operators_that_faild:
                count_operators += 1
                latex_after_operator = res[index][1]
                
                reduced, path_to_latex, last_pages_pdf = handle_new_operator_and_check_reduced(latex_after_operator, paper_name,iteration,target,num_of_pages,2)

                if not reduced:
                    df , lidor = features_single.run_feature_extraction(path_to_latex, last_pages_pdf, 'code/greedy_from_machine/bibliography.bib',
                                                        "code/~/results/dct0",
                                                        "code/~/results/new_files/dct0", "test", pd.DataFrame())

                iteration += 1
                total_cost += res[index][0]
                index = 0
            else:
                index += 1
                count_operators += 1
                if index >= (len(res)):
                    print("Out of operators, starts checking operators again.")
                    start_check_operators_that_faild = True
                    index = 0

        end = time.time()
        print("RESULTS: non stop heuristic, ", paper_name, ": ", iteration, " iterations, ", end - start, " seconds, ", reduced, " reduced, ", total_cost, " total cost")
        return iteration, end - start, reduced, total_cost,count_operators
    except Exception as e:
        print(e)
        if iteration > 0:
            end = time.time()
            return iteration, end - start, reduced, total_cost,count_operators
        return -1, -1, reduced, -1,-1





""" 
    This is a greedy algorithm based on the models, parameters:
    path_to_pdf - path to the pdf file 
    path_to_latex - path to the latex file 
    models - dict of models (dictionary) 
"""
def model_greedy(path_to_pdf, path_to_latex, models,num_of_pages , paper_name):
    reduced = False
    try:
        operators_done = []
        index = 0
        reduced = False
        count_operators = 0
        iteration = 0
        total_cost = 0
       
        #perform feature extraction to the file
        df1, lidor, lines, pages, valid = feature_extract_and_validate_paper(path_to_pdf, path_to_latex, paper_name)
        if not valid:
            return -1, -1, False, -1
        

        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                    'num_of_object'], axis=1, inplace=True)

        # define stop condition and some variables
        target = lines - 2
        starting_lines = lines
        print("begin lines:", lines)
        print("begin pages:", pages)

        start = time.time()
        while (not reduced):
            # get the dictionary of the file
            with open('code/~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)

            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, path_to_pdf, "code/~/results/new_files/", paper_name, lidor)
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)):
                print("Out of operators")
                break

            
            prediction, model_to_predict = get_prediction(operator=res[index],operators_done=operators_done, models=models,df1=df1)
            if prediction == -1:
                index += 1
                continue

            # condition to apply the operator
            if prediction > 0:
                count_operators += 1
                latex_after_operator = res[index][1]
                operators_done.append(model_to_predict)
                reduced, path_to_latex, last_pages_pdf = handle_new_operator_and_check_reduced(latex_after_operator, paper_name,iteration,target,num_of_pages,3)
                
                if not reduced:

                    df1, lidor = features_single.run_feature_extraction(
                        path_to_latex,
                        last_pages_pdf, 'code/~/results/bibliography.bib',
                        "code/~/results/dct0", "code/~/results/new_files/dct0", "test",
                        pd.DataFrame())
                    df1 = df1.T
                    df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                                'num_of_object'], axis=1, inplace=True)

                total_cost += res[index][0]
                index = 0
                iteration += 1
                
            else:
                index += 1
                count_operators += 1

        end = time.time()
        print("RESULTS: classification, ", paper_name, ": ", iteration, " iterations, ", end - start, " seconds, ", reduced, " reduced, ", total_cost, " total cost")
        print("operators done:",operators_done)
        return iteration, end - start, reduced, total_cost, count_operators
    except Exception as e:
        print(e)
        if iteration > 0:
            end = time.time()
            return iteration, end - start, reduced, total_cost,count_operators
        return -1, -1, reduced, -1,-1
    
    
def non_stop_classification_greedy(path_to_pdf, path_to_latex, models,num_of_pages , paper_name):
    reduced = False
    try:
        operators_done = []
        index = 0
        reduced = False
        iteration = 0
        count_operators = 0
        total_cost = 0
        start_check_operators_that_faild = False
        
        df1, lidor, lines, pages, valid = feature_extract_and_validate_paper(path_to_pdf, path_to_latex, paper_name)
        if not valid:
            return -1, -1, False, -1

        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                    'num_of_object'], axis=1, inplace=True)

        # define stop condition and some variables
        target = lines - 2
        starting_lines = lines
        print("begin lines:", lines)
        print("begin pages:", pages)
        start = time.time()
        while (not reduced):

            # get the dictionary of the file
            with open('code/~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)

            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, path_to_pdf, "code/~/results/new_files/", paper_name, lidor)
            print("total operators:", len(res))
            
            # whether there are no more operators
            if index >= (len(res)) and not start_check_operators_that_faild:
                print("Out of operators, starts checking operators again.")
                start_check_operators_that_faild = True
                index = 0
            elif index >= (len(res)) and start_check_operators_that_faild:
                print("Out of operators, also out of operators that failed.")
                break
                

            prediction, model_to_predict = get_prediction(operator=res[index],operators_done=operators_done, models=models,df1=df1)
            if prediction == -1:
                index += 1
                continue


            # condition to apply the operator
            if prediction or start_check_operators_that_faild:
                count_operators += 1
                latex_after_operator = res[index][1]
                operators_done.append(model_to_predict)
                
                reduced, path_to_latex, last_pages_pdf = handle_new_operator_and_check_reduced(latex_after_operator, paper_name,iteration,target,num_of_pages,4)
                
                if not reduced:
                    df1, lidor = features_single.run_feature_extraction(
                        path_to_latex, last_pages_pdf, 'code/greedy_from_machine/bibliography.bib',
                                                        "code/~/results/dct0",
                                                        "code/~/results/new_files/dct0", "test", pd.DataFrame())
                    df1 = df1.T
                    df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                                'num_of_object'], axis=1, inplace=True)

                total_cost += res[index][0]
                index = 0
                iteration += 1
                
            else:
                index += 1
                count_operators += 1
                if index >= (len(res)):
                    print("Out of operators, starts checking operators again.")
                    start_check_operators_that_faild = True
                    index = 0
                
        end = time.time()
        print("RESULTS: non stop classification, ", paper_name, ": ", iteration, " iterations, ", end - start, " seconds, ", reduced, " reduced, ", total_cost, " total cost")
        return iteration, end - start, reduced, total_cost,count_operators
    except Exception as e:
        print(e)
        if iteration > 0:
            end = time.time()
            return iteration, end - start, reduced, total_cost,count_operators
        return -1, -1, reduced, -1,-1
    
    
def regreession_model_greedy(path_to_pdf, path_to_latex, models,num_of_pages , paper_name):
    reduced = False
    try:
        operators_done = []
        index = 0
        reduced = False
        count_operators = 0
        iteration = 0
        total_cost = 0

        df1, lidor, lines, pages, valid = feature_extract_and_validate_paper(path_to_pdf, path_to_latex, paper_name)
        if not valid:
            return -1, -1, False, -1
        
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                    'num_of_object'], axis=1, inplace=True)

        # define stop condition and some variables
        target = lines - 2
        starting_lines = lines
        print("begin lines:", lines)
        print("begin pages:", pages)

        start = time.time()
        while (not reduced):
            # get the dictionary of the file
            with open('code/~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)

            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, path_to_pdf, "code/~/results/new_files/", paper_name, lidor)
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)):
                print("Out of operators")
                break
            
            oparators_to_check = res[index:] # all the operators that we need to check
            closest_operators = get_closest_operators(oparators_to_check) # get the closest operators to the current operator
            sorted_by_prediction_operators =  []
            for operator in closest_operators:
                prediction, model_to_predict = get_prediction(operator=operator,operators_done=operators_done, models=models,df1=df1)
                if prediction != -1:                
                    sorted_by_prediction_operators.append((operator,prediction, model_to_predict))
            # sort from highest to lowest prediction
            sorted_by_prediction_operators = sorted(sorted_by_prediction_operators, key=lambda x: x[1], reverse=True)

            if len(sorted_by_prediction_operators) == 0:
                index += 1
                continue

            operator = sorted_by_prediction_operators[0][0]
            prediction = sorted_by_prediction_operators[0][1]
            model_to_predict = sorted_by_prediction_operators[0][2]

            if model_to_predict in operators_done:
                index += 1
                continue
           
            if prediction > 0 :
                count_operators += 1
                latex_after_operator = res[index][1]
                operators_done.append(model_to_predict)
                
                reduced, path_to_latex, last_pages_pdf = handle_new_operator_and_check_reduced(latex_after_operator, paper_name,iteration,target,num_of_pages,5)
                
                if not reduced:

                    df1, lidor = features_single.run_feature_extraction(
                        path_to_latex, last_pages_pdf, 'code/greedy_from_machine/bibliography.bib',
                                                        "code/~/results/dct0",
                                                        "code/~/results/new_files/dct0", "test", pd.DataFrame())
                    df1 = df1.T
                    df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                                'num_of_object'], axis=1, inplace=True)

                total_cost += res[index][0]
                index  = 0
                iteration += 1

            else:
                index += 1
                count_operators += 1

        end = time.time()
        print("RESULTS: regression, ", paper_name, ": ", iteration, " iterations, ", end - start, " seconds, ", reduced, " reduced, ", total_cost, " total cost")
        return iteration, end - start, reduced, total_cost, count_operators
    except Exception as e:
        print(e)
        if iteration > 0:
            end = time.time()
            return iteration, end - start, reduced, total_cost,count_operators
        return -1, -1, reduced, -1,-1


def non_stop_regreession_model_greedy(path_to_pdf, path_to_latex, models,num_of_pages , paper_name):
    reduced = False
    try:
        operators_done = []
        index = 0
        reduced = False
        iteration = 0
        total_cost = 0
        count_operators = 0
        start_check_operators_that_faild = False

        
        df1, lidor, lines, pages, valid = feature_extract_and_validate_paper(path_to_pdf, path_to_latex, paper_name)
        if not valid:
            return -1, -1, False, -1
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                    'num_of_object'], axis=1, inplace=True)

        # define stop condition and some variables
        target = lines - 2
        starting_lines = lines
        print("begin lines:", lines)
        print("begin pages:", pages)

        start = time.time()
        while (not reduced):

            print("index:", index)

            # get the dictionary of the file
            with open('code/~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)

            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, path_to_pdf, "code/~/results/new_files/", paper_name, lidor)
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)) and not start_check_operators_that_faild:
                print("Out of operators, starts checking operators again.")
                start_check_operators_that_faild = True
                index = 0
            elif index >= (len(res)) and start_check_operators_that_faild:
                print("Out of operators, also out of operators that failed.")
                break
            
           
            oparators_to_check = res[index:] # all the operators that we need to check
            closest_operators = get_closest_operators(oparators_to_check) # get the closest operators to the current operator
            sorted_by_prediction_operators =  []
            for operator in closest_operators:
                prediction, model_to_predict = get_prediction(operator=operator,operators_done=operators_done, models=models,df1=df1)
                if prediction != -1:                
                    sorted_by_prediction_operators.append((operator,prediction, model_to_predict))
            # sort from highest to lowest prediction
            sorted_by_prediction_operators = sorted(sorted_by_prediction_operators, key=lambda x: x[1], reverse=True)

            if len(sorted_by_prediction_operators) == 0:
                index += 1
                continue

            operator = sorted_by_prediction_operators[0][0]
            prediction = sorted_by_prediction_operators[0][1]
            model_to_predict = sorted_by_prediction_operators[0][2]

            if model_to_predict in operators_done:
                index += 1
                continue
           
            if prediction > 0 or start_check_operators_that_faild:
                count_operators += 1
                latex_after_operator = res[index][1]
                operators_done.append(model_to_predict)
                
                reduced, path_to_latex, last_pages_pdf = handle_new_operator_and_check_reduced(latex_after_operator, paper_name,iteration,target,num_of_pages,6)
                
                if not reduced:

                    df1, lidor = features_single.run_feature_extraction(
                        path_to_latex, last_pages_pdf, 'code/greedy_from_machine/bibliography.bib',
                                                        "code/~/results/dct0",
                                                        "code/~/results/new_files/dct0", "test", pd.DataFrame())
                    df1 = df1.T
                    df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                                'num_of_object'], axis=1, inplace=True)

                total_cost += res[index][0]
                index = 0 
                iteration += 1

            else:
                count_operators += 1
                index += 1

        end = time.time()
        print("RESULTS: non stop regression, ", paper_name, ": ", iteration, " iterations, ", end - start, " seconds, ", reduced, " reduced, ", total_cost, " total cost")
        return iteration, end - start, reduced, total_cost,count_operators
    except Exception as e:
        print(e)
        if iteration > 0:
            end = time.time()
            return iteration, end - start, reduced, total_cost,count_operators
        return -1, -1, reduced, -1,-1


""" 
    This is a wrapper function to run the experiment, parameters:
    variant_function - function of the variant algorithm (function)
    variant_name - name of the variant (string)
    variant_file_name - name of the results file (string)
    files_dir - directory of the files to run the algorithm on (string)
    results_dir - directory to write the results file (string)
    models - dict of models (dictionary) 
"""
def run_greedy_experiment(variant_function, variant_name, variant_file_name, files_dir, results_dir, models=None):
    directory = files_dir
    results = []
    idx = 0
    done = 1
    #get last name of files_dir
    dir_name = files_dir.split('\\')[-1]
    for paper_dir in os.scandir(directory):
        print("paper_dir:", paper_dir.name)
        names = []
        paper_directory = paper_dir.name
        idx += 1
        path_to_latex = None
        path_to_pdf = None
        for file in os.scandir(paper_dir):
            if file.is_file():
                source_dir = os.path.join("code/greedy_from_machine/files", paper_directory)
                destination_dir = os.path.join("code/~/results/new_files", paper_directory)       
                os.makedirs(destination_dir, exist_ok=True)     
                if file.name.lower().endswith("_changed.pdf") :
                    path_to_pdf = os.path.join(destination_dir, file.name)
                if file.name.lower().endswith("_changed.tex") :
                    path_to_latex = os.path.join(destination_dir, file.name)
                source_path = file.path
                destination_path = os.path.join(destination_dir, file.name)
                shutil.copy(source_path, destination_path)
                if path_to_latex:
                    remove_comments(path_to_latex)
                if path_to_pdf:
                    num_of_pages = check_lines(path_to_pdf)[1]
                    last_pages_pdf_path = copy_last_pages(path_to_pdf,NUMBER_OF_LAST_PAGES, 0)

            elif file.is_dir():
                # move all the directories in 'code/greedy_from_machine/files' directory to 'code/~/results/new_files' directory
                source_dir = os.path.join("code/greedy_from_machine/files", paper_directory)
                destination_dir = os.path.join("code/~/results/new_files", paper_directory)
                os.makedirs(destination_dir, exist_ok=True)
                source_path = file.path
                destination_path = os.path.join(destination_dir, file.name)
                # if directory already exists in destination, do not copy it
                if not os.path.exists(destination_path):
                    shutil.copytree(source_path, destination_path)

        # whether you want to run the model-based greedy algorithm
        if models: 
            iterations, time_taken, reduced, cost,count_operators = variant_function(last_pages_pdf_path, path_to_latex, models,num_of_pages, paper_directory)

        # whether you want to run other greedy algorithms
        else: 
            iterations, time_taken, reduced, cost,count_operators = variant_function(last_pages_pdf_path, path_to_latex,num_of_pages, paper_directory)

        if iterations != -1:
            results.append(( paper_dir.name, variant_name, reduced, iterations, time_taken, cost,count_operators))
            try:
            # write the results every document finished (just in case)
                df = pd.DataFrame(results, columns=["Name", "Algorithm", "Reduced", "Iterations", "Time", "Cost","Total_operators"])
                df.to_csv(f'{results_dir}/{dir_name}_{variant_file_name}.csv', index=False)
            except Exception as e:
                print(e)

            print("Done!", done)
            done += 1

    # write the final results
    df = pd.DataFrame(results, columns=["Name", "Algorithm", "Reduced", "Iterations", "Time", "Cost","Total_operators"])
    df.to_csv(f'{results_dir}/{dir_name}_{variant_file_name}.csv', index=False)  # change here


if __name__ == "__main__":

    # get all the inputs from the script:
    x=int(sys.argv[1])
    pdf_tex_files_dir=sys.argv[2]
    dir_to_results=sys.argv[3]
    # path_to_models=sys.argv[4] # the tree of all optional of applying operators 

    # How to select algorithm type:
    #0 -> simple greedy algorithm.
    #1 -> heuristic greedy algorithm.
    #2 -> model greedy algorithm.
    # for x in range(1,7):
    for x in range(5,7):
        if x==0:  
            run_greedy_experiment(simple_greedy, "simple greedy", "results_simple_greedy", pdf_tex_files_dir, dir_to_results)
        elif x ==1:
            run_greedy_experiment(heuristic_greedy, "heuristic greedy", "results_heuristic_greedy", pdf_tex_files_dir, dir_to_results)
        elif x==2:
            run_greedy_experiment(non_stop_heuristic_greedy, "non stop heuristic greedy", "results_non_stop_heuristic_greedy", pdf_tex_files_dir, dir_to_results)
        elif x == 3:
            run_greedy_experiment(model_greedy, "model greedy", "results_model_greedy", pdf_tex_files_dir, dir_to_results, load_models())
        elif x == 4:
            run_greedy_experiment(non_stop_classification_greedy, "non stop classification greedy", "non_stop_results_classification_greedy", pdf_tex_files_dir, dir_to_results, load_models())
        elif x == 5:
            run_greedy_experiment(regreession_model_greedy, "regreession model greedy", "results_regreession_model_greedy", pdf_tex_files_dir, dir_to_results, load_regression_models_cat())
        elif x == 6:
            run_greedy_experiment(non_stop_regreession_model_greedy, "non stop regreession model greedy", "results_non_stop_regreession_model_greedy", pdf_tex_files_dir, dir_to_results, load_regression_models_cat())
