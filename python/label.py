import pygame

class Label():
    def __init__(self, screen, surface, rect, x, y, text_colour, back_colour, font):
        self.screen = screen
        self.surface = surface
        self.pos = (x, y)
        self.text = ""
        self.text_colour = text_colour
        self.back_colour = back_colour
        self.font = font
        self.rect = rect
    
    def render(self, text):   
        if (self.text != ""):
            old = self.font.render(self.text, 0, self.back_colour)
            self.surface.blit(old, self.pos)
        label = self.font.render(text, 0, self.text_colour)
        self.surface.blit(label, self.pos)
        self.screen.blit(self.surface, self.rect)
        self.text = text