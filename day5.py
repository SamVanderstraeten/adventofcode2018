file = open("input.txt", "r")

#9704

lines = file.readlines()
l = lines[0]



chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
best = 10000000
bestic = '.'
for ic in chars:

    line = []
    for c in l:
        if (not (c.upper() == ic.upper())):
            line.append(c)

    i = 0
    imax = 0
    while i < len(line):
        #print("i: " + str(i))

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
                #print(char, nextchar, char == nextchar, char.upper() == nextchar.upper())
                if (not (char == nextchar)) and (char.upper() == nextchar.upper()):
                    line[i] = '.'
                    line[nextcharj] = '.'
                    
                    #print(line)
                    while line[i] == '.' and i > 0:
                        i -= 1
                    '''if i == 0 and line[i] == '.':
                        for x in range(0, len(line)):
                            if line[x] == '.':
                                x += 1
                        i = x'''
                else:
                    i += 1
                    #print("Resume: " + str(i))
            else:
                i += 1
            
            if i > imax:
                imax = i
                print(ic + ">> " + str(imax) + "/" + str(len(line)))
                #print(line)

    count = 0
    for c in line:
        if not c == '.':
            count += 1

    if count < best:
        best = count
        bestic = ic

print(str(best) + ", " + bestic)