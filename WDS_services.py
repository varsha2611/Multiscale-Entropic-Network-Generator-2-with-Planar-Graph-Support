import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import forceatlas2
import random
from random import randrange
from random import uniform
import os



def write_inp_file(network_data,output_path):
    file = open(output_path, "w+")

    #write title
    file.write("[TITLE]\n")
    file.write("Generated synthetic network;\n")

    #write junctions
    file.write("\n[JUNCTIONS]\n")
    file.write(";ID\tElev\tDemand\tPattern\n")
    for junction in network_data['JUNCTIONS']:
        file.write('JU'+str(junction)+"\t")
        file.write(str(network_data['ELEVATIONS'][int(junction)])+"\t")
        if network_data['DEMANDS'][int(junction)] < 0:
            network_data['DEMANDS'][int(junction)] = 0
        file.write(str(network_data['DEMANDS'][int(junction)])+"\t")
        #file.write(str(1) + "\t")
        file.write(";\n")

    # write reservoirs
    file.write("\n[RESERVOIRS]\n")
    file.write(";ID\tHead\tPattern\n")
    for reservoir in network_data['RESERVOIRS']:
        file.write('R'+str(reservoir)+"\t")
        file.write(str(280))
        file.write(";\n")

    #write tanks
    file.write("\n[TANKS]\n")
    file.write(";ID\tElevation\tInitLevel\tMinLevel\tMaxLevel\tDiameter\tMinVol\tVolCurve\n")
    for tank in network_data['TANKS']:
        file.write('T'+str(tank)+"\t")
        file.write(str(network_data['ELEVATIONS'][int(tank)])+"\t")
        file.write(";\n")

    #write pipes
    file.write("\n[PIPES]\n")
    file.write(";ID\tNode1\tNode2\tLength\tDiameter\tRoughness\tMinorLoss\tStatus\n")
    idx = 1
    diameters = [3,4,6,8,10,12,14,16,18,20,24,30,36,42,48,54,60,64]
    roughness = [120,130,140]
    #length = 100,3500

    for pipe in network_data['PIPES']:
            file.write("PI" + str(idx)+"\t")
            if pipe[0] in network_data['JUNCTIONS']:
                source = "JU"+str(pipe[0])
            elif pipe[0] in network_data['TANKS']:
                source = "T"+str(pipe[0])
            elif pipe[0] in network_data['RESERVOIRS']:
                source = "T" + str(pipe[0])
            if pipe[1] in network_data['JUNCTIONS']:
                target = "JU"+str(pipe[1])
            elif pipe[1] in network_data['TANKS']:
                target = "T"+str(pipe[1])
            elif pipe[1] in network_data['RESERVOIRS']:
                target = "R" + str(pipe[1])
            file.write(source + "\t" + target + "\t")
            file.write(str(uniform(100,3500))+"\t")
            file.write(str(random.choice(diameters))+"\t")
            file.write(str(random.choice(roughness)) + "\t;\n")
            idx+=1

    # write pumps
    file.write("\n[PUMPS]\n")
    file.write(";ID\tNode1\tNode2\tParameters\n")
    idx=1
    for pump in network_data['PUMPS']:
        file.write("PU" + str(idx) + "\t")
        if pump[0] in network_data['JUNCTIONS']:
            source = "JU"+str(pump[0])
        elif pump[0] in network_data['TANKS']:
            source = "T"+str(pump[0])
        elif pump[0] in network_data['RESERVOIRS']:
            source = "T" + str(pump[0])
        if pump[1] in network_data['JUNCTIONS']:
            target = "JU"+str(pump[1])
        elif pump[1] in network_data['TANKS']:
            target = "T"+str(pump[1])
        elif pump[1] in network_data['RESERVOIRS']:
            target = "R" + str(pump[1])
        file.write(source + "\t" + target + "\t")
        file.write("HEAD 280 \t;\n")
        idx+=1

    #write coordinates
    file.write("\n[COORDINATES]\n")
    file.write(";Node\tX - Coord\tY - Coord\n")
    for junction, position in zip(network_data['JUNCTIONS'], network_data['COORDINATES']):
        file.write("JU"+str(junction))
        file.write("\t" + str(network_data['COORDINATES'][junction][0]) + "\t" + str(network_data['COORDINATES'][junction][1]) + "\n")
    for reservoir, position in zip(network_data['RESERVOIRS'], network_data['COORDINATES']):
        file.write("R"+str(reservoir))
        file.write("\t" + str(network_data['COORDINATES'][reservoir][0]) + "\t" + str(network_data['COORDINATES'][reservoir][1]) + "\n")
    for tank, position in zip(network_data['TANKS'], network_data['COORDINATES']):
        file.write("T"+str(tank))
        file.write("\t" + str(network_data['COORDINATES'][tank][0]) + "\t" + str(network_data['COORDINATES'][tank][1]) + "\n")

    file.write("\n[VALVES]\n")
    file.write(";ID\tNode1\tNode2\tDiameter\tType\tSetting\tMinorLoss\n")
    file.write("\n[TAGS]\n")
    file.write("\n[DEMANDS]\n")
    file.write("\n[PATTERNS]\n")
    file.write("\n[STATUS]\n")
    file.write("\n[CURVES]\n")
    file.write("\n[CONTROLS]\n")
    file.write("\n[RULES]\n")
    file.write("\n[ENERGY]\n")

    file.close()

