import re

from get_pdf_order import order

regex = re.compile('[^a-zA-Z]')
regex_1 = re.compile('\bfi\b')

def adding_missing_object_to_list(missing,type_of_missing_object,first_line_of_previous_object_in_pdf_extract,page_num_of_previous_object,
                                                      column_num_of_previous_object,the_next_object_line_in_pdf_extract,current_page_number,current_column_number,
                                                      the_object_before_line_in_lines_to_search,counter):
    missing.append(
        [type_of_missing_object, first_line_of_previous_object_in_pdf_extract, page_num_of_previous_object,
         column_num_of_previous_object, the_next_object_line_in_pdf_extract, current_page_number, current_column_number, the_object_before_line_in_lines_to_search,counter])


def create_objects_list(tags,figures,tables,algorithms,lines_to_search,pdf_extract,figure_captions_set,table_captions_set):
    """
    main function of the mapping.
    :param tags, figures, tables, algorithms: received from the wrapper.  The reseason figures, tables, algorithms are separated
    is because of BHT! options, and they may not be at the exact order.
    :param lines_to_search: textual elements
    :param figure_captions_set: captions for each figure
    :param table_captions_set: captions for each table
    :return: mapping of tex to pdf elements

    :param pdf_extract: the extraction of elements from pdf
    """
    object_counter = 0
    object_dict = []
    figures_dict=[]
    tables_dict=[]
    #
    paragraphs_counter = 0
    counter = 0

    next_line_to_find = 0

    current_par_start = 0

    figures_counter=0
    algorithms_counter=0
    tables_counter=0
    index_line = -1
    object_dict_counter=0
    missing = []
    last_line_bbox=0
    last_text_position=0
    line_number_of_last_next_position=0
    last_k=0
    last_j=0

    current_need_to_be_caption_table=False
    current_need_to_be_caption_figure=False

    pdf_arr_for_appending=[]
    for k in range(2): #every page
        for j in range(2): #every column

            index_line = -1
            for i in pdf_extract[k][j]:  #every row in pdf extraction
                # print(i)
                index_line += 1
                box, line = i #box is the location, line is the contnet

                if i[1].startswith("TABLETABLE"):  # it's a table

                    if tables[tables_counter][0][-1]=="True":
                        current_need_to_be_caption_table=True
                    # object_dict.append([i[0], figures[figures_counter], i[1], index_line, k, j])
                    helper_dict = {"First_line_bbox": i[0], "Text": tables[tables_counter][0], "Line": index_line,
                                    "k": k, "j": j,"Type":"Table","LaTeX":"", "NumberLine":tables[tables_counter][1]}
                    object_dict.append(helper_dict)

                    if len(object_dict) > 1:
                        # object_dict[len(object_dict) - 2].append(last_line_bbox)
                        object_dict[len(object_dict) - 2]["Last_line_bbox"] = last_line_bbox
                        object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
                        object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
                        object_dict[len(object_dict) - 2]["pdf_array"] =pdf_arr_for_appending

                        pdf_arr_for_appending=[i]
                    tables_counter += 1
                    object_dict_counter += 1

                elif i[1].startswith("FIGUREFIGURE"):  # it's a figure

                    helper_str = i[1]
                    while (helper_str.find("_") != -1):
                        helper_str = helper_str.split("_")[0]
                        helper_dict={"First_line_bbox":i[0],"Text":figures[figures_counter][0],"Line":index_line,"k":k,"j":j,"Type":"Figure"
                                     ,"LaTeX":"", "NumberLine":figures[figures_counter][1]}
                        # object_dict.append([i[0], figures[figures_counter], i[1], index_line, k, j])
                        object_dict.append(helper_dict)
                        if len(object_dict)>1:
                            # object_dict[len(object_dict) - 2].append(last_line_bbox)
                            object_dict[len(object_dict) - 2]["Last_line_bbox"] = last_line_bbox
                            object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
                            object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
                            object_dict[len(object_dict) - 2]["pdf_array"] = pdf_arr_for_appending

                            pdf_arr_for_appending = []

                        figures_counter += 1
                        object_dict_counter += 1

                    if figures[figures_counter][0][-1]=="True":
                        current_need_to_be_caption_figure=True
                    # object_dict.append([i[0], figures[figures_counter], i[1], index_line, k, j])
                    helper_dict = {"First_line_bbox": i[0], "Text": figures[figures_counter][0], "Line": index_line,
                                    "k": k, "j": j,"Type":"Figure","LaTeX":"","NumberLine":figures[figures_counter][1]}
                    object_dict.append(helper_dict)

                    if len(object_dict) > 1:
                        # object_dict[len(object_dict) - 2].append(last_line_bbox)
                        object_dict[len(object_dict) - 2]["Last_line_bbox"] = last_line_bbox
                        object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
                        object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
                        object_dict[len(object_dict) - 2]["pdf_array"] = pdf_arr_for_appending

                        pdf_arr_for_appending = []

                    figures_counter += 1
                    object_dict_counter += 1
                    # object_dict[counter]=(box,line)
                    # counter+=1

                else:  # it's a text line or formula
                    line_number_of_last_next_position =index_line

                    currline = regex.sub('', line)
                    currline=currline.replace("fi", "")
                    currline=currline.replace("fl", "")
                    helpline = regex.sub('', lines_to_search[next_line_to_find][1])
                    helpline=helpline.replace("fi", "")
                    helpline=helpline.replace("fl", "")
                    if current_need_to_be_caption_figure==True: #looking for caption

                        for caption in figure_captions_set:
                            helpline = regex.sub('', caption[0][1])
                            helpline = helpline.replace("fi", "")
                            helpline = helpline.replace("fl", "")
                            if currline.startswith(helpline):
                                current_need_to_be_caption_figure = False
                                # object_dict.append([box, line, index_line, k, j])
                                helper_dict = {"First_line_bbox": box, "Text": line,
                                               "Line": index_line, "k": k, "j": j, "Type": "CaptionFigure","LaTeX":"",
                                               "NumberLine":caption[1]}
                                object_dict.append(helper_dict)

                                if len(object_dict) > 1:
                                    # object_dict[len(object_dict) - 2].append(last_line_bbox)
                                    object_dict[len(object_dict) - 2]["Last_line_bbox"] = last_line_bbox
                                    object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
                                    object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
                                    object_dict[len(object_dict) - 2]["pdf_array"] = pdf_arr_for_appending

                                    pdf_arr_for_appending = []
                                # figures_counter += 1
                                # next_line_to_find += 1
                                object_dict_counter += 1
                                last_text_position = len(object_dict)
                                break


                    elif current_need_to_be_caption_table==True:
                        for caption in table_captions_set:
                            helpline = regex.sub('', caption[0][1])
                            helpline=helpline.replace("fi", "")
                            helpline=helpline.replace("fl", "")
                            if currline.startswith(helpline):

                                current_need_to_be_caption_table = False
                                # object_dict.append([box, line, index_line, k, j])
                                helper_dict = {"First_line_bbox": box, "Text": line,
                                               "Line": index_line, "k": k, "j": j,"Type":"CaptionTable","LaTeX":"", "NumberLine":caption[1]}
                                object_dict.append(helper_dict)

                                if len(object_dict) > 1:
                                    # object_dict[len(object_dict) - 2].append(last_line_bbox)
                                    object_dict[len(object_dict) - 2]["Last_line_bbox"] = last_line_bbox
                                    object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
                                    object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
                                    object_dict[len(object_dict) - 2]["pdf_array"] = pdf_arr_for_appending

                                    pdf_arr_for_appending = []
                                # tables_counter += 1
                                # next_line_to_find += 1
                                object_dict_counter += 1
                                last_text_position = len(object_dict)
                                break




                    elif currline.startswith(helpline):

                            # print(helpline)
                            next_line_to_find += 1
                            while tags[counter][0][0] == "Formula" or tags[counter][0][0] == "Algorithm" or tags[counter][0][0] == "Matrix":
                                # object_dict.append(["missed" + tags[counter][0], index_line - 1, k, j])
                                helper_dict = {"First_line_bbox": box, "Text": "missed"+ tags[counter][0][0],
                                               "Line": index_line-1, "k": k, "j": j,"Type":tags[counter][0][0],
                                               "LaTeX":tags[counter][0][0], "NumberLine":tags[counter][1],"pdf_array":[]}

                                object_dict.append(helper_dict)

                                if len(object_dict) > 1:
                                    # object_dict[len(object_dict) - 2].append(last_line_bbox)
                                    object_dict[len(object_dict) - 2]["Last_line_bbox"]=last_line_bbox
                                    object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
                                    object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
                                    object_dict[len(object_dict) - 2]["pdf_array"] = pdf_arr_for_appending

                                    pdf_arr_for_appending = []

                                type_of_missing_object = tags[counter][0][0]
                                # first_line_of_previous_object_in_pdf_extract = object_dict[last_text_position - 1][2]
                                # page_num_of_previous_object = object_dict[last_text_position - 1][3]
                                # column_num_of_previous_object = object_dict[last_text_position - 1][4]
                                first_line_of_previous_object_in_pdf_extract = object_dict[last_text_position - 1]["Line"]
                                page_num_of_previous_object = object_dict[last_text_position - 1]["k"]
                                column_num_of_previous_object = object_dict[last_text_position - 1]["j"]

                                # the_next_object_line_in_pdf_extract = index_line - 1
                                the_next_object_line_in_pdf_extract = line_number_of_last_next_position -1
                                current_page_number = k
                                current_column_number = j
                                the_object_before_line_in_lines_to_search = next_line_to_find - 2
                                adding_missing_object_to_list(missing, type_of_missing_object,
                                                              first_line_of_previous_object_in_pdf_extract,
                                                              page_num_of_previous_object,
                                                              column_num_of_previous_object,
                                                              the_next_object_line_in_pdf_extract, current_page_number,
                                                              current_column_number,
                                                              the_object_before_line_in_lines_to_search,object_dict_counter)
                                counter += 1
                                object_dict_counter += 1
                                last_text_position = len(object_dict)
                            # object_dict.append([box, line, index_line, k, j])

                            helper_dict = {"First_line_bbox": box, "Text": line,
                                           "Line": index_line, "k": k, "j": j,"Type":tags[counter][0][0],
                                           "LaTeX":tags[counter][0][3], "NumberLine":tags[counter][1]}
                            object_dict.append(helper_dict)
                            if len(object_dict) > 1:
                                # object_dict[len(object_dict) - 2].append(last_line_bbox)
                                object_dict[len(object_dict) - 2]["Last_line_bbox"] = last_line_bbox
                                object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
                                object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
                                object_dict[len(object_dict) - 2]["pdf_array"] = pdf_arr_for_appending

                                pdf_arr_for_appending = []

                            counter += 1
                            object_dict_counter += 1
                            last_text_position = len(object_dict)

                    elif currline.startswith("Algorithm"):

                        helpline = regex.sub('', algorithms[algorithms_counter][0][1])
                        helpline = helpline.replace("fi", "")
                        helpline = helpline.replace("fl", "")
                        if currline.startswith(helpline):
                            # object_dict.append([box, line, index_line, k, j])
                            helper_dict = {"First_line_bbox": box, "Text": line,
                                           "Line": index_line, "k": k, "j": j,"Type":"Algorithm","LaTeX":"",
                                           "NumberLine":algorithms[algorithms_counter][1],"Pos":algorithms[algorithms_counter][0][-1]}
                            object_dict.append(helper_dict)

                            if len(object_dict) > 1:
                                # object_dict[len(object_dict) - 2].append(last_line_bbox)
                                object_dict[len(object_dict) - 2]["Last_line_bbox"] = last_line_bbox
                                object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
                                object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
                                object_dict[len(object_dict) - 2]["pdf_array"] = pdf_arr_for_appending

                                pdf_arr_for_appending = []

                            algorithms_counter += 1
                            # next_line_to_find += 1
                            object_dict_counter += 1
                            last_text_position = len(object_dict)


                last_line_bbox=box
                last_k=k
                last_j=j
                pdf_arr_for_appending.append(i)

    # object_dict[len(object_dict) - 1].append(last_line_bbox)
    object_dict[len(object_dict) - 1]["Last_line_bbox"] = last_line_bbox
    object_dict[len(object_dict) - 1]["Last_line_k"] = last_k
    object_dict[len(object_dict) - 1]["Last_line_j"] = last_j
    object_dict[len(object_dict) - 1]["pdf_array"] = pdf_arr_for_appending

    pdf_arr_for_appending = []

    while counter!=len(tags): #missing tags at the end
        # object_dict.append(["missed" + tags[counter][0], index_line - 1, k, j])
        helper_dict = {"First_line_bbox": box, "Text": "missed" + tags[counter][0][0],
                       "Line": index_line - 1, "k": k, "j": j,"Type":tags[counter][0][0],"LaTeX":tags[counter][0][0]
                       , "NumberLine":tags[counter][1]}
        object_dict.append(helper_dict)
        if len(object_dict) > 1:
            # object_dict[len(object_dict) - 2].append(last_line_bbox)
            object_dict[len(object_dict) - 2]["Last_line_bbox"] = last_line_bbox
            object_dict[len(object_dict) - 2]["Last_line_k"] = last_k
            object_dict[len(object_dict) - 2]["Last_line_j"] = last_j
            object_dict[len(object_dict) - 2]["pdf_array"] = pdf_arr_for_appending

            pdf_arr_for_appending = []

        type_of_missing_object = tags[counter][0][0]
        # first_line_of_previous_object_in_pdf_extract = object_dict[last_text_position - 1][2]
        # page_num_of_previous_object = object_dict[last_text_position - 1][3]
        # column_num_of_previous_object = object_dict[last_text_position - 1][4]
        first_line_of_previous_object_in_pdf_extract = object_dict[last_text_position - 1]["Line"]
        page_num_of_previous_object = object_dict[last_text_position - 1]["k"]
        column_num_of_previous_object = object_dict[last_text_position - 1]["j"]

        the_next_object_line_in_pdf_extract = index_line
        current_page_number = k
        current_column_number = j
        the_object_before_line_in_lines_to_search = next_line_to_find - 1
        adding_missing_object_to_list(missing, type_of_missing_object,
                                      first_line_of_previous_object_in_pdf_extract,
                                      page_num_of_previous_object,
                                      column_num_of_previous_object,
                                      the_next_object_line_in_pdf_extract, current_page_number,
                                      current_column_number,
                                      the_object_before_line_in_lines_to_search, object_dict_counter)
        counter+=1
        last_text_position = len(object_dict)
        object_dict_counter+=1
    # print("-------")
    # print("-------")
    # for k in object_dict:
    #     print(k)
    #
    # print("-------")
    # for k in missing:
    #     print(k)
    object_dict+=figures_dict
    object_dict+=tables_dict
    return object_dict,missing


