import os
import time
import networkx as nx
import pickle
import sys
import reload_models
import new_experiment_inferstructure

counter_of_zero = 0

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
                if neighbor[0]>0:
                    edges.append((key, neighbor[7], (alpha * (1/(neighbor[0])))+ ((1-alpha) * neighbor[9]), {'cost': neighbor[9]} ))
                else:
                    edges.append((key, neighbor[7], 1e6, {'cost': neighbor[9]}))
                if len(neighbor[8]) == depth:
                    edges.append((neighbor[7], last_node_id, 0, {'cost': neighbor[9]}))
            
    nodes.append(last_node_id)

    g.add_nodes_from(nodes)
    # g.add_weighted_edges_from(edges)
    for edge in edges:
        g.add_edge(edge[0], edge[1], weight=edge[2], **edge[3])

    return g
    


def dijkstra(g, start, end):
    # print(nx.dijkstra_path(g, start, end))
    # return nx.dijkstra_path(g, start, end)[:-1]
    shortes_list =  k_shortest_paths(g, start, end, 5)
    if shortes_list:
        shortes_list.sort(key=lambda x: x[1])
        return shortes_list[0][0][:-1]
    return None

def bellman_ford(g, start, end):
    return nx.bellman_ford_path(g, start, end)[:-1]

import networkx as nx
import heapq

import networkx as nx

def k_shortest_paths(graph, source, target, k, weight='weight', cost = 'cost'):
    paths = []
    # First, find the shortest path
    path = nx.dijkstra_path(graph, source, target, weight=weight)
    calc_cost = nx.path_weight(graph, path, weight= cost)
    paths.append((path, calc_cost))
    # Initialize the heap to store potential paths
    potential_paths = []
    
    for i in range(1, k):
        for j in range(len(paths[-1][0]) - 1):
            spur_node = paths[-1][0][j]
            root_path = paths[-1][0][:j+1]
            
            # Make a copy of the original graph
            graph_copy = graph.copy()
            
            for path in paths:
                if path[0][:j+1] == root_path:
                    if len(path[0]) > j+1:
                        try:
                            graph_copy.remove_edge(path[0][j], path[0][j+1])
                        except: 
                            continue
            
            for n in range(len(root_path) - 1):
                graph_copy.remove_node(root_path[n])
            
            try:
                spur_path = nx.dijkstra_path(graph_copy, spur_node, target, weight=weight)
                total_path = root_path[:-1] + spur_path
                potential_paths.append((nx.path_weight(graph, total_path, weight=weight), nx.path_weight(graph, total_path, weight= cost), total_path ))
            except nx.NetworkXNoPath:
                continue
        
        if not potential_paths:
            break
        
        potential_paths.sort()
        best_path = potential_paths.pop(0)
        if len(best_path) >=3:
            paths.append((best_path[2], best_path[1]))
        # paths.append((potential_paths.pop(0)[2], potential_paths.pop(0)[1]))
    
    return paths

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

    if not path:
        return None, -1,-1
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