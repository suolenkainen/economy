#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## workorder.py
## TODO: Description

import os, copy
from src.utilities import conf_data_to_attribute_list

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
path = os.path.join(os.path.dirname(__file__), "resources")



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

    selling = []
    buying = []
    complete_orders = []

<<<<<<< HEAD
    # Divide the selling and buying into their of lists and sort them 
=======
    # Divide the selling and buying into their of lists and sort them continuously
>>>>>>> ce30ade81738c31290777b6ae3fa71697e168ade
    for order in ord_objects:
        if order.sell == True:
            selling.append(order)
        else:
            buying.append(order)
<<<<<<< HEAD
    selling = sorted(selling, key=lambda d: d.price, reverse=True)
    buying = sorted(buying, key=lambda d: d.price)

    # Pairing sell and purchase orders so that the most expensive item is sold first to the least paying settlement and then increasing in price
    order = 0
    while len(selling) > 0: 
=======
        selling = sorted(selling, key=lambda d: d.price, reverse=True)
        buying = sorted(buying, key=lambda d: d.price)

    # Pairing sell and purchase orders so that the most expensive item is sold first to the least paying settlement and then increasing in price
    order = 0
    while True: 
>>>>>>> ce30ade81738c31290777b6ae3fa71697e168ade
        sold = selling[order]
        if sold.processed == "sold":
            complete_orders.append(sold)
            order += 1
            if order >= len(selling):
                buying.extend(selling)
                break
            continue
        if buying == []:
            deal = False
        for request in buying:
            deal = False
            
            # Matching the products
            if sold.product == request.product:
                deal = sales_calculator(sold.price, request.price)
            else:
                continue
<<<<<<< HEAD

=======
>>>>>>> ce30ade81738c31290777b6ae3fa71697e168ade
        order += 1

        #when deal is formed, the deal is put into a list of completed transactions. If some of the goods are not sold or remaining in the order, a new order is created
        if deal:
            complete_order, newsale, newbuy = match_orders(sold, request)
            ord_objects.remove(request)
            complete_orders.append(complete_order)
            buying.remove(request)
            buying.extend(newbuy)
            selling.remove(sold)
            selling.extend(newsale)

            #when adding and removing items from lists, they are sorted again
<<<<<<< HEAD
            buying = sorted(buying, key=lambda d: d.price)
            selling = sorted(selling, key=lambda d: d.price, reverse=True)
            order = 0
            if len(buying) == 0 or len(selling) == 0:
                buying.extend(selling)
                selling = []
        if len(selling) == 0 or order >= len(selling):
=======
            if len(buying) == 0 and len(selling) == 0:
                buying = sorted(buying, key=lambda d: d.price)
                selling = sorted(selling, key=lambda d: d.price, reverse=True)
                order = 0
            else:
                buying.extend(selling)
                break
        if order >= len(selling):
>>>>>>> ce30ade81738c31290777b6ae3fa71697e168ade
            buying.extend(selling)
            break

    return complete_orders, buying

<<<<<<< HEAD
=======
    ## Why doesn't this return selling orders?


>>>>>>> ce30ade81738c31290777b6ae3fa71697e168ade

## If we create new orders on the fly, how do we handle identifiers?
def match_orders(seller, buyer):
    # If workorders match each other, the seller order is updated and buy-order is removed
    if seller.amount == buyer.amount:
        seller.destination = buyer.owner
        return seller, [], []

    # If seller has more than buyer is willing to buy, a new order will be created for the surplus
    if seller.amount > buyer.amount:
        new_order = copy.deepcopy(seller)
        seller.destination = buyer.owner
        seller.amount = buyer.amount
        new_order.amount -= buyer.amount
        new_order.destination = -1
        return seller, [new_order], []

    # If buyer wants to buy more than seller has to sell, a new order will be created for the lacking amount
    if seller.amount < buyer.amount:
        new_order = copy.deepcopy(buyer)
        seller.destination = buyer.owner
        new_order.amount -= seller.amount
        new_order.destination = -1
        return seller, [], [new_order]



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



if __name__ == '__main__':
    
    ord_objects = create_workorders_from_configures()
    for o in ord_objects:
        print(o.__dict__)