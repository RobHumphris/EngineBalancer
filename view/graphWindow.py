from tkinter import *
from tkinter import ttk
from tkinter import font
from fullScreen import *

canvasWidth = 800
canvasHeight = 450
axisLength = 720
axisHeight = 400

axisColour = "#94BA65"
canvasColour = "#4E4D4A"
sensorAColour = "#FF0000"
sensorBColour = "#0000FF"
statusMessageColour = "#2790B0"
zColour = "#2B4E72"

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
    global canvas, graphLabelY, axisColour, labelFont
    X = getXfromAngle(angle)
    canvas.create_text(X, graphLabelY, text=label, fill=statusMessageColour, font=labelFont)
    canvas.create_line(X, graphLineY, X, graphLineY + 5, fill=axisColour, width=2)

def drawYTickAndLabel(value, label):
    global canvas, graphLabelX, labelFont
    Y = getYFromValue(value)
    canvas.create_text(graphLabelX, Y, text=label, fill=statusMessageColour, font=labelFont)

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

def drawLegend():
    canvas.create_text(650, 400, text="Sensor A", fill=statusMessageColour, font=labelFont)
    canvas.create_line(700, 400, 750, 400, fill=sensorAColour, width=2)
    canvas.create_text(650, 420, text="Sensor B", fill=statusMessageColour, font=labelFont)
    canvas.create_line(700, 420, 750, 420, fill=sensorBColour, width=2)

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

def callback():
    print("click!")

def init():
    global canvas, root, statusTextID, positionTextID, labelFont
    root = Tk()

    fs = FullScreen(root)
    canvas = Canvas(fs, width=canvasWidth, height=canvasHeight, bg=canvasColour)
    canvas.grid(column=0, row=0, sticky=(N, W, E, S))

    b = Button(fs, text="OK", command=callback)
    b.pack()
    
    statusFont = font.Font(family="Helvetica", size=18, weight="bold")
    positionFont = font.Font(family="Helvetica", size=36, weight="bold")
    labelFont = font.Font(family="Helvetica", size=12, weight="bold")

    statusTextID = canvas.create_text(5, 5, anchor="nw", fill=statusMessageColour, font=statusFont)
    positionTextID = canvas.create_text(5, 390, anchor="nw", fill=statusMessageColour, font=positionFont)

def loop():
    global root
    root.mainloop()

init()
drawGraphAxis()
drawLegend()
