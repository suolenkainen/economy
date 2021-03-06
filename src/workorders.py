#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## workorder.py
## TODO: Description

import os, copy
from src.utilities import conf_data_to_attribute_list, distance_calculator

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
path = os.path.join(os.path.dirname(__file__), "..\\resources")
path = os.path.normpath(path)



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



## Combine buying and selling orders
def combine_workorders(ord_objects):

    ## Combining has divided into part-functions
    selling, buying = sort_buy_sell(ord_objects)
    complete_orders, buying = finish_transactions(selling, buying, ord_objects)

    return complete_orders, buying



def sort_buy_sell(ord_objects):
    selling = []
    buying = []

    # Divide the selling and buying into their of lists and return them sorten by having the most expensive selling to cheapest buying
    for order in ord_objects:
        if order.sell == True:
            selling.append(order)
        else:
            buying.append(order)
    selling = sorted(selling, key=lambda d: d.price, reverse=True)
    buying = sorted(buying, key=lambda d: d.price)

    return selling, buying



def finish_transactions(selling, buying, ord_objects):

    # Pairing sell and purchase orders so that the most expensive item is sold first to the least paying settlement and then increasing in price
    complete_orders = []
    order = 0
    while len(selling) > 0: 
        sold = selling[order]
        if sold.processed in ["sold", "finished"]:
            complete_orders.append(sold)
            order += 1
            if order >= len(selling):
                buying.extend(selling)
                break
            continue
        if buying == []:
            deal = False
        for request in buying:
            if sold.processed in ["sold", "finished"]:
                continue
            deal = False
            
            # Matching the products
            if sold.product == request.product:
                deal = sales_calculator(sold.price, request.price)
                break
            else:
                continue
        order += 1

        #when deal is formed, the deal is put into a list of completed transactions. If some of the goods are not sold or remaining in the order, a new order is created
        if deal:
            complete_order, newsale, newbuy, old_request = match_orders(sold, request, len(ord_objects))
            sold = complete_order
            # ord_objects.remove(request)
            complete_orders.append( selling.pop( selling.index( complete_order ) ) )
            buying.extend(newbuy)
            selling.extend(newsale)

            #when adding and removing items from lists, they are sorted again
            buying = sorted(buying, key=lambda d: d.price)
            selling = sorted(selling, key=lambda d: d.price, reverse=True)
            order = 0
            if len(buying) == 0 or len(selling) == 0:
                buying.extend(selling)
                selling = []
                break
        if len(selling) == 0 or order >= len(selling):
            buying.extend(selling)
            break

    return complete_orders, buying



## If we create new orders on the fly, how do we handle identifiers?
def match_orders(seller, buyer, index):
    # If workorders match each other, the seller order is updated and buy-order is removed
    if seller.amount == buyer.amount:
        seller.destination = buyer.owner
        seller.processed = "combined"
        buyer.processed = "finished"
        return seller, [], [], buyer

    # If seller has more than buyer is willing to buy, a new order will be created for the surplus
    if seller.amount > buyer.amount:
        new_order = copy.deepcopy(seller)
        seller.destination = buyer.owner
        seller.amount = buyer.amount
        seller.processed = "combined"
        buyer.processed = "finished"
        new_order.amount -= buyer.amount
        new_order.destination = -1
        new_order.id = index
        new_order.processed = "free"
        return seller, [new_order], [], buyer

    # If buyer wants to buy more than seller has to sell, a new order will be created for the lacking amount
    if seller.amount < buyer.amount:
        new_order = copy.deepcopy(buyer)
        seller.destination = buyer.owner
        seller.processed = "combined"
        buyer.processed = "finished"
        new_order.amount -= seller.amount
        new_order.destination = -1
        new_order.id = index
        new_order.processed = "free"
        return seller, [], [new_order], buyer


# This function checks if a transaction forms a deal
def sales_calculator(asked, payed):

    #Checking that transaction is made within range of reason (5%)
    # If the selling price is just a little less than required, the price is reduced a bit by seller
    # If asked price is less than what the buyer is willing to pay, then the deal is made
    if asked == payed:
        return True
    if asked > payed:
        if asked <= payed*1.05 or asked/1.05 <= payed:
            return True
    elif asked < payed:
        return True

    return False



## Add distance to transactions
def transactions_distance(transactions, sett_objects):

    # loop through workorders and find the settlements 
    for order in transactions:
        if order.destination == -1:
            continue
        ord_settlement1 = order.owner
        for stlm1 in sett_objects:
            if stlm1.id == ord_settlement1:
                s_coordx = stlm1.coordx
                s_coordy = stlm1.coordy
        ord_settlement2 = order.destination
        for stlm2 in sett_objects:
            if stlm2.id == ord_settlement2:
                d_coordx = stlm2.coordx
                d_coordy = stlm2.coordy

        # send the settlement info to distance calculator
        order.distance, order.angle = distance_calculator((s_coordx, s_coordy), (d_coordx, d_coordy))
    


if __name__ == '__main__':
    
    ord_objects = create_workorders_from_configures()
    for o in ord_objects:
        print(o.__dict__)