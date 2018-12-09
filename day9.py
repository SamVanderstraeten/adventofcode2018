#brute force - NOT recommended! :X

file = open("input.txt", "r")
lines = file.readlines()

spl = lines[0].split(" ")
lastscore = int(spl[-2]) * 100
numPlayers = int(spl[0])

circle = [0, 2, 1]
currentIndex = 1
marblescore = 0
nextMarble = 3

players = []

for p in range(0,numPlayers):
    players.append(0)

currentPlayer = 3

while nextMarble < lastscore and marblescore < lastscore*3:
    if nextMarble%23 == 0:
        removeMarbleIndex = currentIndex - 7

        marblescore = nextMarble + circle[removeMarbleIndex]
        #print("score: " + str(marblescore))
        del circle[removeMarbleIndex]
        currentIndex = removeMarbleIndex

        if currentIndex < 0:
            currentIndex += 1

        players[currentPlayer] += marblescore
        #print(str(currentIndex))
    else:
        insertIndex = (currentIndex + 2) % len(circle)
        if insertIndex == 0:
            circle.append(nextMarble)
            currentIndex = len(circle) - 1
        else:
            circle.insert(insertIndex, nextMarble)
            currentIndex = insertIndex

    #print(circle)
    nextMarble += 1
    currentPlayer = (currentPlayer + 1) % numPlayers
    print(str(nextMarble) + "/" + str(lastscore) + " done")

print("done")
#print(players)

max = 0
for s in players:
    if s > max:
        max = s
print(str(max))