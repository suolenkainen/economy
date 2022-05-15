#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## workers.py
## Description of each worker
## It makes .wrk file to a folder "workers" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os
import utilities as utils

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
worker_path = "resources\\workers"
path = os.path.join(os.path.dirname(__file__), worker_path)
postfix = "worker_"
prefix = ".wrk"


class create_worker():
    def __init__(self, attributes):

        # Write attributes into .wrk file

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
    attributes["type"] = "walking"
    attributes["settlement"] = "settlement_0"
    attributes["distance"] = 0
    attributes["speed"] = 0
    attributes["maxspeed"] = 5
    attributes["progression"] = 0
    attributes["workorders"] = []
    attributes["capacity"] = 100
    attributes["order"] = 0
    return attributes



## Creates worker objects where the files were used before
def create_worker_from_configures():
    path = os.path.join(os.path.dirname(__file__), "resources")
    conf = open(os.path.join(path, "workers.conf"), "r")

    # ALl settlements in the file
    workers = []

    # set attributes to object based on the file
    while True:
        
        worker = conf.readline()
        if not worker:
            break

        # Create object from settlement data
        obj = utils.conf_data_to_object(worker)
        workers.append(obj)
    return workers



if __name__ == '__main__':
    
    #  # Test worker creation attributes
    # worker_amount = 1
    # workers = os.listdir(path)

    # # Before creating new files, the old directory needs to be emptied
    # class clear_workers:
    #     for s in workers:
    #         if postfix in s:
    #             os.remove(os.path.join(path, s))
    
    # print("main")

    # attributes = create_attributes()

    # for i in range(worker_amount):
    #     attributes["index"] = i
    #     create_worker(attributes)

    wrkr_objects = create_worker_from_configures()
    print(wrkr_objects)
