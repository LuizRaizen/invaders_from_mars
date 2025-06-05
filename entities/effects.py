# -*- coding: UTF-8 -*-
""" Um módulo para armazenar efeitos do jogo.

"""
import pygame

from utils.settings import Settings
from utils.audio_manager import audio_manager


class ScoreUpEffect:
    """Classe para criar uma exibição de pontuação"""
    
    def __init__(self, game, x, y):
        self.game = game
        self.config = Settings()
        # Configurações da pontuação
        self.font = pygame.font.Font(*self.config.SCOREUP['font'])
        self.text = self.font.render("+" + str(self.config.ALIEN['points']),
                                       True, self.config.SCOREUP['color'])
        self.rect = self.text.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        """Atualiza a animação dos pontos"""
        if self.text.get_alpha() == 0:
            self.game.scoreups.remove(self)
        self.rect.y -= int(self.config.SCOREUP['speed'])
        self.text.set_alpha(self.text.get_alpha() - 15)
    
    def render(self, screen):
        """Exibe a animação na tela """
        screen.blit(self.text, self.rect)
        
        
class AlienExplosionEffect:
    """Uma explosão ao destruir um alienigena"""
    
    def __init__(self, game, x, y):
        self.game = game
        # Configurações da explosão
        self.explosion_color = (200, 200, 60)
        self.image = pygame.Surface((60, 60)) 
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alpha = 255
        self.explosion_rect = (0, 0, 60, 60)
        audio_manager.play_sound("explosion") # Executa o som da explosão
        
    def update(self):
        """Atualiza a animação da explosão"""
        if self.alpha <= 0 :
            self.game.explosions.remove(self) # Remove o disparo da lista de tiros
        self.alpha -= 60
        self.image.set_alpha(self.alpha)
        
    def render(self, screen):
        """Rebderiza a explosão"""
        pygame.draw.ellipse(self.image, self.explosion_color,
                            self.explosion_rect)
        
        screen.blit(self.image, self.rect)


class FlashScreenEffect:
    """Efeito de explosão piscando entre branco e preto antes da tela de Game Over."""

    def __init__(self, window, duration=1.0, flash_speed=0.1):
        """
        :param window: Janela do jogo.
        :param duration: Duração total do efeito de piscar (em segundos).
        :param flash_speed: Velocidade do piscar (intervalo entre mudanças de cor).
        """
        self.window = window
        self.duration = duration
        self.flash_speed = flash_speed
        self.elapsed_time = 0
        self.flash_state = False  # Alterna entre branco e preto
        self.finished = False  # Indica se a explosão terminou

    def update(self, dt):
        """Atualiza o efeito de explosão, alternando entre branco e preto."""
        if self.finished:
            return

        self.elapsed_time += dt

        # Alterna entre branco e preto em intervalos de flash_speed
        if int(self.elapsed_time / self.flash_speed) % 2 == 0:
            self.flash_state = True  # Branco
        else:
            self.flash_state = False  # Preto

        # Se a duração total foi atingida, marca como finalizado
        if self.elapsed_time >= self.duration:
            self.finished = True

    def draw(self):
        """Desenha o efeito de explosão na tela."""
        if not self.finished:
            color = (255, 255, 255) if self.flash_state else (0, 0, 0)
            self.window.fill(color)  # Preenche a tela com branco ou preto


