import os
import time
import networkx as nx
import pickle
import sys
import reload_models
import new_experiment_inferstructure


def load_search_dict(path):
    with open(path, 'rb') as f:
        tree = pickle.load(f)
    return tree



def create_graph_networkx(dct, depth):
    g = nx.Graph()

    nodes = []
    edges = []
    last_node_id = len(dct) + 1
    alpha = 1

    for key, value in dct.items():
        nodes.append(key)
        if value:
            for neighbor in value:
                if neighbor[0]>0: #if prediction is 1 then we want to be smallest weight so like prediction is 0
                    edges.append((key, neighbor[7], ((1-alpha) * neighbor[9])))
                else: #if prediction is 0 then we want to be biggest weight so like prediction is 1
                    edges.append((key, neighbor[7], (alpha * (1/(1* neighbor[1])))+ ((1-alpha) * neighbor[9]) ))

                
                if len(neighbor[8]) == depth:
                    edges.append((neighbor[7], last_node_id, 0))

        #else:
            #edges.append((key, last_node_id, 0))
            

    nodes.append(last_node_id)

    g.add_nodes_from(nodes)
    g.add_weighted_edges_from(edges)

    return g
    


def dijkstra(g, start, end):
    #print(nx.dijkstra_path(g, start, end))
    return nx.dijkstra_path(g, start, end)[:-1]


def bellman_ford(g, start, end):
    return nx.bellman_ford_path(g, start, end)[:-1]



def get_operators(tree, path):
    for i in reversed(path):
        if tree[i]:
            for tup in tree[i]:
                if tup[7] == to_remember:
                    operators = tup[8]
                    return operators

        else:
            to_remember = i



def run_search(tree_depth, file_name,last_pages, algorithm_search, models, mse_dct, bib_path, operators_list=None):
    print("generate graph for file:", file_name)
    tree, current_depth = new_experiment_inferstructure.generate_search_graph(tree_depth, file_name, last_pages, models, mse_dct, bib_path, operators_list)
    #tree = load_search_dict('pdf_extraction\\adi_comparing\\files_for_search\\search_dict')
    if not tree :
        return None, -1,-1
    #print(tree)
    if current_depth==0:
        return None, -1,-1
    if current_depth < tree_depth:
        tree_depth = current_depth
    graph = create_graph_networkx(tree, tree_depth)
    path = algorithm_search(graph, start=1, end=len(tree)+1)

    print("weight of edges:")
    for i in range(len(path)-1):
        print(graph.get_edge_data(path[i], path[i+1]))

    operators = get_operators(tree, path)

    return (operators,len(tree),current_depth)
    


if __name__ == "__main__":
    dct =  new_experiment_inferstructure.create_dict()

    # models_path_hist = "pdf_extraction\\adi_comparing\\regression_models_hist"
    # models = reload_models.load_regression_models_hist(models_path_hist)

    models_path_cat = "pdf_extraction\\adi_comparing\\regression_models_cat"
    models = reload_models.load_regression_models_cat(models_path_cat)

    names = set()
    for file in os.scandir("pdf_extraction\\adi_comparing\\files"):
        if file.is_file():
            names.add(file.name.split('.')[0])
    
    for n in names:
        try:
            s_time = time.time()

            result = run_search(tree_depth=4, file_name=n, algorithm_search=dijkstra, models=models, mse_dct=dct)

            print("best operators:", result)
            print("total time:", time.time() - s_time)
            print()

        except Exception as e:
            print(e)
            print()