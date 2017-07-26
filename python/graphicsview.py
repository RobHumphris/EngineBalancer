# Colours from http://www.colourlovers.com/palette/38562/Hands_On
import pygame
import serial
from graph_window import *
from button import *
import settings as cfg

sensor_a_zero = 320
sensor_b_zero = 0
sample_count = 0
maximums_count = 0

sensorAReadings = []
sensorAMaximums = []
sensorBReadings = []
sensorBMaximums = []

buttons = []
port = serial.Serial()

pygame.init()
pygame.font.init()
pygame.display.set_caption("MASS Racing Engine Balancer")
screen = pygame.display.set_mode([cfg.WIDTH, cfg.HEIGHT])
graph = GraphWindow(screen)

def bytesToInt(array, start, separator):
    acc = 0
    l = len(array)
    while ((start < l) and (array[start] != separator)):
        acc *= 10
        acc += (array[start] - 48)
        start += 1
    start += 1
    return (acc, start)

def init_serial():
    port.baudrate = cfg.COM_BAUD
    port.port = cfg.COM_PORT
    port.timeout = 0.1
    port.open()

def init_arrays():
    for i in range(cfg.ARRAY_SIZE+1):
        sensorAReadings.append(0)
        sensorBReadings.append(0)

def plot_arrays():
    global sample_count
    sample_count = sample_count + 1
    if (sample_count >  cfg.SAMPLE_COUNT) :
        sample_count = 0
        i = 0
        sensorAReadings[i] = sensorAReadings[i] / cfg.SAMPLE_COUNT
        sensorBReadings[i] = sensorBReadings[i] / cfg.SAMPLE_COUNT
        while i < cfg.ARRAY_SIZE:
            j = i+1
            sensorAReadings[j] = sensorAReadings[j] / cfg.SAMPLE_COUNT
            sensorBReadings[j] = sensorBReadings[j] / cfg.SAMPLE_COUNT
            graph.plotReading(i, sensorAReadings[i], sensorAReadings[j], cfg.SENSORACOLOUR)
            graph.plotReading(i, sensorBReadings[i], sensorBReadings[j], cfg.SENSORBCOLOUR)
            i += 1
        graph.draw()  
 
#def my_great_function():
#    print("Clear")
#    graph.clear()

#button = Button(screen, "Clear", (60, 30), my_great_function)
#buttons = [button]
#button.draw()

def mousebuttondown():
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            button.call_back()

def showUnsyncedMessages():
    graph.statusMessage("Unsynced!")
    graph.positionMessage("---")

def showPositionMessages(angleString):
    graph.statusMessage("Synced!")
    graph.positionMessage(angleString)

def handleLineMaximum(sensorAMax, sensorBMax):
    global sensorAMaximums, sensorBMaximums
    sensorAMaximums.append(sensorAMax)
    sensorBMaximums.append(sensorBMax)
    count = len(sensorAMaximums)
    if (count >= 10):
        acc_a = (0, 0)
        acc_b = (0, 0)
        for i in range(0, count):
            acc_a = (acc_a[0] + sensorAMaximums[i][0], acc_a[1] + sensorAMaximums[i][1])
            acc_b = (acc_b[0] + sensorBMaximums[i][0], acc_b[1] + sensorBMaximums[i][1])
        avg_a = ((acc_a[0] / count), (acc_a[1] / count))
        avg_b = ((acc_b[0] / count), (acc_b[1] / count))
        sensorAMaximums = []
        sensorAMaximums.append(avg_a)
        sensorBMaximums = []
        sensorBMaximums.append(avg_b)
        print("Peak Average A. Angle:" + str(round(avg_a[1], 2)) + "°  Value:" + str(round(avg_a[0], 2)))
        #print("Peak Average B. Angle:" + str(avg_b[1]) + "°  Value:" + str(avg_b[0]))    

def showBalanceGraph(line):
    if (len(line) > 500):
        rpm_segement = bytesToInt(line, 1, 44)
        graph.statusMessage("RPM: " + str(rpm_segement[0]))
        parse_position = rpm_segement[1]
        i = 0
        sensorAMax = (0, 0)
        sensorBMax = (0, 0)
        max_parse_position = len(line)
        try:
            while ((i < 89) and (parse_position < max_parse_position) and (line[parse_position] != 10)):
                a = bytesToInt(line, parse_position, 44)
                sensor_a = (a[0] - sensor_a_zero)
                if (sensor_a >= sensorAMax[0]):
                    sensorAMax = (sensor_a, i)
                sensorAReadings[i] = sensorAReadings[i] + sensor_a

                b = bytesToInt(line, a[1], 44)
                sensor_b = (b[0] - sensor_b_zero)
                if (sensor_b >= sensorBMax[0]):
                    sensorBMax = (sensor_b, i)
                sensorBReadings[i] = sensorBReadings[i] + sensor_b

                parse_position = b[1]
                i += 1

            plot_arrays()
            handleLineMaximum(sensorAMax, sensorBMax)
        except:
            print("BANG! i=" + str(i) + " p pos: " + str(parse_position))
            raise

def handleZeroCalibration(line):
    tmp = bytesToInt(line, 1, 44)
    #sensor_a_zero = tmp[0]
    tmp = bytesToInt(line, tmp[1], 10)
    sensor_b_zero = tmp[0]
    print("Channel A Zero: " + str(sensor_a_zero) + " Channel B Zero: " + str(sensor_b_zero))

def handle_line(line):
    if (line != b''):
        if (line[0] == 78):
            showUnsyncedMessages()
        elif(line[0] == 80):
            showPositionMessages(str(bytesToInt(line, 1, 13)[0]))
        elif(line[0] == 82):
            showBalanceGraph(line)
        elif(line[0] == 67):
            handleZeroCalibration(line)

showUnsyncedMessages()
graph.draw()
init_arrays()
plot_arrays()
init_serial()

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