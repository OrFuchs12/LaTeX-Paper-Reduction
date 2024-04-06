import feature_extraction
import get_pdf_order
import using_operators
import using_operators_for_adi
import re
import pickle
import read_single_file
import os
import time
import sys

if __name__ == "__main__":
    #df = feature_extraction.run_feature_extraction(['lidor_test_2','lidor_test_3'],['lidor_test_2','lidor_test_3'],['bibliography','bibliography'])
    df = feature_extraction.run_feature_extraction(['5067_1','5067_2'], ['5067_1','5067_2'],['bibliography','bibliography'])
    #df is the dataframe pre transposed, now we will need to duplicate each column times the files_created at the index of the doc
    #for example if we have doc0 , we will duplicate it for the length of files_created[0] (which is len(files_created[0]) (doc 1 is the first doc, so first element in the files_created[0]
    #first we will need to compile the new tex files in files_created (for example, files_created[0][0] is a tex file)
    #after compiling we will use the pdf extraction to get the new y of the page and then we can compare it with the doc it was created from

    old_columns_list = list(df)
    index_doc_for_operators = 0
    files_created = []
    for column in old_columns_list:
        with open('dct' + str(index_doc_for_operators), 'rb') as dct_file:
            dct = pickle.load(dct_file)
        with open('latex_path'+str(index_doc_for_operators),'rb') as latex_path_file:
            latex_path = pickle.load(latex_path_file)
        with open('bib_path'+str(index_doc_for_operators),'rb') as bib_path_file:
            bib_path = pickle.load(bib_path_file)
        files_created_small = using_operators_for_adi.perform_operators(dct,index_doc_for_operators,latex_path,bib_path)
        files_created.append(files_created_small)
        index_doc_for_operators += 1
    index_of_new_doc = 0
    index_doc = 0
    #compiling all the new files:
    # for idd in range(len(files_created)):
    #     for j in files_created[idd]:
    #         cmd_line_act = '"C:\\Users\\lidor\\tectonic.exe" ' + j[0]
    #         os.system(cmd_line_act)
    #         time.sleep(2)
    for column in old_columns_list:
        old_y = df.at['ending_y_of_doc',column]
        binary = 0
        print(files_created)
        for i in files_created[index_doc]: #[(filename,pdfname,object,vspace(operator),vspace(operator)value)]
            #becasue this is only for vspace so we will name him 1
            df['doc' + str(index_doc)+'_with_operator' + str(index_of_new_doc)] = df.loc[:, column] #create a new column
            if(i[3] == 'vspace'):
                df.at['type','doc' + str(index_doc)+'_with_operator' + str(index_of_new_doc)] = 1 #switch to i[3] when it is all set
            elif(i[3] == 'change_figure_size'):
                df.at['type', 'doc' + str(index_doc) + '_with_operator' + str(index_of_new_doc)] = 2  # switch to i[3] when it is all set
            df.at['value', 'doc' + str(index_doc)+'_with_operator' + str(index_of_new_doc)] = i[4]
            df.at['object_used_on', 'doc' + str(index_doc)+'_with_operator' + str(index_of_new_doc)] = i[2]
            df.at['num_of_object', 'doc' + str(index_doc)+'_with_operator' + str(index_of_new_doc)] = re.findall(r'\d+', str(i[2]))[0]
            index = 0
            x = get_pdf_order.order('C:\\Users\\lidor\\OneDrive\\Desktop\\Overleaf_project\\pdf_extraction\\adi_comparing\\'+i[1])
            pages = len(x.keys())
            #print(x)
            for key,value in x.items():
                if(index == len(x)-1):
                    for array_of_tuples in value:
                        for index_tuple in range(len(array_of_tuples)):
                            if(index_tuple == len(array_of_tuples)-1):
                                end_y = array_of_tuples[index_tuple][0][1]
                    index+=1
                index+=1
            print(x)
            #print("OLD END Y ------------------------")
            print(end_y)
            #print("NEW END Y ------------------------")
            #print(read_single_file.order('C:\\Users\\lidor\\OneDrive\\Desktop\\Overleaf_project\\pdf_extraction\\adi_comparing\\'+i[1]))
            if(pages == 1):
                y_gained = 0
                y_gained += old_y-50
                y_gained += 704-end_y
            else:
                y_gained = old_y - end_y

            if (y_gained > 0):
                binary = 1
                lines_we_get = int(y_gained / 10)
            else:
                binary = 0
                lines_we_get = 0
                #we can change y_gained to 0 if we dont negative numbers
            df.at['y_gained', 'doc' + str(index_doc)+'_with_operator' + str(index_of_new_doc)] = y_gained
            df.at['lines_we_gained', 'doc' + str(index_doc)+'_with_operator' + str(index_of_new_doc)] = lines_we_get
            df.at['binary_class', 'doc' + str(index_doc)+'_with_operator' + str(index_of_new_doc)] = binary
            index_of_new_doc += 1
        index_doc += 1
        df = df.drop(column, axis=1)

    df2 = df.T
    df2.to_csv('example.csv')

        # x = get_pdf_order.order('C:\\Users\\lidor\\Desktop\\FINAL PROJECT - OVERLEAF\\30.10.22\\Overleaf_project\\pdf-tests\\lidor_test_2.pdf')
        # print(x)
