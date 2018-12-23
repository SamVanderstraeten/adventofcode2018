import numpy as np
import sys
target = (740+1, 15+1)
depth = 3558

#target = (10+1,10+1)
#depth = 510

grid = np.zeros([target[0]*2,target[1]*2], dtype=int)
groundmap = np.zeros([target[0]*2, target[1]*2], dtype=int)

risk = 0

def printMap():
    global groundmap

    for row in groundmap:
        for col in row:
            sys.stdout.write(str(col) + " ")
        print("")

for row in range(0,target[0]):
    for col in range(0, target[1]):
        gindex = -1
        if (row == 0 and col == 0) or (row == target[0]-1 and col == target[1]-1): 
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

printMap()
print("Risk level: " + str(risk))

def unvisited_neighbors(currentNode):
    nbs = []
    for r in range(-1,2):
        for c in range(-1,2):
            if r == 0 and c == 0:
                continue
            elif r == 0 or c == 0 and currentNode[0] + r >= 0 and currentNode[1] + c >= 0 and currentNode[0] + r < len(visited) and currentNode[1] + c < len(visited[0]):
                if visited[currentNode[0] + r][currentNode[1] + c] == 0:
                    nbs.append([r,c])

def get_cost(fromNode, toNode):


# dijkstra time
costgrid = np.zeros([target[0]*2, target[1]*2], dtype=int)
visited = np.zeros([target[0]*2, target[1]*2], dtype=int)
current = [0,0]
# keep current equipment

for r in range(0,len(costgrid)):
    for c in range(0, len(costgrid[r])):
        costgrid[r][c] = 999999
costgrid[current[0]][current[1]] = 0

# select unvisited neighbor with smallest distance
nbs = unvisited_neighbors(current)
for nb in nbs:
    cost = get_cost(current, nb)
