file = open("testinput.txt", "r")

lines = file.readlines()
lines.sort()

guards = {} # int array of 60 indices > count sleeps over days

id = -1
sleepStart = -1
sleepEnd = -1

for line in lines:
    line = line.replace("[", "")
    line = line.replace("]", "")
    data = line.split(" ")

    if data[2] == "Guard":
        if sleepStart >= 0:
            sleepEnd = int(data[1].split(":")[1])
            for i in range(sleepStart, sleepEnd):
                guards[id][i] += 1
            sleepStart = -1
            sleepEnd = -1

        id = int(data[3].replace("#", ""))
        if not id in guards:
            guards[id] = {}
            for x in range(0,60):
                guards[id][x] = 0

    if data[2] == "falls":
        sleepStart = int(data[1].split(":")[1])

    if data[2] == "wakes":
        sleepEnd = int(data[1].split(":")[1])
        for i in range(sleepStart, sleepEnd):
            guards[id][i] += 1
        sleepStart = -1
        sleepEnd = -1

#most asleep
mostasleepguard = -1
maxasleep = -1
for guard in guards:
    asleep = 0
    for i in range(0,60):
        asleep += guards[guard][i]
    if asleep > maxasleep:
        maxasleep = asleep
        mostasleepguard = guard

#part 1
max = -1
maxid = -1
for i in range(0,60):
    if guards[mostasleepguard][i] > max:
        max = guards[mostasleepguard][i]
        maxid = i
print(maxid, mostasleepguard, (maxid*mostasleepguard))

#part 2

maxever = -1
bestguard = -1
bestminute = -1
for g in guards:
    for i in guards[g]:
        if guards[g][i] > maxever:
            bestguard = g
            bestminute = i
            maxever = guards[g][i]

print(bestguard, bestminute, maxever, (bestguard*bestminute))
