import numpy as np
import sys
target = (740+1, 15+1)
depth = 3558

#target = (10+1,10+1)
#depth = 510

grid = np.zeros([target[0],target[1]], dtype=int)
groundmap = np.zeros([target[0], target[1]], dtype=int)

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

        risk += riskfactor

printMap()
print("Risk level: " + str(risk))

# dijkstra time