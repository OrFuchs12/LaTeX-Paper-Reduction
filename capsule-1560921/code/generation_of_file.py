import os
from time import sleep

import numpy as np
import sys

import pandas as pd

from get_dictionary import getDict
import objects_generation
import random
import itertools
import features_extraction_single_paper
import read_single_file


def pairwise(iterable):
    """
    helper function as part of the generation of three variants of tex file
    :param iterable:
    :return:
    """
    iters = itertools.tee(iterable, 3)
    for i, it in enumerate(iters):
        next(itertools.islice(it, i, i), None)
    return zip(*iters)


def byrules(iterable):
    """
        helper function as part of the generation of three variants of tex file
        :param iterable:
        :return:
        """
    for x, y, z in pairwise(iterable):
        if (x == 51 and y == 50) or (y == 51 and z == 50):
            return False
        elif (x == 51 and y == 51) or (y == 51 and z == 51):
            return False
        elif (x == 50 and z == 51):
            if (0 <= y <= 49 or 52 <= y <= 101):
                continue
            else:
                return False
        elif (x == 50 and y == 51 and z == 50):
            return False
    return True


def create_tex(lst, name, loc, helper_dct, documents_path):
    """
      Parameters:
      ----------
      lst : list
          list of object indexes
      name : int/string
          name of the file
      loc: int
          location in 'initial_document_path' to insert the content
          :param documents_path:
  """
    os.system(f"echo c1")
    content = ""
    for i in lst:
        content += helper_dct[i]
        content += '\n'
    os.system(f"echo c2")
    specific_object = "\\UseRawInputEncoding \n\\def\\year{2022}\\relax \n\\documentclass[a4paper]{article} \n\\UseRawInputEncoding \n\\usepackage[utf8]{inputenc} \n\\usepackage{../aaai22} \n\\usepackage{times} \n\\usepackage{helvet} \n\\usepackage{courier} \n\\usepackage[hyphens]{url} \n\\usepackage{graphicx} \n\\usepackage{natbib} \n\\usepackage{caption} \n\\frenchspacing \n\\setlength{\\pdfpagewidth}{8.5in} \n\\setlength{\\pdfpageheight}{11in} \n\\usepackage{algpseudocode} \n\\usepackage{algorithm} \n\\newtheorem{definition}{Definition} \n\\usepackage{amssymb} \n\\usepackage{amsmath} \n\\usepackage{amsfonts} \n\\usepackage{adjustbox} \n\\usepackage{subcaption} \n\\usepackage{comment} \n\\setcounter{secnumdepth}{2} \n\\usepackage[T1]{fontenc} \n\\usepackage{mathptmx} \n\\begin{document}\n"

    specific_object += content
    specific_object += "\n"
    specific_object += "\\end{document}"
    os.system(f"echo c3")
    file1 = open(f"{documents_path}{name}.tex", 'w')
    file1.writelines(specific_object)
    file1.close()
    os.system(f"echo c4")
    # single_document_generation.generate(f"{documents_path}\{name}.tex", initial_document_path, loc, content, name)


