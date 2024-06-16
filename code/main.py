import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path
import pickle
import greedy
import pdfMiner_new_checking_length, read_single_file
import time
import features_extraction_single_paper
from time import sleep
from pathlib import Path
import search_algorithms_for_experiment
import reload_models
import new_experiment_inferstructure
import subprocess
import shutil
import handle_full_paper
import Last_2_pages_rows_extract        
import traceback

# Read list to memory
def read_list(path):
    """
    read pickle of model
    :param path: path to file
    :return: model object
    """
    with open(path, 'rb') as fp:
        n_list = pickle.load(fp)
        # print(n_list)
        return n_list


def has_more_operators_to_check(activated, to_activate):
    """
    :param activated: list of operators been activated on document
    :param to_activate: list of operators to activate
    :return: true if there are more operators to activate
    """
    if not to_activate:
        return False
    for operator in to_activate:
        if operator not in activated:
            return True
    return False


def has_more_operators_to_check_greedy(activated, to_activate):
    """
    used for greedy algorithm
        :param activated: list of operators been activated on document
        :param to_activate: list of operators to activate
        :return: true if there are more operators to activate
        """
    index = 0
    while index != len(to_activate):

        if str(to_activate[index][2]) == '1':
            oper = (str(to_activate[index][2]), str(to_activate[index][3]), str(to_activate[index][4]),
                    to_activate[index][5])
        else:
            oper = (str(to_activate[index][2]), str(to_activate[index][3]), to_activate[index][5])
        if oper not in activated:
            return True

        index += 1
    return False


