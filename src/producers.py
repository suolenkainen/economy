#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## producers.py
## Description of each producer
## It makes .prd file to a folder "producers" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os

""" 
Required attributes
- producer location
- producer workers
- produced resourses
"""

# Path to "producers" folder and list of producer names
producer_path = "resources\\producers"
path = os.path.join(os.path.dirname(__file__), producer_path)
producers = os.listdir(path)

# Before creating new files, the old directory needs to be emptied

class clear_producers:
    for p in producers:
        if "remove" in p:
            os.remove(os.path.join(path, p))

class create_producers:
    

    # For testing purposes, recreate the .prd file previously removed
    f = open(os.path.join(path, "remove2.prd"), "a")
    f.write("Test!")
    f.close()

    f = open(os.path.join(path, "remove2.prd"), "r")
    print(f.read())


if __name__ == '__main__':
    
    print("main")
    clear_producers()
    create_producers()