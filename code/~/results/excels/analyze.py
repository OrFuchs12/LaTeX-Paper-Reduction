import pandas as pd
import os
import matplotlib.pyplot as plt

current_directory = os.getcwd()

csv_directory = "code/~/results/excels"

# intersection_rows = list(set.intersection(*reduced_rows))
# Initialize an empty set to store common "Name" values
common_names = None

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
print(len(dfs[0]))
for df in dfs:
    df['reduced'] = df['reduced'].astype(int) * len(df)
    # Extract unique "Name" values from each DataFrame
    names = set(df[df['reduced'].astype(bool)]['docName'])
    # If it's the first DataFrame, initialize the common_names set
    if common_names is None:
        common_names = names
        intersection_len = len(common_names)
    else:
        # Take intersection to find common "Name" values across all DataFrames
        common_names = common_names.intersection(names)
        intersection_len = len(common_names)


for df in dfs:
    del df['experiment_type']

means = {}
for df, file_path in zip(dfs, file_paths):
    file_name = os.path.basename(file_path).split('.')[0]
    #tmp df without name
    tmp_df = df.drop(columns=['docName', 'original_height','last_page_height','gained'])
    means[file_name] = tmp_df.mean()

modified_means = {}
for key, value in means.items():
    new_key = key.replace('files_', '').replace('_', ' ')
    modified_means[new_key] = value

means_df = pd.DataFrame(modified_means)
summary_stats = means_df.describe()
means_df.to_csv('code/~/results/excels/means.csv')
print('means csv file created! ')

reduced_means = {}
for key, df in zip(means.keys(), dfs):
    reduced_df = df[df['reduced'].astype(bool)] 
    tmp_reduced_df = reduced_df.drop(columns=['docName', 'original_height','last_page_height','gained'])
    reduced_means[key] = tmp_reduced_df.mean()

modified_reduced_means = {}
for key, value in reduced_means.items():
    new_key = key.replace('files_', '').replace('_', ' ')
    modified_reduced_means[new_key] = value

for key in modified_means.keys():
    modified_reduced_means[key]['reduced'] = modified_means[key]['reduced']
reduced_means_df = pd.DataFrame(modified_reduced_means)

reduced_means_df.to_csv('code/~/results/excels/reduced_means.csv')
print('Reduced Means CSV file created!')


reduced_rows = []
for df in dfs:
    reduced_rows.append(set(df[df['reduced'].astype(bool)].index))


# Filter rows where "Name" is in common_names for each DataFrame
common_rows = {}
for df, file_path in zip(dfs, file_paths):
    # Filter rows where "Name" is in common_names
    common_rows[file_path] = df[df['docName'].isin(common_names)]

intersection_means = {}
for file_path, common_df in common_rows.items():
    # Calculate mean for the common rows in each DataFrame
    tmp_common_df = common_df.drop(columns=['docName', 'original_height','last_page_height','gained'])
    intersection_means[file_path] = tmp_common_df.mean()

modified_intersection_means = {}
for key, value in intersection_means.items():
    file_name = os.path.basename(key).split('.')[0]
    new_key = file_name.replace('files_', '').replace('_', ' ')
    modified_intersection_means[new_key] = value

for key in modified_means.keys():
    modified_intersection_means[key]['reduced'] = intersection_len
intersection_means_df = pd.DataFrame(modified_intersection_means)

intersection_means_df.to_csv('code/~/results/excels/intersection_means.csv')
print('Intersection Means CSV file created!')

plt.figure(figsize=(10, 6))
means_df.plot(kind='bar', rot=45, ax=plt.gca())
plt.title('Comparison of Algorithms')
plt.xlabel('Criterion')
plt.ylabel('Value')
plt.legend(title='Algorithm')
plt.tight_layout()
plt.show()