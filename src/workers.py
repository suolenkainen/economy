#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## workers.py
## Description of each worker
## It makes .wrk file to a folder "workers" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os
from src.utilities import conf_data_to_attribute_list

""" 
Required attributes to be clarified.
- type of worker
- destination of work order (when not hauling, destination is the current settlement)
- speed of worker (when not hauling anything, speed is 0)
- distance of total journey
- progression of journey
- goods being handled
- carrying or production capacity

"""

# worker file properties
path = os.path.join(os.path.dirname(__file__), "resources")



# This is a utility class to create object within this module instead of utility module
class worker_object:
    def __init__(self, data):
        #create an object in worker module
        for attr in data:
        
            # Add attributes to object
            setattr(self, attr[0], attr[1])



# Fetch configuration data for the creation of workers
def fetch_conf_data():

    # Fetch conf text
    conf = open(os.path.join(path, "workers.conf"), "r")
    text = conf.readlines()

    return text



# Fetch attribute-list
def attribute_list(worker):
    
    list = conf_data_to_attribute_list(worker)

    return list



## Creates worker objects where the files were used before
def create_worker_from_configures():

    # Fetch configuration data
    lines = fetch_conf_data()

    # All workers in the file
    workers = []

    # set attributes to object based on the file
    for worker in lines:
        
        # Create object from worker data using "worker_object" class
        data = attribute_list(worker)
        obj = worker_object(data)
        workers.append(obj)

    return workers



if __name__ == '__main__':
    
    wrkr_objects = create_worker_from_configures()
    for w in wrkr_objects:
        print(w.__dict__)
