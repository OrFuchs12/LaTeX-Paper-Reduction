import os
import pickle
import subprocess
import time
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

NUMBER_OF_LAST_PAGES = 2

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
    lst[index_1] = lst[index_1].replace("\n", " ") + lst.pop(index_2)
    return lst


def perform_operators(objects, doc_index, latex_path, pdf_path,path_to_file):  # ,path_to_file):


    lidor = convert_Latex_to_rows_list(latex_path, pdf_path)
    # lidor = []
    latex_clean_lines = []
    with open(latex_path, encoding='UTF-8') as f:
        file = f.read()
        file = file.split("\n")
        # foundHeader=False
        # foundBottom=False
        for line in file:
            line = line.lstrip()
            line += "\n"
            latex_clean_lines.append(line)
            # if foundHeader==False:
            #     if line.startswith("\\begin{document}"):
            #         foundHeader=True
            #     lidor.append("\n")
            # else:
            #     if foundBottom==False and line.startswith("\\end{document}"):
            #         foundBottom=True
            #     elif foundBottom == False and line == "":
            #         lidor.append("\n")
            #     else:
            #         if foundBottom==False:
            #             lidor.append(line)

    
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
                object_name_key_new_latex_list_value[key] = (new_list_2, 11, 0)

        if (key.startswith('Table')):
            chosen_index_to_insert = mapping_dict[key][0]  # index where the figure starts
            flag = False
            index_to_go_through = chosen_index_to_insert
            while (flag != True):
                if (index_to_go_through > len(latex_clean_lines)):
                    break
                if (latex_clean_lines[index_to_go_through].startswith(
                        '\\begin{adjustbox}')):  # finding the line where we can change the scale of the figure
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
                    heuristic = 0
                elif (i == 1):
                    heuristic = value['height'] * 0.1111
                elif (i == 2):
                    heuristic = value['height'] * 0.2222
                elif (i == 3):
                    heuristic = value['height'] * 0.3333
                new_width = options[i]
                new_str = string_to_edit.replace(str(width), str(new_width))
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
                object_name_key_new_latex_list_value[key] = (new_list_2, 4, 0)

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
                        width = float(number)
                        break
                    running_index += 1
            start_index = string_to_edit.find('height')
            running_index = 0
            if (start_index != -1):  # find the number for height
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
                        height = float(number)
                        break
                    running_index += 1
            # create 5 options:
            options = [0.9, 0.8, 0.7, 0.6, 0.5]  # scale options
            figure_name_key_new_latex_list_value[
                key] = []  # this dict will have the key as the figure name and then value will be the lists of the new latex content for the new file
            string_to_edit = latex_clean_lines[found_index]  # the string to edit
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
                object_name_key_new_latex_list_value[key] = (new_list_2, 2, 0)

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
        latex_string = ''.join(latex_clean_lines)
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

    for key, value in object_name_key_new_latex_list_value.items():
        x_list = value[0]
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', key)[0]
        operators_dict.append(
            (value[2], latex_string, 8, 1, value[1], num_of_object))  # type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for key, value in dict_for_removing_last_2_words_operator.items():
        x_list = value[0]
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', key)[0]
        operators_dict.append(
            (value[2], latex_string, 9, 1, value[1], num_of_object))  # type, value, object_used_on, num_of_object
        index_for_all_operators += 1


    return sorted(operators_dict, key=lambda x: x[0])  # , reverse=True) #remove reversedd



