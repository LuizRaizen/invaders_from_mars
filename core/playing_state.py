import pygame
import random
import time

from core.game_over_state import GameOverState
from utils.settings import Settings
from utils.audio_manager import audio_manager
from utils.hud import Score, Lives, Level, PowerUpTimer
from utils.transitions import NextLevelTransition
from entities.background import GameBackground
from entities.ships import Ship
from entities.enemies import Alien
from entities.powerups import PowerUp
from entities.effects import AlienExplosionEffect, ScoreUpEffect


class PlayingState:
    """Estado onde o jogo acontece"""

    def __init__(self, game):
        self.game = game
        self.config = Settings()

        self.game.background = GameBackground(self.game)  # Adiciona o fundo animado
        
        self.game.ship = Ship(self.game) # Cria a nave do jogador
        self.game.speed_trails = [] # Lista de rastros do power-up de velocidade
        self.game.bullets = [] # Cria a lista de tiros

        # Listas para armazenar objetos referentes aos inimigos
        self.game.aliens = [] # Cria a lista de alienigenas
        self.game.explosions = [] # Cria a lista para armazenar as explosões
        self.game.scoreups = [] # Cria a lista para armazenar os scoreup

        # Define a direção inicial da frota de inimigos
        self.game.fleet_direction = 1 # 1 para a direita, -1 para a esquerda

        # Definições dos powerups
        self.game.powerups = [] # Lista de power-ups
        self.powerup_timer = PowerUpTimer(self.game, 425) # Inicializa o temporizador dos power-ups

        # Definições da HUD
        self.hud_bg = pygame.Surface((self.config.SCREEN['width'], 45)) # Cria o fundo da HUD
        self.hud_bg.set_alpha(160) # Define a opacidade da HUD
        self.score = Score(self.game) # Incializa o sistema de pontuação
        self.lives = Lives(self.game) # Incializa o sistema de vidas
        self.level = Level(self.game) # Define o nível inicial

        self.game.playing_state = self  # Permite acesso pelo alien
        self.level_transition = None

        self.create_fleet() # Cria a frota de alienigenas inicial
        audio_manager.play_music('gameplay_bg') # Executa a música de gameplay

    def create_fleet(self):
        """Cria uma grade de alienigenas na tela"""
        cols = 6 # Quantidade de alienigenas por linha
        rows = 4 # Quantidade de linhas
        
        # Criamos um alienígena temporário para obter sua largura e altura
        temp_alien = Alien(self.game, 0, 0)
        alien_width = temp_alien.rect.width
        alien_height = temp_alien.rect.height

        spacing_x = alien_width + 20  # Espaçamento horizontal (20 pixels entre aliens)
        spacing_y = alien_height + 20  # Espaçamento vertical (20 pixels entre linhas)

        for row in range(rows):
            for col in range(cols):
                x = 100 + col * spacing_x  # Calcula a posição horizontal com espaçamento
                y = 50 + row * spacing_y  # Calcula a posição vertical com espaçamento
                alien = Alien(self.game, x, y)
                # Aumenta a velocidade a cada nível
                alien.speed_x += (self.level.lvl - 1) * self.config.ALIEN['speedup_scale']
                self.game.aliens.append(alien)

    def check_fleet_edges(self):
        """Verifica se algum alienigena atingiu a borda"""
        for alien in self.game.aliens:
            if alien.rect.right >= self.config.SCREEN['width'] or alien.rect.left <= 0:
                self.drop_fleet()
                break # Todos os alienigenas já desceram

    def drop_fleet(self):
        """Faz todos os alienigenas descerem e inverte a direção"""
        for alien in self.game.aliens:
            alien.rect.y += 20 # Todos descem 20 pixels
        self.game.fleet_direction *= -1 # Inverte o movimento da frota

    def check_collisions(self):
        """Verifica as colisões entre tiros e alienigenas"""
        # iteramos sobre cópias das listas
        for bullet in self.game.bullets[:]:
            for alien in self.game.aliens[:]:
                if bullet.rect.colliderect(alien.rect): # Se houver colisão
                    self.game.bullets.remove(bullet)
                    self.game.aliens.remove(alien)
                    self.game.explosions.append(AlienExplosionEffect(self.game, alien.rect.centerx, alien.rect.centery))
                    self.game.scoreups.append(ScoreUpEffect(self.game, alien.rect.centerx, alien.rect.centery))
                    self.score.add_points(self.config.ALIEN['points']) # Ganha pontos por cada alienigena destruido
                    # Chance de soltar um power-up (5%)
                    if random.randint(1, 100) <= 5:
                        powerup_type = random.choice(["speed", "shield", "double_shoot"])
                        self.game.powerups.append(PowerUp(self.game, alien.rect.centerx, alien.rect.centery, powerup_type))
                    break # O tiro só atinge uma alienigena por vez
    
    def check_powerup_collisions(self):
        """Verifica se a nave coletou um power-up"""
        for powerup in self.game.powerups[:]:
            if self.game.ship.rect.colliderect(powerup.rect):
                # Ativa a paralisação temporária por 500ms (0,5 segundos)
                self.game.powerup_freeze = True
                # Salva o power-up que será ativado após a paralisação
                self.game.active_powerup = powerup
                # Ativa a animação do power-up
                self.game.ship.powerup_effect.activate()
                # Remove o power-up da tela
                self.game.powerups.remove(powerup)
    
    def check_next_level(self):
        """Verifica se o jogador passou para o próximo nível"""
        # Se todos os alienigenas forem destruídos, o jogador sobe de nível
        if len(self.game.aliens) == 0:
            self.game.bullets = []
            self.game.powerups = []
            self.level.lvl += 1  # Aumenta o nível
            self.level.update_level(self.level.lvl) # Atualiza a exibição do nível
            self.level_transition = NextLevelTransition(self.game, f"Level {self.level.lvl}")
            self.game.alien_direction = 1  # Reseta a direção dos aliens
            self.create_fleet()  # Cria uma nova frota mais difícil

    def check_game_over(self):
        """Verifica se o jogo terminou"""
        for alien in self.game.aliens:
            if alien.rect.bottom >= self.game.ship.rect.top:
                if self.lives.lives == 0: # Se o jogador estiver sem vidas
                    # Se um alienigena tocar a nave, o jogador perde
                    audio_manager.stop_music() # Interrompe a música de fundo
                    audio_manager.play_sound('game_over') # Executa o som de fim de jogo
                    self.game.state_manager.set_state(GameOverState(self.game))
                    break # Evita múltiplos ocasionamentos
                elif self.lives.lives > 0: # Reinicia o nível e diminui uma vida do jogador
                    self.lives.lives -= 1
                    self.game.aliens = []
                    self.game.alien_direction = 1  # Reseta a direção dos aliens
                    self.create_fleet()  # Cria uma nova frota mais difícil
                    self.level_transition = True
                    self.level_transition = NextLevelTransition(self.game, f"Wave {self.level.lvl}")
                    break # Evita múltiplos ocasionamentos

    def handle_events(self):
        """Captura movimentos do usúario movimentação e ações"""
        events = pygame.event.get() # Obtém a lista de eventos
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Tecla "P" para pausar o jogo
                    self.game.toggle_pause()

            elif event.type == pygame.USEREVENT + 1:  # Evento disparado após a paralisação do power-up
                self.game.powerup_manager.activate_powerup(self.game.active_powerup.type)  # Agora ativa o efeito
                self.game.active_powerup = None

        # Se o jogo não está pausado, processa os inputs da nave normalmente
        if not self.game.paused:
            keys = pygame.key.get_pressed()
            self.game.ship.handle_input(keys, events)

    def update(self):
        """Atualiza a lógica do jogo"""
        self.game.update_powerup_freeze()

        if self.game.paused:
            return  # Não faz nada se o jogo estiver pausado manualmente

        if self.game.powerup_freeze:
            # Permite que apenas a animação do power-up rode durante a paralisação
            self.game.ship.powerup_effect.update()
            return  

        # Atualiza normalmente caso o jogo não esteja paralisado
        self.game.background.update()

        for powerup in self.game.powerups[:]:
            powerup.update()
            
        self.game.ship.update()

        for trail in self.game.speed_trails[:]:
            trail.update()

        for bullet in self.game.bullets[:]:
            bullet.update()

        for alien in self.game.aliens[:]:
            alien.update()

        for explosion in self.game.explosions[:]:
            explosion.update()

        for scoreup in self.game.scoreups[:]:
            scoreup.update()

        self.game.powerup_manager.update()

        self.check_fleet_edges()
        self.check_collisions()
        self.check_powerup_collisions()
        self.check_next_level()
        self.check_game_over()

        # Atualiza a transição de nível se a flag estiver ativa
        if self.level_transition:
            self.level_transition.update()
            if self.level_transition.finished:
                self.level_transition = None  # Remove a referência
            else:
                return  # Evita atualizar o jogo enquanto a transição ocorre

    def render(self, screen):
        """Renderiza os elementos do jogo"""
        self.game.background.render(screen)  # Renderiza o fundo antes de tudo

        # Renderiza os rastros da nave primeiro (para ficarem abaixo da nave)
        for trail in self.game.speed_trails:
            trail.render(screen)

        # Renderiza a nave do jogador na tela
        self.game.ship.render(screen)

        # Renderiza todos os tiros
        for bullet in self.game.bullets:
            bullet.render(screen)

        # Renderiza todos os alienigenas
        for alien in self.game.aliens:
            alien.render(screen)

        # Renderiza as explosões
        for explosion in self.game.explosions:
            explosion.render(screen)

        # Renderiza os power-ups
        for powerup in self.game.powerups:
            powerup.render(screen)

        # Renderiza o scoreup
        for scoreup in self.game.scoreups:
            scoreup.render(screen)

        # Renderiza a transição de nível
        if self.level_transition:
            self.level_transition.render(screen)
        
        # Exibe o fundo da HUD
        screen.blit(self.hud_bg, (0, 0))
        # Exibe a pontuação na tela
        self.score.render(screen)
        # Exibe as vidas na tela
        self.lives.render(screen)
        # Exibe o nível na tela
        self.level.render(screen)
        # Exibe o temporizador do power-up
        self.powerup_timer.render(screen)

        # Se o jogo estiver pausado, exibe a mensagem de pausa
        if self.game.paused:
            pause_overlay = pygame.Surface((self.game.config.SCREEN['width'], self.game.config.SCREEN['height']), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 150))  # Fundo semi-transparente
            screen.blit(pause_overlay, (0, 0))

            font = pygame.font.Font("fonts/BITSUMIS.TTF", 60)
            text = font.render("PAUSADO", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.game.config.SCREEN['width'] // 2, self.game.config.SCREEN['height'] // 2))
            screen.blit(text, text_rect)
