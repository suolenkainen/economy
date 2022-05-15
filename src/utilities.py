#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## utilities.py
## Functions that are commonly used in modules.

from math import sqrt
import os
import ast

# Function is used to return an object based on the attributes in the file
class file_to_object:
    def __init__(self, filename, path):
        stlm = open(os.path.join(path, filename), "r")
        self.filename = filename

        # set attributes to object based on the file
        while True:
            
            line = stlm.readline()
            if not line:
                break
            attr = line.strip().split("=")
            try:
                attr[1] = int(attr[1])
            except:
                pass
            try:
                attr[1] = float(attr[1])
            except:
                pass
            if attr[0] in ["marketsell", "marketbuy", "goods", "producers", "resourcegoods", "workers", "sell", "workorders"]:
                attr[1] = ast.literal_eval(attr[1])
            setattr(self, attr[0], attr[1])



# Temprary tool
class settlement_to_object:
    def __init__(self, line):

        # split the data row into text form attributes
        stlm_data = line.strip().split(",")
        
        # For each attribute in the line, divide it into parameteds and add them to object as object attributes
        for stlm in stlm_data:
            attr = stlm.strip().split("=")
            try:
                attr[1] = int(attr[1])
            except:
                try:
                    attr[1] = float(attr[1])
                except:
                    pass

            # For dicts and lists, use literal eval to transform string into appropriate data type
            if attr[0] in ["marketsell", "marketbuy", "goods", "producers", "workers"]:
                attr[1] = ast.literal_eval(attr[1])
            
            # Add attributes to object
            setattr(self, attr[0], attr[1])



def attributes_to_text(attrs):
    text = []
    for key in attrs:
        # print(key, attrs[key])
        text.append(key + "=" + str(attrs[key]) + "\n")
    print(text)
    return text


def combine_workorders(seller, buyer):
    # If workorders match each other, the seller order is updated and buy-order is removed
    if seller.amount == buyer.amount:
        seller.destination = buyer.owner
        return seller, [], []

    # If seller has more than buyer is willing to buy, a new order will be created for the surplus
    if seller.amount > buyer.amount:
        new_order = seller
        seller.destination = buyer.owner
        new_order.amount -= buyer.amount
        return seller, [new_order], []

    # If buyer wants to buy more than seller has to sell, a new order will be created for the lacking amount
    if seller.amount < buyer.amount:
        new_order = seller
        seller.destination = buyer.owner
        new_order.amount -= seller.amount
        return seller, [], [new_order]


# This function checks if a transaction forms a deal
def sales_calculator(asked, payed):
    deal = False
            
    #Checking that transaction is made within range of reason (5%)
    if asked > payed:
        if asked <= payed*1.05:
            deal = True
        else:

            # If the selling price is just a little less than required, the price is reduced a bit by seller
            if asked/1.05 <= payed:
                deal = True
                asked /= 1.05

    # If asked price is less than what the buyer is willing to pay, then the deal is made
    elif asked < payed:
        deal = True

    return deal


# Distance between two settlements
def distance_calculator(a, b):
    xa = a.coordinate_X
    ya = a.coordinate_Y
    xb = b.coordinate_X
    yb = b.coordinate_Y

    x = abs(xa-xb)
    y = abs(ya-yb)
    d = round(sqrt(x*x + y*y))

    return d


if __name__ == "__main__":

    attributes = {}
    attributes["type"] = "hauling"
    attributes["destination"] = "settlement_1"
    attributes["speed"] = 0
    attributes["maxspeed"] = 5
    attributes["distance"] = 0
    attributes["progression"] = 0
    attributes["goods"] = []
    attributes["capacity"] = 100

    print(attributes_to_text(attributes))