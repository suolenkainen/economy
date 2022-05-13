#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## goods.py
## Description of each good
## It makes .gds file to a folder "goods" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os
import utilities as utils

""" 
Required attributes
- owner (the goods are owned by the last settlement it was in)
- destination (destination can be "consumed" and the requires no hauling)
- required haul method
- worker
- price
- amount
- capacity per item
- haul fee
"""


# goods file properties
goods_path = "resources\\goods"
path = os.path.join(os.path.dirname(__file__), goods_path)
postfix = "goods_"
prefix = ".gds"


class create_goods:
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
    attributes["owner"] = "producer_0"
    attributes["destination"] = "producer_1"
    attributes["product"] = "grain"
    attributes["method"] = ""
    attributes["worker"] = "worker_0"
    attributes["price"] = 5
    attributes["amount"] = 5
    attributes["capacityperitem"] = 1
    attributes["fee"] = 1
    return attributes




if __name__ == '__main__':
    
     # Test goods creation attributes
    goods_amount = 1
    goods = os.listdir(path)

    # Before creating new files, the old directory needs to be emptied
    class clear_goods:
        for s in goods:
            if postfix in s:
                os.remove(os.path.join(path, s))
    
    print("main")

    attributes = create_attributes()

    for i in range(goods_amount):
        attributes["index"] = i
        create_goods(attributes)