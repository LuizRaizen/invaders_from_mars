import itertools
import pygame

from utils.settings import Settings
from utils.audio_manager import audio_manager
from entities.bullets import ShipBullet, DoubleBullet
from entities.effects import SpeedTrailEffect, PowerUpEffect, DoubleShootEffect, ShieldEffect


class Ship:
    """Classe que representa a nave do jogador"""

    def __init__(self, game, xpos=False):
        self.game = game
        self.config = Settings()

        # Carrega sprites da nave
        self.image = pygame.image.load("graphics/sprites/ships/ship_1.png").convert_alpha()
        # Ajusta o tamanho da imagem
        self.size = self.image.get_width() // 3, self.image.get_height() // 3
        self.image = pygame.transform.scale(self.image, self.size)
        # Define a imagem inicial da nave
        self.image = self.image

        # Obtém a posição da nave
        self.rect = self.image.get_rect()
        if xpos:
            self.rect.midbottom = (xpos, self.config.SCREEN['height'] - 20)
        else:
            self.rect.midbottom = (self.config.SCREEN['width'] // 2, self.config.SCREEN['height'] - 20)

        # Cria o efeito de power-up
        self.powerup_effect = PowerUpEffect(game, self)

        # Definições do power-up de velocidade
        self.base_speed = self.config.SHIP['speed']  # Velocidade normal
        self.speed = self.base_speed
        self.max_speed = 12  # Limite de velocidade máxima
        self.acceleration = 0.2  # Taxa normal de aceleração ao segurar a tecla
        self.speed_boost_active = False
        self.velocity = 0 # Velocidade incial
        self.trail_timer = 0 # Controla o tempo entre a criação de rastros

        # Definições do powerup de escudo
        self.shield_effect = ShieldEffect(self)
        self.shield_active = False

        # Flags de movimento da nave
        self.moving_left = False
        self.moving_right = False

    def shoot(self):
        """Dispara tiros, considerando se o power-up está ativo."""
        if len(self.game.bullets) < self.config.SHIP_BULLET['allowed']:
            bullet = ShipBullet(self.game, self.rect.centerx, self.rect.top)
            self.game.bullets.append(bullet)
            audio_manager.play_sound('shoot')
            
    def activate_shield(self):
        """Ativa o power-up de escudo."""
        self.shield_active = True
        self.shield_effect.activate()

    def deactivate_shield(self):
        """Desativa o power-up de escudo."""
        self.shield_active = False
        self.shield_effect.deactivate()

    def activate_double_shoot(self):
        """Ativa o power-up de tiro duplo."""
        xpos = self.game.ship.rect.centerx
        self.game.ship = DoubleShootShip(self.game, xpos)

    def deactivate_double_shoot(self):
        """Desativa o power-up de tiro duplo."""
        xpos = self.game.ship.rect.centerx
        self.game.ship = Ship(self.game, xpos)

    def handle_input(self, keys, events):
        """Gerencia a movimentação e o disparo"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity = max(self.velocity - .5, -self.speed) # Limita a velocidade
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity = min(self.velocity + .5, self.speed)
        else:
            self.velocity *= .9 # Redução gradual da velocidade

        # Disparo com espaço (evita tiros continuos)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.shoot()

    def update(self):
        """Atualiza a posição da nave"""
        keys = pygame.key.get_pressed()

        if self.speed_boost_active:
            # Criar rastro apenas a cada 50ms para evitar sobrecarga visual
            if pygame.time.get_ticks() - self.trail_timer > 50:
                self.game.speed_trails.append(SpeedTrailEffect(self.game, self.rect.centerx, self.rect.centery))
                self.trail_timer = pygame.time.get_ticks()
                
        # Se o power-up de velocidade estiver ativo, a nave responde mais rápido
        if self.speed_boost_active and self.speed < self.max_speed:
            self.speed += self.acceleration  # Aumenta gradualmente até o limite

        elif not self.speed_boost_active and self.speed > self.base_speed:
            self.speed -= self.acceleration  # Reduz gradualmente até voltar ao normal

        # Movimentação normal da nave
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.game.config.SCREEN['width']:
            self.rect.x += self.speed

        # Atualiza o efeito do power-up de escudo
        if self.shield_active:
            self.shield_effect.update()

        # Atualiza o efeito de power-up
        self.powerup_effect.update()

    def render(self, screen):
        """Renderiza a nave e seus efeitos na tela."""
        # Renderiza a imagem da nave
        screen.blit(self.image, self.rect)
        # Renderiza o efeito de power-up
        self.powerup_effect.render(screen)
        # Renderiza o efeito do power-up de escudo
        if self.shield_active:
            self.shield_effect.render(screen)


class DoubleShootShip(Ship):
    """Classe que representa a nave com o powerup de tiro duplo."""

    def __init__(self, game, xpos=False):
        super().__init__(game)  # Chama o construtor da classe pai (Ship)

        # Aqui você pode modificar os atributos para diferenciar a nave
        self.image = pygame.image.load("graphics/sprites/ships/ship_2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()

        # Obtém a posição da nave
        if xpos:
            self.rect.midbottom = (xpos, self.config.SCREEN['height'] - 20)
        else:
            self.rect.midbottom = (self.config.SCREEN['width'] // 2, self.config.SCREEN['height'] - 20)

    def shoot(self):
        """Dispara tiros, considerando se o power-up está ativo."""
        if len(self.game.bullets) < self.config.DOUBLE_BULLET['allowed']:
            # Criar dois projéteis, um à esquerda e outro à direita da nave
            left_xy = self.game.ship.rect.centerx - 18, self.game.ship.rect.centery # Posição do disparo esquerdo
            right_xy = self.game.ship.rect.centerx + 18, self.game.ship.rect.centery # Posição do disparo direito
            bullets = DoubleBullet(self.game, left_xy, right_xy, self.config.DOUBLE_BULLET['color'])
            self.game.bullets.append(bullets.left_bullet)
            self.game.bullets.append(bullets.right_bullet)
            audio_manager.play_sound('shoot')
