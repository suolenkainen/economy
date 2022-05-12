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
- town base wealth
- liquid wealth

Town size grows as wealth
"""

# Path to "towns" folder and list of town names
town_path = "files\\towns"
path = os.path.join(os.path.dirname(__file__), town_path)
towns = os.listdir(path)


# Town creation attributes
town_amount = 1
postfix = "town_"
prefix = ".twn"


# Before creating new files, the old directory needs to be emptied

class clear_towns:
    for t in towns:
        if postfix in t:
            os.remove(os.path.join(path, t))

class create_town():
    def __init__(self, attributes):

        # Write attributes into .twn file
        coord_x, coord_y = attributes["coordinates"]
        text = "coordinate_X=" + str(coord_x) + "\n" + \
                "coordinate_Y=" + str(coord_y) + "\n" + \
                "workers=" + str(attributes["workers"]) + "\n" + \
                "population=" + str(attributes["population"]) + "\n" + \
                "resourses=" + str(attributes["resourses"]) + "\n" + \
                "producers=" + str(attributes["producers"]) + "\n" + \
                "base_wealth=" + str(attributes["base_wealth"]) + "\n" + \
                "liquid_wealth=" + str(attributes["liquid_wealth"])


        # Create a file with a filename generate
        filename = postfix + str(attributes["index"]) + prefix
        f = open(os.path.join(path, filename), "a")
        f.write(text)
        f.close()

        # Test that file exists with proper data
        f = open(os.path.join(path, filename), "r")
        print(f.read())


if __name__ == '__main__':
    
    print("main")

    attributes = {}
    attributes["coordinates"] = [100, 100]
    attributes["workers"] = []
    attributes["population"] = 100
    attributes["resourses"] = []
    attributes["producers"] = []
    attributes["base_wealth"] = 100
    attributes["liquid_wealth"] = 100

    clear_towns()

    for i in range(town_amount):
        attributes["index"] = i
        create_town(attributes)