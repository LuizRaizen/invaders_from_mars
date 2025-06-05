import pygame

from utils.settings import Settings
from entities.effects import AlienSpawnEffect


class Alien:
    """Classe que representa um alienigena inimigo."""

    def __init__(self, game, x, y):
        self.game = game
        self.config = Settings()

        # carrega a imagem do alienigena
        self.image = pygame.image.load(self.config.ALIEN['image'])
        self.size = self.image.get_width() // 3, self.image.get_height() // 3 # Obtém a resolução proporcional
        self.image = pygame.transform.scale(self.image, self.size) # Redimensiona a imagem
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_x = x
        self.spawn_y = y
        self.rect.topleft = (self.spawn_x, self.spawn_y)
        self.image.set_alpha(0)  # Começa invisível

        self.spawn_effect = AlienSpawnEffect(self)

        # Configuraações de movimento
        self.speed_x = 1 # Velocidade horizontal

    def update(self):
        """Movimenta o alienigena lateralmente"""
        if self.spawn_effect.active:
            self.spawn_effect.update()
            self.rect.topleft = (self.spawn_x, self.spawn_y)  # Fixa a posição durante o efeito
            return

        # movimento normal do alien
        self.rect.x += self.speed_x * self.game.fleet_direction

    def render(self, screen):
        """Desenha o alienigena na tela"""
        if self.spawn_effect.active:
            self.spawn_effect.render(screen)
        else:
            screen.blit(self.image, self.rect)
            