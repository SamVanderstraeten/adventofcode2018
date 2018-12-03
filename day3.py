file = open("input.txt", "r")

lines = file.readlines()

ids = {}
field = {}
for line in lines:
    #1 @ 1,3: 4x4
    line = line.strip()
    spl = line.split(" @ ")
    sid = spl[0]
    info = spl[1].split(": ")
    loc = info[0].split(",")
    size = info[1].split("x")

    ids[sid] = False # Has overlap?

    for col in range(0, int(size[0])):
        for row in range(0, int(size[1])):
            sq_x = int(loc[0]) + col
            sq_y = int(loc[1]) + row

            loc_key = "(" + str(sq_x) + "," + str(sq_y) + ")"

            if loc_key in field:
                # field[loc_key] += 1
                ids[sid] = True # Has overlap!
                ids[field[loc_key]] = True
            else:
                #field[loc_key] = 1
                field[loc_key] = sid

    #print(field)


'''count = 0
for k in field:
    if field[k] > 1:
        count += 1

print(str(count))'''

for sid in ids:
    if ids[sid] == False:
        print(sid)