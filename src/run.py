#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

import os
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


# A group of settlement objects
setlist = []

# Generate objects from the settlement files
for stlm in sett_files:
    settlement_object = utils.file_to_object(stlm, setpath)
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


        screen.fill((255, 255, 255))

        # draw all settlements to screen
        for s in setlist:
            x = int(s.coordinate_X)
            y = int(s.coordinate_Y)
            pygame.draw.rect(screen, (0,0,0), (x, y, 5, 5))
        all_sprites.draw(screen)
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("Economy simulator")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    
    main()
 