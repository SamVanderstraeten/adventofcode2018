import numpy as np
import sys
sys.setrecursionlimit(10000)

file = open("input.txt", "r")
lines = file.readlines()

GRIDSIZE = 1000

grid = np.zeros([GRIDSIZE, GRIDSIZE], dtype=int) # 0 = wall, 1 = room, 2 = door

def setRoom(position):
    grid[position[0]][position[1]] = 1

def setDoor(position):
    if position[0] >= 0 and position[0] < len(grid) and position[1] >= 0 and position[1] < len(grid):
        grid[position[0]][position[1]] = 2

def printMap():
    temp = grid[int(GRIDSIZE/2)][int(GRIDSIZE/2)]
    grid[int(GRIDSIZE/2)][int(GRIDSIZE/2)] = 3
    for row in grid:
        for col in row:
            t = "#"
            if col == 1:
                t = "."
            elif col == 2:
                t = "+"
            elif col == 3:
                t = "S"
            sys.stdout.write(t + " ")
        print("")
    grid[int(GRIDSIZE/2)][int(GRIDSIZE/2)] = temp

def printCostGrid():
    for row in costGrid:
        for col in row:
            sys.stdout.write(str(col) + " ")
        print("")

def parseDirections(directions, startPos):
    #print("parse " + directions)
    #print("@ ", startPos)

    origPos = [startPos[0], startPos[1]]
    r = 0
    while r < len(directions):
        t = directions[r]
        if t == "N":
            startPos[0] -= 1
            setDoor(startPos)
            startPos[0] -= 1
            setRoom(startPos)
        elif t == "S":
            startPos[0] += 1
            setDoor(startPos)
            startPos[0] += 1
            setRoom(startPos)
        elif t == "W":
            startPos[1] -= 1
            setDoor(startPos)
            startPos[1] -= 1
            setRoom(startPos)
        elif t == "E":
            startPos[1] += 1
            setDoor(startPos)
            startPos[1] += 1
            setRoom(startPos)
        elif t == "(":
            sub = ""
            open = 0
            for x in range(r+1, len(directions)):
                if directions[x] == "(":
                    open += 1
                if open > 0 or not directions[x] == ")":
                    sub += directions[x]
                if directions[x] == ")":
                    if open == 0:
                        break
                    else:
                        open -= 1
            parseDirections(sub, startPos)
            r += len(sub)+1
        elif t == "|":
            startPos = [origPos[0], origPos[1]]

        #printMap()
        #input("Continnue?")
        r+=1

highestCost = 0
def updateNeighbors(room, currentCost):    
    global highestCost
    if costGrid[room[0]][room[1]] == 0 or costGrid[room[0]][room[1]] > currentCost:
        costGrid[room[0]][room[1]] = currentCost
        if currentCost > highestCost:
            highestCost = currentCost

        if room[0]-2 >= 0 and grid[room[0]-1][room[1]] == 2: # north; valid and door
            updateNeighbors([room[0]-2, room[1]], currentCost+1)
        if room[0]+2 < len(grid) and grid[room[0]+1][room[1]] == 2: # south; valid and door
            updateNeighbors([room[0]+2, room[1]], currentCost+1)
        if room[1]-2 > 0 and grid[room[0]][room[1]-1] == 2: # west; valid and door
            updateNeighbors([room[0], room[1]-2], currentCost+1)
        if room[1]+2 < len(grid) and grid[room[0]][room[1]+1] == 2: # west; valid and door
            updateNeighbors([room[0], room[1]+2], currentCost+1)

# read map
line = lines[0]
setRoom([int(GRIDSIZE/2), int(GRIDSIZE/2)])
parseDirections(line, [int(GRIDSIZE/2), int(GRIDSIZE/2)])

#printMap()

costGrid = np.zeros([GRIDSIZE, GRIDSIZE], dtype=int)
start = [int(GRIDSIZE/2), int(GRIDSIZE/2)]
updateNeighbors(start, 0)
costGrid[start[0]][start[1]] = 0

#print("")
#print("Cost grid:")
#printCostGrid()
print("Highest cost: " + str(highestCost))

count = 0
for row in costGrid:
    for col in row:
        if col >= 1000:
            count += 1
print("Number > 1000 doors: " + str(count))






    