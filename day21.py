file = open("input.txt", "r")
lines = file.readlines()

eqrrcount = 0
eqrrs = []
done = False

def addr(registers, i):
    registers[i[3]] = registers[i[1]] + registers[i[2]]
    return registers

def addi(registers, i):
    registers[i[3]] = registers[i[1]] + i[2]
    return registers

def mulr(registers, i):
    registers[i[3]] = registers[i[1]] * registers[i[2]]
    return registers

def muli(registers, i):
    registers[i[3]] = registers[i[1]] * i[2]
    return registers

def banr(registers, i):
    registers[i[3]] = registers[i[1]] & registers[i[2]]
    return registers

def bani(registers, i):
    registers[i[3]] = registers[i[1]] & i[2]
    return registers

def borr(registers, i):
    registers[i[3]] = registers[i[1]] | registers[i[2]]
    return registers

def bori(registers, i):
    registers[i[3]] = registers[i[1]] | i[2]
    return registers

def setr(registers, i):
    registers[i[3]] = registers[i[1]]
    return registers

def seti(registers, i):
    registers[i[3]] = i[1]
    return registers

def gtir(registers, i):
    registers[i[3]] = 1 if i[1] > registers[i[2]] else 0
    return registers

def gtri(registers, i):
    registers[i[3]] = 1 if registers[i[1]] > i[2] else 0
    return registers

def gtrr(registers, i):
    registers[i[3]] = 1 if registers[i[1]] > registers[i[2]] else 0
    return registers

def eqir(registers, i):
    registers[i[3]] = 1 if i[1] == registers[i[2]] else 0
    return registers

def eqri(registers, i):
    registers[i[3]] = 1 if registers[i[1]] == i[2] else 0
    return registers

def eqrr(registers, i):
    global eqrrcount
    global firstEQRR
    global eqrrs
    global done
    eqrrcount += 1
       
    #print("EQRR " + str(eqrrcount))
    print("EQRR " + str(eqrrcount))
    if registers[3] in eqrrs:
        #registers[3] is the first double > last added = answer
        print("WE DONE")
        print(">> " + str(eqrrs[-1]))
        done = True  
    else:
        eqrrs.append(registers[3])

    registers[i[3]] = 1 if registers[i[1]] == registers[i[2]] else 0
    return registers

banaan = {'addr': addr, "addi": addi, "mulr": mulr, "muli": muli, "banr": banr, "bani": bani, "borr": borr, "bori": bori, "setr": setr, "seti": seti, "gtir": gtir, "gtri": gtri, "gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr}

def execute(instruction):
    global eqrrcount
    global firstEQRR
    global prevEQRR
    global done

    op = instruction[0]
    inA = instruction[1]
    inB = instruction[2]
    outC = instruction[3]
    
    if op == "addr":
        registers[outC] = registers[inA] + registers[inB]
    elif op == "addi":
        registers[outC] = registers[inA] + inB
    elif op == "mulr":
        registers[outC] = registers[inA] * registers[inB]
    elif op == "muli":
        registers[outC] = registers[inA] * inB
    elif op == "banr":
        registers[outC] = registers[inA] & registers[inB]
    elif op == "bani":
        registers[outC] = registers[inA] & inB
    elif op == "borr":
        registers[outC] = registers[inA] | registers[inB]
    elif op == "bori":
        registers[outC] = registers[inA] | inB
    elif op == "setr":
        registers[outC] = registers[inA]
    elif op == "seti":
        registers[outC] = inA
    elif op == "gtir":
        registers[outC] = 1 if inA > registers[inB] else 0
    elif op == "gtri":
        registers[outC] = 1 if registers[inA] > inB else 0
    elif op == "gtrr":
        registers[outC] = 1 if registers[inA] > registers[inB] else 0
    elif op == "eqir":
        registers[outC] = 1 if inA == registers[inB] else 0
    elif op == "eqri":
        registers[outC] = 1 if registers[inA] == inB else 0
    elif op == "eqrr":
        eqrrcount += 1
       
        print("EQRR " + str(eqrrcount))
        print(registers[3])
        if firstEQRR == registers[3]:
            print("WE DONE")
            print("###############################################################################")
            done = True  
        elif firstEQRR == -1:
            firstEQRR = registers[3]

        registers[outC] = 1 if registers[inA] == registers[inB] else 0
  

ipRegister = -1
instructionset = []
registers = [0,0,0,0,0,0]

for l in range(0, len(lines)):
    line = lines[l].strip()
    if line.startswith("#"):
        ipRegister = int(line.split()[1])
        continue
    
    instruction = line.split()
    for i in range(1, len(instruction)):
        instruction[i] = int(instruction[i])
    instructionset.append(instruction)

ip = 0
count = 0

#while ip >= 0 and ip < len(instructionset) and not done:
while not done:    
    registers[ipRegister] = ip
    #execute(instructionset[ip])
    registers = banaan[instructionset[ip][0]](registers, instructionset[ip])
    ip = registers[ipRegister] + 1
    #count += 1

    #print(registers)
    #input("COntiineeu?")

print("Done")