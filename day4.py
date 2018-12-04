file = open("testinput.txt", "r")

lines = file.readlines()
lines.sort()

guards = {} # int array of 60 indices > count sleeps over days

for line in lines:
    line = line.replace("[", "")
    line = line.replace("]", "")
    print(line)
    data = line.split(" ")

    id = -1
    sleepStart = -1
    sleepEnd = -1
    if data[2] == "Guard":
        print("guard")
        if sleepStart >= 0:
            sleepEnd = int(data[1].split(":")[1])
            for i in range(sleepStart, sleepEnd):
                guards[id][i] += 1
            sleepStart = -1
            sleepEnd = -1

        id = int(data[3].replace("#", ""))
        print(id)
        if not id in guards:
            guards[id] = {}
            for x in range(0,60):
                guards[id][x] = 0

    if data[2] == "falls":
        print("falls")
        sleepStart = int(data[1].split(":")[1])
        print(sleepStart)

    if data[2] == "wakes":
        print("wakes")
        sleepEnd = int(data[1].split(":")[1])
        print(sleepEnd)
        for i in range(sleepStart, sleepEnd):
            guards[id][i] += 1
        sleepStart = -1
        sleepEnd = -1

print(guards)
