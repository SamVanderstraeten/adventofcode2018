file = open("input.txt", "r")

lines = file.readlines()
l = lines[0]

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
best = 10000000
bestic = '.'
for ic in chars:

    print("Calculating score for " + ic.upper())

    line = []
    for c in l:
        if (not (c.upper() == ic.upper())):
            line.append(c)

    i = 0
    while i < len(line):
        char = line[i]
        if char == '.':
            i += 1
        else:
            nextchar = '&'
            nextcharj = -1
            for j in range(i+1, len(line)):
                if not line[j] == '.':
                    nextchar = line[j]
                    nextcharj = j
                    break
            if not (nextchar == '&'): # ended
                if (not (char == nextchar)) and (char.upper() == nextchar.upper()):
                    line[i] = '.'
                    line[nextcharj] = '.'
                    while line[i] == '.' and i > 0:
                        i -= 1
                else:
                    i += 1
            else:
                i += 1

    count = 0
    for c in line:
        if not c == '.':
            count += 1

    print("Score: " + str(count))

    if count < best:
        best = count
        bestic = ic
        print("Best so far!")

print(str(best) + ", " + bestic)