def filling_missing_objects_locations(objects_list,missing_objects_list,tags,lines_to_search,pdf_extract):
    #this function fills the missing locations of elements in the tex file. Happens a lot when there are formulas.

    try:
        final_list=objects_list
        missing_new=[]
        for missing_object in missing_objects_list:

            type_obj, line_from, k_from, j_from, line_to, k_to, j_to, next_line_to_find ,counter= missing_object

            helpline = regex.sub('', lines_to_search[next_line_to_find][2])
            helpline = helpline.replace("fi", "")
            helpline = helpline.replace("fl", "")

            if k_from == k_to and j_from==j_to: #same page, same column
                search_from = line_from
                if line_from > 0:  # in case there is only paragraph of one line
                    search_from = line_from - 1

                pdf_arr_for_appending=[]

                #pdf_arr_for_appending.append(arr[0])
                for j in range(search_from, line_to + 1):
                    box, line = pdf_extract[k_from][j_from][j]

                    box_next, line_next = pdf_extract[k_from][j_from][j + 1]
                    # if j==search_from:
                    #     pdf_arr_for_appending.append((box,line))
                    pdf_arr_for_appending.append((box_next, line_next))
                    currline = regex.sub('', line + line_next)
                    currline = currline.replace("fi", "")
                    currline = currline.replace("fl", "")
                    if currline.find(helpline) != -1:
                        # everything bellow the line_next untill the next known element - is a formula

                        beggining_of_formula = j + 2
                        end_of_formula = line_to
                        # bbox_of_the_first_line_of_formula=pdf_extract[k_from][j_from][beggining_of_formula][0]
                        # bbox_of_the_last_line_of_formula=pdf_extract[k_from][j_from][end_of_formula][0]

                        height_min = 1000
                        height_max = -1

                        for i in range(beggining_of_formula, end_of_formula + 1):
                            box, line = pdf_extract[k_from][j_from][i]
                            height_top, height_bottom = box

                            if height_top < height_min:
                                height_min = height_top
                            if height_bottom > height_max:
                                height_max = height_bottom

                        # final_list[counter] = [
                        # (height_min, height_max), type_obj, pdf_extract[k_from][j_from][beggining_of_formula][1],
                        #                            pdf_extract[k_from][j_from][end_of_formula][1],box]
                        helper_dict = {"First_line_bbox": (height_min, height_max), "Text": pdf_extract[k_from][j_from][beggining_of_formula][1],
                                       "Line": beggining_of_formula, "k":k_from, "j": j_from, "Type": type_obj,
                                       "Last_line_bbox":(height_min, height_max),"Last_line_k":k_to,"Last_line_j":j_to,"pdf_array":[]
                                       ,"LaTeX":"",'NumberLine':-1}
                        final_list[counter] = helper_dict

                        if final_list[counter - 1]["Type"]!="Figure" and final_list[counter - 1]["Type"]!="Table":

                            final_list[counter-1]["Last_line_bbox"]= pdf_extract[k_from][j_from][j+1][0]
                            final_list[counter - 1]["Last_line_k"] = k_from
                            final_list[counter - 1]["Last_line_j"] = j_from
                            final_list[counter - 1]["pdf_array"] = pdf_arr_for_appending



                        break

            elif k_from == k_to and j_from < j_to: #same page, different column
                arr=[]
                search_from_first_column = line_from
                if line_from > 0:  # in case there is only paragraph of one line
                    search_from_first_column = line_from - 1

                search_to_first_column=len(pdf_extract[k_from][j_from])-1
                search_from_second_column=0
                search_to_second_column=line_to

                pdf_arr_for_appending = []

                for i in range(search_from_first_column, search_to_first_column + 1):
                    arr.append(pdf_extract[k_from][j_from][i])


                for i in range(search_from_second_column, search_to_second_column + 1):
                    arr.append(pdf_extract[k_from][j_to][i])

                # pdf_arr_for_appending.append(arr[0])
                for j in range(len(arr)):

                    box, line = arr[j]

                    if j!=len(arr)-1:
                        box_next, line_next = arr[j + 1]
                        pdf_arr_for_appending.append((box_next, line_next))
                        currline = regex.sub('', line + line_next)
                        currline = currline.replace("fi", "")
                        currline = currline.replace("fl", "")
                        if currline.find(helpline) != -1:
                            # everything bellow the line_next untill the next known element - is a formula

                            beggining_of_formula = j + 2
                            end_of_formula = len(arr)-1
                            # bbox_of_the_first_line_of_formula=pdf_extract[k_from][j_from][beggining_of_formula][0]
                            # bbox_of_the_last_line_of_formula=pdf_extract[k_from][j_from][end_of_formula][0]

                            # missing_new.append([beggining_of_formula, end_of_formula, k_from, j_from, counter])
                            height_min = 1000
                            height_max = -1

                            for i in range(beggining_of_formula, end_of_formula + 1):
                                box, line = arr[i]
                                height_top, height_bottom = box

                                if height_top < height_min:
                                    height_min = height_top
                                if height_bottom > height_max:
                                    height_max = height_bottom

                            # final_list[counter] = [
                            # (height_min, height_max), (type_obj, arr[beggining_of_formula][1],
                            #                            arr[end_of_formula][1]),box]
                            helper_dict = {"First_line_bbox": (height_min, height_max),
                                           "Text": pdf_extract[k_from][j_from][beggining_of_formula][1],
                                           "Line": beggining_of_formula, "k": k_from, "j": j_from, "Type": type_obj,
                                           "Last_line_bbox":(height_min, height_max),"Last_line_k":k_to,"Last_line_j":j_to,"pdf_array":[]
                                           ,"LaTeX":"",'NumberLine':-1}
                            final_list[counter] = helper_dict

                            if final_list[counter - 1]["Type"]!="Figure" and final_list[counter - 1]["Type"]!="Table":
                                final_list[counter - 1]["Last_line_bbox"] = arr[j+1][0]
                                final_list[counter - 1]["Last_line_k"] = k_from
                                final_list[counter - 1]["Last_line_j"] = j_from
                                final_list[counter - 1]["pdf_array"] = pdf_arr_for_appending
                            break

            else:
                if k_from ==0 and k_to==1 and j_from==1 and j_to==0:  # different page, different column
                    next_line_to_find+=1

                    beggining_of_formula = 0
                    end_of_formula = line_to

                    height_min = 1000
                    height_max = -1

                    pdf_arr_for_appending=[]
                    arr=[]
                    for i in range(beggining_of_formula, end_of_formula + 1):
                        box, line = pdf_extract[k_to][j_to][i]
                        height_top, height_bottom = box

                        if height_top < height_min:
                            height_min = height_top
                        if height_bottom > height_max:
                            height_max = height_bottom



                    search_to_first_column=len(pdf_extract[k_from][j_from])-1
                    for i in range(line_from, search_to_first_column + 1):
                        arr.append(pdf_extract[k_from][j_from][i])


                    for i in range(0, line_to + 1):
                        arr.append(pdf_extract[k_to][j_to][i])

                    pdf_arr_for_appending.append(arr[0])
                    for j in range(len(arr)):
                        box, line = arr[j]

                        if j != len(arr) - 1:
                            box_next, line_next = arr[j + 1]
                            pdf_arr_for_appending.append((box_next, line_next))
                            currline = regex.sub('', line + line_next)
                            currline = currline.replace("fi", "")
                            currline = currline.replace("fl", "")
                            if currline.find(helpline) != -1:
                                beggining_of_formula = j + 2
                                end_of_formula = len(arr) - 1
                                # bbox_of_the_first_line_of_formula=pdf_extract[k_from][j_from][beggining_of_formula][0]
                                # bbox_of_the_last_line_of_formula=pdf_extract[k_from][j_from][end_of_formula][0]

                                # missing_new.append([beggining_of_formula, end_of_formula, k_from, j_from, counter])
                                height_min = 1000
                                height_max = -1

                                for i in range(beggining_of_formula, end_of_formula + 1):
                                    box, line = arr[i]
                                    height_top, height_bottom = box

                                    if height_top < height_min:
                                        height_min = height_top
                                    if height_bottom > height_max:
                                        height_max = height_bottom

                    # final_list[counter] = [
                    #     (height_min, height_max), type_obj, pdf_extract[k_to][j_to][beggining_of_formula][1],
                    #                                pdf_extract[k_to][j_to][end_of_formula][1],box]

                                helper_dict = {"First_line_bbox": (height_min, height_max),
                                               "Text": pdf_extract[k_from][j_from][beggining_of_formula][1],
                                               "Line": beggining_of_formula, "k": k_from, "j": j_from, "Type": type_obj,
                                               "Last_line_bbox":(height_min, height_max),"Last_line_k":k_to,"Last_line_j":j_to,"pdf_array":[]
                                               ,"LaTeX":"",'NumberLine':-1}
                                final_list[counter]=helper_dict
                                if final_list[counter - 1]["Type"] != "Figure" and final_list[counter - 1]["Type"
                                    ] != "Table":
                                    final_list[counter - 1]["Last_line_bbox"] = arr[beggining_of_formula-1][0]
                                    final_list[counter - 1]["Last_line_k"] = k_from
                                    final_list[counter - 1]["Last_line_j"] = j_from
                                    final_list[counter - 1]["pdf_array"] = pdf_arr_for_appending

                                break
                    # final_list[counter - 1][-1] = pdf_extract[k_to][j_to][i][0]

        return final_list
    except:
        return final_list

