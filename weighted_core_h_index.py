"""
python weighted_core.py [input graph file path] [alpha] [beta] [output json file path/name]

- Input Graph Format
    Graph
    # node  neighbor  weight
    0   1   3
    1   2   5
    alpha, and beta are numbers
- Output JSON Format
    A dictionary with keys as nodes, and values as core numbers
Example Command:
python3 weighted_core_h_index.py example.txt 1 1 output.json
"""

import json
import os
import sys
import math


def core_decomposition(graph, weights, alpha, beta):
    h = {}
    for node in graph:
        h[node] = float('inf')
    changed = True
    while changed:
        changed = False
        for node in graph:
            newIndexForNode = getHIndex(node, h, graph, weights, alpha, beta)
            if newIndexForNode != h[node]:
                changed = True
                h[node] = newIndexForNode
    return h

def getHIndex(node, h, graph, weights, alpha, beta):
    root = alpha + beta
    temp = []
    for nei in graph[node]:
        edgeKey = min(node, nei), max(node, nei)
        weight = weights[edgeKey]
        temp.append((weight, h[nei]))
    temp.sort(key=lambda x: x[1], reverse=True)
    pre = 0
    totalWeight = 0
    i = 1
    newHindex = 0
    for tup in temp:
        totalWeight += tup[0]
        newHindex = math.pow(i, alpha) * math.pow(totalWeight, beta)
        newHindex = int(newHindex**(1/root))    
        if newHindex >= tup[1]:
            return max(pre, tup[1])
        pre = newHindex
        i += 1
    return pre

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
    m += 1
    meanWeight += weight
    if weight < minWeight:
        minWeight = weight
meanWeight = meanWeight / m
print("Mean Weight: " + str(meanWeight))

for edge, weight in weights.items():
    normalization = weight / meanWeight
    weights[edge] = int(max(math.floor(normalization / minWeight), 1))

alpha = int(sys.argv[2])
beta = int(sys.argv[3])
cores = core_decomposition(graph, weights, alpha, beta)

with open(sys.argv[4], 'w') as f:
    json.dump(cores, f)
    print("Cores written to :"+sys.argv[4])
