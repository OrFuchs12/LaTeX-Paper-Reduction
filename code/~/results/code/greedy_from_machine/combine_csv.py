import os
import pandas as pd


file_paths = [
    "results_simple_greedy.csv",
    "results_heuristic_greedy.csv",
    "results_non_stop_heuristic_greedy.csv",
    "results_model_greedy.csv",
    "non_stop_results_classification_greedy.csv",
    "results_regreession_model_greedy.csv",
    "results_non_stop_regreession_model_greedy.csv",
    "results_classification_regreession_model_greedy.csv",
]

cwd = os.getcwd()

#create new files with from file_paths in cwd
for file_path in file_paths:
    with open(os.path.join(cwd,file_path), 'w') as f:
        f.write('')


#iterate through directories, find csv files in each directory and concat the csv by its matching name, create a new csv with the same name
directories = 'code/~/results/code/greedy_from_machine/old_results/'
for directory in os.listdir(directories):
    for file in os.listdir(os.path.join(directories, directory)):
        #check if the file in is file paths list
        if file in file_paths:
            #read the file
            df = pd.read_csv(os.path.join(directories, directory, file))
            #add the content to a new file with the same name
            #if file is empty add the header
            if os.stat(file).st_size == 0:
                #write the header without index
                df.to_csv(file, header=True, index=False)
            else:
                df.to_csv(file, mode='a', header=False, index = False)
            
