
from filecmp import clear_cache
from multiprocessing.sharedctypes import Value
from optparse import Values
import random
from re import S
from secrets import choice
from tkinter import font
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 8})


#roll is number of D6 dice rolled   dice equal to of greater than skill show as hits.   6's are crits
def dice_check(rolls, skill, reroll = 0, crit_fish = 0): 
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
    #print(results)
    return(results)

#user input example 
def get_attacks():
    print("Attack Dice:", end='')
    atk_num = input()
  
    print("Defense Dice:", end='')
    def_num = input()

    print(atk_num,def_num)
    return(atk_num,def_num)

#Calculate one round of shooting
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

#not working
def melee_phase_brute_force_try(attacker, defender):
    
    attack_dice = dice_check(attacker['WA'], attacker['WS'])
    defense_dice = dice_check(defender['WA'], defender['WS'])

    attacker_total_dice = attack_dice['Hits'] + attack_dice['Crits']
    defender_total_dice = defense_dice['Hits'] + defense_dice['Crits']

    dice_dif = attacker_total_dice - defender_total_dice
    


    if dice_dif >= 0:
        iterations_x = attacker_total_dice - abs(dice_dif)
    else:
        iterations_x = defender_total_dice - abs(dice_dif)
    
    if iterations_x > 0:
        iterations_y = iterations_x - 1
    else:
        iterations_y = 0

    print('iteration')
    print(iterations_x)

    damage_totals ={}

    
    damage_pos_counter = 0

    for x in range(2**iterations_x):
        for y in range(2**iterations_y):
            print(x,y)

            #reset stats for another calculation
            attack_dmg = 0
            defense_dmg = 0
            
            attacker_hits = attack_dice['Hits']
            attacker_crits = attack_dice['Crits']
            attacker_total_dice = attacker_hits + attacker_crits
            
            defender_hits = defense_dice['Hits']
            defender_crits = defense_dice['Crits']
            defender_total_dice = defender_hits + defender_crits

            attacker_wounds = attacker['W']
            defender_wounds = defender['W']

            mask = 1
            
            print(attack_dmg,defense_dmg,attacker_hits,attacker_crits,defender_hits,defender_crits)

            while attacker_total_dice !=0 and defender_total_dice !=0: #only need to do checks when both players have dice left
                #attacker turn

                #is attacker dead
                if defense_dmg >= attacker_wounds:
                    print('attacker dead')
                    attacker_hits = 0
                    attacker_crits = 0
                
                #pick action
                if attacker_crits != 0 and defender_crits !=0 and (x & mask) == 0: #parry
                    defender_crits -= 1
                    attacker_crits -= 1
                elif attacker_hits != 0 and defender_hits !=0 and (x & mask) == 0: #parry
                    defender_hits -= 1
                    attacker_hits -= 1
                elif attacker_crits != 0: #attack
                    attack_dmg += attacker['WCD']
                    attacker_crits -= 1
                elif attacker_hits != 0: #attack
                    attack_dmg += attacker['WD']
                    attacker_hits -= 1   
                else:
                    pass


                print(attack_dmg,defense_dmg,attacker_hits,attacker_crits,defender_hits,defender_crits)
                
                #defender turn

                #is defender dead
                if attack_dmg >= defender_wounds:
                    print('defender dead')
                    defender_hits = 0
                    defender_crits = 0
                
                #pick action
                if defender_crits != 0 and attacker_crits !=0 and (y & mask) == 0: #parry
                    defender_crits -= 1
                    attacker_crits -= 1
                elif defender_hits != 0 and attacker_hits !=0 and (y & mask) == 0: #parry
                    defender_hits -= 1
                    attacker_hits -= 1
                elif defender_crits != 0: #attack
                    defense_dmg += defender['WCD']
                    defender_crits -= 1
                elif defender_hits != 0: #attack
                    defense_dmg += defender['WD']
                    defender_hits -= 1  
                else:
                    pass

                print(attack_dmg,defense_dmg,attacker_hits,attacker_crits,defender_hits,defender_crits)
                    
                #update leftover dice totals and move resolution round mask for bitwise compare
                attacker_total_dice = attacker_hits + attacker_crits
                defender_total_dice = defender_hits + defender_crits
                mask = mask * 2

                

            

            #add up leftover dice
            attack_dmg += (attacker_hits * attacker['WD'])
            attack_dmg += (attacker_crits * attacker['WCD'])
            attacker_hits = 0
            attacker_crits = 0
            defense_dmg += (defender_hits * defender['WD'])
            defense_dmg += (defender_crits * defender['WCD'])
            defender_hits = 0
            defender_crits = 0
            damage_totals[damage_pos_counter] = (attack_dmg,defense_dmg)
            damage_pos_counter += 1
            print(attack_dmg,defense_dmg,attacker_hits,attacker_crits,defender_hits,defender_crits)

    print(damage_totals)

    # Remove duplicate values in dictionary
    # Using dictionary comprehension
    temp = {val : key for key, val in damage_totals.items()}
    res = {val : key for key, val in temp.items()}
    
    # printing result 
    print()
    print(str(res)) 


