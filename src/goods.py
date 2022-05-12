#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## goods.py
## Description of each good
## It makes .gds file to a folder "goods" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os

""" 
Required attributes
- producer
- destination
- required haul method
- worker
- price
- amount
- haul fee
- distance fee
- spoil time
"""

# Path to "goods" folder and list of good names
goods_path = "resources\\goods"
path = os.path.join(os.path.dirname(__file__), goods_path)
goods = os.listdir(path)

# Before creating new files, the old directory needs to be emptied

class clear_goods:
    for f in goods:
        if f == "remove.gds":
            os.remove(os.path.join(path, f))
            # print(os.path.join(path, f))


# For testing purposes, recreate the .gds file previously removed
f = open(os.path.join(path, "remove.gds"), "a")
f.write("Test!")
f.close()

f = open(os.path.join(path, "remove.gds"), "r")
print(f.read())


if __name__ == '__main__':
    
    print("main")
    clear_goods()