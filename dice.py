import random
import numpy as np
import matplotlib.pyplot as plt

def dice_check(rolls, skill, reroll = 0, crit_fish = 0): #roll is number of D6 dice rolled   dice equal to of greater than skill show as hits.   6's are crits
    #print('Rolls:', end='')
    #print(rolls)
    #print('Skill:', end='')
    #print(skill)
    
    
    rolls = int(rolls)
    
    if rolls <= 0 or skill < 1 or skill > 6:
        print('Invalid Range')
        return
    
    dice_rolls = {} #list of raw dice roll data
    results = {'Rolls':0, 'Hits':0, 'Crits':0, 'Hit %':0, 'Crit %':0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0 }
    results['Rolls'] = rolls

    for n in range(rolls):
        single_roll = random.randint(1,6) #D6 dice
        dice_rolls[n] = single_roll
        results[single_roll] += 1
        if single_roll >= skill:
            results['Hits'] += 1
    
    if reroll != 0 and crit_fish == 0:
        to_reroll = 0 
        for n in range(1, reroll + 1):
            to_reroll += results[n]
            results[n] = 0
        for n in range(to_reroll):
            single_roll = random.randint(1,6) #D6 dice
            dice_rolls[n] = single_roll
            results[single_roll] += 1
            if single_roll >= skill:
                results['Hits'] += 1


    if crit_fish == 1 and reroll == 0:
        for n in range(1,6):
            results[n] = 0
        for n in range(rolls - results[6]):
            single_roll = random.randint(1,6) #D6 dice
            dice_rolls[n] = single_roll
            results[single_roll] += 1
            if single_roll >= skill:
                results['Hits'] += 1

    results['Crits'] = results[6]
    results['Hit %'] = results['Hits'] / results['Rolls']
    results['Crit %'] = results['Crits'] / results['Rolls'] 

    #print(dice_rolls)    
    print(results)
    return(results)

def get_attacks():
    print("Attack Dice:", end='')
    atk_num = input()
  
    print("Defense Dice:", end='')
    def_num = input()

    print(atk_num,def_num)
    return(atk_num,def_num)

def shooting_phase(attacker, defender):
    #print(attacker)
    #print(defender)

    attack_dice = dice_check(attacker['BA'], attacker['BS'])
    defense_dice = dice_check(defender['DF'], defender['SV'])
    
    #print(attack_dice)
    #print(defense_dice)

    # one defense crit can counter one attack crit
    if attack_dice['Crits'] != 0 and defense_dice['Crits'] != 0:
        if attack_dice['Crits'] >= defense_dice['Crits']:
            attack_dice['Crits'] -= defense_dice['Crits']
            defense_dice['Crits'] = 0
        elif attack_dice['Crits'] < defense_dice['Crits']:
            defense_dice['Crits'] -= attack_dice['Crits']
            attack_dice['Crits'] = 0
    #print(attack_dice['Crits'],defense_dice['Crits'])
    
    # one defense hit can counter one attack hit
    if attack_dice['Hits'] != 0 and defense_dice['Hits'] != 0:
        if attack_dice['Hits'] >= defense_dice['Hits']:
            attack_dice['Hits'] -= defense_dice['Hits']
            defense_dice['Hits'] = 0
        elif attack_dice['Hits'] < defense_dice['Hits']:
            defense_dice['Hits'] -= attack_dice['Hits']
            attack_dice['Hits'] = 0
    #print(attack_dice['Hits'],defense_dice['Hits'])

    # one defense crit can counter one attack hit
    if attack_dice['Hits'] != 0 and defense_dice['Crits'] != 0:
        if attack_dice['Hits'] >= defense_dice['Crits']:
            attack_dice['Hits'] -= defense_dice['Crits']
            defense_dice['Crits'] = 0
        elif attack_dice['Hits'] < defense_dice['Crits']:
            defense_dice['Crits'] -= attack_dice['Hits']
            attack_dice['Hits'] = 0
    # two defense hits can counter one attack crit
    if attack_dice['Crits'] != 0 and defense_dice['Hits'] != 0:
        if (attack_dice['Crits'] * 2) >= defense_dice['Hits']:
            attack_dice['Crits'] -= defense_dice['Hits'] // 2
            defense_dice['Hits'] = 0 #not perfect  doesn't carry remainder
        elif (attack_dice['Crits'] * 2) < defense_dice['Hits']:
            defense_dice['Hits'] -= attack_dice['Crits'] * 2
            attack_dice['Crits'] = 0
    #print(attack_dice['Crits'],attack_dice['Hits'])
    #print(defense_dice['Crits'], defense_dice['Hits'])

    damage = attack_dice['Crits'] * attacker['BCD'] + attack_dice['Hits'] * attacker['BD']

    #print(damage)
    return(damage)

def prob_ranged_death(attacker, defender, trials = 10000):
    if trials <= 0:
        print("invalid trials number")
        return
    wounds = defender['W']
    dmg_dict = {}
    results = {}

    for n in range(0, wounds + 1):
        dmg_dict[n] = 0
    for x in range(trials):
        damage = shooting_phase(attacker, defender)
        if damage < wounds:
            dmg_dict[damage] += 1
        else:
            dmg_dict[wounds] += 1

    for n in range(0, wounds + 1):
        results[n] = round(dmg_dict[n] /trials * 100, 2)

    print(results)
    #print(dmg_dict)
    return(results)






guardsmen1 = {'M':6 , 'APL':2, 'GA':2, 'BA':4, 'WA':3, 'BS':4, 'WS':4, 'BD':2, 'BCD':3, 'WD':2, 'WCD':3, 'DF':3, 'SV':5, 'W':7}
kommando = {'M':6 , 'APL':2, 'GA':1, 'BA':5, 'WA':3, 'BS':4, 'WS':3, 'BD':3, 'BCD':4, 'WD':3, 'WCD':4, 'DF':3, 'SV':5, 'W':10}

#dice_check(100000,4)

data = prob_ranged_death(kommando, guardsmen1)



x = list(data.keys())
y = list(data.values())

# plot
fig, ax = plt.subplots()

ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

plt.show()

'''
trials = 10

damage = bytearray(trials)

for x in range(trials):
    damage[x] = shooting_phase(guardsmen1, kommando)

plt.hist(damage, histtype='stepfilled')
plt.show() 

'''
