# Colours from http://www.colourlovers.com/palette/38562/Hands_On
import pygame
import math
from graph_window import *
from button import *
import settings as cfg

sensorAReadings = []
sensorBReadings = []

def init_arrays():
    for i in range(360):
        r = math.radians(i)
        sensorAReadings.append(math.sin(r)*50)
        sensorBReadings.append(math.cos(r)*50)

def plot_arrays(graph):
    for i in range(360):
        graph.plotReading(i, sensorAReadings[i], cfg.SENSORACOLOUR)
        graph.plotReading(i, sensorBReadings[i], cfg.SENSORBCOLOUR)

def mousebuttondown():
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            button.call_back()

def my_great_function():
    print("Great! " * 5)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([cfg.WIDTH, cfg.HEIGHT])
screen.fill(cfg.SCREEN)

graph = GraphWindow(screen)
graph.statusMessage("Unsynced!")
graph.positionMessage("Angle: 0°")
graph.draw()
init_arrays()
plot_arrays(graph)

button = Button(screen, "Great!", (60, 30), my_great_function)
buttons = [button]

button.draw()

pygame.display.set_caption("MASS Racing Engine Balancer")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttondown()

    pygame.display.update()

pygame.quit()