class PowerUpEffect:
    """Efeito visual ao coletar um power-up, incluindo círculo de energia e flash da nave"""

    def __init__(self, game, ship):
        self.game = game
        self.ship = ship
        self.active = False  # Define se o efeito está ativo
        self.start_time = 0

        # Círculo de energia (inicialmente invisível)
        self.circle_alpha = 0
        self.circle_radius = max(1, ship.rect.width * 2)  # Garante que não seja zero
        self.circle_shrink_speed = 3  # Velocidade de redução inicial

        # Flash da nave
        self.flash_alpha = 0
        self.flash_image = pygame.image.load("graphics/sprites/ships/ship_white.png").convert_alpha()
        self.flash_image = pygame.transform.scale(self.flash_image, ship.image.get_size())

    def activate(self):
        """Ativa o efeito ao coletar um power-up"""
        self.active = True
        self.start_time = pygame.time.get_ticks()
        
        # Executa o som do power-up
        audio_manager.play_sound('power_up')
        
        # Reinicia os valores para evitar aceleração infinita
        self.circle_alpha = 0  # Começa invisível
        self.circle_radius = self.ship.rect.width * 2  # Começa grande
        self.circle_shrink_speed = 3  # Reinicia a velocidade de redução
        self.flash_alpha = 0  # Flash inicial invisível

    def update(self):
        """Atualiza o efeito visual do power-up"""
        if not self.active:
            return

        elapsed_time = pygame.time.get_ticks() - self.start_time

        # Crescimento do brilho do círculo e redução progressiva do tamanho
        if elapsed_time < 300:  # Primeira fase (crescimento da opacidade)
            self.circle_alpha = min(255, self.circle_alpha + 15)
            self.circle_radius = max(1, self.circle_radius - self.circle_shrink_speed)  # Evita valores negativos
            self.circle_shrink_speed *= 1.1  # Aumenta a velocidade de redução

        elif elapsed_time < 500:  # Segunda fase (redução de opacidade)
            self.circle_alpha = max(0, self.circle_alpha - 20)
            self.circle_radius = max(1, self.circle_radius - self.circle_shrink_speed)  # Evita valores negativos

        # Flash da nave: aumento da opacidade
        if elapsed_time < 400:
            self.flash_alpha = min(255, self.flash_alpha + 20)
        elif elapsed_time > 500:
            self.flash_alpha = max(0, self.flash_alpha - 30)

        # Quando o efeito termina, libera o jogo
        if elapsed_time > 700:
            self.active = False
            self.game.powerup_freeze = False  # Libera o jogo para continuar normalmente

    def render(self, screen):
        """Renderiza o efeito visual"""
        if not self.active:
            return

        # Renderizar círculo de energia
        if self.circle_alpha > 0 and self.circle_radius > 1:
            circle_surface = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (255, 255, 255, int(self.circle_alpha)), 
                               (self.circle_radius, self.circle_radius), self.circle_radius)
            screen.blit(circle_surface, (self.ship.rect.centerx - self.circle_radius, 
                                         self.ship.rect.centery - self.circle_radius))

        # Renderizar flash da nave
        if self.flash_alpha > 0:
            self.flash_image.set_alpha(self.flash_alpha)
            screen.blit(self.flash_image, self.ship.rect)


class AlienSpawnEffect:
    """Efeito visual para o surgimento dos alienígenas (teleporte dimensional)."""

    def __init__(self, alien):
        self.alien = alien
        self.active = True
        self.start_time = pygame.time.get_ticks()

        # Carrega e redimensiona a sprite branca do alien
        self.original_white = pygame.image.load("graphics/sprites/aliens/alien_1_flash.png").convert_alpha()
        self.original_white = pygame.transform.scale(self.original_white, alien.image.get_size())
        self.white_image = self.original_white.copy()

        # Fase 1: fade-in + escala crescente
        self.alpha = 0
        self.scale_factor = 0.2  # Começa pequeno
        self.finished = False

        # Círculo de energia
        self.circle_alpha = 255
        self.circle_radius = 1
        self.circle_max_radius = alien.rect.width * 1.5
        self.circle_growth_speed = 2

    def update(self):
        """Atualiza o efeito de surgimento."""
        if not self.active:
            return

        elapsed = pygame.time.get_ticks() - self.start_time

        if elapsed < 400:
            # Fase 1: Fade-in e crescimento
            self.alpha = min(255, self.alpha + 10)
            self.scale_factor = min(1.0, self.scale_factor + 0.05)
            scaled_size = (
                int(self.alien.image.get_width() * self.scale_factor),
                int(self.alien.image.get_height() * self.scale_factor),
            )
            self.white_image = pygame.transform.scale(self.original_white, scaled_size)
            self.white_image.set_alpha(self.alpha)

        elif elapsed < 700:
            # Fase 2: Fade-out da imagem branca e início do círculo
            self.alpha = max(0, self.alpha - 15)
            self.white_image.set_alpha(self.alpha)
            if not self.finished:
                self.alien.image.set_alpha(255)
                self.finished = True

            self.circle_radius += self.circle_growth_speed
            self.circle_alpha = max(0, self.circle_alpha - 10)

        else:
            self.active = False  # Fim do efeito

    def render(self, screen):
        """Renderiza o efeito de surgimento."""
        if not self.active:
            return

        # Desenha a imagem branca em fade-in
        if self.alpha > 0:
            white_rect = self.white_image.get_rect(center=self.alien.rect.center)
            screen.blit(self.white_image, white_rect)

        # Desenha o círculo de energia
        if self.circle_alpha > 0 and self.circle_radius > 0:
            circle_surface = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (255, 255, 255, int(self.circle_alpha)),
                               (self.circle_radius, self.circle_radius), self.circle_radius)
            screen.blit(circle_surface, (self.alien.rect.centerx - self.circle_radius,
                                         self.alien.rect.centery - self.circle_radius))


