import pandas as pd
import os
import matplotlib.pyplot as plt

current_directory = os.getcwd()

csv_directory = "code/~/results/code/greedy_from_machine"

# intersection_rows = list(set.intersection(*reduced_rows))
# Initialize an empty set to store common "Name" values
common_names = None

file_paths = [
    "files_results_simple_greedy.csv",
    "files_results_heuristic_greedy.csv",
    "files_results_non_stop_heuristic_greedy.csv",
    "files_results_model_greedy.csv",
    "files_non_stop_results_classification_greedy.csv",
    "files_results_regreession_model_greedy.csv",
    "files_results_non_stop_regreession_model_greedy.csv",
    "files_results_classification_regreession_model_greedy.csv",
]

dfs = [
    pd.read_csv(os.path.join(current_directory, csv_directory, file))
    for file in file_paths
]

only_text_papers = []
only_text_papers_false_in_everyone = []
with open("code/greedy_from_machine/text_only.txt", "r") as f:
    # iteriate over the rows of the txt file
    for row in f.readlines():
        only_text_papers.append(row[:-1])

print(only_text_papers)

for i, df in enumerate(dfs):
    only_text_papers_count_true = 0
    only_text_papers_count_false = 0
    for index, row in df.iterrows():
        if row["Name"] in only_text_papers:
            if row["Reduced"] == 1:
                only_text_papers_count_true += 1
                if row["Name"] in only_text_papers_false_in_everyone:
                    only_text_papers_false_in_everyone.remove(row["Name"])
            else:
                only_text_papers_false_in_everyone.append(row["Name"])
                only_text_papers_count_false += 1

    print("for df ", file_paths[i])
    print(
        f"Only text papers count true: {round((only_text_papers_count_true/ len(only_text_papers)) * 100, 2)}%"
    )
    print(
        f"Only text papers count false: {round((only_text_papers_count_false/ len(only_text_papers)) * 100, 2)}%"
    )

print("Only text papers false in everyone: " , len(only_text_papers_false_in_everyone))