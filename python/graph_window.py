import pygame

SCREEN = (0x4E, 0x4D, 0x4A)
AXISCOLOUR = (0x94, 0xBA, 0x65)
SENSORACOLOUR = (0xFF, 0x00, 0x00)
SENSORBCOLOUR = (0x00, 0x00, 0xFF)
STATUSCOLOUR = (0x27, 0x90, 0xB0)

WIDTH = 800
HEIGHT = 480
AXISLENGTH = 720
AXISHEIGHT = 400
STARTX = 40
STARTY = 25
GRAPHLINEX = (AXISLENGTH / 2) + STARTX
GRAPHLABLEX = GRAPHLINEX + 10
GRAPHLINEY = (AXISHEIGHT / 2) + STARTY
GRAPHLABLEY = GRAPHLINEY + 10
XSCALAR = AXISLENGTH / 360
YSCALAR = AXISHEIGHT / 200

class GraphWindow():
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.surface.Surface((WIDTH, HEIGHT))
        self.rect = self.surface.get_rect(center=(WIDTH/2,HEIGHT/2))
        self.status_font = pygame.font.SysFont("Helvetica", 18, "bold")
        self.position_font = pygame.font.SysFont("Helvetica", 36, "bold")
        self.label_font = pygame.font.SysFont("Helvetica", 12, "bold")

    def getXFromAngle(self, angle):
        return (angle * XSCALAR) + STARTX

    def getYFromValue(self, value):
        retval = AXISHEIGHT / 2
        if value > 0:
            retval = retval - (value * 2)
        elif value < 0:
            retval = retval + (0 - value * 2)
        return retval + STARTY

    def create_text(self, x, y, text, colour, font):
        label = font.render(text, 1, colour)
        self.surface.blit(label, (x, y))

    def drawXTickAndLabel(self, angle, label):
        x = self.getXFromAngle(angle)
        pygame.draw.aaline(self.surface, AXISCOLOUR, [x, GRAPHLINEY-5], [x, GRAPHLINEY+5], 2)
        self.create_text(x, GRAPHLABLEY, label, STATUSCOLOUR, self.label_font)

    def drawYTickAndLabel(self, value, label):
        y = self.getYFromValue(value)
        pygame.draw.aaline(self.surface, AXISCOLOUR, [GRAPHLINEX-5, y], [GRAPHLINEX+5, y], 2)
        self.create_text(GRAPHLABLEX, y, label, STATUSCOLOUR, self.label_font)

    def drawGraphAxis(self):
        pygame.draw.aaline(self.surface, AXISCOLOUR, [STARTX, GRAPHLINEY], [AXISLENGTH + STARTX, GRAPHLINEY], 2)
        pygame.draw.aaline(self.surface, AXISCOLOUR, [GRAPHLINEX, STARTY], [GRAPHLINEX, AXISHEIGHT + STARTY], 2)
        self.drawXTickAndLabel(0, "0")
        self.drawXTickAndLabel(90, "90")
        self.drawXTickAndLabel(180, "180")
        self.drawXTickAndLabel(270, "270")
        self.drawXTickAndLabel(359, "359")
        self.drawYTickAndLabel(100, "100")
        self.drawYTickAndLabel(50, "50")
        self.drawYTickAndLabel(-50, "-50")
        self.drawYTickAndLabel(-100, "-100")

    def drawLegend(self):
        self.create_text(650, 400, "Sensor A", STATUSCOLOUR, self.label_font)
        pygame.draw.aaline(self.surface, SENSORACOLOUR, [720, 406], [770, 406], 2)
        self.create_text(650, 420, "Sensor B", STATUSCOLOUR, self.label_font)
        pygame.draw.aaline(self.surface, SENSORBCOLOUR, [720, 427], [770, 427], 2)

    def statusMessage(self, message):
        self.create_text(5, 5, "Status: " + message, STATUSCOLOUR, self.status_font)

    def positionMessage(self, message):
        self.create_text(5, 390, message, STATUSCOLOUR, self.position_font)

    def plotReading(self, angle, value, colour):
        x = self.getXFromAngle(angle)
        y = self.getYFromValue(value)
        pygame.draw.aaline(self.surface, colour, [x, y], [x+2, y], 2)

    def draw(self):
        self.drawGraphAxis()
        self.drawLegend()
        self.screen.blit(self.surface, self.rect)