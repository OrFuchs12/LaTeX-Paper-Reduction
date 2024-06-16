import pandas as pd
import os


current_directory = os.getcwd()

csv_directory = "code/~/results/excels"

file_paths = [
    "results0.csv",
    "results1.csv",
    "results2.csv",
    "results3.csv",
    "results4.csv",
    "results5.csv",
    "results6.csv",
    "results7.csv"
]

dfs = [pd.read_csv(os.path.join(current_directory, csv_directory, file)) for file in file_paths]

def not_in_intersection(file1, file2):
    """
    Returns the rows of df1 that are not in the intersection of df1 and df2
    """
    with open(file1, 'r') as f:
        df1 = pd.read_csv(f)
    with open(file2, 'r') as f:
        df2 = pd.read_csv(f)
    #find all rows not in intersection of col docName
    not_in_intersection = df1[~df1['docName'].isin(df2['docName'])]
    return not_in_intersection


def find_non_readable():
    for df in dfs:
        #print all rows with compilations greater than 5
        tmp = df[df['compilations'] > 5]
        for row in tmp.iterrows():
            print(row)


find_non_readable()
# print(not_in_intersection("code/~/results/excels/results6.csv", "code/~/results/excels/results7.csv"))
    


