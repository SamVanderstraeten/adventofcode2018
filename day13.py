file = open("testinput.txt", "r")
lines = file.readlines()

tracks = []
carts = []
for y in range(0, len(lines)):
    line = lines[y]
    started = False
    for x in range(0,len(line)):
        t = line[x]        

        if t == "\\":
            started = True
        if t == "/":
            if not started: 
                # parse track
                track = [x, y]

                for i in range(x, len(line)):
                    t = line[i]
                    if t == "\\":
                        track.append(i)

                        for j in range(y, len(lines)):
                            t = lines[j][i]
                            if t == "/":
                                track.append(j)

                tracks.append(track)
            else:
                started = False

print("Found " + str(len(tracks)) + " tracks")

