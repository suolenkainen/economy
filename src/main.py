#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy


import pygame
import settlements as sett
import utilities as utils
import workers as wrk
import workorders as ord
import producers as pro


### Running ID's for item types
settlement_last_id = 2
worker_last_id = 1
producer_last_id = 1
workorder_last_id = 2


# A group of settlement objects
sett_objects = []
wrk_objects = []
ord_objects = []
market = {"grain": {"high": 12.0, "low": 11.5}}


# Generate objects from configuration files
sett_objects = sett.create_settlements_from_configures()
wrk_objects = wrk.create_worker_from_configures()
ord_objects = ord.create_workorders_from_configures()
prod_objects = pro.create_producers_from_configures()



## Add distance to transactions
def transactions_distance(transactions):

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
        order.distance, order.angle = utils.distance_calculator((s_coordx, s_coordy), (d_coordx, d_coordy))
    


## Find the closest worker to a transaction (not yet move it to there)
def reserving_transaction_to_worker(transactions):

    # loop through transactions and find the settlements and workers
    for order in transactions:

        # Only reserve orders that already don't have a worker assigned
        if order.reserved != -1 or order.worker != -1:
            continue
        
        # Workers will be sorted and eventually closest will be chosen
        sorted_workers = []

        # Find starting settlement
        s_coordx, s_coordy = utils.endpoint_calculator(order, sett_objects, "owner")

        for worker in wrk_objects:
            if worker.speed != 0:
                continue

            # Find destination settlement send the settlement info to distance calculator
            d_coordx, d_coordy = utils.endpoint_calculator(worker, sett_objects, "settlementid")

            # send the settlement info to distance calculator
            worker.distance, worker.angle = utils.distance_calculator((s_coordx, s_coordy), (d_coordx, d_coordy))

            # If a worker has reserved to settlement, worker cannot be attached to another settlement
            # This is calculated by checking the the order owner against orders assigned previously
            skip = False

            for tr in transactions:
                if tr.id in worker.workorders and tr.owner == order.owner:
                    skip = True
                    break

            if skip == False:
                sorted_workers.append(worker)
        
        sorted_workers = sorted(sorted_workers, key=lambda d: d.distance)
        
        # Attach the worker to the attributes in the transaction
        if sorted_workers != []:
            order.reserved = sorted_workers[0].id
            sorted_workers[0].workorders.append(order.id)
            sorted_workers[0].settlement = order.owner



## Add money to settlement, charge the selling settlement for taxes and remove goods from settlement
def begin_transaction(transactions):
    for order in transactions:

        if order.processed in ["sold", "paid"]:
            continue

        # Find correct settlement info
        seller_stlm = order.owner
        for seller in sett_objects:
            if seller.id == seller_stlm:

                # Seller get's paid for the transaction and pays taxes and fees
                price = order.amount * order.price
                seller.liquidwealth += price
                seller.liquidwealth -= price*0.1

                # Remove goods from settlement
                try:
                    x = seller.goods[order.product]
                except:
                    seller.goods[order.product] = 0
                seller.goods[order.product] -= order.amount

                order.processed = "sold"



## When worker is at 0 distance to transaction start, the worker will be owning the transaction
def worker_owning_transaction(transactions):

    # loop through transactions and find the settlements and workers
    for order in transactions:
        
        # Only reserve orders that already don't have a worker assigned
        if order.reserved == -1:
            continue

        # Find starting settlement and destination settlement
        s_coordx, s_coordy = utils.endpoint_calculator(order, sett_objects, "owner")
        for worker in wrk_objects:
            d_coordx, d_coordy = worker.coordx, worker.coordy
            dist, angle = utils.distance_calculator((int(s_coordx), int(s_coordy)), (int(d_coordx), int(d_coordy)))
            
            # If a worker is in the settlement, worker owns the transaction and starts journey
            if dist == 0 and worker.type != "assigned":

                # Set the worker and order attributes from transaction owning
                worker.angle = order.angle
                worker.settlement = order.destination
                worker.distance = order.distance
                worker.speed = worker.maxspeed
                order.worker = worker.id
                order.reserved = -1
                worker.type = "assigned"
                break



## Move workers towards the destionation and make a list of finished journeys. This includer journeys to transaction starts
def worker_journey():
    
    # Find all workers with workorders
    finished_orders = []
    for w in wrk_objects:
        if w.speed != 0 and w.distance != 0:
                
                ## Moving the worker
                w.progression += w.speed
                utils.update_worker_coordinates(w)

                ## When worker arriver to destination, finish the order and stop the worker
                if w.progression >= w.distance and w.type == "assigned":
                    
                    # Setting the worker coordinates to match the settlement
                    for o in ord_objects:
                        if o.id in w.workorders:
                            for s in sett_objects:
                                if s.id == o.destination:
                                    w.coordx = s.coordx
                                    w.coordy = s.coordy
                                    break
                            break

                    # Set the worker attributes
                    w.distance = 0
                    w.progression = 0
                    w.speed = 0
                    w.angle = 0
                    finished_orders.extend(w.workorders)
                    print("DONE")

    return finished_orders