#Calculates all possible outcomes
def melee_phase_all_outcomes(attacker, defender):

    def zero_dice():
        print('zero dice')
        
        nonlocal status

        status['ah'] = 0
        status['ac'] = 0
        status['atd'] = 0
        status['dh'] = 0
        status['dc'] = 0
        status['dtd'] = 0

    def tally_leftover():
        print('tally leftover')

        nonlocal status
        attacker_damage = 0
        defender_damage = 0

        #add up leftover dice
        attacker_damage += status['ah'] + status['ahd']
        attacker_damage += status['ac'] + status['acd']
        defender_damage += status['dh'] + status['dhd']
        defender_damage += status['dc'] + status['dcd']
  
        return(attacker_damage,defender_damage)

    def all_parries_dmg(): 
        print('guaranteed dmg')
        
        nonlocal status
        attacker_damage = 0
        defender_damage = 0

        crit_dif = status['ac'] - status['dc']
        hit_dif = status['ah'] - status['dh']
        
        #use up crits to parry hits
        if (crit_dif < 0 and hit_dif > 0) or (crit_dif > 0 and hit_dif < 0):
            if abs(crit_dif) > abs(hit_dif):
                crit_dif = crit_dif + hit_dif
                hit_dif = 0
            else:
                hit_dif = crit_dif + hit_dif
                crit_dif = 0
        
        #assign damage based on polarity
        if crit_dif >= 0:
            attacker_damage +=  crit_dif * status['acd']
        else:
            defender_damage +=  abs(crit_dif) * status['dcd']
        
        if hit_dif >= 0:
            attacker_damage +=  hit_dif * status['ahd']
        else:
            defender_damage +=  abs(hit_dif) * status['dhd']

        return(attacker_damage,defender_damage)
 
    def possible_choices(sequence, whos_turn):
        nonlocal status

        choices = {'Iterations':0, 'Crit_Parry':0, 'Crit_Bad_Parry':0, 'Parry':0, 'Crit_Strike':0, 'Strike':0, 'Alive':1}        
  
        if whos_turn == 'attacker':
            if sequence[5] < status['aw']:
                if sequence[0] != 0:
                    choices['Crit_Strike'] = 1
                    if sequence[3] !=0:
                        choices['Crit_Parry'] = 1
                    if sequence[4] !=0:
                        choices['Crit_Bad_Parry'] = 1
                if sequence[1] != 0:
                    choices['Strike'] = 1
                    if sequence[4] != 0:
                        choices['Parry'] = 1
            else:
                choices['Alive'] = 0
        elif whos_turn == 'defender':
            if sequence[2] < status['dw']:
                if sequence[3] != 0:
                    choices['Crit_Strike'] = 1
                    if sequence[0] !=0:
                        choices['Crit_Parry'] = 1
                    if sequence[1] !=0:
                        choices['Crit_Bad_Parry'] = 1
                if sequence[4] != 0:
                    choices['Strike'] = 1
                    if sequence[1] != 0:
                        choices['Parry'] = 1
            else:
                choices['Alive'] = 0
        else:
            print('Bad Input')
        
        choices['Iterations'] = choices['Alive'] * (choices['Crit_Parry'] + choices['Crit_Bad_Parry'] + choices['Parry'] + choices['Crit_Strike'] + choices['Strike'] )
        return(choices)

        

    #roll the dice
    attack_dice = dice_check(attacker['WA'], attacker['WS'])
    defense_dice = dice_check(defender['WA'], defender['WS'])

    print(attack_dice)
    print(defense_dice)

    #load stats
    status = {}
    status['ah'] = attack_dice['Hits']
    status['ahd'] =  attacker['WD']
    status['ac'] = attack_dice['Crits']
    status['acd'] = attacker['WCD']
    status['atd'] = status['ah'] + status['ac']
    status['aw'] = attacker['W']
    status['ad'] = 0 #attacker total damage done
            
    status['dh'] = defense_dice['Hits']
    status['dhd'] = defender['WD']
    status['dc'] = defense_dice['Crits']
    status['dcd'] = defender['WCD']
    status['dtd'] = status['dh'] + status['dc']
    status['dw'] = defender['W']
    status['dd'] = 0 #defender total damage done

    #tally of each simulation
    event_totals = []
   
    

    #preface Atk Crits Atk Hits Atk Dmg Def Crits Def Hits Def Dmg
    #usually is larger than needed but make up for cases one when side need to run out dice and other just passes
    damage_sequence = [-1] * ((status['atd'] + status['dtd'])*2 + 6)
    max_sequence_length = len(damage_sequence) - 6
    
    damage_sequence[0] = status['ac']
    damage_sequence[1] = status['ah']
    damage_sequence[2] = status['ad']
    damage_sequence[3] = status['dc']
    damage_sequence[4] = status['dh']
    damage_sequence[5] = status['dd']

    event_totals = []
    round = 1
    event_counter = 0
    
   # 
   #add stop if other player doesnt have any dice
   #
   #
    
    branch_options = possible_choices(damage_sequence, 'attacker')
    
    if branch_options['Iterations'] == 0:
        event_totals.append(damage_sequence)
    else:
        for x in range(branch_options['Iterations']):
            event_totals.append(damage_sequence)
            event_counter += 1
    
    #print(branch_options)
    #print(event_totals)
    #print()
    '''
    Odd Attacker Even Defeneder except 1 is both because ran out of digits

    9,8 Crit Parry
    7,6 Pary
    5,4 Crit Strike
    3,2 Strike
    1,0  Crit Parry Normal Hit
    -1 Filler
    -2 No Action
    '''
    event_counter = 0
    iter_dmg_seq = damage_sequence.copy()
    if branch_options['Crit_Parry'] == 1:
        temp_dmg_seq = list(iter_dmg_seq)
        temp_dmg_seq[0] -= 1
        temp_dmg_seq[3] -= 1
        temp_dmg_seq[round + 5] = 9
        event_totals[event_counter] = temp_dmg_seq
        event_counter += 1
    if branch_options['Crit_Bad_Parry'] == 1:
        temp_dmg_seq = list(iter_dmg_seq)
        temp_dmg_seq[0] -= 1
        temp_dmg_seq[4] -= 1
        temp_dmg_seq[round + 5] = 1
        event_totals[event_counter] = temp_dmg_seq
        event_counter += 1
    if branch_options['Parry'] == 1:
        temp_dmg_seq = list(iter_dmg_seq)
        temp_dmg_seq[1] -= 1
        temp_dmg_seq[4] -= 1
        temp_dmg_seq[round + 5] = 7
        event_totals[event_counter] = temp_dmg_seq
        event_counter += 1
    if branch_options['Crit_Strike'] == 1:
        temp_dmg_seq = list(iter_dmg_seq)
        temp_dmg_seq[0] -= 1
        temp_dmg_seq[2] += status['acd']
        temp_dmg_seq[round + 5] = 5
        event_totals[event_counter] = temp_dmg_seq
        event_counter += 1
    if branch_options['Strike'] == 1:
        temp_dmg_seq = list(iter_dmg_seq)
        temp_dmg_seq[1] -= 1
        temp_dmg_seq[2] += status['ahd']
        temp_dmg_seq[round + 5] = 3
        event_totals[event_counter] = temp_dmg_seq
        event_counter += 1

        

    #print(event_totals)
    #print()

    while event_totals[0][len(damage_sequence)-1] == -1:
        round += 1
        #print("*defender* round:",end='')
        #print(round)
        
        counter_1 = 0
        for x in range(len(event_totals)):
            branch_options = possible_choices(event_totals[counter_1], 'defender')
            #print(event_totals[counter_1])
            #print(branch_options)
            
            
            for x in range(branch_options['Iterations'] - 1):
                event_totals.insert(counter_1, event_totals[counter_1])
            
            event_counter = counter_1
            iter_dmg_seq = event_totals[counter_1].copy()
            if branch_options['Crit_Parry'] == 1:
                temp_dmg_seq = list(iter_dmg_seq)
                temp_dmg_seq[0] -= 1
                temp_dmg_seq[3] -= 1
                temp_dmg_seq[round + 5] = 8
                event_totals[event_counter] = temp_dmg_seq
                event_counter += 1
            if branch_options['Crit_Bad_Parry'] == 1:
                temp_dmg_seq = list(iter_dmg_seq)
                temp_dmg_seq[1] -= 1
                temp_dmg_seq[3] -= 1
                temp_dmg_seq[round + 5] = 0
                event_totals[event_counter] = temp_dmg_seq
                event_counter += 1
            if branch_options['Parry'] == 1:
                temp_dmg_seq = list(iter_dmg_seq)
                temp_dmg_seq[1] -= 1
                temp_dmg_seq[4] -= 1
                temp_dmg_seq[round + 5] = 6
                event_totals[event_counter] = temp_dmg_seq
                event_counter += 1
            if branch_options['Crit_Strike'] == 1:
                temp_dmg_seq = list(iter_dmg_seq)
                temp_dmg_seq[3] -= 1
                temp_dmg_seq[5] += status['dcd']
                temp_dmg_seq[round + 5] = 4
                event_totals[event_counter] = temp_dmg_seq
                event_counter += 1
            if branch_options['Strike'] == 1:
                temp_dmg_seq = list(iter_dmg_seq)
                temp_dmg_seq[4] -= 1
                temp_dmg_seq[5] += status['dhd']
                temp_dmg_seq[round + 5] = 2
                event_totals[event_counter] = temp_dmg_seq
                event_counter += 1


            if branch_options['Iterations'] == 0:
                temp_dmg_seq = list(iter_dmg_seq)
                temp_dmg_seq[round + 5] = -2
                event_totals[event_counter] = temp_dmg_seq
                counter_1 += 1
            counter_1 += branch_options['Iterations'] 
            
            #print()
        
        #print(event_totals)
        #print()
        
        

        if event_totals[0][len(damage_sequence)-1] == -1:
            round += 1
            #print("*attacker*  round:",end='')
            #print(round)

            counter_1 = 0
            for x in range(len(event_totals)):
                branch_options = possible_choices(event_totals[counter_1], 'attacker')
                #print(event_totals[counter_1])
                #print(branch_options)

                for x in range(branch_options['Iterations'] - 1):
                    event_totals.insert(counter_1, event_totals[counter_1])
                
                event_counter = counter_1
                iter_dmg_seq = event_totals[counter_1].copy()
                if branch_options['Crit_Parry'] == 1:
                    temp_dmg_seq = list(iter_dmg_seq)
                    temp_dmg_seq[0] -= 1
                    temp_dmg_seq[3] -= 1
                    temp_dmg_seq[round + 5] = 9
                    event_totals[event_counter] = temp_dmg_seq
                    event_counter += 1
                if branch_options['Crit_Bad_Parry'] == 1:
                    temp_dmg_seq = list(iter_dmg_seq)
                    temp_dmg_seq[0] -= 1
                    temp_dmg_seq[4] -= 1
                    temp_dmg_seq[round + 5] = 1
                    event_totals[event_counter] = temp_dmg_seq
                    event_counter += 1
                if branch_options['Parry'] == 1:
                    temp_dmg_seq = list(iter_dmg_seq)
                    temp_dmg_seq[1] -= 1
                    temp_dmg_seq[4] -= 1
                    temp_dmg_seq[round + 5] = 7
                    event_totals[event_counter] = temp_dmg_seq
                    event_counter += 1
                if branch_options['Crit_Strike'] == 1:
                    temp_dmg_seq = list(iter_dmg_seq)
                    temp_dmg_seq[0] -= 1
                    temp_dmg_seq[2] += status['acd']
                    temp_dmg_seq[round + 5] = 5
                    event_totals[event_counter] = temp_dmg_seq
                    event_counter += 1
                if branch_options['Strike'] == 1:
                    temp_dmg_seq = list(iter_dmg_seq)
                    temp_dmg_seq[1] -= 1
                    temp_dmg_seq[2] += status['ahd']
                    temp_dmg_seq[round + 5] = 3
                    event_totals[event_counter] = temp_dmg_seq
                    event_counter += 1

                if branch_options['Iterations'] == 0:
                    temp_dmg_seq = list(iter_dmg_seq)
                    temp_dmg_seq[round + 5] = -2
                    event_totals[event_counter] = temp_dmg_seq
                    counter_1 += 1
                counter_1 += branch_options['Iterations'] 

            #print(event_totals)
            #print()

    #print(status)        
    #print()
    #print(len(event_totals))
    #print()
    #print(event_totals)

    just_dmg_totals = {}
    for x in range(len(event_totals)):
        just_dmg_totals[x] = (event_totals[x][2], event_totals[x][5])

    temp = {val : key for key, val in just_dmg_totals.items()}
    res = {val : key for key, val in temp.items()}
    
    # printing result 
    #print()
    #print(str(res)) 
    return(status, res, event_totals)

    
    '''
    while attacker_total_dice != 0 or defender_total_dice != 0:
        #kill defender
        if attacker_crits != 0 and defender_wounds <= attacker_crit_dmg:
            attack_dmg += attacker_crit_dmg
            defender_wounds = 0
            zero_dice()
        #kill defender
        elif attacker_hits != 0 and defender_wounds <= attacker_hit_dmg:
            attack_dmg += attacker_hit_dmg
            defender_wounds = 0
            zero_dice()
        #get wounds on defender since death in guarantee
    '''