def experiment_on_document(path_for_tex, type_of_experiment, path_for_pdf, operators_max, models, paper_directory,
                          bibliograph_path, num_of_pages ):
    """
    Experiment on single document
    :param path_for_tex: path to tex file
    :param type_of_experiment: which experiment (out of 8) to run
    :param path_for_pdf: path to pdf file
    :param operators_max: number of maximum operators to run
    :param helper_directory: directory of locations
    :param models: models objects
    :return: result of the experiment

    Explanation of each experiment type, using psedu code - see Word File "search experiment"
    """
    original_height = read_single_file.order(path_for_pdf)
    new_number_of_pages= num_of_pages

    if type_of_experiment == "greedy-separate":
        operators_activated = 0
        operators_done = []
        cost = 0
        current_path_for_tex = path_for_tex
        iterations = 1
        last_page_height = original_height
        current_path_for_pdf = path_for_pdf
        gained = 0
        prediction = None
        reduced = False
        start = time.time()
        len_tree = -1
        iter = 0
        compilations = 0
        operators_applied = 0
        for i in range(operators_max):

            df1 , lidor= features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                         bibliograph_path,
                                                         "code/~/results/dct0",
                                                         "code/~/results/dct0",
                                                         "test", pd.DataFrame())
            df1 = df1.T
            df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                      'num_of_object'], axis=1, inplace=True)

            with open("code/~/results/dct0",
                      'rb') as dct_file:
                dct = pickle.load(dct_file)

            operators_list = greedy.perform_operators(dct, current_path_for_tex, lidor)
            found = False
            index = 0

            while found == False and index != len(operators_list):
                if str(operators_list[index][2]) == '1':
                    oper = (str(operators_list[index][2]), str(operators_list[index][3]), str(operators_list[index][4]),
                            operators_list[index][5])
                else:
                    oper = (str(operators_list[index][2]), str(operators_list[index][3]), operators_list[index][5])
                if oper in operators_done:
                    index += 1
                    continue
                try:
                    prediction = models[oper].predict(df1.to_numpy())[0]

                except Exception as e:
                    index += 1
                    continue
                if prediction and prediction > 0:
                    found = True
                    operators_done.append(oper)
                else:
                    index += 1

            if found:
                latex_after_operator = operators_list[index][1]
                current_path_for_tex = os.path.join(f"code/~/results/new_files/{paper_directory}", "new_0.tex")
                f = open(current_path_for_tex, "w")
                f.write(latex_after_operator)
                f.close()

                # cmd_line_act = 'tectonic -X compile ' + current_path_for_tex
                # os.system(cmd_line_act)
                dir_path = os.path.join("code/~/results/new_files", paper_directory)

                    # base_name = os.path.basename(after_path)
                    # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
                subprocess.run(['pdflatex', '-interaction=nonstopmode', os.path.basename(current_path_for_tex)], cwd=dir_path) #On mac
                compilations += 1
                operators_applied += 1

                current_path_for_pdf = current_path_for_tex.split(".tex")[0] + ".pdf"
                lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
                # make a new pdf only with 2 last pages:
                last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
                last_page_height = 0
                lines, pages = greedy.check_lines(last_pages_pdf)
                cost += operators_list[index][0]
                current_path_for_pdf=last_pages_pdf

                if (pages < 2 or new_number_of_pages< num_of_pages):
                    reduced = True
                    operators_activated += 1
                    
                    break
                iter += 1
            

            else:
                break
        end = time.time()

        time_taken = end - start
        gained = original_height - last_page_height

    elif type_of_experiment == "greedy-atOnce":
        operators_activated = 0
        operators_done = []
        index = 0
        cost = 0
        current_path_for_tex = path_for_tex
        iterations = 1
        last_page_height = original_height
        current_path_for_pdf = path_for_pdf
        gained = 0
        reduced = False
        start = time.time()
        len_tree = -1        
        iter = 0
        compilations = 0
        operators_applied = 0

        df1, lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                     bibliograph_path,
                                                     "code/~/results/dct0",
                                                     "code/~/results/dct0",
                                                     "test", pd.DataFrame())
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                  'num_of_object'], axis=1, inplace=True)
        with open("code/~/results/dct0",
                  'rb') as dct_file:
            dct = pickle.load(dct_file)

        original_operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)
        operators_list = []
        for index in range(len(original_operators_list)):
            if str(original_operators_list[index][2]) == '1':
                oper = (str(original_operators_list[index][2]), str(original_operators_list[index][3]),
                        str(original_operators_list[index][4]),
                        original_operators_list[index][5])
            else:
                oper = (str(original_operators_list[index][2]), str(original_operators_list[index][3]),
                        original_operators_list[index][5])
            if oper in operators_list or oper in operators_done:
                index += 1
                continue
            else:
                operators_list.append(oper)

        count_operators = 0
        new_operators_list = original_operators_list
        check_index = 0
        while count_operators < operators_max:
            if count_operators != 0:
                df1,lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                             bibliograph_path,
                                                             "code/~/results/dct0",
                                                             "code/~/results/dct0",
                                                             "test", pd.DataFrame())
                df1 = df1.T
                df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                          'num_of_object'], axis=1, inplace=True)

                with open("code/~/results/dct0",
                          'rb') as dct_file:
                    dct = pickle.load(dct_file)

                new_operators_list = greedy.perform_operators(dct, current_path_for_tex, lidor)

            if check_index == len(operators_list):
                break
            first_element = operators_list[check_index]

            found = False
            for j in range(len(new_operators_list)):
                first_element_new_list = new_operators_list[j]
                if str(first_element_new_list[2]) == '1':
                    oper = (
                        str(first_element_new_list[2]), str(first_element_new_list[3]), str(first_element_new_list[4]),
                        first_element_new_list[5])
                else:
                    oper = (str(first_element_new_list[2]), str(first_element_new_list[3]), first_element_new_list[5])

                if oper == first_element:
                    try:
                        prediction = models[oper].predict(df1.to_numpy())[0]

                    except Exception as e:
                        break
                    if prediction > 0:
                        found = True
                        break
            if found:
                operators_done.append(oper)
                latex_after_operator = first_element_new_list[1]
                current_path_for_tex = os.path.join(f"code/~/results/new_files/{paper_directory}", "new_1.tex")
                f = open(current_path_for_tex, "w")
                f.write(latex_after_operator)
                f.close()

                # cmd_line_act = 'tectonic -X compile ' + current_path_for_tex
                # os.system(cmd_line_act)
                dir_path = os.path.join("code/~/results/new_files", paper_directory)

                    # base_name = os.path.basename(after_path)
                    # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
                subprocess.run(['pdflatex', '-interaction=nonstopmode', os.path.basename(current_path_for_tex)], cwd=dir_path) #On mac
                compilations += 1
                operators_applied += operators_max
                
                current_path_for_pdf = current_path_for_tex.split(".tex")[0] + ".pdf"
                lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
                last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
                current_path_for_pdf = last_pages_pdf
                last_page_height = 0
                cost += first_element_new_list[0]
                iter += 1
                count_operators += 1
                check_index += 1
            else:
                check_index += 1

        lines, pages = greedy.check_lines(current_path_for_pdf)
        if (pages < 2 or new_number_of_pages< num_of_pages):
            reduced = True
        operators_activated = count_operators
        iterations=1
        end = time.time()
        time_taken = end - start
        gained = original_height - last_page_height

    elif type_of_experiment == "search-separate":
        operators_activated = 0
        cost = 0
        current_path_for_tex = path_for_tex
        iterations = 1
        last_page_height = original_height
        current_path_for_pdf = path_for_pdf
        gained = 0
        count_operators = 0
        reduced = False
        start = time.time()
        mse_dct = new_experiment_inferstructure.create_dict()
        max_len_tree = 0
        iter = 0
        compilations = 0
        operators_applied = 0
        operators_done = []
        
        for i in range(operators_max):
            if reduced:
                break
            df1, lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                         bibliograph_path,
                                                         "code/~/results/dct0",
                                                          "code/~/results/dct0",
                                                         "test", pd.DataFrame())
            df1 = df1.T
            df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                      'num_of_object'], axis=1, inplace=True)

            with open(  "code/~/results/dct0",
                      'rb') as dct_file:
                dct = pickle.load(dct_file)

            original_operators_list = greedy.perform_operators(dct,  current_path_for_tex,lidor)
            results, len_tree ,current_depth = search_algorithms_for_experiment.run_search(tree_depth=operators_max,
                                                                            file_name=current_path_for_tex, last_pages=current_path_for_pdf,
                                                                            algorithm_search=search_algorithms_for_experiment.dijkstra,
                                                                            models=models, mse_dct=mse_dct, bib_path=bibliograph_path, operators_list=original_operators_list)
            if not results:
                break
            first_element = results[0]
            max_len_tree = max(max_len_tree, len_tree)

            for j in range(len(original_operators_list)):
                first_element_new_list = original_operators_list[j]
                if str(first_element_new_list[2]) == '1':
                    oper = (
                        str(first_element_new_list[2]), str(first_element_new_list[3]), str(first_element_new_list[4]),
                        first_element_new_list[5])
                else:
                    oper = (str(first_element_new_list[2]), str(first_element_new_list[3]), first_element_new_list[5])
                if oper in operators_done:
                    continue
                if oper == first_element:
                    operators_done.append(oper)
                    latex_after_operator = first_element_new_list[1]
                    current_path_for_tex = os.path.join(f"code/~/results/new_files/{paper_directory}", "new_2.tex")
                    f = open(current_path_for_tex, "w")
                    f.write(latex_after_operator)
                    f.close()

                    # cmd_line_act = 'tectonic -X compile ' + current_path_for_tex
                    # os.system(cmd_line_act)
                    dir_path = os.path.join("code/~/results/new_files", paper_directory)

                    # base_name = os.path.basename(after_path)
                    # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
                    subprocess.run(['pdflatex', '-interaction=nonstopmode', os.path.basename(current_path_for_tex)], cwd=dir_path) #On mac
                    compilations += 1
                    operators_applied += 1

                    current_path_for_pdf = current_path_for_tex.split(".tex")[0] + ".pdf"
                     #todo check why this takes so long
                    cost += first_element_new_list[0]
                    
                    lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
                    # make a new pdf only with 2 last pages:
                    last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
                    last_page_height = 0
                    lines, pages = greedy.check_lines(last_pages_pdf)
                    
                    if (pages < 2 or new_number_of_pages< num_of_pages):
                        reduced = True
                        operators_activated += 1
                        break
                    iter += 1
                    current_path_for_pdf = last_pages_pdf

        end = time.time()
        time_taken = end - start
        gained = original_height - last_page_height
        len_tree = max_len_tree

    elif type_of_experiment == "search-atOnce":
        operators_activated = 0
        cost = 0
        current_path_for_tex = path_for_tex
        iterations = 1
        last_page_height = original_height
        current_path_for_pdf = path_for_pdf
        gained = 0
        count_operators = 0
        reduced = False
        start = time.time()
        iter = 0
        compilations = 0
        operators_applied = 0
        operators_done = []

        df1, lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                    bibliograph_path,
                                                    "code/~/results/dct0",
                                                    "code/~/results/dct0",
                                                    "test", pd.DataFrame())   
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                'num_of_object'], axis=1, inplace=True)

        with open( "code/~/results/dct0",'rb') as dct_file:
            dct = pickle.load(dct_file)

        original_operators_list = greedy.perform_operators(dct,  current_path_for_tex,lidor)
        mse_dct = new_experiment_inferstructure.create_dict()
        results, len_tree,current_depth = search_algorithms_for_experiment.run_search(tree_depth=operators_max,
                                                                        file_name=current_path_for_tex,last_pages=current_path_for_pdf,
                                                                        algorithm_search=search_algorithms_for_experiment.dijkstra,
                                                                      models=models, mse_dct=mse_dct , bib_path=bibliograph_path, operators_list=original_operators_list)
        if results:    
            print(results)
            for operator in results:
                if reduced:
                    break
                df1, lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                            bibliograph_path,
                                                            "code/~/results/dct0",
                                                            "code/~/results/dct0",
                                                            "test", pd.DataFrame())   
                df1 = df1.T
                df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                        'num_of_object'], axis=1, inplace=True)

                with open( "code/~/results/dct0",
                        'rb') as dct_file:
                    dct = pickle.load(dct_file)

                original_operators_list = greedy.perform_operators(dct,  current_path_for_tex,lidor)
                for j in range(len(original_operators_list)):
                    first_element_new_list = original_operators_list[j]
                    if str(first_element_new_list[2]) == '1':
                        oper = (
                            str(first_element_new_list[2]), str(first_element_new_list[3]), str(first_element_new_list[4]),
                            first_element_new_list[5])
                    else:
                        oper = (str(first_element_new_list[2]), str(first_element_new_list[3]), first_element_new_list[5])
                    if oper in operators_done:
                        continue
                    print(f"oper:{oper}")
                    print(operator)
                    if oper == operator:
                        operators_done.append(oper)
                        latex_after_operator = first_element_new_list[1]
                        current_path_for_tex = os.path.join(f"code/~/results/new_files/{paper_directory}", "new_3.tex")
                        f = open(current_path_for_tex, "w")
                        f.write(latex_after_operator)
                        f.close()

                        # cmd_line_act = 'tectonic -X compile ' + current_path_for_tex
                        # os.system(cmd_line_act)
                        dir_path = os.path.join("code/~/results/new_files", paper_directory)

                        # base_name = os.path.basename(after_path)
                        # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
                        subprocess.run(['pdflatex', '-interaction=nonstopmode', os.path.basename(current_path_for_tex)], cwd=dir_path) #On mac
                        compilations += 1
                        operators_applied += operators_max
                        current_path_for_pdf = current_path_for_tex.split(".tex")[0] + ".pdf"
                        lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
                        last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
                        current_path_for_pdf = last_pages_pdf
                        last_page_height = 0
                        cost += first_element_new_list[0]
                        iter += 1
                        count_operators += 1
                        if (new_number_of_pages< num_of_pages):
                            reduced = True
                        break

        # if (last_page_height < original_height or last_page_height == 0):
        #     reduced = True
        # lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
        # make a new pdf only with 2 last pages:
        # last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
        lines, pages = greedy.check_lines(current_path_for_pdf)
        if (pages < 2 or new_number_of_pages< num_of_pages):
            reduced = True


        iterations = 1
        operators_activated = count_operators

        end = time.time()
        time_taken = end - start
        gained = original_height - last_page_height

    elif type_of_experiment == "loop-greedy-separate":
        operators_activated = 0
        operators_done = []
        index = 0
        cost = 0
        current_path_for_tex = path_for_tex
        iterations = 0
        last_page_height = original_height
        current_path_for_pdf = path_for_pdf
        gained = 0
        reduced = False
        start = time.time()
        len_tree = -1
        count_operators = 0
        iter=0
        compilations = 0
        operators_applied = 0

        df1 , lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                     bibliograph_path,
                                                    "code/~/results/dct0",
                                                     "code/~/results/dct0",
                                                     "test", pd.DataFrame())
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                  'num_of_object'], axis=1, inplace=True)

        with open( "code/~/results/dct0",
                      'rb') as dct_file:
                dct = pickle.load(dct_file)

        operators_list = greedy.perform_operators(dct, current_path_for_tex, lidor)
        while reduced == False and has_more_operators_to_check_greedy(operators_done,
                                                                      operators_list) == True and iterations < 10:
            iterations += 1
            for i in range(operators_max):
                found = False
                while found == False and index != len(operators_list):
                    if str(operators_list[index][2]) == '1':
                        oper = (
                            str(operators_list[index][2]), str(operators_list[index][3]), str(operators_list[index][4]),
                            operators_list[index][5])
                    else:
                        oper = (str(operators_list[index][2]), str(operators_list[index][3]), operators_list[index][5])
                    if oper in operators_done:
                        index += 1
                        continue
                    try:
                        prediction = models[oper].predict(df1.to_numpy())[0]

                    except Exception as e:
                        index += 1
                        continue
                    if prediction > 0:
                        found = True

                    else:
                        index += 1

                if found:
                    operators_done.append(oper)
                    latex_after_operator = operators_list[index][1]
                    current_path_for_tex = os.path.join(f"code/~/results/new_files/{paper_directory}", "new_4.tex")
                    f = open(current_path_for_tex, "w")
                    f.write(latex_after_operator)
                    f.close()

                    # cmd_line_act = 'tectonic -X compile ' + current_path_for_tex
                    # os.system(cmd_line_act)
                    dir_path = os.path.join("code/~/results/new_files", paper_directory)

                    # base_name = os.path.basename(after_path)
                    # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
                    subprocess.run(['pdflatex', '-interaction=nonstopmode', os.path.basename(current_path_for_tex)], cwd=dir_path) #On mac
                    compilations +=1
                    operators_applied +=1

                    current_path_for_pdf = current_path_for_tex.split(".tex")[0] + ".pdf"
                    cost += operators_list[index][0]
                    
                    lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
                    # make a new pdf only with 2 last pages:
                    last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
                    last_page_height =0
                    lines, pages = greedy.check_lines(last_pages_pdf)
                    current_path_for_pdf = last_pages_pdf
                    if (pages < 2 or new_number_of_pages< num_of_pages):
                        reduced = True
                        count_operators += 1
                        break
                    iter += 1
                else:
                    break
                df1 , lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                             bibliograph_path,
                                                             "code/~/results/dct0",
                                                             "code/~/results/dct0",
                                                             "test", pd.DataFrame())
                df1 = df1.T
                df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                          'num_of_object'], axis=1, inplace=True)

                with open("code/~/results/dct0",
                          'rb') as dct_file:
                    dct = pickle.load(dct_file)

                operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)
                index=0

        operators_activated = count_operators
        end = time.time()
        time_taken = end - start
        gained = original_height - last_page_height

    elif type_of_experiment == "loop-greedy-atOnce":
        operators_activated = 0
        operators_done = []
        index = 0
        cost = 0
        current_path_for_tex = path_for_tex
        iterations = 0
        last_page_height = original_height
        current_path_for_pdf = path_for_pdf
        gained = 0
        reduced = False
        start = time.time()
        count_operators = 0
        len_tree = -1
        compilations = 0
        operators_applied = 0

        df1 , lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                     bibliograph_path,
                                                     "code/~/results/dct0",
                                                     "code/~/results/dct0",
                                                     "test", pd.DataFrame())
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                  'num_of_object'], axis=1, inplace=True)
        with open( "code/~/results/dct0",
                      'rb') as dct_file:
                dct = pickle.load(dct_file)

        original_operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)
        operators_list = []
        iter = 0
        while reduced == False and has_more_operators_to_check_greedy(operators_done,
                                                                      original_operators_list) == True and iterations < 10:
            iterations += 1

            for index in range(len(original_operators_list)):
                if str(original_operators_list[index][2]) == '1':
                    oper = (str(original_operators_list[index][2]), str(original_operators_list[index][3]),
                            str(original_operators_list[index][4]),
                            original_operators_list[index][5])
                else:
                    oper = (str(original_operators_list[index][2]), str(original_operators_list[index][3]),
                            original_operators_list[index][5])
                if oper in operators_list or oper in operators_done:
                    index += 1
                    continue
                else:
                    operators_list.append(oper)

            count_operators = 0
            new_operators_list = original_operators_list
            check_index = 0
            

            while count_operators < operators_max:
                if count_operators != 0:
                    df1, lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                                 bibliograph_path,
                                                                 "code/~/results/dct0",
                                                                 "code/~/results/dct0",
                                                                 "test", pd.DataFrame())
                    df1 = df1.T
                    df1.drop(
                        ['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                         'num_of_object'], axis=1, inplace=True)

                    with open("code/~/results/dct0",
                              'rb') as dct_file:
                        dct = pickle.load(dct_file)

                    new_operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)

                if check_index == len(operators_list):
                    break
                first_element = operators_list[check_index]

                found = False
                for j in range(len(new_operators_list)):
                    first_element_new_list = new_operators_list[j]
                    if str(first_element_new_list[2]) == '1':
                        oper = (
                            str(first_element_new_list[2]), str(first_element_new_list[3]),
                            str(first_element_new_list[4]),
                            first_element_new_list[5])
                    else:
                        oper = (
                            str(first_element_new_list[2]), str(first_element_new_list[3]), first_element_new_list[5])

                    if oper == first_element:
                        try:
                            prediction = models[oper].predict(df1.to_numpy())[0]

                        except Exception as e:
                            break
                        if prediction > 0:
                            found = True
                            break
                
                if found:
                    operators_done.append(oper)
                    latex_after_operator = first_element_new_list[1]
                    current_path_for_tex = os.path.join(f"code/~/results/new_files/{paper_directory}", "new_5.tex")

                    f = open(current_path_for_tex, "w")
                    f.write(latex_after_operator)
                    f.close()

                    # cmd_line_act = 'tectonic -X compile ' + current_path_for_tex
                    # os.system(cmd_line_act)
                    dir_path = os.path.join("code/~/results/new_files", paper_directory)

                    # base_name = os.path.basename(after_path)
                    # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
                    subprocess.run(['pdflatex', '-interaction=nonstopmode', os.path.basename(current_path_for_tex)], cwd=dir_path) #On mac
                    compilations += 1
                    operators_applied += operators_max


                    current_path_for_pdf = current_path_for_tex.split(".tex")[0] + ".pdf"
                    lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
                    # make a new pdf only with 2 last pages:
                    last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
                    last_page_height = 0
                    
                    current_path_for_pdf = last_pages_pdf
                    iter += 1
                    cost += first_element_new_list[0]

                    count_operators += 1
                    check_index += 1
                else:
                    check_index += 1
                    operators_done.append(oper)
                lines, pages = greedy.check_lines(current_path_for_pdf)
                if (pages < 2 or new_number_of_pages< num_of_pages):
                    reduced = True

                    break
            lines, pages = greedy.check_lines(current_path_for_pdf)
            if (pages < 2 or new_number_of_pages< num_of_pages):
                reduced = True

                break
            df1 , lidor = features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                         bibliograph_path,
                                                         "code/~/results/dct0",
                                                         "code/~/results/dct0",
                                                         "test", pd.DataFrame())
            df1 = df1.T
            df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                      'num_of_object'], axis=1, inplace=True)
            with open("code/~/results/dct0",
                      'rb') as dct_file:
                dct = pickle.load(dct_file)

            original_operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)
            operators_list = []

        operators_activated = count_operators

        end = time.time()
        time_taken = end - start
        gained = original_height - last_page_height

    elif type_of_experiment == "loop-search-atOnce":
        cost = 0
        current_path_for_tex = path_for_tex
        iterations = 0
        last_page_height = original_height
        current_path_for_pdf = path_for_pdf
        gained = 0
        count_operators = 0
        reduced = False
        start = time.time()
        operators_done = []
        compilations = 0
        operators_applied = 0
        
        df1 , lidor= features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                            bibliograph_path,
                                            "code/~/results/dct0",
                                            "code/~/results/dct0",
                                            "test", pd.DataFrame())
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                'num_of_object'], axis=1, inplace=True)

        with open("code/~/results/dct0",
                'rb') as dct_file:
            dct = pickle.load(dct_file)

        original_operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)
        mse_dct = new_experiment_inferstructure.create_dict()
        results, len_tree ,current_depth = search_algorithms_for_experiment.run_search(tree_depth=operators_max,
                                                                        file_name=current_path_for_tex,last_pages=current_path_for_pdf,
                                                                        algorithm_search=search_algorithms_for_experiment.dijkstra,
                                                                     models=models, mse_dct=mse_dct, bib_path=bibliograph_path, operators_list=original_operators_list)

        iter = 0
        if results:
            while reduced == False and has_more_operators_to_check(operators_done, results) == True and iterations < 10:

                iterations += 1
                for operator in results:
                    if reduced or not has_more_operators_to_check(operators_done, results):
                        break
                    df1 , lidor= features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                                bibliograph_path,
                                                                "code/~/results/dct0",
                                                                "code/~/results/dct0",
                                                                "test", pd.DataFrame())
                    df1 = df1.T
                    df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                            'num_of_object'], axis=1, inplace=True)

                    with open("code/~/results/dct0",
                            'rb') as dct_file:
                        dct = pickle.load(dct_file)

                    original_operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)

                    for j in range(len(original_operators_list)):
                        first_element_new_list = original_operators_list[j]
                        if str(first_element_new_list[2]) == '1':
                            oper = (
                                str(first_element_new_list[2]), str(first_element_new_list[3]),
                                str(first_element_new_list[4]),
                                first_element_new_list[5])
                        else:
                            oper = (
                                str(first_element_new_list[2]), str(first_element_new_list[3]), first_element_new_list[5])
                        if oper in operators_done:
                            continue
                        if oper == operator:
                            operators_done.append(oper)
                            latex_after_operator = first_element_new_list[1]
                            current_path_for_tex = os.path.join(f"code/~/results/new_files/{paper_directory}", "new_7.tex")
                            f = open(current_path_for_tex, "w")
                            f.write(latex_after_operator)
                            f.close()

                            # cmd_line_act = 'tectonic -X compile ' + current_path_for_tex
                            # os.system(cmd_line_act)
                            dir_path = os.path.join("code/~/results/new_files", paper_directory)
                            subprocess.run(['pdflatex', '-interaction=nonstopmode', os.path.basename(current_path_for_tex)], cwd=dir_path) #On mac
                            compilations += 1
                            operators_applied += operators_max
                            current_path_for_pdf = current_path_for_tex.split(".tex")[0] + ".pdf"
                            lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
                            # make a new pdf only with 2 last pages:
                            last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
                            last_page_height =0
                            
                            current_path_for_pdf = last_pages_pdf
                            cost += first_element_new_list[0]
                            iter += 1

                            count_operators += 1
                            break
                    lines, pages = greedy.check_lines(current_path_for_pdf)
                    if (pages < 2 or new_number_of_pages< num_of_pages):
                        reduced = True
                        break
                lines, pages = greedy.check_lines(current_path_for_pdf)
                if (pages < 2 or new_number_of_pages< num_of_pages):
                    reduced = True
                    if current_depth<operators_max and current_depth!=0:
                        operators_applied -= operators_max-current_depth
                    break
                if current_depth<operators_max and current_depth!=0:
                    operators_applied -= operators_max-current_depth
                    break
                results, len_tree ,current_depth = search_algorithms_for_experiment.run_search(tree_depth=operators_max,
                                                                                file_name=current_path_for_tex,last_pages=current_path_for_pdf,
                                                                                algorithm_search=search_algorithms_for_experiment.dijkstra,
                                                                                models=models, mse_dct=mse_dct, bib_path=bibliograph_path, operators_list=original_operators_list)
                if not results:
                    break

        end = time.time()
        time_taken = end - start
        gained = original_height - last_page_height
        operators_activated = count_operators

    elif type_of_experiment == "loop-search-separate":
        cost = 0
        current_path_for_tex = path_for_tex
        iterations = 0
        last_page_height = original_height
        current_path_for_pdf = path_for_pdf
        gained = 0
        count_operators = 0
        reduced = False
        start = time.time()
        mse_dct = new_experiment_inferstructure.create_dict()
        max_len_tree = 0
        operators_done = []
        compilations = 0
        operators_applied = 0
        
        df1,lidor= features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                            bibliograph_path,
                                            "code/~/results/dct0",
                                            "code/~/results/dct0",
                                            "test", pd.DataFrame())
        df1 = df1.T
        df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                'num_of_object'], axis=1, inplace=True)

        with open("code/~/results/dct0",
                'rb') as dct_file:
            dct = pickle.load(dct_file)

        original_operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)
        results, len_tree,current_depth = search_algorithms_for_experiment.run_search(tree_depth=operators_max,
                                                                        file_name=current_path_for_tex,last_pages=current_path_for_pdf,
                                                                        algorithm_search=search_algorithms_for_experiment.dijkstra,
                                                                        models=models, mse_dct=mse_dct , bib_path=bibliograph_path, operators_list=original_operators_list)
        iter=0
        if results:
            while reduced == False and has_more_operators_to_check(operators_done, results) == True and iterations < 10:
                iterations += 1
                if not results:
                    break
                for i in range(operators_max):
                    if reduced==True:
                        break
                    first_element = results[i]
                    if first_element in operators_done:
                        continue

                    max_len_tree = max(max_len_tree, len_tree)
                    df1,lidor= features_extraction_single_paper.run_feature_extraction(current_path_for_tex, current_path_for_pdf,
                                                                bibliograph_path,
                                                                "code/~/results/dct0",
                                                                "code/~/results/dct0",
                                                                "test", pd.DataFrame())
                    df1 = df1.T
                    df1.drop(['herustica', 'binary_class', 'lines_we_gained', 'y_gained', 'type', 'value', 'object_used_on',
                            'num_of_object'], axis=1, inplace=True)

                    with open("code/~/results/dct0",
                            'rb') as dct_file:
                        dct = pickle.load(dct_file)

                    original_operators_list = greedy.perform_operators(dct,  current_path_for_tex, lidor)
                    found = False
                    for j in range(len(original_operators_list)):
                        first_element_new_list = original_operators_list[j]
                        if str(first_element_new_list[2]) == '1':
                            oper = (
                                str(first_element_new_list[2]), str(first_element_new_list[3]),
                                str(first_element_new_list[4]),
                                first_element_new_list[5])
                        else:
                            oper = (
                                str(first_element_new_list[2]), str(first_element_new_list[3]), first_element_new_list[5])

                        if oper == first_element:
                            found = True
                            operators_done.append(oper)
                            latex_after_operator = first_element_new_list[1]
                            current_path_for_tex = os.path.join(f"code/~/results/new_files/{paper_directory}", "new_6.tex")
                            f = open(current_path_for_tex, "w")
                            f.write(latex_after_operator)
                            f.close()

                            # cmd_line_act = 'tectonic -X compile ' + current_path_for_tex
                            # os.system(cmd_line_act)
                            dir_path = os.path.join("code/~/results/new_files", paper_directory)
                            # base_name = os.path.basename(after_path)
                            # subprocess.run(['pdflatex.exe', base_name], cwd=dir_path) #On windows
                            subprocess.run(['pdflatex', '-interaction=nonstopmode', os.path.basename(current_path_for_tex)], cwd=dir_path) #On mac
                            compilations += 1
                            operators_applied += 1

                            current_path_for_pdf = current_path_for_tex.split(".tex")[0] + ".pdf"
                            lines, new_number_of_pages= greedy.check_lines(current_path_for_pdf)
                            # make a new pdf only with 2 last pages:
                            last_pages_pdf= handle_full_paper.copy_last_pages(current_path_for_pdf,2,iter)
                            last_page_height = 0
                            lines, pages = greedy.check_lines(last_pages_pdf)
                            current_path_for_pdf=last_pages_pdf
                            cost += first_element_new_list[0]
                            iter += 1
                            if (pages < 2 or new_number_of_pages< num_of_pages):
                                reduced = True
                                count_operators += 1
                            break

                    # if (last_page_height == 0):
                    #     break
                    if reduced == True or found == True:
                        break
                    if found == False:
                        operators_done.append(first_element)
                        continue

                if reduced == True:
                    break
                results, len_tree ,current_depth = search_algorithms_for_experiment.run_search(tree_depth=operators_max,
                                                                                file_name=current_path_for_tex,last_pages=current_path_for_pdf,
                                                                                algorithm_search=search_algorithms_for_experiment.dijkstra,
                                                                                models=models, mse_dct=mse_dct, bib_path=bibliograph_path, operators_list=original_operators_list)
                if not results:
                    break

        end = time.time()
        time_taken = end - start
        gained = original_height - last_page_height
        operators_activated = count_operators
        len_tree = max_len_tree

    return (
        original_height, last_page_height, gained, time_taken, reduced, cost, iterations, len_tree, compilations,operators_applied)


