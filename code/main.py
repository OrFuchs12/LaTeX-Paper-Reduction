import subprocess
import using_operators
import re
import pickle
import read_single_file
import os
import time
import sys
import pandas

def run(path_to_original_excel,created_excel_path,path_to_excel_dct,path_to_latex_files,path_to_file):
    """
    Calls the 'using_operators.perform_operators' function to receive all files of operators. Then activate
    each operator, and creates labels.
    Finally, writes a new csv file

    :param path_to_original_excel: Excel path of feature_extraction
    :param created_excel_path: path to write new file
    :param path_to_excel_dct: path to pickle of result from feature extraction process
    :param path_to_latex_files: path to folder of tex files
    :param path_to_file: path to write updated file with operator
    """

    df = pandas.read_csv(path_to_original_excel, index_col=0)
    df = df.T
    old_columns_list = list(df)
    index_doc_for_operators = 0
    files_created = {}
    os.system(f"echo 1")
    for column in old_columns_list: #column means file
        os.system(f"echo {column}")
        old_y = df.at['ending_y_of_doc', column] #ending_y_of_doc means the height of second page
        if old_y == 0:
            continue
        try:
            with open(path_to_excel_dct + column, 'rb') as dct_file:
                dct = pickle.load(dct_file) #load the pickle
        except Exception as e:
            print(e)
            continue

        latex_path = path_to_latex_files + column + ".tex"
        os.system(f"echo 2")
        files_created_small = using_operators.perform_operators(dct, column, latex_path, path_to_file) #get list of files of activated operators
        os.system(f"echo 3")
        files_created[column] = files_created_small
        # print(files_created)
        index_doc_for_operators += 1
        # except Exception as e:
        #     print(e)
        #     print("here2")
        #     continue
    os.system(f"echo 4")
    index_of_new_doc = 0
    index_doc = 0

    counter_problems = 0
    max_counter=0
    cmd_line_create_pdf = 'tectonic -X compile '
    try:
        cmd_line_del_tex = ""
        for column in old_columns_list:
            try:
                old_y = df.at['ending_y_of_doc', column]
                if old_y == 0:
                    continue

                pdf_path = path_to_latex_files + column + ".pdf"

                if os.path.exists(pdf_path) == False:
                    old_y = read_single_file.order(pdf_path)

                os.system(f"echo 5")
                binary = 0
                if column in files_created: #for each paper
                    max_counter=0
                    for i in files_created[column]:  # [(filename,pdfname,object,vspace(operator),vspace(operator)value)]
                        max_counter+=1

                        os.system(f"echo {i}")
                        # cmd_line_act = cmd_line_create_pdf + i[0]
                        
                        os.system(f"echo {i}")
                        row_name = i[1][0]
                        try:
                            subprocess.run(['pdflatex', '-interaction=nonstopmode', i[1][0].split("/")[-1]], cwd="results/oper_files/files/") #On mac
                            # df[column + '_with_operator' + str(index_of_new_doc)] = df.loc[:,column]  # create a new column
                            df[row_name] = df.loc[:,column] 
                            for op_num in range(2):

                                os.system(f"echo 7")
                                if (i[op_num][3] == 'vspace'):
                                    df.at['type'+str(op_num), row_name] = 1  # switch to i[3] when it is all set
                                elif (i[op_num][3] == 'change_figure_size'):
                                    df.at['type'+str(op_num), row_name] = 2  # switch to i[3] when it is all set
                                elif (i[op_num][3] == 'change_algorithm_size'):
                                    df.at['type'+str(op_num), row_name] = 3  # switch to i[3] when it is all set
                                elif (i[op_num][3] == 'convert_enum'):
                                    df.at['type'+str(op_num), row_name] = 4  # switch to i[3] when it is all set
                                elif (i[op_num][3] == 'remove_par_tag'):
                                    df.at['type'+str(op_num), row_name] = 5  # switch to i[3] when it is all set
                                elif (i[op_num][3] == 'combine_two_paragraphs'):
                                    df.at['type'+str(op_num), row_name] = 6  # switch to i[3] when it is all set
                                elif (i[op_num][3] == 'change_table_size'):
                                    df.at['type'+str(op_num), row_name] = 7  # switch to i[3] when it is all set
                                elif (i[op_num][3] == 'remove_special_positional_chars'):
                                    df.at['type'+str(op_num), row_name] = 8  # switch to i[3] when it is all set
                                elif (i[op_num][3] == 'remove_last_2_words'):
                                    df.at['type'+str(op_num), row_name] = 9  # switch to i[3] when it is all set
                                df.at['value'+str(op_num), row_name] = i[op_num][4]
                                df.at['object_used_on'+str(op_num), row_name] = i[op_num][2]
                                df.at['num_of_object'+str(op_num), row_name] = \
                                    re.findall(r'\d+', str(i[op_num][5]))[0]
                                df.at['herustica'+str(op_num), row_name] = i[op_num][6]
                            df.at['ending_y_of_doc', row_name] = old_y
                            index = 0
                            os.system(f"echo 8")
                            os.system(f"echo {i[1]}")
                            x = read_single_file.order(i[1][1]) #height of second page after operator activation
                            os.system(f"echo 9")
                            if (x == 0):  # the new paper has only_one_page
                                binary = 1
                                y_gained = old_y #height of previous second page
                                lines_we_get = int(old_y / 10)

                            else: # the new paper has two pages
                                if x < old_y: #height of new paper's second page is smaller than previous paper's second page
                                    binary = 1
                                    y_gained = old_y - x
                                    lines_we_get = int((old_y - y_gained) / 10)
                                else: #height of new paper's second page is larger than previous paper's second page
                                    binary = 0
                                    y_gained = 0
                                    lines_we_get = 0


                            df.at['y_gained', row_name] = y_gained
                            df.at['lines_we_gained', row_name] = lines_we_get
                            df.at['binary_class', row_name] = binary
                            index_of_new_doc += 1
                            os.system(f"echo 10")
                            cmd_line_del_pdf = ""
                            # cmd_line_act = i[1]
                            # os.remove(cmd_line_act)
                            os.system(f"echo 11")
                            # cmd_line_act = i[0]
                            # os.remove(cmd_line_act)
                            os.system(f"echo 12")
                        except Exception as e:
                            print(e)
                            print("here4")
                            df.at['y_gained', row_name] = -1
                            df.at['lines_we_gained', row_name] = -1
                            df.at['binary_class', row_name] = -1
                            df.at['type', row_name] = 9
                            
                            for opt_num in range(2):
                                df.at['value'+ str(opt_num), row_name] = i[opt_num][4]
                                df.at['object_used_on'+ str(opt_num), row_name] = i[opt_num][2]
                                df.at['num_of_object'+ str(opt_num), row_name] = \
                                    re.findall(r'\d+', str(i[opt_num][5]))[0]
                                df.at['herustica'+ str(opt_num), row_name] = i[opt_num][6]
                            df.at['ending_y_of_doc', row_name] = old_y
                            # try:
                            #     # cmd_line_act = i[1]
                            #     # os.remove(cmd_line_act)

                            # except Exception as e:
                            #     print(e)
                            #     print("here5")
                            #     counter_problems += 1
            except Exception as e:
                print(e)
                
            index_doc += 1
            df = df.drop(column, axis=1) #remove original row

        os.system(f"echo 13")
        df2 = df.T
        # remove "['type', 'value', 'object_used_on', 'num_of_object']" columns
        df2 = df2.drop('type', axis=1)
        df2 = df2.drop('value', axis=1)
        df2 = df2.drop('object_used_on', axis=1)
        df2 = df2.drop('num_of_object', axis=1)
        df2 = df2.drop('herustica', axis=1)
        df2.to_csv(created_excel_path)
        os.system(f"echo 14")
    except Exception as e:
        print(e)
        print("here")
        df2 = df.T
        df2.to_csv(created_excel_path)

if __name__ == "__main__":
    path_to_original_excel = sys.argv[1]
    created_excel_path = sys.argv[2]

    path_to_excel_dct = sys.argv[3]
    path_to_latex_files = sys.argv[4]
    path_to_file = sys.argv[5]
    # max_number_of_operators= int(sys.argv[6])

    run(path_to_original_excel,created_excel_path,path_to_excel_dct,path_to_latex_files,path_to_file)

