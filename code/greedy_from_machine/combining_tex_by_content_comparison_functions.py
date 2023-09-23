import re

from get_pdf_order import order
from new_parsing import run

regex = re.compile('[^a-zA-Z]')


def adding_missing_object_to_list(missing,type_of_missing_object,first_line_of_previous_object_in_pdf_extract,page_num_of_previous_object,
                                                      column_num_of_previous_object,the_next_object_line_in_pdf_extract,current_page_number,current_column_number,
                                                      the_object_before_line_in_lines_to_search,counter):
    missing.append(
        [type_of_missing_object, first_line_of_previous_object_in_pdf_extract, page_num_of_previous_object,
         column_num_of_previous_object, the_next_object_line_in_pdf_extract, current_page_number, current_column_number, the_object_before_line_in_lines_to_search,counter])


def create_objects_list(tags,lines_to_search,pdf_extract):
    object_counter = 0
    object_dict = []
    #
    paragraphs_counter = 0
    counter = 0

    next_line_to_find = 0

    current_par_start = 0

    index_line = -1

    missing = []
    for k in range(2):
        for j in range(2):

            index_line = -1
            for i in pdf_extract[k][j]:  # left_column_page_0
                print(i)
                index_line += 1
                box, line = i

                if i[1].startswith("TABLETABLE"):  # it's a table
                    if tags[counter][0] != "Table":
                        object_dict.append(["missed" + tags[counter][0], index_line - 1, k, j])
                        type_of_missing_object=tags[counter][0]
                        first_line_of_previous_object_in_pdf_extract = object_dict[counter - 1][2]
                        page_num_of_previous_object = object_dict[counter - 1][3]
                        column_num_of_previous_object = object_dict[counter - 1][4]
                        the_next_object_line_in_pdf_extract=index_line - 1
                        current_page_number=k
                        current_column_number=j
                        the_object_before_line_in_lines_to_search=next_line_to_find - 1
                        adding_missing_object_to_list(missing,type_of_missing_object,first_line_of_previous_object_in_pdf_extract,page_num_of_previous_object,
                                                      column_num_of_previous_object,the_next_object_line_in_pdf_extract,current_page_number,current_column_number,
                                                      the_object_before_line_in_lines_to_search,counter)
                        counter += 1

                    object_dict.append((box, line, index_line, k, j))
                    counter += 1

                elif i[1].startswith("FIGUREFIGURE"):  # it's a table
                    if tags[counter][0] != "Figure":
                        object_dict.append(["missed" + tags[counter][0], index_line - 1, k, j])
                        type_of_missing_object=tags[counter][0]
                        first_line_of_previous_object_in_pdf_extract = object_dict[counter - 1][2]
                        page_num_of_previous_object = object_dict[counter - 1][3]
                        column_num_of_previous_object = object_dict[counter - 1][4]
                        the_next_object_line_in_pdf_extract=index_line - 1
                        current_page_number=k
                        current_column_number=j
                        the_object_before_line_in_lines_to_search=next_line_to_find - 1
                        adding_missing_object_to_list(missing,type_of_missing_object,first_line_of_previous_object_in_pdf_extract,page_num_of_previous_object,
                                                      column_num_of_previous_object,the_next_object_line_in_pdf_extract,current_page_number,current_column_number,
                                                      the_object_before_line_in_lines_to_search,counter)
                        counter += 1

                    helper_str = i[1]
                    while (helper_str.find("_") != -1):
                        helper_str = helper_str.split("_")[0]
                        object_dict.append((i[0], tags[counter], i[1], index_line, k, j))
                        counter += 1
                    object_dict.append((i[0], tags[counter], i[1], index_line, k, j))
                    counter += 1
                    # object_dict[counter]=(box,line)
                    # counter+=1

                else:  # it's a text line or formula
                    currline = regex.sub('', line)
                    helpline = regex.sub('', lines_to_search[next_line_to_find][1])

                    if currline.startswith(helpline):
                        # print(helpline)
                        next_line_to_find += 1
                        while tags[counter][0] == "Formula" or tags[counter][0] == "Algorithm" or tags[counter][0] == "Matrix":
                            object_dict.append(["missed" + tags[counter][0], index_line - 1, k, j])
                            type_of_missing_object = tags[counter][0]
                            first_line_of_previous_object_in_pdf_extract = object_dict[counter - 1][2]
                            page_num_of_previous_object = object_dict[counter - 1][3]
                            column_num_of_previous_object = object_dict[counter - 1][4]
                            the_next_object_line_in_pdf_extract = index_line - 1
                            current_page_number = k
                            current_column_number = j
                            the_object_before_line_in_lines_to_search = next_line_to_find - 2
                            adding_missing_object_to_list(missing, type_of_missing_object,
                                                          first_line_of_previous_object_in_pdf_extract,
                                                          page_num_of_previous_object,
                                                          column_num_of_previous_object,
                                                          the_next_object_line_in_pdf_extract, current_page_number,
                                                          current_column_number,
                                                          the_object_before_line_in_lines_to_search,counter)
                            counter += 1
                        object_dict.append((box, line, index_line, k, j))
                        counter += 1
    while counter!=len(tags): #missing tags at the end
        object_dict.append(["missed" + tags[counter][0], index_line - 1, k, j])
        type_of_missing_object = tags[counter][0]
        first_line_of_previous_object_in_pdf_extract = object_dict[counter - 1][2]
        page_num_of_previous_object = object_dict[counter - 1][3]
        column_num_of_previous_object = object_dict[counter - 1][4]
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
                                      the_object_before_line_in_lines_to_search, counter)
        counter+=1

    print("-------")
    print("-------")
    for k in object_dict:
        print(k)

    print("-------")
    for k in missing:
        print(k)

    return object_dict,missing


