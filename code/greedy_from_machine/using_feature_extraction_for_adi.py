import using_operators_for_adi
import re
import pickle
import read_single_file
import os
import time
import sys
import pandas

if __name__ == "__main__":
    path_to_original_excel = sys.argv[1]
    created_excel_path = sys.argv[2]

    path_to_lidor_dct = sys.argv[3]
    path_to_latex_files = sys.argv[4]
    path_to_file = sys.argv[5]
    # print(os.path.exists(created_excel_path))
    if os.path.exists(created_excel_path) == False:

        df = pandas.read_csv(path_to_original_excel, index_col=0)
        df = df.T
        old_columns_list = list(df)
        index_doc_for_operators = 0
        files_created = {}
        os.system(f"echo 1")
        for column in old_columns_list:
            os.system(f"echo {column}")
            old_y = df.at['ending_y_of_doc', column]
            if old_y == 0:
                continue
            try:
                with open(path_to_lidor_dct + column, 'rb') as dct_file:
                    dct = pickle.load(dct_file)
                # with open(path_to_latex_files + column+".tex", 'rb') as latex_path_file:
                #     latex_path = pickle.load(latex_path_file)
                latex_path = path_to_latex_files + column + ".tex"
                os.system(f"echo 2")
                files_created_small = using_operators_for_adi.perform_operators(dct, column, latex_path, path_to_file)
                os.system(f"echo 3")
                files_created[column] = files_created_small
                # print(files_created)
                index_doc_for_operators += 1
            except Exception as e:
                print(e)
                print("here2")
                continue
        os.system(f"echo 4")
        index_of_new_doc = 0
        index_doc = 0
        # compiling all the new files:
        cmd_line_del_tex = ""
        cmd_line_create_pdf = ""
        # for idd in range(len(files_created)):
        #     for j in files_created[idd]:
        #
        #         cmd_line_act = cmd_line_create_pdf + j[0]
        #         os.system(cmd_line_act)
        #
        #         time.sleep(2)
        #
        #         cmd_line_act =cmd_line_del_tex + j[0]
        #         os.system(cmd_line_act)
        counter_problems = 0
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
                    # old_y=read_single_file.order(path_to_latex_files+column+".pdf")
                    os.system(f"echo 5")
                    binary = 0
                    if column in files_created:
                        # print("exists")

                        # print(files_created)
                        for i in files_created[
                            column]:  # [(filename,pdfname,object,vspace(operator),vspace(operator)value)]
                            # print(f"{i}")
                            # becasue this is only for vspace so we will name him 1
                            os.system(f"echo 6")
                            cmd_line_act = cmd_line_create_pdf + i[0]
                            os.system(f"echo {i[0]}")
                            df[column + '_with_operator' + str(index_of_new_doc)] = df.loc[:,
                                                                                    column]  # create a new column
                            try:
                                os.system(cmd_line_act)
                                # time.sleep(2)
                                os.system(f"echo 7")
                                if (i[3] == 'vspace'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 1  # switch to i[3] when it is all set
                                elif (i[3] == 'change_figure_size'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 2  # switch to i[3] when it is all set
                                elif (i[3] == 'change_algorithm_size'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 3  # switch to i[3] when it is all set
                                elif (i[3] == 'convert_enum'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 4  # switch to i[3] when it is all set
                                elif (i[3] == 'remove_par_tag'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 5  # switch to i[3] when it is all set
                                elif (i[3] == 'combine_two_paragraphs'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 6  # switch to i[3] when it is all set
                                elif (i[3] == 'change_table_size'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 7  # switch to i[3] when it is all set
                                elif (i[3] == 'remove_special_positional_chars'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 8  # switch to i[3] when it is all set
                                elif (i[3] == 'remove_last_2_words'):
                                    df.at['type', column + '_with_operator' + str(
                                        index_of_new_doc)] = 9  # switch to i[3] when it is all set
                                df.at['value', column + '_with_operator' + str(index_of_new_doc)] = i[4]
                                df.at['object_used_on', column + '_with_operator' + str(index_of_new_doc)] = i[2]
                                df.at['num_of_object', column + '_with_operator' + str(index_of_new_doc)] = \
                                    re.findall(r'\d+', str(i[5]))[0]
                                df.at['herustica', column + '_with_operator' + str(index_of_new_doc)] = i[6]
                                df.at['ending_y_of_doc', column + '_with_operator' + str(index_of_new_doc)] = old_y
                                index = 0
                                os.system(f"echo 8")
                                os.system(f"echo {i[1]}")
                                x = read_single_file.order(i[1])
                                os.system(f"echo 9")
                                if (x == 0):  # only_one_page
                                    binary = 1
                                    y_gained = old_y
                                    lines_we_get = int(old_y / 10)

                                else:
                                    if x < old_y:
                                        binary = 1
                                        y_gained = old_y - x
                                        lines_we_get = int((old_y - y_gained) / 10)
                                    else:
                                        binary = 0
                                        y_gained = x - old_y
                                        lines_we_get = 0

                                    # we can change y_gained to 0 if we dont negative numbers
                                df.at['y_gained', column + '_with_operator' + str(index_of_new_doc)] = y_gained
                                df.at[
                                    'lines_we_gained', column + '_with_operator' + str(index_of_new_doc)] = lines_we_get
                                df.at['binary_class', column + '_with_operator' + str(index_of_new_doc)] = binary
                                index_of_new_doc += 1
                                os.system(f"echo 10")
                                cmd_line_del_pdf = ""
                                cmd_line_act = i[1]
                                os.remove(cmd_line_act)
                                os.system(f"echo 11")
                                cmd_line_act = i[0]
                                os.remove(cmd_line_act)
                                os.system(f"echo 12")
                            except Exception as e:
                                print(e)
                                print("here4")
                                df.at['y_gained', column + '_with_operator' + str(index_of_new_doc)] = -1
                                df.at['lines_we_gained', column + '_with_operator' + str(index_of_new_doc)] = -1
                                df.at['binary_class', column + '_with_operator' + str(index_of_new_doc)] = -1
                                df.at['type', column + '_with_operator' + str(index_of_new_doc)] = 9
                                df.at['value', column + '_with_operator' + str(index_of_new_doc)] = i[4]
                                df.at['object_used_on', column + '_with_operator' + str(index_of_new_doc)] = i[2]
                                df.at['num_of_object', column + '_with_operator' + str(index_of_new_doc)] = \
                                    re.findall(r'\d+', str(i[5]))[0]
                                df.at['herustica', column + '_with_operator' + str(index_of_new_doc)] = i[6]
                                df.at['ending_y_of_doc', column + '_with_operator' + str(index_of_new_doc)] = old_y
                                try:
                                    cmd_line_act = i[1]
                                    os.remove(cmd_line_act)

                                except Exception as e:
                                    print(e)
                                    print("here5")
                                    counter_problems += 1
                except Exception as e:
                    print(e)
                index_doc += 1
                df = df.drop(column, axis=1)

            os.system(f"echo 13")
            df2 = df.T
            df2.to_csv(created_excel_path)
            os.system(f"echo 14")
        except Exception as e:
            print(e)
            print("here")
            df2 = df.T
            df2.to_csv(created_excel_path)

        # x = get_pdf_order.order('C:\\Users\\lidor\\Desktop\\FINAL PROJECT - OVERLEAF\\30.10.22\\Overleaf_project\\pdf-tests\\lidor_test_2.pdf')
        # print(x)
