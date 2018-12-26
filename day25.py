import math

file = open("input.txt", "r")
lines = file.readlines()

# 4D distance
def dist(p1, p2):
    return int(math.fabs(p1[0]-p2[0]) + math.fabs(p1[1]-p2[1]) + math.fabs(p1[2]-p2[2]) + math.fabs(p1[3]-p2[3]))

# parse
points = []
for l in range(0, len(lines)):
    line = lines[l].strip()
    coord = [int(x) for x in line.split(",")]
    points.append(coord)

# divide in constellations
constellations = []
for point in points:
    cs = []
    for c in range(0, len(constellations)):
        constellation = constellations[c]
        for cp in constellation:
            if dist(point, cp) <= 3:
                cs.append(c)
                break
    
    if len(cs) == 0: #add new constellation
        constellations.append([point])
    elif len(cs) == 1: #add point to constellation
        constellations[cs[0]].append(point)
    else: #merge constellations
        newconstellations = []
        for r in range(0, len(constellations)):
            if not r in cs:
                newconstellations.append(constellations[r])

        combo = [point]
        for c in cs:
            combo += constellations[c]
        newconstellations.append(combo)
        constellations = newconstellations

print("#constellations: " + str(len(constellations)))

# 624 too high
# 342 too low