def fixing_missing_objects(final_list, tags, lines_to_search, pdf_extract):
    #this function fixes missing objects locations.
    #happen rarely.

    try:
        last_paragraph_index=0
        next_paragraph_index=0

        index_for_type_of_object=2
        index=-1
        possible_locations=[]
        former_location_last=0
        current_location_current=0
        for k in final_list:
            index+=1
            if k["Type"] in ("Paragraph","Par","Section","SubSection","Enum","SubSubSection","AbstractSection","AbstractPar","Title"):
                last_paragraph_index=index

            if isinstance(k["Text"],str):
                if k["Text"].startswith("missed"):
                    former_location_last=final_list[last_paragraph_index]
                    for m in final_list[last_paragraph_index+1:]:
                        if m["Type"] in ("Paragraph","Par","Section","SubSection","Enum","SubSubSection","AbstractSection","AbstractPar","Title"):
                            to_line=m["First_line_bbox"][0]
                            from_line=final_list[last_paragraph_index]['Last_line_bbox']
                            last_k=m["Last_line_k"]
                            last_j = m["Last_line_j"]
                            # [former_location_last, k["First_line_bbox"], m["First_line_bbox"]]
                            replaced_obj=k
                            replaced_obj['First_line_bbox']=from_line
                            replaced_obj['Last_line_k']=last_k
                            replaced_obj['Last_line_j'] = last_j
                            replaced_obj['NumberLine']=-1
                            replaced_obj['pdf_array']=[]
                            final_list[index] = replaced_obj

                            pdf_arr_for_appending=[]
                            helpline = regex.sub('', former_location_last["LaTeX"][-20:-1])
                            helpline = helpline.replace("fi", "")
                            helpline = helpline.replace("fl", "")
                            current_arr=former_location_last["pdf_array"]
                            for j in range(len(current_arr)):
                                box, line = current_arr[j]
                                if j != len(current_arr) - 1:
                                    box_next, line_next = current_arr[j + 1]
                                    if j==0:

                                        pdf_arr_for_appending.append((box, line))
                                    pdf_arr_for_appending.append((box_next, line_next))
                                    currline = regex.sub('', line + line_next)
                                    currline = currline.replace("fi", "")
                                    currline = currline.replace("fl", "")
                                    if currline.find(helpline) != -1:
                                        break
                            if pdf_arr_for_appending!=[]:
                                former_location_last["pdf_array"]=pdf_arr_for_appending

                            break

                        current_location_current=m["First_line_bbox"][1]
                        if current_location_current-former_location_last["Last_line_bbox"][1]>11:
                            from_line=former_location_last["Last_line_bbox"]
                            to_line=m["First_line_bbox"]
                            last_k=m["Last_line_k"]
                            last_j = m["Last_line_j"]

                            replaced_obj=k
                            replaced_obj['First_line_bbox']=from_line
                            replaced_obj['Last_line_bbox']=to_line
                            replaced_obj['Last_line_k']=last_k
                            replaced_obj['Last_line_j'] = last_j
                            replaced_obj['NumberLine'] = -1
                            replaced_obj['pdf_array'] = []
                            # replaced_obj=[former_location_last["Last_line_bbox"],k["First_line_bbox"],m["First_line_bbox"]]
                            final_list[index]=replaced_obj

                            pdf_arr_for_appending=[]
                            helpline = regex.sub('', former_location_last["LaTeX"][-20:-1])
                            helpline = helpline.replace("fi", "")
                            helpline = helpline.replace("fl", "")
                            current_arr=former_location_last["pdf_array"]
                            for j in range(len(current_arr)):
                                box, line = current_arr[j]
                                if j != len(current_arr) - 1:
                                    box_next, line_next = current_arr[j + 1]
                                    if j == 0:
                                        pdf_arr_for_appending.append((box, line))
                                    pdf_arr_for_appending.append((box_next, line_next))
                                    currline = regex.sub('', line + line_next)
                                    currline = currline.replace("fi", "")
                                    currline = currline.replace("fl", "")

                                    if currline.find(helpline) != -1:
                                        break
                            if pdf_arr_for_appending!=[]:
                                former_location_last["pdf_array"]=pdf_arr_for_appending

                            break
                        else:
                            former_location_last=m

        return final_list
    except:
        return final_list