def unattached_worker_towards_workorder(transactions):

    ## Checking for workorders which have reserved but worker isn't at the place
    for order in transactions:
        for worker in wrk_objects:
            if order.reserved == worker.id:
                print(worker.name)
                if worker.speed != 0 and worker.distance != 0:
                        
                        ## When worker arriver to destination, finish the order and stop the worker
                        if worker.progression >= worker.distance:
                            
                            # Setting the worker coordinates to match the settlement
                            for o in ord_objects:
                                if o.id in worker.workorders:
                                    for s in sett_objects:
                                        if s.id == o.owner:
                                            worker.coordx = s.coordx
                                            worker.coordy = s.coordy
                                            break
                                    break

                            # Set the worker distance
                            worker.angle = order.angle
                            worker.settlement = order.destination
                            worker.progression = 0
                            worker.distance = order.distance
                            worker.speed = worker.maxspeed
                            order.worker = worker.id
                            order.reserved = -1
                            worker.type = "assigned"
                else:
                    s_coordx, s_coordy = worker.coordx, worker.coordy
                    d_coordx, d_coordy = utils.endpoint_calculator(order, sett_objects, "owner")
                    distance, angle = utils.distance_calculator((s_coordx, s_coordy), (d_coordx, d_coordy))
                    distance, angle = utils.distance_calculator((200, 170), (440, 190))
                    worker.speed = worker.maxspeed
                    worker.distance = distance
                    worker.angle = angle
                    worker.type = "travel"



## On completing the journey, charge the settlement for goods and taxes and add them to settlement's goods
def end_transactions(finished_orders, transactions):
    
    # Check which transactions have been ended
    for o_id in finished_orders:
        for t in transactions:
            if t.id == o_id: 
                transaction = t 
                break
        
        # connect transaction to the buyer's settlement
        for s in sett_objects:
            if transaction.destination == s.id:
                buyer = s
                break
        
        # Charge the buyer town accordingly
        price = transaction.amount * transaction.price
        buyer.liquidwealth -= price
        buyer.liquidwealth -= price*0.1

        # Add goods to their supply
        try:
            x = buyer.goods[transaction.product]
        except:
            buyer.goods[transaction.product] = 0
        buyer.goods[transaction.product] += transaction.amount

        # Remove transaction
        transactions.remove(transaction)
        ord_objects.remove(transaction)

    return transactions


"""
MAIN LOOP:
This contains the main actions that call other functions in the module
"""

def main():

    running = True

    while running:
        # keep loop running at the right speed
        clock.tick(10)

        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))


        ### ALL Drawing are now for the sake of demoing. They will be done separately later.
        # Draw all settlements to screen
        for s in sett_objects:
            x = int(s.coordx)
            y = int(s.coordy)
            pygame.draw.rect(screen, (0,0,0), (x, y, 10, 10))
            font = pygame.font.SysFont("Arial", 10)
            img = font.render(s.name, True, (0,0,0))
            screen.blit(img, (x + 15, y-2))
            img = font.render("population: "+ str(s.population), True, (0,0,0))
            screen.blit(img, (x + 15, y+12))
            
            for w in wrk_objects:
                
                # Draw an amber dor in the settlement if there's a worker in there
                if w.settlementid == s.id and w.speed == 0:
                    pygame.draw.rect(screen, (210,210,110), (w.coordx + 2, w.coordy + 2, 6, 6))
                
                # Draw a marker of the worker on screen
                pygame.draw.rect(screen, (0,0,110), (w.coordx + 4, w.coordy + 4, 2, 2))
                font = pygame.font.SysFont("Arial", 10)
                img = font.render(w.name, True, (0,0,0))
                screen.blit(img, (w.coordx + 10, w.coordy - 2))

            # Make the display and settlements larger and add text next to them representing the workorders. 
            # Mark the workorders in other color if made into transactions


        ## Work orders are created by demand of a production place or a settlement population
        ## A production place always aims to have their resource storage filled and goods emptied
        ## The work orders are always attached to a settlement instead of the production place
        ## If there is no items not for sell at the requested price, the settlement will pay for maximum of 5% increase from the cheapest
        ## Settlement always buys from the cheapest supplier

        transactions, incomplete = ord.combine_workorders(ord_objects)



        ## If there is a requirement in some settlement for some resource and there is room in storage, check if there is workorder in near by settlement
        ## Order workers based on the closest settlement.

        transactions_distance(transactions)



        ## If there isn't enough suppliers for a resource, the production place boosts up their buy market price
        ## If there is more than the capacity of resource storage being offered, production lowers market price
        ## If there is more demand than the supplier can produce, the sell price goes up
        ## If there isn't enough buyer for a good, the production place lowers their sell price
        ## All price modifications are calculated based on the surplus/lack of products -> Utilities
        
        sett.adjust_settlement_markets(incomplete, sett_objects)



        ## If not the current settlement, travel to nearest settlement. If a workorder is larger than capacity of the worker, the workorder can be split into smaller pieces
        ## A workorder can be reserved for that worker
        ## Same worker can do two workorders from same starting place to same destination if there is capacity and enough workorders (TODO)

        reserving_transaction_to_worker(transactions)
        


        ## In addition to workers making a purchase journey, they can move to a work order settlement
        ## start moving workers to destinations based on their work order.

        worker_owning_transaction(transactions)
        unattached_worker_towards_workorder(transactions)
        begin_transaction(transactions)



        ## Worker walks until at destination
        finished_orders = worker_journey()


        
        ## The work order always costs to a settlement 10% of the selling fee and for purchase fee
        ## The goods are then attached to that settlement and distributed between production placed by percentage of nee
        if finished_orders != []:
            transactions = end_transactions(finished_orders, transactions)

        


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
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Economy simulator")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    
    main()
 