def read_inp_file(filename):
    G = nx.Graph()
    file = open(filename, 'r')
    network_data = {}
    elevation = []
    reservoirs = []
    tanks = []
    pumps = []
    junctions = []
    pipes = []
    roughness = []
    lengths = []
    demands = []
    for fulline in file:
        # Network Components
        key = fulline.split()
        if(len(key)>0):
            line = key[0]
        if line == "[TITLE]":
           current_tag = "TITLE"
        elif line == "[PIPES]":
            current_tag = "PIPES"
        elif line == "[JUNCTIONS]":
            current_tag = "JUNCTIONS"
        elif line == "[RESERVOIRS]":
            current_tag = "RESERVOIRS"
        elif line == "[TANKS]":
            current_tag = "TANKS"
        elif line == "[PIPES]":
            current_tag = "PIPES"
        elif line == "[PUMPS]":
            current_tag = "PUMPS"
        elif line == "[VALVES]":
            current_tag = "VALVES"
        elif line == "[EMITTERS]":
            current_tag = "EMITTERS"
        elif line == "[CURVES]":
            current_tag = "CURVES"
        elif line == "[PATTERNS]":
            current_tag = "PATTERNS"
        elif line == "[ENERGY]":
            current_tag = "ENERGY"
        elif line == "[STATUS]":
            current_tag = "STATUS"
        elif line == "[CONTROLS]":
            current_tag = "CONTROLS"
        elif line == "[RULES]":
            current_tag = "RULES"
        elif line == "[DEMANDS]":
            current_tag = "DEMANDS"
        elif line == "[QUALITY]":
            current_tag = "QUALITY"
        elif line == "[REACTIONS]":
            current_tag = "REACTIONS"
        elif line == "[SOURCES]":
            current_tag = "SOURCES"
        elif line == "[MIXING]":
            current_tag = "MIXING"
        elif line == "[OPTIONS]":
            current_tag = "OPTIONS"
        elif line == "[TIMES]":
            current_tag = "TIMES"
        elif line == "[REPORT]":
            current_tag = "REPORT"
        elif line == "[COORDINATES]":
            current_tag = "COORDINATES"
        elif line == "[TAGS]":
            current_tag = "TAGS"
        elif line[0] == ";" or fulline.isspace():
            continue
        elif line[0] == "[":
            current_tag = "INVALID"
        elif current_tag == "PIPES" or current_tag == "VALVES":
            line = fulline.split()
            pipes.append(line[0])
            lengths.append(line[3])
            roughness.append(line[5])
            G.add_edge(str(line[1]),str(line[2]))
        elif current_tag == "PUMPS":
            line = fulline.split()
            pumps.append(line[0])
            G.add_edge(str(line[1]), str(line[2]))
        elif current_tag == "JUNCTIONS":
            line = fulline.split()
            elevation.append(line[1])
            demands.append(line[2])
            junctions.append(str(line[0]))
        elif current_tag == "RESERVOIRS":
            line = fulline.split()
            reservoirs.append(str(line[0]))
        elif current_tag == "TANKS":
            line = fulline.split()
            tanks.append(str(line[0]))
            elevation.append(line[1])
        else:
            current_tag ="NONE"

    network_data['JUNCTIONS'] = junctions
    network_data['PUMPS'] = pumps
    network_data['RESERVOIRS'] = reservoirs
    network_data['TANKS'] = tanks
    network_data['PIPES'] = pipes
    network_data['ELEVATIONS'] = elevation
    network_data['ROUGHNESS'] = roughness
    network_data['LENGTH'] = lengths
    network_data['DEMANDS'] = demands
    print(len(G.edges()),len(G.nodes()))
    file.close()
    return G,network_data

