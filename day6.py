file = open("testinput.txt", "r")
limit = 32

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

for x in range(0, max):
    for y in range(0, max):
        mindist = 100000
        tie = False
        shortest = '.'
        for c in range(0, len(coords)):
            coord = coords[c]
            dist = abs(coord[0] - x) + abs(coord[1] - y)
            if dist == mindist:
                tie = True
            if dist < mindist:
                mindist = dist
                shortest = c
                tie = False
            
        if not tie:
            if shortest in scores:
                scores[shortest] += 1
            else:
                scores[shortest] = 1

        if x == 0 or y == 0 or x == max-1 or y == max -1:
            scores[shortest] = -100000

best = 0
for s in scores:
    if scores[s] > best:
        best = scores[s]

print(str(best))

#10097 too high
