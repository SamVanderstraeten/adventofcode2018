file = open("input.txt", "r")
line = file.readlines()[0]
numbers = line.split(" ")

def parseNode(i=0):
    numChilds = int(numbers[i])
    numMeta = int(numbers[i+1])
    currentChild = i+2
    nodeValue = 0
    childNodeValue = 0
    childNodeValues = {}
    for n in range(0, numChilds):
        (childNodeValue, currentChildDelta) = parseNode(currentChild)
        currentChild += currentChildDelta
        childNodeValues[(n+1)] = childNodeValue
    for m in range(0, numMeta):
        if numChilds == 0:
            nodeValue += int(numbers[currentChild+m])
        elif int(numbers[currentChild+m]) <= numChilds:
            nodeValue += childNodeValues[int(numbers[currentChild+m])]
    return (nodeValue, currentChild-i+numMeta)

(value, count) = parseNode()
print(str(value))