""" 
    This function return the number of lines in the last page of pdf file, parameters:
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
def simple_greedy(path_to_pdf, path_to_latex):
    try:
        operators_done = []
        #perform feature extraction to the file
        # extract_name= path_to_pdf.split("/")[-1].split(".")[0]
        # remove_comments(path_to_latex)
            
        # new_path= "new.pdf"
        # copy_last_pages(path_to_pdf, new_path, 2)
        features_single.run_feature_extraction(path_to_latex, path_to_pdf, '/code/greedy_from_machine/bibliography.bib',
                                                    "code/~/results/dct0",
                                                    "~/results/new_files/dct0", "test", pd.DataFrame())
        lines, pages = check_lines(path_to_pdf)

        #check whether the file is not good for the algorithm:
        if lines < 2:
            print("Less then 2 lines")
            return -1, -1, False, -1
        if pages < 2:
            print("Less then 2 pages")
            return -1, -1, False, -1
        
        # define stop condition and some variables
        target = lines - 2
        index = 0
        reduced = False
        iteration = 0
        total_cost = 0

        print("begin lines:", lines)
        print("begin pages:", pages)
        start = time.time()
        while (lines > target and pages > 1):
            print("index:", index)
            # get the dictionary of the file
            with open('code/~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)

            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, path_to_pdf ,"~/results/new_files/")
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)):
                print("Out of operators")
                break

            if str(res[index][2]) == '1':
                oper = (str(res[index][2]), str(res[index][3]), str(res[index][4]), res[index][5])
            else:
                oper = (str(res[index][2]), str(res[index][3]), res[index][5])

            # whether we applied the operator before
            if oper in operators_done:
                index += 1
                continue
            else:
                operators_done.append(oper)

            latex_after_operator = res[index][1]
            # write the file after operator to file
            f = open("code/~/results/new_files/after_operator1.tex", "w")
            f.write(latex_after_operator)
            f.close()

            # compile the file
            # cmd_line_act = 'tectonic -X compile ' + "code/~/results/new_files/after_operator1.tex"
            dir_path = "code/~/results/new_files"
            base_name = os.path.basename("code/~/results/new_files/after_operator1.tex")
            # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
            subprocess.run(['pdflatex', base_name], cwd=dir_path) #On mac
            last_pages_pdf = copy_last_pages(path_to_pdf, NUMBER_OF_LAST_PAGES)
            
            
            # os.system(cmd_line_act)

            lines_before = lines
            # check the new current number of lines
            lines, pages = check_lines(last_pages_pdf)
            fullLines , fullPages = check_lines("code/~/results/new_files/after_operator1.pdf")
            print("current lines:", fullLines)
            print("current pages:", fullPages)

            path_to_latex = "code/~/results/new_files/after_operator1.tex"

            features_single.run_feature_extraction("code/~/results/new_files/after_operator1.tex", 
                    last_pages_pdf, '~/results/bibliography.bib',
                    "code/~/results/dct0", "~/results/new_files/dct0", "test", pd.DataFrame())

            total_cost += res[index][0]
            index += 1
            iteration += 1

            # if we manage to short the paper
            if (lines <= target or pages < 2):
                reduced = True

        end = time.time()

        return iteration, end - start, reduced, total_cost
    except Exception as e:
        print(e)
        return -1, -1, reduced, -1


""" 
    This is a heuristic algorithm based on the heuristic, parameters:
    path_to_pdf - path to the pdf file 
    path_to_latex - path to the latex file 