def generate_network(G,output_path,network_data):
    initial_pos =  nx.graphviz_layout(G,prog='neato')
    pos = forceatlas2.forceatlas2_networkx_layout(G, pos = initial_pos, niter=100,gravity=.12,strongGravityMode=True,scalingRatio = 5.0) # Optionally specify iteration count
    probable_reservoirs = []
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    for node in pos:
        if(min_x > pos[node][0]) and (G.degree(node) == 1):
            min_x = pos[node][0]
            probable_reservoirs.append(node)
        if(max_x < pos[node][0]) and (G.degree(node) == 1):
            max_x = pos[node][0]
            probable_reservoirs.append(node)
        if (min_y > pos[node][1]) and (G.degree(node) == 1):
            min_y = pos[node][1]
            probable_reservoirs.append(node)
        if (max_y < pos[node][1]) and (G.degree(node) == 1):
           max_y = pos[node][1]
           probable_reservoirs.append(node)

    random_index = randrange(int(len(probable_reservoirs)/2), len(probable_reservoirs))
    reservoir = probable_reservoirs[random_index]
    node_colors = ['blue' if node == reservoir else 'red' for node in G.nodes()]
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=50)
    plt.show()
    write_inp_file(G,pos,output_path,network_data,output_path)

def assign_reservoirs(G, network_data, new_network_data):
    if network_data.has_key('RESERVOIRS'):
        nb_of_reservoirs = len(network_data['RESERVOIRS'])
        probable_reservoirs = []
        reservoirs = []
        pos = new_network_data['COORDINATES']
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        for node in pos:
            if (min_x > pos[node][0]) and (G.degree(node) == 1):
                min_x = pos[node][0]
                probable_reservoirs.append(node)
            if (max_x < pos[node][0]) and (G.degree(node) == 1):
                max_x = pos[node][0]
                probable_reservoirs.append(node)
            if (min_y > pos[node][1]) and (G.degree(node) == 1):
                min_y = pos[node][1]
                probable_reservoirs.append(node)
            if (max_y < pos[node][1]) and (G.degree(node) == 1):
                max_y = pos[node][1]
                probable_reservoirs.append(node)

        random_index = random.sample(range(int(len(probable_reservoirs) / 2), len(probable_reservoirs)),nb_of_reservoirs)
        for index in random_index:
            reservoirs.append(probable_reservoirs[index])
        new_network_data['RESERVOIRS'] = reservoirs

    return new_network_data

def write_metis_format(G,output_path):
    file = open(output_path, "w+")
    file.write(str(len(G.nodes()))+"\t"+ str(len(G.edges()))+"\n")
    for node in G.nodes():
        #file.write(str(node) + "\t")
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            file.write(str(neighbor)+"\t")
        file.write("\n")
    file.close()

