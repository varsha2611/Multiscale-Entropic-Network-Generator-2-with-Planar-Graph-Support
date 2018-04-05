import networkx as nx
from networkx.algorithms.community import kernighan_lin_bisection
#from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import math

def recursive_partition(G,all_partitions,levels):
    if len(all_partitions)>0 and math.log(len(all_partitions),2) >= levels:
        return all_partitions
    print("nodes in original",len(G.nodes()))
    partitions = kernighan_lin_bisection(G, partition=None, max_iter=10, weight='weight')
    pos = nx.nx_pydot.graphviz_layout(G, prog='neato')
    nx.draw(G, pos, with_labels=False, node_size=10)
    plt.show()
    print("nb_of_partitions",len(partitions))
    print("nodes in 1", len(partitions[0]))
    print("nodes in 2", len(partitions[1]))
    all_partitions.append(partitions[0])
    all_partitions.append(partitions[1])
    G_1 = nx.Graph()
    G_2 = nx.Graph()
    for edge in G.edges():
        if edge[0] and edge[1] in partitions[0]:
            G_1.add_edge(edge[0], edge[1])
        else:
            G_2.add_edge(edge[0], edge[1])
    if (len(G_1.edges()) > 10):
        all_partitions = recursive_partition(G_1,all_partitions=all_partitions,levels=levels)
    print(len(all_partitions))
    if(len(G_2.edges())>10):
        all_partitions = recursive_partition(G_2, all_partitions=all_partitions,levels=levels)
    print(len(all_partitions))
    return all_partitions

def find_partitions():
    G = nx.read_edgelist('temp_graph.edges')
    file = open('temp_nb_of_tanks')
    for fulline in file:
        # Network Components
        values = fulline.split()
    nb_of_tanks = int(values[0])
    print(nb_of_tanks)
    while len(all_partitions)<2^nb_of_tanks:
        partitions =kernighan_lin_bisection(G, partition = None, max_iter=10, weight='weight')
        all_partitions.append(partitions[0])
        all_partitions.append(partitions[1])
        G_1 = nx.Graph()
        G_2 = nx.Graph()
        for edge in G.edges():
            if edge[0] and edge[1] in partitions[0]:
                G_1.add_edge(edge[0],edge[1])
            elif edge[0] and edge[1] in partitions[1]:
                G_2.add_edge(edge[0],edge[1])
        partitions = kernighan_lin_bisection(G_1,partition = None, max_iter=10, weight='weight')
        all_partitions.append(partitions[0])
        all_partitions.append(partitions[1])
        partitions = kernighan_lin_bisection(G_2, partition=None, max_iter=10, weight='weight')
        all_partitions.append(partitions[0])
        all_partitions.append(partitions[1])

def finding_partitions():
    G = nx.read_edgelist('temp_graph.edges')
    file = open('temp_nb_of_tanks')
    for fulline in file:
        # Network Components
        values = fulline.split()
    nb_of_tanks = int(values[0])
    print(nb_of_tanks)
    all_partitions = []
    recursive_partition(G,all_partitions,2)
    print(len(all_partitions))




finding_partitions()


