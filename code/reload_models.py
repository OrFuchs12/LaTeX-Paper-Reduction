import os
import pickle
import re
import sys
import numpy as np
from catboost import CatBoostRegressor


def load_regression_models_hist(dir):
    #Load models
    models = {}
    directory = dir
    for file in os.scandir(directory):
        if file.is_file():
            n = re.findall('\d+\.?\d*', file.name)
            if n[0] == '1':
                i = (n[0], n[4], n[5], n[6])
            else:
                i = (n[0], n[4], n[5])
            
            file_path = directory + '/' + file.name
            
            with open(file_path, 'rb') as f:
                clf = pickle.load(f)

            print(i)
            models[i] = clf

    print("total models in memory:", len(models))
    return models


def load_regression_models_cat(dir):
    #Load models
    models = {}
    directory = dir
    #print(directory)
    for file in os.scandir(directory):
        if file.is_file():
            n = re.findall('\d+\.?\d*', file.name)
            if n[0] == '1':
                i = (n[0], n[4], n[5], n[6])
            else:
                i = (n[0], n[4], n[5])
            
            file_path = directory + '/' + file.name
            clf = CatBoostRegressor()
            clf.load_model(file_path)
            print(i)
            #print(file_path)
            models[i] = clf

            
    print("total models in memory:", len(models))
    return models


#load_regression_models_hist("pdf_extraction\\adi_comparing\\regression_models_hist")
#load_regression_models_cat("pdf_extraction\\adi_comparing\\regression_models_cat")


