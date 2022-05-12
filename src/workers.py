#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## workers.py
## Description of each worker
## It makes .wrk file to a folder "workers" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os

""" 
Required attributes to be clarified. The idea is to name worker  and to link it to a town or a resource production place
"""

# Path to "workers" folder and list of worker names
worker_path = "resources\\workers"
path = os.path.join(os.path.dirname(__file__), worker_path)
workers = os.listdir(path)

# Before creating new files, the old directory needs to be emptied

class clear_workers:
    for f in workers:
        if f == "remove.wrk":
            os.remove(os.path.join(path, f))
            # print(os.path.join(path, f))


# For testing purposes, recreate the .wrk file previously removed
f = open(os.path.join(path, "remove.wrk"), "a")
f.write("Test!")
f.close()

f = open(os.path.join(path, "remove.wrk"), "r")
print(f.read())


if __name__ == '__main__':
    
    print("main")
    clear_workers()