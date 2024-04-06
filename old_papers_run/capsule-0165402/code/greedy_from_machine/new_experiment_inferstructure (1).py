import feature_extraction_for_search_algorithm
import get_pdf_order
import using_operators
import using_operators_for_adi
import re
import pickle
import read_single_file
import os
import time
import sys
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def simulating_vspace_for_prediction(value, key,operator_value,df_copy):  # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    type = 1
    value_of_operator = 0 #to be determined
    object_used_on = ''.join([i for i in key if not i.isdigit()])
    num_of_object = re.findall(r'\d+', str(key))[0]
    print(object_used_on)
    print(num_of_object)
    print(value['space_between_this_object_and_last_object'])
    vspace_sizes = []
    if (value['space_between_this_object_and_last_object'] > 10):  # candidate to add vspace
        # object_to_add_vspace_behind = key
        print()
        if ('Formula' in key):
            # we will make 3 partitions:
            vspace_size_max = value['space_between_this_object_and_last_object'] / 7
            herustica = 0
            vspace_size_part = vspace_size_max / 4
            for i in range(1, 5):
                print("Part " + str(i) + " :")
                vspace_size = "{:.2f}".format(vspace_size_part * i)
                vspace_sizes.append(vspace_size)
                print("vspace size: " + str(vspace_size))
                # latex_clean_lines.insert(chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n')
        else:
            vspace_size_max = value['space_between_this_object_and_last_object'] / 3.5
            vspace_size_part = vspace_size_max / 4
            for i in range(1, 5):
                print("Part " + str(i) + " :")
                herustica = (value['space_between_this_object_and_last_object'] * i) / 4
                vspace_size = "{:.2f}".format(vspace_size_part * i)
                vspace_sizes.append(vspace_size)
                print("vspace size: " + str(vspace_size))
                # latex_clean_lines.insert(chosen_index_to_insert, '\\vspace{-' + str(vspace_size) + 'mm}\n')
        #now we have the vspace sizes, now we will take the chosen one.
        value_of_operator = vspace_sizes[operator_value-1]
        #now we will create a new row that we will give to the model to predict
        df_copy.at['type','Doc0'] = type
        df_copy.at['value', 'Doc0'] = value_of_operator
        df_copy.at['object_used_on', 'Doc0'] = object_used_on
        df_copy.at['num_of_object', 'Doc0'] = num_of_object
        print(df_copy)
        #df_copy = df_copy.T
        #now we have the new df, and now we can predict to see if it fits
        #first we need to select the right model
        #model = RandomForestRegressor(max_depth=2, random_state=0)
        #prediction
        #return the prediction and confidance
        return 0,0,type,value_of_operator,object_used_on,num_of_object,df_copy
    else:
        return -1,-1,-1,-1,-1,-1,-1

def simulating_figure_reduction_for_prediction(value, key,operator_value,df_copy):  # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    type = 2
    value_of_operator = 0
    object_used_on = ''.join([i for i in key if not i.isdigit()])
    num_of_object = re.findall(r'\d+', str(key))[0]
    print(object_used_on)
    print(num_of_object)
    print(value['space_between_this_object_and_last_object'])
    figure_scale_sizes = [0.9, 0.8, 0.7, 0.6, 0.5]
    #now we have the figure scale sizes, now we will take the chosen one.
    value_of_operator = figure_scale_sizes[operator_value]
    #now we will create a new row that we will give to the model to predict
    df_copy.at['type','Doc0'] = type
    df_copy.at['value', 'Doc0'] = value_of_operator
    df_copy.at['object_used_on', 'Doc0'] = object_used_on
    df_copy.at['num_of_object', 'Doc0'] = num_of_object
    print(df_copy)
    #df_copy = df_copy.T
    #now we have the new df, and now we can predict to see if it fits
    #first we need to select the right model
    #model = RandomForestRegressor(max_depth=2, random_state=0)
    #prediction
    #return the prediction and confidance
    return 0,0,type,value_of_operator,object_used_on,num_of_object,df_copy

def simulating_algo_reduction_for_prediction(value, key,operator_value,df_copy):  # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    type = 3
    value_of_operator = 0
    object_used_on = ''.join([i for i in key if not i.isdigit()])
    num_of_object = re.findall(r'\d+', str(key))[0]
    print(object_used_on)
    print(num_of_object)
    print(value['space_between_this_object_and_last_object'])
    table_sizes = [1]
    #now we have the figure scale sizes, now we will take the chosen one.
    value_of_operator = table_sizes[operator_value]
    #now we will create a new row that we will give to the model to predict
    df_copy.at['type','Doc0'] = type
    df_copy.at['value', 'Doc0'] = value_of_operator
    df_copy.at['object_used_on', 'Doc0'] = object_used_on
    df_copy.at['num_of_object', 'Doc0'] = num_of_object
    print(df_copy)
    #df_copy = df_copy.T
    #now we have the new df, and now we can predict to see if it fits
    #first we need to select the right model
    #model = RandomForestRegressor(max_depth=2, random_state=0)
    #prediction
    #return the prediction and confidance
    return 0,0,type,value_of_operator,object_used_on,num_of_object,df_copy

def simulating_enum_operator_for_prediction(value, key,operator_value,df_copy):  # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    type = 4
    value_of_operator = 0
    object_used_on = ''.join([i for i in key if not i.isdigit()])
    num_of_object = re.findall(r'\d+', str(key))[0]
    print(object_used_on)
    print(num_of_object)
    print(value['space_between_this_object_and_last_object'])
    table_sizes = [1]
    #now we have the figure scale sizes, now we will take the chosen one.
    value_of_operator = table_sizes[operator_value]
    #now we will create a new row that we will give to the model to predict
    df_copy.at['type','Doc0'] = type
    df_copy.at['value', 'Doc0'] = value_of_operator
    df_copy.at['object_used_on', 'Doc0'] = object_used_on
    df_copy.at['num_of_object', 'Doc0'] = num_of_object
    print(df_copy)
    #df_copy = df_copy.T
    #now we have the new df, and now we can predict to see if it fits
    #first we need to select the right model
    #model = RandomForestRegressor(max_depth=2, random_state=0)
    #prediction
    #return the prediction and confidance
    return 0,0,type,value_of_operator,object_used_on,num_of_object,df_copy

def simulating_paragraph_tag_operator_for_prediction(value, key,operator_value,df_copy):  # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    type = 5
    value_of_operator = 0
    object_used_on = ''.join([i for i in key if not i.isdigit()])
    num_of_object = re.findall(r'\d+', str(key))[0]
    print(object_used_on)
    print(num_of_object)
    print(value['space_between_this_object_and_last_object'])
    table_sizes = [1]
    #now we have the figure scale sizes, now we will take the chosen one.
    value_of_operator = table_sizes[operator_value]
    #now we will create a new row that we will give to the model to predict
    df_copy.at['type','Doc0'] = type
    df_copy.at['value', 'Doc0'] = value_of_operator
    df_copy.at['object_used_on', 'Doc0'] = object_used_on
    df_copy.at['num_of_object', 'Doc0'] = num_of_object
    print(df_copy)
    #df_copy = df_copy.T
    #now we have the new df, and now we can predict to see if it fits
    #first we need to select the right model
    #model = RandomForestRegressor(max_depth=2, random_state=0)
    #prediction
    #return the prediction and confidance
    return 0,0,type,value_of_operator,object_used_on,num_of_object,df_copy

def simulating_combine_paragraphs_for_prediction(value,key_1, key_2,operator_value,df_copy):  # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    type = 6
    value_of_operator = 0
    object_used_on = ''.join([i for i in key_2 if not i.isdigit()])
    num_of_object = re.findall(r'\d+', str(key))[0]
    print(object_used_on)
    print(num_of_object)
    print(value['space_between_this_object_and_last_object'])
    table_sizes = [1]
    #now we have the figure scale sizes, now we will take the chosen one.
    value_of_operator = table_sizes[operator_value]
    #now we will create a new row that we will give to the model to predict
    df_copy.at['type','Doc0'] = type
    df_copy.at['value', 'Doc0'] = value_of_operator
    df_copy.at['object_used_on', 'Doc0'] = object_used_on
    df_copy.at['num_of_object', 'Doc0'] = num_of_object
    print(df_copy)
    #df_copy = df_copy.T
    #now we have the new df, and now we can predict to see if it fits
    #first we need to select the right model
    #model = RandomForestRegressor(max_depth=2, random_state=0)
    #prediction
    #return the prediction and confidance
    return 0,0,type,value_of_operator,object_used_on,num_of_object,df_copy

def simulating_table_reduction_for_prediction(value, key,operator_value,df_copy):  # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    type = 7
    value_of_operator = 0
    object_used_on = ''.join([i for i in key if not i.isdigit()])
    num_of_object = re.findall(r'\d+', str(key))[0]
    print(object_used_on)
    print(num_of_object)
    print(value['space_between_this_object_and_last_object'])
    table_sizes = [0.9, 0.8, 0.7, 0.6]
    #now we have the figure scale sizes, now we will take the chosen one.
    value_of_operator = table_sizes[operator_value]
    #now we will create a new row that we will give to the model to predict
    df_copy.at['type','Doc0'] = type
    df_copy.at['value', 'Doc0'] = value_of_operator
    df_copy.at['object_used_on', 'Doc0'] = object_used_on
    df_copy.at['num_of_object', 'Doc0'] = num_of_object
    print(df_copy)
    #df_copy = df_copy.T
    #now we have the new df, and now we can predict to see if it fits
    #first we need to select the right model
    #model = RandomForestRegressor(max_depth=2, random_state=0)
    #prediction
    #return the prediction and confidance
    return 0,0,type,value_of_operator,object_used_on,num_of_object,df_copy

# def simulating_tag_removal_for_prediction(value, key,operator_value,df_copy):  # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
#     type = 8
#     value_of_operator = 0
#     object_used_on = ''.join([i for i in key if not i.isdigit()])
#     num_of_object = re.findall(r'\d+', str(key))[0]
#     print(object_used_on)
#     print(num_of_object)
#     print(value['space_between_this_object_and_last_object'])
#     table_sizes = [1]
#     #now we have the figure scale sizes, now we will take the chosen one.
#     value_of_operator = table_sizes[operator_value]
#     #now we will create a new row that we will give to the model to predict
#     df_copy.at['type','Doc0'] = type
#     df_copy.at['value', 'Doc0'] = value_of_operator
#     df_copy.at['object_used_on', 'Doc0'] = object_used_on
#     df_copy.at['num_of_object', 'Doc0'] = num_of_object
#     print(df_copy)
#     #df_copy = df_copy.T
#     #now we have the new df, and now we can predict to see if it fits
#     #first we need to select the right model
#     #model = RandomForestRegressor(max_depth=2, random_state=0)
#     #prediction
#     #return the prediction and confidance
#     return 0,0,type,value_of_operator,object_used_on,num_of_object,df_copy



