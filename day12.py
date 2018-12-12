import math

file = open("input.txt", "r")
lines = file.readlines()

theState = "#.#.#...#..##..###.##.#...#.##.#....#..#.#....##.#.##...###.#...#######.....##.###.####.#....#.#..##"
generations = 250

patterns = {}

for line in lines:
    patterns[line.split()[0]] = line.split()[2]

for i in range(1,len(theState)):
    theState = '.'+theState

for i in range(1,len(theState)*4):
    theState = '.' + theState + '.'

prevScore = 0
def printScore(gen):
    global theState
    global prevScore
    score = 0
    first = -1* math.floor((len(theState) / 2))
    for i in range(0, len(theState)):
        if theState[i] == "#":
            score += (first + i)
    print("#" + str(gen) + " Total score: " + str(score) + ", diff " + str(score-prevScore))
    prevScore = score
    return score

#print("#0" + theState)

for gen in range(0, generations):
    newState = ""
    for i in range(0, len(theState)):
        subState = ''
        start = i-2
        end = i+2
        if start == -1:
            subState = '.' + theState[0:end+1]
        elif start == -2:
            subState = '..' + theState[0:end+1]
        elif end == len(theState):
            subState = theState[start:len(theState)] + '.'
        elif end == len(theState)+1:
            subState = theState[start:len(theState)] + '..'
        else:
            subState = theState[start:end+1] 

        setT = False
        for pattern in patterns:
            if subState == pattern:
                newState += patterns[pattern]
                setT = True
                break
        if not setT:
            newState += '.'

    theState = newState
    #print("#" + str(gen+1) + " " + theState)
    printScore(gen+1)

# Pattern starting at generation #103 !! increase in score by 59 each generation (shifting up all the time)
# #250 Total score: 16348, diff 59 (repeated, stable)
diff = 50000000000 - 250
result = 16348 + (diff*59)
print(str(result))