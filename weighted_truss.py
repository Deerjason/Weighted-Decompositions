"""
python3 weighted_truss.py [input G file] [output json file]

- Input Graph Format
    # node  neighbor  weight
    0   1   3
    1   2   5
- Output JSON Format
    Dictionary of edges (represented as a vertex to vertex pair) to weighted truss numbers

Example Command:
python3 weighted_truss.py example.txt example_truss.json

To adapt the code for your own weighted truss implementation, change the code commented
with "depends on weighted decomposition method" with your own implementation
"""

import json
import math
import sys

# Peeling for weighted truss decomposition
def weighted_truss_decomposition(G, W):
    truss = {}
    triangles = {}
    for e1 in W:
        v1, v2 = e1
        truss[e1] = 0
        triangles[e1] = []
        for v3 in G[v1]:
            if v3 in G[v2]:
                e2 = (min(v1, v3), max(v1, v3))
                e3 = (min(v2, v3), max(v2, v3))

                # The following line depends on weighted decomposition method
                truss[e1] += min(W[e1], W[e2], W[e3])

                triangles[e1].append((e2, e3))
    while len(triangles) > 0:
        e1 = None
        min_truss = sys.maxsize
        for e in triangles:
            if truss[e] < min_truss:
                min_truss = truss[e]
                e1 = e
        for triangle in triangles[e1]:
            e2 = triangle[0]
            e3 = triangle[1]
            for e in triangle:
                if truss[e] > min_truss:

                    # The following line depends on weighted decomposition method
                    truss[e] -= min(W[e1], W[e2], W[e3])

                    if truss[e] < min_truss:
                        truss[e] = min_truss
                v1, v2 = e
                v3 = -1
                for v in e1:
                    if v not in e:
                        v3 = v
                triangles[e].remove(((min(v1, v3), max(v1, v3)), (min(v2, v3), max(v2, v3))))
        triangles.pop(e1)
    return truss

# Adjacency List
G = {}

# Edge weights
W = {}

# Reads input file
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
        values = line.split(delim)
        values = [i for i in values if i]
        values = list(map(int, values))
        # No self loops
        if values[0] != values[1]:
            # Populate adjacency list
            if values[0] not in G:
                G[values[0]] = []
            if values[1] not in G:
                G[values[1]] = []
            if values[1] not in G[values[0]]:
                G[values[0]].append(values[1])
            if values[0] not in G[values[1]]:
                G[values[1]].append(values[0])
            # Populate edge weights
            e = (min(values[0], values[1]), max(values[0], values[1]))
            if e not in W:
                W[e] = values[2]

# Calculates mean weight
m = 0
for node, neighbors in G.items():
    m += len(neighbors)
m = m/2
meanW = 0
for e, w in W.items():
    meanW += w
meanW = meanW / m

# Normalizes weights (depends on weighted decomposition method)
for e, w in W.items():
    W[e] = max(math.floor(w/meanW), 1)

weighted_truss = weighted_truss_decomposition(G, W)

# Outputs weighted truss to json file
with open(sys.argv[2], 'w') as f:
    json.dump({str(k): v for k, v in weighted_truss.items()}, f)
