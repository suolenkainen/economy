#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## workers.py
## Description of each worker
## It makes .wrk file to a folder "workers" and includes all relevant information
## These files are then read by the main loop and added to the simulation

import os

""" 
Required attributes to be clarified.
- type of worker
- start of hauling
- destination of hauling
- speed of worker
- distance of total journey
- progression of journey
- goods being handled
- carrying or production capacity

"""

# Path to "workers" folder and list of worker names
worker_path = "resources\\workers"
path = os.path.join(os.path.dirname(__file__), worker_path)
workers = os.listdir(path)


# worker creation attributes
worker_amount = 1
postfix = "worker_"
prefix = ".wrk"


# Before creating new files, the old directory needs to be emptied

class clear_workers:
    for s in workers:
        if postfix in s:
            os.remove(os.path.join(path, s))

class create_worker():
    def __init__(self, attributes):

        # Write attributes into .wrk file
        text = "type=" + str(attributes["type"]) + "\n" + \
                "start=" + str(attributes["start"]) + "\n" + \
                "destination=" + str(attributes["destination"]) + "\n" + \
                "speed=" + str(attributes["speed"]) + "\n" + \
                "distance=" + str(attributes["distance"]) + "\n" + \
                "progression=" + str(attributes["progression"]) + "\n" + \
                "goods=" + str(attributes["goods"]) + "\n" + \
                "capacity=" + str(attributes["capacity"]) + "\n"


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
    attributes["type"] = "hauling"
    attributes["start"] = "settlement_0"
    attributes["destination"] = "settlement_1"
    attributes["speed"] = 5
    attributes["distance"] = 50
    attributes["progression"] = 25
    attributes["goods"] = ["goods_0"]
    attributes["capacity"] = 10


    clear_workers()

    for i in range(worker_amount):
        attributes["index"] = i
        create_worker(attributes)

    ### We need some attributes to indicate a worker that is creating things, not just hauling