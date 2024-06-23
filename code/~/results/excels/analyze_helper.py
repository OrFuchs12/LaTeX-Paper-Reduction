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
    for row in merged_df.iterrows():
        print(row)

def find_doc_that_dont_exist(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Find the docNames that are in df1 but not in df2
    docNames1 = set(df1['docName'])
    docNames2 = set(df2['docName'])
    
    docNames_not_in_df2 = docNames1 - docNames2
    docNames_not_in_df1 = docNames2 - docNames1
    
    print("DocNames in df1 but not in df2:")
    print(docNames_not_in_df2)
    print("DocNames in df2 but not in df1:")
    print(docNames_not_in_df1)


def find_non_readable():
    for df in dfs:
        #print all rows with compilations greater than 5
        tmp = df[df['compilations'] > 5]
        for row in tmp.iterrows():
            print(row)


# find_non_readable()
print(find_doc_that_dont_exist("code/~/results/excels/results4.csv", "code/~/results/excels/files_results_model_greedy (5).csv"))
    


