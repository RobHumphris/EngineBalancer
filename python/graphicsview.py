# Colours from http://www.colourlovers.com/palette/38562/Hands_On
import pygame
import serial
from graph_window import *
from button import *
import settings as cfg

sensor_a_zero = 0
sensor_b_zero = 0
sample_count = 0
maximums_count = 0

sensor_a_readings = []
sensor_a_maximums = []
sensor_b_readings = []
sensor_b_maximums = []

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
        sensor_a_readings.append(0)
        sensor_b_readings.append(0)

def plot_arrays():
    global sample_count
    sample_count = sample_count + 1
    if (sample_count >  cfg.SAMPLE_COUNT) :
        sample_count = 0
        i = 0
        sensor_a_readings[i] = sensor_a_readings[i] / cfg.SAMPLE_COUNT
        sensor_b_readings[i] = sensor_b_readings[i] / cfg.SAMPLE_COUNT
        while i < cfg.ARRAY_SIZE:
            j = i+1
            sensor_a_readings[j] = sensor_a_readings[j] / cfg.SAMPLE_COUNT
            sensor_b_readings[j] = sensor_b_readings[j] / cfg.SAMPLE_COUNT
            graph.plotReading(i, sensor_a_readings[i], sensor_a_readings[j], cfg.SENSORACOLOUR)
            graph.plotReading(i, sensor_b_readings[i], sensor_b_readings[j], cfg.SENSORBCOLOUR)
            i += 1
        graph.draw()  

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

def resetMaximums(avg_a, avg_b):
    global sensor_a_maximums, sensor_b_maximums
    sensor_a_maximums = []
    sensor_a_maximums.append(avg_a)
    sensor_b_maximums = []
    sensor_b_maximums.append(avg_b)

def handleLineMaximum(sensorAMax, sensorBMax):
    global sensor_a_maximums, sensor_b_maximums
    sensor_a_maximums.append(sensorAMax)
    sensor_b_maximums.append(sensorBMax)
    count = len(sensor_a_maximums)
    if (count >= 10):
        acc_a = (0, 0)
        acc_b = (0, 0)
        for i in range(0, count):
            acc_a = (acc_a[0] + sensor_a_maximums[i][0], acc_a[1] + sensor_a_maximums[i][1])
            acc_b = (acc_b[0] + sensor_b_maximums[i][0], acc_b[1] + sensor_b_maximums[i][1])
        avg_a = ((acc_a[0] / count), (acc_a[1] / count))
        avg_b = ((acc_b[0] / count), (acc_b[1] / count))
        #resetMaximums(avg_a, avg_b)
        #print("Peak Average A. Angle:" + str(round((avg_a[1]*cfg.ANGLE_MULTIPLE))) + "°  Value:" + str(round(avg_a[0])))
        graph.plotMaximum(avg_a)
        print("Peak Average B. Angle:" + str(round(avg_b[1]*cfg.ANGLE_MULTIPLE)) + "°  Value:" + str(round(avg_b[0])))    

def __showBalanceGraph(line):
    global sensor_a_zero, sensor_b_zero
    line.split

def showBalanceGraph(line):
    global sensor_a_zero, sensor_b_zero
    if (len(line) > 500):
        rpm_segement = bytesToInt(line, 1, 44)
        rpm = rpm_segement[0]
        graph.statusMessage("RPM: " + str(rpm))
        if (rpm > 494):
            parse_position = rpm_segement[1]
            i = 0
            sensor_a_max = (0, 0)
            sensor_b_max = (0, 0)
            max_parse_position = len(line) - 2
            try:
                while (parse_position < max_parse_position):
                    a = bytesToInt(line, parse_position, 44)
                    sensor_a = (a[0] - sensor_a_zero)
                    if (sensor_a >= sensor_a_max[0]):
                        sensor_a_max = (sensor_a, i)
                    sensor_a_readings[i] = sensor_a_readings[i] + sensor_a

                    b = bytesToInt(line, a[1], 44)
                    sensor_b = (b[0] - sensor_b_zero)
                    if (sensor_b >= sensor_b_max[0]):
                        sensor_b_max = (sensor_b, i)
                    sensor_b_readings[i] = sensor_b_readings[i] + sensor_b

                    parse_position = b[1]
                    i += 1

                plot_arrays()
                handleLineMaximum(sensor_a_max, sensor_b_max)
            except:
                print("BANG! i=" + str(i) + " p pos: " + str(parse_position))
                raise

def handleZeroCalibration(line):
    global sensor_a_zero, sensor_b_zero
    tmp = bytesToInt(line, 2, 44)
    sensor_a_zero = tmp[0]
    tmp = bytesToInt(line, tmp[1], 13)
    sensor_b_zero = tmp[0]
    graph.statusMessage("Calibrating...")
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

#def my_great_function():
#    print("Clear")
#    graph.clear()

#button = Button(screen, "Clear", (60, 30), my_great_function)
#buttons = [button]
#button.draw()