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

dfs = [pd.read_csv(os.path.join(current_directory, csv_directory, file)) for file in file_paths]
# print(len(dfs[0]))
# for df in dfs:
#     df['Reduced'] = df['Reduced'].astype(int) * len(df)
#     # Extract unique "Name" values from each DataFrame
#     names = set(df[df['Reduced'].astype(bool)]['Name'])
#     # If it's the first DataFrame, initialize the common_names set
#     if common_names is None:
#         common_names = names
#         intersection_len = len(common_names)
#     else:
#         # Take intersection to find common "Name" values across all DataFrames
#         common_names = common_names.intersection(names)
#         intersection_len = len(common_names)


# for df in dfs:
#     del df['Algorithm']

# means = {}
# for df, file_path in zip(dfs, file_paths):
#     file_name = os.path.basename(file_path).split('.')[0]
#     #tmp df without name
#     tmp_df = df.drop(columns=['Name'])
#     means[file_name] = tmp_df.mean()

# modified_means = {}
# for key, value in means.items():
#     new_key = key.replace('files_', '').replace('_', ' ')
#     modified_means[new_key] = value

# means_df = pd.DataFrame(modified_means)
# summary_stats = means_df.describe()
# means_df.to_csv('code/~/results/code/greedy_from_machine/means.csv')
# print('means csv file created! ')

# reduced_means = {}
# for key, df in zip(means.keys(), dfs):
#     reduced_df = df[df['Reduced'].astype(bool)] 
#     tmp_reduced_df = reduced_df.drop(columns=['Name'])
#     reduced_means[key] = tmp_reduced_df.mean()

# modified_reduced_means = {}
# for key, value in reduced_means.items():
#     new_key = key.replace('files_', '').replace('_', ' ')
#     modified_reduced_means[new_key] = value

# for key in modified_means.keys():
#     modified_reduced_means[key]['Reduced'] = modified_means[key]['Reduced']
# reduced_means_df = pd.DataFrame(modified_reduced_means)

# reduced_means_df.to_csv('code/~/results/code/greedy_from_machine/reduced_means.csv')
# print('Reduced Means CSV file created!')


# reduced_rows = []
# for df in dfs:
#     reduced_rows.append(set(df[df['Reduced'].astype(bool)].index))


# # Filter rows where "Name" is in common_names for each DataFrame
# common_rows = {}
# for df, file_path in zip(dfs, file_paths):
#     # Filter rows where "Name" is in common_names
#     common_rows[file_path] = df[df['Name'].isin(common_names)]

# intersection_means = {}
# for file_path, common_df in common_rows.items():
#     # Calculate mean for the common rows in each DataFrame
#     tmp_common_df = common_df.drop(columns=['Name'])
#     intersection_means[file_path] = tmp_common_df.mean()

# modified_intersection_means = {}
# for key, value in intersection_means.items():
#     file_name = os.path.basename(key).split('.')[0]
#     new_key = file_name.replace('files_', '').replace('_', ' ')
#     modified_intersection_means[new_key] = value

# for key in modified_means.keys():
#     modified_intersection_means[key]['Reduced'] = intersection_len
# intersection_means_df = pd.DataFrame(modified_intersection_means)

# intersection_means_df.to_csv('code/~/results/code/greedy_from_machine/intersection_means.csv')
# print('Intersection Means CSV file created!')

# plt.figure(figsize=(10, 6))
# means_df.plot(kind='bar', rot=45, ax=plt.gca())
# plt.title('Comparison of Algorithms')
# plt.xlabel('Criterion')
# plt.ylabel('Value')
# plt.legend(title='Algorithm')
# plt.tight_layout()
# plt.show()

def find_not_reduced_at_all():
   # find the intersection of all the rows that reduced == false in all the dataframes 
    not_reduced = dfs[0][dfs[0]['Reduced'] == False]
    for df in dfs[1:]:
        not_reduced = not_reduced[not_reduced['Name'].isin(df[df['Reduced'] == False]['Name'])]
    return not_reduced
       
   

print(find_not_reduced_at_all())
