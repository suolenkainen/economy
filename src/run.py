#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

import pygame
import towns, resources, workers

# town = towns.create_town()
# print(town_list.__dict__)

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
		all_sprites.draw(screen)
		pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

if __name__ == '__main__':
	
	main()
 