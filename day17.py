import sys
import numpy as np
from collections import OrderedDict

file = open("inputarno.txt", "r")
lines = file.readlines()

DEFAULT_GRID_SIZE = 2500
tempgrid = np.zeros([DEFAULT_GRID_SIZE, DEFAULT_GRID_SIZE], dtype=int)

def printGrid(showReachable=False):
    for r in range(0, len(grid)):
        row = grid[r]
        for c in range(0, len(row)):
            t = row[c]
            if [r,c] in runningWater:
                sys.stdout.write("|")
            elif t == 0: # sand
                sys.stdout.write(".")
            elif t == 1: # clay
                sys.stdout.write("#")
            elif t == 2: # settled water
                sys.stdout.write("~")
            elif t == 9: # well
                sys.stdout.write("+")
        print("")

    if showReachable:
        for r in range(0, len(reachable_grid)):
            row = reachable_grid[r]
            for c in range(0, len(row)):
                t = row[c]
                sys.stdout.write(str(t))
            print("")

structures = []
for line in lines:
    spl = line.strip().split(", ")
    
    s1 = spl[0].split("=")
    s2 = spl[1].split("=")

    structures.append({s1[0]: s1[1], s2[0]: s2[1]})

# fill the grid
xmin = ymin = 999999
xmax = ymax = 0
for structure in structures:
    # x
    xvalue = structure['x']
    xvalue_start = 0
    xvalue_end = 0
    if xvalue.find('..') >= 0:
        xvalue_start = int(xvalue.split('..')[0])
        xvalue_end = int(xvalue.split('..')[1])
    else:
        xvalue_start = int(xvalue)
        xvalue_end = int(xvalue)

    # y
    yvalue = structure['y']
    yvalue_start = 0
    yvalue_end = 0
    if yvalue.find('..') >= 0:
        yvalue_start = int(yvalue.split('..')[0])
        yvalue_end = int(yvalue.split('..')[1])
    else:
        yvalue_start = int(yvalue)
        yvalue_end = int(yvalue)

    for x in range(xvalue_start, xvalue_end+1):
        for y in range(yvalue_start, yvalue_end+1):
            tempgrid[y][x] = 1

    if xvalue_start < xmin:
        xmin = xvalue_start
    if yvalue_start < ymin:
        ymin = yvalue_start

    if xvalue_end > xmax:
        xmax = xvalue_end
    if yvalue_end > ymax:
        ymax = yvalue_end

maxwidth = xmax - xmin
maxheight = ymax - ymin

grid = np.zeros([maxheight+2, maxwidth+3], dtype=int)
reachable_grid = np.zeros([maxheight+2, maxwidth+3], dtype=int)

for r in range(0, maxheight+2):
    for c in range(0, maxwidth+3):
        grid[r][c] = tempgrid[ymin-1+r][xmin-1+c]

well = (0, 500-(xmin-1))
grid[well[0]][well[1]] = 9
waterSpawns = [(0, 500-(xmin-1))]

runningWater = []
def dropTheWater():
    spawn_rm = []
    for spawn in waterSpawns:
        running = []
        w = [spawn[0], spawn[1]]
        while w[0]+1 < len(grid) and grid[w[0]+1][w[1]] == 0: # continue down while sand below
            w[0] += 1
            running.append([w[0],w[1]])
            reachable_grid[w[0]][w[1]] = 1

        if w[0]+1 == len(grid): # bottom of grid was reached, spawn not needed
            spawn_rm.append(spawn)
        else:   # clay or water below; spread out
            rm = []
            for wi in range(0, len(running)):
                # spread left & right
                leftBorder = rightBorder = False
                outerLeft = outerRight = None
                waterplane = [w]
                current = [w[0], w[1]]
                # L
                while (not grid[current[0]+1][current[1]] == 0) and (not grid[current[0]][current[1]-1] == 1): # find left
                    current[1] -= 1
                    waterplane.append([current[0], current[1]])
                if grid[current[0]][current[1]-1] == 1:
                    leftBorder = True
                else:
                    outerLeft = [current[0], current[1]]
                # R
                current = [w[0], w[1]]
                while (not grid[current[0]+1][current[1]] == 0) and (current[1]+1 < len(grid[0])) and (not grid[current[0]][current[1]+1] == 1): # find right
                    current[1] += 1
                    waterplane.append([current[0], current[1]])
                if (current[1]+1 < len(grid[0])) and grid[current[0]][current[1]+1] == 1:
                    rightBorder = True
                else:
                    outerRight = [current[0], current[1]]

                if leftBorder and rightBorder: # add settled water
                    for p in waterplane:
                        grid[p[0]][p[1]] = 2
                        reachable_grid[p[0]][p[1]] = 1
                    rm.append(wi)
                else:
                    for p in waterplane:
                        if not p in running:
                            running.append(p)
                            reachable_grid[p[0]][p[1]] = 1
                    if not outerLeft == None:
                        if not outerLeft in waterSpawns:
                            waterSpawns.append(outerLeft)
                    if not outerRight == None:
                        if not outerRight in waterSpawns:
                            waterSpawns.append(outerRight)

            for r in range(0, len(rm)):
                ri = max(rm)
                del running[ri]
                rm.remove(ri) 

    for rem in spawn_rm:
        waterSpawns.remove(rem)
        
def addWater():
    for spawn in waterSpawns:
        runningWater.append([spawn[0], spawn[1]])

def countReachable():
    count = 0
    for row in reachable_grid:
        for t in row:
            if t == 1:
                count += 1
    return count

def countAtRest():
    count = 0
    for row in grid:
        for t in row:
            if t == 2:
                count += 1
    return count

def cleanRunningWater():
    global runningWater
    rw = []
    for r in runningWater:
        if (not r in rw) and (not grid[r[0]][r[1] == 2]):
            rw.append(r)
    runningWater = rw

#start dropping water
ticks = 0
prevReachable = -1
done = False
while not done:
    dropTheWater()    
    ticks += 1
    print("Tick #" + str(ticks))

    currentReachable = countReachable()
    if ticks > 500 and prevReachable == currentReachable: # hacky, i know
        done = True
        print("# Reachable: " + str(prevReachable))
    prevReachable = currentReachable

print("At rest: " + str(countAtRest()))
printGrid()
rw = []