def results(path_for_docs, type_of_experiment, operators_max, models, bibliograph_path):
    """
    Run experiments on all documents in path_for_docs
    :param path_for_docs: directory of tex files and their corresponding pdf
    :param filename: file to run
    :param type_of_experiment: which experiment to run
    :param operators_max: maxmium number of operators
    :param helper_directory: where to write the new activated files
    :param models: models objects
    :return:
    """

    results_data = []

    # path_to_latex = ""
    # path_to_pdf = ""
    # file_path = os.path.join(path_for_docs, filename + ".pdf")
    # if os.path.isfile(file_path):
    #     path_to_pdf = file_path

    # file_path = os.path.join(path_for_docs, filename + ".tex")
    # print(file_path)
    # if os.path.isfile(file_path):
    #     path_to_latex = file_path
    directory = path_for_docs
    
    idx = 0
    done = 1
    #get last name of files_dir
    dir_name = path_for_docs.split('\\')[-1]
    for paper_dir in os.scandir(directory):
        print("paper_dir:", paper_dir.name)
        names = []
        paper_directory = paper_dir.name
        idx += 1
        path_to_latex = None
        path_to_pdf = None
        for file in os.scandir(paper_dir):
            if file.is_file():
                source_dir = os.path.join("data/files", paper_directory)
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
                    handle_full_paper.remove_comments(path_to_latex)
                if path_to_pdf:
                    num_of_pages = greedy.check_lines(path_to_pdf)[1]
                    last_pages_pdf_path = handle_full_paper.copy_last_pages(path_to_pdf,2, 0)

            elif file.is_dir():
                # move all the directories in 'code/greedy_from_machine/files' directory to 'code/~/results/new_files' directory
                source_dir = os.path.join("data/files", paper_directory)
                destination_dir = os.path.join("code/~/results/new_files", paper_directory)
                os.makedirs(destination_dir, exist_ok=True)
                source_path = file.path
                destination_path = os.path.join(destination_dir, file.name)
                # if directory already exists in destination, do not copy it
                if not os.path.exists(destination_path):
                    shutil.copytree(source_path, destination_path)

    # lines, pages = greedy.check_lines(path_to_pdf)

    # if lines < 2:
    #     # print("Less then 2 lines")
    #     return {}
    # if pages < 2:
    #     # print("Less then 2 pages")
    #     return {}
        try:
            original_height, last_page_height, gained, time_taken, reduced, cost, iterations, len_tree, compilations,operators_applied = experiment_on_document(
                    path_to_latex, type_of_experiment, last_pages_pdf_path, operators_max, models,paper_directory, bibliograph_path,num_of_pages)
            results_data.append(
                    {"docName": paper_directory, "experiment_type": type_of_experiment, "operators_max": operators_max,
                    "iterations": iterations, "reduced": reduced,
                    "original_height": original_height, "last_page_height": last_page_height, "gained": gained,
                    "cost": cost, "time_taken": time_taken, "max_len_tree": len_tree, "compilations": compilations,"operators_applied":operators_applied})
            print(results_data[-1])
        except Exception as e:
            traceback.print_exc()
            print(f"Error in {paper_directory}: {e}")
            with open("code/~/results/error_files.txt", "a") as f:
                f.write(f"{paper_directory}, {type_of_experiment}, {e}\n")
            continue
    results_df = pd.DataFrame.from_records(results_data)
    results_df.to_csv(path_for_write_csv, index=False)

    # return results_data


