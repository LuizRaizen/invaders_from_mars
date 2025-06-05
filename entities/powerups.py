import pygame
import random

from utils.settings import Settings


class PowerUp:
    """Um Power Up para a nave do jogador"""

    def __init__(self, game, x, y, type):
        self.game = game
        self.config = Settings()
        self.type = type # Tipo do PowerUp (ex: 'speed', 'shield', 'double_shot')

        # Carrega a imagem do PowerUp que aparecerá na tela
        if self.type == 'double_shoot':
            self.image = pygame.image.load(self.config.DOUBLE_BULLET['image'])
        elif self.type == 'shield':
            self.image = pygame.image.load(self.config.SHIELD['image'])
        elif self.type == 'speed':
            self.image = pygame.image.load(self.config.SPEED['image'])
        
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = self.config.POWERUP['speed'] # Velocidade da queda do PowerUp

    def update(self):
        """Movimenta o PoweUp na tela"""
        self.rect.y += self.speed

        # Remove o power-up se sair da tela
        if self.rect.top > self.game.config.SCREEN['height']:
            self.game.powerups.remove(self)

    def render(self, screen):
        """Renderiza o PowerUp"""
        screen.blit(self.image, self.rect)
