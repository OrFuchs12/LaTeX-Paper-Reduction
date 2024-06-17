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

def compare_csv_files(file1, file2):
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Filter rows where `reduced` is False in df1 and True in df2
    df1_filtered = df1[df1['reduced'] == False]
    df2_filtered = df2[df2['reduced'] == True]
    
    merged_df = pd.merge(df1_filtered, df2_filtered, on='docName')
    cols_to_keep = ['docName', 'compilations_x', 'compilations_y', 'reduced_x', 'reduced_y']
    return merged_df[cols_to_keep]




def find_non_readable():
    for df in dfs:
        #print all rows with compilations greater than 5
        tmp = df[df['compilations'] > 5]
        for row in tmp.iterrows():
            print(row)


# find_non_readable()
print(compare_csv_files("code/~/results/excels/results7.csv", "code/~/results/excels/results5.csv"))
    


