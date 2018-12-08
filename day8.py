file = open("input.txt", "r")

lines = file.readlines()
line = lines[0]
numbers = line.split(" ")
metas = []

def parseNode(i=0):
    numChilds = int(numbers[i])
    numMeta = int(numbers[i+1])
    currentChild = i+2
    for n in range(0, numChilds):
        currentChild += parseNode(currentChild)
    for m in range(0, numMeta):
        metas.append(int(numbers[currentChild+m]))
    return currentChild-i+numMeta

metasum = 0
parseNode()
for m in metas:
    metasum += m
print(str(metasum))

