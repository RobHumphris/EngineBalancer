import graphWindow as gw
import math

sensorAReadings = []
sensorBReadings = []

def initArrays():
    for i in range(360):
        r = math.radians(i)
        sensorAReadings.append(math.sin(r)*50)
        sensorBReadings.append(math.cos(r)*50)

def plotArrays():
    for i in range(360):
        gw.plotReading(i, sensorAReadings[i], gw.sensorAColour)
        gw.plotReading(i, sensorBReadings[i], gw.sensorBColour)

initArrays()
plotArrays()

gw.statusMessage("Unsynced!")
gw.positionMessage("Angle: 0°")

gw.loop()
