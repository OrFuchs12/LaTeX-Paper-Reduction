
**Main File**:
1. main.py - receives directory of tex&pdf files.  
For each such document, by calling the function in search or greedy files, we look for best operators to activate. 
In the main.py we will compile each variant and calculate the height of elements on the 2nd page (if exists). 

**feature extraction files, etc**:

we used the same feature extraction files as used in the other capsules, which do the same thing.

the only difference is the feature_extraction_for_search_algorithm.py file which returns more information that is needed to create the search space.


**Search space creation**:

to create the search space we first needed to create the simulations, so that what **new_experiment_inferstructure.py** is for.

in the file we can see that there is a function for each simulation of operator (more info on how we created the simulation and what are the rules we made are in the 'Search Experiment.docx')

after the function there is the function that creates the search space and it is generate_search_graph (function).

and to create the edges with the respective weight (mse*prediction) we created a function (create_dict) to get the mse for each model-operator.

so after creating all these functions we used a "wrapper" function to run it all together which is search_algorithms_for_experiment.py

You can read Word file: 'Search Experiment.docx' for further explanation.


**Models**:

You need to load 2 folders:
One folder for regression models and one folder for classification models. 


**Tex Parsing Files:**

This is a bit different code from the parsing in documents generation. The difference is in main_parsing function. Here we have 2 versions of main_parsing.py and main_parsing2.py. A bit different than each other.