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
- producer location settlement
- producer workers
- produced resourses stored
- producer required goods
- manufacturing speed
- maximum capacity of storaged resources
- maximum capacity of stored goods
"""


# Producer file properties
producer_path = "resources\\producers"
path = os.path.join(os.path.dirname(__file__), producer_path)
postfix = "producer_"
prefix = ".prd"


class create_producer:
    def __init__(self, attributes):

        # Write attributes into .prd file
        text = "product=" + str(attributes["product"]) + "\n" + \
                "requirement=" + str(attributes["requirement"]) + "\n" + \
                "requiredperunit=" + str(attributes["requiredperunit"]) + "\n" + \
                "location=" + str(attributes["location"]) + "\n" + \
                "workers=" + str(attributes["workers"]) + "\n" + \
                "storedresources=" + str(attributes["storedresources"]) + "\n" + \
                "storedproduct=" + str(attributes["storedproduct"]) + "\n" + \
                "speed=" + str(attributes["speed"]) + "\n" + \
                "maxresources=" + str(attributes["maxresources"]) + "\n" + \
                "maxgoods=" + str(attributes["maxgoods"])

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
    attributes["product"] = "grain"
    attributes["requirement"] = ""
    attributes["requiredperunit"] = 0
    attributes["location"] = "settlement_1"
    attributes["workers"] = []
    attributes["storedresources"] = 0
    attributes["storedproduct"] = 0
    attributes["speed"] = 1
    attributes["maxresources"] = 100
    attributes["maxgoods"] = 100
    return attributes


if __name__ == '__main__':
    
     # Test producer creation attributes
    producer_amount = 1
    producers = os.listdir(path)

    # Before creating new files, the old directory needs to be emptied
    class clear_producers:
        for s in producers:
            if postfix in s:
                os.remove(os.path.join(path, s))
    
    print("main")

    attributes = create_attributes()

    for i in range(producer_amount):
        attributes["index"] = i
        create_producer(attributes)
