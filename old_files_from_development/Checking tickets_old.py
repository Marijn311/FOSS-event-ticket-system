# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:09:40 2022

@author: 20192010
"""
#This script is for checking the send out codes (tickets).
import json


#First we load in the valid_codes and the used_codes.
with open(r'/data/user/0/ru.iiec.pydroid3/app_HOME/Checking tickets/saved_valid_codes.txt', 'r') as f:
    valid_codes = json.loads(f.read())
    
with open(r'/data/user/0/ru.iiec.pydroid3/app_HOME/Checking tickets/saved_used_codes.txt', 'r') as f:
    used_codes = json.loads(f.read())

given_code = input(str("please enter code (three capital letters):"))
while len(used_codes) != len(valid_codes):   
    if given_code in used_codes:
        print('This code has already been used')
        
    if given_code in valid_codes and given_code not in used_codes:
        print('This code is: VALID')
        used_codes.append(given_code)
        
    if given_code not in valid_codes:
        print('This code is: WRONG')
        
    if given_code == 'save used codes':
        with open('saved_used_codes.txt', 'w') as f:
            f.write(json.dumps(used_codes))
        print('used codes have been saved')
        
    given_code = input(str("please enter code:"))
        
    