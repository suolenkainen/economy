#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## utilities.py
## Functions that are commonly used in modules.

from math import sqrt
import ast



# Configuration data to a list of attributes tool
def conf_data_to_attribute_list(line):

    # split the data row into text form attributes
    data = line.strip().split(",")
    
    # For each attribute in the line, divide it into parameteds and add them to object as object attributes
    for i, d in enumerate(data):
        attr = d.strip().split("=")
        try:
            attr[1] = int(attr[1])
        except:
            try:
                attr[1] = float(attr[1])
            except:
                pass

        # For dicts and lists, use literal eval to transform string into appropriate data type
        if attr[0] in ["marketsell", "marketbuy", "goods", "producers", "workers", "workorders", "requirements", "sell"]:
            attr[1] = ast.literal_eval(attr[1])
        
        data[i] = attr
    
    return data



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
    xa = a.coordx
    ya = a.coordy
    xb = b.coordx
    yb = b.coordy

    x = abs(xa-xb)
    y = abs(ya-yb)
    d = round(sqrt(x*x + y*y))

    return d


# #  , transactions = [], sett_objects = [], params = ("owner", "destination")
# def endpoint_calculator1(transactions, sett_objects):
#     for order in transactions:
#         ord_settlement = order.owner
#         for stlm1 in sett_objects:
#             if stlm1.id == ord_settlement:
#                 starting = stlm1
#                 break

#     for worker in wrk_objects:
#         if worker.speed != 0:
#             continue
#         wrk_settlement = worker.settlementid
#         for stlm2 in sett_objects:
#             if stlm2.id == wrk_settlement:
#                 destination = stlm2
#                 break

#     return starting.__dict__, destination.__dict__

#  , transactions = [], sett_objects = [], params = ("owner", "destination")
def endpoint_calculator(searched_objects, sett_objects, param):

    # calculate 
    for s_obj in searched_objects:
        s_var = s_obj.__dict__[param]
        for d_var in sett_objects:
            if d_var.id == s_var:
                settlement = d_var
                break

    return settlement


if __name__ == "__main__":
    pass