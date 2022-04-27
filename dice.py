import random
import numpy as np
import matplotlib.pyplot as plt

def dice_check(rolls, skill): #roll is number of D6 dice rolled   dice equal to of greater than skill show as hits.   6's are crits
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

    results['Crits'] = results[6]
    results['Hit %'] = results['Hits'] / results['Rolls']
    results['Crit %'] = results['Crits'] / results['Rolls'] 

    #print(dice_rolls)    
    #print(results)
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

guardsmen1 = {'M':6 , 'APL':2, 'GA':2, 'BA':4, 'WA':3, 'BS':4, 'WS':4, 'BD':2, 'BCD':3, 'WD':2, 'WCD':3, 'DF':3, 'SV':5, 'W':7}
guardsmen2 = {'M':6 , 'APL':2, 'GA':2, 'BA':4, 'WA':3, 'BS':4, 'WS':4, 'BD':2, 'BCD':3, 'WD':2, 'WCD':3, 'DF':3, 'SV':5, 'W':7}



trials = 100000

damage = bytearray(trials)

for x in range(trials):
    damage[x] = shooting_phase(guardsmen1, guardsmen2)


 

plt.hist(damage, histtype='stepfilled')
plt.show() 


