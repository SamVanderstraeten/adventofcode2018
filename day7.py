import collections

file = open("input.txt", "r")

lines = file.readlines()

done = []
prq = {}

for line in lines:
    spl = line.split(" ")
    pre = spl[1]
    post = spl[-3]

    if not pre in prq:
        prq[pre] = []
    if not post in prq:
        prq[post] = []

    prq[post].append(pre)

prq = collections.OrderedDict(sorted(prq.items()))
print(prq)

for i in range(0, len(prq)):
    for post in prq:
        if not post in done:
            allDone = True
            for pre in prq[post]:
                if not pre in done:
                    allDone = False
            if allDone:
                #execute this one
                done.append(post)
                break

solution = ''.join(done)
print(solution)
    