def simulating_using_vspace(value_of_operator,object_used_on,num_of_object,df_copy,summative_features,dct_of_elements_in_order): # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    #first we will need to evaluate index inside the csv(df_copy) to a real object, if it existed:
    #REMEMBER VSPACE IS ADDED BEFORE THE OBJECT IT IS USED ON
    Par_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                'single_word_in_last_line', 'space_between_this_object_and_last_object',
                'space_between_this_object_and_the_next_object']
    Paragraph_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                      'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                      'single_word_in_last_line', 'space_between_this_object_and_last_object',
                      'space_between_this_object_and_the_next_object']

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

    Section_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                    'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']

    SubSection_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                       'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']

    Enum_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height', 'number_of_lines',
                 'num_of_chars', 'num_of_words', 'last_line_length_chars', 'last_line_length_words',
                 'single_word_in_last_line', 'space_between_this_object_and_last_object',
                 'space_between_this_object_and_the_next_object']

    Formula_keys = ['page', 'column', 'start_y', 'end_y', 'height', 'bad_detection_formula',
                    'space_between_this_object_and_last_object',
                    'space_between_this_object_and_the_next_object']

    Algorithm_keys = ['page', 'column', 'start_y', 'end_y', 'spread_on_more_than_1_column', 'height',
                      'algorithm_position_param',
                      'space_between_this_object_and_last_object', 'space_between_this_object_and_the_next_object']

    dict_for_indexes = {0:'Par',1:'Par',2:'Par',3:'Par',4:'Par',5:'Par',6:'Par',7:'Par',8:'Paragraph',9:'Paragraph',10:'Figure',11:'Figure',12:'Figure',13:'Figure',14:'CaptionFigure',15:'CaptionFigure',16:'CaptionFigure',17:'CaptionFigure',18:'Table',19:'Table',20:'CaptionTable',21:'CaptionTable',22:'Section',23:'Section',24:'Section',25:'SubSection',26:'SubSection',27:'SubSection',28:'Enum',29:'Enum',30:'Enum',31:'Enum',32:'Enum',33:'Formula',34:'Formula',35:'Formula',36:'Formula',37:'Formula',38:'Algorithm',39:'Algorithm'}
    dict_for_indexes_inverse = {'Par1':0, 'Par2':1, 'Par3':2, 'Par4':3, 'Par5':4, 'Par6':5, 'Par7':6, 'Par8':7, 'Paragraph1':8,
                        'Paragraph2':9, 'Figure1':10, 'Figure2':11, 'Figure3':12, 'Figure4':13, 'CaptionFigure1':14,
                        'CaptionFigure2':15, 'CaptionFigure3':16, 'CaptionFigure4':17, 'Table1':18, 'Table2':19,
                        'CaptionTable1':20, 'CaptionTable2':21,'Section1':22, 'Section2':23, 'Section3':24,
                        'SubSection1':25, 'SubSection2':26, 'SubSection3':27, 'Enum1':28, 'Enum2':29, 'Enum3':30,
                        'Enum4':31, 'Enum5':32, 'Formula1':33, 'Formula2':34, 'Formula3':35, 'Formula4':36,
                        'Formula5':37, 'Algorithm1':38, 'Algorithm2':39}
    object_used_on_combind_with_num_of_object = object_used_on+str(num_of_object)
    #we can know the hierarchy based on
    start_remembering = False
    objects_after_chosen_object = []
    last_key = 0
    for key in dct_of_elements_in_order.keys():
        if(object_used_on_combind_with_num_of_object == key):
            print(key)
            print(object_used_on_combind_with_num_of_object)
            objects_after_chosen_object.append(last_key) #we will want to add the object before the object on which we performed the operator (vspace) so we can reduce his space_between_this_object_and_the_next_object
            objects_after_chosen_object.append(key) #adding the object on which we performed the operator(vspace)
            start_remembering = True
            continue
        if(start_remembering):
            objects_after_chosen_object.append(key)
        last_key = key
    print(objects_after_chosen_object)
    indexx = 0
    reduce_by_20 = False
    skip_next = False
    #now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)
    for j in objects_after_chosen_object:
        object_without_index = ''.join([i for i in j if not i.isdigit()])
        get_index_representing_object_in_csv = dict_for_indexes_inverse[j]
        after_object_key = objects_after_chosen_object[indexx + 1]  # captions
        get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
        if(j == objects_after_chosen_object[0]): #object before the object on which we performed the operator (vspace)
            if(object_without_index == 'Table'): #it has an extra feature, same for figures
                if(df_copy.at['space_between_caption_and_table' + str(get_index_representing_object_in_csv), 'Doc0'] - 10 > 0):
                    df_copy.at['space_between_caption_and_table' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    #caption
                    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                if(df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_object_in_csv), 'Doc0'] - 10 > 0):
                    df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            elif(object_without_index == 'Figure'):
                if(df_copy.at['space_between_caption_and_figure' + str(get_index_representing_object_in_csv), 'Doc0'] - 10 > 0):
                    df_copy.at['space_between_caption_and_figure' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                if(df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_object_in_csv), 'Doc0'] - 10 > 0):
                    df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            else:
                df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                # caption
                df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            indexx+=1
            continue
        if(skip_next):
            skip_next = False
            indexx+=1
            continue
        if(object_without_index == 'Par' or object_without_index == 'Paragraph' or object_without_index == 'Enum'): #to move a par,paragraph,enum to a before column we will need at least 3 rows of free space, so we will need to check it
            print(j)
            if(df_copy.at['start_y'+str(get_index_representing_object_in_csv),'Doc0'] < 60): #if the par,paragraph,enum is the first object in the column
                #we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx-1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if(df_copy.at['end_y'+str(get_index_representing_before_object_in_csv),'Doc0'] < 670 and df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] > 660): #there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 680 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_before_object_in_csv), 'Doc0'] = space_between #update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_object_in_csv), 'Doc0'] = space_between
                    #now we will change the par,paragraph,enum information:
                    if(df_copy.at['page'+str(get_index_representing_object_in_csv),'Doc0'] == 1 and df_copy.at['column'+str(get_index_representing_object_in_csv),'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 680
                    if(df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] > 85): #some of the par,paragraph,enum will still stay on the 2nd column
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                        df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                else: #at this point nothing can change because there is not enough space to move
                    break
            else: #nothing moves to another column
                if(reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y'+str(get_index_representing_object_in_csv),'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif(object_without_index == 'Section' or object_without_index == 'SubSection'):
            print(j)
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the section,subsection is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 680 and df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] > 670):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 690 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 690
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10

        elif(object_without_index == 'Formula' or object_without_index == 'Algorithm'):
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60 and df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] > 0):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
                if(abs(700 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700-space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:
                    break #nothing can change past him
            else: #place to move
                # i will try to fix a bug here:
                if(df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0 and df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0):
                    if (reduce_by_20):
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif(object_without_index == 'Figure' or object_without_index == 'Table'): #we will need to move them as a chunk
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] + df_copy.at['height' + str(get_index_representing_after_object_in_csv), 'Doc0']
                if(abs(700 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        #caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        #caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700-space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] + df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
                    #caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] + 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 700
                else:
                    break #nothing can change past him
            else: #place to move
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    #caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    #caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            skip_next = True

        indexx += 1

    # update summative features:
    # stuff about pars first:
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
    sum_space_taken = 0
    sum_open_space = 0
    sum_of_chars_across_doc = 0
    sum_of_chars_from_pars = 0
    sum_of_words_from_pars = 0
    num_of_paragraphs_with_1_word_at_the_end = 0

    num_of_pars = count_dict_of_elements['Par']
    num_of_elements = len(dct_of_elements_in_order)
    num_of_paragraphs = count_dict_of_elements['Paragraph']
    num_of_algorithms = count_dict_of_elements['Algorithm']
    num_of_formulas = count_dict_of_elements['Formula']
    num_of_enums = count_dict_of_elements['Enum']
    num_of_captionfigures = count_dict_of_elements['CaptionFigure']
    num_of_captiontables = count_dict_of_elements['CaptionTable']
    num_of_figures = count_dict_of_elements['Figure']
    num_of_tables = count_dict_of_elements['Table']
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []

    for i in range(0, num_of_pars):
        list_1.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_pars_in_col_1 += 1
        else:
            num_of_pars_in_col_2 += 1
        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(8, num_of_paragraphs + 8):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_paragraphs_in_col_1 += 1
        else:
            num_of_paragraphs_in_col_2 += 1

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(28, num_of_enums + 28):
        list_2.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']

    if (len(list_2) != 0):
        max_lines_enum = max(list_2)
        min_lines_enum = min(list_2)
    else:
        max_lines_enum = 0
        min_lines_enum = 0

    for i in range(14, num_of_captionfigures + 14):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    for i in range(20, num_of_captiontables + 20):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    if (len(list_3) != 0):
        max_lines_caption = max(list_3)
        min_lines_caption = min(list_3)
    else:
        max_lines_caption = 0
        min_lines_caption = 0

    for i in range(10, num_of_figures + 10):
        list_4.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_figures_in_col_1 += 1
        else:
            num_of_figures_in_col_2 += 1

    if (len(list_4) != 0):
        max_figure_y_space = max(list_4)
        min_figure_y_space = min(list_4)
        sum_space_taken_by_figures = sum(list_4)
    else:
        max_figure_y_space = 0
        min_figure_y_space = 0
        sum_space_taken_by_figures = 0

    for i in range(18, num_of_tables + 18):
        list_5.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_tables_in_col_1 += 1
        else:
            num_of_tables_in_col_2 += 1

    if (len(list_5) != 0):
        max_table_y_space = max(list_5)
        min_table_y_space = min(list_5)
        sum_space_taken_by_tables = sum(list_5)
    else:
        max_table_y_space = 0
        min_table_y_space = 0
        sum_space_taken_by_tables = 0

    part_of_last_height = 0
    for i in range(0, 39):
        if (df_copy.at['height' + str(i), 'Doc0'] > 0):
            list_6.append(df_copy.at['height' + str(i), 'Doc0'])
            sum_space_taken += df_copy.at['height' + str(i), 'Doc0']
        if (df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] > 0):
            sum_open_space += df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0']

        if(df_copy.at['start_y' + str(i), 'Doc0'] > df_copy.at['end_y' + str(i), 'Doc0'] and df_copy.at['column' + str(i), 'Doc0'] == 1): #we will want to see if there is an object that starts at the 2nd to last column and spread to the next column
            #we found one that starts at column 1 and ends on the 2nd page
            part_of_last_height += df_copy.at['end_y' + str(i), 'Doc0'] - 50
        if(df_copy.at['page' + str(i), 'Doc0'] == 1): #on the last page we will take all of the objects height
            part_of_last_height += df_copy.at['height' + str(i), 'Doc0']

    new_ending_y =  part_of_last_height

    if (len(list_6) != 0):
        max_height_object = max(list_6)
        min_height_object = min(list_6)
    else:
        max_height_object = 0
        min_height_object = 0

    for i in range(38, num_of_algorithms + 38):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_algorithms_in_col_1 += 1
        else:
            num_of_algorithms_in_col_2 += 1

    for i in range(33, num_of_formulas + 33):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_formulas_in_col_1 += 1
        else:
            num_of_formulas_in_col_2 += 1

    last_element = list(dct_of_elements_in_order)[-1]
    get_index_of_last_element = dict_for_indexes_inverse[last_element]
    last_element_with_no_index = ''.join([i for i in last_element if not i.isdigit()])
    if (last_element_with_no_index == 'Par'):
        last_object_index = 1
    elif (last_element_with_no_index == 'Figure'):
        last_object_index = 2
    elif (last_element_with_no_index == 'CaptionFigure'):
        last_object_index = 3
    elif (last_element_with_no_index == 'Table'):
        last_object_index = 4
    elif (last_element_with_no_index == 'CaptionTable'):
        last_object_index = 5
    elif (last_element_with_no_index == 'Section'):
        last_object_index = 6
    elif (last_element_with_no_index == 'SubSection'):
        last_object_index = 7
    elif (last_element_with_no_index == 'Matrix'):
        last_object_index = 8
    elif (last_element_with_no_index == 'Enum'):
        last_object_index = 9
    elif (last_element_with_no_index == 'Formula'):
        last_object_index = 10
    elif (last_element_with_no_index == 'Algorithm'):
        last_object_index = 11
    else:
        last_object_index = 0

    if (len(list_1) != 0):
        max_lines_par = max(list_1)
        min_lines_par = min(list_1)
    else:
        max_lines_par = 0
        min_lines_par = 0

    if (count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'] != 0):
        avg_num_of_words_from_pars = sum_of_words_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
        avg_num_of_chars_from_pars = sum_of_chars_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
    else:
        avg_num_of_words_from_pars = 0
        avg_num_of_chars_from_pars = 0

    num_of_figures_with_captions = num_of_figures
    num_of_tables_with_captions = num_of_tables

    # putting it all together:
    summative_features['max_lines_par'] = max_lines_par
    summative_features['min_lines_par'] = min_lines_par
    summative_features['max_lines_enum'] = max_lines_enum
    summative_features['min_lines_enum'] = min_lines_enum
    summative_features['max_lines_caption'] = max_lines_caption
    summative_features['min_lines_caption'] = min_lines_caption
    summative_features['max_figure_y_space'] = max_figure_y_space
    summative_features['min_figure_y_space'] = min_figure_y_space
    summative_features['max_table_y_space'] = max_table_y_space
    summative_features['min_table_y_space'] = min_table_y_space
    summative_features['max_height_object'] = max_height_object
    summative_features['min_height_object'] = min_height_object
    summative_features['num_of_elements'] = num_of_elements
    summative_features['num_of_pars'] = num_of_pars
    summative_features['num_of_pars_in_col_1'] = num_of_pars_in_col_1
    summative_features['num_of_pars_in_col_2'] = num_of_pars_in_col_2
    summative_features['num_of_paragraphs'] = num_of_paragraphs
    summative_features['num_of_paragraphs_in_col_1'] = num_of_paragraphs_in_col_1
    summative_features['num_of_paragraphs_in_col_2'] = num_of_paragraphs_in_col_2
    summative_features['num_of_algorithms'] = num_of_algorithms
    summative_features['num_of_algorithms_in_col_1'] = num_of_algorithms_in_col_1
    summative_features['num_of_algorithms_in_col_2'] = num_of_algorithms_in_col_2
    summative_features['num_of_formulas'] = num_of_formulas
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
    summative_features['avg_num_of_words_from_pars'] = avg_num_of_words_from_pars
    summative_features['avg_num_of_chars_from_pars'] = avg_num_of_chars_from_pars
    summative_features['num_of_paragraphs_with_1_word_at_the_end'] = num_of_paragraphs_with_1_word_at_the_end
    summative_features['num_of_figures_with_captions'] = num_of_figures_with_captions
    summative_features['num_of_tables_with_captions'] = num_of_tables_with_captions
    if (new_ending_y < summative_features['ending_y_of_doc']):
        summative_features['ending_y_of_doc'] = new_ending_y

    df_copy.at['max_lines_par', 'Doc0'] = max_lines_par
    df_copy.at['min_lines_par', 'Doc0'] = min_lines_par
    df_copy.at['max_lines_enum', 'Doc0'] = max_lines_enum
    df_copy.at['min_lines_enum', 'Doc0'] = min_lines_enum
    df_copy.at['max_lines_caption', 'Doc0'] = max_lines_caption
    df_copy.at['min_lines_caption', 'Doc0'] = min_lines_caption
    df_copy.at['max_figure_y_space', 'Doc0'] = max_figure_y_space
    df_copy.at['min_figure_y_space', 'Doc0'] = min_figure_y_space
    df_copy.at['max_table_y_space', 'Doc0'] = max_table_y_space
    df_copy.at['min_table_y_space', 'Doc0'] = min_table_y_space
    df_copy.at['max_height_object', 'Doc0'] = max_height_object
    df_copy.at['min_height_object', 'Doc0'] = min_height_object
    df_copy.at['num_of_elements', 'Doc0'] = num_of_elements
    df_copy.at['num_of_pars', 'Doc0'] = num_of_pars
    df_copy.at['num_of_pars_in_col_1', 'Doc0'] = num_of_pars_in_col_1
    df_copy.at['num_of_pars_in_col_2', 'Doc0'] = num_of_pars_in_col_2
    df_copy.at['num_of_paragraphs', 'Doc0'] = num_of_paragraphs
    df_copy.at['num_of_paragraphs_in_col_1', 'Doc0'] = num_of_paragraphs_in_col_1
    df_copy.at['num_of_paragraphs_in_col_2', 'Doc0'] = num_of_paragraphs_in_col_2
    df_copy.at['num_of_algorithms', 'Doc0'] = num_of_algorithms
    df_copy.at['num_of_algorithms_in_col_1', 'Doc0'] = num_of_algorithms_in_col_1
    df_copy.at['num_of_algorithms_in_col_2', 'Doc0'] = num_of_algorithms_in_col_2
    df_copy.at['num_of_formulas', 'Doc0'] = num_of_formulas
    df_copy.at['num_of_formulas_in_col_1', 'Doc0'] = num_of_formulas_in_col_1
    df_copy.at['num_of_formulas_in_col_2', 'Doc0'] = num_of_formulas_in_col_2
    df_copy.at['num_of_figures_in_col_1', 'Doc0'] = num_of_figures_in_col_1
    df_copy.at['num_of_figures_in_col_2', 'Doc0'] = num_of_figures_in_col_2
    df_copy.at['num_of_tables_in_col_1', 'Doc0'] = num_of_tables_in_col_1
    df_copy.at['num_of_tables_in_col_2', 'Doc0'] = num_of_tables_in_col_2
    df_copy.at['last_element', 'Doc0'] = last_object_index
    df_copy.at['sum_space_taken', 'Doc0'] = sum_space_taken
    df_copy.at['sum_open_space', 'Doc0'] = sum_open_space
    df_copy.at['sum_space_taken_by_figures', 'Doc0'] = sum_space_taken_by_figures
    df_copy.at['sum_space_taken_by_tables', 'Doc0'] = sum_space_taken_by_tables
    df_copy.at['sum_of_chars_across_doc', 'Doc0'] = sum_of_chars_across_doc
    df_copy.at['sum_of_words_from_pars', 'Doc0'] = sum_of_words_from_pars
    df_copy.at['sum_of_chars_from_pars', 'Doc0'] = sum_of_chars_from_pars
    df_copy.at['avg_num_of_words_from_pars', 'Doc0'] = avg_num_of_words_from_pars
    df_copy.at['avg_num_of_chars_from_pars', 'Doc0'] = avg_num_of_chars_from_pars
    df_copy.at['num_of_paragraphs_with_1_word_at_the_end', 'Doc0'] = num_of_paragraphs_with_1_word_at_the_end
    df_copy.at['num_of_figures_with_captions', 'Doc0'] = num_of_figures_with_captions
    df_copy.at['num_of_tables_with_captions', 'Doc0'] = num_of_tables_with_captions
    if (new_ending_y < df_copy.at['ending_y_of_doc', 'Doc0']):
        df_copy.at['ending_y_of_doc', 'Doc0'] = new_ending_y


    # df_copy = df_copy.T
    # df_copy.to_csv('pdf_extraction\\adi_comparing\\new_files\\example_test_for_me_1_4_2023_2.csv')
    # sys.exit()
    return dct_of_elements_in_order,count_dict_of_elements,summative_features,df_copy


def simulating_using_figure_reduction(value_of_operator,object_used_on,num_of_object,df_copy,summative_features,dct_of_elements_in_order): # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    dict_for_indexes = {0: 'Par', 1: 'Par', 2: 'Par', 3: 'Par', 4: 'Par', 5: 'Par', 6: 'Par', 7: 'Par', 8: 'Paragraph',
                        9: 'Paragraph', 10: 'Figure', 11: 'Figure', 12: 'Figure', 13: 'Figure', 14: 'CaptionFigure',
                        15: 'CaptionFigure', 16: 'CaptionFigure', 17: 'CaptionFigure', 18: 'Table', 19: 'Table',
                        20: 'CaptionTable', 21: 'CaptionTable', 22: 'Section', 23: 'Section', 24: 'Section',
                        25: 'SubSection', 26: 'SubSection', 27: 'SubSection', 28: 'Enum', 29: 'Enum', 30: 'Enum',
                        31: 'Enum', 32: 'Enum', 33: 'Formula', 34: 'Formula', 35: 'Formula', 36: 'Formula',
                        37: 'Formula', 38: 'Algorithm', 39: 'Algorithm'}
    dict_for_indexes_inverse = {'Par1': 0, 'Par2': 1, 'Par3': 2, 'Par4': 3, 'Par5': 4, 'Par6': 5, 'Par7': 6, 'Par8': 7,
                                'Paragraph1': 8,
                                'Paragraph2': 9, 'Figure1': 10, 'Figure2': 11, 'Figure3': 12, 'Figure4': 13,
                                'CaptionFigure1': 14,
                                'CaptionFigure2': 15, 'CaptionFigure3': 16, 'CaptionFigure4': 17, 'Table1': 18,
                                'Table2': 19,
                                'CaptionTable1': 20, 'CaptionTable2': 21, 'Section1': 22, 'Section2': 23,
                                'Section3': 24,
                                'SubSection1': 25, 'SubSection2': 26, 'SubSection3': 27, 'Enum1': 28, 'Enum2': 29,
                                'Enum3': 30,
                                'Enum4': 31, 'Enum5': 32, 'Formula1': 33, 'Formula2': 34, 'Formula3': 35,
                                'Formula4': 36,
                                'Formula5': 37, 'Algorithm1': 38, 'Algorithm2': 39}
    object_used_on_combind_with_num_of_object = object_used_on + str(num_of_object)
    # we can know the hierarchy based on
    start_remembering = False
    objects_after_chosen_object = []
    for key in dct_of_elements_in_order.keys():
        if (object_used_on_combind_with_num_of_object == key):
            print(key)
            print(object_used_on_combind_with_num_of_object)
            objects_after_chosen_object.append(key)  # adding the object on which we performed the operator
            start_remembering = True
            continue
        if (start_remembering):
            objects_after_chosen_object.append(key)
    print(objects_after_chosen_object)
    indexx = 0
    reduce_by_20 = False
    skip_next = False
    # now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)
    for j in objects_after_chosen_object: #first will always be the figure that we are manipulating
        object_without_index = ''.join([i for i in j if not i.isdigit()])
        get_index_representing_object_in_csv = dict_for_indexes_inverse[j]
        after_object_key = objects_after_chosen_object[indexx + 1]  # captions
        get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
        if(indexx == 0):#changing the figure
            #we will want to change the height of the figure and his ending y
            df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
            df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
            #we will also change his caption
            df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            indexx+=1
            continue
        #now we will change all the next objects after the figure and his caption
        if (skip_next):
            skip_next = False
            indexx += 1
            continue
        if (object_without_index == 'Par' or object_without_index == 'Paragraph' or object_without_index == 'Enum'):  # to move a par,paragraph,enum to a before column we will need at least 3 rows of free space, so we will need to check it
            print(j)
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the par,paragraph,enum is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 670 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 660):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 680 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 680
                    if (df_copy.at['end_y' + str(
                            get_index_representing_object_in_csv), 'Doc0'] > 85):  # some of the par,paragraph,enum will still stay on the 2nd column
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                        df_copy.at[
                            'spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (object_without_index == 'Section' or object_without_index == 'SubSection'):
            print(j)
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the section,subsection is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 680 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 670):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 690 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 690
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10

        elif (object_without_index == 'Formula' or object_without_index == 'Algorithm'):
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60 and df_copy.at[
                'start_y' + str(
                        get_index_representing_object_in_csv), 'Doc0'] > 0):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                # i will try to fix a bug here:
                if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0 and df_copy.at[
                    'end_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0):
                    if (reduce_by_20):
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (
                object_without_index == 'Figure' or object_without_index == 'Table'):  # we will need to move them as a chunk
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] + df_copy.at[
                    'height' + str(get_index_representing_after_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                  'start_y' + str(
                                                                                                      get_index_representing_object_in_csv), 'Doc0'] + \
                                                                                              df_copy.at['height' + str(
                                                                                                  get_index_representing_object_in_csv), 'Doc0']
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                          'end_y' + str(
                                                                                                              get_index_representing_object_in_csv), 'Doc0'] + 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            skip_next = True

        indexx += 1

    # update summative features:
    # stuff about pars first:
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
    sum_space_taken = 0
    sum_open_space = 0
    sum_of_chars_across_doc = 0
    sum_of_chars_from_pars = 0
    sum_of_words_from_pars = 0
    num_of_paragraphs_with_1_word_at_the_end = 0

    num_of_pars = count_dict_of_elements['Par']
    num_of_elements = len(dct_of_elements_in_order)
    num_of_paragraphs = count_dict_of_elements['Paragraph']
    num_of_algorithms = count_dict_of_elements['Algorithm']
    num_of_formulas = count_dict_of_elements['Formula']
    num_of_enums = count_dict_of_elements['Enum']
    num_of_captionfigures = count_dict_of_elements['CaptionFigure']
    num_of_captiontables = count_dict_of_elements['CaptionTable']
    num_of_figures = count_dict_of_elements['Figure']
    num_of_tables = count_dict_of_elements['Table']
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []

    for i in range(0, num_of_pars):
        list_1.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_pars_in_col_1 += 1
        else:
            num_of_pars_in_col_2 += 1
        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(8, num_of_paragraphs + 8):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_paragraphs_in_col_1 += 1
        else:
            num_of_paragraphs_in_col_2 += 1

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(28, num_of_enums + 28):
        list_2.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']

    if (len(list_2) != 0):
        max_lines_enum = max(list_2)
        min_lines_enum = min(list_2)
    else:
        max_lines_enum = 0
        min_lines_enum = 0

    for i in range(14, num_of_captionfigures + 14):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    for i in range(20, num_of_captiontables + 20):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    if (len(list_3) != 0):
        max_lines_caption = max(list_3)
        min_lines_caption = min(list_3)
    else:
        max_lines_caption = 0
        min_lines_caption = 0

    for i in range(10, num_of_figures + 10):
        list_4.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_figures_in_col_1 += 1
        else:
            num_of_figures_in_col_2 += 1

    if (len(list_4) != 0):
        max_figure_y_space = max(list_4)
        min_figure_y_space = min(list_4)
        sum_space_taken_by_figures = sum(list_4)
    else:
        max_figure_y_space = 0
        min_figure_y_space = 0
        sum_space_taken_by_figures = 0

    for i in range(18, num_of_tables + 18):
        list_5.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_tables_in_col_1 += 1
        else:
            num_of_tables_in_col_2 += 1

    if (len(list_5) != 0):
        max_table_y_space = max(list_5)
        min_table_y_space = min(list_5)
        sum_space_taken_by_tables = sum(list_5)
    else:
        max_table_y_space = 0
        min_table_y_space = 0
        sum_space_taken_by_tables = 0

    part_of_last_height = 0
    for i in range(0, 39):
        if (df_copy.at['height' + str(i), 'Doc0'] > 0):
            list_6.append(df_copy.at['height' + str(i), 'Doc0'])
            sum_space_taken += df_copy.at['height' + str(i), 'Doc0']
        if (df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] > 0):
            sum_open_space += df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0']

        if (df_copy.at['start_y' + str(i), 'Doc0'] > df_copy.at['end_y' + str(i), 'Doc0'] and df_copy.at[
            'column' + str(
                    i), 'Doc0'] == 1):  # we will want to see if there is an object that starts at the 2nd to last column and spread to the next column
            # we found one that starts at column 1 and ends on the 2nd page
            part_of_last_height += df_copy.at['end_y' + str(i), 'Doc0'] - 50
        if (df_copy.at['page' + str(i), 'Doc0'] == 1):  # on the last page we will take all of the objects height
            part_of_last_height += df_copy.at['height' + str(i), 'Doc0']

    new_ending_y = part_of_last_height

    if (len(list_6) != 0):
        max_height_object = max(list_6)
        min_height_object = min(list_6)
    else:
        max_height_object = 0
        min_height_object = 0

    for i in range(38, num_of_algorithms + 38):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_algorithms_in_col_1 += 1
        else:
            num_of_algorithms_in_col_2 += 1

    for i in range(33, num_of_formulas + 33):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_formulas_in_col_1 += 1
        else:
            num_of_formulas_in_col_2 += 1

    last_element = list(dct_of_elements_in_order)[-1]
    get_index_of_last_element = dict_for_indexes_inverse[last_element]
    last_element_with_no_index = ''.join([i for i in last_element if not i.isdigit()])
    if (last_element_with_no_index == 'Par'):
        last_object_index = 1
    elif (last_element_with_no_index == 'Figure'):
        last_object_index = 2
    elif (last_element_with_no_index == 'CaptionFigure'):
        last_object_index = 3
    elif (last_element_with_no_index == 'Table'):
        last_object_index = 4
    elif (last_element_with_no_index == 'CaptionTable'):
        last_object_index = 5
    elif (last_element_with_no_index == 'Section'):
        last_object_index = 6
    elif (last_element_with_no_index == 'SubSection'):
        last_object_index = 7
    elif (last_element_with_no_index == 'Matrix'):
        last_object_index = 8
    elif (last_element_with_no_index == 'Enum'):
        last_object_index = 9
    elif (last_element_with_no_index == 'Formula'):
        last_object_index = 10
    elif (last_element_with_no_index == 'Algorithm'):
        last_object_index = 11
    else:
        last_object_index = 0

    if (len(list_1) != 0):
        max_lines_par = max(list_1)
        min_lines_par = min(list_1)
    else:
        max_lines_par = 0
        min_lines_par = 0

    if (count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'] != 0):
        avg_num_of_words_from_pars = sum_of_words_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
        avg_num_of_chars_from_pars = sum_of_chars_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
    else:
        avg_num_of_words_from_pars = 0
        avg_num_of_chars_from_pars = 0

    num_of_figures_with_captions = num_of_figures
    num_of_tables_with_captions = num_of_tables

    # putting it all together:
    summative_features['max_lines_par'] = max_lines_par
    summative_features['min_lines_par'] = min_lines_par
    summative_features['max_lines_enum'] = max_lines_enum
    summative_features['min_lines_enum'] = min_lines_enum
    summative_features['max_lines_caption'] = max_lines_caption
    summative_features['min_lines_caption'] = min_lines_caption
    summative_features['max_figure_y_space'] = max_figure_y_space
    summative_features['min_figure_y_space'] = min_figure_y_space
    summative_features['max_table_y_space'] = max_table_y_space
    summative_features['min_table_y_space'] = min_table_y_space
    summative_features['max_height_object'] = max_height_object
    summative_features['min_height_object'] = min_height_object
    summative_features['num_of_elements'] = num_of_elements
    summative_features['num_of_pars'] = num_of_pars
    summative_features['num_of_pars_in_col_1'] = num_of_pars_in_col_1
    summative_features['num_of_pars_in_col_2'] = num_of_pars_in_col_2
    summative_features['num_of_paragraphs'] = num_of_paragraphs
    summative_features['num_of_paragraphs_in_col_1'] = num_of_paragraphs_in_col_1
    summative_features['num_of_paragraphs_in_col_2'] = num_of_paragraphs_in_col_2
    summative_features['num_of_algorithms'] = num_of_algorithms
    summative_features['num_of_algorithms_in_col_1'] = num_of_algorithms_in_col_1
    summative_features['num_of_algorithms_in_col_2'] = num_of_algorithms_in_col_2
    summative_features['num_of_formulas'] = num_of_formulas
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
    summative_features['avg_num_of_words_from_pars'] = avg_num_of_words_from_pars
    summative_features['avg_num_of_chars_from_pars'] = avg_num_of_chars_from_pars
    summative_features['num_of_paragraphs_with_1_word_at_the_end'] = num_of_paragraphs_with_1_word_at_the_end
    summative_features['num_of_figures_with_captions'] = num_of_figures_with_captions
    summative_features['num_of_tables_with_captions'] = num_of_tables_with_captions
    if (new_ending_y < summative_features['ending_y_of_doc']):
        summative_features['ending_y_of_doc'] = new_ending_y

    df_copy.at['max_lines_par', 'Doc0'] = max_lines_par
    df_copy.at['min_lines_par', 'Doc0'] = min_lines_par
    df_copy.at['max_lines_enum', 'Doc0'] = max_lines_enum
    df_copy.at['min_lines_enum', 'Doc0'] = min_lines_enum
    df_copy.at['max_lines_caption', 'Doc0'] = max_lines_caption
    df_copy.at['min_lines_caption', 'Doc0'] = min_lines_caption
    df_copy.at['max_figure_y_space', 'Doc0'] = max_figure_y_space
    df_copy.at['min_figure_y_space', 'Doc0'] = min_figure_y_space
    df_copy.at['max_table_y_space', 'Doc0'] = max_table_y_space
    df_copy.at['min_table_y_space', 'Doc0'] = min_table_y_space
    df_copy.at['max_height_object', 'Doc0'] = max_height_object
    df_copy.at['min_height_object', 'Doc0'] = min_height_object
    df_copy.at['num_of_elements', 'Doc0'] = num_of_elements
    df_copy.at['num_of_pars', 'Doc0'] = num_of_pars
    df_copy.at['num_of_pars_in_col_1', 'Doc0'] = num_of_pars_in_col_1
    df_copy.at['num_of_pars_in_col_2', 'Doc0'] = num_of_pars_in_col_2
    df_copy.at['num_of_paragraphs', 'Doc0'] = num_of_paragraphs
    df_copy.at['num_of_paragraphs_in_col_1', 'Doc0'] = num_of_paragraphs_in_col_1
    df_copy.at['num_of_paragraphs_in_col_2', 'Doc0'] = num_of_paragraphs_in_col_2
    df_copy.at['num_of_algorithms', 'Doc0'] = num_of_algorithms
    df_copy.at['num_of_algorithms_in_col_1', 'Doc0'] = num_of_algorithms_in_col_1
    df_copy.at['num_of_algorithms_in_col_2', 'Doc0'] = num_of_algorithms_in_col_2
    df_copy.at['num_of_formulas', 'Doc0'] = num_of_formulas
    df_copy.at['num_of_formulas_in_col_1', 'Doc0'] = num_of_formulas_in_col_1
    df_copy.at['num_of_formulas_in_col_2', 'Doc0'] = num_of_formulas_in_col_2
    df_copy.at['num_of_figures_in_col_1', 'Doc0'] = num_of_figures_in_col_1
    df_copy.at['num_of_figures_in_col_2', 'Doc0'] = num_of_figures_in_col_2
    df_copy.at['num_of_tables_in_col_1', 'Doc0'] = num_of_tables_in_col_1
    df_copy.at['num_of_tables_in_col_2', 'Doc0'] = num_of_tables_in_col_2
    df_copy.at['last_element', 'Doc0'] = last_object_index
    df_copy.at['sum_space_taken', 'Doc0'] = sum_space_taken
    df_copy.at['sum_open_space', 'Doc0'] = sum_open_space
    df_copy.at['sum_space_taken_by_figures', 'Doc0'] = sum_space_taken_by_figures
    df_copy.at['sum_space_taken_by_tables', 'Doc0'] = sum_space_taken_by_tables
    df_copy.at['sum_of_chars_across_doc', 'Doc0'] = sum_of_chars_across_doc
    df_copy.at['sum_of_words_from_pars', 'Doc0'] = sum_of_words_from_pars
    df_copy.at['sum_of_chars_from_pars', 'Doc0'] = sum_of_chars_from_pars
    df_copy.at['avg_num_of_words_from_pars', 'Doc0'] = avg_num_of_words_from_pars
    df_copy.at['avg_num_of_chars_from_pars', 'Doc0'] = avg_num_of_chars_from_pars
    df_copy.at['num_of_paragraphs_with_1_word_at_the_end', 'Doc0'] = num_of_paragraphs_with_1_word_at_the_end
    df_copy.at['num_of_figures_with_captions', 'Doc0'] = num_of_figures_with_captions
    df_copy.at['num_of_tables_with_captions', 'Doc0'] = num_of_tables_with_captions
    if (new_ending_y < df_copy.at['ending_y_of_doc', 'Doc0']):
        df_copy.at['ending_y_of_doc', 'Doc0'] = new_ending_y


    # df_copy = df_copy.T
    # df_copy.to_csv('pdf_extraction\\adi_comparing\\new_files\\example_test_for_me_1_4_2023_2.csv')
    # sys.exit()

    return dct_of_elements_in_order, count_dict_of_elements, summative_features, df_copy

def simulating_using_table_reduction(value_of_operator,object_used_on,num_of_object,df_copy,summative_features,dct_of_elements_in_order): # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    dict_for_indexes = {0: 'Par', 1: 'Par', 2: 'Par', 3: 'Par', 4: 'Par', 5: 'Par', 6: 'Par', 7: 'Par', 8: 'Paragraph',
                        9: 'Paragraph', 10: 'Figure', 11: 'Figure', 12: 'Figure', 13: 'Figure', 14: 'CaptionFigure',
                        15: 'CaptionFigure', 16: 'CaptionFigure', 17: 'CaptionFigure', 18: 'Table', 19: 'Table',
                        20: 'CaptionTable', 21: 'CaptionTable', 22: 'Section', 23: 'Section', 24: 'Section',
                        25: 'SubSection', 26: 'SubSection', 27: 'SubSection', 28: 'Enum', 29: 'Enum', 30: 'Enum',
                        31: 'Enum', 32: 'Enum', 33: 'Formula', 34: 'Formula', 35: 'Formula', 36: 'Formula',
                        37: 'Formula', 38: 'Algorithm', 39: 'Algorithm'}
    dict_for_indexes_inverse = {'Par1': 0, 'Par2': 1, 'Par3': 2, 'Par4': 3, 'Par5': 4, 'Par6': 5, 'Par7': 6, 'Par8': 7,
                                'Paragraph1': 8,
                                'Paragraph2': 9, 'Figure1': 10, 'Figure2': 11, 'Figure3': 12, 'Figure4': 13,
                                'CaptionFigure1': 14,
                                'CaptionFigure2': 15, 'CaptionFigure3': 16, 'CaptionFigure4': 17, 'Table1': 18,
                                'Table2': 19,
                                'CaptionTable1': 20, 'CaptionTable2': 21, 'Section1': 22, 'Section2': 23,
                                'Section3': 24,
                                'SubSection1': 25, 'SubSection2': 26, 'SubSection3': 27, 'Enum1': 28, 'Enum2': 29,
                                'Enum3': 30,
                                'Enum4': 31, 'Enum5': 32, 'Formula1': 33, 'Formula2': 34, 'Formula3': 35,
                                'Formula4': 36,
                                'Formula5': 37, 'Algorithm1': 38, 'Algorithm2': 39}
    object_used_on_combind_with_num_of_object = object_used_on + str(num_of_object)
    # we can know the hierarchy based on
    start_remembering = False
    objects_after_chosen_object = []
    for key in dct_of_elements_in_order.keys():
        if (object_used_on_combind_with_num_of_object == key):
            print(key)
            print(object_used_on_combind_with_num_of_object)
            objects_after_chosen_object.append(key)  # adding the object on which we performed the operator
            start_remembering = True
            continue
        if (start_remembering):
            objects_after_chosen_object.append(key)
    print(objects_after_chosen_object)
    indexx = 0
    reduce_by_20 = False
    skip_next = False
    # now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)
    for j in objects_after_chosen_object: #first will always be the table that we are manipulating
        object_without_index = ''.join([i for i in j if not i.isdigit()])
        get_index_representing_object_in_csv = dict_for_indexes_inverse[j]
        if(indexx != len(objects_after_chosen_object)-1):
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
        if(indexx == 0):#changing the table
            #we will want to change the height of the table and his ending y
            df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
            df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
            #we will also change his caption
            df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            indexx+=1
            continue
        #now we will change all the next objects after the table and his caption
        if (skip_next):
            skip_next = False
            indexx += 1
            continue
        if (object_without_index == 'Par' or object_without_index == 'Paragraph' or object_without_index == 'Enum'):  # to move a par,paragraph,enum to a before column we will need at least 3 rows of free space, so we will need to check it
            print(j)
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the par,paragraph,enum is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 670 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 660):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 680 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 680
                    if (df_copy.at['end_y' + str(
                            get_index_representing_object_in_csv), 'Doc0'] > 85):  # some of the par,paragraph,enum will still stay on the 2nd column
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                        df_copy.at[
                            'spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (object_without_index == 'Section' or object_without_index == 'SubSection'):
            print(j)
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the section,subsection is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 680 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 670):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 690 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 690
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10

        elif (object_without_index == 'Formula' or object_without_index == 'Algorithm'):
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60 and df_copy.at[
                'start_y' + str(
                        get_index_representing_object_in_csv), 'Doc0'] > 0):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                # i will try to fix a bug here:
                if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0 and df_copy.at[
                    'end_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0):
                    if (reduce_by_20):
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (
                object_without_index == 'Figure' or object_without_index == 'Table'):  # we will need to move them as a chunk
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] + df_copy.at[
                    'height' + str(get_index_representing_after_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                  'start_y' + str(
                                                                                                      get_index_representing_object_in_csv), 'Doc0'] + \
                                                                                              df_copy.at['height' + str(
                                                                                                  get_index_representing_object_in_csv), 'Doc0']
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                          'end_y' + str(
                                                                                                              get_index_representing_object_in_csv), 'Doc0'] + 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            skip_next = True

        indexx += 1

    # update summative features:
    # stuff about pars first:
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
    sum_space_taken = 0
    sum_open_space = 0
    sum_of_chars_across_doc = 0
    sum_of_chars_from_pars = 0
    sum_of_words_from_pars = 0
    num_of_paragraphs_with_1_word_at_the_end = 0

    num_of_pars = count_dict_of_elements['Par']
    num_of_elements = len(dct_of_elements_in_order)
    num_of_paragraphs = count_dict_of_elements['Paragraph']
    num_of_algorithms = count_dict_of_elements['Algorithm']
    num_of_formulas = count_dict_of_elements['Formula']
    num_of_enums = count_dict_of_elements['Enum']
    num_of_captionfigures = count_dict_of_elements['CaptionFigure']
    num_of_captiontables = count_dict_of_elements['CaptionTable']
    num_of_figures = count_dict_of_elements['Figure']
    num_of_tables = count_dict_of_elements['Table']
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []

    for i in range(0, num_of_pars):
        list_1.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_pars_in_col_1 += 1
        else:
            num_of_pars_in_col_2 += 1
        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(8, num_of_paragraphs + 8):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_paragraphs_in_col_1 += 1
        else:
            num_of_paragraphs_in_col_2 += 1

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(28, num_of_enums + 28):
        list_2.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']

    if (len(list_2) != 0):
        max_lines_enum = max(list_2)
        min_lines_enum = min(list_2)
    else:
        max_lines_enum = 0
        min_lines_enum = 0

    for i in range(14, num_of_captionfigures + 14):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    for i in range(20, num_of_captiontables + 20):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    if (len(list_3) != 0):
        max_lines_caption = max(list_3)
        min_lines_caption = min(list_3)
    else:
        max_lines_caption = 0
        min_lines_caption = 0

    for i in range(10, num_of_figures + 10):
        list_4.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_figures_in_col_1 += 1
        else:
            num_of_figures_in_col_2 += 1

    if (len(list_4) != 0):
        max_figure_y_space = max(list_4)
        min_figure_y_space = min(list_4)
        sum_space_taken_by_figures = sum(list_4)
    else:
        max_figure_y_space = 0
        min_figure_y_space = 0
        sum_space_taken_by_figures = 0

    for i in range(18, num_of_tables + 18):
        list_5.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_tables_in_col_1 += 1
        else:
            num_of_tables_in_col_2 += 1

    if (len(list_5) != 0):
        max_table_y_space = max(list_5)
        min_table_y_space = min(list_5)
        sum_space_taken_by_tables = sum(list_5)
    else:
        max_table_y_space = 0
        min_table_y_space = 0
        sum_space_taken_by_tables = 0

    part_of_last_height = 0
    for i in range(0, 39):
        if (df_copy.at['height' + str(i), 'Doc0'] > 0):
            list_6.append(df_copy.at['height' + str(i), 'Doc0'])
            sum_space_taken += df_copy.at['height' + str(i), 'Doc0']
        if (df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] > 0):
            sum_open_space += df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0']

        if (df_copy.at['start_y' + str(i), 'Doc0'] > df_copy.at['end_y' + str(i), 'Doc0'] and df_copy.at[
            'column' + str(
                i), 'Doc0'] == 1):  # we will want to see if there is an object that starts at the 2nd to last column and spread to the next column
            # we found one that starts at column 1 and ends on the 2nd page
            part_of_last_height += df_copy.at['end_y' + str(i), 'Doc0'] - 50
        if (df_copy.at['page' + str(i), 'Doc0'] == 1):  # on the last page we will take all of the objects height
            part_of_last_height += df_copy.at['height' + str(i), 'Doc0']

    new_ending_y = part_of_last_height

    if (len(list_6) != 0):
        max_height_object = max(list_6)
        min_height_object = min(list_6)
    else:
        max_height_object = 0
        min_height_object = 0

    for i in range(38, num_of_algorithms + 38):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_algorithms_in_col_1 += 1
        else:
            num_of_algorithms_in_col_2 += 1

    for i in range(33, num_of_formulas + 33):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_formulas_in_col_1 += 1
        else:
            num_of_formulas_in_col_2 += 1

    last_element = list(dct_of_elements_in_order)[-1]
    get_index_of_last_element = dict_for_indexes_inverse[last_element]
    last_element_with_no_index = ''.join([i for i in last_element if not i.isdigit()])
    if (last_element_with_no_index == 'Par'):
        last_object_index = 1
    elif (last_element_with_no_index == 'Figure'):
        last_object_index = 2
    elif (last_element_with_no_index == 'CaptionFigure'):
        last_object_index = 3
    elif (last_element_with_no_index == 'Table'):
        last_object_index = 4
    elif (last_element_with_no_index == 'CaptionTable'):
        last_object_index = 5
    elif (last_element_with_no_index == 'Section'):
        last_object_index = 6
    elif (last_element_with_no_index == 'SubSection'):
        last_object_index = 7
    elif (last_element_with_no_index == 'Matrix'):
        last_object_index = 8
    elif (last_element_with_no_index == 'Enum'):
        last_object_index = 9
    elif (last_element_with_no_index == 'Formula'):
        last_object_index = 10
    elif (last_element_with_no_index == 'Algorithm'):
        last_object_index = 11
    else:
        last_object_index = 0

    if (len(list_1) != 0):
        max_lines_par = max(list_1)
        min_lines_par = min(list_1)
    else:
        max_lines_par = 0
        min_lines_par = 0

    if (count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'] != 0):
        avg_num_of_words_from_pars = sum_of_words_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
        avg_num_of_chars_from_pars = sum_of_chars_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
    else:
        avg_num_of_words_from_pars = 0
        avg_num_of_chars_from_pars = 0

    num_of_figures_with_captions = num_of_figures
    num_of_tables_with_captions = num_of_tables

    # putting it all together:
    summative_features['max_lines_par'] = max_lines_par
    summative_features['min_lines_par'] = min_lines_par
    summative_features['max_lines_enum'] = max_lines_enum
    summative_features['min_lines_enum'] = min_lines_enum
    summative_features['max_lines_caption'] = max_lines_caption
    summative_features['min_lines_caption'] = min_lines_caption
    summative_features['max_figure_y_space'] = max_figure_y_space
    summative_features['min_figure_y_space'] = min_figure_y_space
    summative_features['max_table_y_space'] = max_table_y_space
    summative_features['min_table_y_space'] = min_table_y_space
    summative_features['max_height_object'] = max_height_object
    summative_features['min_height_object'] = min_height_object
    summative_features['num_of_elements'] = num_of_elements
    summative_features['num_of_pars'] = num_of_pars
    summative_features['num_of_pars_in_col_1'] = num_of_pars_in_col_1
    summative_features['num_of_pars_in_col_2'] = num_of_pars_in_col_2
    summative_features['num_of_paragraphs'] = num_of_paragraphs
    summative_features['num_of_paragraphs_in_col_1'] = num_of_paragraphs_in_col_1
    summative_features['num_of_paragraphs_in_col_2'] = num_of_paragraphs_in_col_2
    summative_features['num_of_algorithms'] = num_of_algorithms
    summative_features['num_of_algorithms_in_col_1'] = num_of_algorithms_in_col_1
    summative_features['num_of_algorithms_in_col_2'] = num_of_algorithms_in_col_2
    summative_features['num_of_formulas'] = num_of_formulas
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
    summative_features['avg_num_of_words_from_pars'] = avg_num_of_words_from_pars
    summative_features['avg_num_of_chars_from_pars'] = avg_num_of_chars_from_pars
    summative_features['num_of_paragraphs_with_1_word_at_the_end'] = num_of_paragraphs_with_1_word_at_the_end
    summative_features['num_of_figures_with_captions'] = num_of_figures_with_captions
    summative_features['num_of_tables_with_captions'] = num_of_tables_with_captions
    if (new_ending_y < summative_features['ending_y_of_doc']):
        summative_features['ending_y_of_doc'] = new_ending_y

    df_copy.at['max_lines_par', 'Doc0'] = max_lines_par
    df_copy.at['min_lines_par', 'Doc0'] = min_lines_par
    df_copy.at['max_lines_enum', 'Doc0'] = max_lines_enum
    df_copy.at['min_lines_enum', 'Doc0'] = min_lines_enum
    df_copy.at['max_lines_caption', 'Doc0'] = max_lines_caption
    df_copy.at['min_lines_caption', 'Doc0'] = min_lines_caption
    df_copy.at['max_figure_y_space', 'Doc0'] = max_figure_y_space
    df_copy.at['min_figure_y_space', 'Doc0'] = min_figure_y_space
    df_copy.at['max_table_y_space', 'Doc0'] = max_table_y_space
    df_copy.at['min_table_y_space', 'Doc0'] = min_table_y_space
    df_copy.at['max_height_object', 'Doc0'] = max_height_object
    df_copy.at['min_height_object', 'Doc0'] = min_height_object
    df_copy.at['num_of_elements', 'Doc0'] = num_of_elements
    df_copy.at['num_of_pars', 'Doc0'] = num_of_pars
    df_copy.at['num_of_pars_in_col_1', 'Doc0'] = num_of_pars_in_col_1
    df_copy.at['num_of_pars_in_col_2', 'Doc0'] = num_of_pars_in_col_2
    df_copy.at['num_of_paragraphs', 'Doc0'] = num_of_paragraphs
    df_copy.at['num_of_paragraphs_in_col_1', 'Doc0'] = num_of_paragraphs_in_col_1
    df_copy.at['num_of_paragraphs_in_col_2', 'Doc0'] = num_of_paragraphs_in_col_2
    df_copy.at['num_of_algorithms', 'Doc0'] = num_of_algorithms
    df_copy.at['num_of_algorithms_in_col_1', 'Doc0'] = num_of_algorithms_in_col_1
    df_copy.at['num_of_algorithms_in_col_2', 'Doc0'] = num_of_algorithms_in_col_2
    df_copy.at['num_of_formulas', 'Doc0'] = num_of_formulas
    df_copy.at['num_of_formulas_in_col_1', 'Doc0'] = num_of_formulas_in_col_1
    df_copy.at['num_of_formulas_in_col_2', 'Doc0'] = num_of_formulas_in_col_2
    df_copy.at['num_of_figures_in_col_1', 'Doc0'] = num_of_figures_in_col_1
    df_copy.at['num_of_figures_in_col_2', 'Doc0'] = num_of_figures_in_col_2
    df_copy.at['num_of_tables_in_col_1', 'Doc0'] = num_of_tables_in_col_1
    df_copy.at['num_of_tables_in_col_2', 'Doc0'] = num_of_tables_in_col_2
    df_copy.at['last_element', 'Doc0'] = last_object_index
    df_copy.at['sum_space_taken', 'Doc0'] = sum_space_taken
    df_copy.at['sum_open_space', 'Doc0'] = sum_open_space
    df_copy.at['sum_space_taken_by_figures', 'Doc0'] = sum_space_taken_by_figures
    df_copy.at['sum_space_taken_by_tables', 'Doc0'] = sum_space_taken_by_tables
    df_copy.at['sum_of_chars_across_doc', 'Doc0'] = sum_of_chars_across_doc
    df_copy.at['sum_of_words_from_pars', 'Doc0'] = sum_of_words_from_pars
    df_copy.at['sum_of_chars_from_pars', 'Doc0'] = sum_of_chars_from_pars
    df_copy.at['avg_num_of_words_from_pars', 'Doc0'] = avg_num_of_words_from_pars
    df_copy.at['avg_num_of_chars_from_pars', 'Doc0'] = avg_num_of_chars_from_pars
    df_copy.at['num_of_paragraphs_with_1_word_at_the_end', 'Doc0'] = num_of_paragraphs_with_1_word_at_the_end
    df_copy.at['num_of_figures_with_captions', 'Doc0'] = num_of_figures_with_captions
    df_copy.at['num_of_tables_with_captions', 'Doc0'] = num_of_tables_with_captions
    if (new_ending_y < df_copy.at['ending_y_of_doc', 'Doc0']):
        df_copy.at['ending_y_of_doc', 'Doc0'] = new_ending_y


    # df_copy = df_copy.T
    # df_copy.to_csv('pdf_extraction\\adi_comparing\\new_files\\example_test_for_me_1_4_2023_2.csv')
    # sys.exit()

    return dct_of_elements_in_order,count_dict_of_elements,summative_features,df_copy

def simulating_using_algorithm_reduction(value_of_operator,object_used_on,num_of_object,df_copy,summative_features,dct_of_elements_in_order): # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    dict_for_indexes = {0: 'Par', 1: 'Par', 2: 'Par', 3: 'Par', 4: 'Par', 5: 'Par', 6: 'Par', 7: 'Par', 8: 'Paragraph',
                        9: 'Paragraph', 10: 'Figure', 11: 'Figure', 12: 'Figure', 13: 'Figure', 14: 'CaptionFigure',
                        15: 'CaptionFigure', 16: 'CaptionFigure', 17: 'CaptionFigure', 18: 'Table', 19: 'Table',
                        20: 'CaptionTable', 21: 'CaptionTable', 22: 'Section', 23: 'Section', 24: 'Section',
                        25: 'SubSection', 26: 'SubSection', 27: 'SubSection', 28: 'Enum', 29: 'Enum', 30: 'Enum',
                        31: 'Enum', 32: 'Enum', 33: 'Formula', 34: 'Formula', 35: 'Formula', 36: 'Formula',
                        37: 'Formula', 38: 'Algorithm', 39: 'Algorithm'}
    dict_for_indexes_inverse = {'Par1': 0, 'Par2': 1, 'Par3': 2, 'Par4': 3, 'Par5': 4, 'Par6': 5, 'Par7': 6, 'Par8': 7,
                                'Paragraph1': 8,
                                'Paragraph2': 9, 'Figure1': 10, 'Figure2': 11, 'Figure3': 12, 'Figure4': 13,
                                'CaptionFigure1': 14,
                                'CaptionFigure2': 15, 'CaptionFigure3': 16, 'CaptionFigure4': 17, 'Table1': 18,
                                'Table2': 19,
                                'CaptionTable1': 20, 'CaptionTable2': 21, 'Section1': 22, 'Section2': 23,
                                'Section3': 24,
                                'SubSection1': 25, 'SubSection2': 26, 'SubSection3': 27, 'Enum1': 28, 'Enum2': 29,
                                'Enum3': 30,
                                'Enum4': 31, 'Enum5': 32, 'Formula1': 33, 'Formula2': 34, 'Formula3': 35,
                                'Formula4': 36,
                                'Formula5': 37, 'Algorithm1': 38, 'Algorithm2': 39}
    object_used_on_combind_with_num_of_object = object_used_on + str(num_of_object)
    # we can know the hierarchy based on
    start_remembering = False
    objects_after_chosen_object = []
    for key in dct_of_elements_in_order.keys():
        if (object_used_on_combind_with_num_of_object == key):
            print(key)
            print(object_used_on_combind_with_num_of_object)
            objects_after_chosen_object.append(key)  # adding the object on which we performed the operator
            start_remembering = True
            continue
        if (start_remembering):
            objects_after_chosen_object.append(key)
    print(objects_after_chosen_object)
    indexx = 0
    reduce_by_20 = False
    skip_next = False
    # now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)
    for j in objects_after_chosen_object: #first will always be the algorithm that we are manipulating
        object_without_index = ''.join([i for i in j if not i.isdigit()])
        get_index_representing_object_in_csv = dict_for_indexes_inverse[j]
        if(indexx != len(objects_after_chosen_object)-1):
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
        if(indexx == 0):#changing the table
            #we will want to change the height of the algorithm and his ending y
            df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
            df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
            indexx+=1
            continue
        #now we will change all the next objects after the table and his caption
        if (skip_next):
            skip_next = False
            indexx += 1
            continue
        if (object_without_index == 'Par' or object_without_index == 'Paragraph' or object_without_index == 'Enum'):  # to move a par,paragraph,enum to a before column we will need at least 3 rows of free space, so we will need to check it
            print(j)
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the par,paragraph,enum is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 670 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 660):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 680 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 680
                    if (df_copy.at['end_y' + str(
                            get_index_representing_object_in_csv), 'Doc0'] > 85):  # some of the par,paragraph,enum will still stay on the 2nd column
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                        df_copy.at[
                            'spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (object_without_index == 'Section' or object_without_index == 'SubSection'):
            print(j)
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the section,subsection is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 680 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 670):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 690 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 690
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10

        elif (object_without_index == 'Formula' or object_without_index == 'Algorithm'):
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60 and df_copy.at[
                'start_y' + str(
                        get_index_representing_object_in_csv), 'Doc0'] > 0):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                # i will try to fix a bug here:
                if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0 and df_copy.at[
                    'end_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0):
                    if (reduce_by_20):
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (
                object_without_index == 'Figure' or object_without_index == 'Table'):  # we will need to move them as a chunk
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] + df_copy.at[
                    'height' + str(get_index_representing_after_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                  'start_y' + str(
                                                                                                      get_index_representing_object_in_csv), 'Doc0'] + \
                                                                                              df_copy.at['height' + str(
                                                                                                  get_index_representing_object_in_csv), 'Doc0']
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                          'end_y' + str(
                                                                                                              get_index_representing_object_in_csv), 'Doc0'] + 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            skip_next = True

        indexx += 1

    # update summative features:
    # stuff about pars first:
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
    sum_space_taken = 0
    sum_open_space = 0
    sum_of_chars_across_doc = 0
    sum_of_chars_from_pars = 0
    sum_of_words_from_pars = 0
    num_of_paragraphs_with_1_word_at_the_end = 0

    num_of_pars = count_dict_of_elements['Par']
    num_of_elements = len(dct_of_elements_in_order)
    num_of_paragraphs = count_dict_of_elements['Paragraph']
    num_of_algorithms = count_dict_of_elements['Algorithm']
    num_of_formulas = count_dict_of_elements['Formula']
    num_of_enums = count_dict_of_elements['Enum']
    num_of_captionfigures = count_dict_of_elements['CaptionFigure']
    num_of_captiontables = count_dict_of_elements['CaptionTable']
    num_of_figures = count_dict_of_elements['Figure']
    num_of_tables = count_dict_of_elements['Table']
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []

    for i in range(0, num_of_pars):
        list_1.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_pars_in_col_1 += 1
        else:
            num_of_pars_in_col_2 += 1
        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(8, num_of_paragraphs + 8):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_paragraphs_in_col_1 += 1
        else:
            num_of_paragraphs_in_col_2 += 1

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(28, num_of_enums + 28):
        list_2.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']

    if (len(list_2) != 0):
        max_lines_enum = max(list_2)
        min_lines_enum = min(list_2)
    else:
        max_lines_enum = 0
        min_lines_enum = 0

    for i in range(14, num_of_captionfigures + 14):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    for i in range(20, num_of_captiontables + 20):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    if (len(list_3) != 0):
        max_lines_caption = max(list_3)
        min_lines_caption = min(list_3)
    else:
        max_lines_caption = 0
        min_lines_caption = 0

    for i in range(10, num_of_figures + 10):
        list_4.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_figures_in_col_1 += 1
        else:
            num_of_figures_in_col_2 += 1

    if (len(list_4) != 0):
        max_figure_y_space = max(list_4)
        min_figure_y_space = min(list_4)
        sum_space_taken_by_figures = sum(list_4)
    else:
        max_figure_y_space = 0
        min_figure_y_space = 0
        sum_space_taken_by_figures = 0

    for i in range(18, num_of_tables + 18):
        list_5.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_tables_in_col_1 += 1
        else:
            num_of_tables_in_col_2 += 1

    if (len(list_5) != 0):
        max_table_y_space = max(list_5)
        min_table_y_space = min(list_5)
        sum_space_taken_by_tables = sum(list_5)
    else:
        max_table_y_space = 0
        min_table_y_space = 0
        sum_space_taken_by_tables = 0

    part_of_last_height = 0
    for i in range(0, 39):
        if (df_copy.at['height' + str(i), 'Doc0'] > 0):
            list_6.append(df_copy.at['height' + str(i), 'Doc0'])
            sum_space_taken += df_copy.at['height' + str(i), 'Doc0']
        if (df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] > 0):
            sum_open_space += df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0']

        if (df_copy.at['start_y' + str(i), 'Doc0'] > df_copy.at['end_y' + str(i), 'Doc0'] and df_copy.at[
            'column' + str(
                i), 'Doc0'] == 1):  # we will want to see if there is an object that starts at the 2nd to last column and spread to the next column
            # we found one that starts at column 1 and ends on the 2nd page
            part_of_last_height += df_copy.at['end_y' + str(i), 'Doc0'] - 50
        if (df_copy.at['page' + str(i), 'Doc0'] == 1):  # on the last page we will take all of the objects height
            part_of_last_height += df_copy.at['height' + str(i), 'Doc0']

    new_ending_y = part_of_last_height

    if (len(list_6) != 0):
        max_height_object = max(list_6)
        min_height_object = min(list_6)
    else:
        max_height_object = 0
        min_height_object = 0

    for i in range(38, num_of_algorithms + 38):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_algorithms_in_col_1 += 1
        else:
            num_of_algorithms_in_col_2 += 1

    for i in range(33, num_of_formulas + 33):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_formulas_in_col_1 += 1
        else:
            num_of_formulas_in_col_2 += 1

    last_element = list(dct_of_elements_in_order)[-1]
    get_index_of_last_element = dict_for_indexes_inverse[last_element]
    last_element_with_no_index = ''.join([i for i in last_element if not i.isdigit()])
    if (last_element_with_no_index == 'Par'):
        last_object_index = 1
    elif (last_element_with_no_index == 'Figure'):
        last_object_index = 2
    elif (last_element_with_no_index == 'CaptionFigure'):
        last_object_index = 3
    elif (last_element_with_no_index == 'Table'):
        last_object_index = 4
    elif (last_element_with_no_index == 'CaptionTable'):
        last_object_index = 5
    elif (last_element_with_no_index == 'Section'):
        last_object_index = 6
    elif (last_element_with_no_index == 'SubSection'):
        last_object_index = 7
    elif (last_element_with_no_index == 'Matrix'):
        last_object_index = 8
    elif (last_element_with_no_index == 'Enum'):
        last_object_index = 9
    elif (last_element_with_no_index == 'Formula'):
        last_object_index = 10
    elif (last_element_with_no_index == 'Algorithm'):
        last_object_index = 11
    else:
        last_object_index = 0

    if (len(list_1) != 0):
        max_lines_par = max(list_1)
        min_lines_par = min(list_1)
    else:
        max_lines_par = 0
        min_lines_par = 0

    if (count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'] != 0):
        avg_num_of_words_from_pars = sum_of_words_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
        avg_num_of_chars_from_pars = sum_of_chars_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
    else:
        avg_num_of_words_from_pars = 0
        avg_num_of_chars_from_pars = 0

    num_of_figures_with_captions = num_of_figures
    num_of_tables_with_captions = num_of_tables

    # putting it all together:
    summative_features['max_lines_par'] = max_lines_par
    summative_features['min_lines_par'] = min_lines_par
    summative_features['max_lines_enum'] = max_lines_enum
    summative_features['min_lines_enum'] = min_lines_enum
    summative_features['max_lines_caption'] = max_lines_caption
    summative_features['min_lines_caption'] = min_lines_caption
    summative_features['max_figure_y_space'] = max_figure_y_space
    summative_features['min_figure_y_space'] = min_figure_y_space
    summative_features['max_table_y_space'] = max_table_y_space
    summative_features['min_table_y_space'] = min_table_y_space
    summative_features['max_height_object'] = max_height_object
    summative_features['min_height_object'] = min_height_object
    summative_features['num_of_elements'] = num_of_elements
    summative_features['num_of_pars'] = num_of_pars
    summative_features['num_of_pars_in_col_1'] = num_of_pars_in_col_1
    summative_features['num_of_pars_in_col_2'] = num_of_pars_in_col_2
    summative_features['num_of_paragraphs'] = num_of_paragraphs
    summative_features['num_of_paragraphs_in_col_1'] = num_of_paragraphs_in_col_1
    summative_features['num_of_paragraphs_in_col_2'] = num_of_paragraphs_in_col_2
    summative_features['num_of_algorithms'] = num_of_algorithms
    summative_features['num_of_algorithms_in_col_1'] = num_of_algorithms_in_col_1
    summative_features['num_of_algorithms_in_col_2'] = num_of_algorithms_in_col_2
    summative_features['num_of_formulas'] = num_of_formulas
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
    summative_features['avg_num_of_words_from_pars'] = avg_num_of_words_from_pars
    summative_features['avg_num_of_chars_from_pars'] = avg_num_of_chars_from_pars
    summative_features['num_of_paragraphs_with_1_word_at_the_end'] = num_of_paragraphs_with_1_word_at_the_end
    summative_features['num_of_figures_with_captions'] = num_of_figures_with_captions
    summative_features['num_of_tables_with_captions'] = num_of_tables_with_captions
    if (new_ending_y < summative_features['ending_y_of_doc']):
        summative_features['ending_y_of_doc'] = new_ending_y

    df_copy.at['max_lines_par', 'Doc0'] = max_lines_par
    df_copy.at['min_lines_par', 'Doc0'] = min_lines_par
    df_copy.at['max_lines_enum', 'Doc0'] = max_lines_enum
    df_copy.at['min_lines_enum', 'Doc0'] = min_lines_enum
    df_copy.at['max_lines_caption', 'Doc0'] = max_lines_caption
    df_copy.at['min_lines_caption', 'Doc0'] = min_lines_caption
    df_copy.at['max_figure_y_space', 'Doc0'] = max_figure_y_space
    df_copy.at['min_figure_y_space', 'Doc0'] = min_figure_y_space
    df_copy.at['max_table_y_space', 'Doc0'] = max_table_y_space
    df_copy.at['min_table_y_space', 'Doc0'] = min_table_y_space
    df_copy.at['max_height_object', 'Doc0'] = max_height_object
    df_copy.at['min_height_object', 'Doc0'] = min_height_object
    df_copy.at['num_of_elements', 'Doc0'] = num_of_elements
    df_copy.at['num_of_pars', 'Doc0'] = num_of_pars
    df_copy.at['num_of_pars_in_col_1', 'Doc0'] = num_of_pars_in_col_1
    df_copy.at['num_of_pars_in_col_2', 'Doc0'] = num_of_pars_in_col_2
    df_copy.at['num_of_paragraphs', 'Doc0'] = num_of_paragraphs
    df_copy.at['num_of_paragraphs_in_col_1', 'Doc0'] = num_of_paragraphs_in_col_1
    df_copy.at['num_of_paragraphs_in_col_2', 'Doc0'] = num_of_paragraphs_in_col_2
    df_copy.at['num_of_algorithms', 'Doc0'] = num_of_algorithms
    df_copy.at['num_of_algorithms_in_col_1', 'Doc0'] = num_of_algorithms_in_col_1
    df_copy.at['num_of_algorithms_in_col_2', 'Doc0'] = num_of_algorithms_in_col_2
    df_copy.at['num_of_formulas', 'Doc0'] = num_of_formulas
    df_copy.at['num_of_formulas_in_col_1', 'Doc0'] = num_of_formulas_in_col_1
    df_copy.at['num_of_formulas_in_col_2', 'Doc0'] = num_of_formulas_in_col_2
    df_copy.at['num_of_figures_in_col_1', 'Doc0'] = num_of_figures_in_col_1
    df_copy.at['num_of_figures_in_col_2', 'Doc0'] = num_of_figures_in_col_2
    df_copy.at['num_of_tables_in_col_1', 'Doc0'] = num_of_tables_in_col_1
    df_copy.at['num_of_tables_in_col_2', 'Doc0'] = num_of_tables_in_col_2
    df_copy.at['last_element', 'Doc0'] = last_object_index
    df_copy.at['sum_space_taken', 'Doc0'] = sum_space_taken
    df_copy.at['sum_open_space', 'Doc0'] = sum_open_space
    df_copy.at['sum_space_taken_by_figures', 'Doc0'] = sum_space_taken_by_figures
    df_copy.at['sum_space_taken_by_tables', 'Doc0'] = sum_space_taken_by_tables
    df_copy.at['sum_of_chars_across_doc', 'Doc0'] = sum_of_chars_across_doc
    df_copy.at['sum_of_words_from_pars', 'Doc0'] = sum_of_words_from_pars
    df_copy.at['sum_of_chars_from_pars', 'Doc0'] = sum_of_chars_from_pars
    df_copy.at['avg_num_of_words_from_pars', 'Doc0'] = avg_num_of_words_from_pars
    df_copy.at['avg_num_of_chars_from_pars', 'Doc0'] = avg_num_of_chars_from_pars
    df_copy.at['num_of_paragraphs_with_1_word_at_the_end', 'Doc0'] = num_of_paragraphs_with_1_word_at_the_end
    df_copy.at['num_of_figures_with_captions', 'Doc0'] = num_of_figures_with_captions
    df_copy.at['num_of_tables_with_captions', 'Doc0'] = num_of_tables_with_captions
    if (new_ending_y < df_copy.at['ending_y_of_doc', 'Doc0']):
        df_copy.at['ending_y_of_doc', 'Doc0'] = new_ending_y


    # df_copy = df_copy.T
    # df_copy.to_csv('pdf_extraction\\adi_comparing\\new_files\\example_test_for_me_1_4_2023_2.csv')
    # sys.exit()

    return dct_of_elements_in_order, count_dict_of_elements, summative_features, df_copy

def simulating_using_enum_operator(value_of_operator,object_used_on,num_of_object,df_copy,summative_features,dct_of_elements_in_order,count_dict_of_elements): # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    dict_for_indexes = {0: 'Par', 1: 'Par', 2: 'Par', 3: 'Par', 4: 'Par', 5: 'Par', 6: 'Par', 7: 'Par', 8: 'Paragraph',
                        9: 'Paragraph', 10: 'Figure', 11: 'Figure', 12: 'Figure', 13: 'Figure', 14: 'CaptionFigure',
                        15: 'CaptionFigure', 16: 'CaptionFigure', 17: 'CaptionFigure', 18: 'Table', 19: 'Table',
                        20: 'CaptionTable', 21: 'CaptionTable', 22: 'Section', 23: 'Section', 24: 'Section',
                        25: 'SubSection', 26: 'SubSection', 27: 'SubSection', 28: 'Enum', 29: 'Enum', 30: 'Enum',
                        31: 'Enum', 32: 'Enum', 33: 'Formula', 34: 'Formula', 35: 'Formula', 36: 'Formula',
                        37: 'Formula', 38: 'Algorithm', 39: 'Algorithm'}
    dict_for_indexes_inverse = {'Par1': 0, 'Par2': 1, 'Par3': 2, 'Par4': 3, 'Par5': 4, 'Par6': 5, 'Par7': 6, 'Par8': 7,
                                'Paragraph1': 8,
                                'Paragraph2': 9, 'Figure1': 10, 'Figure2': 11, 'Figure3': 12, 'Figure4': 13,
                                'CaptionFigure1': 14,
                                'CaptionFigure2': 15, 'CaptionFigure3': 16, 'CaptionFigure4': 17, 'Table1': 18,
                                'Table2': 19,
                                'CaptionTable1': 20, 'CaptionTable2': 21, 'Section1': 22, 'Section2': 23,
                                'Section3': 24,
                                'SubSection1': 25, 'SubSection2': 26, 'SubSection3': 27, 'Enum1': 28, 'Enum2': 29,
                                'Enum3': 30,
                                'Enum4': 31, 'Enum5': 32, 'Formula1': 33, 'Formula2': 34, 'Formula3': 35,
                                'Formula4': 36,
                                'Formula5': 37, 'Algorithm1': 38, 'Algorithm2': 39}
    object_used_on_combind_with_num_of_object = object_used_on + str(num_of_object)
    # we can know the hierarchy based on
    start_remembering = False
    objects_after_chosen_object = []
    enum_counter = 0
    for key in dct_of_elements_in_order.keys():
        if (object_used_on_combind_with_num_of_object == key):
            print(key)
            print(object_used_on_combind_with_num_of_object)
            objects_after_chosen_object.append(key)  # adding the object on which we performed the operator
            enum_counter+=1
            start_remembering = True
            continue
        if (start_remembering):
            if(key.startswith('Enum')):
                enum_counter+=1
            objects_after_chosen_object.append(key)
    print(objects_after_chosen_object)
    indexx = 0
    reduce_by_20 = False
    skip_next = False
    booleanexp = True
    new_dct_of_elements_in_order = {}
    # print(dct_of_elements_in_order)
    # for i in dct_of_elements_in_order:
    #     print(f'{i}' ':' f'{dct_of_elements_in_order[i]}')
    # now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)

    object_without_index = ''.join([i for i in objects_after_chosen_object[0] if not i.isdigit()])
    get_index_representing_object_in_csv = dict_for_indexes_inverse[objects_after_chosen_object[0]]
    enum_list = []
    for i in range(1,enum_counter):
        after_object_key = objects_after_chosen_object[indexx + i]  # captions
        get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
        enum_list.append(get_index_representing_after_object_in_csv)
    if(count_dict_of_elements['Par'] == 8):
        return
    else:
        index_of_new_par = count_dict_of_elements['Par']+1
        string_of_new_par = 'Par' + str(index_of_new_par)
        #new_par_key = objects_after_chosen_object[string_of_new_par]  # captions
        get_index_representing_new_par_key_in_csv = dict_for_indexes_inverse[string_of_new_par]
        df_copy.at['page' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['column' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['start_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['end_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['end_y' + str(enum_list[-1]), 'Doc0']-10
        spread_on_more_than_1 = False
        for i in enum_list:
            if(df_copy.at['page' + str(i), 'Doc0'] != df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] or df_copy.at['column' + str(i), 'Doc0'] != df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0']): #one of the enums is in a different page or column, then it is spreading on more than 1 column
                spread_on_more_than_1 = True
                break
        if(spread_on_more_than_1):
            df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = 1
        else:
            df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = 0
        combined_height = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
        combined_number_of_lines = df_copy.at['number_of_lines' + str(get_index_representing_object_in_csv), 'Doc0']
        combined_num_of_chars = df_copy.at['num_of_chars' + str(get_index_representing_object_in_csv), 'Doc0']
        combined_num_of_words = df_copy.at['num_of_words' + str(get_index_representing_object_in_csv), 'Doc0']
        for i in enum_list:
            combined_height += df_copy.at['height' + str(i), 'Doc0']
            combined_number_of_lines += df_copy.at['number_of_lines' + str(i), 'Doc0']
            combined_num_of_chars += df_copy.at['num_of_chars' + str(i), 'Doc0']
            combined_num_of_words += df_copy.at['num_of_words' + str(i), 'Doc0']

        df_copy.at['height' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = combined_height-10
        df_copy.at['number_of_lines' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = combined_number_of_lines
        df_copy.at['num_of_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = combined_num_of_chars
        df_copy.at['num_of_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = combined_num_of_words
        df_copy.at['last_line_length_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['last_line_length_chars' + str(enum_list[-1]), 'Doc0']
        df_copy.at['last_line_length_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['last_line_length_words' + str(enum_list[-1]), 'Doc0']
        df_copy.at['single_word_in_last_line' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['single_word_in_last_line' + str(enum_list[-1]), 'Doc0']
        df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] =df_copy.at['space_between_this_object_and_the_next_object' + str(enum_list[-1]), 'Doc0']

        #end of creation of new Par
        #delete the enums:
        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['number_of_lines' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['num_of_chars' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['num_of_words' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['last_line_length_chars' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['last_line_length_words' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['single_word_in_last_line' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        for i in enum_list:
            df_copy.at['page' + str(i), 'Doc0'] = 0
            df_copy.at['column' + str(i), 'Doc0'] = 0
            df_copy.at['start_y' + str(i), 'Doc0'] = 0
            df_copy.at['end_y' + str(i), 'Doc0'] = 0
            df_copy.at['spread_on_more_than_1_column' + str(i), 'Doc0'] = 0
            df_copy.at['height' + str(i), 'Doc0'] = 0
            df_copy.at['number_of_lines' + str(i), 'Doc0'] = 0
            df_copy.at['num_of_chars' + str(i), 'Doc0'] = 0
            df_copy.at['num_of_words' + str(i), 'Doc0'] = 0
            df_copy.at['last_line_length_chars' + str(i), 'Doc0'] = 0
            df_copy.at['last_line_length_words' + str(i), 'Doc0'] = 0
            df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] = 0
            df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] = 0
            df_copy.at['space_between_this_object_and_the_next_object' + str(i), 'Doc0'] = 0

        count_dict_of_elements['Par'] +=1
        count_dict_of_elements['Enum'] = 0
        Par_counter = 0
        for key in dct_of_elements_in_order.keys():
            if(key.startswith('Enum1')):
                Par_counter += 1
                new_key_to_remember = 'Par' + str(Par_counter)
                new_dct_of_elements_in_order['Par' + str(Par_counter)] = {'page':df_copy.at['page' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'column': df_copy.at['column' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'start_y': df_copy.at['start_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'end_y': df_copy.at['end_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'spread_on_more_than_1_column': df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'height': df_copy.at['height' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'number_of_lines': df_copy.at['number_of_lines' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'num_of_chars': df_copy.at['num_of_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'num_of_words': df_copy.at['num_of_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'last_line_length_chars': df_copy.at['last_line_length_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'single_word_in_last_line': df_copy.at['single_word_in_last_line' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'space_between_this_object_and_last_object': df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'space_between_this_object_and_the_next_object': df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0']}
                continue
            elif(key.startswith('Enum')):
                continue
            else:
                new_key_for_par = ''.join(i for i in key if not i.isdigit())
                if(new_key_for_par == 'Par'):
                    Par_counter += 1
                    new_dct_of_elements_in_order['Par' + str(Par_counter)] = dct_of_elements_in_order[key]
                else:
                    new_dct_of_elements_in_order[key] = dct_of_elements_in_order[key]

        print(dct_of_elements_in_order)
        for i in dct_of_elements_in_order:
            print(f'{i}' ':' f'{dct_of_elements_in_order[i]}')

        print(new_dct_of_elements_in_order)
        for i in new_dct_of_elements_in_order:
            print(f'{i}' ':' f'{new_dct_of_elements_in_order[i]}')


        #neeed to know from where we need to reduce the page: (it will be from this: new_key_to_remember)
        objects_after_chosen_object = []
        start_remembering = False
        for key in new_dct_of_elements_in_order.keys():
            if (new_key_to_remember == key):
                start_remembering = True
                continue
            if (start_remembering):
                objects_after_chosen_object.append(key)

        print(objects_after_chosen_object)
        #now we will need to update the csv to represent the right pars:
        for key in new_dct_of_elements_in_order.keys():
            new_key_for_par = ''.join(i for i in key if not i.isdigit())
            if(new_key_for_par == 'Par'):
                #get his represented number in the csv
                df_copy.at['page' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['page']
                df_copy.at['column' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['column']
                df_copy.at['start_y' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['start_y']
                df_copy.at['end_y' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['end_y']
                df_copy.at['spread_on_more_than_1_column' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['spread_on_more_than_1_column']
                df_copy.at['height' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['height']
                df_copy.at['number_of_lines' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['number_of_lines']
                df_copy.at['num_of_chars' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['num_of_chars']
                df_copy.at['num_of_words' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['num_of_words']
                df_copy.at['last_line_length_chars' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['last_line_length_chars']
                df_copy.at['single_word_in_last_line' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['single_word_in_last_line']
                df_copy.at['space_between_this_object_and_last_object' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['space_between_this_object_and_last_object']
                df_copy.at['space_between_this_object_and_the_next_object' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['space_between_this_object_and_the_next_object']

    indexx = 0
    reduce_by_20 = False
    skip_next = False
    # now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)
    for j in objects_after_chosen_object:
        object_without_index = ''.join([i for i in j if not i.isdigit()])
        get_index_representing_object_in_csv = dict_for_indexes_inverse[j]
        if (indexx != len(objects_after_chosen_object) - 1):
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
        #now we will change all the next objects after the object (enum3)
        if (skip_next):
            skip_next = False
            indexx += 1
            continue
        if (object_without_index == 'Par' or object_without_index == 'Paragraph' or object_without_index == 'Enum'):  # to move a par,paragraph,enum to a before column we will need at least 3 rows of free space, so we will need to check it
            print(j)
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the par,paragraph,enum is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 670 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 660):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 680 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 680
                    if (df_copy.at['end_y' + str(
                            get_index_representing_object_in_csv), 'Doc0'] > 85):  # some of the par,paragraph,enum will still stay on the 2nd column
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                        df_copy.at[
                            'spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (object_without_index == 'Section' or object_without_index == 'SubSection'):
            print(j)
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the section,subsection is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 680 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 670):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 690 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 690
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10

        elif (object_without_index == 'Formula' or object_without_index == 'Algorithm'):
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60 and df_copy.at[
                'start_y' + str(
                        get_index_representing_object_in_csv), 'Doc0'] > 0):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                # i will try to fix a bug here:
                if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0 and df_copy.at[
                    'end_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0):
                    if (reduce_by_20):
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (
                object_without_index == 'Figure' or object_without_index == 'Table'):  # we will need to move them as a chunk
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] + df_copy.at[
                    'height' + str(get_index_representing_after_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                  'start_y' + str(
                                                                                                      get_index_representing_object_in_csv), 'Doc0'] + \
                                                                                              df_copy.at['height' + str(
                                                                                                  get_index_representing_object_in_csv), 'Doc0']
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                          'end_y' + str(
                                                                                                              get_index_representing_object_in_csv), 'Doc0'] + 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            skip_next = True

        indexx += 1

    # update summative features:
    # stuff about pars first:
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
    sum_space_taken = 0
    sum_open_space = 0
    sum_of_chars_across_doc = 0
    sum_of_chars_from_pars = 0
    sum_of_words_from_pars = 0
    num_of_paragraphs_with_1_word_at_the_end = 0

    num_of_pars = count_dict_of_elements['Par']
    num_of_elements = len(new_dct_of_elements_in_order)
    num_of_paragraphs = count_dict_of_elements['Paragraph']
    num_of_algorithms = count_dict_of_elements['Algorithm']
    num_of_formulas = count_dict_of_elements['Formula']
    num_of_enums = count_dict_of_elements['Enum']
    num_of_captionfigures = count_dict_of_elements['CaptionFigure']
    num_of_captiontables = count_dict_of_elements['CaptionTable']
    num_of_figures = count_dict_of_elements['Figure']
    num_of_tables = count_dict_of_elements['Table']
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []

    for i in range(0, num_of_pars):
        list_1.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_pars_in_col_1 += 1
        else:
            num_of_pars_in_col_2 += 1
        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(8, num_of_paragraphs + 8):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_paragraphs_in_col_1 += 1
        else:
            num_of_paragraphs_in_col_2 += 1

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(28, num_of_enums + 28):
        list_2.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']

    if (len(list_2) != 0):
        max_lines_enum = max(list_2)
        min_lines_enum = min(list_2)
    else:
        max_lines_enum = 0
        min_lines_enum = 0

    for i in range(14, num_of_captionfigures + 14):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    for i in range(20, num_of_captiontables + 20):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    if (len(list_3) != 0):
        max_lines_caption = max(list_3)
        min_lines_caption = min(list_3)
    else:
        max_lines_caption = 0
        min_lines_caption = 0

    for i in range(10, num_of_figures + 10):
        list_4.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_figures_in_col_1 += 1
        else:
            num_of_figures_in_col_2 += 1

    if (len(list_4) != 0):
        max_figure_y_space = max(list_4)
        min_figure_y_space = min(list_4)
        sum_space_taken_by_figures = sum(list_4)
    else:
        max_figure_y_space = 0
        min_figure_y_space = 0
        sum_space_taken_by_figures = 0

    for i in range(18, num_of_tables + 18):
        list_5.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_tables_in_col_1 += 1
        else:
            num_of_tables_in_col_2 += 1

    if (len(list_5) != 0):
        max_table_y_space = max(list_5)
        min_table_y_space = min(list_5)
        sum_space_taken_by_tables = sum(list_5)
    else:
        max_table_y_space = 0
        min_table_y_space = 0
        sum_space_taken_by_tables = 0

    part_of_last_height = 0
    for i in range(0, 39):
        if (df_copy.at['height' + str(i), 'Doc0'] > 0):
            list_6.append(df_copy.at['height' + str(i), 'Doc0'])
            sum_space_taken += df_copy.at['height' + str(i), 'Doc0']
        if (df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] > 0):
            sum_open_space += df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0']

        if (df_copy.at['start_y' + str(i), 'Doc0'] > df_copy.at['end_y' + str(i), 'Doc0'] and df_copy.at[
            'column' + str(
                i), 'Doc0'] == 1):  # we will want to see if there is an object that starts at the 2nd to last column and spread to the next column
            # we found one that starts at column 1 and ends on the 2nd page
            part_of_last_height += df_copy.at['end_y' + str(i), 'Doc0'] - 50
        if (df_copy.at['page' + str(i), 'Doc0'] == 1):  # on the last page we will take all of the objects height
            part_of_last_height += df_copy.at['height' + str(i), 'Doc0']

    new_ending_y = part_of_last_height

    if (len(list_6) != 0):
        max_height_object = max(list_6)
        min_height_object = min(list_6)
    else:
        max_height_object = 0
        min_height_object = 0

    for i in range(38, num_of_algorithms + 38):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_algorithms_in_col_1 += 1
        else:
            num_of_algorithms_in_col_2 += 1

    for i in range(33, num_of_formulas + 33):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_formulas_in_col_1 += 1
        else:
            num_of_formulas_in_col_2 += 1

    last_element = list(new_dct_of_elements_in_order)[-1]
    get_index_of_last_element = dict_for_indexes_inverse[last_element]
    last_element_with_no_index = ''.join([i for i in last_element if not i.isdigit()])
    if (last_element_with_no_index == 'Par'):
        last_object_index = 1
    elif (last_element_with_no_index == 'Figure'):
        last_object_index = 2
    elif (last_element_with_no_index == 'CaptionFigure'):
        last_object_index = 3
    elif (last_element_with_no_index == 'Table'):
        last_object_index = 4
    elif (last_element_with_no_index == 'CaptionTable'):
        last_object_index = 5
    elif (last_element_with_no_index == 'Section'):
        last_object_index = 6
    elif (last_element_with_no_index == 'SubSection'):
        last_object_index = 7
    elif (last_element_with_no_index == 'Matrix'):
        last_object_index = 8
    elif (last_element_with_no_index == 'Enum'):
        last_object_index = 9
    elif (last_element_with_no_index == 'Formula'):
        last_object_index = 10
    elif (last_element_with_no_index == 'Algorithm'):
        last_object_index = 11
    else:
        last_object_index = 0

    if (len(list_1) != 0):
        max_lines_par = max(list_1)
        min_lines_par = min(list_1)
    else:
        max_lines_par = 0
        min_lines_par = 0

    if (count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'] != 0):
        avg_num_of_words_from_pars = sum_of_words_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
        avg_num_of_chars_from_pars = sum_of_chars_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
    else:
        avg_num_of_words_from_pars = 0
        avg_num_of_chars_from_pars = 0

    num_of_figures_with_captions = num_of_figures
    num_of_tables_with_captions = num_of_tables

    # putting it all together:
    summative_features['max_lines_par'] = max_lines_par
    summative_features['min_lines_par'] = min_lines_par
    summative_features['max_lines_enum'] = max_lines_enum
    summative_features['min_lines_enum'] = min_lines_enum
    summative_features['max_lines_caption'] = max_lines_caption
    summative_features['min_lines_caption'] = min_lines_caption
    summative_features['max_figure_y_space'] = max_figure_y_space
    summative_features['min_figure_y_space'] = min_figure_y_space
    summative_features['max_table_y_space'] = max_table_y_space
    summative_features['min_table_y_space'] = min_table_y_space
    summative_features['max_height_object'] = max_height_object
    summative_features['min_height_object'] = min_height_object
    summative_features['num_of_elements'] = num_of_elements
    summative_features['num_of_pars'] = num_of_pars
    summative_features['num_of_pars_in_col_1'] = num_of_pars_in_col_1
    summative_features['num_of_pars_in_col_2'] = num_of_pars_in_col_2
    summative_features['num_of_paragraphs'] = num_of_paragraphs
    summative_features['num_of_paragraphs_in_col_1'] = num_of_paragraphs_in_col_1
    summative_features['num_of_paragraphs_in_col_2'] = num_of_paragraphs_in_col_2
    summative_features['num_of_algorithms'] = num_of_algorithms
    summative_features['num_of_algorithms_in_col_1'] = num_of_algorithms_in_col_1
    summative_features['num_of_algorithms_in_col_2'] = num_of_algorithms_in_col_2
    summative_features['num_of_formulas'] = num_of_formulas
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
    summative_features['avg_num_of_words_from_pars'] = avg_num_of_words_from_pars
    summative_features['avg_num_of_chars_from_pars'] = avg_num_of_chars_from_pars
    summative_features['num_of_paragraphs_with_1_word_at_the_end'] = num_of_paragraphs_with_1_word_at_the_end
    summative_features['num_of_figures_with_captions'] = num_of_figures_with_captions
    summative_features['num_of_tables_with_captions'] = num_of_tables_with_captions
    if (new_ending_y < summative_features['ending_y_of_doc']):
        summative_features['ending_y_of_doc'] = new_ending_y

    df_copy.at['max_lines_par', 'Doc0'] = max_lines_par
    df_copy.at['min_lines_par', 'Doc0'] = min_lines_par
    df_copy.at['max_lines_enum', 'Doc0'] = max_lines_enum
    df_copy.at['min_lines_enum', 'Doc0'] = min_lines_enum
    df_copy.at['max_lines_caption', 'Doc0'] = max_lines_caption
    df_copy.at['min_lines_caption', 'Doc0'] = min_lines_caption
    df_copy.at['max_figure_y_space', 'Doc0'] = max_figure_y_space
    df_copy.at['min_figure_y_space', 'Doc0'] = min_figure_y_space
    df_copy.at['max_table_y_space', 'Doc0'] = max_table_y_space
    df_copy.at['min_table_y_space', 'Doc0'] = min_table_y_space
    df_copy.at['max_height_object', 'Doc0'] = max_height_object
    df_copy.at['min_height_object', 'Doc0'] = min_height_object
    df_copy.at['num_of_elements', 'Doc0'] = num_of_elements
    df_copy.at['num_of_pars', 'Doc0'] = num_of_pars
    df_copy.at['num_of_pars_in_col_1', 'Doc0'] = num_of_pars_in_col_1
    df_copy.at['num_of_pars_in_col_2', 'Doc0'] = num_of_pars_in_col_2
    df_copy.at['num_of_paragraphs', 'Doc0'] = num_of_paragraphs
    df_copy.at['num_of_paragraphs_in_col_1', 'Doc0'] = num_of_paragraphs_in_col_1
    df_copy.at['num_of_paragraphs_in_col_2', 'Doc0'] = num_of_paragraphs_in_col_2
    df_copy.at['num_of_algorithms', 'Doc0'] = num_of_algorithms
    df_copy.at['num_of_algorithms_in_col_1', 'Doc0'] = num_of_algorithms_in_col_1
    df_copy.at['num_of_algorithms_in_col_2', 'Doc0'] = num_of_algorithms_in_col_2
    df_copy.at['num_of_formulas', 'Doc0'] = num_of_formulas
    df_copy.at['num_of_formulas_in_col_1', 'Doc0'] = num_of_formulas_in_col_1
    df_copy.at['num_of_formulas_in_col_2', 'Doc0'] = num_of_formulas_in_col_2
    df_copy.at['num_of_figures_in_col_1', 'Doc0'] = num_of_figures_in_col_1
    df_copy.at['num_of_figures_in_col_2', 'Doc0'] = num_of_figures_in_col_2
    df_copy.at['num_of_tables_in_col_1', 'Doc0'] = num_of_tables_in_col_1
    df_copy.at['num_of_tables_in_col_2', 'Doc0'] = num_of_tables_in_col_2
    df_copy.at['last_element', 'Doc0'] = last_object_index
    df_copy.at['sum_space_taken', 'Doc0'] = sum_space_taken
    df_copy.at['sum_open_space', 'Doc0'] = sum_open_space
    df_copy.at['sum_space_taken_by_figures', 'Doc0'] = sum_space_taken_by_figures
    df_copy.at['sum_space_taken_by_tables', 'Doc0'] = sum_space_taken_by_tables
    df_copy.at['sum_of_chars_across_doc', 'Doc0'] = sum_of_chars_across_doc
    df_copy.at['sum_of_words_from_pars', 'Doc0'] = sum_of_words_from_pars
    df_copy.at['sum_of_chars_from_pars', 'Doc0'] = sum_of_chars_from_pars
    df_copy.at['avg_num_of_words_from_pars', 'Doc0'] = avg_num_of_words_from_pars
    df_copy.at['avg_num_of_chars_from_pars', 'Doc0'] = avg_num_of_chars_from_pars
    df_copy.at['num_of_paragraphs_with_1_word_at_the_end', 'Doc0'] = num_of_paragraphs_with_1_word_at_the_end
    df_copy.at['num_of_figures_with_captions', 'Doc0'] = num_of_figures_with_captions
    df_copy.at['num_of_tables_with_captions', 'Doc0'] = num_of_tables_with_captions
    if (new_ending_y < df_copy.at['ending_y_of_doc', 'Doc0']):
        df_copy.at['ending_y_of_doc', 'Doc0'] = new_ending_y


    # df_copy = df_copy.T
    # df_copy.to_csv('pdf_extraction\\adi_comparing\\new_files\\example_test_for_me_1_4_2023_2.csv')
    # sys.exit()
    return new_dct_of_elements_in_order,count_dict_of_elements,summative_features,df_copy


def simulating_using_paragraph_tag_removal_operator(value_of_operator,object_used_on,num_of_object,df_copy,summative_features,dct_of_elements_in_order,count_dict_of_elements): # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    dict_for_indexes = {0: 'Par', 1: 'Par', 2: 'Par', 3: 'Par', 4: 'Par', 5: 'Par', 6: 'Par', 7: 'Par', 8: 'Paragraph',
                        9: 'Paragraph', 10: 'Figure', 11: 'Figure', 12: 'Figure', 13: 'Figure', 14: 'CaptionFigure',
                        15: 'CaptionFigure', 16: 'CaptionFigure', 17: 'CaptionFigure', 18: 'Table', 19: 'Table',
                        20: 'CaptionTable', 21: 'CaptionTable', 22: 'Section', 23: 'Section', 24: 'Section',
                        25: 'SubSection', 26: 'SubSection', 27: 'SubSection', 28: 'Enum', 29: 'Enum', 30: 'Enum',
                        31: 'Enum', 32: 'Enum', 33: 'Formula', 34: 'Formula', 35: 'Formula', 36: 'Formula',
                        37: 'Formula', 38: 'Algorithm', 39: 'Algorithm'}
    dict_for_indexes_inverse = {'Par1': 0, 'Par2': 1, 'Par3': 2, 'Par4': 3, 'Par5': 4, 'Par6': 5, 'Par7': 6, 'Par8': 7,
                                'Paragraph1': 8,
                                'Paragraph2': 9, 'Figure1': 10, 'Figure2': 11, 'Figure3': 12, 'Figure4': 13,
                                'CaptionFigure1': 14,
                                'CaptionFigure2': 15, 'CaptionFigure3': 16, 'CaptionFigure4': 17, 'Table1': 18,
                                'Table2': 19,
                                'CaptionTable1': 20, 'CaptionTable2': 21, 'Section1': 22, 'Section2': 23,
                                'Section3': 24,
                                'SubSection1': 25, 'SubSection2': 26, 'SubSection3': 27, 'Enum1': 28, 'Enum2': 29,
                                'Enum3': 30,
                                'Enum4': 31, 'Enum5': 32, 'Formula1': 33, 'Formula2': 34, 'Formula3': 35,
                                'Formula4': 36,
                                'Formula5': 37, 'Algorithm1': 38, 'Algorithm2': 39}
    object_used_on_combind_with_num_of_object = object_used_on + str(num_of_object)
    # we can know the hierarchy based on
    start_remembering = False
    objects_after_chosen_object = []
    enum_counter = 0
    for key in dct_of_elements_in_order.keys():
        if (object_used_on_combind_with_num_of_object == key):
            print(key)
            print(object_used_on_combind_with_num_of_object)
            objects_after_chosen_object.append(key)  # adding the object on which we performed the operator
            start_remembering = True
            continue
        if (start_remembering):
            objects_after_chosen_object.append(key)
    print(objects_after_chosen_object)
    indexx = 0
    new_dct_of_elements_in_order = {}
    print(dct_of_elements_in_order)
    for i in dct_of_elements_in_order:
        print(f'{i}' ':' f'{dct_of_elements_in_order[i]}')

    #sys.exit()
    object_without_index = ''.join([i for i in objects_after_chosen_object[0] if not i.isdigit()])
    get_index_representing_object_in_csv = dict_for_indexes_inverse[objects_after_chosen_object[0]]

    if(count_dict_of_elements['Par'] == 8):
        return
    else:
        index_of_new_par = count_dict_of_elements['Par']+1
        string_of_new_par = 'Par' + str(index_of_new_par)
        #new_par_key = objects_after_chosen_object[string_of_new_par]  # captions
        get_index_representing_new_par_key_in_csv = dict_for_indexes_inverse[string_of_new_par]
        df_copy.at['page' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['column' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['start_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0']
        if(df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):
            df_copy.at['end_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0']
        else:
            df_copy.at['end_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] - 10

        df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0']

        df_copy.at['height' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']-10
        df_copy.at['number_of_lines' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['number_of_lines' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['num_of_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['num_of_chars' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['num_of_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['num_of_words' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['last_line_length_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['last_line_length_chars' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['last_line_length_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['last_line_length_words' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['single_word_in_last_line' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['single_word_in_last_line' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_object_in_csv), 'Doc0']
        df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_object_in_csv), 'Doc0']
        #end of creation of new Par

        #delete the Paragraph:
        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['number_of_lines' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['num_of_chars' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['num_of_words' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['last_line_length_chars' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['last_line_length_words' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['single_word_in_last_line' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
        df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_object_in_csv), 'Doc0'] = 0

        count_dict_of_elements['Par'] +=1
        count_dict_of_elements['Paragraph'] -= 1

        Par_counter = 0
        for key in dct_of_elements_in_order.keys():
            if(key.startswith('Paragraph')):
                Par_counter += 1
                new_key_to_remember = 'Par' + str(Par_counter)
                new_dct_of_elements_in_order['Par' + str(Par_counter)] = {'page':df_copy.at['page' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'column': df_copy.at['column' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'start_y': df_copy.at['start_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'end_y': df_copy.at['end_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'spread_on_more_than_1_column': df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'height': df_copy.at['height' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'number_of_lines': df_copy.at['number_of_lines' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'num_of_chars': df_copy.at['num_of_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'num_of_words': df_copy.at['num_of_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'last_line_length_chars': df_copy.at['last_line_length_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'single_word_in_last_line': df_copy.at['single_word_in_last_line' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'space_between_this_object_and_last_object': df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                          ,'space_between_this_object_and_the_next_object': df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0']}
                continue
            else:
                new_key_for_par = ''.join(i for i in key if not i.isdigit())
                if(new_key_for_par == 'Par'):
                    Par_counter += 1
                    new_dct_of_elements_in_order['Par' + str(Par_counter)] = dct_of_elements_in_order[key]
                else:
                    new_dct_of_elements_in_order[key] = dct_of_elements_in_order[key]

        print(dct_of_elements_in_order)
        for i in dct_of_elements_in_order:
            print(f'{i}' ':' f'{dct_of_elements_in_order[i]}')

        print(new_dct_of_elements_in_order)
        for i in new_dct_of_elements_in_order:
            print(f'{i}' ':' f'{new_dct_of_elements_in_order[i]}')

        #neeed to know from where we need to reduce the page: (it will be from this: new_key_to_remember)
        objects_after_chosen_object = []
        start_remembering = False
        for key in new_dct_of_elements_in_order.keys():
            if (new_key_to_remember == key):
                start_remembering = True
                continue
            if (start_remembering):
                objects_after_chosen_object.append(key)

        print(objects_after_chosen_object)
        #now we will need to update the csv to represent the right pars:
        for key in new_dct_of_elements_in_order.keys():
            new_key_for_par = ''.join(i for i in key if not i.isdigit())
            if(new_key_for_par == 'Par'):
                #get his represented number in the csv
                df_copy.at['page' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['page']
                df_copy.at['column' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['column']
                df_copy.at['start_y' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['start_y']
                df_copy.at['end_y' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['end_y']
                df_copy.at['spread_on_more_than_1_column' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['spread_on_more_than_1_column']
                df_copy.at['height' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['height']
                df_copy.at['number_of_lines' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['number_of_lines']
                df_copy.at['num_of_chars' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['num_of_chars']
                df_copy.at['num_of_words' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['num_of_words']
                df_copy.at['last_line_length_chars' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['last_line_length_chars']
                df_copy.at['single_word_in_last_line' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['single_word_in_last_line']
                df_copy.at['space_between_this_object_and_last_object' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['space_between_this_object_and_last_object']
                df_copy.at['space_between_this_object_and_the_next_object' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['space_between_this_object_and_the_next_object']

    indexx = 0
    reduce_by_20 = False
    skip_next = False
    # now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)
    for j in objects_after_chosen_object:
        object_without_index = ''.join([i for i in j if not i.isdigit()])
        get_index_representing_object_in_csv = dict_for_indexes_inverse[j]
        if (indexx != len(objects_after_chosen_object) - 1):
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
        #now we will change all the next objects after the object (enum3)
        if (skip_next):
            skip_next = False
            indexx += 1
            continue
        if (object_without_index == 'Par' or object_without_index == 'Paragraph' or object_without_index == 'Enum'):  # to move a par,paragraph,enum to a before column we will need at least 3 rows of free space, so we will need to check it
            print(j)
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the par,paragraph,enum is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 670 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 660):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 680 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 680
                    if (df_copy.at['end_y' + str(
                            get_index_representing_object_in_csv), 'Doc0'] > 85):  # some of the par,paragraph,enum will still stay on the 2nd column
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                        df_copy.at[
                            'spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (object_without_index == 'Section' or object_without_index == 'SubSection'):
            print(j)
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the section,subsection is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 680 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 670):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 690 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 690
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10

        elif (object_without_index == 'Formula' or object_without_index == 'Algorithm'):
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60 and df_copy.at[
                'start_y' + str(
                        get_index_representing_object_in_csv), 'Doc0'] > 0):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                # i will try to fix a bug here:
                if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0 and df_copy.at[
                    'end_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0):
                    if (reduce_by_20):
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (
                object_without_index == 'Figure' or object_without_index == 'Table'):  # we will need to move them as a chunk
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] + df_copy.at[
                    'height' + str(get_index_representing_after_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                  'start_y' + str(
                                                                                                      get_index_representing_object_in_csv), 'Doc0'] + \
                                                                                              df_copy.at['height' + str(
                                                                                                  get_index_representing_object_in_csv), 'Doc0']
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                          'end_y' + str(
                                                                                                              get_index_representing_object_in_csv), 'Doc0'] + 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            skip_next = True

        indexx += 1

    # update summative features:
    # stuff about pars first:
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
    sum_space_taken = 0
    sum_open_space = 0
    sum_of_chars_across_doc = 0
    sum_of_chars_from_pars = 0
    sum_of_words_from_pars = 0
    num_of_paragraphs_with_1_word_at_the_end = 0

    num_of_pars = count_dict_of_elements['Par']
    num_of_elements = len(new_dct_of_elements_in_order)
    num_of_paragraphs = count_dict_of_elements['Paragraph']
    num_of_algorithms = count_dict_of_elements['Algorithm']
    num_of_formulas = count_dict_of_elements['Formula']
    num_of_enums = count_dict_of_elements['Enum']
    num_of_captionfigures = count_dict_of_elements['CaptionFigure']
    num_of_captiontables = count_dict_of_elements['CaptionTable']
    num_of_figures = count_dict_of_elements['Figure']
    num_of_tables = count_dict_of_elements['Table']
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []

    for i in range(0, num_of_pars):
        list_1.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_pars_in_col_1 += 1
        else:
            num_of_pars_in_col_2 += 1
        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(8, num_of_paragraphs + 8):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_paragraphs_in_col_1 += 1
        else:
            num_of_paragraphs_in_col_2 += 1

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(28, num_of_enums + 28):
        list_2.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']

    if (len(list_2) != 0):
        max_lines_enum = max(list_2)
        min_lines_enum = min(list_2)
    else:
        max_lines_enum = 0
        min_lines_enum = 0

    for i in range(14, num_of_captionfigures + 14):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    for i in range(20, num_of_captiontables + 20):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    if (len(list_3) != 0):
        max_lines_caption = max(list_3)
        min_lines_caption = min(list_3)
    else:
        max_lines_caption = 0
        min_lines_caption = 0

    for i in range(10, num_of_figures + 10):
        list_4.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_figures_in_col_1 += 1
        else:
            num_of_figures_in_col_2 += 1

    if (len(list_4) != 0):
        max_figure_y_space = max(list_4)
        min_figure_y_space = min(list_4)
        sum_space_taken_by_figures = sum(list_4)
    else:
        max_figure_y_space = 0
        min_figure_y_space = 0
        sum_space_taken_by_figures = 0

    for i in range(18, num_of_tables + 18):
        list_5.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_tables_in_col_1 += 1
        else:
            num_of_tables_in_col_2 += 1

    if (len(list_5) != 0):
        max_table_y_space = max(list_5)
        min_table_y_space = min(list_5)
        sum_space_taken_by_tables = sum(list_5)
    else:
        max_table_y_space = 0
        min_table_y_space = 0
        sum_space_taken_by_tables = 0

    part_of_last_height = 0
    for i in range(0, 39):
        if (df_copy.at['height' + str(i), 'Doc0'] > 0):
            list_6.append(df_copy.at['height' + str(i), 'Doc0'])
            sum_space_taken += df_copy.at['height' + str(i), 'Doc0']
        if (df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] > 0):
            sum_open_space += df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0']

        if (df_copy.at['start_y' + str(i), 'Doc0'] > df_copy.at['end_y' + str(i), 'Doc0'] and df_copy.at[
            'column' + str(
                i), 'Doc0'] == 1):  # we will want to see if there is an object that starts at the 2nd to last column and spread to the next column
            # we found one that starts at column 1 and ends on the 2nd page
            part_of_last_height += df_copy.at['end_y' + str(i), 'Doc0'] - 50
        if (df_copy.at['page' + str(i), 'Doc0'] == 1):  # on the last page we will take all of the objects height
            part_of_last_height += df_copy.at['height' + str(i), 'Doc0']

    new_ending_y = part_of_last_height

    if (len(list_6) != 0):
        max_height_object = max(list_6)
        min_height_object = min(list_6)
    else:
        max_height_object = 0
        min_height_object = 0

    for i in range(38, num_of_algorithms + 38):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_algorithms_in_col_1 += 1
        else:
            num_of_algorithms_in_col_2 += 1

    for i in range(33, num_of_formulas + 33):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_formulas_in_col_1 += 1
        else:
            num_of_formulas_in_col_2 += 1

    last_element = list(new_dct_of_elements_in_order)[-1]
    get_index_of_last_element = dict_for_indexes_inverse[last_element]
    last_element_with_no_index = ''.join([i for i in last_element if not i.isdigit()])
    if (last_element_with_no_index == 'Par'):
        last_object_index = 1
    elif (last_element_with_no_index == 'Figure'):
        last_object_index = 2
    elif (last_element_with_no_index == 'CaptionFigure'):
        last_object_index = 3
    elif (last_element_with_no_index == 'Table'):
        last_object_index = 4
    elif (last_element_with_no_index == 'CaptionTable'):
        last_object_index = 5
    elif (last_element_with_no_index == 'Section'):
        last_object_index = 6
    elif (last_element_with_no_index == 'SubSection'):
        last_object_index = 7
    elif (last_element_with_no_index == 'Matrix'):
        last_object_index = 8
    elif (last_element_with_no_index == 'Enum'):
        last_object_index = 9
    elif (last_element_with_no_index == 'Formula'):
        last_object_index = 10
    elif (last_element_with_no_index == 'Algorithm'):
        last_object_index = 11
    else:
        last_object_index = 0

    if (len(list_1) != 0):
        max_lines_par = max(list_1)
        min_lines_par = min(list_1)
    else:
        max_lines_par = 0
        min_lines_par = 0

    if (count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'] != 0):
        avg_num_of_words_from_pars = sum_of_words_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
        avg_num_of_chars_from_pars = sum_of_chars_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
    else:
        avg_num_of_words_from_pars = 0
        avg_num_of_chars_from_pars = 0

    num_of_figures_with_captions = num_of_figures
    num_of_tables_with_captions = num_of_tables

    # putting it all together:
    summative_features['max_lines_par'] = max_lines_par
    summative_features['min_lines_par'] = min_lines_par
    summative_features['max_lines_enum'] = max_lines_enum
    summative_features['min_lines_enum'] = min_lines_enum
    summative_features['max_lines_caption'] = max_lines_caption
    summative_features['min_lines_caption'] = min_lines_caption
    summative_features['max_figure_y_space'] = max_figure_y_space
    summative_features['min_figure_y_space'] = min_figure_y_space
    summative_features['max_table_y_space'] = max_table_y_space
    summative_features['min_table_y_space'] = min_table_y_space
    summative_features['max_height_object'] = max_height_object
    summative_features['min_height_object'] = min_height_object
    summative_features['num_of_elements'] = num_of_elements
    summative_features['num_of_pars'] = num_of_pars
    summative_features['num_of_pars_in_col_1'] = num_of_pars_in_col_1
    summative_features['num_of_pars_in_col_2'] = num_of_pars_in_col_2
    summative_features['num_of_paragraphs'] = num_of_paragraphs
    summative_features['num_of_paragraphs_in_col_1'] = num_of_paragraphs_in_col_1
    summative_features['num_of_paragraphs_in_col_2'] = num_of_paragraphs_in_col_2
    summative_features['num_of_algorithms'] = num_of_algorithms
    summative_features['num_of_algorithms_in_col_1'] = num_of_algorithms_in_col_1
    summative_features['num_of_algorithms_in_col_2'] = num_of_algorithms_in_col_2
    summative_features['num_of_formulas'] = num_of_formulas
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
    summative_features['avg_num_of_words_from_pars'] = avg_num_of_words_from_pars
    summative_features['avg_num_of_chars_from_pars'] = avg_num_of_chars_from_pars
    summative_features['num_of_paragraphs_with_1_word_at_the_end'] = num_of_paragraphs_with_1_word_at_the_end
    summative_features['num_of_figures_with_captions'] = num_of_figures_with_captions
    summative_features['num_of_tables_with_captions'] = num_of_tables_with_captions
    if (new_ending_y < summative_features['ending_y_of_doc']):
        summative_features['ending_y_of_doc'] = new_ending_y

    df_copy.at['max_lines_par', 'Doc0'] = max_lines_par
    df_copy.at['min_lines_par', 'Doc0'] = min_lines_par
    df_copy.at['max_lines_enum', 'Doc0'] = max_lines_enum
    df_copy.at['min_lines_enum', 'Doc0'] = min_lines_enum
    df_copy.at['max_lines_caption', 'Doc0'] = max_lines_caption
    df_copy.at['min_lines_caption', 'Doc0'] = min_lines_caption
    df_copy.at['max_figure_y_space', 'Doc0'] = max_figure_y_space
    df_copy.at['min_figure_y_space', 'Doc0'] = min_figure_y_space
    df_copy.at['max_table_y_space', 'Doc0'] = max_table_y_space
    df_copy.at['min_table_y_space', 'Doc0'] = min_table_y_space
    df_copy.at['max_height_object', 'Doc0'] = max_height_object
    df_copy.at['min_height_object', 'Doc0'] = min_height_object
    df_copy.at['num_of_elements', 'Doc0'] = num_of_elements
    df_copy.at['num_of_pars', 'Doc0'] = num_of_pars
    df_copy.at['num_of_pars_in_col_1', 'Doc0'] = num_of_pars_in_col_1
    df_copy.at['num_of_pars_in_col_2', 'Doc0'] = num_of_pars_in_col_2
    df_copy.at['num_of_paragraphs', 'Doc0'] = num_of_paragraphs
    df_copy.at['num_of_paragraphs_in_col_1', 'Doc0'] = num_of_paragraphs_in_col_1
    df_copy.at['num_of_paragraphs_in_col_2', 'Doc0'] = num_of_paragraphs_in_col_2
    df_copy.at['num_of_algorithms', 'Doc0'] = num_of_algorithms
    df_copy.at['num_of_algorithms_in_col_1', 'Doc0'] = num_of_algorithms_in_col_1
    df_copy.at['num_of_algorithms_in_col_2', 'Doc0'] = num_of_algorithms_in_col_2
    df_copy.at['num_of_formulas', 'Doc0'] = num_of_formulas
    df_copy.at['num_of_formulas_in_col_1', 'Doc0'] = num_of_formulas_in_col_1
    df_copy.at['num_of_formulas_in_col_2', 'Doc0'] = num_of_formulas_in_col_2
    df_copy.at['num_of_figures_in_col_1', 'Doc0'] = num_of_figures_in_col_1
    df_copy.at['num_of_figures_in_col_2', 'Doc0'] = num_of_figures_in_col_2
    df_copy.at['num_of_tables_in_col_1', 'Doc0'] = num_of_tables_in_col_1
    df_copy.at['num_of_tables_in_col_2', 'Doc0'] = num_of_tables_in_col_2
    df_copy.at['last_element', 'Doc0'] = last_object_index
    df_copy.at['sum_space_taken', 'Doc0'] = sum_space_taken
    df_copy.at['sum_open_space', 'Doc0'] = sum_open_space
    df_copy.at['sum_space_taken_by_figures', 'Doc0'] = sum_space_taken_by_figures
    df_copy.at['sum_space_taken_by_tables', 'Doc0'] = sum_space_taken_by_tables
    df_copy.at['sum_of_chars_across_doc', 'Doc0'] = sum_of_chars_across_doc
    df_copy.at['sum_of_words_from_pars', 'Doc0'] = sum_of_words_from_pars
    df_copy.at['sum_of_chars_from_pars', 'Doc0'] = sum_of_chars_from_pars
    df_copy.at['avg_num_of_words_from_pars', 'Doc0'] = avg_num_of_words_from_pars
    df_copy.at['avg_num_of_chars_from_pars', 'Doc0'] = avg_num_of_chars_from_pars
    df_copy.at['num_of_paragraphs_with_1_word_at_the_end', 'Doc0'] = num_of_paragraphs_with_1_word_at_the_end
    df_copy.at['num_of_figures_with_captions', 'Doc0'] = num_of_figures_with_captions
    df_copy.at['num_of_tables_with_captions', 'Doc0'] = num_of_tables_with_captions
    if (new_ending_y < df_copy.at['ending_y_of_doc', 'Doc0']):
        df_copy.at['ending_y_of_doc', 'Doc0'] = new_ending_y


    # df_copy = df_copy.T
    # df_copy.to_csv('pdf_extraction\\adi_comparing\\new_files\\example_test_for_me_1_4_2023_2.csv')
    # sys.exit()
    return new_dct_of_elements_in_order,count_dict_of_elements,summative_features,df_copy


def simulating_using_combining_pars_operator(value_of_operator,object_used_on,num_of_object,df_copy,summative_features,dct_of_elements_in_order,count_dict_of_elements): # value = object_used_on(dict),key = object_used_on_name+index,operator_value = which operator value to use, in the case of vspace its 1,2,3,4
    dict_for_indexes = {0: 'Par', 1: 'Par', 2: 'Par', 3: 'Par', 4: 'Par', 5: 'Par', 6: 'Par', 7: 'Par', 8: 'Paragraph',
                        9: 'Paragraph', 10: 'Figure', 11: 'Figure', 12: 'Figure', 13: 'Figure', 14: 'CaptionFigure',
                        15: 'CaptionFigure', 16: 'CaptionFigure', 17: 'CaptionFigure', 18: 'Table', 19: 'Table',
                        20: 'CaptionTable', 21: 'CaptionTable', 22: 'Section', 23: 'Section', 24: 'Section',
                        25: 'SubSection', 26: 'SubSection', 27: 'SubSection', 28: 'Enum', 29: 'Enum', 30: 'Enum',
                        31: 'Enum', 32: 'Enum', 33: 'Formula', 34: 'Formula', 35: 'Formula', 36: 'Formula',
                        37: 'Formula', 38: 'Algorithm', 39: 'Algorithm'}
    dict_for_indexes_inverse = {'Par1': 0, 'Par2': 1, 'Par3': 2, 'Par4': 3, 'Par5': 4, 'Par6': 5, 'Par7': 6, 'Par8': 7,
                                'Paragraph1': 8,
                                'Paragraph2': 9, 'Figure1': 10, 'Figure2': 11, 'Figure3': 12, 'Figure4': 13,
                                'CaptionFigure1': 14,
                                'CaptionFigure2': 15, 'CaptionFigure3': 16, 'CaptionFigure4': 17, 'Table1': 18,
                                'Table2': 19,
                                'CaptionTable1': 20, 'CaptionTable2': 21, 'Section1': 22, 'Section2': 23,
                                'Section3': 24,
                                'SubSection1': 25, 'SubSection2': 26, 'SubSection3': 27, 'Enum1': 28, 'Enum2': 29,
                                'Enum3': 30,
                                'Enum4': 31, 'Enum5': 32, 'Formula1': 33, 'Formula2': 34, 'Formula3': 35,
                                'Formula4': 36,
                                'Formula5': 37, 'Algorithm1': 38, 'Algorithm2': 39}
    object_used_on_combind_with_num_of_object = object_used_on + str(int(num_of_object)-1) #we will want the first object so it will be easy to find the next one
    # we can know the hierarchy based on
    start_remembering = False
    objects_after_chosen_object = []
    par_counter = 0
    par_1 = 0
    par_2 = 0
    for key in dct_of_elements_in_order.keys():
        new_key_for_par = ''.join(i for i in key if not i.isdigit())
        if (object_used_on_combind_with_num_of_object == key):
            print(key)
            print(object_used_on_combind_with_num_of_object)
            objects_after_chosen_object.append(key)  # adding the object on which we performed the operator
            par_counter+=1
            par_1 = par_counter
            start_remembering = True
            continue
        if (start_remembering):
            new_key_for_par = ''.join(i for i in key if not i.isdigit())
            if(new_key_for_par == 'Par'):
                if(par_1 == par_counter):
                    par_counter += 1
                    par_2 = par_counter
                else:
                    par_counter += 1
            objects_after_chosen_object.append(key)
            continue
        if(new_key_for_par == 'Par'):
            par_counter+=1
    print(objects_after_chosen_object)
    print(par_1)
    print(par_2)
    indexx = 0
    new_dct_of_elements_in_order = {}
    print(dct_of_elements_in_order)
    for i in dct_of_elements_in_order:
        print(f'{i}' ':' f'{dct_of_elements_in_order[i]}')
    # now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)

    object_without_index = ''.join([i for i in objects_after_chosen_object[0] if not i.isdigit()])
    get_index_representing_object_in_csv = dict_for_indexes_inverse[objects_after_chosen_object[0]]
    enum_list = []

    index_of_first_par = dict_for_indexes_inverse['Par'+str(par_1)]
    index_of_second_par = dict_for_indexes_inverse['Par'+str(par_2)]
    print(index_of_first_par)
    print(index_of_second_par)

    index_of_new_par = count_dict_of_elements['Par']+1
    string_of_new_par = 'Par' + str(index_of_new_par)
    #new_par_key = objects_after_chosen_object[string_of_new_par]  # captions
    get_index_representing_new_par_key_in_csv = index_of_second_par #we do that because if we dont have space for another par, it will not crash
    df_copy.at['page' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['page' + str(index_of_first_par), 'Doc0']
    df_copy.at['column' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['column' + str(index_of_first_par), 'Doc0']
    df_copy.at['start_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['start_y' + str(index_of_first_par), 'Doc0']
    if(df_copy.at['end_y' + str(index_of_second_par), 'Doc0'] < 60): #ending of 2nd par is at the top of a new column
        df_copy.at['end_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = 700
        spread_on_more_than_1 = False
        if (df_copy.at['spread_on_more_than_1_column' + str(index_of_first_par), 'Doc0'] == 1 or df_copy.at['spread_on_more_than_1_column' + str(index_of_second_par), 'Doc0'] == 1):  # one of the enums is in a different page or column, then it is spreading on more than 1 column
            spread_on_more_than_1 = True
    else:
        df_copy.at['end_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['end_y' + str(index_of_second_par), 'Doc0']-10
        spread_on_more_than_1 = False
        if (df_copy.at['spread_on_more_than_1_column' + str(index_of_first_par), 'Doc0'] == 1 or df_copy.at['spread_on_more_than_1_column' + str(index_of_second_par), 'Doc0'] == 1):  # one of the enums is in a different page or column, then it is spreading on more than 1 column
            spread_on_more_than_1 = True
    if(spread_on_more_than_1):
        df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = 1
    else:
        df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = 0

    combined_height = df_copy.at['height' + str(index_of_first_par), 'Doc0'] + df_copy.at['height' + str(index_of_second_par), 'Doc0']
    combined_number_of_lines = df_copy.at['number_of_lines' + str(index_of_first_par), 'Doc0'] + df_copy.at['number_of_lines' + str(index_of_second_par), 'Doc0'] - 1
    combined_num_of_chars = df_copy.at['num_of_chars' + str(index_of_first_par), 'Doc0'] + df_copy.at['num_of_chars' + str(index_of_second_par), 'Doc0']
    combined_num_of_words = df_copy.at['num_of_words' + str(index_of_first_par), 'Doc0'] + df_copy.at['num_of_words' + str(index_of_second_par), 'Doc0']

    df_copy.at['height' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = combined_height-10
    df_copy.at['number_of_lines' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = combined_number_of_lines
    df_copy.at['num_of_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = combined_num_of_chars
    df_copy.at['num_of_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = combined_num_of_words
    df_copy.at['last_line_length_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['last_line_length_chars' + str(index_of_second_par), 'Doc0']
    df_copy.at['last_line_length_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['last_line_length_words' + str(index_of_second_par), 'Doc0']
    df_copy.at['single_word_in_last_line' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['single_word_in_last_line' + str(index_of_second_par), 'Doc0']
    df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] = df_copy.at['space_between_this_object_and_last_object' + str(index_of_first_par), 'Doc0']
    df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0'] =df_copy.at['space_between_this_object_and_the_next_object' + str(index_of_second_par), 'Doc0']

    #end of creation of new Par

    count_dict_of_elements['Par'] -=1

    Par_counter = 0
    skip_nextt = False
    for key in dct_of_elements_in_order.keys():
        if(skip_nextt):
            skip_nextt = False
            continue
        if(key == 'Par' + str(index_of_first_par+1)): #found the par we need to replace
            skip_nextt = True
            Par_counter += 1
            new_key_to_remember = 'Par' + str(Par_counter)
            new_dct_of_elements_in_order['Par' + str(Par_counter)] = {'page':df_copy.at['page' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'column': df_copy.at['column' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'start_y': df_copy.at['start_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'end_y': df_copy.at['end_y' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'spread_on_more_than_1_column': df_copy.at['spread_on_more_than_1_column' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'height': df_copy.at['height' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'number_of_lines': df_copy.at['number_of_lines' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'num_of_chars': df_copy.at['num_of_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'num_of_words': df_copy.at['num_of_words' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'last_line_length_chars': df_copy.at['last_line_length_chars' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'single_word_in_last_line': df_copy.at['single_word_in_last_line' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'space_between_this_object_and_last_object': df_copy.at['space_between_this_object_and_last_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0']
                                                                      ,'space_between_this_object_and_the_next_object': df_copy.at['space_between_this_object_and_the_next_object' + str(get_index_representing_new_par_key_in_csv), 'Doc0']}

            # delete par 2 and (replace par 1 after):
            df_copy.at['page' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['column' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['start_y' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['end_y' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['spread_on_more_than_1_column' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['height' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['number_of_lines' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['num_of_chars' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['num_of_words' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['last_line_length_chars' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['last_line_length_words' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['single_word_in_last_line' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['space_between_this_object_and_last_object' + str(index_of_second_par), 'Doc0'] = 0
            df_copy.at['space_between_this_object_and_the_next_object' + str(index_of_second_par), 'Doc0'] = 0
            continue
        else:
            new_key_for_par = ''.join(i for i in key if not i.isdigit())
            if(new_key_for_par == 'Par'):
                Par_counter += 1
                new_dct_of_elements_in_order['Par' + str(Par_counter)] = dct_of_elements_in_order[key]
            else:
                new_dct_of_elements_in_order[key] = dct_of_elements_in_order[key]

    print(dct_of_elements_in_order)
    for i in dct_of_elements_in_order:
        print(f'{i}' ':' f'{dct_of_elements_in_order[i]}')

    print(new_dct_of_elements_in_order)
    for i in new_dct_of_elements_in_order:
        print(f'{i}' ':' f'{new_dct_of_elements_in_order[i]}')

    #neeed to know from where we need to reduce the page: (it will be from this: new_key_to_remember)
    objects_after_chosen_object = []
    start_remembering = False
    for key in new_dct_of_elements_in_order.keys():
        if (new_key_to_remember == key):
            start_remembering = True
            continue
        if (start_remembering):
            objects_after_chosen_object.append(key)

    print(objects_after_chosen_object)
    #now we will need to update the csv to represent the right pars:
    counter = 0
    for key in new_dct_of_elements_in_order.keys():
        new_key_for_par = ''.join(i for i in key if not i.isdigit())
        if(new_key_for_par == 'Par'):
            counter+=1
            #get his represented number in the csv
            df_copy.at['page' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['page']
            df_copy.at['column' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['column']
            df_copy.at['start_y' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['start_y']
            df_copy.at['end_y' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['end_y']
            df_copy.at['spread_on_more_than_1_column' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['spread_on_more_than_1_column']
            df_copy.at['height' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['height']
            df_copy.at['number_of_lines' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['number_of_lines']
            df_copy.at['num_of_chars' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['num_of_chars']
            df_copy.at['num_of_words' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['num_of_words']
            df_copy.at['last_line_length_chars' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['last_line_length_chars']
            df_copy.at['single_word_in_last_line' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['single_word_in_last_line']
            df_copy.at['space_between_this_object_and_last_object' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['space_between_this_object_and_last_object']
            df_copy.at['space_between_this_object_and_the_next_object' + str(dict_for_indexes_inverse[key]), 'Doc0'] = new_dct_of_elements_in_order[key]['space_between_this_object_and_the_next_object']

    for i in range(counter,8):
        df_copy.at['page' + str(i), 'Doc0'] = 0
        df_copy.at['column' + str(i), 'Doc0'] = 0
        df_copy.at['start_y' + str(i), 'Doc0'] = 0
        df_copy.at['end_y' + str(i), 'Doc0'] = 0
        df_copy.at['spread_on_more_than_1_column' + str(i), 'Doc0'] =0
        df_copy.at['height' + str(i), 'Doc0'] = 0
        df_copy.at['number_of_lines' + str(i), 'Doc0'] = 0
        df_copy.at['num_of_chars' + str(i), 'Doc0'] = 0
        df_copy.at['num_of_words' + str(i), 'Doc0'] = 0
        df_copy.at['last_line_length_chars' + str(i), 'Doc0'] =0
        df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] = 0
        df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] = 0
        df_copy.at['space_between_this_object_and_the_next_object' + str(i), 'Doc0'] = 0

    indexx = 0
    reduce_by_20 = False
    skip_next = False
    # now we will need to change each object, to go up 1 row (we assume we managed to reduce atleast 1 row)
    for j in objects_after_chosen_object:
        object_without_index = ''.join([i for i in j if not i.isdigit()])
        get_index_representing_object_in_csv = dict_for_indexes_inverse[j]
        if (indexx != len(objects_after_chosen_object) - 1):
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
        #now we will change all the next objects after the object (enum3)
        if (skip_next):
            skip_next = False
            indexx += 1
            continue
        if (object_without_index == 'Par' or object_without_index == 'Paragraph' or object_without_index == 'Enum'):  # to move a par,paragraph,enum to a before column we will need at least 3 rows of free space, so we will need to check it
            print(j)
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the par,paragraph,enum is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 670 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 660):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 680 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 680
                    if (df_copy.at['end_y' + str(
                            get_index_representing_object_in_csv), 'Doc0'] > 85):  # some of the par,paragraph,enum will still stay on the 2nd column
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        reduce_by_20 = True
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                        df_copy.at[
                            'spread_on_more_than_1_column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (object_without_index == 'Section' or object_without_index == 'SubSection'):
            print(j)
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the section,subsection is the first object in the column
                # we will need to check if there is enough space to insert the start of this object (par,paragraph,enum) in the before column
                before_object_key = objects_after_chosen_object[indexx - 1]
                get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
                if (df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0'] < 680 and df_copy.at[
                    'end_y' + str(
                            get_index_representing_before_object_in_csv), 'Doc0'] > 670):  # there is enough space to put the start of the par,paragraph,enum on the before column
                    space_between = 690 - df_copy.at['end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    # now we will change the par,paragraph,enum information:
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 690
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:  # at this point nothing can change because there is not enough space to move
                    break
            else:  # nothing moves to another column
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10

        elif (object_without_index == 'Formula' or object_without_index == 'Algorithm'):
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] < 60 and df_copy.at[
                'start_y' + str(
                        get_index_representing_object_in_csv), 'Doc0'] > 0):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                # i will try to fix a bug here:
                if (df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0 and df_copy.at[
                    'end_y' + str(get_index_representing_object_in_csv), 'Doc0'] != 0):
                    if (reduce_by_20):
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    else:
                        df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                        df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
        elif (
                object_without_index == 'Figure' or object_without_index == 'Table'):  # we will need to move them as a chunk
            print(j)
            before_object_key = objects_after_chosen_object[indexx - 1]
            get_index_representing_before_object_in_csv = dict_for_indexes_inverse[before_object_key]
            after_object_key = objects_after_chosen_object[indexx + 1]  # captions
            get_index_representing_after_object_in_csv = dict_for_indexes_inverse[after_object_key]
            if (df_copy.at['start_y' + str(
                    get_index_representing_object_in_csv), 'Doc0'] < 60):  # if the object is first in the column
                space_needed = df_copy.at['height' + str(get_index_representing_object_in_csv), 'Doc0'] + df_copy.at[
                    'height' + str(get_index_representing_after_object_in_csv), 'Doc0']
                if (abs(700 - df_copy.at[
                    'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']) >= space_needed + 10):
                    space_between = 700 - space_needed - df_copy.at[
                        'end_y' + str(get_index_representing_before_object_in_csv), 'Doc0']
                    df_copy.at['space_between_this_object_and_the_next_object' + str(
                        get_index_representing_before_object_in_csv), 'Doc0'] = space_between  # update for before object
                    df_copy.at['space_between_this_object_and_last_object' + str(
                        get_index_representing_object_in_csv), 'Doc0'] = space_between
                    if (df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] == 1 and df_copy.at[
                        'column' + str(get_index_representing_object_in_csv), 'Doc0'] == 0):
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 1
                        df_copy.at['page' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    else:
                        df_copy.at['column' + str(get_index_representing_object_in_csv), 'Doc0'] = 0
                        # caption
                        df_copy.at['column' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 0
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] = 700 - space_needed
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                  'start_y' + str(
                                                                                                      get_index_representing_object_in_csv), 'Doc0'] + \
                                                                                              df_copy.at['height' + str(
                                                                                                  get_index_representing_object_in_csv), 'Doc0']
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = df_copy.at[
                                                                                                          'end_y' + str(
                                                                                                              get_index_representing_object_in_csv), 'Doc0'] + 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] = 700
                else:
                    break  # nothing can change past him
            else:  # place to move
                if (reduce_by_20):
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 20
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 20
                else:
                    df_copy.at['start_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_object_in_csv), 'Doc0'] -= 10
                    # caption
                    df_copy.at['start_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
                    df_copy.at['end_y' + str(get_index_representing_after_object_in_csv), 'Doc0'] -= 10
            skip_next = True

        indexx += 1

    # update summative features:
    # stuff about pars first:
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
    sum_space_taken = 0
    sum_open_space = 0
    sum_of_chars_across_doc = 0
    sum_of_chars_from_pars = 0
    sum_of_words_from_pars = 0
    num_of_paragraphs_with_1_word_at_the_end = 0

    num_of_pars = count_dict_of_elements['Par']
    num_of_elements = len(new_dct_of_elements_in_order)
    num_of_paragraphs = count_dict_of_elements['Paragraph']
    num_of_algorithms = count_dict_of_elements['Algorithm']
    num_of_formulas = count_dict_of_elements['Formula']
    num_of_enums = count_dict_of_elements['Enum']
    num_of_captionfigures = count_dict_of_elements['CaptionFigure']
    num_of_captiontables = count_dict_of_elements['CaptionTable']
    num_of_figures = count_dict_of_elements['Figure']
    num_of_tables = count_dict_of_elements['Table']
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []

    for i in range(0, num_of_pars):
        list_1.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_pars_in_col_1 += 1
        else:
            num_of_pars_in_col_2 += 1
        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(8, num_of_paragraphs + 8):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_paragraphs_in_col_1 += 1
        else:
            num_of_paragraphs_in_col_2 += 1

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']
            sum_of_chars_from_pars += df_copy.at['num_of_chars' + str(i), 'Doc0']

        if (df_copy.at['num_of_words' + str(i), 'Doc0'] > 0):
            sum_of_words_from_pars += df_copy.at['num_of_words' + str(i), 'Doc0']

        if (df_copy.at['single_word_in_last_line' + str(i), 'Doc0'] == 1):
            num_of_paragraphs_with_1_word_at_the_end += 1

    for i in range(28, num_of_enums + 28):
        list_2.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

        if (df_copy.at['num_of_chars' + str(i), 'Doc0'] > 0):
            sum_of_chars_across_doc += df_copy.at['num_of_chars' + str(i), 'Doc0']

    if (len(list_2) != 0):
        max_lines_enum = max(list_2)
        min_lines_enum = min(list_2)
    else:
        max_lines_enum = 0
        min_lines_enum = 0

    for i in range(14, num_of_captionfigures + 14):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    for i in range(20, num_of_captiontables + 20):
        list_3.append(df_copy.at['number_of_lines' + str(i), 'Doc0'])

    if (len(list_3) != 0):
        max_lines_caption = max(list_3)
        min_lines_caption = min(list_3)
    else:
        max_lines_caption = 0
        min_lines_caption = 0

    for i in range(10, num_of_figures + 10):
        list_4.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_figures_in_col_1 += 1
        else:
            num_of_figures_in_col_2 += 1

    if (len(list_4) != 0):
        max_figure_y_space = max(list_4)
        min_figure_y_space = min(list_4)
        sum_space_taken_by_figures = sum(list_4)
    else:
        max_figure_y_space = 0
        min_figure_y_space = 0
        sum_space_taken_by_figures = 0

    for i in range(18, num_of_tables + 18):
        list_5.append(df_copy.at['height' + str(i), 'Doc0'])
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_tables_in_col_1 += 1
        else:
            num_of_tables_in_col_2 += 1

    if (len(list_5) != 0):
        max_table_y_space = max(list_5)
        min_table_y_space = min(list_5)
        sum_space_taken_by_tables = sum(list_5)
    else:
        max_table_y_space = 0
        min_table_y_space = 0
        sum_space_taken_by_tables = 0

    part_of_last_height = 0
    for i in range(0, 39):
        if (df_copy.at['height' + str(i), 'Doc0'] > 0):
            list_6.append(df_copy.at['height' + str(i), 'Doc0'])
            sum_space_taken += df_copy.at['height' + str(i), 'Doc0']
        if (df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0'] > 0):
            sum_open_space += df_copy.at['space_between_this_object_and_last_object' + str(i), 'Doc0']

        if (df_copy.at['start_y' + str(i), 'Doc0'] > df_copy.at['end_y' + str(i), 'Doc0'] and df_copy.at[
            'column' + str(
                i), 'Doc0'] == 1):  # we will want to see if there is an object that starts at the 2nd to last column and spread to the next column
            # we found one that starts at column 1 and ends on the 2nd page
            part_of_last_height += df_copy.at['end_y' + str(i), 'Doc0'] - 50
        if (df_copy.at['page' + str(i), 'Doc0'] == 1):  # on the last page we will take all of the objects height
            part_of_last_height += df_copy.at['height' + str(i), 'Doc0']

    new_ending_y = part_of_last_height

    if (len(list_6) != 0):
        max_height_object = max(list_6)
        min_height_object = min(list_6)
    else:
        max_height_object = 0
        min_height_object = 0

    for i in range(38, num_of_algorithms + 38):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_algorithms_in_col_1 += 1
        else:
            num_of_algorithms_in_col_2 += 1

    for i in range(33, num_of_formulas + 33):
        if (df_copy.at['column' + str(i), 'Doc0'] == 0):
            num_of_formulas_in_col_1 += 1
        else:
            num_of_formulas_in_col_2 += 1

    last_element = list(new_dct_of_elements_in_order)[-1]
    get_index_of_last_element = dict_for_indexes_inverse[last_element]
    last_element_with_no_index = ''.join([i for i in last_element if not i.isdigit()])
    if (last_element_with_no_index == 'Par'):
        last_object_index = 1
    elif (last_element_with_no_index == 'Figure'):
        last_object_index = 2
    elif (last_element_with_no_index == 'CaptionFigure'):
        last_object_index = 3
    elif (last_element_with_no_index == 'Table'):
        last_object_index = 4
    elif (last_element_with_no_index == 'CaptionTable'):
        last_object_index = 5
    elif (last_element_with_no_index == 'Section'):
        last_object_index = 6
    elif (last_element_with_no_index == 'SubSection'):
        last_object_index = 7
    elif (last_element_with_no_index == 'Matrix'):
        last_object_index = 8
    elif (last_element_with_no_index == 'Enum'):
        last_object_index = 9
    elif (last_element_with_no_index == 'Formula'):
        last_object_index = 10
    elif (last_element_with_no_index == 'Algorithm'):
        last_object_index = 11
    else:
        last_object_index = 0

    if (len(list_1) != 0):
        max_lines_par = max(list_1)
        min_lines_par = min(list_1)
    else:
        max_lines_par = 0
        min_lines_par = 0

    if (count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'] != 0):
        avg_num_of_words_from_pars = sum_of_words_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
        avg_num_of_chars_from_pars = sum_of_chars_from_pars / (
                count_dict_of_elements['Par'] + count_dict_of_elements['Paragraph'])
    else:
        avg_num_of_words_from_pars = 0
        avg_num_of_chars_from_pars = 0

    num_of_figures_with_captions = num_of_figures
    num_of_tables_with_captions = num_of_tables

    # putting it all together:
    summative_features['max_lines_par'] = max_lines_par
    summative_features['min_lines_par'] = min_lines_par
    summative_features['max_lines_enum'] = max_lines_enum
    summative_features['min_lines_enum'] = min_lines_enum
    summative_features['max_lines_caption'] = max_lines_caption
    summative_features['min_lines_caption'] = min_lines_caption
    summative_features['max_figure_y_space'] = max_figure_y_space
    summative_features['min_figure_y_space'] = min_figure_y_space
    summative_features['max_table_y_space'] = max_table_y_space
    summative_features['min_table_y_space'] = min_table_y_space
    summative_features['max_height_object'] = max_height_object
    summative_features['min_height_object'] = min_height_object
    summative_features['num_of_elements'] = num_of_elements
    summative_features['num_of_pars'] = num_of_pars
    summative_features['num_of_pars_in_col_1'] = num_of_pars_in_col_1
    summative_features['num_of_pars_in_col_2'] = num_of_pars_in_col_2
    summative_features['num_of_paragraphs'] = num_of_paragraphs
    summative_features['num_of_paragraphs_in_col_1'] = num_of_paragraphs_in_col_1
    summative_features['num_of_paragraphs_in_col_2'] = num_of_paragraphs_in_col_2
    summative_features['num_of_algorithms'] = num_of_algorithms
    summative_features['num_of_algorithms_in_col_1'] = num_of_algorithms_in_col_1
    summative_features['num_of_algorithms_in_col_2'] = num_of_algorithms_in_col_2
    summative_features['num_of_formulas'] = num_of_formulas
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
    summative_features['avg_num_of_words_from_pars'] = avg_num_of_words_from_pars
    summative_features['avg_num_of_chars_from_pars'] = avg_num_of_chars_from_pars
    summative_features['num_of_paragraphs_with_1_word_at_the_end'] = num_of_paragraphs_with_1_word_at_the_end
    summative_features['num_of_figures_with_captions'] = num_of_figures_with_captions
    summative_features['num_of_tables_with_captions'] = num_of_tables_with_captions
    if (new_ending_y < summative_features['ending_y_of_doc']):
        summative_features['ending_y_of_doc'] = new_ending_y

    df_copy.at['max_lines_par', 'Doc0'] = max_lines_par
    df_copy.at['min_lines_par', 'Doc0'] = min_lines_par
    df_copy.at['max_lines_enum', 'Doc0'] = max_lines_enum
    df_copy.at['min_lines_enum', 'Doc0'] = min_lines_enum
    df_copy.at['max_lines_caption', 'Doc0'] = max_lines_caption
    df_copy.at['min_lines_caption', 'Doc0'] = min_lines_caption
    df_copy.at['max_figure_y_space', 'Doc0'] = max_figure_y_space
    df_copy.at['min_figure_y_space', 'Doc0'] = min_figure_y_space
    df_copy.at['max_table_y_space', 'Doc0'] = max_table_y_space
    df_copy.at['min_table_y_space', 'Doc0'] = min_table_y_space
    df_copy.at['max_height_object', 'Doc0'] = max_height_object
    df_copy.at['min_height_object', 'Doc0'] = min_height_object
    df_copy.at['num_of_elements', 'Doc0'] = num_of_elements
    df_copy.at['num_of_pars', 'Doc0'] = num_of_pars
    df_copy.at['num_of_pars_in_col_1', 'Doc0'] = num_of_pars_in_col_1
    df_copy.at['num_of_pars_in_col_2', 'Doc0'] = num_of_pars_in_col_2
    df_copy.at['num_of_paragraphs', 'Doc0'] = num_of_paragraphs
    df_copy.at['num_of_paragraphs_in_col_1', 'Doc0'] = num_of_paragraphs_in_col_1
    df_copy.at['num_of_paragraphs_in_col_2', 'Doc0'] = num_of_paragraphs_in_col_2
    df_copy.at['num_of_algorithms', 'Doc0'] = num_of_algorithms
    df_copy.at['num_of_algorithms_in_col_1', 'Doc0'] = num_of_algorithms_in_col_1
    df_copy.at['num_of_algorithms_in_col_2', 'Doc0'] = num_of_algorithms_in_col_2
    df_copy.at['num_of_formulas', 'Doc0'] = num_of_formulas
    df_copy.at['num_of_formulas_in_col_1', 'Doc0'] = num_of_formulas_in_col_1
    df_copy.at['num_of_formulas_in_col_2', 'Doc0'] = num_of_formulas_in_col_2
    df_copy.at['num_of_figures_in_col_1', 'Doc0'] = num_of_figures_in_col_1
    df_copy.at['num_of_figures_in_col_2', 'Doc0'] = num_of_figures_in_col_2
    df_copy.at['num_of_tables_in_col_1', 'Doc0'] = num_of_tables_in_col_1
    df_copy.at['num_of_tables_in_col_2', 'Doc0'] = num_of_tables_in_col_2
    df_copy.at['last_element', 'Doc0'] = last_object_index
    df_copy.at['sum_space_taken', 'Doc0'] = sum_space_taken
    df_copy.at['sum_open_space', 'Doc0'] = sum_open_space
    df_copy.at['sum_space_taken_by_figures', 'Doc0'] = sum_space_taken_by_figures
    df_copy.at['sum_space_taken_by_tables', 'Doc0'] = sum_space_taken_by_tables
    df_copy.at['sum_of_chars_across_doc', 'Doc0'] = sum_of_chars_across_doc
    df_copy.at['sum_of_words_from_pars', 'Doc0'] = sum_of_words_from_pars
    df_copy.at['sum_of_chars_from_pars', 'Doc0'] = sum_of_chars_from_pars
    df_copy.at['avg_num_of_words_from_pars', 'Doc0'] = avg_num_of_words_from_pars
    df_copy.at['avg_num_of_chars_from_pars', 'Doc0'] = avg_num_of_chars_from_pars
    df_copy.at['num_of_paragraphs_with_1_word_at_the_end', 'Doc0'] = num_of_paragraphs_with_1_word_at_the_end
    df_copy.at['num_of_figures_with_captions', 'Doc0'] = num_of_figures_with_captions
    df_copy.at['num_of_tables_with_captions', 'Doc0'] = num_of_tables_with_captions
    if (new_ending_y < df_copy.at['ending_y_of_doc', 'Doc0']):
        df_copy.at['ending_y_of_doc', 'Doc0'] = new_ending_y

    # df_copy = df_copy.T
    # df_copy.to_csv('pdf_extraction\\adi_comparing\\new_files\\example_test_for_me_1_4_2023_2.csv')
    # sys.exit()
    return new_dct_of_elements_in_order,count_dict_of_elements,summative_features,df_copy

if __name__ == "__main__":
    # df = feature_extraction.run_feature_extraction(['lidor_test_2','lidor_test_3'],['lidor_test_2','lidor_test_3'],['bibliography','bibliography'])
    df,summative_features,dct_of_elements_in_order,count_dict_of_elements = feature_extraction_for_search_algorithm.run_feature_extraction(['TestingGroundsForMe'], ['TestingGroundsForMe'],['bibliography'])
    # df is the dataframe pre transposed, now we will need to duplicate each column times the files_created at the index of the doc
    # for example if we have doc0 , we will duplicate it for the length of files_created[0] (which is len(files_created[0]) (doc 1 is the first doc, so first element in the files_created[0]
    # first we will need to compile the new tex files in files_created (for example, files_created[0][0] is a tex file)
    # after compiling we will use the pdf extraction to get the new y of the page and then we can compare it with the doc it was created from
    #write to csv:

    df = df.T #no need for it yet. might need it at the end ------------------------

    print(df)
    df.to_csv('pdf_extraction\\adi_comparing\\new_files\\example_test_for_me_1_4_2023_1.csv')
    df = df.T  # no need for it yet. might need it at the end ------------------------
    #sys.exit()
    print(summative_features)
    print(dct_of_elements_in_order)
    print(count_dict_of_elements)
    base_df = df.copy(deep=True)
    dict_based_tree_levels = {} #each key in this dict, will be a tree (search space) level (depth level) and the values will be a list of tuples which represent (pred,confidance,df_copy), df_copy is the new df after

    node_id = 2
    for depth in range(1,5):
        #testing for vpsace:
        dict_based_tree_levels[depth] = []
        counter = 0
        found_enum = False
        key_1 = 0
        key_2 = 0
        for key in dct_of_elements_in_order.keys(): #preforming vspace on all elements
            if(counter == len(dct_of_elements_in_order.keys())-1):
                break
            value = dct_of_elements_in_order[key]
            #vspace has 4 options so we will iterate 4 times:
            for iteration in range(1,5):
                df_copy = base_df.copy(deep=True)
                prediction,confidance,type,value_of_operator,object_used_on,num_of_object,df_copy = simulating_vspace_for_prediction(value,key,iteration,df_copy)
                if(prediction == -1 and confidance == -1 and df_copy == -1):
                    continue
                dict_based_tree_levels[depth].append((prediction,confidance,type,value_of_operator,object_used_on,num_of_object,df_copy,node_id))
                node_id+=1
            #figure and table have 5 sizes
            if(key.startswith('Figure')):
                for iteration in range(0,5):
                    df_copy = base_df.copy(deep=True)
                    prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy = simulating_figure_reduction_for_prediction(value, key, iteration, df_copy)
                    if (prediction == -1 and confidance == -1 and df_copy == -1):
                        continue
                    dict_based_tree_levels[depth].append((prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy,node_id))
                    node_id+=1
            #table have 4 sizes:
            if(key.startswith('Table')):
                for iteration in range(0,4):
                    df_copy = base_df.copy(deep=True)
                    prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy = simulating_table_reduction_for_prediction(value, key, iteration, df_copy)
                    if (prediction == -1 and confidance == -1 and df_copy == -1):
                        continue
                    dict_based_tree_levels[depth].append((prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy,node_id))
                    node_id+=1
            if (key.startswith('Algorithm')):
                for iteration in range(0, 1):
                    df_copy = base_df.copy(deep=True)
                    prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy = simulating_algo_reduction_for_prediction(value, key, iteration, df_copy)
                    if (prediction == -1 and confidance == -1 and df_copy == -1):
                        continue
                    dict_based_tree_levels[depth].append(
                        (prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy,node_id))
                    node_id+=1
            if(found_enum and key.startswith('Enum')): #good if there is no seperate enums, which makes no sense but yeah
                continue
            if (key.startswith('Enum')):
                found_enum = True
                for iteration in range(0, 1):
                    df_copy = base_df.copy(deep=True)
                    prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy = simulating_enum_operator_for_prediction(value, key, iteration, df_copy)
                    if (prediction == -1 and confidance == -1 and df_copy == -1):
                        continue
                    dict_based_tree_levels[depth].append((prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy,node_id))
                    node_id+=1
            if (key.startswith('Paragraph')):
                for iteration in range(0, 1):
                    df_copy = base_df.copy(deep=True)
                    prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy = simulating_paragraph_tag_operator_for_prediction(value, key, iteration, df_copy)
                    if (prediction == -1 and confidance == -1 and df_copy == -1):
                        continue
                    dict_based_tree_levels[depth].append(
                        (prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy,node_id))
                    node_id+=1
            new_key_for_par = ''.join(i for i in key if not i.isdigit())
            if (new_key_for_par == 'Par'):
                if(key_1 == 0): #we didnt find a par
                    key_1 = key
                    continue
                elif(key_1 != 0 and key_2 == 0): #found 1 par, now need the 2nd so we can combine them
                    key_2 = key
                    for iteration in range(0, 1):
                        df_copy = base_df.copy(deep=True)
                        prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy = simulating_combine_paragraphs_for_prediction(
                            value, key_1,key_2, iteration, df_copy)
                        if (prediction == -1 and confidance == -1 and df_copy == -1):
                            continue
                        dict_based_tree_levels[depth].append(
                            (prediction, confidance, type, value_of_operator, object_used_on, num_of_object, df_copy,node_id))
                        node_id+=1
                    key_1 = key
                    key_2 = 0
            else:
                key_1 = 0
                key_2 = 0

            counter+=1
            
            print(df)
        #after finding out the best operator to use, based on prediction and confidance, we will now simulate performing this operator:
        #we will assume that vpsace with 1 is the chosen one:
        #print("here")
        for node in dict_based_tree_levels[depth]:
            #current_df = 
            print(node)
            if node[2] == 1:
                print("here")#
                print(node)
                dct_of_elements_in_order1,count_dict_of_elements,summative_features1,df_copy = simulating_using_vspace(node[3],node[4],node[5],node[6],summative_features,dct_of_elements_in_order)

            # elif node[2] == 2:
            #     simulating_using_figure_reduction(node[3],node[4],node[5],node[6],summative_features,dct_of_elements_in_order)
        
            # elif node[2] == 3:
            #     simulating_using_algorithm_reduction(node[3],node[4],node[5],node[6],summative_features,dct_of_elements_in_order)
        
            # elif node[2] == 4:
            #     simulating_using_enum_operator(node[3],node[4],node[5],node[6],summative_features,dct_of_elements_in_order,count_dict_of_elements)

            # elif node[2] == 5:
            #     simulating_using_paragraph_tag_removal_operator(node[3],node[4],node[5],node[6],summative_features,dct_of_elements_in_order,count_dict_of_elements)
        
            # elif node[2] == 6:
            #     simulating_using_combining_pars_operator(node[3],node[4],node[5],node[6],summative_features,dct_of_elements_in_order,count_dict_of_elements)
        
            # elif node[2] == 7:
            #     simulating_using_table_reduction(node[3],node[4],node[5],node[6],summative_features,dct_of_elements_in_order)

            # else:
            #     print("not found")
        
        
        

        # print(dict_based_tree_levels)
        # sys.exit()


        # print(dct_of_elements_in_order)
        # print()
        # print(count_dict_of_elements)
        # print()
        # print(summative_features)
        # print()
        # print(df_copy)
        print()
        #print(dict_based_tree_levels[depth][4][6].equals(df_copy))
            

        #print(dict_based_tree_levels[1])
        #break


        sys.exit()


    #read df from csv






