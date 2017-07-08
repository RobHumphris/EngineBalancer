import pygame
import settings as cfg

class GraphWindow():
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.surface.Surface((cfg.WIDTH, cfg.HEIGHT))
        self.rect = self.surface.get_rect(center=(cfg.WIDTH/2, cfg.HEIGHT/2))
        self.status_font = pygame.font.SysFont(cfg.FONT_NAME, 18, "bold")
        self.position_font = pygame.font.SysFont(cfg.FONT_NAME, 36, "bold")
        self.label_font = pygame.font.SysFont(cfg.FONT_NAME, 12, "bold")

    def getXFromAngle(self, angle):
        return (angle * cfg.XSCALAR) + cfg.STARTX

    def getYFromValue(self, value):
        retval = cfg.AXISHEIGHT / 2
        if value > 0:
            retval = retval - (value * 2)
        elif value < 0:
            retval = retval + (0 - value * 2)
        return retval + cfg.STARTY

    def create_text(self, x, y, text, colour, font):
        label = font.render(text, 1, colour)
        self.surface.blit(label, (x, y))
        #labelpos = label.get_rect()
        #labelpos.topleft = (x, y)
        #self.screen.blit(label, labelpos)

    def drawXTickAndLabel(self, angle, label):
        x = self.getXFromAngle(angle)
        pygame.draw.aaline(self.surface, cfg.AXISCOLOUR, [x, cfg.GRAPHLINEY-5], [x, cfg.GRAPHLINEY+5], 2)
        self.create_text(x, cfg.GRAPHLABLEY, label, cfg.STATUSCOLOUR, self.label_font)

    def drawYTickAndLabel(self, value, label):
        y = self.getYFromValue(value)
        pygame.draw.aaline(self.surface, cfg.AXISCOLOUR, [cfg.GRAPHLINEX-5, y], [cfg.GRAPHLINEX+5, y], 2)
        self.create_text(cfg.GRAPHLABLEX, y, label, cfg.STATUSCOLOUR, self.label_font)

    def drawGraphAxis(self):
        pygame.draw.aaline(self.surface, cfg.AXISCOLOUR, [cfg.STARTX, cfg.GRAPHLINEY], [cfg.AXISLENGTH + cfg.STARTX, cfg.GRAPHLINEY], 2)
        pygame.draw.aaline(self.surface, cfg.AXISCOLOUR, [cfg.GRAPHLINEX, cfg.STARTY], [cfg.GRAPHLINEX, cfg.AXISHEIGHT + cfg.STARTY], 2)
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
        self.create_text(650, 400, "Sensor A", cfg.STATUSCOLOUR, self.label_font)
        pygame.draw.aaline(self.surface, cfg.SENSORACOLOUR, [720, 406], [770, 406], 2)
        self.create_text(650, 420, "Sensor B", cfg.STATUSCOLOUR, self.label_font)
        pygame.draw.aaline(self.surface, cfg.SENSORBCOLOUR, [720, 427], [770, 427], 2)

    def statusMessage(self, message):
        self.create_text(5, 5, "Status: " + message, cfg.STATUSCOLOUR, self.status_font)

    def positionMessage(self, message):
        self.create_text(5, 390, message, cfg.POSITIONCOLOUR, self.position_font)

    def plotReading(self, angle, value, colour):
        x = self.getXFromAngle(angle)
        y = self.getYFromValue(value)
        pygame.draw.aaline(self.surface, colour, [x, y], [x+2, y], 2)

    def draw(self):
        self.drawGraphAxis()
        self.drawLegend()
        self.screen.blit(self.surface, self.rect)