"""
def heuristic_greedy(path_to_pdf, path_to_latex):
    try:
        operators_done = []
        #perform feature extraction to the file
        features_single.run_feature_extraction(path_to_latex, path_to_pdf, 'code/greedy_from_machine/bibliography.bib',
                                                    "~/results/dct0",
                                                    "~/results/new_files/dct0", "test", pd.DataFrame())
        lines, pages = check_lines(path_to_pdf)
        #check whether the file is not good for the algorithm:
        if lines < 2:
            print("Less then 2 lines")
            return -1, -1, False, -1
        if pages < 2:
            print("Less then 2 pages")
            return -1, -1, False, -1
        
        # define stop condition and some variables
        target = lines - 2
        index = 0
        reduced = False
        iteration = 0
        LINE_WIDTH = 10
        total_cost = 0
        print("begin lines:", lines)
        print("begin pages:", pages)
        start = time.time()
        while (lines > target and pages > 1):
            print("index:", index)
            # get the dictionary of the file
            with open('~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)
            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, "~/results/new_files/")
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)):
                print("Out of operators")
                break

            if str(res[index][2]) == '1':
                oper = (str(res[index][2]), str(res[index][3]), str(res[index][4]), res[index][5])
            else:
                oper = (str(res[index][2]), str(res[index][3]), res[index][5])

            # whether we applied the operator before
            if oper in operators_done:
                index += 1
                continue
            else:
                operators_done.append(oper)

            # condition to apply the operator
            if res[index][0] >= LINE_WIDTH:
                latex_after_operator = res[index][1]
                # write the file after operator to file
                f = open("~/results/new_files/after_operator2.tex", "w")
                f.write(latex_after_operator)
                f.close()

                # compile the file
                cmd_line_act = 'tectonic -X compile ' + "~/results/new_files/after_operator2.tex"
                os.system(cmd_line_act)

                lines_before = lines
                # check the new current number of lines
                lines, pages = check_lines("~/results/new_files/after_operator2.pdf")
                print("current lines:", lines)
                print("current pages:", pages)

                path_to_latex = "~/results/new_files/after_operator2.tex"

                features_single.run_feature_extraction("~/results/new_files/after_operator2.tex", 
                    "~/results/new_files/after_operator2.pdf", '~/results/bibliography.bib',
                    "~/results/dct0", "~/results/new_files/dct0", "test", pd.DataFrame())

                iteration += 1
                total_cost += res[index][0]
                index += 1

                # if we manage to short the paper
                if (lines <= target or pages < 2):
                    reduced = True

            else:
                index += 1

        end = time.time()
        return iteration, end - start, reduced, total_cost
    except Exception as e:
        print(e)
        return -1, -1, reduced, -1


"""
    This function load the models and stores them in dictionary, parameters:
    models_path - path to the models directory (string)
"""
def load_models(models_path):
    # Load models
    models = {}
    directory = models_path
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


""" 
    This is a greedy algorithm based on the models, parameters:
    path_to_pdf - path to the pdf file 
    path_to_latex - path to the latex file 
    models - dict of models (dictionary) 
