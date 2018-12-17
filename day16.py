file = open("newinput.txt", "r")
lines = file.readlines()

file2 = open("testprog.txt", "r")
commands = file2.readlines()

opCodes = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]
registers_before = [0,0,0,0]
registers_after = [0,0,0,0]
instruction = [0,0,0,0]
registers = [0,0,0,0]

def execute():
    op = combos[int(instruction[0])]
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
        registers[outC] = 1 if registers[inA] == registers[inB] else 0

def isValidResult(op):
    global registers_before
    global registers_after
    result = [0,0,0,0]
    for r in range(0, len(registers_before)):
        result[r] = registers_before[r]
    
    opc = instruction[0]
    inA = instruction[1]
    inB = instruction[2]
    outC = instruction[3]
    
    if op == "addr":
        result[outC] = registers_before[inA] + registers_before[inB]
    elif op == "addi":
        result[outC] = registers_before[inA] + inB
    elif op == "mulr":
        result[outC] = registers_before[inA] * registers_before[inB]
    elif op == "muli":
        result[outC] = registers_before[inA] * inB
    elif op == "banr":
        result[outC] = registers_before[inA] & registers_before[inB]
    elif op == "bani":
        result[outC] = registers_before[inA] & inB
    elif op == "borr":
        result[outC] = registers_before[inA] | registers_before[inB]
    elif op == "bori":
        result[outC] = registers_before[inA] | inB
    elif op == "setr":
        result[outC] = registers_before[inA]
    elif op == "seti":
        result[outC] = inA
    elif op == "gtir":
        result[outC] = 1 if inA > registers_before[inB] else 0
    elif op == "gtri":
        result[outC] = 1 if registers_before[inA] > inB else 0
    elif op == "gtrr":
        result[outC] = 1 if registers_before[inA] > registers_before[inB] else 0
    elif op == "eqir":
        result[outC] = 1 if inA == registers_before[inB] else 0
    elif op == "eqri":
        result[outC] = 1 if registers_before[inA] == inB else 0
    elif op == "eqrr":
        result[outC] = 1 if registers_before[inA] == registers_before[inB] else 0

    for r in range(0, len(result)):
        if not result[r] == registers_after[r]:
            return False
    return True


def addPossibleCombos(number, opcodes):
    global combos
    if instruction[0] in possibleCombos:
        # only disection remains
        result = []
        for pos in possibleCombos[number]:
            if pos in opcodes:
                result.append(pos)
        possibleCombos[number] = result
    else:
        possibleCombos[number] = opcodes

def getValidOpCodes():
    count = 0
    possibilities = []
    for opcode in opCodes:
        if isValidResult(opcode):
            count += 1
            possibilities.append(opcode)
    addPossibleCombos(instruction[0], possibilities)
    return count
        

banaan = 0
alleindianen = 0
inner_count = 0
possibleCombos = {}
combos = {}

for line in lines:
    if inner_count == 0:
        registers_before = line.split(":")[1].split("[")[1].split("]")[0].split(", ")
        for i in range(0,len(registers_before)):
            registers_before[i] = int(registers_before[i])
    elif inner_count == 1:
        instruction = line.split(" ")
        for i in range(0,len(instruction)):
            instruction[i] = int(instruction[i])
    elif inner_count == 2:
        registers_after = line.split(":")[1].split("[")[1].split("]")[0].split(", ")
        for i in range(0,len(registers_after)):
            registers_after[i] = int(registers_after[i])

    inner_count = (inner_count + 1) % 4

    if inner_count == 3:
        validopcodes = getValidOpCodes()
        if validopcodes >= 3:
            banaan += 1
        alleindianen += 1


while len(combos) < 16:    
    for pc in possibleCombos:
        if len(possibleCombos[pc]) == 1:
            combos[pc] = possibleCombos[pc][0]
            for pc2 in possibleCombos:
                if combos[pc] in possibleCombos[pc2]:
                    possibleCombos[pc2].remove(combos[pc])

for c in combos:
    print(str(c) + ": " + combos[c])

for command in commands:
    instruction = command.split(" ")
    execute()

print(registers)




#print("Result: " + str(banaan) + "/" + str(alleindianen))