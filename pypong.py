import sys
import pygame
from pygame.locals import *
pygame.init()
pygame.display.set_mode((640,680))
pygame.display.set_caption('PyPongV0.0')
black = (0,0,0)
white = (255,255,255)
terrain = pygame.Surface(fenetre.get_size())
terrain.file(black)
pygame.draw.rect(terrain, white, Rect((5,5),(630,470),2))
pygame.draw.aaline(terrain, white, ((330,5),(330,475)))
while True : 
	draw(fenetre)
	pygame.display.update()
	fps.tick(60)