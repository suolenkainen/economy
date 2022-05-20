#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## settlements.py
## TODO: Description

import os
from src.utilities import conf_data_to_attribute_list

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
path = os.path.join(os.path.dirname(__file__), "..\\resources")
path = os.path.normpath(path)



# This is a utility class to create object within this module instead of utility module
class settlement_object:
    def __init__(self, data):
        #create an object in settlement module
        for attr in data:
        
            # Add attributes to object
            setattr(self, attr[0], attr[1])



# Fetch configuration data for the creation of settlement
def fetch_conf_data():

    # Fetch conf text
    conf = open(os.path.join(path, "settlements.conf"), "r")
    text = conf.readlines()

    return text



# Fetch attribute-list
def attribute_list(settlement):
    
    list = conf_data_to_attribute_list(settlement)

    return list



## Creates settlement objects where the files were used before
def create_settlements_from_configures():

    # Fetch configuration data
    lines = fetch_conf_data()

    # All settlements in the file
    settlements = []

    # set attributes to object based on the file
    for settlement in lines:
        
        # Create object from settlement data using "settlement_object" class
        data = attribute_list(settlement)
        obj = settlement_object(data)
        settlements.append(obj)

    return settlements



## Adjust the market prices based on non-successful transactions
def adjust_settlement_markets(workorders, sett_objects):

    # loop through workorders and combine them with settlements
    for order in workorders:
        ord_settlement = order.owner
        for stlm in sett_objects:
            if stlm.id == ord_settlement:

                # Adjust the market price for that product in that settlement
                if order.product in stlm.marketsell and order.sell == True:
                    sellprice = stlm.marketsell[order.product]
                    stlm.marketsell[order.product] = round(sellprice/1.005, 1)
                if order.product in stlm.marketbuy and order.sell == False:
                    buyprice = stlm.marketbuy[order.product]
                    stlm.marketbuy[order.product] = round(buyprice*1.005, 1)



if __name__ == '__main__':
        
    settl_objects = create_settlements_from_configures()
    for s in settl_objects:
        print(s.__dict__)