#automated dice but both players actions are chosen by users
def melee_phase_user_picks(attacker, defender):

    def zero_dice():
        #print('zero dice')
        
        nonlocal status

        status['ah'] = 0
        status['ac'] = 0
        status['atd'] = 0
        status['dh'] = 0
        status['dc'] = 0
        status['dtd'] = 0

    def retotal_dice():
         nonlocal status

         status['atd'] = status['ah'] + status['ac']
         status['dtd'] = status['dh'] + status['dc']

    def print_update_text():
        nonlocal status

        if status['aw'] <= 0:
            print('DEAD**',end='')
        else:
            print('      ',end='')
        print('Attacker-',end='')
        print(' Crits:',end='')
        print(status['ac'],end='')
        print(' Hits:',end='')
        print(status['ah'],end='')
        print(' Wounds:',end='')
        print(status['aw'],end='')
        print(' Damage Done:',end='')
        print(status['ad'],end='')
        
        
        print('       ',end='')
        
        
        if status['dw'] <= 0:
            print('DEAD**',end='')
        else:
            print('      ',end='')
        print('Defender-',end='')
        print(' Crits:',end='')
        print(status['dc'],end='')
        print(' Hits:',end='')
        print(status['dh'],end='')
        print(' Wounds:',end='')
        print(status['dw'],end='')
        print(' Damage Done:',end='')
        print(status['dd'],end='')

        print()


    def tally_leftover():

        #print('tally leftover')

        nonlocal status
        attacker_damage = 0
        defender_damage = 0

        #add up leftover dice
        attacker_damage += status['ah'] * status['ahd']
        attacker_damage += status['ac'] * status['acd']
        defender_damage += status['dh'] * status['dhd']
        defender_damage += status['dc'] * status['dcd']

        status['ad'] += attacker_damage
        status['dd'] += defender_damage

        status['dw']-= attacker_damage
        status['aw'] -= defender_damage

        zero_dice()
        if  status['aw'] < 0:
            status['aw'] = 0
        if  status['dw'] < 0:
            status['dw'] = 0

    def get_decision():
        print("Enter Decision:", end='')
        usr_choice = input()

        while usr_choice != 'p' and usr_choice != 'a' and usr_choice != 'attack' and usr_choice != 'parry':
            print("Enter Decision:", end='')
            usr_choice = input()

        if usr_choice == 'p':
            usr_choice = 'parry'
        if usr_choice == 'a':
            usr_choice = 'attack'
        return(usr_choice)    


    #roll the dice
    attack_dice = dice_check(attacker['WA'], attacker['WS'])
    defense_dice = dice_check(defender['WA'], defender['WS'])

    #load stats
    status = {}
    status['ah'] = attack_dice['Hits']
    status['ahd'] =  attacker['WD']
    status['ac'] = attack_dice['Crits']
    status['acd'] = attacker['WCD']
    status['atd'] = status['ah'] + status['ac']
    status['aw'] = attacker['W']
    status['ad'] = 0 #attacker total damage done
            
    status['dh'] = defense_dice['Hits']
    status['dhd'] = defender['WD']
    status['dc'] = defense_dice['Crits']
    status['dcd'] = defender['WCD']
    status['dtd'] = status['dh'] + status['dc']
    status['dw'] = defender['W']
    status['dd'] = 0 #defender total damage done


    if status['atd'] == 0 or status['dtd'] == 0:
        tally_leftover()
    
    print_update_text()
    while status['atd'] != 0 and status['dtd'] != 0:
        print('Attacker ', end='')
        if get_decision() == 'parry':
            if status['ac'] != 0 and status['dc'] != 0:
                status['ac'] -= 1
                status['dc'] -= 1
            elif status['ac'] != 0 and status['dh'] != 0:
                status['ac'] -= 1
                status['dh'] -= 1
            elif status['ah'] != 0 and status['dh'] != 0:
                status['ah'] -= 1
                status['dh'] -= 1
            elif status['ac'] != 0:
                status['ad'] += status['acd']
                status['ac'] -= 1
                status['dw'] -= status['acd']
            elif status['ah'] != 0:
                status['ad'] += status['ahd']
                status['ah'] -= 1
                status['dw'] -= status['ahd']
            else:
                pass
        else:
            if status['ac'] != 0:
                status['ad'] += status['acd']
                status['ac'] -= 1
                status['dw'] -= status['acd']
            elif status['ah'] != 0:
                status['ad'] += status['ahd']
                status['ah'] -= 1
                status['dw'] -= status['ahd']
            else:
                pass
        if status['dw'] <= 0:
            status['dw'] = 0
            zero_dice()
        retotal_dice()
        print_update_text()


        print('Defender ', end='')
        if get_decision() == 'parry':
            if status['dc'] != 0 and status['ac'] != 0:
                status['dc'] -= 1
                status['ac'] -= 1
            elif status['dc'] != 0 and status['ah'] != 0:
                status['dc'] -= 1
                status['ah'] -= 1
            elif status['dh'] != 0 and status['ah'] != 0:
                status['dh'] -= 1
                status['ah'] -= 1
            elif status['dc'] != 0:
                status['dd'] += status['dcd']
                status['dc'] -= 1
                status['aw'] -= status['dcd']
            elif status['dh'] != 0:
                status['dd'] += status['dhd']
                status['dh'] -= 1
                status['aw'] -= status['ahd']
            else:
                pass
        else:
            if status['dc'] != 0:
                status['dd'] += status['dcd']
                status['dc'] -= 1
                status['aw'] -= status['dcd']
            elif status['dh'] != 0:
                status['dd'] += status['dhd']
                status['dh'] -= 1
                status['aw'] -= status['dhd']
            else:
                pass
        if status['dw'] <= 0:
            status['dw'] = 0
            zero_dice()
        retotal_dice()
        print_update_text()
    
    tally_leftover()
    print_update_text()        

    '''
    print("Attack Dice:", end='')
    atk_num = input()
  
    print("Defense Dice:", end='')
    def_num = input()

    print(atk_num,def_num)
    return(atk_num,def_num)


    while attacker_total_dice != 0 or defender_total_dice != 0:
        #kill defender
        if attacker_crits != 0 and defender_wounds <= attacker_crit_dmg:
            attack_dmg += attacker_crit_dmg
            defender_wounds = 0
            zero_dice()
        #kill defender
        elif attacker_hits != 0 and defender_wounds <= attacker_hit_dmg:
            attack_dmg += attacker_hit_dmg
            defender_wounds = 0
            zero_dice()
        #get wounds on defender since death in guarantee
    '''
              
