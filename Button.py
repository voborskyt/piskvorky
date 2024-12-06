import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, click_handler, font_size=32):
        super().__init__()

        # Vytvoření obrázku tlačítka
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pressed = False

        # Nastavení textu
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.click_handler = click_handler

        # Barvy pro různé stavy
        self.color_normal = (100, 100, 100)
        self.color_hover = (130, 130, 130)
        self.color_current = self.color_normal

        self._draw()

    def _draw(self):
        # Vykreslení tlačítka
        self.image.fill(self.color_current)

        # Vykreslení textu na střed tlačítka
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)

    def update(self):
        # Detekce najetí myší
        mouse_pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(mouse_pos)
        current_pressed = pygame.mouse.get_pressed()[0]

        if mouse_over:
            if current_pressed:
                self.pressed = True
            elif self.pressed:  # tlačítko bylo puštěno
                self.pressed = False
                self.click_handler.click()
