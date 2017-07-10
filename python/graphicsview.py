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

pygame.init()
pygame.font.init()
pygame.display.set_caption("MASS Racing Engine Balancer")
screen = pygame.display.set_mode([cfg.WIDTH, cfg.HEIGHT])
graph = GraphWindow(screen)

def bytesToInt(array, start, separator):
    acc = 0
    while array[start] != separator:
        acc *= 10
        acc += (array[start] - 48)
        start += 1
    start += 1
    return (acc, start)

def init_serial():
    port.baudrate = 115200
    port.port = 'COM3'
    port.timeout = 0.1
    port.open()

def init_arrays():
    for i in range(cfg.ARRAY_SIZE+1):
        sensorAReadings.append(0)
        sensorBReadings.append(0)

def plot_arrays():
    i = 0
    while i < cfg.ARRAY_SIZE:
        graph.plotReading(i, sensorAReadings[i], sensorAReadings[i+1], cfg.SENSORACOLOUR)
        graph.plotReading(i, sensorBReadings[i], sensorBReadings[i+1], cfg.SENSORBCOLOUR)
        i += 1        

def mousebuttondown():
    pos = pygame.mouse.get_pos()
    #for button in buttons:
    #    if button.rect.collidepoint(pos):
    #        button.call_back()

def my_great_function():
    print("Great! " * 5)


def showUnsyncedMessages():
    graph.statusMessage("Unsynced!")
    graph.positionMessage("---")

def showPositionMessages(angleString):
    graph.statusMessage("Synced!")
    graph.positionMessage(angleString)
    
def showBalanceGraph(line):
    rpm_segement = bytesToInt(line, 1, 44)
    graph.statusMessage("RPM: " + str(rpm_segement[0]))
    parse_position = rpm_segement[1]
    i = 0
    max_i_size = cfg.ARRAY_SIZE - 1
    while ((line[parse_position] != 13) and (i < max_i_size)):
        a = bytesToInt(line, parse_position, 44)
        sensorAReadings[i] = a[0]
        b = bytesToInt(line, a[1], 44)
        sensorBReadings[i] = b[0]    
        parse_position = b[1]
        i += 1
    plot_arrays()
    graph.draw()

def handle_line(line):
    if (line != b''):
        if (line[0] == 78):
            showUnsyncedMessages()
        elif(line[0] == 80):
            showPositionMessages(str(bytesToInt(line, 1, 13)[0]))
        elif(line[0] == 82):
            showBalanceGraph(line)

showUnsyncedMessages()
graph.draw()
init_arrays()
plot_arrays()
init_serial()

#button = Button(screen, "Great!", (60, 30), my_great_function)
#buttons = [button]
#button.draw()

done = False

while not done:
    handle_line(port.readline())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttondown()
    pygame.display.update()
pygame.quit()