"""
def model_greedy(path_to_pdf, path_to_latex, models):
    try:
        operators_done = []
        lines, pages = check_lines(path_to_pdf) 

        #check whether the file is not good for the algorithm:
        if lines < 2:
            print("Less then 2 lines")
            return -1, -1, False, -1
        if pages < 2:
            print("Less then 2 pages")
            return -1, -1, False, -1

        #perform feature extraction to the file
        df1 = features_single.run_feature_extraction(path_to_latex, path_to_pdf, 'code/greedy_from_machine/bibliography.bib',
                                                        "~/results/dct0",
                                                        "~/results/new_files/dct0", "test",
                                                        pd.DataFrame())
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                    'num_of_object'], axis=1, inplace=True)

        # define stop condition and some variables
        target = lines - 2
        index = 0
        reduced = False
        iteration = 0
        total_cost = 0

        print("begin lines:", lines)
        print("begin pages:", pages)

        start = time.time()
        while (lines > target and pages > 1):

            print("index:", index)

            # get the dictionary of the file
            with open('~/results/dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)

            # get list of all possible operators to apply on the file
            res = perform_operators(dct, 0, path_to_latex, "~/results/new_files/")
            print("total operators:", len(res))

            # whether there are no more operators
            if index >= (len(res)):
                print("Out of operators")
                break

            if str(res[index][2]) == '1':
                model_to_predict = (str(res[index][2]), str(res[index][3]), str(res[index][4]), res[index][5])
            else:
                model_to_predict = (str(res[index][2]), str(res[index][3]), res[index][5])

            # whether we applied the operator before
            if model_to_predict in operators_done:
                index += 1
                continue
            else:
                operators_done.append(model_to_predict)

            print("model_to_predict:", model_to_predict)

            try:
                # get the prediction from the model
                prediction = models[model_to_predict].predict(df1.to_numpy())[0]

            except Exception as e:
                print("not found model:", e)
                index += 1
                continue

            # condition to apply the operator
            if prediction > 0 and res[index][0] >= 10:
                latex_after_operator = res[index][1]

                f = open("~/results/new_files/after_operator3.tex", "w")
                # write the file after operator to file
                f.write(latex_after_operator)
                f.close()

                # compile the file
                cmd_line_act = 'tectonic -X compile ' + "~/results/new_files/after_operator3.tex"
                os.system(cmd_line_act)

                lines_before = lines
                # check the new current number of lines
                lines, pages = check_lines("~/results/new_files/after_operator3.pdf")
                print("current lines:", lines)
                print("current pages:", pages)

                path_to_latex = "/results/new_files/after_operator3.tex"

                df1 = features_single.run_feature_extraction(
                    "~/results/new_files/after_operator3.tex",
                    "~/results/new_files/after_operator3.pdf", '~/results/bibliography.bib',
                    "~/results/dct0", "~/results/new_files/dct0", "test",
                    pd.DataFrame())
                df1 = df1.T
                df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                            'num_of_object'], axis=1, inplace=True)

                total_cost += res[index][0]
                index += 1
                iteration += 1
                
                # if we manage to short the paper
                if (lines <= target or pages < 2):
                    reduced = True
            else:
                index += 1

        end = time.time()

        return iteration, end - start, reduced, total_cost
    except Exception as e:
        print(e)
        return -1, -1, reduced, -1


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
    names = []
    directory = files_dir
    for file in os.scandir(directory):
        if file.is_file():
            # uncomment this 2 lines if you don't have the pdfs
            # cmd_line_act = '"C:\\Users\\user\\tectonic.exe" ' + f"{directory}\\{file.name}"
            # os.system(cmd_line_act)
            names.append(file.name.split('.')[0])

    results = []
    idx = 0
    done = 1

    # iterate all the files in the directory
    for filename in set(names):
        print(f"file in test {idx}:", filename)
        idx += 1
        try:
            # get the full pdf path of the file
            file_path = os.path.join(directory, filename + ".pdf")
            if os.path.isfile(file_path):
                path_to_pdf = file_path
                last_pages_pdf_path = copy_last_pages(path_to_pdf,NUMBER_OF_LAST_PAGES )
            
            # get the full latex path of the file
            file_path = os.path.join(directory, filename + ".tex")
            if os.path.isfile(file_path):
                path_to_latex = file_path
                remove_comments(path_to_latex)


            # whether you want to run the model-based greedy algorithm
            if models: 
                iterations, time_taken, reduced, cost = variant_function(last_pages_pdf_path, path_to_latex, models)

            # whether you want to run other greedy algorithms
            else: 
                iterations, time_taken, reduced, cost = variant_function(last_pages_pdf_path, path_to_latex)

            if iterations != -1:
                results.append((filename, variant_name, reduced, iterations, time_taken, cost))

                # write the results every document finished (just in case)
                df = pd.DataFrame(results, columns=["Name", "Algorithm", "Reduced", "Iterations", "Time", "Cost"])
                df.to_csv(f'{results_dir}/{variant_file_name}.csv', index=False)

                print("Done!", done)
                done += 1

        except Exception as e:
            print(e)

    # write the final results
    df = pd.DataFrame(results, columns=["Name", "Algorithm", "Reduced", "Iterations", "Time", "Cost"])
    df.to_csv(f'{results_dir}/{variant_file_name}.csv', index=False)  # change here


if __name__ == "__main__":

    # get all the inputs from the script:
    x=int(sys.argv[1])
    pdf_tex_files_dir=sys.argv[2]
    dir_to_results=sys.argv[3]
    path_to_models=sys.argv[4]

    # How to select algorithm type:
    #0 -> simple greedy algorithm.
    #1 -> heuristic greedy algorithm.
    #2 -> model greedy algorithm.
    if x==0:  
        run_greedy_experiment(simple_greedy, "simple greedy", "results_simple_greedy", pdf_tex_files_dir, dir_to_results)
    elif x==1:
        run_greedy_experiment(heuristic_greedy, "heuristic greedy", "results_heuristic_greedy", pdf_tex_files_dir, dir_to_results)
    elif x==2:
        run_greedy_experiment(model_greedy, "model greedy", "results_model_greedy", pdf_tex_files_dir, dir_to_results, load_models(path_to_models))
