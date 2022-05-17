#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## workorder.py
## Description of each good
## It makes .gds file to a folder "workorder" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os
from src.utilities import conf_data_to_attribute_list

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
path = os.path.join(os.path.dirname(__file__), "resources")



# This is a utility class to create object within this module instead of utility module
class workorder_object:
    def __init__(self, data):
        #create an object in workorder module
        for attr in data:
        
            # Add attributes to object
            setattr(self, attr[0], attr[1])



# Fetch configuration data for the creation of work orders
def fetch_conf_data():

    # Fetch conf text
    conf = open(os.path.join(path, "workorders.conf"), "r")
    text = conf.readlines()

    return text



# Fetch attribute-list
def attribute_list(workorder):
    
    list = conf_data_to_attribute_list(workorder)

    return list



## Creates workorder objects where the files were used before
def create_workorders_from_configures():

    # Fetch configuration data
    lines = fetch_conf_data()

    # All workorders in the file
    workorders = []

    # set attributes to object based on the file
    for workorder in lines:
        
        # Create object from workorder data using "workorder_object" class
        data = attribute_list(workorder)
        obj = workorder_object(data)
        workorders.append(obj)

    return workorders



if __name__ == '__main__':
    
    ord_objects = create_workorders_from_configures()
    for o in ord_objects:
        print(o.__dict__)