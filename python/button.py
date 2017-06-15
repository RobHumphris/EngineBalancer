import pygame

class Button():
    def __init__(self, screen, txt, location, action, bg=(0x88, 0x88, 0x88), fg=(0xFF, 0xFF, 0xFF), size=(80, 30), font_name="Segoe Print", font_size=16):
        self.color = bg
        self.bg = bg
        self.fg = fg
        self.size = size
        self.font = pygame.font.SysFont(font_name, font_size)
        self.screen = screen
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)
        self.call_back_ = action

    def draw(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        self.screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = (200, 200, 200)

    def call_back(self):
        self.call_back_()

