#https://pythonprogramming.altervista.org/buttons-in-pygame/
import pygame
 
 
class Button:
    "Create a button, then blit the surface in the while loop"
 
    def __init__(self, text, font, x=0, y=0, bg="black"):
        self.x = y
        self.y = x
        self.font = font
        self.text = text
        self.is_clicked = True
 
        # init
        self.change_text(text, bg)

    def change_text(self, text, bg):
        text = self.font.render(text, 1, pygame.Color("White"))
        size = text.get_size()
        self.surface = pygame.Surface(size)
        self.surface.fill(bg)
        self.surface.blit(text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, size[0], size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def onClick(self, event):
        x, y = pygame.mouse.get_pos()
        #if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(x, y):
                if self.is_clicked:
                    self.change_text(self.text, "red")
                    self.is_clicked = False
                elif not self.is_clicked:
                    self.change_text(self.text, "navy")
                    self.is_clicked = True