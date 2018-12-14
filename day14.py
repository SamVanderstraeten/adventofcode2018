scorelist = [3,7]

elfA = 0
elfB = 1

target = "633601"
recipes = 0
finalscorelength = 10
finalscorestart = -1
targetfound = False

targetLen = len(target)

while not targetfound:
    currentA = scorelist[elfA]
    currentB = scorelist[elfB]
    newscore = currentA + currentB
    if newscore > 9:
        scorelist.append(1)
    scorelist.append(newscore % 10)
    elfA = (elfA + (1+currentA)) % len(scorelist)
    elfB = (elfB + (1+currentB)) % len(scorelist)

    if len(scorelist) > targetLen:
        sublist = scorelist[-targetLen:]
        checker = ''.join(str(x) for x in sublist)
        if checker == target:
            print("match found @1")
            targetfound = True
            recipes = len(scorelist) - targetLen
        
        sublist = scorelist[-(targetLen+1):-1]
        checker = ''.join(str(x) for x in sublist)
        if checker == target:
            print("match found @2")
            targetfound = True
            recipes = len(scorelist) - (targetLen+1)

print(str("left: " + str(recipes)))