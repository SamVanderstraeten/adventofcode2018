import sys

file = open("input.txt", "r")
lines = file.readlines()

points = []

# oranje boven
def getMaxima():
    maxx = 0
    maxy = 0
    for point in points:
        if point[0] > maxx:
            maxx = point[0]
        
        if point[1] > maxy:
            maxy = point[1]
    return (maxx, maxy)

def getMinima():
    minx = 99999999
    miny = 99999999
    for point in points:
        if point[0] < minx:
            minx = point[0]
        if point[1] < miny:
            miny = point[1]
    return (minx, miny)

def tick():
    global points
    newpoints = []
    for point in points:
        v = (point[0]+point[2], point[1]+point[3], point[2], point[3])
        newpoints.append(v)
    points = newpoints

def printer(ticker):
    (maxX, maxY) = getMaxima()
    (minX, minY) = getMinima()

    if (maxX-minX) < 100 and (maxY-minY) < 100:
        print("Tick #" + str(ticker))
        #build sky when all points are in good range
        sky = []
        for row in range(0, (maxY-minY)+1):
            sky.append(['.'] * ((maxX-minX)+1))
        for point in points:
            sky[point[1]-minY][point[0]-minX] = '#'
                
        # print sky
        for row in range(0, len(sky)):
            for col in range(0, len(sky[0])):
                sys.stdout.write(sky[row][col] + " ")
            print("")
        return True
    return False


if __name__ == "__main__":
    #read lines
    for line in lines:
        spl = line.split(",")
        posX  = int(spl[0].split("<")[1])
        posY = int(spl[1].split(">")[0])

        velX = int(spl[1].split("<")[1])
        velY = int(spl[2].split(">")[0])

        points.append((posX, posY, velX, velY))

    con = ""
    ticker = 1
    while con != "q":
        tick()
        if printer(ticker):
            print("")
            print("----")        
            con = input('Go on?')
            print("")
        else:
            print("Nothing found, going on...")
        ticker += 1