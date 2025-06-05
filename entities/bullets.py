import pygame

from utils.settings import Settings


class ShipBullet:
    """Classe que representa os projéteis disparados pela nave."""

    def __init__(self, game, x, y, color=None):
        self.game = game
        self.config = Settings()

        self.image = pygame.Surface((5, 15)) # Criamos um retângulo como tiro

        # Define a cor dos projéteis
        if color:
            self.color = color
        else:
            self.color = self.config.SHIP_BULLET['color']

        self.image.fill(self.color) # Cor do projetil

        self.rect = self.image.get_rect(midbottom=(x, y)) # Posição inicial
        self.speed = 7 # Velocidade do tiro

    def update(self):
        """Move o tiro para cima"""
        self.rect.y -= self.speed

        # Se o tiro sair da tela, remove ele da lista
        if self.rect.bottom < 0:
            self.game.bullets.remove(self)

    def render(self, screen):
        """Desenha o tiro na tela"""
        pygame.draw.ellipse(screen, self.config.SHIP_BULLET['color'], self.rect)


class DoubleBullet:
    """Projéteis duplos disparados pela nave quando o power-up de Double Shoot está ativo."""

    def __init__(self, game, left_xy, right_xy, color=None):
        self.game = game
        self.config = Settings()

        # Define a cor dos projéteis
        if color:
            self.color = color
        else:
            self.color = self.config.DOUBLE_BULLET['color']

        self.left_bullet = ShipBullet(self.game, left_xy[0], left_xy[1], color=self.color)
        self.right_bullet = ShipBullet(self.game, right_xy[0], right_xy[1], color=self.color)

    def update(self):
        """Move os tiros duplos para cima."""
        self.left_bullet.update()
        self.right_bullet.update()

    def render(self, screen):
        """Desenha o tiro na tela."""
        self.left_bullet.render(screen)
        self.right_bullet.render(screen)
