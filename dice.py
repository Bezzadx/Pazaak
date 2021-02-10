import random as r

def roll(dice, number = 1, ad = 0):
    if dice < 1:
        return 0
    else:
        score = 0
        if ad != 0:
            x = roll(dice, number)
            y = roll(dice, number)
            if ad > 0:
                return max(x,y) 
            elif ad < 0:
                return min(x,y)
        else:
            for i in range(number):
                score += r.randint(1,dice)
            return score

def rolln(dice, number = 1, repetitions = 1):
    array = []
    for i in range(repetitions):
        array.append(roll(dice, number))
    return array