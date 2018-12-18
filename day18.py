import sys
import math
import numpy as np

file = open("input.txt", "r")
lines = file.readlines()

grid = np.zeros([len(lines), len(lines[0].strip())])

for row in range(0, len(lines)):
    line = lines[row].strip()
    for col in range(0, len(line)):
        t = line[col]
        if t == "#":    # lumberyard
            grid[row][col] = 1
        elif t == "|":   # tree  
            grid[row][col] = 2

def printGrid():
    for row in grid:
        for t in row:
            if t == 0:
                sys.stdout.write(". ")
            elif t == 1:
                sys.stdout.write("# ")
            elif t == 2:
                sys.stdout.write("| ")
        print("")

def getResourceScore():
    lumbs = 0
    trees = 0
    for row in grid:
        for t in row:
            if t == 1:
                lumbs += 1
            elif t == 2:
                trees += 1
    return lumbs*trees

def getAdjacents(row, col):
    startrow = max(0, row-1)
    endrow = min(row+1, len(grid)-1)
    startcol = max(0, col-1)
    endcol = min(col+1, len(grid[0])-1)

    adjs = {'trees': 0, 'lumbs': 0, 'opens': 0}

    for r in range(startrow, endrow+1):
        for c in range(startcol, endcol+1):
            if r == row and c == col:
                continue

            t = grid[r][c]
            if t == 0:
                adjs['opens'] += 1
            elif t == 1:
                adjs['lumbs'] += 1
            elif t == 2:
                adjs['trees'] += 1

    return adjs


print("Initial state")
printGrid()

result = prevResult = 0
steps = 1000000000
loopStart = -1
theloop = []
loopStartScore = -1
for i in range(0, steps):
    newGrid = np.zeros([len(lines), len(lines[0].strip())])
    for r in range(0, len(grid)):
        row = grid[r]
        for c in range(0, len(row)):
            t = row[c]
            adj = getAdjacents(r,c)
            if t == 0:
                if adj['trees'] >= 3:
                    newGrid[r][c] = 2
                else:
                    newGrid[r][c] = 0
            elif t == 2:
                if adj['lumbs'] >= 3:
                    newGrid[r][c] = 1
                else:
                    newGrid[r][c] = 2
            elif t == 1:
                if adj['lumbs'] > 0 and adj['trees'] > 0:
                    newGrid[r][c] = 1
                else:
                    newGrid[r][c] = 0
    
    grid = newGrid
    prevResult = result
    result = getResourceScore()

    diff = result - prevResult
    if not loopStart == -1 and not diff == -4012:
        theloop.append(diff)
        print(diff)
    
    if diff == -4012:
        if loopStart == -1:
            loopStart = i
            loopStartScore = prevResult
            print("Loop starts at " + str(i))
            print(diff)
            theloop.append(diff)
        else:
            break

loopDiff = 0
for l in theloop:
    loopDiff += l

rest = steps - loopStart
final = rest % len(theloop)
restLoops = math.floor(rest / len(theloop))

loopStartScore += (loopDiff * restLoops) # loop diff = 0 so not really needed...

for i in range(0, final):
    loopStartScore += theloop[i]

print("Resource score: " + str(loopStartScore))
