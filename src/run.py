#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

import os
from numpy import place
import pygame
import settlements as smtns
import utilities as utils

# town = towns.create_town()
# print(town_list.__dict__)

for i in range(1):
    attr = smtns.create_attributes()
    attr["index"] = i
    smtns.create_settlement(attr)

# Path to "settlements" folder and list of settlement names
settlement_path = "resources\\settlements"
setpath = os.path.join(os.path.dirname(__file__), settlement_path)
sett_files = os.listdir(setpath)

# Path to "workers" folder and list of worker names
worker_path = "resources\\workers"
wrkpath = os.path.join(os.path.dirname(__file__), worker_path)
work_files = os.listdir(wrkpath)

# Path to "workorder" folder and list of workorder names
workorder_path = "resources\\workorders"
ordpath = os.path.join(os.path.dirname(__file__), workorder_path)
workorder_files = os.listdir(ordpath)

# A group of settlement objects
settlement_list = []
worker_list = []
existing_workorder_list = []

# Generate objects from the settlement files
for s in sett_files:
    settlement_obj = utils.file_to_object(s, setpath)
    settlement_list.append(settlement_obj)

for w in work_files:
    workr_obj = utils.file_to_object(w, wrkpath)
    worker_list.append(workr_obj)

for o in workorder_files:
    workorder_obj = utils.file_to_object(o, ordpath)
    existing_workorder_list.append(workorder_obj)


## Combine buying and selling orders

def combine_workorders():

    selling = []
    buying = []
    complete_orders = []

    # Divide the selling and buying into their of lists and sort them continuously
    for order in existing_workorder_list:
        if order.sell == "True":
            selling.append(order)
        else:
            buying.append(order)
        selling = sorted(selling, key=lambda d: d.price, reverse=True)
        buying = sorted(buying, key=lambda d: d.price)

    # Pairing sell and purchase orders so that the most expensive item is sold first to the least paying settlement and then increasing in price
    order = 0
    while True: 
        sold = selling[order]
        for request in buying:
            deal = False
            
            # Matching the products
            if sold.product == request.product:
                deal = utils.sales_calculator(sold.price, request.price)
            else:
                continue
        order += 1

        #when deal is formed, the deal is put into a list of completed transactions. If some of the goods are not sold or remaining in the order, a new order is created
        if deal:
            complete_order, newsall, newbuy = utils.combine_workorders(sold, request)
            complete_orders.append(complete_order)
            buying.remove(request)
            buying.extend(newbuy)
            selling.remove(sold)
            selling.extend(newsall)

            #when adding and removing items from lists, they are sorted again
            if len(buying) == 0 and len(selling) == 0:
                buying = sorted(buying, key=lambda d: d.price)
                selling = sorted(selling, key=lambda d: d.price, reverse=True)
                order = 0
            else:
                buying.extend(selling)
                break
        if order > len(selling):
            break

    print(complete_orders)
    return complete_orders, buying

    # handle the remaining sell and buy orders and how they affect the prices


"""
MAIN LOOP:
This contains the main actions that call other functions in the module
"""

def main():

    running = True

    while running:
        # keep loop running at the right speed
        clock.tick(5)

        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Draw all settlements to screen
        for s in settlement_list:
            x = int(s.coordinate_X)
            y = int(s.coordinate_Y)
            pygame.draw.rect(screen, (0,0,0), (x, y, 5, 5))

        ## Work orders are created by demand of a production place or a settlement population
        ## A production place always aims to have their resource storage filled and goods emptied
        ## If there isn't enough suppliers for a resource, the production place boosts up their buy market price
        ## If there is more than the capacity of resource storage being offered, production lowers market price
        ## If there is more demand than the supplier can produce, the sell price goes up
        ## If there isn't enough buyer for a good, the production place lowers their sell price
        ## All price modifications are calculated based on the surplus/lack of products -> Utilities
        ## The work orders are always attached to a settlement instead of the production place
        ## If there is no items not for sell at the requested price, the settlement will pay for maximum of 5% increase from the cheapest
        ## Settlement always buys from the cheapers supplier



        ## If there is a requirement in some settlement for some resource and there is room in storage, check if there is workorder in near by settlement
        ## Order workers based on the closest settlement.
        ## If not the current settlement, travel to nearest settlement. If a workorder is larger than capacity of the worker, the workorder can be split into smaller pieces
        ## A workorder can be reserved for that worker
        ## Same worker can do two workorders from same starting place to same destination if there is capacity and enough workorders

        # def create_list_of_work_orders():
        #     pass
        #     return list_of_work_orders

        transactions, incomplete = combine_workorders()

        # for activeworker in worker_list:
        #     def search_for_nearest_requirement():
        #         pass
        #         return list of workers sorted by closeness to some requirement

        # for closest_worker_to_resource in worker_list:
        #     if list_of_work_orders is reserved, then redo calculation for that worker and sort to correct place
        #     remove payment amount from city and 
        #     end result is attaching all workers to work orders.



        ## Start moving workers to destinations based on their work order.
        ## The work order always costs to a settlement 10% of the selling fee and for purchase fee
        ## The goods are then attached to that settlement and distributed between production placed by percentage of need

        # def move_workers_towards_destination():
        #     pass
        #     check if arrived
        
        # def unload_goods_to_settlement():
        #     receive payment



        ## Resource goods are depleted from settlements by producers
        ## If a settlement has goods that are used by producers they are moved to that producers storage.
        ## If there is no room in production storage, no work orders are made for that good

        

        ## A settlement has needs based on the population. -> Utilities
        ## If a need is met, settlement can grow in population by some amount per turn
        ## If the needs are not met, the population decreases
        ## Based on the population, new production sites can appear to a settlement and production sites can increase and decrease
        ## If a production site decreases to 0, it is removed from settlement



        ## Future: Create paths the workers take to move between settlements. In crossroads, there might be a new settlement.
        ## Needs to have some mechanic to always go through the nearest settlement to reach the true destination


        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("Economy simulator")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    
    main()
 