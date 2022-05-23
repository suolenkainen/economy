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
path = os.path.join(os.path.dirname(__file__), "..\\resources")
path = os.path.normpath(path)



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


def request_production_resources(settlement_object, producer_object):
    prod_requirements = []

    ## Pair producer and settlement
    for producer in producer_object:
        for settlement in settlement_object:
            if producer.settlementid == settlement.id:

                ## Check the current state of resources 
                ## and if there can be a request for more
                currentres = 0

                ## If there are no resources stored, create new instances
                ## for values
                if producer.storedresources == {}:
                    for key in producer.requirements:
                        producer.storedresources[key] = 0
                maxres = producer.maxresources

                ## Calculate which resources need to be requested
                total_requirement = {}
                
                if producer.requirements == {}:
                    continue

                for key in producer.requirements:
                    total_requirement[key] = 0
                
                topvalue = 0
                loop = True

                ## Calculate necessary resources to be required in total
                while loop == True:
                    for key in producer.requirements:
                        if maxres - topvalue < currentres:
                            for key in producer.storedresources:
                                total_requirement[key] -= producer.storedresources[key]

                            # Add producer id, settlement id, and required resources to list
                            prod_requirements.append((producer.id, settlement.id, total_requirement))
                            loop = False
                            break
                        total_requirement[key] += producer.requirements[key]
                        if producer.requirements[key] > topvalue:
                            topvalue = producer.requirements[key]
                        currentres += producer.requirements[key]

    return prod_requirements



def move_resources_from_settlement(sett_objects, prod_requirements, prod_objects):

    new_orders = {}
    index = 0

    ## Find settlements and production places and attach prod-place
    for p, s, requirement in prod_requirements:
        for producer in prod_objects:
            if p == producer.id:
                prod = producer
                break
        for settlement in sett_objects:
            if s == settlement.id:
                sett = settlement
                break
    
        ## Move resources from settlement to production
        for key in requirement.keys():
            if key in requirement and key in sett.resourcegoods and prod.pending == False:
                value = requirement[key]
                if value > sett.resourcegoods[key]:
                    newvalue = value - sett.resourcegoods[key]
                    prod.storedresources[key] += sett.resourcegoods[key]
                    sett.resourcegoods[key] = 0
                    new_orders = {index: {key: newvalue, "sett": sett.id}}
                    index += 1
                    prod.pending = True
                else:
                    value = prod.storedresources[key]
                    prod.storedresources[key] += sett.resourcegoods[key]
                    sett.resourcegoods[key] -= value
        
        return new_orders


if __name__ == '__main__':
    
    ord_objects = create_producers_from_configures()
    for o in ord_objects:
        print(o.__dict__)