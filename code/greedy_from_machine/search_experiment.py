import os
import pickle
import time
#import perry
import perry
import perry2
import PyPDF2
import sys
from itertools import islice
import copy
import re
import feature_extraction
#sys.path.insert(1, 'pdf_extraction\\adi_comparing\\')
#import feature_extraction

import features_single
import pandas as pd
import time
import xgboost as xg

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
    for i in reversed(range(index+1)):
        if '\\paragraph' in lst[i]:
            return True
        elif lst[i] == '\n':
            continue
        else:
            return False


def combine_two_paragraphs(lst, index_1, index_2):
    lst[index_1] = lst[index_1].replace("\n", " ") + lst.pop(index_2)
    return lst



def perform_operators(objects,doc_index,latex_path, path_to_file): #,path_to_file):
    
    with open(latex_path, encoding='UTF-8') as file:
        lidor=[]
        # doc = file.read()
        latex_clean_lines = []
        with open(latex_path, encoding='UTF-8') as file:
            # doc = file.read()

            foundHeader = False
            foundBottom = False
            for line in file:
                latex_clean_lines.append(line)
                if foundHeader == False:
                    if line.startswith("\\begin{document}"):
                        foundHeader = True
                    lidor.append("\n")
                else:
                    if foundBottom == False and line.startswith("\\end{document}"):
                        foundBottom = True
                    else:
                        if foundBottom == False:
                            lidor.append(line)

    #print(latex_clean_lines)
    #trying vspace
    #latex_clean_lines = Lidor_part.read_file(latex_path, bib_path)
    # latex_clean_lines = base_doc
    # for k in lidor:
    #     #print(k)
    # #print(lidor)
    #print(latex_clean_lines)
    list_of_starts,tags = perry2.parse2_lidor(latex_path, lidor) #perry.parse2_lidor(latex_path, lidor)
    ##print("PERRY-----------------------------------------------------------------------")
    #list_of_starts = list_of_starts[1:]
    #latex_clean_lines = latex_clean_lines[1:]
    #print(list_of_starts)
    #print(tags)
    #print(list_of_starts)
    #print(latex_clean_lines[29])
    # ##print(latex_clean_lines[60])
    # #print(list_of_starts)
    # #print(tags)
    # x = get_list_of_locations.run(latex_path)
    # #print(x)
    # #print(base_doc[80])
    # #print(base_doc[81])
    # #print(base_doc[88])

    index_for_object = {'Par':1,'Figure':2,'CaptionFigure':3,'Table':4,'CaptionTable':5,'Section':6,'SubSection':7,'Matrix':8,'Enum':9,'Formula':10,'Algorithm':11}
    #mapping:
    mapping_dict ={}
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
    figure_index=0
    table_index=0
    # print(tags)
    # print(list_of_starts)
    for i in range(len(list_of_starts)):
        #print(i)
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
        elif(tags[i][0][0] == 'CaptionFigure'):
            caption_index+=1
            index=caption_index
        elif(tags[i][0][0] == 'CaptionTable'):
            caption_table_index+=1
            index = caption_table_index
        elif(tags[i][0][0] == 'Formula'):
            formula_index+=1
            index = formula_index
        elif (tags[i][0][0] == 'Paragraph'):
            paragraph_index += 1
            index = paragraph_index
        else:
            undetected_index += 1
            index = undetected_index
        if (tags[i][0][0] == 'Figure'):
            # print(tags[i][0][0])
            # print(str(tags[i][1]))
            mapping_dict[tags[i][0][0] + str(tags[i][0][1])] = (list_of_starts[i], latex_clean_lines[list_of_starts[i]])
        elif (tags[i][0][0] == 'Table'):
            mapping_dict[tags[i][0][0] + str(int(tags[i][0][1]) + 1)] = (
            list_of_starts[i], latex_clean_lines[list_of_starts[i]])
        else:
            ##print(str(index))
            #print(tags[i][0][0])
            mapping_dict[tags[i][0][0] + str(index)] = (list_of_starts[i], latex_clean_lines[list_of_starts[i]])

    # for i in objects:
    #     print(f'{i}' ':' f'{objects[i]}')
    # for i in mapping_dict:
    #     print(f'{i}' ':' f'{mapping_dict[i]}')
    
    #we are taking into a account that latex and pdf may be ordered differently

    # print(objects)
    ##print(summative_features)
    indexer = 0
    object_to_add_vspace_behind = 0
    #print(latex_clean_lines)
    #latex_clean_lines = latex_clean_lines[1:]
    arr_of_places_and_vspace_to_add = []
    figure_name_key_new_latex_list_value = {}
    table_name_key_new_latex_list_value = {}
    object_name_key_new_latex_list_value = {} #for removing special positioning chars
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

    for key,value in objects.items(): #in this loop we will make all the operators

        if(key.startswith('CaptionTable')):
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

        if(key.startswith('CaptionFigure')):
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

        if(key.startswith('Paragraph')):
            chosen_index_to_insert = mapping_dict[key][0]
            new_list = copy.deepcopy(latex_clean_lines)
            if is_par(new_list, chosen_index_to_insert):  # remove tag of paragraph operator
                seen_paragraph = False
                for i in reversed(range(chosen_index_to_insert+1)):
                    if '\\paragraph' in new_list[i]:
                        tag = new_list.pop(i)
                        temp = tag[tag.find("{") + 1:tag.find("}")]
                        temp = "\\textbf{" + temp + "} "
                        new_list[i] = temp + new_list[i]
                        break
                if(value['last_line_length_words'] == 1):
                    par_remove_list.append((new_list, key,10))
                else:
                    par_remove_list.append((new_list,key,0))

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
                    combined_paragraphs_list.append((new_list,key,10))
                    pair_to_check.clear()
                    pair_to_check.append(key)
                    previous_par_index = chosen_index_to_insert
            else:
                seen_paragraph = True
                pair_to_check.append(key)
                previous_par_index = chosen_index_to_insert

            #remove last 2 words if the sentence end with 1 word
            if(value['last_line_length_words'] == 1):
                #remove last 2 words
                chosen_index_to_insert = mapping_dict[key][0]
                new_list_2 = copy.deepcopy(latex_clean_lines)
                if (new_list_2[chosen_index_to_insert][-1] == '\n'):  # remember that the par ends that way
                    new_part_last = new_list_2[chosen_index_to_insert][:len(new_list_2[chosen_index_to_insert]) - 1]
                    new_part_last_2 = new_part_last.rsplit(' ', 2)[0] #remove last 2 words
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
                if(new_list[i].startswith('\\end{algorithmic}')):
                    start_counting = False
                    break
                if(start_counting):
                    counter_lines += 1
                if(new_list[i].startswith('\\begin{algorithmic}')):
                    start_counting = True

            new_list.insert(chosen_index_to_insert + 1, "\\small\n")
            heuristic = counter_lines * 0.77
            algorithm_list.append((new_list, key, heuristic))

        #another operator for algorithm, remove special postion letter:
            new_list_2 = copy.deepcopy(latex_clean_lines)
            string_to_edit = new_list_2[chosen_index_to_insert]
            index_to_edit = string_to_edit.find('[')
            if(index_to_edit != -1): #there is a special positional char
                new_string_to_edit = re.sub("[\(\[].*?[\)\]]", "", string_to_edit)
                new_list_2[chosen_index_to_insert] = new_string_to_edit
                object_name_key_new_latex_list_value[key] = (new_list_2,11,0)



        if(key.startswith('Table')):
            chosen_index_to_insert = mapping_dict[key][0]  # index where the figure starts
            flag = False
            index_to_go_through = chosen_index_to_insert
            while (flag != True):
                if (index_to_go_through > len(latex_clean_lines)):
                    break
                if (latex_clean_lines[index_to_go_through].startswith('\\begin{adjustbox}')):  # finding the line where we can change the scale of the figure
                    found_index = index_to_go_through
                    flag = True
                else:
                    index_to_go_through += 1
            if (flag == False):
                continue
            # now we will shrink the figure to the 5 options of shrinking:
            # we will first find the places and then add the values based on the scale
            #print(found_index)
            #print(latex_clean_lines[found_index])
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
            #print(width)
            options = [0.9, 0.8, 0.7, 0.6]  # scale options
            table_name_key_new_latex_list_value[key] = []  # this dict will have the key as the table name and then value will be the lists of the new latex content for the new file
            string_to_edit = latex_clean_lines[found_index]  # the string to edit
            heuristic = 0
            for i in range(4):
                if(i == 0):
                    heuristic = 0
                elif(i == 1):
                    heuristic = value['height'] * 0.1111
                elif(i ==2):
                    heuristic = value['height'] * 0.2222
                elif(i==3):
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
            #print(found_index)
            #print(latex_clean_lines[found_index])
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
            #print(width)
            #print(height)
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

        if(indexer == 0): #in this if we wanted to skip the first object for the vspace but we need the first element for the other operators.
            indexer+=1
            continue
        # else:
        #     #print(value['space_between_this_object_and_last_object'])
        #     if(value['space_between_this_object_and_last_object'] > 10): #candidate to add vspace
        #         #object_to_add_vspace_behind = key
        #         #print()
        #         #print(mapping_dict[key])
        #         chosen_index_to_insert = mapping_dict[key][0]
        #         if('Formula' in key):
        #             #we will make 3 partitions:
        #             vspace_size_max = value['space_between_this_object_and_last_object'] / 7
        #             herustica = 0
        #             vspace_size_part = vspace_size_max/4
        #             for i in range(1,5):
        #                 #print("Part " + str(i) + " :")
        #                 herustica = (value['space_between_this_object_and_last_object']*i) /4
        #                 vspace_size = "{:.2f}".format(vspace_size_part*i)
        #                 #print("vspace size: " + str(vspace_size))
        #                 #latex_clean_lines.insert(chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n')
        #                 for i in index_for_object.keys():
        #                     if(key.startswith(i)):
        #                         num = index_for_object[i]
        #                 arr_of_places_and_vspace_to_add.append((chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n',num,vspace_size,key,herustica))
        #                 offset += 1
        #         else:
        #             vspace_size_max = value['space_between_this_object_and_last_object']/3.5
        #             vspace_size_part = vspace_size_max / 4
        #             for i in range(1, 5):
        #                 #print("Part " + str(i) + " :")
        #                 herustica = (value['space_between_this_object_and_last_object'] * i) / 4
        #                 vspace_size = "{:.2f}".format(vspace_size_part * i)
        #                 #print("vspace size: " + str(vspace_size))
        #                 # latex_clean_lines.insert(chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n')
        #                 for i in index_for_object.keys():
        #                     if(key.startswith(i)):
        #                         num = index_for_object[i]
        #                 arr_of_places_and_vspace_to_add.append((chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n', num, vspace_size,key,herustica))
        #                 offset += 1




    
    #we will create a new doc with each vspace addition:
    # print(figure_name_key_new_latex_list_value)
    # for i in figure_name_key_new_latex_list_value:
    #     print(f'{i}' ':' f'{figure_name_key_new_latex_list_value[i]}')
    new_clean_latex_to_remember = copy.deepcopy(latex_clean_lines)
    #we will make changes to latex_clean_lines and then clean it with new_clean_latex_to_remember
    files_created = []
    operators_dict = []
    index_for_all_operators = 1
    # for i in range(len(arr_of_places_and_vspace_to_add)):
    #     ##print("clean: ")
    #     ##print(new_clean_latex_to_remember)
    #     latex_clean_lines = []
    #     latex_clean_lines = copy.deepcopy(new_clean_latex_to_remember)
    #     #f = open(path_to_file +str(doc_index)+str(index_for_all_operators)+".tex","w")
    #     # files_created.append((path_to_file +str(doc_index)+str(index_for_all_operators)+".tex",
    #     #                       path_to_file +str(doc_index)+str(index_for_all_operators)+".pdf",
    #     #                       arr_of_places_and_vspace_to_add[i][2],
    #     #                       'vspace',
    #     #                       arr_of_places_and_vspace_to_add[i][3],
    #     #                       arr_of_places_and_vspace_to_add[i][4], arr_of_places_and_vspace_to_add[i][5])) # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key-num_of_object_used_on)]
    #     chosen_index_to_insert = arr_of_places_and_vspace_to_add[i][0]
    #     str__ = arr_of_places_and_vspace_to_add[i][1]
    #     latex_clean_lines.insert(chosen_index_to_insert,str__)
    #     latex_clean_lines = latex_clean_lines#[1:]
    #     #print(latex_clean_lines)
    #     #for item in latex_clean_lines:
    #         # write each item on a new line
    #         #f.write(item)
        
    #     latex_string = ''.join(latex_clean_lines)
    #     operators_dict.append((arr_of_places_and_vspace_to_add[i][5], latex_string))
    #     #f.write(latex_string)
    #     index_for_all_operators+=1

    # here we will create the new files for figure changes
    options = [0.9, 0.8, 0.7, 0.6, 0.5]
    for key,value in figure_name_key_new_latex_list_value.items():
        for i in range(5):
            #f = open(path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex", "w")
            # files_created.append((path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex", path_to_file + str(doc_index) + str(index_for_all_operators) + ".pdf",
            #                       2, 'change_figure_size',  options[i],key,value[i][1]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key-num_of_object_used_on)]
            x_list = value[i][0]#[1:]
            #print(x_list)
            #for item in x_list:
                # write each item on a new line
                #f.write(item)
            #f.close()
            #print(x_list)
            #print(value[i][1])
            latex_string = ''.join(x_list)
            #print(latex_string)
            num_of_object = re.findall('\d+', key)[0]
            operators_dict.append((value[i][1], latex_string, 2, options[i], 2, num_of_object)) #type, value, object_used_on, num_of_object

            #print('Done')
            index_for_all_operators += 1

    #create new files for table changes
    options = [0.9, 0.8, 0.7, 0.6]
    for key, value in table_name_key_new_latex_list_value.items():
        #print(index_for_all_operators)
        for i in range(4):
            #f = open(path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex", "w")
            # files_created.append((path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex",
            #                       path_to_file + str(doc_index) + str(index_for_all_operators) + ".pdf",
            #                       4, 'change_table_size',
            #                       options[i], key, value[i][1]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key,num_of_object_used_on)]
            x_list = value[i][0]#[1:]
            #print(value[i][1])
            #print(x_list)
            #for item in x_list:
                # write each item on a new line
                #f.write(item)
            #f.close()
            #print('Done')
            latex_string = ''.join(x_list)
            num_of_object = re.findall('\d+', key)[0]
            
            operators_dict.append((value[i][1], latex_string, 7, options[i], 4, num_of_object)) #type, value, object_used_on, num_of_object

            index_for_all_operators += 1

    for al in algorithm_list:
        #f = open(path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex", "w")
        # files_created.append((path_to_file + str(doc_index) + str(
        #     index_for_all_operators) + ".tex", path_to_file + str(doc_index) + str(
        #     index_for_all_operators) + ".pdf",
        #                       11, 'change_algorithm_size',
        #                       1, al[1], al[2]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key-num_of_object_used_on)]

        x_list = al[0]#[1:]
        #print(x_list)

        #for item in x_list:
            # write each item on a new line
            #f.write(item)
        #f.close()
        #print('Done')
        latex_string = ''.join(x_list)
        #print(al[2])
        num_of_object = re.findall('\d+', al[1])[0]
        
        operators_dict.append((al[2], latex_string, 3, 1, 11, num_of_object)) #type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for enum in enum_list:
        #print(enum)
        #f = open(path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex", "w")
        # files_created.append((path_to_file + str(doc_index) + str(
        #     index_for_all_operators) + ".tex", path_to_file + str(doc_index) + str(
        #     index_for_all_operators) + ".pdf",
        #                       9, 'convert_enum',
        #                       1, enum[1], enum[2]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key-num_of_object_used_on)]

        x_list = enum[0]#[1:]
        #print(x_list)

        #for item in x_list:
            # write each item on a new line
            #f.write(item)
        #f.close()
        #print('Done')
        latex_string = ''.join(x_list)
        #print(enum[2])
        num_of_object = re.findall('\d+', enum[1])[0]
        operators_dict.append((enum[2], latex_string, 4, 1, 9, num_of_object)) #type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for par in par_remove_list:
        #f = open(path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex","w")
        # files_created.append((path_to_file + str(doc_index) + str(
        #     index_for_all_operators) + ".tex", path_to_file + str(doc_index) + str(
        #     index_for_all_operators) + ".pdf",
        #                       1, 'remove_par_tag',
        #                       1, par[1], par[2]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key-num_of_object_used_on)]

        x_list = par[0]#[1:]
        #print(x_list)

        #for item in x_list:
            # write each item on a new line
            #f.write(item)
        #f.close()
        #print('Done')
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', par[1])[0]
        operators_dict.append((par[2], latex_string, 5, 1, 1, num_of_object)) #type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for par in combined_paragraphs_list:
        #f = open(path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex", "w")
        # files_created.append((path_to_file + str(doc_index) + str(
        #     index_for_all_operators) + ".tex",
        #                       path_to_file + str(doc_index) + str(
        #                           index_for_all_operators) + ".pdf",
        #                       1, 'combine_two_paragraphs',
        #                       1, par[1], par[2]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key-num_of_object_used_on)]

        x_list = par[0]#[1:]
        #print(x_list)

        #for item in x_list:
            # write each item on a new line
           # f.write(item)
        #f.close()
        #print('Done')
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', par[1])[0]
        operators_dict.append((par[2], latex_string, 6, 1, 1, num_of_object)) #type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for key,value in object_name_key_new_latex_list_value.items():
        #f = open(path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex", "w")
        # files_created.append((path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex",
        #                       path_to_file + str(doc_index) + str(index_for_all_operators) + ".pdf",
        #                       value[1], 'remove_special_positional_chars',
        #                       1,
        #                       key, value[2]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key-num_of_object_used_on)]
        x_list = value[0]#[1:]
        #print(x_list)
        #for item in x_list:
            # write each item on a new line
            #f.write(item)
        #f.close()
        #print('Done')
        #print(value[2])
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', key)[0]
        operators_dict.append((value[2], latex_string, 8, 1, value[1], num_of_object)) #type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    for key,value in dict_for_removing_last_2_words_operator.items():
        #f = open(path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex", "w")
        # files_created.append((path_to_file + str(doc_index) + str(index_for_all_operators) + ".tex",
        #                       path_to_file + str(doc_index) + str(index_for_all_operators) + ".pdf",
        #                       value[1], 'remove_last_2_words',
        #                       1,
        #                       key,value[2]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value,key-num_of_object_used_on)]
        x_list = value[0]#[1:]
        #print(x_list)
        #for item in x_list:
            # write each item on a new line
           # f.write(item)
       # f.close()
        #print('Done')
        #print(value[2])
        latex_string = ''.join(x_list)
        num_of_object = re.findall('\d+', key)[0]
        #print(num_of_object)
        operators_dict.append((value[2], latex_string, 9, 1, value[1], num_of_object)) #type, value, object_used_on, num_of_object
        index_for_all_operators += 1

    #print(files_created)
    return sorted(operators_dict, key=lambda x: x[0])#, reverse=True) #remove reversedd


