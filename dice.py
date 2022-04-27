import random

def attack_check(rolls, skill):
    rolls = int(rolls)
    if rolls <= 0 or skill < 1 or skill > 6:
        print('Invalid Range')
        return
    dice_rolls = {}
    results = {'Rolls':0, 'Hits':0, 'Crits':0, 'Hit %':0, 'Crit %':0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0 }
    results['Rolls'] = rolls

    for n in range(rolls):
        single_roll = random.randint(1,6)
        dice_rolls[n] = single_roll
        results[single_roll] += 1
        if single_roll >= skill:
            results['Hits'] += 1

    results['Crits'] = results[6]
    results['Hit %'] = results['Hits'] / results['Rolls']
    results['Crit %'] = results['Crits'] / results['Rolls'] 

    #print(dice_rolls)    
    print(results)

def get_attacks():
    print("Attack Dice:", end='')
    atk_num = input()
  
    print("Defense Dice:", end='')
    def_num = input()

    print(atk_num,def_num)
    return(atk_num,def_num)

attack_check(10, 4) #number of rolls, BS/WS level
