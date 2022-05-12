#!/usr/bin/env python3py
# Author: Pekka Marjamäki - Suolenkainen

## resources.py
## Description of each resource
## It makes .rsc file to a folder "resources" and includes all relevant information
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

# Path to "resources" folder and list of resource names
resource_path = "files\\resources"
path = os.path.join(os.path.dirname(__file__), resource_path)
resources = os.listdir(path)

# Before creating new files, the old directory needs to be emptied

class clear_resources:
    for f in resources:
        if f == "remove.rsc":
            os.remove(os.path.join(path, f))
            # print(os.path.join(path, f))


# For testing purposes, recreate the .rsc file previously removed
f = open(os.path.join(path, "remove.rsc"), "a")
f.write("Test!")
f.close()

f = open(os.path.join(path, "remove.rsc"), "r")
print(f.read())


if __name__ == '__main__':
    
    print("main")
    clear_resources()