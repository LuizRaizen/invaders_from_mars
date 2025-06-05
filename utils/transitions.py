import pygame

from utils.settings import Settings
from utils.audio_manager import audio_manager
from utils.animations import ImpactFadeAnimation, ExpandFadeAnimation


import pygame
from utils.settings import Settings
from utils.audio_manager import audio_manager


class NextLevelTransition:
    """Animação de transição visual ao subir de nível (ex: 'Wave X')."""

    def __init__(self, game, text="Onda 1"):
        self.game = game
        self.config = Settings()
        self.text = text
        self.font_path = "fonts/Android Assassin.ttf"
        self.opacity = 255

        # Tamanhos de animação
        self.size_init = 300
        self.size_transition = 90
        self.size_end = 60
        self.current_size = self.size_init

        # Velocidades da animação
        self.impact_speed = 0.3
        self.shrink_speed = 0.01
        self.fade_out_speed = 5

        # Controle de fases
        self.impact_done = False
        self.finished = False

        # Tempo de exibição
        self.font = pygame.font.Font(self.font_path, int(self.current_size))
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.game.screen.get_rect().center)

        # Toca som de nível
        audio_manager.play_sound("level_up")

    def update(self):
        """Atualiza o efeito de impacto e fade-out."""
        if self.finished:
            return

        # Fase 1: Redução rápida (impacto)
        if not self.impact_done:
            if self.current_size > self.size_transition:
                self.current_size -= max((self.current_size - self.size_transition) * self.impact_speed, 1)
            else:
                self.impact_done = True

        # Fase 2: Redução contínua + fade-out
        else:
            if self.current_size > self.size_end:
                self.current_size -= max((self.current_size - self.size_end) * self.shrink_speed, 0.5)
            else:
                self.opacity -= self.fade_out_speed
                if self.opacity <= 0:
                    self.finished = True
                    return

        # Atualiza o texto com novo tamanho e opacidade
        self.font = pygame.font.Font(self.font_path, int(self.current_size))
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.image.set_alpha(self.opacity)
        self.rect = self.image.get_rect(center=self.game.screen.get_rect().center)

    def render(self, screen):
        """Renderiza a transição no centro da tela."""
        if not self.finished:
            screen.blit(self.image, self.rect)


class GameOverTransition:
    """Efeito de transição para o Game Over."""
    
    def __init__(self, game):
        """Inicializa o efeito de Game Over."""
        # Criando o fundo vermelho translúcido
        self.bg_rect = self.window.get_rect()
        self.surface = pygame.Surface((self.bg_rect.width, self.bg_rect.height))
        self.surface.fill((255, 0, 0))  # Vermelho
        self.surface.set_alpha(100)  # Ajuste da opacidade do fundo

        # Criando o efeito de explosão
        self.flash_effect = FlashScreenEffect(window, duration=1.0, flash_speed=0.1)
        self.flash_finished = False  # Flag para saber quando a explosão terminou

        # Configuração do texto do Game Over (ainda não criado)
        self.animation = None

        # Criando a tela de Game Over (inicialmente oculta)
        self.game_over_screen = GameOverTransition(self.game)

        # Configuração da animação ExpandFadeAnimation
        self.animation = None
        self.wait_timer = 0  # Tempo decorrido após a animação

    def update(self, fps):
        """Atualiza o efeito de explosão e depois inicia o Game Over."""
        if not self.flash_finished:
            self.flash_effect.update(fps)
            if self.flash_effect.finished:
                self.flash_finished = True
                self._start_game_over_animation()
        else:
            if self.animation:
                self.animation.update(fps)
                self.wait_timer += fps
                if self.wait_timer >= 1:  # Após 1 segundo, exibe os botões e pontuação
                    self.game_over_screen.show()

    def render(self):
        """Desenha o efeito de Game Over na tela."""
        if not self.flash_finished:
            self.flash_effect.draw()  # Exibe apenas o efeito de explosão
        else:
            # Exibir o fundo vermelho translúcido
            self.window.blit(self.surface, self.bg_rect)
            
            # Exibir a animação do texto "GAME OVER"
            if self.animation:
                self.animation.render()
        
        # Exibe a tela de Game Over
        self.game_over_screen.render()

    def _start_game_over_animation(self):
        """Inicia a animação de Game Over após o efeito de explosão."""
        self.animation = ExpandFadeAnimation(
            text="GAME OVER",
            font_path="fonts/Android Assassin.ttf",
            window=self.window,
            font_sizes={
                'init': 30,       # Tamanho inicial pequeno
                'transition': 60, # Tamanho após impacto rápido
                'end': 80         # Tamanho final antes do fade-out
            },
            impact_speed=0.8,    # Crescimento rápido no impacto
            distance_speed=0.008, # Crescimento mais lento após o impacto
            fade_in_speed=5,     # Fade-in suave
            fade_out_speed=6,    # Fade-out controlado
            use_fade_in=True,    # Ativa o fade-in
            use_fade_out=False    # Ativa o fade-out
        )

