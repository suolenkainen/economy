#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

import os
import pygame
import settlements

# town = towns.create_town()
# print(town_list.__dict__)

attributes = {}
attributes["coordinates"] = [100, 100]
attributes["workers"] = []
attributes["population"] = 10
attributes["goods"] = []
attributes["producers"] = []
attributes["base_wealth"] = 100
attributes["liquid_wealth"] = 100

# clear_settlements()

for i in range(1):
    attributes["index"] = i
    settlements.create_settlement(attributes)

# Path to "settlements" folder and list of settlement names
settlement_path = "resources\\settlements"
path = os.path.join(os.path.dirname(__file__), settlement_path)
sett_files = os.listdir(path)

# A group of settlement objects
setlist = []

# Generate objects from the settlement files
for stlm in sett_files:
    settlement_object = settlements.file_to_object(stlm)
    setlist.append(settlement_object)



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

        # Update sprites
        all_sprites.update()


        screen.fill((0, 0, 0))

        # draw all settlements to screen
        for settlement in setlist:
            x = int(settlement.coordinate_X)
            y = int(settlement.coordinate_Y)
            pygame.draw.rect(screen, (200,200,200), (x, y, 5, 5))
        all_sprites.draw(screen)
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    
    main()
 