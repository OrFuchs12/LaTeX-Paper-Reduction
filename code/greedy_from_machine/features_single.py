import test
import pandas as pd
import pickle
import sys
import openpyxl
from pathlib import Path


# if __name__ == "__main__":
def run_feature_extraction(latex_path, pdf_path, bib_path, path_to_save_lidor_dct,
                           path_to_save_adi_dct, name, df):
    #print(22)
    summative_features_keys = ['max_lines_par', 'min_lines_par', 'max_lines_enum', 'min_lines_enum',
                               'max_lines_caption', 'min_lines_caption', 'max_figure_y_space', 'min_figure_y_space',
                               'max_table_y_space', 'min_table_y_space',
                               'max_height_object', 'min_height_object', 'num_of_elements',
                               'num_of_pars', 'num_of_pars_in_col_1', 'num_of_pars_in_col_2',
                               'num_of_paragraphs', 'num_of_paragraphs_in_col_1', 'num_of_paragraphs_in_col_2',
                               'num_of_algorithms', 'num_of_algorithms_in_col_1', 'num_of_algorithms_in_col_2',
                               'num_of_formulas', 'num_of_formulas_in_col_1', 'num_of_formulas_in_col_2',
                               'num_of_figures_in_col_1', 'num_of_figures_in_col_2',
                               'num_of_tables_in_col_1', 'num_of_tables_in_col_2', 'last_element',
                               'sum_space_taken',
                               'sum_open_space', 'sum_space_taken_by_figures', 'sum_space_taken_by_tables',
                               'sum_of_chars_across_doc',
                               'sum_of_words_from_pars', 'sum_of_chars_from_pars', 'avg_num_of_words_from_pars',
                               'avg_num_of_chars_from_pars', 'num_of_paragraphs_with_1_word_at_the_end',
                               'num_of_figures_with_captions', 'num_of_tables_with_captions', 'ending_y_of_doc']
    columns = []
    # name = list_latex_files.split(".")[0]
    for i in range(1):
        columns.append(name)
    Rows = []
    for key in summative_features_keys:
        Rows.append(key)

    Par_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                'single_word_in_last_line', 'space_between_this_object_and_last_object',
                'space_between_this_object_and_the_next_object']
    Paragraph_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                      'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                      'single_word_in_last_line', 'space_between_this_object_and_last_object',
                      'space_between_this_object_and_the_next_object']
    # Title_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
    #               'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
    #               'single_word_in_last_line', 'space_between_this_object_and_last_object',
    #               'space_between_this_object_and_the_next_object']
    Figure_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'figure_has_caption', 'figure_position_param',
                   'space_between_this_object_and_last_object', 'space_between_caption_and_figure',
                   'space_between_this_object_and_the_next_object']
    CaptionFigure_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'number_of_lines', 'last_line_length_chars',
                          'last_line_length_words', 'space_between_this_object_and_last_object',
                          'space_between_this_object_and_the_next_object']
    Table_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'table_has_caption', 'table_position_param',
                  'space_between_this_object_and_last_object', 'space_between_caption_and_table',
                  'space_between_this_object_and_the_next_object']
    CaptionTable_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'number_of_lines', 'last_line_length_chars',
                         'last_line_length_words', 'space_between_this_object_and_last_object',
                         'space_between_this_object_and_the_next_object']
    # AbstractSection_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
    #                         'space_between_this_object_and_last_object',
    #                         'space_between_this_object_and_the_next_object']
    # AbstractPar_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
    #                     'number_of_lines', 'num_of_chars', 'num_of_words', 'last_line_length_chars',
    #                     'last_line_length_words', 'single_word_in_last_line',
    #                     'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
    Section_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                    'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
    SubSection_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                       'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
    # subsubsection to add
    # Matrix_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'space_between_this_object_and_last_object',
    #                'space_between_this_object_and_the_next_object']
    Enum_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                 'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                 'single_word_in_last_line', 'space_between_this_object_and_last_object',
                 'space_between_this_object_and_the_next_object']
    Formula_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'bad_detection_formula','space_between_this_object_and_last_object',
                    'space_between_this_object_and_the_next_object']
    Algorithm_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                      'algorithm_position_param',
                      'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']

    operators_keys = ['type', 'value', 'object_used_on', 'num_of_object']
    classes_keys = ['y_gained', 'lines_we_gained', 'binary_class', 'herustica']
    # print(len(Par_keys))
    # print(len(Title_keys))
    # print(len(Figure_keys))
    # print(len(CaptionFigure_keys))
    # print(len(Table_keys))
    # print(len(CaptionTable_keys))
    # print(len(AbstractSection_keys))
    # print(len(AbstractPar_keys))
    # print(len(Section_keys))
    # print(len(SubSection_keys))
    # print(len(Matrix_keys))
    # print(len(Enum_keys))
    # print(len(Formula_keys))
    # print(len(Algorithm_keys))
    # print(len(operators_keys))
    # print(len(classes_keys))

    j = 0
    # 43 starting features
    # 8 pars:
    for i in range(8):  # 8*14 = 112+42(starting features) 155
        for key in Par_keys:
            Rows.append(key + str(j))
        j += 1
    for i in range(2):  # 2*14 = 28 -> 183
        for key in Paragraph_keys:
            Rows.append(key + str(j))
        j += 1
    # #0 titles at most #1*14 = 14 #249
    # for key in Title_keys:
    #     Rows.append(key+str(j))
    #     j += 1
    # 4 figures at most #4*10 = 40 223
    for i in range(4):
        for key in Figure_keys:
            Rows.append(key + str(j))
        j += 1
    # 4 CaptionFigures at most #4*10 = 40 263
    for i in range(4):
        for key in CaptionFigure_keys:
            Rows.append(key + str(j))
        j += 1
    # 2 Tables at most 2*10 = 20 283
    for i in range(2):
        for key in Table_keys:
            Rows.append(key + str(j))
        j += 1
    # 2 CaptionTables at most 2*10 = 20 303
    for i in range(2):
        for key in CaptionTable_keys:
            Rows.append(key + str(j))
        j += 1
    # #0 AbstractSec at most #1*8 = 8 417
    # for key in AbstractSection_keys:
    #     Rows.append(key+str(j))
    #     j += 1
    # #0 AbstractPar at most #1*14 = 14 421
    # for key in AbstractPar_keys:
    #     Rows.append(key+str(j))
    #     j += 1
    # 3 sections at most #3*8 = 24 327
    for i in range(3):
        for key in Section_keys:
            Rows.append(key + str(j))
        j += 1
    # 3 subsections at most #3*8 = 24 351
    for i in range(3):
        for key in SubSection_keys:
            Rows.append(key + str(j))
        j += 1
    # 2 matrixes at most #2*7 = 14 320
    # for i in range(2):
    #     for key in Matrix_keys:
    #         Rows.append(key + str(j))
    #     j += 1
    # 5 Enum at most #5*14 = 70 421
    for i in range(5):
        for key in Enum_keys:
            Rows.append(key + str(j))
        j += 1
    # 5 Formulas at most #5*8 = 40 461
    for i in range(5):
        for key in Formula_keys:
            Rows.append(key + str(j))
        j += 1
    # 2 Algorithms at most #2*9 = 18 479
    for i in range(2):
        for key in Algorithm_keys:
            Rows.append(key + str(j))
        j += 1

    # 4 operator defining features at most 4 => 483
    for key in operators_keys:
        Rows.append(key)
    j += 1

    # 4 Classes at most 4 => 487
    for key in classes_keys:
        Rows.append(key)
    j += 1
    # print(Rows)
    # print(len(Rows))
    if df.empty:
        df = pd.DataFrame(index=Rows, columns=columns)
    else:
        df[name] = [0 for x in range(len(Rows))]
    files_created = []
    # for loop blablabla
    max_height = 0

    for file_index in range(1):
        res = test.run(latex_path, pdf_path, bib_path)
        #print(res)
        
        # try:
        #     with open(path_to_save_adi_dct, 'rb') as dct_file:
        #         res = pickle.load(dct_file)
        # except:
        #     #res = test.run(latex_path=latex_path,pdf_path=pdf_path,bib_path=bib_path)
        #     return df
        if res == []:
            return df
        max_height = res[-1]
        # with open(path_to_save_adi_dct, 'wb') as dct_file:
        #     pickle.dump(res, dct_file)
        res = res[:-1]
        # print(order)
        # print("-0-------")
        # pdf = []
        # for page in order:
        #     for column in order[page]:
        #         for line in column:
        #             pdf.extend(line)

        # print(pdf)

        # START OF PAGE IS 50.01389562499992 (BASED ON FIGURE LOCATION)
        # END OF PAGE IS 704.1519215999999 (BASED ON LAST PARAGRAPH IS A PAGE)
        # print("--------")
        count_dct = {}  # contains: key- object name, value- number of appearances
        updating_count_dct = {}
        par_dct = {}
        figure_dct = {}
        dct = {}
        figure_index = 0
        figure_has_caption = False
        table_has_caption = False
        index = 0
        par_index = 0
        paragraph_index = 0
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
        table_index = 0
        caption_table_index = 0
        index = 0
        flag = False
        last_object = 0
        object_name = ''
        last_object_name = ''
        whole_string = ''
        add_space = False
        new_start_y_needed_formula = False
        new_end_y_needed_formula = False
        num_of_pars_in_col_1 = 0
        num_of_pars_in_col_2 = 0
        num_of_paragraphs_in_col_1 = 0
        num_of_paragraphs_in_col_2 = 0
        num_of_figures_in_col_1 = 0
        num_of_figures_in_col_2 = 0
        num_of_tables_in_col_1 = 0
        num_of_tables_in_col_2 = 0
        num_of_algorithms_in_col_1 = 0
        num_of_algorithms_in_col_2 = 0
        num_of_formulas_in_col_1 = 0
        num_of_formulas_in_col_2 = 0
        last_object_index = 0
        # the (1,0) is a place holder (i mean for the 1 at the start of the tuple)
        max_lines_enum = (1, 0)
        max_lines_caption = (1, 0)
        max_lines_par = (1, 0)
        min_lines_enum = (1, 1000)
        min_lines_caption = (1, 1000)
        min_lines_par = (1, 1000)
        max_figure_y_space = (1, 0)
        min_figure_y_space = (1, 10000)
        max_table_y_space = (1, 0)
        min_table_y_space = (1, 10000)
        max_height_object = (1, 0)
        min_height_object = (1, 1000)
        sum_space_taken = 0
        sum_open_space = 0
        sum_space_taken_by_figures = 0
        sum_space_taken_by_tables = 0
        sum_of_chars_across_doc = 0
        sum_of_chars_from_pars = 0
        sum_of_words_from_pars = 0
        num_of_paragraphs_with_1_word_at_the_end = 0
        num_of_figures_with_captions = 0
        num_of_tables_with_captions = 0
        end_y_of_doc = max_height
        summative_features = {}
        first_object = False
        indexxx = 0
        for object in res:
            add_space = False
            if (last_object == 0):
                last_object = object
                first_object = True
            #print(object)
            # LETS START WITH COUNTING THE NUMBER OF DIFFERENT OBJECTS WE HAVE IN OUR DOCUMENT
            if (object['Type'] not in count_dct.keys()):
                count_dct[object['Type']] = 1
            else:
                count_dct[object['Type']] += 1
            # figure details:
            if (object['Type'] == 'Figure'):
                figure_index += 1
                if (object['j'] == 0):
                    num_of_figures_in_col_1 += 1
                else:
                    num_of_figures_in_col_2 += 1
                object_name = object['Type'] + str(figure_index)
                dct[object_name] = {}
                # lets try and find intresting stuff about figures:
                # start with height and col postion
                dct[object_name]['page'] = object['k']
                dct[object_name]['column'] = object['j']
                # dct[object_name]['figure_dimensions_y'] = object['First_line_bbox']
                dct[object_name]['start_y'] = object['First_line_bbox'][0]
                dct[object_name]['end_y'] = object['First_line_bbox'][1]
                dct[object_name]['height'] = object['First_line_bbox'][1] - object['First_line_bbox'][0]
                sum_space_taken_by_figures += dct[object_name]['height']
                # dct[object_name]['figure_area'] = '' #need to do
                # dct[object_name]['figure_width'] = '' #need to do
                bool_to_num = 0
                if (object['Text'][3] == 'True'):
                    bool_to_num = 1
                    num_of_figures_with_captions += 1
                    figure_has_caption = True
                else:
                    bool_to_num = 0
                dct[object_name]['figure_has_caption'] = bool_to_num
                position_par= object['Text'][2]
                if position_par=="":
                    dct[object_name]['figure_position_param']=0
                elif position_par=="b":
                    dct[object_name]['figure_position_param']=1
                elif position_par=="t":
                    dct[object_name]['figure_position_param']=2
                elif position_par=="h":
                    dct[object_name]['figure_position_param']=3
                else:
                    dct[object_name]['figure_position_param']=4
                if (dct[object_name]['height'] > max_figure_y_space[1]):
                    max_figure_y_space = (object_name, dct[object_name]['height'])
                if (dct[object_name]['height'] < min_figure_y_space[1] and dct[object_name]['height'] >= 0):
                    min_figure_y_space = (object_name, dct[object_name]['height'])

            elif (object['Type'] == 'CaptionFigure'):
                caption_index += 1
                object_name = last_object['Type'] + str(figure_index)
                # dct[object_name]['figure_caption'] = object
                dct[object_name]['space_between_caption_and_figure'] = abs(
                    last_object['First_line_bbox'][1] - object['First_line_bbox'][0])
                figure_has_caption = False

                # creating the captionfigure object
                object_name = object['Type'] + str(caption_index)
                dct[object_name] = {}
                dct[object_name]['page'] = object['k']
                dct[object_name]['column'] = object['j']
                # dct[object_name]['par_dimensions_y'] = (object['First_line_bbox'][0], object['Last_line_bbox'][1])
                dct[object_name]['start_y'] = object['First_line_bbox'][0]
                dct[object_name]['end_y'] = object['Last_line_bbox'][1]
                dct[object_name]['height'] = object['Last_line_bbox'][1] - object['First_line_bbox'][0]
                # stuff about the content of the caption
                pdf = object['pdf_array']
                dct[object_name]["number_of_lines"] = len(pdf)
                if pdf != []:

                    dct[object_name]["last_line_length_chars"] = len(pdf[-1][1])
                    dct[object_name]["last_line_length_words"] = len(pdf[-1][1].split())
                else:
                    dct[object_name]["last_line_length_chars"] = 0
                    dct[object_name]["last_line_length_words"] = 0

                if (dct[object_name]["number_of_lines"] > max_lines_caption[1]):
                    max_lines_caption = (object_name, dct[object_name]["number_of_lines"])
                if (dct[object_name]["number_of_lines"] < min_lines_caption[1]):
                    min_lines_caption = (object_name, dct[object_name]["number_of_lines"])

            elif (object['Type'] == 'Table'):
                table_index += 1
                if (object['j'] == 0):
                    num_of_tables_in_col_1 += 1
                else:
                    num_of_tables_in_col_2 += 1
                object_name = object['Type'] + str(table_index)
                dct[object_name] = {}
                # lets try and find intresting stuff about figures:
                # start with height and col postion
                dct[object_name]['page'] = object['k']
                dct[object_name]['column'] = object['j']
                # dct[object_name]['figure_dimensions_y'] = object['First_line_bbox']
                dct[object_name]['start_y'] = object['First_line_bbox'][0]
                dct[object_name]['end_y'] = object['First_line_bbox'][1]
                dct[object_name]['height'] = object['First_line_bbox'][1] - object['First_line_bbox'][0]
                sum_space_taken_by_tables += dct[object_name]['height']
                # dct[object_name]['figure_area'] = '' #need to do
                # dct[object_name]['figure_width'] = '' #need to do
                bool_to_num = 0
                if (object['Text'][3] == 'True'):
                    bool_to_num = 1
                    num_of_tables_with_captions += 1
                    table_has_caption = True
                else:
                    bool_to_num = 0
                dct[object_name]['table_has_caption'] = bool_to_num
                position_par = object['Text'][2]
                if position_par=="":
                    dct[object_name]['table_position_param']=0
                elif position_par=="b":
                    dct[object_name]['table_position_param']=1
                elif position_par=="t":
                    dct[object_name]['table_position_param']=2
                elif position_par=="h":
                    dct[object_name]['table_position_param']=3
                else:
                    dct[object_name]['table_position_param']=4
                if (dct[object_name]['height'] > max_table_y_space[1]):
                    max_table_y_space = (object_name, dct[object_name]['height'])
                if (dct[object_name]['height'] < min_table_y_space[1] and dct[object_name]['height'] >= 0):
                    min_table_y_space = (object_name, dct[object_name]['height'])
            elif (object['Type'] == 'CaptionTable'):
                caption_table_index += 1
                object_name = last_object['Type'] + str(table_index)
                # dct[object_name]['figure_caption'] = object
                dct[object_name]['space_between_caption_and_table'] = abs(
                    last_object['First_line_bbox'][1] - object['First_line_bbox'][0])
                table_has_caption = False

                # creating the captionfigure object
                object_name = object['Type'] + str(caption_table_index)
                dct[object_name] = {}
                dct[object_name]['page'] = object['k']
                dct[object_name]['column'] = object['j']
                # dct[object_name]['par_dimensions_y'] = (object['First_line_bbox'][0], object['Last_line_bbox'][1])
                dct[object_name]['start_y'] = object['First_line_bbox'][0]
                dct[object_name]['end_y'] = object['Last_line_bbox'][1]
                dct[object_name]['height'] = object['Last_line_bbox'][1] - object['First_line_bbox'][0]
                # stuff about the content of the caption
                pdf = object['pdf_array']
                dct[object_name]["number_of_lines"] = len(pdf)
                if pdf!=[]:

                    dct[object_name]["last_line_length_chars"] = len(pdf[-1][1])
                    dct[object_name]["last_line_length_words"] = len(pdf[-1][1].split())
                else:
                    dct[object_name]["last_line_length_chars"] = 0
                    dct[object_name]["last_line_length_words"] = 0

                if (dct[object_name]["number_of_lines"] > max_lines_caption[
                    1]):  # we can make it more specific to CaptionTable insted of combining CaptionFigure and CaptionTable
                    max_lines_caption = (object_name, dct[object_name]["number_of_lines"])
                if (dct[object_name]["number_of_lines"] < min_lines_caption[1]):
                    min_lines_caption = (object_name, dct[object_name]["number_of_lines"])

            elif (object['Type'] == 'Matrix'):
                matrix_index += 1
                object_name = object['Type'] + str(matrix_index)
                dct[object_name] = {}

                dct[object_name]['page'] = object['k']
                dct[object_name]['column'] = object['j']
                # dct[object_name]['matrix_dimensions_y'] = object['First_line_bbox']
                dct[object_name]['start_y'] = object['First_line_bbox'][0]
                dct[object_name]['end_y'] = object['First_line_bbox'][1]
                dct[object_name]['height'] = object['First_line_bbox'][1] - object['First_line_bbox'][0]
                # dct[object_name]['matrix_area'] = ''  # need to do
                # dct[object_name]['matrix_width'] = ''  # need to do


            elif (object['Type'] == 'Formula'):
                formula_index += 1
                if (object['j'] == 0):
                    num_of_formulas_in_col_1 += 1
                else:
                    num_of_formulas_in_col_2 += 1
                object_name = object['Type'] + str(formula_index)
                dct[object_name] = {}
                dct[object_name]['page'] = object['k']
                dct[object_name]['column'] = object['j']
                if (object['First_line_bbox'][0] > 704):  # bad formula
                    new_start_y_needed_formula = True
                if (object['First_line_bbox'][1] < 0):
                    new_end_y_needed_formula = True
                if (new_start_y_needed_formula or new_end_y_needed_formula):
                    dct[object_name]['start_y'] = 0
                    dct[object_name]['end_y'] = 0
                    dct[object_name]['height'] = 0
                    dct[object_name]['bad_detection_formula'] = 1
                else:
                    dct[object_name]['start_y'] = object['First_line_bbox'][0]
                    dct[object_name]['end_y'] = object['First_line_bbox'][1]
                    dct[object_name]['height'] = object['First_line_bbox'][1] - object['First_line_bbox'][0]
                    dct[object_name]['bad_detection_formula'] = 0
                # dct[object_name]['formula_dimensions_y'] = object['First_line_bbox']


            elif (object['Type'] == 'Par' or object['Type'] == 'Paragraph' or object['Type'] == 'Title' or object[
                'Type'] == 'AbstractSection' or object['Type'] == 'AbstractPar' or object['Type'] == 'Section' or
                  object['Type'] == 'SubSection' or object['Type'] == 'SubSubSection' or object['Type'] == 'Enum' or
                  object['Type'] == 'Algorithm'):
                if (object['Type'] == 'Par'):
                    par_index += 1
                    if (object['j'] == 0):
                        num_of_pars_in_col_1 += 1
                    else:
                        num_of_pars_in_col_2 += 1
                    index = par_index
                elif (object['Type'] == 'Paragraph'):
                    paragraph_index += 1
                    if (object['j'] == 0):
                        num_of_paragraphs_in_col_1 += 1
                    else:
                        num_of_paragraphs_in_col_2 += 1
                    index = paragraph_index
                elif (object['Type'] == 'Title'):
                    title_index += 1
                    index = title_index
                elif (object['Type'] == 'AbstractSection'):
                    abstractsec_index += 1
                    index = abstractsec_index
                elif (object['Type'] == 'AbstractPar'):
                    abstractpar_index += 1
                    index = abstractpar_index
                elif (object['Type'] == 'Section'):
                    section_index += 1
                    index = section_index
                elif (object['Type'] == 'SubSection'):
                    subsection_index += 1
                    index = subsection_index
                elif (object['Type'] == 'SubSubSection'):
                    subsubsection_index += 1
                    index = subsubsection_index
                elif (object['Type'] == 'Enum'):
                    enum_index += 1
                    index = enum_index
                elif (object['Type'] == 'Algorithm'):
                    algo_index += 1
                    if (object['j'] == 0):
                        num_of_algorithms_in_col_1 += 1
                    else:
                        num_of_algorithms_in_col_2 += 1
                    index = algo_index
                else:
                    undetected_index += 1
                    index = undetected_index
                object_name = object['Type'] + str(index)
                dct[object_name] = {}
                dct[object_name]['page'] = object['k']
                dct[object_name]['column'] = object['j']
                # dct[object_name]['par_dimensions_y'] = (object['First_line_bbox'][0],object['Last_line_bbox'][1])
                dct[object_name]['start_y'] = object['First_line_bbox'][0]
                if 'Last_line_bbox' in object:
                    dct[object_name]['end_y'] = object['Last_line_bbox'][1]
                else:
                    dct[object_name]['end_y']=-1
                height = 0
                # we are assuming a paragraph wont be more than 1 column long
                if (object['First_line_bbox'][0] > object['Last_line_bbox'][1]):
                    height += 704.1519215999999 - object['First_line_bbox'][0]
                    height += object['Last_line_bbox'][1] - 50.01389562499992
                    dct[object_name]['spread_on_more_than_1_column'] = 1
                else:
                    height += object['Last_line_bbox'][1] - object['First_line_bbox'][0]
                    dct[object_name]['spread_on_more_than_1_column'] = 0
                # WONT WORK UNTILL LAST_LINE_J AND LAST_LINE_K WILL BE FIXED
                # if(object['k'] != object['Last_line_k'] or object['j'] != object['Last_line_j']):
                #     height += 704.1519215999999 - object['First_line_bbox'][0]
                #     height += object['Last_line_bbox'][1] - 50.01389562499992
                #     dct[object_name]['spread_on_more_than_1_column'] = True
                # else:
                #     height += object['Last_line_bbox'][1] - object['First_line_bbox'][0]
                #     dct[object_name]['spread_on_more_than_1_column'] = False
                dct[object_name]['height'] = height
                if (object['Type'] == 'Algorithm'):
                    # dct[object_name]['algorithm_position_param'] = object['Pos']

                    position_par = object['Pos']
                    if position_par == "":
                        dct[object_name]['algorithm_position_param'] = 0
                    elif position_par == "b":
                        dct[object_name]['algorithm_position_param'] = 1
                    elif position_par == "t":
                        dct[object_name]['algorithm_position_param'] = 2
                    elif position_par == "h":
                        dct[object_name]['algorithm_position_param'] = 3
                    else:
                        dct[object_name]['algorithm_position_param'] = 4


                if (object['Type'] != 'Algorithm' and object['Type'] != 'Section' and object['Type'] != 'SubSection' and
                        object['Type'] != 'SubSubSection' and object['Type'] != 'AbstractSection'):
                    pdf = object['pdf_array']
                    for i in pdf:
                        if (i[1][-1] == '-'):
                            if (add_space):
                                whole_string += ' ' + i[1][:-1]
                                add_space = False
                            else:
                                whole_string += i[1][:-1]
                                add_space = False
                        else:
                            if (add_space):
                                whole_string += ' ' + i[1]
                                add_space = True
                            else:
                                whole_string += i[1]
                                add_space = True
                    dct[object_name]["number_of_lines"] = len(pdf)
                    dct[object_name]["num_of_chars"] = len(whole_string)
                    dct[object_name]["num_of_words"] = len(whole_string.split())
                    if pdf != []:

                        dct[object_name]["last_line_length_chars"] = len(pdf[-1][1])
                        dct[object_name]["last_line_length_words"] = len(pdf[-1][1].split())
                    else:
                        dct[object_name]["last_line_length_chars"] = 0
                        dct[object_name]["last_line_length_words"] = 0

                    if (dct[object_name]["last_line_length_words"] == 1):
                        dct[object_name]["single_word_in_last_line"] = 1
                    else:
                        dct[object_name]["single_word_in_last_line"] = 0

                    if (object['Type'] == 'Par' or object[
                        'Type'] == 'Paragraph'):  # we could change it that many of the same size will count as max, not only a single first max (or min)
                        sum_of_words_from_pars += dct[object_name]["num_of_words"]
                        sum_of_chars_from_pars += dct[object_name]["num_of_chars"]
                        if (dct[object_name]["single_word_in_last_line"]):
                            num_of_paragraphs_with_1_word_at_the_end += 1
                        if (dct[object_name]["number_of_lines"] > max_lines_par[1]):
                            max_lines_par = (object_name, dct[object_name]["number_of_lines"])
                        if (dct[object_name]["number_of_lines"] < min_lines_par[1] and dct[object_name][
                            "number_of_lines"] >= 0):
                            min_lines_par = (object_name, dct[object_name]["number_of_lines"])
                    elif (object['Type'] == 'Enum'):
                        if (dct[object_name]["number_of_lines"] > max_lines_enum[1]):
                            max_lines_enum = (object_name, dct[object_name]["number_of_lines"])
                        if (dct[object_name]["number_of_lines"] < min_lines_enum[1] and dct[object_name][
                            "number_of_lines"] >= 0):
                            min_lines_enum = (object_name, dct[object_name]["number_of_lines"])
                    whole_string = ''
                    # dct[object_name]['number of chars in object'] =

            if (first_object):
                last_object_name = object_name

            # spaces part
            if (last_object['Type'] == 'Matrix' or last_object['Type'] == 'Formula' or last_object[
                'Type'] == 'Figure' or last_object['Type'] == 'Table'):
                if (object['Type'] == 'Figure' or object['Type'] == 'Table'):  # trying to detect subfigures
                    if (object['First_line_bbox'] == last_object['First_line_bbox']):
                        #print(dct)
                        if ('space_between_this_object_and_last_object' not in dct[
                            last_object_name]):  # if we start the doc with an image
                            dct[object_name]['space_between_this_object_and_last_object'] = abs(
                                50.01389562499992 - object['First_line_bbox'][0])
                        else:
                            dct[object_name]['space_between_this_object_and_last_object'] = dct[last_object_name][
                                'space_between_this_object_and_last_object']
                    else:
                        dct[object_name]['space_between_this_object_and_last_object'] = abs(
                            last_object['First_line_bbox'][1] - object['First_line_bbox'][0])
                else:
                    # print(last_object['Type'])
                    # print(object['Type'])
                    dct[object_name]['space_between_this_object_and_last_object'] = abs(
                        last_object['First_line_bbox'][1] - object['First_line_bbox'][0])
                dct[last_object_name]['space_between_this_object_and_the_next_object'] = dct[object_name][
                    'space_between_this_object_and_last_object']
            else:
                # print(last_object['Last_line_bbox'][1])
                # print(object['First_line_bbox'][0])
                # print(abs(last_object['Last_line_bbox'][1] -object['First_line_bbox'][0]))
                if (
                        last_object == object):  # for title we will calculate the space between the title and the coords of the first figure if it existed (coords of first figure in a page is: (50.01389562499992))
                    dct[object_name]['space_between_this_object_and_last_object'] = abs(
                        50.01389562499992 - object['First_line_bbox'][0])
                else:
                    if (last_object['Last_line_bbox'][1] - object['First_line_bbox'][
                        0] > 100):  # next page difference, so we will take space from the top of the page which is: (50.01389562499992)
                        dct[object_name]['space_between_this_object_and_last_object'] = abs(
                            50.01389562499992 - object['First_line_bbox'][0])

                    else:
                        dct[object_name]['space_between_this_object_and_last_object'] = abs(
                            last_object['Last_line_bbox'][1] - object['First_line_bbox'][0])
                    dct[last_object_name]['space_between_this_object_and_the_next_object'] = dct[object_name][
                        'space_between_this_object_and_last_object']

            if (dct[object_name]['height'] >= 0):
                sum_space_taken += dct[object_name]['height']
            if (dct[object_name]['space_between_this_object_and_last_object'] >= 0):
                sum_open_space += dct[object_name]['space_between_this_object_and_last_object']

            if (dct[object_name]['height'] > max_height_object[1]):
                max_height_object = (object_name, dct[object_name]['height'])
            if (dct[object_name]['height'] < min_height_object[1] and dct[object_name]['height'] >= 0):
                min_height_object = (object_name, dct[object_name]['height'])

            if ('num_of_chars' in dct[object_name].keys()):
                sum_of_chars_across_doc += dct[object_name]['num_of_chars']

            last_object = object
            last_object_name = object_name
            if (indexxx == len(res) - 1):
                if(object['Type'] == 'Par'):
                    last_object_index = 1
                elif(object['Type'] == 'Figure'):
                    last_object_index = 2
                elif(object['Type'] == 'CaptionFigure'):
                    last_object_index = 3
                elif (object['Type'] == 'Table'):
                    last_object_index = 4
                elif (object['Type'] == 'CaptionTable'):
                    last_object_index = 5
                elif (object['Type'] == 'Section'):
                    last_object_index = 6
                elif (object['Type'] == 'SubSection'):
                    last_object_index = 7
                elif (object['Type'] == 'Matrix'):
                    last_object_index = 8
                elif (object['Type'] == 'Enum'):
                    last_object_index = 9
                elif (object['Type'] == 'Formula'):
                    last_object_index = 10
                elif (object['Type'] == 'Algorithm'):
                    last_object_index = 11
                else:
                    last_object_index = 0
            indexxx+=1
            # end_y_of_doc = dct[object_name]['end_y']

        summative_features['max_lines_par'] = max_lines_par
        if (min_lines_par[1] == 1000 or min_lines_par[1] < 0):
            min_lines_par=list(min_lines_par)
            min_lines_par[1] = 0
            min_lines_par=tuple(min_lines_par)
            summative_features['min_lines_par'] = min_lines_par
        else:
            summative_features['min_lines_par'] = min_lines_par

        summative_features['max_lines_enum'] = max_lines_enum

        if (min_lines_enum[1] == 1000 or min_lines_enum[1] < 0):
            min_lines_enum=list(min_lines_enum)
            min_lines_enum[1] = 0
            min_lines_enum=tuple(min_lines_enum)
            summative_features['min_lines_enum'] = min_lines_enum
        else:
            summative_features['min_lines_enum'] = min_lines_enum

        summative_features['max_lines_caption'] = max_lines_caption

        if (min_lines_caption[1] == 1000 or min_lines_caption[1] < 0):
            min_lines_caption=list(min_lines_caption)
            min_lines_caption[1] = 0
            min_lines_caption=tuple(min_lines_caption)
            summative_features['min_lines_caption'] = min_lines_caption
        else:
            summative_features['min_lines_caption'] = min_lines_caption

        summative_features['max_figure_y_space'] = max_figure_y_space

        if (min_figure_y_space[1] == 10000 or min_figure_y_space[1] < 0):
            min_figure_y_space=list(min_figure_y_space)
            min_figure_y_space[1] = 0
            min_figure_y_space=tuple(min_figure_y_space)
            summative_features['min_figure_y_space'] = min_figure_y_space
        else:
            summative_features['min_figure_y_space'] = min_figure_y_space

        summative_features['max_table_y_space'] = max_table_y_space

        if (min_table_y_space[1] == 10000 or min_table_y_space[1] < 0):
            min_table_y_space=list(min_table_y_space)
            min_table_y_space[1] = 0
            min_table_y_space=tuple(min_table_y_space)
            summative_features['min_table_y_space'] = min_table_y_space
        else:
            summative_features['min_table_y_space'] = min_table_y_space

        summative_features['max_height_object'] = max_height_object

        if (min_height_object[1] == 10000 or min_height_object[1] < 0):
            min_height_object=list(min_height_object)
            min_height_object[1] = 0
            min_height_object=tuple(min_height_object)
            summative_features['min_height_object'] = min_height_object
        else:
            summative_features['min_height_object'] = min_height_object

        summative_features['num_of_elements'] = sum(count_dct.values())
        summative_features['num_of_pars'] = par_index
        summative_features['num_of_pars_in_col_1'] = num_of_pars_in_col_1
        summative_features['num_of_pars_in_col_2'] = num_of_pars_in_col_2
        summative_features['num_of_paragraphs'] = paragraph_index
        summative_features['num_of_paragraphs_in_col_1'] = num_of_paragraphs_in_col_1
        summative_features['num_of_paragraphs_in_col_2'] = num_of_paragraphs_in_col_2
        summative_features['num_of_algorithms'] = algo_index
        summative_features['num_of_algorithms_in_col_1'] = num_of_algorithms_in_col_1
        summative_features['num_of_algorithms_in_col_2'] = num_of_algorithms_in_col_2
        summative_features['num_of_formulas'] = formula_index
        summative_features['num_of_formulas_in_col_1'] = num_of_formulas_in_col_1
        summative_features['num_of_formulas_in_col_2'] = num_of_formulas_in_col_2
        summative_features['num_of_figures_in_col_1'] = num_of_figures_in_col_1
        summative_features['num_of_figures_in_col_2'] = num_of_figures_in_col_2
        summative_features['num_of_tables_in_col_1'] = num_of_tables_in_col_1
        summative_features['num_of_tables_in_col_2'] = num_of_tables_in_col_2
        summative_features['last_element'] = last_object_index
        summative_features['sum_space_taken'] = sum_space_taken
        summative_features['sum_open_space'] = sum_open_space
        summative_features['sum_space_taken_by_figures'] = sum_space_taken_by_figures
        summative_features['sum_space_taken_by_tables'] = sum_space_taken_by_tables
        summative_features['sum_of_chars_across_doc'] = sum_of_chars_across_doc
        summative_features['sum_of_words_from_pars'] = sum_of_words_from_pars
        summative_features['sum_of_chars_from_pars'] = sum_of_chars_from_pars
        if 'Par' in count_dct:
            summative_features['avg_num_of_words_from_pars'] = sum_of_words_from_pars / count_dct['Par']
            summative_features['avg_num_of_chars_from_pars'] = sum_of_chars_from_pars / count_dct['Par']
        elif 'Paragraph' in count_dct:
            summative_features['avg_num_of_words_from_pars'] = sum_of_words_from_pars / count_dct['Paragraph']
            summative_features['avg_num_of_chars_from_pars'] = sum_of_chars_from_pars / count_dct['Paragraph']
        else:
            summative_features['avg_num_of_words_from_pars'] = 0
            summative_features['avg_num_of_chars_from_pars'] = 0
        summative_features['num_of_paragraphs_with_1_word_at_the_end'] = num_of_paragraphs_with_1_word_at_the_end
        summative_features['num_of_figures_with_captions'] = num_of_figures_with_captions
        summative_features['num_of_tables_with_captions'] = num_of_tables_with_captions
        summative_features['ending_y_of_doc'] = end_y_of_doc

        # print(summative_features)
        # print(dct)
        # for i in dct:
        #     print(f'{i}' ':' f'{dct[i]}')

        # saving objects into files so that we can use them later.
        #print(11)
        with open(path_to_save_lidor_dct, 'wb') as dct_file:
            pickle.dump(dct, dct_file)

        # files_created_small = using_operators.perform_operators(dct,file_index,summative_features,latex_path="C:\\Users\\lidor\\Desktop\\FINAL PROJECT - OVERLEAF\\30.10.22\\Overleaf_project\\pdf-tests\\" + list_latex_files[file_index] + ".tex",pdf_path="C:\\Users\\lidor\\Desktop\\FINAL PROJECT - OVERLEAF\\30.10.22\\Overleaf_project\\pdf-tests\\"+list_pdf_files[file_index] +".pdf",bib_path="C:\\Users\\lidor\\Desktop\\FINAL PROJECT - OVERLEAF\\30.10.22\\Overleaf_project\\pdf-tests\\"+list_bib_files[file_index]+".bib")
        # files_created.append(files_created_small)

        # summative_features_keys = ['max_lines_par','min_lines_par','max_lines_enum','min_lines_enum','max_lines_caption','min_lines_caption','max_figure_y_space','min_figure_y_space','max_height_object','min_height_object','num_of_elements','sum_space_taken','sum_open_space','sum_space_taken_by_figures','sum_of_chars_across_doc','sum_of_words_from_pars','sum_of_chars_from_pars','avg_num_of_words_from_pars','avg_num_of_chars_from_pars','num_of_paragraphs_with_1_word_at_the_end','num_of_figures_with_captions']
        # columns = ['Doc1']
        # Rows = []
        # for key in summative_features_keys:
        #     Rows.append(key)
        #
        # Par_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines', 'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words', 'single_word_in_last_line', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # Title_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines', 'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words', 'single_word_in_last_line', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # Figure_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'figure_has_caption', 'figure_position_param', 'space_between_this_object_and_last_object', 'space_between_caption_and_figure', 'space_between_this_object_and_the_next_object']
        # CaptionFigure_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'number_of_lines', 'last_line_length_chars', 'last_line_length_words', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # AbstractSection_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # AbstractPar_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines', 'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words', 'single_word_in_last_line', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # Section_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # SubSection_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # #subsubsection to add
        # Matrix_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # Enum_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines', 'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words', 'single_word_in_last_line', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # Formula_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # Algorithm_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        #
        # print(len(Par_keys))
        # print(len(Title_keys))
        # print(len(Figure_keys))
        # print(len(CaptionFigure_keys))
        # print(len(AbstractSection_keys))
        # print(len(AbstractPar_keys))
        # print(len(Section_keys))
        # print(len(SubSection_keys))
        # print(len(Matrix_keys))
        # print(len(Enum_keys))
        # print(len(Formula_keys))
        # print(len(Algorithm_keys))
        #
        # j = 0
        # #8 pars:
        # for i in range(8): #8*14 = 112+21(starting features)
        #     for key in Par_keys:
        #         Rows.append(key+str(j))
        #     j += 1
        # # #0 titles at most #1*14 = 14 #245
        # # for key in Title_keys:
        # #     Rows.append(key+str(j))
        # #     j += 1
        # #4 figures at most #4*10 = 40 173
        # for i in range(4):
        #     for key in Figure_keys:
        #         Rows.append(key+str(j))
        #     j += 1
        # #4 CaptionFigures at most #4*10 = 40 213
        # for i in range(4):
        #     for key in CaptionFigure_keys:
        #         Rows.append(key+str(j))
        #     j += 1
        # # #0 AbstractSec at most #1*8 = 8 413
        # # for key in AbstractSection_keys:
        # #     Rows.append(key+str(j))
        # #     j += 1
        # # #0 AbstractPar at most #1*14 = 14 427
        # # for key in AbstractPar_keys:
        # #     Rows.append(key+str(j))
        # #     j += 1
        # #3 sections at most #3*8 = 24 237
        # for i in range(3):
        #     for key in Section_keys:
        #         Rows.append(key+str(j))
        #     j += 1
        # # 3 subsections at most #3*8 = 24 261
        # for i in range(3):
        #     for key in SubSection_keys:
        #         Rows.append(key + str(j))
        #     j += 1
        # #2 matrixes at most #2*7 = 14 275
        # for i in range(2):
        #     for key in Matrix_keys:
        #         Rows.append(key+str(j))
        #     j += 1
        # #5 Enum at most #5*14 = 70 345
        # for i in range(5):
        #     for key in Enum_keys:
        #         Rows.append(key+str(j))
        #     j += 1
        # #5 Formulas at most #5*7 = 35 380
        # for i in range(5):
        #     for key in Formula_keys:
        #         Rows.append(key+str(j))
        #     j += 1
        # #2 Algorithms at most #2*8 = 16 396
        # for i in range(2):
        #     for key in Algorithm_keys:
        #         Rows.append(key+str(j))
        #     j += 1
        #
        # print(Rows)
        # print(len(Rows))
        # df = pd.DataFrame(index=Rows,columns=columns)
        # print(df)
        # df.at[Rows[0],'Doc1'] = summative_features[Rows[0]]
        counter_par = 1
        counter_paragraph = 1
        # counter_title = 1
        counter_figure = 1
        counter_captionfigure = 1
        counter_table = 1
        counter_captiontable = 1
        # counter_abstractsection = 1
        # counter_abstractpar = 1
        counter_section = 1
        counter_subsection = 1
        counter_matrix = 1
        counter_enum = 1
        counter_formula = 1
        counter_algo = 1
        i = 0

        while (i < len(Rows)):
            if (i < 43):
                if (i < 12):
                    df.at[Rows[i], name] = summative_features[Rows[i]][1]
                    i += 1
                else:
                    df.at[Rows[i], name] = summative_features[Rows[i]]
                    i += 1
            elif (i < 155):
                if ('Par' in count_dct):
                    if (counter_par <= count_dct['Par']):
                        stri = 'Par' + str(counter_par)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            # df.loc[Rows[i]] = value
                            i += 1
                        counter_par += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            elif (i < 183):
                if ('Paragraph' in count_dct):
                    if (counter_paragraph <= count_dct['Paragraph']):
                        stri = 'Paragraph' + str(counter_paragraph)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            # df.loc[Rows[i]] = value
                            i += 1
                        counter_paragraph += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            # elif(i<245):
            #     if (counter_title <= count_dct['Title']):
            #         stri = 'Title' + str(counter_title)
            #         for value in dct[stri].values():
            #             df.at[Rows[i], 'Doc1'] = value
            #             i += 1
            #         counter_title += 1
            #     else:
            #         df.at[Rows[i], 'Doc1'] = 0
            #         i += 1
            elif (i < 223):
                if ('Figure' in count_dct):
                    if (counter_figure <= count_dct['Figure']):
                        stri = 'Figure' + str(counter_figure)
                        # print(stri)
                        # print("adi")
                        for value in dct[stri].values():
                            # print(Rows[i])
                            # print("adi1")
                            # print(name)
                            # print("adi2")
                            # print(value)
                            # print("adi3")
                            if value:
                              df.at[str(Rows[i]), str(name)] = value
                            else:
                              df.at[str(Rows[i]), str(name)] = 0
                            i += 1
                        counter_figure += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            elif (i < 263):
                if ('CaptionFigure' in count_dct):
                    if (counter_captionfigure <= count_dct['CaptionFigure']):
                        stri = 'CaptionFigure' + str(counter_captionfigure)
                        for value in dct[stri].values():
                            if value:
                                df.at[str(Rows[i]), str(name)] = value
                            else:
                                df.at[str(Rows[i]), str(name)] = 0
                            i += 1
                        counter_captionfigure += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            # elif (i < 413):
            #     if (counter_abstractsection <= count_dct['AbstractSection']):
            #         stri = 'AbstractSection' + str(counter_abstractsection)
            #         for value in dct[stri].values():
            #             df.at[Rows[i], 'Doc1'] = value
            #             i += 1
            #         counter_abstractsection += 1
            #     else:
            #         df.at[Rows[i], 'Doc1'] = 0
            #         i += 1
            # elif (i < 427):
            #     if (counter_abstractpar <= count_dct['AbstractPar']):
            #         stri = 'AbstractPar' + str(counter_abstractpar)
            #         for value in dct[stri].values():
            #             df.at[Rows[i], 'Doc1'] = value
            #             i += 1
            #         counter_abstractpar += 1
            #     else:
            #         df.at[Rows[i], 'Doc1'] = 0
            #         i += 1
            elif (i < 283):
                if ('Table' in count_dct):
                    if (counter_table <= count_dct['Table']):
                        stri = 'Table' + str(counter_table)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            i += 1
                        counter_table += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            elif (i < 303):
                if ('CaptionTable' in count_dct):
                    if (counter_captiontable <= count_dct['CaptionTable']):
                        stri = 'CaptionTable' + str(counter_captiontable)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            i += 1
                        counter_captiontable += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            elif (i < 327):
                if ('Section' in count_dct):
                    if (counter_section <= count_dct['Section']):
                        stri = 'Section' + str(counter_section)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            i += 1
                        counter_section += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            elif (i < 351):
                if ('SubSection' in count_dct):
                    if (counter_subsection <= count_dct['SubSection']):
                        stri = 'SubSection' + str(counter_subsection)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            i += 1
                        counter_subsection += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            # elif (i < 320):
            #     if ('Matrix' in count_dct):
            #         if (counter_matrix <= count_dct['Matrix']):
            #             stri = 'Matrix' + str(counter_matrix)
            #             for value in dct[stri].values():
            #                 if value:
            #                     df.at[Rows[i], name] = value
            #                 else:
            #                     df.at[Rows[i], name] = 0
            #                 i += 1
            #             counter_matrix += 1
            #         else:
            #             df.at[Rows[i], name] = 0
            #             i += 1
            #     else:
            #         df.at[Rows[i], name] = 0
            #         i += 1
            elif (i < 421):
                if ('Enum' in count_dct):
                    if (counter_enum <= count_dct['Enum']):
                        stri = 'Enum' + str(counter_enum)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            i += 1
                        counter_enum += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            elif (i < 461):
                if ('Formula' in count_dct):
                    if (counter_formula <= count_dct['Formula']):
                        stri = 'Formula' + str(counter_formula)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            i += 1
                        counter_formula += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            elif (i < 479):
                if ('Algorithm' in count_dct):
                    if (counter_algo <= count_dct['Algorithm']):
                        stri = 'Algorithm' + str(counter_algo)
                        for value in dct[stri].values():
                            if value:
                                df.at[Rows[i], name] = value
                            else:
                                df.at[Rows[i], name] = 0
                            i += 1
                        counter_algo += 1
                    else:
                        df.at[Rows[i], name] = 0
                        i += 1
                else:
                    df.at[Rows[i], name] = 0
                    i += 1
            elif (i < 483):  # operators
                df.at[Rows[i], name] = 0
                i += 1
            elif (i < 487):  # classes
                df.at[Rows[i], name] = 0
                i += 1

    # print(df)
    # print(df.T)
    # df2 = df.T
    return df
    # return df,files_created
    # df2.to_csv('example.csv')


