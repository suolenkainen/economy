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
        if order.sell == True:
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
        if order >= len(selling):
            buying.extend(selling)
            break

    print(complete_orders)
    return complete_orders, buying



## Add distance to transactions
def transactions_distance(transactions):

    # loop through workorders and find the settlements 
    for order in transactions:
        ord_settlement1 = order.owner
        for stlm1 in settlement_list:
            if stlm1.name == ord_settlement1:
                starting = stlm1
        ord_settlement2 = order.destination
        for stlm2 in settlement_list:
            if stlm2.name == ord_settlement2:
                destination = stlm2
    
        # send the settlement info to distance calculator
        order.distance = utils.distance_calculator(starting, destination)
    


## Adjust the market prices based on non-successful transactions
def adjust_settlement_markets(workorders):

    # loop through workorders and combine them with settlements
    for order in workorders:
        ord_settlement = order.owner
        for stlm in settlement_list:
            if stlm.name == ord_settlement:

                # Adjust the market price for that product in that settlement
                if order.product in stlm.marketsell and order.sell == True:
                    sellprice = stlm.marketsell[order.product]
                    stlm.marketsell[order.product] = round(sellprice/1.05, 1)
                if order.product in stlm.marketbuy and order.sell == False:
                    buyprice = stlm.marketbuy[order.product]
                    stlm.marketbuy[order.product] = round(buyprice*1.05, 1)



## Find the closest worker to a transaction (not yet move it to there)
def reserving_transaction_to_worker(transactions):

    # loop through transactions and find the settlements and workers
    for order in transactions:

        # Only reserve orders that already don't have a worker assigned
        if order.reserved != "":
            continue
        
        # Workers will be sorted and eventually closest will be chosen
        sorted_workers = []

        # Find correct settlement info
        ord_settlement = order.owner
        for stlm1 in settlement_list:
            if stlm1.name == ord_settlement:
                starting = stlm1
                break

        # Find all workers not moving
        for worker in worker_list:
            if worker.speed != 0:
                continue
            wrk_settlement = worker.settlement
            for stlm2 in settlement_list:
                if stlm2.name == wrk_settlement:
                    destination = stlm2
                    break

            # send the settlement info to distance calculator
            worker.distance = utils.distance_calculator(starting, destination)
            sorted_workers.append(worker)
            sorted_workers = sorted(sorted_workers, key=lambda d: d.distance)
        
        # Attach the worker to the attributes in the transaction
        order.reserved = sorted_workers[0].name

        # Attach the transaction to worker's list (currently filename but later some other identifier)
        sorted_workers[0].workorders.append(order.filename)



## Add money to settlement, charge the selling settlement for taxes and remove goods from settlement
def begin_transaction(transactions):
    for order in transactions:

        # Only reserve orders that already don't have a worker assigned
        if order.reserved == "" or order.worker == "":
            continue

        # Find correct settlement info
        seller_stlm = order.owner
        for seller in settlement_list:
            if seller.name == seller_stlm:

                # Seller get's paid for the transaction and pays taxes and fees
                price = order.amount * order.price
                seller.liquid_wealth += price
                seller.liquid_wealth -= price*0.1

                # Remove goods from settlement
                try:
                    x = seller.goods[order.product]
                except:
                    seller.goods[order.product] = 0
                seller.goods[order.product] -= order.amount



## When worker is at 0 distance to transaction start, the worker will be owning the transaction
def worker_owning_transaction(transactions):
        # loop through transactions and find the settlements and workers
    for order in transactions:

        # Only reserve orders that already don't have a worker assigned
        if order.reserved == "":
            continue

        # Find correct settlement info
        ord_settlement = order.owner
        for stlm1 in settlement_list:
            if stlm1.name == ord_settlement:
                starting = stlm1
                break

        # Find all workers not moving
        for worker in worker_list:
            if worker.speed != 0:
                continue
            wrk_settlement = worker.settlement
            for stlm2 in settlement_list:
                if stlm2.name == wrk_settlement:
                    destination = stlm2
                    break

            # send the settlement info to distance calculator
            worker.distance = utils.distance_calculator(starting, destination)
            if worker.distance == 0:

                # Set the worker distance
                worker.settlement = order.destination
                worker.distance = order.distance
                worker.speed = worker.maxspeed
                order.worker = worker.name


## Move workers towards the destionation and make a list of finished journeys. This includer journeys to transaction starts
def worker_journey(transactions):
    
    # Find all workers with workorders
    finished_journeys = []
    for w in worker_list:
        for ord in transactions:
            if  ord.filename in w.workorders:
                for stlm in settlement_list:
                    if stlm.name == ord.destination:
                        # Move worker with their maximum speed towards destination 
                        speed = w.maxspeed
                        w.progression += speed
                        if w.progression >= w.distance:
                            finished_journeys.append(w.filename)
                            print("DONE")
                
    return finished_journeys



## On completing the journey, charge the settlement for goods and taxes and add them to settlement's goods


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

            # Make the display and settlements larger and add text next to them representing the workorders. 
            # Mark the workorders in other color if made into transactions


        ## Work orders are created by demand of a production place or a settlement population
        ## A production place always aims to have their resource storage filled and goods emptied
        ## If there isn't enough suppliers for a resource, the production place boosts up their buy market price
        ## If there is more than the capacity of resource storage being offered, production lowers market price
        ## If there is more demand than the supplier can produce, the sell price goes up
        ## If there isn't enough buyer for a good, the production place lowers their sell price
        ## All price modifications are calculated based on the surplus/lack of products -> Utilities
        ## The work orders are always attached to a settlement instead of the production place
        ## If there is no items not for sell at the requested price, the settlement will pay for maximum of 5% increase from the cheapest
        ## Settlement always buys from the cheapest supplier

        transactions, incomplete = combine_workorders()
        transactions_distance(transactions)
        adjust_settlement_markets(incomplete)

        ## If there is a requirement in some settlement for some resource and there is room in storage, check if there is workorder in near by settlement
        ## Order workers based on the closest settlement.
        ## If not the current settlement, travel to nearest settlement. If a workorder is larger than capacity of the worker, the workorder can be split into smaller pieces
        ## A workorder can be reserved for that worker
        ## Same worker can do two workorders from same starting place to same destination if there is capacity and enough workorders

        reserving_transaction_to_worker(transactions)
        worker_owning_transaction(transactions)
        begin_transaction(transactions)

        ## Worker walks until at destination
        finished_journeys = worker_journey(transactions)
        if finished_journeys != []:
            # handle the finished orders
            print(123)
        for w in worker_list:
            if w == 0:
                pass

        # def create_list_of_work_orders():
        #     pass
        #     return list_of_work_orders


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
 