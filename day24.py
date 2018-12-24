from collections import namedtuple
import math

immune_file = open("input.txt", "r")
infection_file = open("input2.txt", "r")
immune_lines = immune_file.readlines()
infection_lines = infection_file.readlines()

orig = []
allgroups = []

#boost = 0
boost = 59
# 60 0 wins (1005 left, too HIGH)
#886too high
# 55 1 wins

class Group():
    turn = False
    chosen = False
    target = None
    unit_count = 0
    initiative = 0
    damage = 0
    damage_type = ""
    faction = -1
    hp = -1
    weakness = []
    immunity = []

    def __init__(self, faction):
        self.faction = faction

    def getEffectivePower(self):
        return self.unit_count * self.damage

    def print(self):
        print(str(self.faction) + " | units:" + str(self.unit_count) + ", DMG:" + str(self.damage) + ", HP: " + str(self.hp) + ", EP: " + str(self.getEffectivePower()) + ", IN: " + str(self.initiative) + ", type: " + self.damage_type + ", weak: " + str(self.weakness) + ", immu:" + str(self.immunity))

def resetTurn(endturn=False):
    for u in allgroups:
        u.turn = False
        u.chosen = False
        if endturn:
            u.target = None

def parseGroups(lines, faction, dmg_boost=0):
    groups = []
    for l in range(1, len(lines)):
        if l == 0:
            continue
        
        group = Group(faction)
        line = lines[l].strip()
        group_data = line.split()
        group.faction = faction
        group.turn = False
        group.chosen = False
        group.target = None
        group.unit_count = int(group_data[0])
        group.hp = int(group_data[4])
        group.initiative = int(group_data[-1])
        group.damage = int(group_data[-6]) + dmg_boost
        group.damage_type = group_data[-5]

        #weaknesses and immunities
        sp = line.split("(")
        if len(sp) > 1:
            specials = sp[1].split(")")[0].split("; ")
            for special in specials:
                spl = special.split()
                types = spl[2:]
                typelist = []
                for t in range(0, len(types)):
                    ttype = types[t]
                    if t < len(types) - 1:
                        typelist.append(ttype[0:-1])
                    else:
                        typelist.append(ttype)

                if spl[0] == "immune":                
                    group.immunity = typelist
                elif spl[0] == "weak":
                    group.weakness = typelist

        groups.append(group)
    return groups

def countFactionGroups(faction):
    count = 0
    for u in allgroups:
        if u.faction == faction:
            count += 1
    return count

def findHighestEffective():
    best = None
    for u in allgroups:
        if (not u.turn) and (best == None or (u.getEffectivePower() > best.getEffectivePower()) or (u.getEffectivePower() == best.getEffectivePower() and u.initiative > best.initiative)):
            best = u
    return best

def findHighestInitiative():
    highest = 0
    best = None
    for u in allgroups:
        if (not u.turn) and (u.initiative > highest):
            highest = u.initiative
            best = u
    return best

def getDamage(attacker, target):
    damage = attacker.getEffectivePower()
    if attacker.damage_type in target.weakness:
        damage *= 2
    elif attacker.damage_type in target.immunity:
        damage = 0
    return damage

boost = 0
immuneWon = False
while not immuneWon:
    boost += 1
    print("BOOST: " + str(boost))
    allgroups = []
    allgroups += parseGroups(immune_lines, 0, dmg_boost=boost)
    allgroups += parseGroups(infection_lines, 1)

    roundCount = 0

    while countFactionGroups(0) > 0 and countFactionGroups(1) > 0:
        #print("Round " + str(roundCount+1))

        # target selection
        resetTurn(endturn=True)
        for i in range(0, len(allgroups)):
            current = findHighestEffective()
            mostDamage = 0
            bestTarget = None

            if current == None:
                continue

            for enemy in allgroups:
                if enemy.faction == current.faction:
                    continue
                if enemy.chosen:
                    continue
                if enemy.unit_count <= 0:
                    continue
                
                #future_damage = enemy.hp * (getDamage(current, enemy) // enemy.hp) #real dmg that is done to units
                future_damage = getDamage(current, enemy)
                if future_damage > 0:
                    if bestTarget == None or future_damage > mostDamage or (future_damage == mostDamage and enemy.getEffectivePower() > bestTarget.getEffectivePower()) or (future_damage == mostDamage and enemy.getEffectivePower() == bestTarget.getEffectivePower() and enemy.initiative > bestTarget.initiative):
                        bestTarget = enemy
                        mostDamage = future_damage
            current.turn = True
            current.target = bestTarget
            if not bestTarget == None:
                bestTarget.chosen = True

        # attack
        resetTurn()
        totalKills = 0
        for i in range(0, len(allgroups)):
            current = findHighestInitiative()
            if current.unit_count > 0:
                if not current.target == None:
                    #print("Dealing damage: " + str(getDamage(current, current.target)))
                    unitsKilled = getDamage(current, current.target) // current.target.hp
                    current.target.unit_count -= unitsKilled
                    totalKills += unitsKilled
                    #print("Killed " + str(unitsKilled) + " units")
                
            current.turn = True

        # remove defeated enemies
        rm = []
        for u in range(0, len(allgroups)):
            unit = allgroups[u]
            if unit.unit_count <= 0:
                rm.append(u)
        for r in range(0,len(rm)):
            rmv = max(rm)
            del allgroups[rmv]
            rm.remove(rmv)     

        if totalKills == 0:
            print("Stalemate, move on...")  
            # make sure it doesnt stop
            allgroups[0].faction = 1
            break

        roundCount += 1
        #print("")

    print("WINNING FACTION: " + str(allgroups[0].faction))
    totalRemaining = 0
    for u in allgroups:
        u.print()
        totalRemaining += u.unit_count
    print("Unit count: " + str(totalRemaining))
    immuneWon = allgroups[0].faction == 0