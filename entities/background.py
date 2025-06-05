import pygame

class GameBackground:
    """Anima camadas de estrelas para criar um efeito de profundidade no fundo do jogo"""

    def __init__(self, game):
        self.game = game
        self.screen_width = self.game.config.SCREEN["width"]
        self.screen_height = self.game.config.SCREEN["height"]

        # Carregar imagens das camadas
        self.layers = [
            {"image": pygame.image.load("graphics/backgrounds/space_bg.png").convert(), "speed": 0.5, "y": 0},  # Fundo móvel
            {"image": pygame.image.load("graphics/backgrounds/stars_far.png").convert_alpha(), "speed": 0.3, "y": 0},
            {"image": pygame.image.load("graphics/backgrounds/stars_mid.png").convert_alpha(), "speed": 0.6, "y": 0},
            {"image": pygame.image.load("graphics/backgrounds/stars_near.png").convert_alpha(), "speed": 1.2, "y": 0},
        ]

        # Ajustar tamanho das imagens para cobrir a tela
        for layer in self.layers:
            layer["image"] = pygame.transform.scale(layer["image"], (self.screen_width, self.screen_height))
            layer["y2"] = -self.screen_height  # Adiciona uma segunda posição para garantir o loop

    def update(self):
        """Atualiza a posição das camadas para criar o efeito de movimento contínuo"""
        if self.game.paused or self.game.powerup_freeze:
            return  # Se estiver pausado ou em paralisação, não move o fundo
    
        for layer in self.layers:
            if layer["speed"] > 0:  # Apenas move camadas que devem se deslocar
                layer["y"] += layer["speed"]
                layer["y2"] += layer["speed"]

                # Quando uma imagem sai totalmente da tela, reposicionamos acima da outra
                if layer["y"] >= self.screen_height:
                    layer["y"] = layer["y2"] - self.screen_height

                if layer["y2"] >= self.screen_height:
                    layer["y2"] = layer["y"] - self.screen_height

    def render(self, screen):
        """Renderiza as camadas na tela, garantindo um loop contínuo"""
        for layer in self.layers:
            screen.blit(layer["image"], (0, layer["y"]))  
            screen.blit(layer["image"], (0, layer["y2"]))  # Segunda posição para continuidade
