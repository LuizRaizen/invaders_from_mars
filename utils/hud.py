import pygame

from utils.settings import Settings


class Score:
    """Gerencia a pontuação do jogador"""

    def __init__(self, game):
        self.game = game
        self.config = Settings()
        self.font = pygame.font.Font(*self.config.HUD['score_font'])
        self.color = self.config.HUD['color']
        self.score = self.config.PLAYER['score'] # Pontuação inicial

    def add_points(self, points):
        """Adiciona pontos ao jogador"""
        self.score += points

    def render(self, screen):
        """Exibe a pontuação na tela"""
        # Arredondar a pontuação para multiplos de dez;
        self.rounded_score = int(round(self.score, -1))
        # Inserir uma vírgula nos agrupamentos decimais;
        self.str_score =  str(self.rounded_score)
        # Complementar a pontuação com zeros até a casa do milhão;
        self.decimals = 10 - len(self.str_score)
        # Formatar string da pontuação de modo elegante;
        self.formated_score = ("0" * self.decimals) + self.str_score
        # Renderizar a string da pontuação;
        self.text = self.font.render(self.formated_score, True, self.color)
        # Renderizar a pontuação na tela
        screen.blit(self.text, (10, 10))


class Lives:
    """Gerencia as vidas do jogador"""

    def __init__(self, game):
        self.game = game
        self.config = Settings()

        # Obtém a quantidade de vidas inicial
        self.lives = self.config.PLAYER['lives']
        
        # Carrega e redimensiona a imagem da vida
        self.image = pygame.image.load(self.config.SHIP['image'])
        self.image = pygame.transform.scale(self.image, (28, 28))
        
        # Cria um fundo a partir da imagem da vida
        self.bg_image = self.image.copy()
        self.bg_image.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MULT)
        self.bg_image.set_alpha(120)

        # Carrega e configura a imagem do fundo do temporizador
        self.powerup_bg = pygame.image.load('graphics/sprites/powerups/powerup_bg.png')
        self.powerup_bg = pygame.transform.scale(self.powerup_bg, (32, 32))
        self.powerup_bg.set_alpha(100)
        self.powerup_bg_rect = self.powerup_bg.get_rect()
        self.powerup_bg_rect.x = 425
        self.powerup_bg_rect.y = 5

    def render(self, screen):
        """Renderiza as imagens das vidas na tela."""
        pos = (215, 10)

        # Renderiza a imagem do fundo
        x, y = pos[0], pos[1]
        for life in range(5):
            x += self.bg_image.get_rect().width
            screen.blit(self.bg_image, (x, y))

        # Renderiza a imagem da vida
        x, y = pos[0], pos[1]
        for life in range(self.lives):
            x += self.image.get_rect().width
            screen.blit(self.image, (x, y))

        # Renderiza o fundo dos powerups no temporizador
        x, y = 345, 5
        for powerup in range(3):
            x += 80
            screen.blit(self.powerup_bg, (x, y))
        

class Level:
    """Gerencia o nível do jogo"""

    def __init__(self, game):
        self.game = game
        self.config = Settings()
        self.font = pygame.font.Font(*self.config.HUD['lvl_font'])
        self.lvl = self.config.LEVEL # Nivel inicial
        self.text = self.font.render(f"{self.config.HUD['lvl_text']}{self.lvl}", True, self.config.HUD['color'])
        self.rect = self.text.get_rect()
        
    def update_level(self, level):
        """Atualiza a exibição do nível"""
        self.text = self.font.render(f"{self.config.HUD['lvl_text']}{self.lvl}", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.right = self.config.SCREEN['width'] - 20
        self.lvl = level

    def render(self, screen):
        """Exibe a pontuação na tela"""
        self.rect.right = self.config.SCREEN['width'] - 10
        self.rect.y = 10
        screen.blit(self.text, self.rect)


class PowerUpTimer:
    """Temporizador que exibe o tempo restante para o efeito do power-up"""

    def __init__(self, game, x_offset=0):
        self.game = game
        self.config = Settings()

        self.font = pygame.font.Font(*self.config.HUD['score_font'])
        self.base_x_offset = x_offset  # Posição inicial dos temporizadores

    def render(self, screen):
        """Renderiza o temporizador na tela"""
        if self.game.powerup_freeze or self.game.paused:  
            return  # Se o jogo estiver em paralisação, não atualiza o temporizador
    
        x_offset = self.base_x_offset  # Começa na posição definida

        for powerup_type in self.game.powerup_manager.active_powerups:
            remaining_time = self.game.powerup_manager.get_remaining_time(powerup_type)
            if powerup_type == 'speed':
                powerup_image = pygame.image.load('graphics/sprites/powerups/powerup_7.png')
            elif powerup_type == 'shield':
                powerup_image = pygame.image.load('graphics/sprites/powerups/powerup_2.png')
            elif powerup_type == 'double_shoot':
                powerup_image = pygame.image.load('graphics/sprites/powerups/powerup_1.png')
            
            # Redimensiona a imagem do power-up e obtém o rect da mesma
            powerup_image = pygame.transform.scale(powerup_image, (32, 32))
            powerup_rect = powerup_image.get_rect()
            powerup_rect.x = x_offset
            powerup_rect.y = 5
            
            # Cria o texto que exibe os segundos restantes para o efeito do power-up
            powerup_text = self.font.render(f"{remaining_time}s", True, (255, 255, 255))

            # Renderiza a imagem do power-up e os segundos restantes
            x, y = x_offset, 5
            screen.blit(powerup_image, (x, y))
            screen.blit(powerup_image, powerup_rect)
            screen.blit(powerup_text, (powerup_rect.right + 5, 10))  # Usa y_offset atualizado
            
            # Move para a direita a cada power-up
            x_offset += 80
