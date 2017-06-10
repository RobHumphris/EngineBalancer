import graphWindow as gw

gw.init()
gw.drawGraphAxis()

gw.plotReading(45, 50, gw.sensorAColour)
gw.plotReading(50, 55, gw.sensorAColour)
gw.plotReading(55, 60, gw.sensorAColour)

gw.plotReading(45, -50, gw.sensorBColour)
gw.plotReading(50, -55, gw.sensorBColour)
gw.plotReading(55, -60, gw.sensorBColour)

gw.statusMessage("Unsynced!")
gw.positionMessage("Angle: 0°")

gw.loop()
