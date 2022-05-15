#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## settlements.py
## Description of each settlement
## It makes .slm file to a folder "settlements" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os, ast
import utilities as utils

""" 
Required attributes
- settlement location
- settlement population
- settlement workers
- settlement resourses
- settlement producers
- settlement base wealth
- liquid wealth

settlement size grows as wealth
"""

# Settlement file properties
settlement_path = "resources\\settlements"
path = os.path.join(os.path.dirname(__file__), settlement_path)

postfix = "settlement_"
prefix = ".slm"


class create_settlement():
    def __init__(self, attributes):

        # Write attributes into .slm file

        # Create text from attributes
        text = utils.attributes_to_text(attributes)

        # Create a file with a filename generate
        filename = postfix + str(attributes["index"]) + prefix
        f = open(os.path.join(path, filename), "w")
        f.writelines(text)

        # Test that file exists with proper data
        f = open(os.path.join(path, filename), "r")
        print(f.read())
        f.close()

### Obsolete
def create_attributes():

    # This will be randomized in the future based on something
    attributes = {}
    attributes["name"] = "settlement_0"
    attributes["coordinate_X"] = 100
    attributes["coordinate_Y"] = 100
    attributes["workers"] = []
    attributes["population"] = 10
    attributes["goods"] = {"grain": 10}
    attributes["resourcegoods"] = {}
    attributes["producers"] = []
    attributes["basewealth"] = 100
    attributes["liquid_wealth"] = 100
    attributes["marketsell"] = {"grain": 12}
    attributes["marketbuy"] = {"grain": 10}
    return attributes



# This is a utility class to create object within this module instead of utility module
class settlement_object:
    def __init__(self, data):
        #create an object in settlement module
        for attr in data:
        
            # Add attributes to object
            setattr(self, attr[0], attr[1])



## Creates settlements objects where the files were used before
def create_settlements_from_configures():
    path = os.path.join(os.path.dirname(__file__), "resources")
    conf = open(os.path.join(path, "settlements.conf"), "r")

    # ALl settlements in the file
    settlements = []

    # set attributes to object based on the file
    while True:
        
        settlement = conf.readline()
        if not settlement:
            break

        # Create object from settlement data using "settlement_object" class
        data = utils.conf_data_to_attribute_list(settlement)
        obj = settlement_object(data)
        settlements.append(obj)

    return settlements



if __name__ == '__main__':
        
    # # Test settlement creation attributes
    # settlement_amount = 1
    # settlements = os.listdir(path)

    # # Before creating new files, the old directory needs to be emptied
    # class clear_settlements:
    #     for s in settlements:
    #         if postfix in s:
    #             os.remove(os.path.join(path, s))

    # print("main")

    # attributes = create_attributes()


    # for i in range(settlement_amount):
    #     attributes["index"] = i
    #     create_settlement(attributes)

    settl_objects = create_settlements_from_configures()
    print(settl_objects)