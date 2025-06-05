import pygame


class ImpactFadeAnimation:
    """
    Animação de impacto e fade-out para textos (usado no efeito de Level Up).
    Texto inicia em tamanho grande e opaco, depois diminui de tamanho e se desvanece.
    """

    def __init__(self, game, text, font_path, font_sizes, 
                 impact_speed=0.1, distance_speed=0.02, fade_out_speed=5):
        self.game = game
        self.window = game.screen
        self.text = text
        self.font_path = font_path

        # Tamanhos da animação
        self.initial_size = font_sizes['init']
        self.transition_size = font_sizes['transition']
        self.final_size = font_sizes['end']
        self.current_size = self.initial_size

        # Velocidades da animação
        self.impact_speed = impact_speed
        self.distance_speed = distance_speed
        self.fade_out_speed = fade_out_speed

        # Propriedades visuais
        self.opacity = 255
        self.font = pygame.font.Font(self.font_path, int(self.current_size))
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.window.get_rect().center)

        self.impact_finished = False

    def update(self, fps):
        """Atualiza a animação de transição."""
        if not self.impact_finished:
            if self.current_size > self.transition_size:
                self.current_size -= max((self.current_size - self.transition_size) * self.impact_speed, 1)
            else:
                self.impact_finished = True
        else:
            if self.current_size > self.final_size:
                self.current_size -= max((self.current_size - self.final_size) * self.distance_speed, 0.5)

        # Atualiza o texto com o novo tamanho e opacidade
        self.font = pygame.font.Font(self.font_path, int(self.current_size))
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.image.set_alpha(self.opacity)
        self.rect = self.image.get_rect(center=self.window.get_rect().center)

        # Aplica fade-out
        if self.opacity > 0:
            self.opacity -= self.fade_out_speed
            self.opacity = max(0, self.opacity)

    def render(self):
        """Desenha o texto animado na tela."""
        self.window.blit(self.image, self.rect)

    def is_finished(self):
        """Retorna True se a animação terminou completamente."""
        return self.opacity <= 0


class ExpandFadeAnimation:
    """Classe responsável pela animação de impacto, crescimento e fade-out do texto."""

    def __init__(self, text, font_path, window, font_sizes, 
                 impact_speed=0.1, distance_speed=0.02, 
                 fade_in_speed=10, fade_out_speed=5,
                 use_fade_in=True, use_fade_out=True):
        """
        :param text: Texto a ser animado.
        :param font_path: Caminho para a fonte.
        :param window: Tela do jogo.
        :param font_sizes: Dicionário com tamanhos {'init': inicial, 'transition': intermediário, 'end': final}.
        :param impact_speed: Velocidade do crescimento inicial (impacto).
        :param distance_speed: Velocidade do crescimento contínuo.
        :param fade_in_speed: Velocidade do aparecimento (ocorre junto com o impacto).
        :param fade_out_speed: Velocidade do desaparecimento.
        :param use_fade_in: Ativa ou desativa o fade-in.
        :param use_fade_out: Ativa ou desativa o fade-out.
        """
        self.window = window

        # Tamanhos da fonte
        self.initial_size = font_sizes['init']
        self.transition_size = font_sizes['transition']  # Tamanho intermediário do impacto
        self.final_size = font_sizes['end']
        self.current_size = self.initial_size
        self.opacity = 0 if use_fade_in else 255  # Se o fade-in estiver desativado, começa com opacidade total

        # Velocidades ajustáveis
        self.impact_speed = impact_speed  
        self.distance_speed = distance_speed  
        self.fade_in_speed = fade_in_speed  
        self.fade_out_speed = fade_out_speed  
        self.use_fade_in = use_fade_in
        self.use_fade_out = use_fade_out

        # Configurar fonte inicial
        self.font = pygame.font.Font(font_path, int(self.current_size))
        self.text = text

        # Renderizar o texto inicial
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.window.get_rect().center

        # Flags de estado
        self.impact_finished = False
        self.fade_in_finished = not use_fade_in  # Se o fade-in não for usado, já começa como finalizado

    def update(self, fps):
        """Atualiza a animação de impacto, crescimento e fade-out."""

        # Fase 1: Impacto + Fade-in simultâneo (se ativado)
        if not self.fade_in_finished:
            self.opacity += self.fade_in_speed
            if self.opacity >= 255:
                self.opacity = 255  # Garante que o fade-in termine em 255
                self.fade_in_finished = True  # Marca que o fade-in foi concluído

        if not self.impact_finished:
            if self.current_size < self.transition_size:
                self.current_size += max((self.transition_size - self.current_size) * self.impact_speed, 1)
            else:
                self.impact_finished = True  # Passa para a fase de crescimento contínuo

        # Fase 2: Crescimento contínuo até o tamanho final
        else:
            if self.current_size < self.final_size:
                self.current_size += max((self.final_size - self.current_size) * self.distance_speed, 0.5)

        # Atualiza a fonte e o texto renderizado
        self.font = pygame.font.Font("fonts/Android Assassin.ttf", int(self.current_size))
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.window.get_rect().center

        # Fase 3: Fade-out se ativado
        if self.use_fade_out and self.impact_finished and self.current_size >= self.final_size:
            if self.opacity > 0:
                self.opacity -= self.fade_out_speed
                self.opacity = max(0, self.opacity)  # Garante que não fique negativo

        # Define a opacidade do texto
        self.image.set_alpha(self.opacity)

    def draw(self):
        """Exibe a animação na tela."""
        self.window.blit(self.image, self.rect)
