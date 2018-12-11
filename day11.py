import math

file = open("testinput.txt", "r")
lines = file.readlines()

grid = [[] for i in range(0,300)]
serial = 5034

def getGridValue(x,y):
    global grid
    return grid[y][x]

for y in range(0, 300):
    grid[y] = [0]*300
    for x in range(0,300):
        rackID = x + 10
        power = rackID * y
        power += serial
        power *= rackID
        power = math.floor(power / 100) % 10
        grid[y][x] = power - 5

bestx= 0
besty = 0
besttotal = 0
bestsize = 0
for y in range(0, 300):
    print("row " + str(y) + " best so far:  " + str(bestx) + ", "+  str(besty) + ","  + str(bestsize) + ", " + str(besttotal))
    for x in range(0,300):
        currenttotal = 0
        for s in range(1,300):
            if x+s < 300 and y+s < 300:                
                for ly in range(y, y+s):
                    currenttotal += grid[ly][x+s-1]
                for lx in range(x, x+s-1):
                    currenttotal += grid[y+s-1][lx]

                if currenttotal > besttotal:
                    besttotal = currenttotal
                    bestx = x
                    besty = y
                    bestsize = s          


print(str(bestx))
print(str(besty))
print(str(bestsize))
print(str(besttotal))