# def check_lines(file_path):
#     # Open the PDF file
#     with open(file_path, 'rb') as file:
#         pdf = PyPDF2.PdfFileReader(file)
#         # Get the number of pages in the PDF
#         pages = pdf.getNumPages()
#         # Initialize a variable to store the total number of lines
#         total_lines = 0
#         # Iterate through each page in the PDF
#         for page in range(pages):
#             # Get the current page
#             current_page = pdf.getPage(page)
#             # Extract the text from the current page
#             text = current_page.extractText()
#             # Split the text into lines
#             lines = text.split('\n')
#             # Add the number of lines in the current page to the total
#             total_lines += len(lines)
#         # Check if the number of lines decreased
#         return total_lines



#def get_prediction():













def check_lines(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        pdf = PyPDF2.PdfFileReader(file)
        # Get the number of pages in the PDF
        pages = pdf.getNumPages()
        # Get the last page
        last_page = pdf.getPage(pages-1)
        # Extract the text from the last page
        text = last_page.extractText()
        # Split the text into lines
        lines = text.split('\n')
        # Print the number of lines in the last page
        #print("The number of lines in the last page is:", len(lines))
        return len(lines), pages


# Example usage:
# print(check_lines("pdf-tests\\5067_1.pdf"))

def simple_greedy(path_to_pdf, path_to_latex):
    
    try:
        features_single.run_feature_extraction(path_to_latex,path_to_pdf,'pdf-tests\\bibliography.bib',"pdf_extraction\\adi_comparing\\dct0", "pdf_extraction\\adi_comparing\\new_files\\dct0", "test", pd.DataFrame())

        lines, pages = check_lines(path_to_pdf)

        if lines < 2:
            print("Less then 2 lines")
            return -1,-1,False,-1
        if pages < 2:
            print("Less then 2 pages")
            return -1,-1,False, -1
        target = lines - 2 
        index = 0
        reduced = False
        iteration = 0
        total_cost = 0

        print("begin lines:", lines)
        print("begin pages:", pages)

        start = time.time()
        while(lines > target and pages > 1):
            
            print("index:", index)
            with open('pdf_extraction\\adi_comparing\\dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)

            
            res = perform_operators(dct, 0, path_to_latex, "pdf_extraction\\adi_comparing\\new_files\\")
            print("total operators:", len(res))
            if index >= (len(res)):
                print("Out of operators")
                break
            latex_after_operator = res[index][1]

            f = open("pdf_extraction\\adi_comparing\\new_files\\after_operator.tex", "w")
            f.write(latex_after_operator)
            f.close()

            cmd_line_act = '"C:\\Users\\user\\tectonic.exe" ' + "pdf_extraction\\adi_comparing\\new_files\\after_operator.tex"
            os.system(cmd_line_act)
            #time.sleep(1)

            lines_before = lines
            lines, pages = check_lines("pdf_extraction\\adi_comparing\\new_files\\after_operator.pdf")
            print("current lines:", lines)
            print("current pages:", pages)
            
           
            path_to_latex = "pdf_extraction\\adi_comparing\\new_files\\after_operator.tex"
            
            #feature_extraction.run_feature_extraction(["pdf_extraction\\adi_comparing\\new_files\\after_operator"],["pdf_extraction\\adi_comparing\\new_files\\after_operator"],['bibliography'])
            features_single.run_feature_extraction("pdf_extraction\\adi_comparing\\new_files\\after_operator.tex","pdf_extraction\\adi_comparing\\new_files\\after_operator.pdf",'pdf-tests\\bibliography.bib',"pdf_extraction\\adi_comparing\\dct0", "pdf_extraction\\adi_comparing\\new_files\\dct0", "test", pd.DataFrame())
            
            total_cost += res[index][0]
            index+=1
            iteration += 1
            

            # if(lines_before <= lines):
            #     index+=1
            # if lines_before > lines:
            #     index = 0
            
            if(lines <= target or pages < 2):
                reduced = True

        
        end = time.time()

        return iteration, end-start, reduced, total_cost
    except Exception as e:
        print(e)
        return -1, -1, reduced, -1



def heuristic_greedy(path_to_pdf, path_to_latex):
    try:
        features_single.run_feature_extraction(path_to_latex,path_to_pdf,'pdf-tests\\bibliography.bib',"pdf_extraction\\adi_comparing\\dct0", "pdf_extraction\\adi_comparing\\new_files\\dct0", "test", pd.DataFrame())
        lines, pages = check_lines(path_to_pdf)

        if lines < 2:
            print("Less then 2 lines")
            return -1,-1,False, -1
        if pages < 2:
            print("Less then 2 pages")
            return -1,-1,False,-1
        target = lines - 2 
        index = 0
        reduced = False
        iteration = 0
        LINE_WIDTH = 10
        total_cost = 0

        print("begin lines:", lines)
        print("begin pages:", pages)

        start = time.time()
        while(lines > target and pages > 1):
            
            print("index:", index)
            with open('pdf_extraction\\adi_comparing\\dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)
 
            res = perform_operators(dct, 0, path_to_latex, "pdf_extraction\\adi_comparing\\new_files\\")
            print("total operators:", len(res))
            if index >= (len(res)):
                print("Out of operators")
                break
            

            if res[index][0] >= LINE_WIDTH:
                latex_after_operator = res[index][1]

                f = open("pdf_extraction\\adi_comparing\\new_files\\after_operator.tex", "w")
                f.write(latex_after_operator)
                f.close()

                cmd_line_act = '"C:\\Users\\user\\tectonic.exe" ' + "pdf_extraction\\adi_comparing\\new_files\\after_operator.tex"
                os.system(cmd_line_act)
                #time.sleep(1)

                lines_before = lines
                lines, pages = check_lines("pdf_extraction\\adi_comparing\\new_files\\after_operator.pdf")
                print("current lines:", lines)
                print("current pages:", pages)
                
                path_to_latex = "pdf_extraction\\adi_comparing\\new_files\\after_operator.tex"
                
                #feature_extraction.run_feature_extraction(["pdf_extraction\\adi_comparing\\new_files\\after_operator"],["pdf_extraction\\adi_comparing\\new_files\\after_operator"],['bibliography'])
                features_single.run_feature_extraction("pdf_extraction\\adi_comparing\\new_files\\after_operator.tex","pdf_extraction\\adi_comparing\\new_files\\after_operator.pdf",'pdf-tests\\bibliography.bib',"pdf_extraction\\adi_comparing\\dct0", "pdf_extraction\\adi_comparing\\new_files\\dct0", "test", pd.DataFrame())
                
                
                iteration += 1
                total_cost += res[index][0]
                index+=1

                # if(lines_before <= lines):
                #     index+=1
                    
                # if lines_before > lines:
                #     index = 0
                
                if(lines <= target or pages < 2):
                    reduced = True
            
            else:
                index+=1

        
        end = time.time()

        return iteration, end-start, reduced, total_cost
    except Exception as e:
        print(e)
        return -1, -1, reduced, -1





###################################################################################################################



models = {}
directory = "pdf_extraction\\adi_comparing\\new_models"
for file in os.scandir(directory):
    if file.is_file():
        n = re.findall('\d+\.?\d*', file.name)
        i = (n[0], n[4], n[5])
        
        file_path = directory + '\\' + file.name
        #print(file_path)
        clf = xg.XGBClassifier()
        booster = xg.Booster()
        booster.load_model(file_path)
        clf._Booster = booster
        print(i)
        models[i] = clf

       

print(len(models))

def model_greedy(path_to_pdf, path_to_latex):
    try:
        lines, pages = check_lines(path_to_pdf)

        if lines < 2:
            print("Less then 2 lines")
            return -1,-1,False, -1
        if pages < 2:
            print("Less then 2 pages")
            return -1,-1,False,-1

        df1 = features_single.run_feature_extraction(path_to_latex,path_to_pdf,'pdf-tests\\bibliography.bib',"pdf_extraction\\adi_comparing\\dct0", "pdf_extraction\\adi_comparing\\new_files\\dct0", "test", pd.DataFrame())
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on', 'num_of_object'], axis=1, inplace=True)
        old_df=df1
        print(df1)##################
        target = lines - 2 
        index = 0
        reduced = False
        iteration = 0
        total_cost = 0

        print("begin lines:", lines)
        print("begin pages:", pages)

        start = time.time()
        while(lines > target and pages > 1):
            
            print("index:", index)
            with open('pdf_extraction\\adi_comparing\\dct0', 'rb') as dct_file:
                dct = pickle.load(dct_file)
 
            print(dct) #########################

            res = perform_operators(dct, 0, path_to_latex, "pdf_extraction\\adi_comparing\\new_files\\")
            print("total operators:", len(res))
            if index >= (len(res)):
                print("Out of operators")
                break
              
        
            model_to_predict = (str(res[index][2]), str(res[index][3]), res[index][5])
            #model_to_predict = ('5','1','1')
            print("model_to_predict:", model_to_predict)


            #df1.at['test','type'] = res[index][2]
            #df1.at['test', 'value'] = res[index][3]
            #df1.at['test', 'object_used_on'] = res[index][4]
            #df1.at['test', 'num_of_object'] = int(res[index][5])
            
            #print(models[('8', '1', '4')].predict(df1.to_numpy())[0])
            try:
                prediction = models[model_to_predict].predict(df1.to_numpy())[0]
                #prediction = 1

                #print(prediction)
                #prediction = models[model_to_predict].predict_proba(df1.to_numpy())[0]
                #print(prediction)
                #exit()

            except Exception as e:
                print("not found model:", e)
                index+=1
                continue

            #return

            if prediction > 0:
                latex_after_operator = res[index][1]

                f = open("pdf_extraction\\adi_comparing\\new_files\\after_operator.tex", "w")
                f.write(latex_after_operator)
                f.close()

                cmd_line_act = '"C:\\Users\\user\\tectonic.exe" ' + "pdf_extraction\\adi_comparing\\new_files\\after_operator.tex"
                os.system(cmd_line_act)
                #time.sleep(1)

                lines_before = lines
                lines, pages = check_lines("pdf_extraction\\adi_comparing\\new_files\\after_operator.pdf")
                print("current lines:", lines)
                print("current pages:", pages)
                
                path_to_latex = "pdf_extraction\\adi_comparing\\new_files\\after_operator.tex"
                
                #feature_extraction.run_feature_extraction(["pdf_extraction\\adi_comparing\\new_files\\after_operator"],["pdf_extraction\\adi_comparing\\new_files\\after_operator"],['bibliography'])
                df1 = features_single.run_feature_extraction("pdf_extraction\\adi_comparing\\new_files\\after_operator.tex","pdf_extraction\\adi_comparing\\new_files\\after_operator.pdf",'pdf-tests\\bibliography.bib',"pdf_extraction\\adi_comparing\\dct0", "pdf_extraction\\adi_comparing\\new_files\\dct0", "test", pd.DataFrame())
                df1 = df1.T
                df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on', 'num_of_object'], axis=1, inplace=True)

                sub_df = old_df.subtract(df1) ####################
                sub_df.to_csv(f'pdf_extraction\\adi_comparing\\new_files\\sub_df2_{model_to_predict}.csv', index=False) #change here
                
                print(df1)###################
                total_cost += res[index][0]
                index+=1
                iteration += 1
                

                # if(lines_before <= lines):
                #     index+=1
                    
                # if lines_before > lines:
                #     index = 0
                
                if(lines <= target or pages < 2):
                    reduced = True
            
            else:
                index+=1

        
        end = time.time()

        return iteration, end-start, reduced, total_cost
    except Exception as e:
        print(e)
        return -1, -1, reduced, -1

    
###################################################################################################################



#feature_extraction.run_feature_extraction(["5067_4"],["5067_4"],['bibliography'])   


#feature_extraction.run_feature_extraction(['pdf-tests\\5067_4'], ['pdf-tests\\5067_4'],['bibliography'])

#with open('pdf_extraction\\adi_comparing\\dct0', 'rb') as dct_file:
    #dct = pickle.load(dct_file)


#res = perform_operators(dct, 0, "pdf-tests\\5067_4.tex", "pdf_extraction\\adi_comparing\\new_files\\")

#print(len(res))

#print(features_single.run_feature_extraction("pdf-tests\\5067_4.tex","pdf-tests\\5067_4.pdf",'pdf-tests\\bibliography.bib',"pdf_extraction\\adi_comparing\\dct0", "pdf_extraction\\adi_comparing\\new_files\\dct0", "test", pd.DataFrame()))


# iterations, time_taken, reduced = simple_greedy("pdf-tests\\123001_1.pdf", "pdf-tests\\123001_1.tex")
# exit()

names = []
directory = 'pdf_extraction\\adi_comparing\\files'
for file in os.scandir(directory):
    if file.is_file():
        #cmd_line_act = '"C:\\Users\\user\\tectonic.exe" ' + f"{directory}\\{file.name}"
        #os.system(cmd_line_act)
        names.append(file.name.split('.')[0])

# print(names)
# print(len(names))
# exit()

results = []
idx = 0
done = 1
for filename in set(names):
    print(f"file in test {idx}:", filename)
    idx+=1
    try:
        file_path = os.path.join(directory, filename + ".pdf")
        if os.path.isfile(file_path):
            path_to_pdf = file_path

        file_path = os.path.join(directory, filename + ".tex")
        if os.path.isfile(file_path):
            path_to_latex = file_path

        iterations, time_taken, reduced, cost = model_greedy(path_to_pdf, path_to_latex) #change here
        #print("Number of iteration:", iterations)
        #print("Time:", time_taken)

        if iterations != -1:
            results.append((filename, "model greedy", reduced, iterations, time_taken, cost)) #change here

            df = pd.DataFrame(results, columns=["Name", "Algorithm", "Reduced", "Iterations", "Time", "Cost"])
            df.to_csv('pdf_extraction\\adi_comparing\\new_files\\results_model_greedy.csv', index=False) #change here

            print("Done!", done)
            done+=1
    
        break
        
        
    except Exception as e:
        print(e)
    
    

df = pd.DataFrame(results, columns=["Name", "Algorithm", "Reduced", "Iterations", "Time", "Cost"])
df.to_csv('pdf_extraction\\adi_comparing\\new_files\\results_model_greedy.csv', index=False) #change here

##################################################################################################################