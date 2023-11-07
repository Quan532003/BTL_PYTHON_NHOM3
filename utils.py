import pygame
from constants import *

def limit_screen(target):
    if target.x + target.width > GAME_WIDTH:
        target.x = GAME_WIDTH - target.width
    if target.x < 0:
        target.x = 0
    if target.y + target.height > GAME_HEIGHT:
        target.y = GAME_HEIGHT - target.height
    if target.y < GAME_TOP_LIMIT:
        target.y = GAME_TOP_LIMIT

def drawBar(screen):
    pygame.draw.rect(screen, (0,0,0), (0, 2, 100 * 2 + 2, 22))
    pygame.draw.rect(screen, (255,255,255), (0, 3, 100 * 2 , 20))
    pygame.draw.rect(screen, (0,0,0), (0, 24, 100 * 2 + 2, 22))
    pygame.draw.rect(screen, (255,255,255), (0, 25, 100 * 2 , 20))