import pygame
import settings as cfg
from label import Label

class GraphWindow():
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.surface.Surface((cfg.WIDTH, cfg.HEIGHT))
        self.rect = self.surface.get_rect(center=(cfg.WIDTH/2, cfg.HEIGHT/2))

        self.status = Label(screen, self.surface, self.rect, 5, 5, cfg.STATUSCOLOUR, cfg.SCREEN, pygame.font.SysFont(cfg.FONT_NAME, 18, "bold"))  
        self.position = Label(screen, self.surface, self.rect, 5, 390, cfg.POSITIONCOLOUR, cfg.SCREEN, pygame.font.SysFont(cfg.FONT_NAME, 36, "bold"))
        
        self.label_font = pygame.font.SysFont(cfg.FONT_NAME, 12, "bold")
        self.surface.fill(cfg.SCREEN)
        self.screen.blit(self.surface, self.rect)

    def getXFromAngle(self, angle):
        return (angle * cfg.XSCALAR) + cfg.STARTX

    def getPlotXFromAngle(self, angle):
        return (angle * cfg.PLOTXSCALAR) + cfg.STARTX

    def getYFromValue(self, value):
        gain = 1
        retval = cfg.AXISHEIGHT / 2
        if value > 0:
            retval = retval - (value * 2)
        elif value < 0:
            retval = retval + (0 - value * 2)
        return (retval * gain) + cfg.STARTY 

    def create_text(self, x, y, text, text_colour, back_colour, font):
        label = font.render(text, 1, text_colour, back_colour)
        self.surface.blit(label, (x, y))

    def drawXTickAndLabel(self, angle, label):
        x = self.getXFromAngle(angle)
        pygame.draw.aaline(self.surface, cfg.AXISCOLOUR, [x, cfg.GRAPHLINEY-5], [x, cfg.GRAPHLINEY+5], 2)
        self.create_text(x, cfg.GRAPHLABLEY, label, cfg.STATUSCOLOUR, cfg.SCREEN, self.label_font)

    def drawYTickAndLabel(self, value, label):
        y = self.getYFromValue(value)
        pygame.draw.aaline(self.surface, cfg.AXISCOLOUR, [cfg.GRAPHLINEX-5, y], [cfg.GRAPHLINEX+5, y], 2)
        self.create_text(cfg.GRAPHLABLEX, y, label, cfg.STATUSCOLOUR, cfg.SCREEN, self.label_font)

    def drawGraphAxis(self):
        pygame.draw.aaline(self.surface, cfg.AXISCOLOUR, [cfg.STARTX, cfg.GRAPHLINEY], [cfg.AXISLENGTH + cfg.STARTX, cfg.GRAPHLINEY], 2)
        pygame.draw.aaline(self.surface, cfg.AXISCOLOUR, [cfg.GRAPHLINEX, cfg.STARTY], [cfg.GRAPHLINEX, cfg.AXISHEIGHT + cfg.STARTY], 2)

        for x in [0, 90, 180, 270, 359]:
            self.drawXTickAndLabel(x, str(x))

        for y in [100, 50, -50, -100]:
            self.drawYTickAndLabel(y, str(y))

    def drawLegend(self):
        self.create_text(650, 400, "Sensor A", cfg.STATUSCOLOUR, cfg.SCREEN, self.label_font)
        pygame.draw.aaline(self.surface, cfg.SENSORACOLOUR, [720, 406], [770, 406], 2)
        self.create_text(650, 420, "Sensor B", cfg.STATUSCOLOUR, cfg.SCREEN, self.label_font)
        pygame.draw.aaline(self.surface, cfg.SENSORBCOLOUR, [720, 427], [770, 427], 2)

    def statusMessage(self, message):
        self.status.render("Status: " + message)

    def positionMessage(self, position):
        self.position.render("Angle: " + position + "°")
        
    def plotReading(self, angle, v1, v2, colour):
        start = [self.getPlotXFromAngle(angle), self.getYFromValue(v1)]
        end = [self.getPlotXFromAngle(angle+1), self.getYFromValue(v2)]
        pygame.draw.aaline(self.surface, colour, start, end, 2)

    def plotMaximum(self, max):
        x = int(self.getPlotXFromAngle(max[1]))
        y = int(self.getYFromValue(max[0]))
        pygame.draw.circle(self.surface, (255, 255, 255), (x, y), 5, 1)
        self.screen.blit(self.surface, self.rect)

    def draw(self):
        self.drawGraphAxis()
        self.drawLegend()
        self.status.refresh()
        self.position.refresh()
        self.screen.blit(self.surface, self.rect)

    def clear(self):
        self.surface.fill(cfg.SCREEN)
