file = open("input.txt", "r")
lines = file.readlines()

def execute(instruction):
    global firstEQRR, prevEQRR

    op = instruction[0]
    inA = int(instruction[1])
    inB = int(instruction[2])
    outC = int(instruction[3])
    
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
       
        print("EQRR")
        print(registers[3])
        print("diff: " + str(registers[3] - prevEQRR))
        prevEQRR = registers[3]
        if firstEQRR == registers[3]:
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
done = False
firstEQRR = -1
prevEQRR = -1
while ip >= 0 and ip < len(instructionset) and not done:
    
    registers[ipRegister] = ip
    execute(instructionset[ip])
    ip = registers[ipRegister]
    ip += 1
    count += 1

    #print(registers)
    #input("COntiineeu?")

print("Done")