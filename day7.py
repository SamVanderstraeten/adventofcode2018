import collections

file = open("input.txt", "r")

lines = file.readlines()

done = []
prq = {}

workers = [[],[],[],[],[]]

def goToWork(task):
    for i in range(0,len(workers)):
        worker = workers[i]
        if len(worker) == 0:
            print("worker " + str(i) + " started on " + post)
            # fill
            for i in range(0, getDuration(task)):
                worker.append(task)
            break

def getDuration(task):
    num = ord(task) - 64
    return num + 60

# initialize (which prerequisites are needed for a certain step): A -> (needs) -> [B, C, D]
# This way, we can check if all needed steps are done (if so, we can execute 'post' task)
for line in lines:
    spl = line.split(" ")
    pre = spl[1]
    post = spl[-3]

    if not pre in prq:
        prq[pre] = []
    if not post in prq:
        prq[post] = []

    prq[post].append(pre)

# Order keys alfabetically
prq = collections.OrderedDict(sorted(prq.items()))

ticks = 0
while len(done) < len(prq):    
    print("Tick #" + str(ticks))
    #find first available task
    for post in prq:

        # check if already being executed by workers
        workingonit = False
        for worker in workers:
            if post in worker:
                workingonit = True

        if (not post in done) and (not workingonit):
            allDone = True
            for pre in prq[post]:
                if not pre in done:
                    allDone = False
            if allDone:
                #add this one to a worker that is idling
                goToWork(post)

    # work, work!
    for i in range(0, len(workers)):
        worker = workers[i]
        if len(worker) > 0:
            workertask = worker[0]
            del worker[-1]
            if len(worker) == 0:
                print("worker " + str(i) + " is done with " + workertask)
                done.append(workertask)

    ticks += 1

print("Ticks required: " + str(ticks))