def assign_tanks_and_pumps(new_G, G, network_data, new_network_data):
    if network_data.has_key('TANKS'):
        rescale = int(len(new_G.nodes())/len(G.nodes()))
        new_network_data['TANKS'] = []
        new_network_data['PUMPS'] = []
        nb_of_tanks = len(network_data['TANKS'])*rescale
        if nb_of_tanks == 0:
            nb_of_tanks = 4
        write_metis_format(new_G,'temp_graph.graph')
        print(nb_of_tanks)
        import subprocess
        subprocess.call(["/home/varsha/Documents/softwares/KaHIP-master/deploy/kaffpaE", 'temp_graph.graph', '--k',str(nb_of_tanks),'--imbalance','10','--preconfiguration','strong','--output_filename','partitions'])
        os.remove('temp_graph.graph')
        Partitions = read_partition('partitions')
        os.remove('partitions')
        for partition in Partitions:
            for node in Partitions[partition]:
                if new_G.degree(node) == 1:
                    new_network_data['TANKS'].append(node)
                    break
                else:
                    continue

        for partition in Partitions:
            for node in Partitions[partition]:
                if node not in new_network_data['TANKS'] and new_G.degree(str(node)) > 1:
                    neighbors = new_G.neighbors(node)
                    new_network_data['PUMPS'].append((node,random.choice(neighbors)))
                    break
                else:
                    continue

        return new_network_data


def generate_network_data(new_G,G,network_data):
    labeled_new_G = nx.convert_node_labels_to_integers(new_G, first_label=1, ordering='default', label_attribute=None)
    new_network_data = {}
    initial_pos = nx.graphviz_layout(G, prog='neato')
    pos = forceatlas2.forceatlas2_networkx_layout(G, pos=initial_pos, niter=100, gravity=0.12, strongGravityMode=True,
                                                  scalingRatio=5.0)
    nx.draw(G, pos, with_labels=False, node_size=10)
    plt.show()
    # Assign coordinates
    initial_pos = nx.graphviz_layout(labeled_new_G, prog='neato')
    pos = forceatlas2.forceatlas2_networkx_layout(labeled_new_G, pos=initial_pos, niter=100, gravity=0.12, strongGravityMode=True,scalingRatio=5.0)

    new_network_data['COORDINATES'] = pos

    #Assign reservoirs
    new_network_data = assign_reservoirs(labeled_new_G,network_data,new_network_data)

    # Assign tanks
    new_network_data = assign_tanks_and_pumps(labeled_new_G,G,network_data,new_network_data)

    #Assign junctions
    new_network_data = assign_junctions(labeled_new_G,network_data,new_network_data)

    #Assign elevation
    new_network_data = assign_elevation(labeled_new_G,network_data,new_network_data)

    #Assign pipes
    new_network_data = assign_pipes(labeled_new_G,network_data,new_network_data)

    #Assign demand
    new_network_data = assign_demand(labeled_new_G, network_data, new_network_data)

    initial_pos = nx.graphviz_layout(new_G, prog='neato')
    pos = forceatlas2.forceatlas2_networkx_layout(new_G, pos=initial_pos, niter=100, gravity=0.12, strongGravityMode=True,
                                                  scalingRatio=5.0)
    nx.draw(new_G, pos, with_labels=False, node_size=10)
    plt.show()
    return new_network_data