def create_files(documents_path, current_permutation, min_max, tot_dict, helper_dct, locations, mod, number_of_version,
                 page_difference):
    """
    generate tex content

    :param documents_path: path where the new file will be at
    :param current_permutation: list represents the permutation
    :param min_max: dictionary, explained in readme file
    :param tot_dict: dictionary, explained in readme file
    :param helper_dct: dictionary of tex code, explained in readme file
    :param locations: hard-coded number represents which line starts the '\begin{document}', when in following lines we will write the tex elements.
    :param mod: F means first try to the page, T means second try
    :param number_of_version: the number of current variant
    :param page_difference: value of exceeding height in the second page of compiled pdf . We use it in order to make the total height
    of tex objects higher/lower in 'page_difference' units.
    :return: tex objects
    """
    min_value = 1100
    max_value = 1500

    min_amount = 0
    max_amount = 0
    permutation = []
    for object_index in range(len(current_permutation)):
        if current_permutation[object_index] != 0:
            min_amount += min_max[object_index][0] * current_permutation[object_index]
            max_amount += min_max[object_index][1] * current_permutation[object_index]
            for i in range(current_permutation[object_index]):
                permutation.append(object_index)

    if page_difference > 0:
        min_value += page_difference
    else:
        max_value += page_difference

    if max_amount < min_value:
        return False


    else:
        os.system(f"echo g3")
        current_sum = 0
        current_sum = min_amount
        current_index = 0
        current_items = [0 for x in permutation]
        current_items_values = []
        current_items_values_sum = []
        randomint = random.random()
        isSpecialFloat = False
        if randomint < 0.1:
            isSpecialFloat = True

        given = True
        helpertuple = [-1, 0]
        if isSpecialFloat == True:
            given = False
        ans = 0
        randomint = random.random()
        if randomint < 0.25:
            ans = 1
        elif randomint >= 0.25 and randomint < 0.5:
            ans = 2
        elif randomint >= 0.5 and randomint < 0.75:
            ans = 3
        else:
            ans = 4
        for x in permutation:
            if x == 4 or x == 5 or x == 6:
                if given == False:
                    current_items_values.append(tot_dict[x][ans][0][0][0])
                    current_items_values_sum.append(tot_dict[x][ans][0][0][1])
                    helpertuple = [x, ans]
                    given = True
                else:
                    current_items_values.append(tot_dict[x][0][0][0][0])
                    current_items_values_sum.append(tot_dict[x][0][0][0][1])

            else:
                current_items_values.append(tot_dict[x][0][0][0])
                current_items_values_sum.append(tot_dict[x][0][0][1])

        os.system(f"echo g4")
        # current_items_values=[tot_dict[x][0][0] for x in permutation]
        # current_items_values_sum = [tot_dict[x][0][1] for x in permutation]
        current_nos = [False for x in permutation]
        totno = 0

        while current_sum < min_value and totno != len(permutation):
            current_items[current_index] += 1

            if current_nos[current_index] == False:
                if permutation[current_index] == 4 or permutation[current_index] == 5 or permutation[
                    current_index] == 6:
                    if current_index == helpertuple[0]:
                        if current_items[current_index] < len(tot_dict[permutation[current_index]][helpertuple[1]]) - 1:
                            random_location = random.randint(0, len(
                                tot_dict[permutation[current_index]][helpertuple[1]][current_items[current_index]]) - 1)
                            new_obj = \
                                tot_dict[permutation[current_index]][helpertuple[1]][current_items[current_index]][
                                    random_location]
                            diff = new_obj[1] - current_items_values_sum[current_index]
                            current_sum += diff
                            current_items_values_sum[current_index] = new_obj[1]
                            current_items_values[current_index] = new_obj[0]

                        if current_items[current_index] >= len(
                                tot_dict[permutation[current_index]][helpertuple[1]]) - 1:
                            totno += 1
                            current_nos[current_index] = True
                    else:
                        if current_items[current_index] < len(tot_dict[permutation[current_index]][0]) - 1:
                            random_location = random.randint(0, len(
                                tot_dict[permutation[current_index]][0][current_items[current_index]]) - 1)
                            new_obj = tot_dict[permutation[current_index]][0][current_items[current_index]][
                                random_location]
                            diff = new_obj[1] - current_items_values_sum[current_index]
                            current_sum += diff
                            current_items_values_sum[current_index] = new_obj[1]
                            current_items_values[current_index] = new_obj[0]

                        if current_items[current_index] >= len(tot_dict[permutation[current_index]][0]) - 1:
                            totno += 1
                            current_nos[current_index] = True

                else:
                    if current_items[current_index] < len(tot_dict[permutation[current_index]]) - 1:
                        random_location = random.randint(0, len(
                            tot_dict[permutation[current_index]][current_items[current_index]]) - 1)

                        new_obj = tot_dict[permutation[current_index]][current_items[current_index]][random_location]
                        diff = new_obj[1] - current_items_values_sum[current_index]
                        current_sum += diff
                        current_items_values_sum[current_index] = new_obj[1]
                        current_items_values[current_index] = new_obj[0]

                    if current_items[current_index] >= len(tot_dict[permutation[current_index]]) - 1:
                        totno += 1
                        current_nos[current_index] = True

            current_index += 1
            if current_index == len(permutation):
                current_index = 0

        os.system(f"echo g5")
        if current_sum > min_value and current_sum <= max_value:

            # random 3 variants, while making sure they are different.

            exists = False
            for x in current_items_values:
                if x == 51 or x == 50:
                    exists = True
                    os.system(f"echo g6")
            if exists == False:
                os.system(f"echo g7")
                np.random.shuffle(current_items_values)
                p1 = np.copy(current_items_values)
                if mod == True:
                    create_tex(p1, f"{current_permutation_index}_{number_of_version}", locations[0], helper_dct,
                               documents_path)
                    os.system(f"echo g8")
                    return True
                np.random.shuffle(current_items_values)
                p2 = np.copy(current_items_values)
                max_shuffles = 50
                counter = 0
                os.system(f"echo g9")
                while np.array_equal(p1, p2) and counter < max_shuffles:
                    p2 = np.copy(current_items_values)
                    np.random.shuffle(p2)
                    counter += 1

                os.system(f"echo g10")
                np.random.shuffle(current_items_values)
                p3 = np.copy(current_items_values)
                counter = 0
                os.system(f"echo g11")
                while (np.array_equal(p2, p3) or np.array_equal(p3, p1)) and counter < max_shuffles:
                    p3 = np.copy(current_items_values)
                    np.random.shuffle(p3)
                    counter += 1
                os.system(f"echo g12a")
                if np.array_equal(p1, p2) == True or np.array_equal(p3, p2) == True or np.array_equal(p1, p3) == True:
                    os.system(f"echo g12b")
                    return False
                else:
                    os.system(f"echo g13a")
                    create_tex(p1, f"{current_permutation_index}_1", locations[0], helper_dct, documents_path)
                    create_tex(p2, f"{current_permutation_index}_2", locations[0], helper_dct, documents_path)
                    create_tex(p3, f"{current_permutation_index}_3", locations[0], helper_dct, documents_path)
                    os.system(f"echo g13b")
                    return True
            else:
                os.system(f"echo g14")
                np.random.shuffle(current_items_values)
                p1 = np.copy(current_items_values)

                max_shuffles = 50
                counter = 0
                while byrules(p1) == False and counter < max_shuffles:
                    p1 = np.copy(current_items_values)
                    np.random.shuffle(p1)
                    counter += 1
                if byrules(p1) == False:
                    os.system(f"echo g15")
                    return False
                else:
                    os.system(f"echo g16")
                    np.random.shuffle(current_items_values)
                    p2 = np.copy(current_items_values)

                    counter = 0
                    while (byrules(p2) == False or np.array_equal(p1, p2)) and counter < max_shuffles:
                        p2 = np.copy(current_items_values)
                        np.random.shuffle(p2)
                        counter += 1
                    os.system(f"echo g17")
                    if byrules(p2) == False or np.array_equal(p1, p2) == True:
                        os.system(f"echo g18")
                        return False
                    else:
                        np.random.shuffle(current_items_values)
                        p3 = np.copy(current_items_values)
                        counter = 0
                        while (byrules(p3) == False or np.array_equal(p2, p3) or np.array_equal(p3,
                                                                                                p1)) and counter < max_shuffles:
                            p3 = np.copy(current_items_values)
                            np.random.shuffle(p3)
                            counter += 1
                        os.system(f"echo g19")
                        if byrules(p3) == False or np.array_equal(p3, p2) == True or np.array_equal(p1, p3) == True:
                            os.system(f"echo g20")
                            return False
                        else:
                            os.system(f"echo g21")
                            create_tex(p1, f"{current_permutation_index}_1", locations[0], helper_dct, documents_path)
                            create_tex(p2, f"{current_permutation_index}_2", locations[0], helper_dct, documents_path)
                            create_tex(p3, f"{current_permutation_index}_3", locations[0], helper_dct, documents_path)
                            os.system(f"echo g22")
                            return True


        else:
            return False


