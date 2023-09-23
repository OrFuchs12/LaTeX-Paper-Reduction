import Lidor_part
import perry
import sys
from itertools import islice
import copy
import get_list_of_locations

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def perform_operators(objects,doc_index,latex_path,bib_path):
    with open(latex_path, encoding='UTF-8') as file:
        # doc = file.read()
        base_doc = [line for line in file]

    #trying vspace
    latex_clean_lines = Lidor_part.read_file(latex_path, bib_path)
    # for k in lidor:
    #     print(k)
    # print(lidor)
    list_of_starts,tags = perry.parse2_lidor(latex_path, latex_clean_lines)
    #print("PERRY-----------------------------------------------------------------------")
    list_of_starts = list_of_starts[1:]
    #print(list_of_starts)
    #print(tags)
    print(latex_clean_lines)
    print(list_of_starts)
    print(tags)
    x = get_list_of_locations.run(latex_path)
    print(x)
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
    for i in range(len(list_of_starts)):
        if (tags[i][0] == 'Par'):
            par_index += 1
            index = par_index
        elif (tags[i][0] == 'Title'):
            title_index += 1
            index = title_index
        elif (tags[i][0] == 'AbstractSection'):
            abstractsec_index += 1
            index = abstractsec_index
        elif (tags[i][0] == 'AbstractPar'):
            abstractpar_index += 1
            index = abstractpar_index
        elif (tags[i][0] == 'Section'):
            section_index += 1
            index = section_index
        elif (tags[i][0] == 'SubSection'):
            subsection_index += 1
            index = subsection_index
        elif (tags[i][0] == 'SubSubSection'):
            subsubsection_index += 1
            index = subsubsection_index
        elif (tags[i][0] == 'Enum'):
            enum_index += 1
            index = enum_index
        elif (tags[i][0] == 'Algorithm'):
            algo_index += 1
            index = algo_index
        elif(tags[i][0] == 'CaptionFigure'):
            caption_index+=1
            index=caption_index
        elif(tags[i][0] == 'CaptionTable'):
            caption_table_index+=1
            index = caption_table_index
        elif(tags[i][0] == 'Formula'):
            formula_index+=1
            index = formula_index
        else:
            undetected_index += 1
            index = undetected_index
        if(tags[i][0] == 'Figure'):
            mapping_dict[tags[i][0] + str(tags[i][1])] = (list_of_starts[i], latex_clean_lines[list_of_starts[i]])
        elif(tags[i][0] == 'Table'):
            mapping_dict[tags[i][0] + str(int(tags[i][1])+1)] = (list_of_starts[i], latex_clean_lines[list_of_starts[i]])
        else:
            mapping_dict[tags[i][0] + str(index)] = (list_of_starts[i], latex_clean_lines[list_of_starts[i]])

    #print(mapping_dict)
    for i in objects:
        print(f'{i}' ':' f'{objects[i]}')
    for i in mapping_dict:
        print(f'{i}' ':' f'{mapping_dict[i]}')

    sys.exit()
    #we are taking into a account that latex and pdf may be ordered differently

    #print(objects)
    #print(summative_features)
    indexer = 0
    object_to_add_vspace_behind = 0
    #print(latex_clean_lines)
    arr_of_places_and_vspace_to_add = []
    figure_name_key_new_latex_list_value = {}
    offset = 0

    for key,value in objects.items(): #in this loop we will make all the operators
        if(indexer == 0): #in this if we wanted to skip the first object for the vspace but we need the first element for the other operators.
            indexer+=1
            if (key.startswith('Figure')): #changing size of figure
                chosen_index_to_insert = mapping_dict[key][0] #index where the figure starts
                flag = False
                index_to_go_through = chosen_index_to_insert
                while (flag != True):
                    if (index_to_go_through > len(latex_clean_lines)):
                        break
                    if (latex_clean_lines[index_to_go_through].startswith('\\includegraphics')): #finding the line where we can change the scale of the figure
                        found_index = index_to_go_through
                        flag = True
                    else:
                        index_to_go_through += 1
                if (flag == False):
                    continue
                # now we will shrink the figure to the 5 options of shrinking:
                # we will first find the places and then add the values based on the scale
                print(found_index)
                print(latex_clean_lines[found_index])
                string_to_edit = latex_clean_lines[found_index] #the line that we need to edit in order to change the scale
                # we will look for width and if it exists we will change it
                start_index = string_to_edit.find('width')
                running_index = 0
                if (start_index != -1): #find the number for width
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
                if (start_index != -1): #find the number for height
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
                print(width)
                print(height)
                # create 5 options:
                options = [0.9, 0.8, 0.7, 0.6, 0.5] #scale options
                figure_name_key_new_latex_list_value[key] = [] #this dict will have the key as the figure name and then value will be the lists of the new latex content for the new file
                string_to_edit = latex_clean_lines[found_index] #the string to edit
                for i in range(5):
                    new_width = width * options[i]
                    new_height = height * options[i]
                    new_str = string_to_edit.replace(str(width), str(new_width))
                    new_str = new_str.replace(str(height), str(new_height))
                    copy_list = copy.deepcopy(latex_clean_lines)
                    copy_list[found_index] = new_str
                    figure_name_key_new_latex_list_value[key].append(copy_list) #changing the string and adding the new latex list into the dict
            continue
        else:
            print(value['space_between_this_object_and_last_object'])
            if(value['space_between_this_object_and_last_object'] > 10): #candidate to add vspace
                #object_to_add_vspace_behind = key
                print()
                print(mapping_dict[key])
                chosen_index_to_insert = mapping_dict[key][0]
                if('Formula' in key):
                    #we will make 3 partitions:
                    vspace_size_max = value['space_between_this_object_and_last_object'] / 7
                    vspace_size_part = vspace_size_max/4
                    for i in range(1,5):
                        print("Part " + str(i) + " :")
                        vspace_size = "{:.2f}".format(vspace_size_part*i)
                        print("vspace size: " + str(vspace_size))
                        #latex_clean_lines.insert(chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n')
                        arr_of_places_and_vspace_to_add.append((chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n',key,vspace_size))
                        offset += 1
                else:
                    vspace_size_max = value['space_between_this_object_and_last_object']/3.5
                    vspace_size_part = vspace_size_max / 4
                    for i in range(1, 5):
                        print("Part " + str(i) + " :")
                        vspace_size = "{:.2f}".format(vspace_size_part * i)
                        print("vspace size: " + str(vspace_size))
                        # latex_clean_lines.insert(chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n')
                        arr_of_places_and_vspace_to_add.append((chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n', key, vspace_size))
                        offset += 1
            #now we will move to changing figure sizes:
            if(key.startswith('Figure')):
                chosen_index_to_insert = mapping_dict[key][0]
                flag = False
                index_to_go_through = chosen_index_to_insert
                while(flag != True):
                    if(index_to_go_through > len(latex_clean_lines)):
                        break
                    if(latex_clean_lines[index_to_go_through].startswith('\\includegraphics')):
                        found_index = index_to_go_through
                        flag = True
                    else:
                        index_to_go_through+=1
                if(flag == False):
                    continue
                #now we will shrink the figure to the 5 options of shrinking:
                #we will first find the places and then add the values based on the scale
                print(found_index)
                print(latex_clean_lines[found_index])
                string_to_edit = latex_clean_lines[found_index]
                #we will look for width and if it exists we will change it
                start_index = string_to_edit.find('width')
                running_index = 0
                if(start_index != -1):
                    running_index = start_index
                    while(running_index < len(string_to_edit)):
                        if(string_to_edit[running_index] == '='):
                            running_index+= 1 #now we will find the number and change it
                            end_number = False
                            number = ''
                            while(end_number!= True):
                                if(string_to_edit[running_index] == '\\'):
                                    end_number = True
                                else:
                                    number += string_to_edit[running_index]
                                    running_index+=1
                            width = float(number)
                            break
                        running_index+=1
                start_index = string_to_edit.find('height')
                running_index = 0
                if (start_index != -1):
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
                        running_index+=1
                print(width)
                print(height)
                #create 5 options:
                options = [0.9,0.8,0.7,0.6,0.5]
                figure_name_key_new_latex_list_value[key] = []
                string_to_edit = latex_clean_lines[found_index]
                for i in range(5):
                    new_width = width*options[i]
                    new_height = height*options[i]
                    new_str = string_to_edit.replace(str(width),str(new_width))
                    new_str = new_str.replace(str(height),str(new_height))
                    copy_list = copy.deepcopy(latex_clean_lines)
                    copy_list[found_index] = new_str
                    figure_name_key_new_latex_list_value[key].append(copy_list)

                #new_text = string_to_edit.replace(width,)




    #we will create a new doc with each vspace addition:
    print(figure_name_key_new_latex_list_value)
    for i in figure_name_key_new_latex_list_value:
        print(f'{i}' ':' f'{figure_name_key_new_latex_list_value[i]}')
    new_clean_latex_to_remember = copy.deepcopy(latex_clean_lines)
    #we will make changes to latex_clean_lines and then clean it with new_clean_latex_to_remember
    files_created = []
    index_for_all_operators = 1
    for i in range(len(arr_of_places_and_vspace_to_add)):
        #print("clean: ")
        #print(new_clean_latex_to_remember)
        latex_clean_lines = []
        latex_clean_lines = copy.deepcopy(new_clean_latex_to_remember)
        f = open("test" +str(doc_index)+str(index_for_all_operators)+".tex","w")
        files_created.append(("test" +str(doc_index)+str(index_for_all_operators)+".tex","test" +str(doc_index)+str(index_for_all_operators)+".pdf",arr_of_places_and_vspace_to_add[i][2],'vspace',arr_of_places_and_vspace_to_add[i][3])) #[(filename,pdfname,object,vspace(operator),vspace(operator)value)]
        chosen_index_to_insert = arr_of_places_and_vspace_to_add[i][0]
        str__ = arr_of_places_and_vspace_to_add[i][1]
        latex_clean_lines.insert(chosen_index_to_insert,str__)
        latex_clean_lines = latex_clean_lines[1:]
        #print(base_doc)
        for i in range(len(base_doc)):  # find the index of \\begin{document}
            if ('\\begin{document}' in base_doc[i]):
                new_list = base_doc[0:i + 1]
                new_list = new_list + latex_clean_lines
                break
        #print(new_list)
        for item in new_list:
            # write each item on a new line
            f.write(item)
        index_for_all_operators+=1

    # here we will create the new files for figure changes
    options = [0.9, 0.8, 0.7, 0.6, 0.5]
    for key,value in figure_name_key_new_latex_list_value.items():
        for i in range(5):
            f = open("test" + str(doc_index) + str(index_for_all_operators) + ".tex", "w")
            files_created.append(("test" + str(doc_index) + str(index_for_all_operators) + ".tex", "test" + str(doc_index) + str(index_for_all_operators) + ".pdf",
                                  key, 'change_figure_size', options[i]))  # [(filename,pdfname,object,vspace(operator),vspace(operator)value)]
            x_list = value[i][1:]
            #print(x_list)
            # print(base_doc)
            for i in range(len(base_doc)):  # find the index of \\begin{document}
                if ('\\begin{document}' in base_doc[i]):
                    new_list = base_doc[0:i + 1]
                    new_list = new_list + x_list
                    break
            #print(new_list)
            for item in new_list:
                # write each item on a new line
                f.write(item)
            f.close()
            print('Done')
            index_for_all_operators += 1

    print(files_created)
    return files_created




