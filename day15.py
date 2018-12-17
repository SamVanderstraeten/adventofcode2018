import sys

file = open("input.txt", "r")
lines = file.readlines()

grid = [[] for i in range(0,len(lines))]
units = []
GOBLIN_STRENGTH = 3
ELVEN_STRENGTH = 10

''' A* implementation '''
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    neverland = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0 and len(open_list) < 1500:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f: #was f
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1][1:] # Return reversed path

        # Generate children
        children = []
        for new_position in [(-1,0), (0,-1), (0,1), (1,0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            readorder_rowbonus = 5 + 2*(child.position[0] - current_node.position[0])
            readorder_colbonus = 3 + 1*(child.position[1] - current_node.position[1])
            child.g = current_node.g + 1

            # heuristic, this is where it's at... force readorder movement here: in order of priority: up (-1,0) - left (0,-1) - right (0,1) - down (1,0)
            #child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1]) + readorder_rowbonus + readorder_colbonus
            #child.h = 0
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Child already visited
            if child in neverland:
                continue

            # Add the child to the open list
            open_list.append(child)
            neverland.append(child)

''' End of A* implementation '''

def printStatus(printUnits=False, shadow=False):
    sortUnits()
    for row in range(0, len(grid)):
        for col in range(0, len(grid[row])):
            uk = '.'
            for unit in units:
                if unit[0] == row and unit[1] == col:
                    uk = unit[3]
                    break
            if not uk == '.':
                sys.stdout.write(str(uk))            
            elif grid[row][col] == 1:
                sys.stdout.write("#")
            else:
                sys.stdout.write(".")
            sys.stdout.write(" ")
        print("")

    if printUnits:        
        for unit in units:
            if unit[3] == 2:
                sys.stdout.write("ELF ")
            else:
                sys.stdout.write("GOB ")
            sys.stdout.write(str(unit[2]) + " HP")
            print("")
        totalHP = 0
        for unit in units:
            if unit[2] > 0:
                totalHP += unit[2]
        result = (rounds)*totalHP
        print("Result: " + str(result))

    # print grid state
    if shadow:
        print("Shadow")
        for row in range(0, len(grid)):
            for col in range(0, len(grid[row])):
                if grid[row][col] == 1:
                    sys.stdout.write("#")
                else:
                    sys.stdout.write(".")
                sys.stdout.write(" ")
            print("")

def sortUnits():
    global units
    units = sorted(units, key=lambda tup: tup[1])
    units = sorted(units, key=lambda tup: tup[0])

def sortByReadingOrder(stuff): # same as sort units but with given list of tuples (e.g. locations)
    stuff = sorted(stuff, key=lambda tup: tup[1])
    stuff = sorted(stuff, key=lambda tup: tup[0])
    return stuff

def sortByHitpoints(stuff): # same as sort units but with given list of tuples (e.g. locations)
    stuff = sorted(stuff, key=lambda tup: tup[2])
    return stuff

def unitOn(row, col):
    for u in units:
        if u[0] == row and u[1] == col and u[2] > 0:
            return True
    return False

def getAdjs(target):
    adjs = []
    for row in range(-1,2):
        for col in range(-1,2):
            if abs(row)+abs(col) == 1:
                adjRow = target[0] + row
                adjCol = target[1] + col                
                if unit[2] > 0 and  grid[adjRow][adjCol] == 0 and not unitOn(adjRow, adjCol):
                    adjs.append((adjRow, adjCol))
    return sortByReadingOrder(adjs)

def getSurrounding(attacker) :
    surr = []
    for row in range(-1,2):
        for col in range(-1,2):
            if abs(row)+abs(col) == 1:
                adjRow = attacker[0] + row
                adjCol = attacker[1] + col 
                for unit in units:
                    if unit[2] > 0 and unit[0] == adjRow and unit[1] == adjCol:
                        surr.append(unit)
    return sortByHitpoints(surr)

def find_path(loc1,loc2):
    start = (loc1[0],loc1[1])
    end = (loc2[0],loc2[1])
    path = astar(grid, start, end)
    return path

def findTarget(attacker):
    minsteps = 999999
    bestpath = None
    for unit in units:
        if unit[2] > 0 and not unit[3] == attacker[3]: # other faction
            adjs = getAdjs(unit)
            for adj in adjs:
                path = find_path(attacker, adj)
                if path != None and len(path) < minsteps:
                    minsteps = len(path)
                    bestpath = path
    return bestpath

def allEnemiesDead(theFaction):
    for unit in units:
        if not unit[3] == theFaction:
            if unit[2] > 0:
                return False
    return True

# parse grid and unit locations
for y in range(0, len(lines)):
    line = lines[y].strip()
    for x in range(0, len(line)):
        t = line[x]
        if t == "E":
            units.append((y,x,200,2))
            grid[y].append(1)
        elif t == "G":
            units.append((y,x,200,3))
            grid[y].append(1)
        elif t == "#":
            grid[y].append(1)   # 1 is wall
        else:
            grid[y].append(0)   # 0 is empty

        

enemyFound = True
rounds = 0
continu = '.'
printStatus()
while enemyFound:
    print("Round " + str(rounds+1))
    units = sortByReadingOrder(units)
    for u in range(0, len(units)):
        unit = units[u]
        if unit[2] > 0: # if unit died by attack of an enemy this round, skip (will be deleted after round)
            alreadyAttacked = False

            # if already adjacent to enemy >> attack
            adjs = getSurrounding(unit)
            for adj in adjs:
                if (not alreadyAttacked) and (not adj[3] == unit[3]):
                    for eu in range(0, len(units)):
                        eunit = units[eu]
                        if eunit[0] == adj[0] and eunit[1] == adj[1]: # enemy within attacking range!
                            attackpower = GOBLIN_STRENGTH
                            if unit[3] == 2: # elf
                                attackpower = ELVEN_STRENGTH
                            units[eu] = (eunit[0], eunit[1], eunit[2]-attackpower, eunit[3])
                            alreadyAttacked = True

                            if units[eu][2] <= 0:
                                grid[units[eu][0]][units[eu][1]] = 0  # clear from grid
                            break              

            # if unit could not attack directly, move and then check for attack
            if not alreadyAttacked:
                # find path to nearest
                path = findTarget(unit)
                if path == None:
                    if allEnemiesDead(unit[3]):
                        enemyFound = False
                    else:
                        # No valid path found
                        print("Cant' move... no valid path")
                else:
                    move = path[0]
                    grid[units[u][0]][units[u][1]] = 0 # clear old position in grid
                    units[u] = (move[0], move[1], unit[2], unit[3]) 
                    grid[move[0]][move[1]] = 1 # set new position in grid 
                    
                unit = units[u]
                # if now adjacent to enemy >> attack
                adjs = getSurrounding(unit)
                for adj in adjs:
                    if (not alreadyAttacked) and (not adj[3] == unit[3]):
                        for eu in range(0, len(units)):
                            eunit = units[eu]
                            if eunit[0] == adj[0] and eunit[1] == adj[1]: # enemy within attacking range!
                                attackpower = GOBLIN_STRENGTH
                                if unit[3] == 2: # elf
                                    attackpower = ELVEN_STRENGTH
                                units[eu] = (eunit[0], eunit[1], eunit[2]-attackpower, eunit[3])
                                alreadyAttacked = True

                                if units[eu][2] <= 0:
                                    grid[units[eu][0]][units[eu][1]] = 0  # clear from grid
                                break
    
    to_remove = []
    for u in range(0, len(units)):
        if units[u][2] <= 0:
            to_remove.append(u)
    for r in range(0, len(to_remove)):
        removalIndex = max(to_remove)
        del units[removalIndex]
        to_remove.remove(removalIndex)

    printStatus(printUnits=True)
    print("LEFT: " + (str(len(units))))
    #continu = input("Continue?")
    if enemyFound:
        rounds += 1

printStatus(printUnits=True)
totalHP = 0
for unit in units:
    if unit[2] > 0:
        totalHP += unit[2]
result = (rounds)*totalHP
print(str(rounds))
print(totalHP)
print("Result: " + str(result))

#remaining health should be 1076 instead of 1049
