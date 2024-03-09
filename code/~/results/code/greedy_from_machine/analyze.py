import pandas as pd
import os
import matplotlib.pyplot as plt

current_directory = os.getcwd()

csv_directory = "code/~/results/code/greedy_from_machine"

file_paths = [
    "files_results_simple_greedy.csv",
    "files_results_heuristic_greedy.csv",
    "files_results_non_stop_heuristic_greedy.csv",
    "files_results_model_greedy.csv",
    "files_non_stop_results_classification_greedy.csv",
    "files_results_regreession_model_greedy.csv",
    "files_results_non_stop_regreession_model_greedy.csv",
    "files_results_classification_regreession_model_greedy.csv",
    "files_results_classification_regreession_v2_model_greedy.csv"
]

dfs = [pd.read_csv(os.path.join(current_directory, csv_directory, file)) for file in file_paths]
print(len(dfs[0]))
for df in dfs:
    df['Reduced'] = df['Reduced'].astype(int) * len(df)

for df in dfs:
    del df['Algorithm']
    del df['Name']

means = {}
for df, file_path in zip(dfs, file_paths):
    file_name = os.path.basename(file_path).split('.')[0]
    means[file_name] = df.mean()

modified_means = {}
for key, value in means.items():
    new_key = key.replace('files_', '').replace('_', ' ')
    modified_means[new_key] = value

means_df = pd.DataFrame(modified_means)
summary_stats = means_df.describe()
means_df.to_csv('code/~/results/code/greedy_from_machine/means.csv')
print('means csv file created! ')

reduced_means = {}
for key, df in zip(means.keys(), dfs):
    reduced_df = df[df['Reduced'].astype(bool)] 
    reduced_means[key] = reduced_df.mean()

modified_reduced_means = {}
for key, value in reduced_means.items():
    new_key = key.replace('files_', '').replace('_', ' ')
    modified_reduced_means[new_key] = value

for key in modified_means.keys():
    modified_reduced_means[key]['Reduced'] = modified_means[key]['Reduced']
reduced_means_df = pd.DataFrame(modified_reduced_means)

reduced_means_df.to_csv('code/~/results/code/greedy_from_machine/reduced_means.csv')
print('Reduced Means CSV file created!')


reduced_rows = []
for df in dfs:
    reduced_rows.append(set(df[df['Reduced'].astype(bool)].index))

intersection_rows = list(set.intersection(*reduced_rows))

intersection_means = {}
for df, file_path in zip(dfs, file_paths):
    reduced_df = df.loc[intersection_rows]  
    intersection_means[file_path] = reduced_df.mean()

modified_intersection_means = {}
for key, value in intersection_means.items():
    file_name = os.path.basename(key).split('.')[0]
    new_key = file_name.replace('files_', '').replace('_', ' ')
    modified_intersection_means[new_key] = value

for key in modified_means.keys():
    modified_intersection_means[key]['Reduced'] = len(intersection_rows)
intersection_means_df = pd.DataFrame(modified_intersection_means)

intersection_means_df.to_csv('code/~/results/code/greedy_from_machine/intersection_means.csv')
print('Intersection Means CSV file created!')

plt.figure(figsize=(10, 6))
means_df.plot(kind='bar', rot=45, ax=plt.gca())
plt.title('Comparison of Algorithms')
plt.xlabel('Criterion')
plt.ylabel('Value')
plt.legend(title='Algorithm')
plt.tight_layout()
plt.show()