file = open("input.txt", "r")

lines = file.readlines()

'''totaltwos = 0
totalthrees = 0

for line in lines:
    twos = 0
    threes = 0
    for c in line:
        ccount = line.count(c)
        if ccount == 2:
            twos = 1
        elif ccount == 3:
            threes = 1
        line.replace(c,"")
    totaltwos += twos
    totalthrees += threes

print(totaltwos*totalthrees)'''

for line in lines:
    for line2 in lines:
        if not line == line2:
            for i in range(0, len(line)):
                subber = line[:i] + line[i+1:]
                for i2 in range(0, len(line2)):
                    subber2 = line2[:i2] + line2[i2+1:]
                    if subber == subber2:
                        print(">>> "+subber)
                