def generate_single_file(perm, batch_number, documents_path,
                         bib_path,errors_path, fixing_path, excel_path, features_path, analysis_path, locations):
    helper_dct = objects_generation.getDict()
    min_max, tot_dict = getDict()

    objects_list = [8, 2, 3, 2, 4, 2, 2, 5, 1]
    # Each location in the array represents different object. The objects_list represents for each object type,
    # what is the maximum recurrences for the object.
    # 0-paragraphs
    # 1-section
    # 2-subsection
    # 3-paragraph
    # 4-figures
    # 5-tables
    # 6-algorithms
    # 7-formulas
    # 8-enum

    # creating all combinations possibles for objects counts:
    finallist = []
    curlist = []
    for p in range(objects_list[0] + 1):
        for e in range(objects_list[1] + 1):
            for f in range(objects_list[2] + 1):
                for s in range(objects_list[3] + 1):
                    for ss in range(objects_list[4] + 1):
                        for sss in range(objects_list[5] + 1):
                            for a in range(objects_list[6] + 1):
                                for formula in range(objects_list[7] + 1):
                                    for t in range(objects_list[8] + 1):
                                        curlist = [p, e, f, s, ss, sss, a, formula, t]
                                        finallist.append(curlist)

    df = pd.DataFrame()

    # compiler commands
    cmd_line_act = 'tectonic -X compile ' + documents_path

    i = perm
    os.system(f"echo '{i}'")
    if i % 10 == 0:
        helper_dct = objects_generation.getDict()
    current_permutation_index = i
    current_permutation = finallist[current_permutation_index]
    response = create_files(documents_path, current_permutation, min_max, tot_dict, helper_dct, locations, False, 0,
                            0) #generation of tex content
    if response == True:  # creation success
        # print("1")
        os.system(f"echo 1")
        cmds = []
        for j in range(1, 4): #3 variants for the page
            # (j)
            os.system(f"echo '{j}'")
            cmd_line_to_run = cmd_line_act + str(i) + "_" + str(j) + ".tex"
            os.system(cmd_line_to_run) #compiling tex
            try:
                sleep(3)
                pdf_path = documents_path + str(i) + "_" + str(j) + ".pdf"
                page_difference = read_single_file.order(pdf_path) #receives the height of the second page
                os.system(f"echo 'PageDifference: {page_difference}'")
                if page_difference == 0:  # good page
                    print("2")
                    os.system(f"echo 2")
                    latex_path = documents_path + str(i) + "_" + str(j) + ".tex"
                    pdf_path = documents_path + str(i) + "_" + str(j) + ".pdf"
                    pdf_path_excel_df_result = features_path + str(i) + "_" + str(j)
                    pdf_path_analysis = analysis_path + str(i) + "_" + str(j)
                    file_name = str(i) + "_" + str(j)
                    df = features_extraction_single_paper.run_from_outside(latex_path, pdf_path, bib_path, pdf_path_excel_df_result,
                                                          pdf_path_analysis, file_name, df) #do feature extraction process
                    print("3")
                    os.system(f"echo 3")
                else: #bad page
                    print("4")
                    os.system(f"echo 4")
                    cmd_line_to_run = documents_path + str(i) + "_" + str(j) + ".tex"
                    os.system(f"echo {cmd_line_to_run}")
                    if os.path.exists(cmd_line_to_run):
                        os.system(f"echo 4a")
                        os.remove(cmd_line_to_run) #delete tex
                    os.system(f"echo 4a1")

                    cmd_line_to_run = documents_path + str(i) + "_" + str(j) + ".pdf"
                    os.system(f"echo {cmd_line_to_run}")
                    if os.path.exists(cmd_line_to_run):
                        os.system(f"echo 4b")
                        os.remove(cmd_line_to_run) #delete compiled pdf

                    os.system(f"echo 4b1")
                    res = create_files(documents_path, current_permutation, min_max, tot_dict, helper_dct,
                                       locations, True, j, page_difference) #create again, send the page difference to the function
                    print("5")
                    os.system(f"echo 5")
                    if res == True: #created tex content successfully
                        print("6")
                        os.system(f"echo 6")
                        cmd_line_to_run = cmd_line_act + str(i) + "_" + str(j) + ".tex"
                        os.system(cmd_line_to_run) #compile tex
                        sleep(3)
                        pdf_path = documents_path + str(i) + "_" + str(j) + ".pdf"
                        page_difference = read_single_file.order(pdf_path) #receives the height of the second page
                        print("7")
                        os.system(f"echo 7")
                        if page_difference == 0: #good page
                            print("8")
                            os.system(f"echo 8")
                            latex_path = documents_path + str(i) + "_" + str(j) + ".tex"
                            pdf_path = documents_path + str(i) + "_" + str(j) + ".pdf"
                            pdf_path_excel_df_result = features_path + str(i) + "_" + str(j)
                            pdf_path_analysis = analysis_path + str(i) + "_" + str(j)
                            file_name = str(i) + "_" + str(j)
                            df = features_extraction_single_paper.run_from_outside(latex_path, pdf_path, bib_path, pdf_path_excel_df_result,
                                                                  pdf_path_analysis, file_name, df) #feature extraction
                            print("9")
                            os.system(f"echo 9")
                        else:
                            print("10")
                            os.system(f"echo 10")
                            cmd_line_to_run = documents_path + str(i) + "_" + str(j) + ".tex"
                            if os.path.exists(cmd_line_to_run):
                                os.remove(cmd_line_to_run) #delete tex file
                            cmd_line_to_run = documents_path + str(i) + "_" + str(j) + ".pdf"
                            if os.path.exists(cmd_line_to_run):
                                os.remove(cmd_line_to_run) #delete pdf file

                            hs = open(fixing_path, "a")
                            hs.write(str(i) + "_" + str(j) + "\n") #write to log the permutation creation failed
                            hs.close()
                            print("11")
                            os.system(f"echo 11")

                    else:
                        print("12")
                        os.system(f"echo 12")
                        hs = open(fixing_path, "a")
                        hs.write(str(i) + "_" + str(j) + "\n")
                        hs.close()
                        print("13")
                        os.system(f"echo 13")
            except:
                print("14")
                os.system(f"echo 14")
                hs = open(errors_path, "a")
                hs.write(str(i) + "_" + str(j) + "\n")
                hs.close()
                print("15")
                os.system(f"echo 15")

    else:
        print("16")
        os.system(f"echo 16")
        hs = open(errors_path, "a")
        hs.write(str(i) + "\n")
        hs.close()
        print("17")
        os.system(f"echo 17")

    print("18")
    if df.empty == False:
        print("19")
        df = df.T
        df.to_csv(excel_path, index=True, header=True)  # write csv of feature extraction
