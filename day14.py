scorelist = [3,7]

elfA = 0
elfB = 1

target = "633601"
recipes = 0
finalscorelength = 10
finalscorestart = -1
targetfound = False

targetLen = len(target)
count = 0

while not targetfound:
    currentA = scorelist[elfA]
    currentB = scorelist[elfB]
    newscore = currentA + currentB
    if newscore > 9:
        scorelist.append(1)
        scorelist.append(newscore % 10)
    else:
        scorelist.append(newscore)
    elfA = (elfA + (1+currentA)) % len(scorelist)
    elfB = (elfB + (1+currentB)) % len(scorelist)

    if len(scorelist) > targetLen:
        checker = ""
        for i in range(len(scorelist)-targetLen, len(scorelist)):
            checker += str(scorelist[i])
        if checker == target:
            print("match found @1")
            targetfound = True
            recipes = len(scorelist) - targetLen
        
        checker = ""
        for i in range(len(scorelist)-(targetLen+1), len(scorelist)-1):
            checker+= str(scorelist[i])
        if checker == target:
            print("match found @2")
            targetfound = True
            recipes = len(scorelist) - (targetLen+1)

    count += 1
    print(str(count))

print(str("left: " + str(recipes)))

'''result = ""
for i in range(0, finalscorelength):
    result += str(scorelist[recipes+i])

print(result)'''