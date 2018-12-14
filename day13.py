import math

file = open("input.txt", "r")
lines = file.readlines()

carts = []
grid = [[] for i in range(0,len(lines))]

def isBefore(c1, c2):
    cart1 = carts[c1]
    cart2 = carts[c2]
    if cart1[1] < cart2[1]:
        return True
    elif cart1[1] == cart2[1]  and cart1[0] < cart2[0]:
        return True
    return False

def turn(velx, vely, dir):
    if dir == 'left':
        if velx == 0: # going up or down
            velx = vely
            vely = 0
        else: 
            vely = -1 * velx
            velx = 0
    elif dir == 'right':
        if velx == 0:
            velx = -1 * vely
            vely = 0
        else:
            vely = velx
            velx = 0
    return (velx, vely)

for y in range(0, len(lines)):
    line = lines[y].strip('\n')
    for x in range(0, len(line)):
        t = line[x]
        if t == "v":
            carts.append((x,y,0,1,0))
        elif t == "^":
            carts.append((x,y,0,-1,0))
        elif t == "<":
            carts.append((x,y,-1,0,0))
        elif t == ">":
            carts.append((x,y,1,0,0))
        grid[y].append(t)

collision = False
blackboxdata = []
count = 0

print("Initial state")
for cart in carts:
    print(cart)

while not collision:
    print("Tick #"+str(count+1))
    # update all carts
    for c in range(0, len(carts)):
        (posx, posy, velx, vely, cross) = carts[c]
        # update positions
        newPosX = posx + velx
        newPosY = posy + vely
        newVelX = velx
        newVelY = vely
        newCross = cross

        #carts[c] = (x + velx, y + vely, velx, vely, cross)
        # update velocities
        if grid[newPosY][newPosX] == "+":
            if cross == 0: # turn left
                (vx, vy) = turn(velx, vely, 'left')
                newVelX = vx
                newVelY = vy
            elif cross == 2:
                (vx, vy) = turn(velx, vely, 'right')
                newVelX = vx
                newVelY = vy
            newCross = (cross + 1) % 3
        elif grid[newPosY][newPosX] == "/":
            if velx == 0:
                (vx, vy) = turn(velx, vely, 'right')
                newVelX = vx
                newVelY = vy
            else:
                (vx, vy) = turn(velx, vely, 'left')
                newVelX = vx
                newVelY = vy
        elif grid[newPosY][newPosX] == "\\":
            if velx == 0:
                (vx, vy) = turn(velx, vely, 'left')
                newVelX = vx
                newVelY = vy
            else:
                (vx, vy) = turn(velx, vely, 'right')
                newVelX = vx
                newVelY = vy
        elif not (grid[newPosY][newPosX] == "|" or grid[newPosY][newPosX] == "-" or grid[newPosY][newPosX] == "<" or grid[newPosY][newPosX] == ">" or grid[newPosY][newPosX] == "v"or grid[newPosY][newPosX] == "^"):
            print("Off track!@"+grid[newPosY][newPosX]+"@!")

        carts[c] = (newPosX, newPosY, newVelX, newVelY, newCross)

    '''print("Iteration #" + str(count+1))
    for cart in carts:
        print(cart)'''

    # check for collisions
    cartremoval = []
    for c1 in range(0, len(carts)):
        for c2 in range(0, len(carts)):
            if not c1 == c2:                
                if isBefore(c1,c2):
                    futuredist = abs(carts[c1][0]+carts[c1][2]-carts[c2][0])+abs(carts[c1][1]+carts[c1][3]-carts[c2][1])
                    if futuredist == 0:
                        print("Pre-collision interception!")
                        print("Status:")
                        for c in range(0, len(carts)):
                            print(str(c), carts[c])

                        if not c1 in cartremoval:
                            cartremoval.append(c1)
                        if not c2 in cartremoval:
                            cartremoval.append(c2)
                if carts[c1][0] == carts[c2][0] and carts[c1][1] == carts[c2][1]:
                    print("Normal collision!")
                    print("Status:")
                    for c in range(0, len(carts)):
                        print(str(c), carts[c])

                    # remove collidiing carts                    
                    # collision = True
                    if not c1 in cartremoval:
                        cartremoval.append(c1)
                    if not c2 in cartremoval:
                        cartremoval.append(c2)

                    #blackboxdata = (carts[c1][0], carts[c1][1])

    rem = False
    if(len(cartremoval) > 0):
        rem = True
        print("Remove carts: ")
        print(cartremoval)
        print("Carts left: " + str(len(carts) - len(cartremoval)))
    for r in range(0, len(cartremoval)):
        m = max(cartremoval)
        del carts[m]
        cartremoval.remove(m)
    
    if count == 285:
        print("Status at 285 :")
        for c in range(0, len(carts)):
            print(str(c), carts[c])

    if(len(carts) == 1):
        collision = True
        blackboxdata = carts[0]

    '''test = input("Go on?")
    if test == "q" or test == "n":
        collision = True'''
    
    count += 1

print(blackboxdata)