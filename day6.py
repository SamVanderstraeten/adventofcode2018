file = open("input.txt", "r")
limit = 10000

lines = file.readlines()

bounds = 0
coords = {}
for i in range(0, len(lines)):
    spl = lines[i].split(", ")
    x = int(spl[0])
    y = int(spl[1])
    coords[i] = [x, y]

    if x > bounds or y > bounds:
        bounds = max(x,y)    
    
scores = {}
count = 0
for x in range(0, bounds):
    
    for y in range(0, bounds):
        sumdist = 0
        for c in range(0, len(coords)):
            coord = coords[c]
            dist = abs(coord[0] - x) + abs(coord[1] - y)
            sumdist += dist            
        if sumdist < limit:
            count += 1

print(str(count))