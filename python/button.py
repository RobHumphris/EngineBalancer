# https://pythonprogramming.net/pygame-buttons-part-1-button-rectangle/
import pygame
import settings as cfg

#UNCLICKED = (0x2B, 0x4E, 0x72)
#CLICKED = (0x27, 0x90, 0xB0)
#FOREGROUND = (0xFF, 0xFF, 0xFF)
class Button():
    def __init__(self, screen, txt, location, action):
        self.color = cfg.BTN_UNCLICKED
        self.bg = self.color
        self.fg = cfg.BTN_FOREGROUND
        self.size = (80, 30)
        self.font = pygame.font.SysFont(cfg.FONT_NAME, 12, "bold")
        self.screen = screen
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])
        self.surface = pygame.surface.Surface(self.size)
        self.rect = self.surface.get_rect(center=location)
        self.call_back_ = action

    def draw(self):
        self.mouseover()
        self.unclicked()

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = (200, 200, 200)

    def clicked(self):
        self.surface.fill(cfg.BTN_CLICKED)
        self.surface.blit(self.txt_surf, self.txt_rect)
        self.screen.blit(self.surface, self.rect)

    def unclicked(self):
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        self.screen.blit(self.surface, self.rect)

    def call_back(self):
        self.clicked()
        self.call_back_()
        self.unclicked()