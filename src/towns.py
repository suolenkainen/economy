#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen

## towns.py
## Description of each town
## It makes .twn file to a folder "towns" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os

""" 
Required attributes
- town location
- town population
- town workers
- town resourses
- town producers
"""

# Path to "towns" folder and list of town names
town_path = "files\\towns"
path = os.path.join(os.path.dirname(__file__), town_path)
towns = os.listdir(path)

# Before creating new files, the old directory needs to be emptied

class clear_towns:
    for f in towns:
        if f == "remove.twn":
            os.remove(os.path.join(path, f))
            # print(os.path.join(path, f))


# For testing purposes, recreate the .twn file previously removed
f = open(os.path.join(path, "remove.twn"), "a")
f.write("Test!")
f.close()

f = open(os.path.join(path, "remove.twn"), "r")
print(f.read())


if __name__ == '__main__':
    
    print("main")
    clear_towns()