def run_from_outside(latex_path, pdf_path, bib_path, path_to_save_lidor_dct,
                     path_to_save_adi_dct, name, df):
    try:

        df = run_feature_extraction(latex_path, pdf_path, bib_path, path_to_save_lidor_dct,
                                    path_to_save_adi_dct, name, df)
        return df
    except Exception as e:
        print(e)
        if df.empty:
            return df
        df[name] = [0 for x in range(df.shape[0])]
        return df


if __name__ == "__main__":
    path = sys.argv[1]
    permutation_num = sys.argv[3]
    file_num = sys.argv[2]
    excel_path = sys.argv[4]
    bib_path = sys.argv[5]
    line_num = int(sys.argv[6])
    path_to_save_lidor = sys.argv[7]
    path_to_save_adi = sys.argv[8]
    print(path_to_save_adi)

    latex_path = path + "/" + file_num + "_" + permutation_num + ".tex"
    # latex_path=path+"_"+permutation_num+".tex"
    # pdf_path = path+"_"+permutation_num+".pdf	"

    pdf_path = path + "/" + file_num + "_" + permutation_num + ".pdf"

    pdf_path_lidor = path_to_save_lidor + "/" + file_num + "_" + permutation_num
    pdf_path_adi = path_to_save_adi + "/" + file_num + "_" + permutation_num
    print(pdf_path_adi)
    file_name = file_num + "_" + permutation_num

    try:
        df = run_feature_extraction(latex_path, pdf_path, bib_path, pdf_path_lidor, pdf_path_adi, file_name)
        # df.to_csv(excel_path, mode="a", header=False)
        # df.to_excel(excel_path)

        my_path = Path(excel_path)
        if my_path.exists():
            df.to_csv(excel_path, mode='a', index=True, header=False)
        else:
            df.to_csv(excel_path, index=True, header=True)
    except:
        summative_features_keys = ['max_lines_par', 'min_lines_par', 'max_lines_enum', 'min_lines_enum',
                                   'max_lines_caption', 'min_lines_caption', 'max_figure_y_space', 'min_figure_y_space',
                                   'max_table_y_space', 'min_table_y_space',
                                   'max_height_object', 'min_height_object', 'num_of_elements',
                                   'sum_space_taken',
                                   'sum_open_space', 'sum_space_taken_by_figures', 'sum_space_taken_by_tables',
                                   'sum_of_chars_across_doc',
                                   'sum_of_words_from_pars', 'sum_of_chars_from_pars', 'avg_num_of_words_from_pars',
                                   'avg_num_of_chars_from_pars', 'num_of_paragraphs_with_1_word_at_the_end',
                                   'num_of_figures_with_captions', 'num_of_tables_with_captions', 'ending_y_of_doc']
        columns = []
        # name = list_latex_files.split(".")[0]
        for i in range(1):
            columns.append(file_name)
        Rows = []
        for key in summative_features_keys:
            Rows.append(key)

        Par_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                    'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                    'single_word_in_last_line', 'space_between_this_object_and_last_object',
                    'space_between_this_object_and_the_next_object']
        Title_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                      'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                      'single_word_in_last_line', 'space_between_this_object_and_last_object',
                      'space_between_this_object_and_the_next_object']
        Figure_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'figure_has_caption', 'figure_position_param',
                       'space_between_this_object_and_last_object', 'space_between_caption_and_figure',
                       'space_between_this_object_and_the_next_object']
        CaptionFigure_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'number_of_lines',
                              'last_line_length_chars',
                              'last_line_length_words', 'space_between_this_object_and_last_object',
                              'space_between_this_object_and_the_next_object']
        Table_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'table_has_caption', 'table_position_param',
                      'space_between_this_object_and_last_object', 'space_between_caption_and_table',
                      'space_between_this_object_and_the_next_object']
        CaptionTable_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'number_of_lines',
                             'last_line_length_chars',
                             'last_line_length_words', 'space_between_this_object_and_last_object',
                             'space_between_this_object_and_the_next_object']
        AbstractSection_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                                'space_between_this_object_and_last_object',
                                'space_between_this_object_and_the_next_object']
        AbstractPar_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                            'number_of_lines', 'num_of_chars', 'num_of_words', 'last_line_length_chars',
                            'last_line_length_words', 'single_word_in_last_line',
                            'space_between_this_object_and_last_object',
                            'space_between_this_object_and_the_next_object']
        Section_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                        'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        SubSection_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                           'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']
        # subsubsection to add
        Matrix_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'space_between_this_object_and_last_object',
                       'space_between_this_object_and_the_next_object']
        Enum_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                     'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                     'single_word_in_last_line', 'space_between_this_object_and_last_object',
                     'space_between_this_object_and_the_next_object']
        Formula_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'space_between_this_object_and_last_object',
                        'space_between_this_object_and_the_next_object']
        Algorithm_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                          'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']

        operators_keys = ['type', 'value', 'object_used_on', 'num_of_object']
        classes_keys = ['y_gained', 'lines_we_gained', 'binary_class', 'herustica']

        j = 0
        # 8 pars:
        for i in range(8):  # 8*14 = 112+26(starting features) 138
            for key in Par_keys:
                Rows.append(key + str(j))
            j += 1
        # #0 titles at most #1*14 = 14 #245
        # for key in Title_keys:
        #     Rows.append(key+str(j))
        #     j += 1
        # 4 figures at most #4*10 = 40 178
        for i in range(4):
            for key in Figure_keys:
                Rows.append(key + str(j))
            j += 1
        # 4 CaptionFigures at most #4*10 = 40 218
        for i in range(4):
            for key in CaptionFigure_keys:
                Rows.append(key + str(j))
            j += 1
        # 2 Tables at most 2*10 = 20 238
        for i in range(2):
            for key in Table_keys:
                Rows.append(key + str(j))
            j += 1
        # 2 CaptionTables at most 2*10 = 20 258
        for i in range(2):
            for key in CaptionTable_keys:
                Rows.append(key + str(j))
            j += 1
        # #0 AbstractSec at most #1*8 = 8 417
        # for key in AbstractSection_keys:
        #     Rows.append(key+str(j))
        #     j += 1
        # #0 AbstractPar at most #1*14 = 14 421
        # for key in AbstractPar_keys:
        #     Rows.append(key+str(j))
        #     j += 1
        # 3 sections at most #3*8 = 24 282
        for i in range(3):
            for key in Section_keys:
                Rows.append(key + str(j))
            j += 1
        # 3 subsections at most #3*8 = 24 306
        for i in range(3):
            for key in SubSection_keys:
                Rows.append(key + str(j))
            j += 1
        # 2 matrixes at most #2*7 = 14 320
        for i in range(2):
            for key in Matrix_keys:
                Rows.append(key + str(j))
            j += 1
        # 5 Enum at most #5*14 = 70 390
        for i in range(5):
            for key in Enum_keys:
                Rows.append(key + str(j))
            j += 1
        # 5 Formulas at most #5*7 = 35 425
        for i in range(5):
            for key in Formula_keys:
                Rows.append(key + str(j))
            j += 1
        # 2 Algorithms at most #2*8 = 16 441
        for i in range(2):
            for key in Algorithm_keys:
                Rows.append(key + str(j))
            j += 1
        # 4 operator defining features at most 4 => 445
        for key in operators_keys:
            Rows.append(key)
        j += 1
        # 4 Classes at most 4 => 449
        for key in classes_keys:
            Rows.append(key)
        j += 1
        print(Rows)
        print(len(Rows))
        df = pd.DataFrame(index=Rows, columns=columns)
        x = df.T
        my_path = Path(excel_path)
        if my_path.exists():
            x.to_csv(excel_path, mode='a', index=True, header=False)
        else:
            x.to_csv(excel_path, index=True, header=True)

    # with pd.ExcelWriter(excel_path, mode='a') as writer:
    #    df.to_excel(writer, sheet_name="Sheet1", startrow=line_num, header=False)
    # # df.to_excel(excel_path,index=True,header=True)
    # writer = pd.ExcelWriter(excel_path, engine='openpyxl')
    # # df.to_excel(writer,index=True,header=True)
    # # book = openpyxl.load_workbook(excel_path)
    # # writer.book = book
    #
    # df.to_excel(writer, startrow=file_num)
    # # df.to_excel(writer, sheet_name="sheetname", startrow=writer.sheets["sheetname"].max_row, index=False, header=True)
    # writer.save()