class SpeedTrailEffect:
    """Rastros da nave quando o power-up de velocidade está ativo"""

    def __init__(self, game, x, y):
        self.game = game
        self.config = Settings()
        self.image = pygame.image.load(self.config.SHIP['image']).convert_alpha()
        self.size = self.image.get_width() // 3, self.image.get_height() // 3 # Obtém a resolução proporcional
        self.image = pygame.transform.scale(self.image, self.size) # Redimensiona a imagem

        # Criar um efeito de coloração azulada na imagem
        self.image = self.image.copy()
        for px in range(self.image.get_width()):
            for py in range(self.image.get_height()):
                color = self.image.get_at((px, py))
                self.image.set_at((px, py), (color.r // 2, color.g // 2, 255, color.a))

        self.rect = self.image.get_rect(center=(x, y))
        self.alpha = 200  # Transparência inicial

    def update(self):
        """Reduz a opacidade gradualmente até desaparecer"""
        self.alpha -= 10  # Reduz a opacidade de maneira suave
        if self.alpha <= 0:
            self.game.speed_trails.remove(self)  # Remove da lista quando invisível
        else:
            self.image.set_alpha(self.alpha)  # Aplica a opacidade na sprite

    def render(self, screen):
        """Desenha o rastro na tela"""
        screen.blit(self.image, self.rect)


class DoubleShootEffect:
    """Efeito visual ao ativar e desativar o Double Shoot"""

    def __init__(self, game, ship):
        self.game = game
        self.ship = ship

        # Carregar as sprites da nave para o efeito de Double Shoot
        self.normal_image = pygame.image.load("graphics/sprites/ships/ship_1.png").convert_alpha()
        self.double_shoot_image = pygame.image.load("graphics/sprites/ships/ship_double_shoot.png").convert_alpha()
        self.white_flash_image = pygame.image.load("graphics/sprites/ships/ship_double_shoot_white.png").convert_alpha()

        # Ajustar tamanho das imagens
        size = self.normal_image.get_width() // 3, self.normal_image.get_height() // 3
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        self.double_shoot_image = pygame.transform.scale(self.double_shoot_image, size)
        self.white_flash_image = pygame.transform.scale(self.white_flash_image, size)

        # Estados de efeito
        self.active = False
        self.transitioning = False  # Se a nave está no efeito de fade-out para retornar ao normal
        self.alpha = 255  # Transparência da nave
        self.fade_speed = 15  # Velocidade da transição
        self.start_time = 0  # Tempo de ativação do efeito

    def activate(self):
        """Ativa o efeito de Double Shoot na nave"""
        self.active = True
        self.transitioning = False
        self.alpha = 255
        self.ship.image = self.double_shoot_image

    def deactivate(self):
        """Inicia a transição de fade-out para voltar à nave normal"""
        self.transitioning = True
        self.start_time = pygame.time.get_ticks()

    def update(self):
        """Atualiza a transição entre as sprites"""
        if self.transitioning:
            elapsed_time = pygame.time.get_ticks() - self.start_time

            if elapsed_time < 300:
                # Aplicar fade-out da sprite de double shoot
                self.alpha = max(0, self.alpha - self.fade_speed)
                self.double_shoot_image.set_alpha(self.alpha)
                self.ship.image = self.double_shoot_image
            elif elapsed_time < 600:
                # Aplicar fade-in da sprite branca
                self.alpha = min(255, self.alpha + self.fade_speed)
                self.white_flash_image.set_alpha(self.alpha)
                self.ship.image = self.white_flash_image
            else:
                # Retornar à sprite normal
                self.ship.image = self.normal_image
                self.active = False
                self.transitioning = False

    def render(self, screen):
        """Renderiza a nave com os efeitos ativos"""
        screen.blit(self.ship.image, self.ship.rect)


class ShieldEffect:
    """Efeito visual de escudo protetor ao redor da nave com pulsação."""

    def __init__(self, ship):
        self.ship = ship
        self.circles = []  # Cada círculo é um dicionário com {raio, opacidade}
        self.active = False

        self.spawn_interval = 250  # Tempo entre novos círculos (ms)
        self.last_spawn_time = pygame.time.get_ticks()

        # Parâmetros visuais
        self.color = (0, 255, 100)  # Verde brilhante
        self.initial_radius = 10
        self.max_radius = ship.rect.width * 1.2
        self.growth_speed = 1.5
        self.fade_speed = 2.5

    def activate(self):
        """Ativa o escudo."""
        self.active = True
        self.circles.clear()
        self.last_spawn_time = pygame.time.get_ticks()

    def deactivate(self):
        """Desativa o escudo."""
        self.active = False
        self.circles.clear()

    def update(self):
        """Atualiza os círculos do escudo."""
        if not self.active:
            return

        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.spawn_interval:
            # Cria novo círculo no centro da nave
            self.circles.append({
                "radius": self.initial_radius,
                "alpha": 100
            })
            self.last_spawn_time = now

        # Atualiza os círculos existentes
        for circle in self.circles:
            circle["radius"] += self.growth_speed
            circle["alpha"] -= self.fade_speed

        # Remove os círculos totalmente invisíveis
        self.circles = [c for c in self.circles if c["alpha"] > 0]

    def render(self, screen):
        """Renderiza o efeito de escudo."""
        if not self.active:
            return

        for circle in self.circles:
            radius = int(circle["radius"])
            alpha = int(circle["alpha"])
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, alpha), (radius, radius), radius)
            rect = surface.get_rect(center=self.ship.rect.center)
            screen.blit(surface, rect)
