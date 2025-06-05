import pygame
from pygame.sprite import Sprite
from utils.audio_manager import AudioManager

import pygame
from pygame.sprite import Sprite
from utils.audio_manager import audio_manager


class BaseButton(Sprite):
    """Botão visual com efeito hover, som e clique."""

    def __init__(self, pos, size, font, text, action):
        super().__init__()
        self.pos = pos
        self.width, self.height = size
        self.font = font
        self.text = text
        self.action = action  # Função ou lambda

        self.text_color = (255, 255, 255)
        self.default_color = (50, 50, 50)
        self.hover_color = self._lighter_color(self.default_color)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.pos

        self.text_render = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_render.get_rect(center=self.rect.center)

        self.hovered = False
        self.sound_hover = audio_manager.play_sound("button_hover")
        self.sound_click = audio_manager.play_sound("button_click")

    def _lighter_color(self, color):
        r, g, b = color
        return (min(r+30, 255), min(g+30, 255), min(b+30, 255))

    def update(self, mouse_pos):
        """Atualiza efeito hover baseado na posição do mouse."""
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                audio_manager.play_sound("button_hover")
            self.hovered = True
        else:
            self.hovered = False

    def handle_click(self):
        """Executa a ação ao clicar."""
        if self.hovered:
            audio_manager.play_sound("button_click")
            if self.action:
                self.action()

    def draw(self, screen):
        """Desenha o botão na tela."""
        color = self.hover_color if self.hovered else self.default_color
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        screen.blit(self.text_render, self.text_rect)


class MenuButton(BaseButton):
    """
    Botão visual moderno da tela de Menu com aparência translúcida.
    Comporta-se exatamente como BaseButton.
    """

    def __init__(self, pos, size, font, text, action):
        super().__init__(pos, size, font, text, action)

        # Personalização visual
        self.default_color = (20, 10, 40)  # Roxo acinzentado
        self.hover_color = self._lighter_color(self.default_color)

        # Surface com canal alfa
        self.button_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.alpha = 180  # Nível de transparência

    def draw(self, screen):
        """Desenha o botão com fundo translúcido moderno."""
        color = self.hover_color if self.hovered else self.default_color
        translucent_color = (*color, self.alpha)

        # Limpa a surface com transparência total
        self.button_surf.fill((0, 0, 0, 0))

        # Desenha botão arredondado com cor translúcida
        pygame.draw.rect(self.button_surf, translucent_color, (0, 0, self.width, self.height), border_radius=20)

        # Blit da surface translúcida e texto
        screen.blit(self.button_surf, self.rect)
        screen.blit(self.text_render, self.text_rect)
