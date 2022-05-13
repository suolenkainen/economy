#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## workorder.py
## Description of each good
## It makes .gds file to a folder "workorder" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os
import utilities as utils

""" 
Required attributes
- owner (the workorder are owned by the last settlement it was in)
- destination
- required haul method
- worker
- price
- amount
- capacity per item
- haul fee
"""


# workorder file properties
workorder_path = "resources\\workorders"
path = os.path.join(os.path.dirname(__file__), workorder_path)
postfix = "workorder_"
prefix = ".ord"


class create_workorder:
    def __init__(self, attributes):

        # Write attributes into .gds file

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


def create_attributes():
    # This will be randomized in the future based on something
    attributes = {}
    attributes["owner"] = "settlement_0"
    attributes["destination"] = ""
    attributes["sell"] = True
    attributes["product"] = "grain"
    attributes["method"] = ""
    attributes["worker"] = ""
    attributes["reserved"] = ""
    attributes["price"] = 12.00
    attributes["amount"] = 5
    attributes["capacityperitem"] = 1
    return attributes


if __name__ == '__main__':
    
     # Test workorder creation attributes
    workorders_amount = 1
    workorders = os.listdir(path)

    # Before creating new files, the old directory needs to be emptied
    class clear_workorders:
        for s in workorders:
            if postfix in s:
                os.remove(os.path.join(path, s))
    
    print("main")

    attributes = create_attributes()

    for i in range(workorders_amount):
        attributes["index"] = i
        create_workorder(attributes)