def running_from_outside(pdf_path,tags,figures,tables,algorithms,lines_to_search,figure_captions_set,table_captions_set):
    """
    A wrapper function for the mapping, and caluclation of height on second page.
    :param pdf_path:
    :param tags, figures, tables, algorithms: received from the wrapper.  The reseason figures, tables, algorithms are separated
    is because of BHT! options, and they may not be at the exact order.
    :param lines_to_search: textual elements
    :param figure_captions_set: captions for each figure
    :param table_captions_set: captions for each table
    :return: mapping of tex to pdf elements
    """
    try:
        pdf_extract=order(pdf_path)

        objects_list,missing_objects_list=create_objects_list(tags,figures,tables,algorithms,lines_to_search,pdf_extract,figure_captions_set,table_captions_set)

        final_list=filling_missing_objects_locations(objects_list,missing_objects_list,tags,lines_to_search,pdf_extract)

        final_list=fixing_missing_objects(final_list,tags,lines_to_search,pdf_extract)

        #calculation of height on second page
        totheight=0
        for k in pdf_extract[1][0]:
            box,line=k
            totheight+=box[1]-box[0]

        final_list.append(totheight)

        return final_list
    except:
        return []


# if __name__=="__main__":
#     tex_path = "../../pdf-tests/ProjectOverleaf_Tests (22).pdf"
#     pdf_path = "../../pdf-tests/two_pages_with_specific_v6.pdf"
#
#     lst= receive_locations_of_file(tex_path,pdf_path)
#
#     # for item in lst:
#     #     print(item)