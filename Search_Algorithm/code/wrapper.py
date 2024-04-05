import sklearn

import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path
import pickle
import greedy
import pdfMiner_new_checking_length, read_single_file
import time
import features_single
from time import sleep
from pathlib import Path
import search_algorithms_for_experiment
import reload_models
import new_experiment_inferstructure

import main

def results(path_for_docs, path_for_write_csv, from_doc, to_doc, type_of_experiment, operators_max, helper_directory,bibliograph_path):
    """
    Run experiments on all documents in path_for_docs
    :param path_for_docs: directory of tex files and their corresponding pdf
    :param path_for_write_csv: path to write the results csv file
    :param from_doc: beggining
    :param to_doc:
    :param type_of_experiment:
    :param operators_max:
    :param helper_directory:
    :return:
    """

    my_file = Path(path_for_write_csv)

    files_created = []
    results_data = []
    names = []
    for file in os.scandir(path_for_docs):
        if file.is_file():
            fname = file.name.split('.')[0]
            if fname not in names:
                names.append(fname)

    idx = 0
    if type_of_experiment.find("search") != -1:
        models_path_cat = "/sise/home/toris/latex_files/creating_batches/modelling/second_exp/regression_models"
        models = reload_models.load_regression_models_cat(models_path_cat)
    else:
        models = greedy.load_models()

    for filename in names[from_doc:to_doc]:
        try:
            results_data.append(main.results(
                results(path_for_docs, path_for_write_csv, filename, type_of_experiment, operators_max,
                        helper_directory,models,bibliograph_path)))
            results_df = pd.DataFrame.from_records(results_data)
            results_df.to_csv(path_for_write_csv, index=False)
        except Exception as e:
            print(e)
            continue
