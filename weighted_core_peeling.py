"""
python weighted_core_peeling.py [path to graph file] [alpha] [beta] [output json file path]

- Input Graph Format
    Graph
    # node  neighbor  weight
    0   1   3
    1   2   5
    alpha, and beta are numbers
- Output JSON Format
    A dictionary with keys as nodes, and values as core numbers
Example Command:
python3 weighted_core_peeling.py example.txt 1 1 output.json

"""

import ast
import json
import sys
from copy import deepcopy
import math
import statistics
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker
import os

def core_decomposition(graph, weights, alpha, beta):
    cores = {}
    nodes = []
    for node, neighbors in graph.items():
        weights_sum = 0
        for neighbor in neighbors:
            weights_sum += weights[(min(node, neighbor), max(node, neighbor))]
        degree = len(neighbors)
        weights_sum = math.pow(degree, alpha) * math.pow(weights_sum, beta)
        root = alpha + beta
        cores[node] = int(weights_sum**(1/root))
        nodes.append(node)
    while len(nodes) > 0:
        min_node = -1
        min_core = sys.maxsize
        for node in nodes:
            if cores[node] < min_core:
                min_core = cores[node]
                min_node = node
        nodes.remove(min_node)
        for neighbor in graph[min_node]:
            if neighbor in nodes:
                if cores[neighbor] > min_core:
                    weights_sum = 0
                    degree = 0
                    for node in graph[neighbor]:
                        if node in nodes:
                            weights_sum += weights[(min(node, neighbor), max(node, neighbor))]
                            degree += 1
                    weights_sum = math.pow(degree, alpha) * math.pow(weights_sum, beta)
                    new_core = int(weights_sum**(1/root))
                    cores[neighbor] = max(new_core, min_core)
    return cores

graph = {}
weights = {}

f = open(sys.argv[1], "r")

for line in f:
    line = line.strip()
    delim = ""
    if line[:1].isdigit():
        if delim == "":
            for char in line:
                if not char.isdigit():
                    delim = char
                    break
        nodes = line.split(delim)
        nodes = [i for i in nodes if i]
        nodes = list(map(int, nodes))
        if nodes[0] not in graph:
            graph[nodes[0]] = []
        if nodes[1] not in graph:
            graph[nodes[1]] = []
        if nodes[1] not in graph[nodes[0]]:
            graph[nodes[0]].append(nodes[1])
        if nodes[0] not in graph[nodes[1]]:
            graph[nodes[1]].append(nodes[0])
        if (min(nodes[0], nodes[1]), max(nodes[0], nodes[1])) not in weights:
            weights[min(nodes[0], nodes[1]), max(nodes[0], nodes[1])] = nodes[2]

meanWeight = 0
minWeight = sys.maxsize
m = 0
for edge, weight in weights.items():
    meanWeight += weight
    if weight < minWeight:
        minWeight = weight
    m += 1
meanWeight = meanWeight / m
print("Mean Weight: " + str(meanWeight))

alpha = int(sys.argv[2])
beta = int(sys.argv[3])
for edge, weight in weights.items():
    normalization = weight / meanWeight
    weights[edge] = int(max(math.floor(normalization / minWeight), 1))

cores = core_decomposition(graph, weights, alpha, beta)

outputJsonPath = sys.argv[4]
with open(outputJsonPath, 'w') as f:
    json.dump(cores, f)

k_shells = []
for node, core in cores.items():
    if core not in k_shells:
        k_shells.append(core)
print("Number of k-cores: " + str(len(k_shells)))

nodes_per_core = {}
allCores = []
for node, core in cores.items():
    if core not in nodes_per_core:
        nodes_per_core[core] = 1
    else:
        nodes_per_core[core] += 1
    allCores.append(core)

title = "Weighted k-core peeling- alpha:" + str(alpha) + ", beta: " + str(beta)
plt.figure(figsize=(20,10)).suptitle(title , y = 0.90)
plt.hist(allCores, bins=50)
plt.xlabel('core number')
plt.ylabel('# of nodes')
outputFilePath = os.path.join(sys.argv[4][0:-5]+ ".png")
plt.savefig(outputFilePath)