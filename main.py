from settings import *
from controller import Controller
import pygame

pygame.init()
# Beta 0.1
# 666 lines of code

icon_image = pygame.image.load("assets/icon.png")

screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Not Another Tetris 0.1b")
pygame.display.set_icon(icon_image)
clock = pygame.time.Clock()

controller = Controller(screen, False)

while True:		
	# Concept:
	# 				  SOUND
	#                   \ 
	# GAME_LOGIC - CONTROLLER - VIEW
	controller.update()

	# Update Buffer
	pygame.display.flip()
	clock.tick(FPS)