import pygame, sys
from button import *

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

def my_great_function():
    print("Great! " * 5)

def my_fantastic_function():
    print("Fantastic! " * 5)
 
def mousebuttondown():
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            button.call_back()

screen = pygame.display.set_mode((120, 100))

button_01 = Button(screen, "Great!", (60, 30), my_great_function)
button_02 = Button(screen, "Fantastic!", (60, 70), my_fantastic_function, bg=(50, 200, 20))
buttons = [button_01, button_02]
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttondown()
 
    for button in buttons:
        button.draw()

    pygame.display.flip()
    pygame.time.wait(40)
