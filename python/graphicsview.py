# Colours from http://www.colourlovers.com/palette/38562/Hands_On
import pygame
import math
import serial
from graph_window import *
from button import *
import settings as cfg

sensorAReadings = []
sensorBReadings = []
port = serial.Serial()

def init_serial():
    port.baudrate = 115200
    port.port = 'COM3'
    port.timeout = 0.1
    port.open()

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

def handle_line(line):
    print(line)
    if (line != b''):
        if (line[0] == 78) :
            graph.statusMessage("Unsynced!")
        elif(line[0] == 80) :
            graph.statusMessage("Synced!")

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

init_serial()

button = Button(screen, "Great!", (60, 30), my_great_function)
buttons = [button]

button.draw()

pygame.display.set_caption("MASS Racing Engine Balancer")

done = False
clock = pygame.time.Clock()

while not done:
    handle_line(port.readline())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttondown()

    pygame.display.update()

pygame.quit()