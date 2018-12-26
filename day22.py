import numpy as np
import sys
import math

target = (740, 15)
depth = 3558

#target = (10,10)
#depth = 510

gridSize = (int(target[0]*3), int(target[1]*3))

grid = np.zeros([gridSize[0], gridSize[1]], dtype=int)
groundmap = np.zeros([gridSize[0], gridSize[1]], dtype=int)

risk = 0

def printMap():
    global groundmap

    for r in range(0, len(groundmap)):
        row = groundmap[r]
        for c in range(0, len(row)):
            col = row[c]
            if r == target[0] and c == target[1]:
                sys.stdout.write("X ")
            else:
                sys.stdout.write(str(col) + " ")

        print("")

for row in range(0,gridSize[0]):
    for col in range(0, gridSize[1]):
        gindex = -1
        if (row == 0 and col == 0) or (row == target[0] and col == target[1]): 
            gindex = 0
        elif row == 0:
            gindex = (col * 16807) % 20183
        elif col == 0:
            gindex = (row * 48271) % 20183
        else:
            gindex = ((grid[row-1][col]) * (grid[row][col-1])) % 20183
        
        erosionlevel = (gindex + depth) % 20183
        grid[row][col] = erosionlevel        
        riskfactor = erosionlevel % 3
        groundmap[row][col] = riskfactor

        if row < target[0] and col < target[1]:
            risk += riskfactor

#printMap()
#print("Risk level: " + str(risk))

# create 3D grid (3 layers of gridsize) (each layer is for 1 tool)
# mark reachable/walkable terrain in each layer
# setup graph & run dijkstra

layerTorch = np.zeros([gridSize[0], gridSize[1]], dtype=int)
layerGear = np.zeros([gridSize[0], gridSize[1]], dtype=int)
layerNone = np.zeros([gridSize[0], gridSize[1]], dtype=int)

distances = {} # "1$15$12" -> 812
unvisited = []

def build_id(layer, row, col):
    vid = str(layer) + "$" + str(row) + "$" + str(col)
    return vid

def parse_id(idtje):
    return [int(x) for x in idtje.split("$")]

def get_smallest_unvisited():
    smallest = None
    smallest_dist = 8888889
    for u in unvisited:
        if distances[u] < smallest_dist:
            smallest_dist = distances[u]
            smallest = u

    if smallest == 8888888:
        print("WARNING! Smallest is infinity")
    return smallest

# build layers
for r in range(0, len(groundmap)):
    row = groundmap[r]
    for c in range(0, len(row)):
        t = row[c]
        if t == 0: # rocky
            layerTorch[r][c] = 1
            layerGear[r][c] = 1
            layerNone[r][c] = 99999
        elif t == 1: # wet
            layerGear[r][c] = 1
            layerNone[r][c] = 1
            layerTorch[r][c] = 99999
        elif t == 2: # narrow
            layerTorch[r][c] = 1
            layerNone[r][c] = 1
            layerGear[r][c] = 99999

layers = [layerTorch, layerGear, layerNone] # this is the graph

# init 'distances'
for l in range(0, len(layers)):
    layer = layers[l]
    for r in range(0, len(layer)):
        row = layer[r]
        for c in range(0, len(row)):
            v = row[c]
            vid = build_id(l,r,c)
            distances[vid] = 8888888 #infinity
            if not v == 99999: # not allowed
                unvisited.append(vid)

distances["0$0$0"] = 0 # start at 0,0 with torch = layer 0

num = len(unvisited)
while len(unvisited) > 0:
    # select from D smallest distance
    closest = get_smallest_unvisited()
    coords = parse_id(closest)   

    # remove from unvisited
    unvisited.remove(closest)

    # find neighbors and search for shortest routes
    for layer in range(-1, 2):
        for row in range(-1, 2):
            for col in range(-1, 2):
                if math.fabs(layer) + math.fabs(row) + math.fabs(col) == 1:
                    nl = (coords[0] + layer) % 3
                    nr = coords[1] + row
                    nc = coords[2] + col
                    #if nid in unvisited:
                    if 0 <= nr < len(layers[nl]) and 0 <= nc < len(layers[nl][nr]):
                        if not layers[nl][nr][nc] == 99999:
                            nid = build_id(nl, nr, nc)
                        
                            cost = 1
                            if not nl == coords[0]: #switch gear costs 7 minutes
                                cost = 7    
                            a = distances[closest] + cost
                            if a < distances[nid]:
                                distances[nid] = a

    if (num-len(unvisited)) % 100 == 0:
        print(str(num - len(unvisited)) + "/" + str(num))
    if len(unvisited) == 0:
        print("I AM DONE MASTER")
                        

print("DIST TO TARGET: " + str(distances[build_id(0, target[0], target[1])]))

print("NEIGHBORS:")
for layer in range(-1, 2):
    for row in range(-1, 2):
        for col in range(-1, 2):
            if math.fabs(layer) + math.fabs(row) + math.fabs(col) == 1:
                nl = (coords[0] + layer) % 3
                nr = coords[1] + row
                nc = coords[2] + col
                nbid = build_id(nl, nr, nc)
                if nbid in distances:
                    print("NB " + str(distances[nbid]))

#for d in distances:
#    print(str(d) + " >>> " + str(distances[d]))
#757 too low
#1036 too high