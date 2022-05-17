#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## producer.py
## TODO: Description

import os
from src.utilities import conf_data_to_attribute_list

""" 
Required attributes
- producer location settlement
- producer workers
- produced resourses stored
- producer required goods
- manufacturing speed
- maximum capacity of storaged resources
- maximum capacity of stored goods
"""



# producer file properties
path = os.path.join(os.path.dirname(__file__), "resources")



# This is a utility class to create object within this module instead of utility module
class producer_object:
    def __init__(self, data):
        #create an object in producer module
        for attr in data:
        
            # Add attributes to object
            setattr(self, attr[0], attr[1])



# Fetch configuration data for the creation of work orders
def fetch_conf_data():

    # Fetch conf text
    conf = open(os.path.join(path, "producers.conf"), "r")
    text = conf.readlines()

    return text



# Fetch attribute-list
def attribute_list(producer):
    
    list = conf_data_to_attribute_list(producer)

    return list



## Creates producer objects where the files were used before
def create_producers_from_configures():

    # Fetch configuration data
    lines = fetch_conf_data()

    # All producers in the file
    producers = []

    # set attributes to object based on the file
    for producer in lines:
        
        # Create object from producer data using "producer_object" class
        data = attribute_list(producer)
        obj = producer_object(data)
        producers.append(obj)

    return producers



if __name__ == '__main__':
    
    ord_objects = create_producers_from_configures()
    for o in ord_objects:
        print(o.__dict__)