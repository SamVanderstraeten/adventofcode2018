import math
import sys

file = open("input.txt", "r")
lines = file.readlines()

def dist(d1, d2):
    return math.fabs(d1[0] - d2[0]) + math.fabs(d1[1] - d2[1]) + math.fabs(d1[2] - d2[2])

strongest = []
weakest = []
bots = []
for line in lines:
    line = line.strip()
    spl = line.split(", ")
    coords = spl[0].split("=")[1][1:-1].split(",")
    strength = int(spl[1].split("=")[1])
    
    bot = [int(coords[0]), int(coords[1]), int(coords[2]), strength]
    bots.append(bot)

    if len(strongest) == 0 or strength > strongest[3]:
        strongest = bot 
    if len(weakest) == 0 or strength < weakest[3]:
        weakest = bot 

count = 0
for bot in bots:
    if dist(bot, strongest) <= strongest[3]:
        count += 1

print("Number: " + str(count))

# binary (?) search, find best regions and search deeper there
def dostuff():
    xs = [bot[0] for bot in bots]
    ys = [bot[1] for bot in bots]
    zs = [bot[2] for bot in bots]

    xs.append(0)
    ys.append(0)
    zs.append(0)

    box_size = 1
    while box_size < max(xs) - min(xs):
        box_size *= 2

    while True:
        target_count = 0
        best = None
        best_distance = -1
        for x in range(min(xs), max(xs) + 1, box_size):
            for y in range(min(ys), max(ys) + 1, box_size):
                for z in range(min(zs), max(zs) + 1, box_size):
                    count = 0
                    for bot in bots:
                        #dist = abs(x - bx) + abs(y - by) + abs(z - bz)
                        distance = dist([x,y,z],bot)
                        if math.floor((distance - bot[3]) / box_size) <= 0:
                            count += 1
                    if count > target_count:
                        target_count = count
                        best_distance = dist([x,y,z],[0,0,0])
                        best = (x, y, z)
                    elif count == target_count:
                        if best_distance == -1 or dist([x,y,z],[0,0,0]) < best_distance:
                            best_distance = dist([x,y,z],[0,0,0])
                            best = (x, y, z)

        if box_size == 1:
            return int(best_distance)
        else:
            xs = [best[0] - box_size, best[0] + box_size]
            ys = [best[1] - box_size, best[1] + box_size]
            zs = [best[2] - box_size, best[2] + box_size]
            box_size = box_size // 2

maximum = dostuff()
print("MAX: " + str(maximum))

# 87924130 too low