def plot_graph(G,network_data):
    initial_pos = nx.graphviz_layout(G, prog='neato')
    pos = forceatlas2.forceatlas2_networkx_layout(G, pos=initial_pos, niter=100, gravity=0.12,strongGravityMode=True, scalingRatio=5.0)
    nx.draw(G, pos, with_labels=False, node_size=10)
    plt.show()
    blue_nodes = []
    red_nodes =[]
    black_nodes =[]
    for node in network_data['RESERVOIRS']:
        print ('reservoir',node)
        blue_nodes.append(str(node))
    for node in network_data['TANKS']:
        print('tank', node)
        red_nodes.append(str(node))
    for node in network_data['JUNCTIONS']:
        print('junction', node)
        black_nodes.append(str(node))

    nx.draw_networkx_nodes(G, pos, nodelist=blue_nodes, node_color='b', node_size=20)
    nx.draw_networkx_nodes(G, pos, nodelist=red_nodes, node_color='r', node_size=20)
    nx.draw_networkx_nodes(G, pos, nodelist=black_nodes, node_color='black', node_size=5)
    #nx.draw_networkx_nodes(G, pos, nodelist=other_nodes, node_color='black', node_size=5)
    nx.draw_networkx_edges(G, pos)
    # nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=50)
    plt.show()

def read_partition(file_path):
    Partitions = {}
    file = open(file_path)
    node_number = 1
    for line in file:
        values = line.split()
        partition_nb = values[0]
        partition = []
        if Partitions.has_key(partition_nb):
            Partitions[partition_nb].append(node_number)
        else:
            partition.append(node_number)
            Partitions[partition_nb] = partition
        node_number +=1

    return Partitions

def assign_junctions(new_G,network_data,new_network_data):
    junctions = []
    for node in new_G.nodes():
        if node not in new_network_data['TANKS'] and node not in new_network_data['RESERVOIRS']:
            junctions.append(node)

    new_network_data['JUNCTIONS'] = junctions

    return new_network_data


def assign_elevation(new_G, network_data, new_network_data):
    original_distribution = network_data['ELEVATIONS']
    new_distribution = []

    #initialize with zero
    for node in new_G.nodes():
        new_distribution.append(0)

    #neglect zero position add additional indexing
    new_distribution.append(0)

    #Assign initial random values
    for node in new_G.nodes():
        new_distribution[int(node)] = original_distribution[((int(node))%(len(original_distribution)))]

    #smoothing process
    iterations = 3
    smoothened_values = smoothen_values(new_G,new_distribution,iterations)
    #update Elevation for tanks
    for idx in range(1,len(smoothened_values)):
        if idx in new_network_data['TANKS']:
            neighbors = new_G.neighbors(idx)
            sum = 0
            for neighbor in neighbors:
                sum += float(smoothened_values[neighbor])
            smoothened_values[idx] = sum+random.uniform(50, 70)
        idx += 1

    new_network_data['ELEVATIONS'] = smoothened_values
    return new_network_data

def assign_demand(new_G, network_data, new_network_data):
    original_distribution = network_data['DEMANDS']
    new_distribution = []

    # initialize with zero
    for node in new_G.nodes():
        new_distribution.append(0)

    # neglect zero position add additional indexing
    new_distribution.append(0)

    #Assign initial random values
    for node in new_G.nodes():
        new_distribution[int(node)] = original_distribution[int(node)%len(original_distribution)]

    #smoothing process
    iterations = 3
    new_network_data['DEMANDS'] = smoothen_values(new_G,new_distribution,iterations)

    return new_network_data

def assign_pipes(new_G, network_data, new_network_data):
    new_network_data['PIPES'] = []
    for edge in new_G.edges():
        if (edge[0],edge[1]) not in new_network_data['PUMPS'] and (edge[1],edge[0]) not in new_network_data['PUMPS']:
            new_network_data['PIPES'].append((edge[0],edge[1]))

    return new_network_data

def smoothen_values(G,distribution,iterations):
    itr = 0
    while itr < iterations:
        idx = 1
        while idx<len(distribution):
            neighbors = G.neighbors(idx)
            sum = 0
            for neighbor in neighbors:
                sum += float(distribution[neighbor])
            distribution[idx]=float(sum/len(neighbors))
            idx+=1
        itr+=1

    return distribution

def write_hyper_graph_format(G,output):
    print ("does nothing")