#Run trials on ranged attack
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





#character stats
guardsmen1 = {'M':6 , 'APL':2, 'GA':2, 'BA':4, 'WA':3, 'BS':4, 'WS':4, 'BD':2, 'BCD':3, 'WD':2, 'WCD':3, 'DF':3, 'SV':5, 'W':7}
kommando = {'M':6 , 'APL':2, 'GA':1, 'BA':5, 'WA':3, 'BS':4, 'WS':3, 'BD':3, 'BCD':4, 'WD':3, 'WCD':4, 'DF':3, 'SV':5, 'W':10}

#dice_check(100000,4)

#melee_phase_user_picks(kommando, guardsmen1)


status_parse, damage_parse, turn_order_parse = melee_phase_all_outcomes(kommando, guardsmen1)
print('****')
print(status_parse)
print()
print(damage_parse)
print()
print(len(turn_order_parse))
print(turn_order_parse)
'''
    Odd Attacker Even Defeneder except 1 is both because ran out of digits

    9,8 Crit Parry
    7,6 Pary
    5,4 Crit Strike
    3,2 Strike
    1,0 Crit Parry Normal Hit
    -1 Filler
    -2 No Action
'''


print()
turn_order = []
total_outcomes = len(turn_order_parse)
crit_parry_outcomes = []
crit_parry_normal_hit_outcomes = []
parry_outcomes = []
crit_attack_outcomes = []
attack_outcomes = []
round_offset = 6
res = []