def filling_missing_objects_locations(objects_list,missing_objects_list,tags,lines_to_search,pdf_extract):
    final_list=objects_list
    missing_new=[]
    for missing_object in missing_objects_list:

        type_obj, line_from, k_from, j_from, line_to, k_to, j_to, next_line_to_find ,counter= missing_object

        helpline = regex.sub('', lines_to_search[next_line_to_find][2])

        if k_from == k_to and j_from==j_to: #same page, same column
            search_from = line_from
            if line_from > 0:  # in case there is only paragraph of one line
                search_from = line_from - 1

            for i in range(search_from, line_to + 1):

                box, line = pdf_extract[k_from][j_from][i]
                box_next, line_next = pdf_extract[k_from][j_from][i + 1]
                currline = regex.sub('', line + line_next)
                if currline.find(helpline) != -1:
                    # everything bellow the line_next untill the next known element - is a formula

                    beggining_of_formula = i + 2
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

                    final_list[counter] = (
                    (height_min, height_max), (type_obj, pdf_extract[k_from][j_from][beggining_of_formula][1],
                                               pdf_extract[k_from][j_from][end_of_formula][1]))

                    break

        elif k_from == k_to and j_from < j_to: #same page, different column
            arr=[]
            search_from_first_column = line_from
            if line_from > 0:  # in case there is only paragraph of one line
                search_from_first_column = line_from - 1

            search_to_first_column=len(pdf_extract[k_from][j_from])-1
            search_from_second_column=0
            search_to_second_column=line_to

            for i in range(search_from_first_column, search_to_first_column + 1):
                arr.append(pdf_extract[k_from][j_from][i])

            for i in range(search_from_second_column, search_to_second_column + 1):
                arr.append(pdf_extract[k_from][j_to][i])

            for i in range(len(arr)):

                box, line = arr[i]
                box_next, line_next = arr[i + 1]
                currline = regex.sub('', line + line_next)
                if currline.find(helpline) != -1:
                    # everything bellow the line_next untill the next known element - is a formula

                    beggining_of_formula = i + 2
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

                    final_list[counter] = (
                    (height_min, height_max), (type_obj, arr[beggining_of_formula][1],
                                               arr[end_of_formula][1]))

                    break

        else:
            if k_from ==0 and k_to==1 and j_from==1 and j_to==0:  # different page, different column
                next_line_to_find+=1

                beggining_of_formula = 0
                end_of_formula = line_to

                height_min = 1000
                height_max = -1

                for i in range(beggining_of_formula, end_of_formula + 1):
                    box, line = pdf_extract[k_to][j_to][i]
                    height_top, height_bottom = box

                    if height_top < height_min:
                        height_min = height_top
                    if height_bottom > height_max:
                        height_max = height_bottom

                final_list[counter] = (
                    (height_min, height_max), (type_obj, pdf_extract[k_to][j_to][beggining_of_formula][1],
                                               pdf_extract[k_to][j_to][end_of_formula][1]))



    # for element in missing_new:
    #
    #     beggining_of_formula, end_of_formula, page_num, column_num,counter = element
    #
    #     height_min = 1000
    #     height_max = -1
    #
    #     for i in range(beggining_of_formula, end_of_formula + 1):
    #         box, line = pdf_extract[page_num][column_num][i]
    #         height_top, height_bottom = box
    #
    #         if height_top < height_min:
    #             height_min = height_top
    #         if height_bottom > height_max:
    #             height_max = height_bottom
    #
        # final_list[counter]=((height_min,height_max),("Formula",pdf_extract[page_num][column_num][beggining_of_formula][1],
        #                                               pdf_extract[page_num][column_num][end_of_formula][1]))

    return final_list

def receive_locations_of_file(tex_path,pdf_path):

    tags,lines_to_search = run(tex_path)

    pdf_extract=order(pdf_path)

    objects_list,missing_objects_list=create_objects_list(tags,lines_to_search,pdf_extract)

    final_list=filling_missing_objects_locations(objects_list,missing_objects_list,tags,lines_to_search,pdf_extract)

    return final_list

def running_from_outside(pdf_path,tags,lines_to_search):
    pdf_extract=order(pdf_path)

    objects_list,missing_objects_list=create_objects_list(tags,lines_to_search,pdf_extract)

    final_list=filling_missing_objects_locations(objects_list,missing_objects_list,tags,lines_to_search,pdf_extract)

    return final_list


if __name__=="__main__":
    tex_path = "../../pdf-tests/ProjectOverleaf_Tests (22).pdf"
    pdf_path = "../../pdf-tests/two_pages_with_specific_v6.pdf"

    lst= receive_locations_of_file(tex_path,pdf_path)

    for item in lst:
        print(item)