print("20")

if __name__ == '__main__':
    perm = int(sys.argv[1])
    batch_number = int(sys.argv[2])
    documents_path = sys.argv[3]
    bib_path = sys.argv[4]
    errors_path = sys.argv[5]
    fixing_path = sys.argv[6]
    excel_path = sys.argv[7]
    features_path = sys.argv[8]
    analysis_path = sys.argv[9]
    locations = [30]

    objects_list = [8, 2, 3, 2, 4, 2, 2, 5, 1]
    # Each location in the array represents different object. The objects_list represents for each object type,
    # what is the maximum recurrences for the object.
    # 0-paragraphs
    # 1-section
    # 2-subsection
    # 3-paragraph
    # 4-figures
    # 5-tables
    # 6-algorithms
    # 7-formulas
    # 8-enum

    # creating all combinations possibles for objects counts:
    finallist = []
    curlist = []
    for p in range(objects_list[0] + 1):
        for e in range(objects_list[1] + 1):
            for f in range(objects_list[2] + 1):
                for s in range(objects_list[3] + 1):
                    for ss in range(objects_list[4] + 1):
                        for sss in range(objects_list[5] + 1):
                            for a in range(objects_list[6] + 1):
                                for formula in range(objects_list[7] + 1):
                                    for t in range(objects_list[8] + 1):
                                        curlist = [p, e, f, s, ss, sss, a, formula, t]
                                        finallist.append(curlist)

    current_permutation_index = perm
    current_permutation = finallist[current_permutation_index]
    generate_single_file(perm, batch_number, documents_path, bib_path,errors_path, fixing_path, excel_path, features_path, analysis_path, locations)