if __name__ == "__main__":
    # filename = sys.argv[1]
    type_of_experiment = int(sys.argv[1])
    operators_max = int(sys.argv[2])
    path_for_docs = sys.argv[3]
    path_for_write_csv = sys.argv[4]
    # helper_directory = sys.argv[6]
    bibliograph_path = sys.argv[5]
    models_path_cat = sys.argv[6]
    models_path_xgb = sys.argv[7]

    if type_of_experiment == 0:
        type_of_experiment = "greedy-separate"
    elif type_of_experiment == 1:
        type_of_experiment = "greedy-atOnce"
    elif type_of_experiment == 2:
        type_of_experiment = "search-separate"
    elif type_of_experiment == 3:
        type_of_experiment = "search-atOnce"
    elif type_of_experiment == 4:
        type_of_experiment = "loop-greedy-separate"
    elif type_of_experiment == 5:
        type_of_experiment = "loop-greedy-atOnce"
    elif type_of_experiment == 6:
        type_of_experiment = "loop-search-separate"
    elif type_of_experiment == 7:
        type_of_experiment = "loop-search-atOnce"

    # loading models
    if type_of_experiment.find("search") != -1:
        models = reload_models.load_regression_models_cat(models_path_cat)
    else:
        models = greedy.load_models(models_path_xgb)

    results(path_for_docs, type_of_experiment, operators_max, models,
                           bibliograph_path)

    # writing results to csv
    # results_df = pd.DataFrame.from_records(results_data)
    # results_df.to_csv(path_for_write_csv, index=False)
    ###fdfdfdfd
    #FDD