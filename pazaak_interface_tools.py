from dice import *
import math

def get_int(message = "", sign = 0):
    value = None
    
    while not isinstance(value, int):
        value = input(message)
        try:
            value = int(value)
        except:
            continue
            
        if sign < 0:
            value = -abs(value)
            continue
        elif sign > 0:
            value = abs(value)
            continue
        else:
            continue
    
    return value
    
def get_string(message = ""):
    string = input(message)
    return string
    
def get_bool(message = ""):
    value = None
    true_strings = set(["True", "true", "t", "T", "1", "Yes", "yes", "Y", "y"])
    false_strings = set(["False", "false", "f", "F", "0", "No", "no", "N", "n"])
    
    while not isinstance(value, bool):
        value = input(message)
        if value in true_strings:
            value = True
        elif value in false_strings:
            value = False
    
    return value
        