print('Start')
while (status_parse['ah'] > 0 or status_parse['ac'] > 1 or status_parse['dh'] > 0 or status_parse['dc'] > 0):

    print()
    print('Attacker\'s Turn Round:',(round_offset-5))
    print(turn_order)
    print()
    if status_parse['ah'] > 0 or status_parse['ac'] > 1:
        total_outcomes = len(turn_order_parse)
        for n in range(total_outcomes):
            if turn_order_parse[n][round_offset] == 9:
                crit_parry_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
            elif turn_order_parse[n][round_offset] == 7:
                parry_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
            elif turn_order_parse[n][round_offset] == 5:
                crit_attack_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
            elif turn_order_parse[n][round_offset] == 3:
                attack_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
            elif turn_order_parse[n][round_offset] == 1:
                crit_parry_normal_hit_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
        
        if len(crit_parry_outcomes) > 0:
            print("Crit Parry Options")
            res = []
            for i in crit_parry_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            crit_attack_outcomes.clear()
        
        if len(crit_parry_normal_hit_outcomes) > 0:
            print("Crit Parry Normal Hit Options")
            res = []
            for i in crit_parry_normal_hit_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            crit_parry_normal_hit_outcomes.clear()
  
        if len(parry_outcomes) > 0:
            print("Parry Hit Options")
            res = []
            for i in parry_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            parry_outcomes.clear()
    
        if len(crit_attack_outcomes) > 0:
            print("Crit Attack Options")
            res = []
            for i in crit_attack_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            crit_attack_outcomes.clear()
       
        if len(attack_outcomes) > 0:
            print("Attack Options")
            res = []
            for i in attack_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            attack_outcomes.clear()
        

        user_choice = input()

        if user_choice == 'cp':
            status_parse['ac'] -= 1
            status_parse['dc'] -= 1
            turn_order.append(9)
        elif user_choice == 'cpn':
            status_parse['ac'] -= 1
            status_parse['dh'] -= 1
            turn_order.append(1)
        elif user_choice == 'p':
            status_parse['ah'] -= 1
            status_parse['dh'] -= 1
            turn_order.append(7)
        elif user_choice == 'ca':
            status_parse['ac'] -= 1
            turn_order.append(5)
        elif user_choice == 'a':
            status_parse['ah'] -= 1
            turn_order.append(3)
        else:
            turn_order.append(-2)
                    
    else:
        print('No Dice Left')
        turn_order.append(-2)

    list_offset = 0
    for n in range(total_outcomes):
        if turn_order_parse[n - list_offset][round_offset] != turn_order[round_offset-6]:
            del turn_order_parse[n - list_offset]
            list_offset += 1
    

    round_offset += 1

    
    print()
    print('Defender\'s Turn Round:',(round_offset-5))
    print(turn_order)

    print()
    if status_parse['dh'] > 0 or status_parse['dc'] > 1:
        total_outcomes = len(turn_order_parse)
        for n in range(total_outcomes):
            if turn_order_parse[n][round_offset] == 8:
                crit_parry_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
            elif turn_order_parse[n][round_offset] == 6:
                parry_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
            elif turn_order_parse[n][round_offset] == 4:
                crit_attack_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
            elif turn_order_parse[n][round_offset] == 2:
                attack_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
            elif turn_order_parse[n][round_offset] == 0:
                crit_parry_normal_hit_outcomes.append((turn_order_parse[n][2],turn_order_parse[n][5]))
        
        if len(crit_parry_outcomes) > 0:
            print("Crit Parry Options")
            res = []
            for i in crit_parry_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            crit_attack_outcomes.clear()
        if len(crit_parry_normal_hit_outcomes) > 0:
            print("Crit Parry Normal Hit Options")
            res = []
            for i in crit_parry_normal_hit_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            crit_parry_normal_hit_outcomes.clear()
        if len(parry_outcomes) > 0:
            print("Parry Hit Options")
            res = []
            for i in parry_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            parry_outcomes.clear()
        if len(crit_attack_outcomes) > 0:
            print("Crit Attack Options")
            res = []
            for i in crit_attack_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            crit_attack_outcomes.clear()
        if len(attack_outcomes) > 0:
            print("Attack Options")
            res = []
            for i in attack_outcomes:
                if i not in res:
                    res.append(i)
            print(str(res))
            res.clear()
            attack_outcomes.clear()


        user_choice = input()

        if user_choice == 'cp':
            status_parse['dc'] -= 1
            status_parse['ac'] -= 1
            turn_order.append(8)
        elif user_choice == 'cpn':
            status_parse['dc'] -= 1
            status_parse['ah'] -= 1
            turn_order.append(0)
        elif user_choice == 'p':
            status_parse['dh'] -= 1
            status_parse['ah'] -= 1
            turn_order.append(6)
        elif user_choice == 'ca':
            status_parse['dc'] -= 1
            turn_order.append(4)
        elif user_choice == 'a':
            status_parse['dh'] -= 1
            turn_order.append(2)
        else:
            turn_order.append(-2)
                    
    else:
        print('No Dice Left')
        turn_order.append(-2)

    list_offset = 0
    for n in range(total_outcomes):
        if turn_order_parse[n - list_offset][round_offset] != turn_order[round_offset-6]:
            del turn_order_parse[n - list_offset]
            list_offset += 1
    
    
    round_offset += 1



    
print(status_parse)







'''
outcome_tally = {}
entry = ''
for x in range(1000):
    raw_data = melee_phase_algo1(kommando, guardsmen1)
    for x in list(raw_data.keys()):
        entry = str(raw_data[x]).replace('(','')
        entry = entry.replace(')','')
        if entry in outcome_tally:
            outcome_tally[entry] += 1
        else:
            outcome_tally[entry] = 1




print(outcome_tally)
'''



'''
#data = dict(sorted(outcome_tally.items()))
data = outcome_tally

data_sorted = {k: v for k, v in sorted(data.items(), key=lambda x: x[1])}



x = list(data_sorted.keys())
y = list(data_sorted.values())

# plot
fig, ax = plt.subplots()

ax.bar(x, y, width=1, edgecolor="white", linewidth=3)

plt.show()
'''



'''
data = prob_ranged_death(kommando, guardsmen1)

x = list(data.keys())
y = list(data.values())

# plot
fig, ax = plt.subplots()

ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

plt.show()
'''

'''
trials = 10

damage = bytearray(trials)

for x in range(trials):
    damage[x] = shooting_phase(guardsmen1, kommando)

plt.hist(damage, histtype='stepfilled')
plt.show() 

'''
