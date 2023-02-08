import pygame
from pygame.locals import *


pygame.init()

window = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
runningAnim = True
background_color = (0,0,0)

t1 = pygame.Rect(100,100,200,200)

systemObjects = [['rect',t1,(0,0,225)]]
 
# Draws the surface object to the screen.
while runningAnim:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runningAnim = False
    clock.tick(30)
    window.fill(background_color)
    
    # Using draw.rect module of
    # pygame to draw the outlined rectangle
    pygame.draw.rect(window, (0, 0, 255),
                    t1)
                    
    #t1.move_ip((5,5))
    pygame.display.update()