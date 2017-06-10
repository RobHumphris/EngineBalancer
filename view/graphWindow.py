from tkinter import *
from tkinter import ttk

canvasWidth = 800
canvasHeight = 450
axisLength = 720
axisHeight = 400
axisColour = "#476042"
sensorAColour = "#FF0000"
sensorBColour = "#0000FF"
startX = 40
startY = 25
graphLineX = (axisLength / 2) + startX
graphLabelX = graphLineX + 10
graphLineY = (axisHeight / 2) + startY
graphLabelY = graphLineY + 10
xScalar = axisLength / 360
yScalar = axisHeight / 200

def getXfromAngle(angle): # 
    global startX, axisLength, xScalar
    retVal = (angle * xScalar) + startX
    return retVal

def getYFromValue(value):
    global startY, axisHeight
    retVal = axisHeight / 2
    if value > 0:
        retVal = retVal - (value * 2)
    elif value < 0:
        retVal = retVal + (0 - value * 2)
    return retVal + startY

def drawXTickAndLabel(angle, label):
    global canvas, graphLabelY, axisColour
    X = getXfromAngle(angle)
    canvas.create_text(X, graphLabelY, text=label)
    canvas.create_line(X, graphLineY, X, graphLineY + 5, fill=axisColour, width=2)

def drawYTickAndLabel(value, label):
    global canvas, graphLabelX
    Y = getYFromValue(value)
    canvas.create_text(graphLabelX, Y, text=label)

def drawGraphAxis():
    global canvas, startX, startY, graphLineX, graphLineY, axisHeight, axisLength, axisColour
    canvas.create_line(startX, graphLineY, axisLength + startX, graphLineY, fill=axisColour, width=2)
    canvas.create_line(graphLineX, startY, graphLineX, axisHeight + startY, fill=axisColour, width=2)
    drawXTickAndLabel(0, "0")
    drawXTickAndLabel(90, "90")
    drawXTickAndLabel(180, "180")
    drawXTickAndLabel(270, "270")
    drawXTickAndLabel(359, "359")
    drawYTickAndLabel(100, "100")
    drawYTickAndLabel(50, "50")
    drawYTickAndLabel(-50, "-50")
    drawYTickAndLabel(-100, "-100")

def plotReading(angle, value, colour):
    global canvas
    X = getXfromAngle(angle)
    Y = getYFromValue(value)
    canvas.create_line(X, Y, X+2, Y, fill=colour, width=2)

def statusMessage(message):
    global canvas, statusTextID
    canvas.itemconfig(statusTextID, text="Status: " + message)

def positionMessage(message):
    global canvas, positionTextID
    canvas.itemconfig(positionTextID, text=message)

def init():
    global canvas, root, statusTextID, positionTextID
    root = Tk()
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.grid(column=0, row=0, sticky=(N, W, E, S))
    statusTextID = canvas.create_text(5, 5, anchor="nw")
    positionTextID = canvas.create_text(5, 400, anchor="nw")

def loop():
    global root
    root.mainloop()

#drawGraphAxis()
#
#plotReading(45, 50, sensorAColour)
#plotReading(50, 55, sensorAColour)
#plotReading(55, 60, sensorAColour)
#
#plotReading(45, -50, sensorBColour)
#plotReading(50, -55, sensorBColour)
#plotReading(55, -60, sensorBColour)
