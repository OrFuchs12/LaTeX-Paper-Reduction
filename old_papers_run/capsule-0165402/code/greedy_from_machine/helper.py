# from xgboost import XGBClassifier

# from sklearn.model_selection import train_test_split

# from sklearn import metrics
import pandas as pd



# def simpleModel(path, estimator, target, to_drop=None):
#     print("here")
#     df = pd.read_csv(path) 
#     df = df.head(1000)

#     df.fillna(df.mean(numeric_only=True), inplace=True) #replace missing values with mean of the feature
#     X = df.drop(columns=[target], axis=1) #create a dataframe with all training data except the target column
#     y = df[target].values #separate target values
#     if to_drop:
#         X.drop(columns=[col for col in to_drop], axis=1, inplace=True) #remove inappropriate features
    
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

   
#     estimator = estimator.fit(X_train, y_train)

#     y_pred = estimator.predict(X_test)

#     print("\t\t---Before Optimization---")
#     print("\t\tMSE: ",metrics.accuracy_score(y_test, y_pred))

    

# simpleModel(path='pdf_extraction\\adi_comparing\\concatted.csv', estimator=XGBClassifier(), target='binary_class', to_drop=['Unnamed: 0.1', 'herustica', 'lines_we_gained', 'y_gained'])



# path1 = "C:\\Users\\user\\Desktop\\results_simple_greedy.csv"
# path2 = "C:\\Users\\user\\Desktop\\results_heuristic_greedy.csv"
# path3 = "C:\\Users\\user\\Desktop\\results_model_greedy.csv"
# df1 = pd.read_csv(path1) 
# df2 = pd.read_csv(path2) 
# df3 = pd.read_csv(path3) 

# df = df1.merge(df2, on='Name')
# df = df.merge(df3, on='Name')


# df.to_csv('C:\\Users\\user\\Desktop\\new_finals.csv', index=False) #change here
#print(df)

df = pd.read_csv('C:\\Users\\user\\Desktop\\new_finals.csv') 


df = df[df.Reduced == True]

print(df)

df.to_csv('C:\\Users\\user\\Desktop\\new_finals2.csv', index=False) #change here
