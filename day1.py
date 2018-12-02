file = open("input.txt", "r")

lines = file.readlines()
freq = 0
freqs = dict()
bingo = 999999
while bingo == 999999:
    for line in lines:
        freq += int(line)
        if freq in freqs:
            bingo = freq
            break
        else:
            freqs[freq] = 1
print(str(bingo))