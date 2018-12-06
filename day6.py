file = open("input.txt", "r")
limit = 10000

lines = file.readlines()

max = 0

coords = {}
ix = 0
for line in lines:
    spl = line.split(", ")
    x = int(spl[0])
    y = int(spl[1])

    if x > max:
        max = x
    if y > max:
        max = y
    
    coords[ix] = [x, y]
    ix += 1

scores = {}
count = 0
for x in range(0, max):
    for y in range(0, max):
        sumdist = 0
        for c in range(0, len(coords)):
            coord = coords[c]
            dist = abs(coord[0] - x) + abs(coord[1] - y)
            sumdist += dist

        #print(str(sumdist))
            
        if sumdist < limit:
            count += 1

print(str(count))

#10097 too high
