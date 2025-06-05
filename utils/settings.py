class Settings:
    """Classe que contém as configurações do jogo."""

    def __init__(self):
        # Configurações de tela
        self.SCREEN = {
            'caption': "Invaders From Mars",
            'width': 800,
            'height': 600,
            'fps': 60
        }
        # Configurações do jogador;
        self.PLAYER = {
            'score': 0,
            'high_score': 5000,
            'lives': 0
        }
        # Configurações da nave do jogador;
        self.SHIP = {
            'image': "graphics/sprites/ships/ship_1.png",
            'speed': 5,
        }
        # Configurações dos projéteis da nave do jogador;
        self.SHIP_BULLET = {
            'width': 6,
            'height': 15,
            'color': (200, 200, 60),
            'allowed': 3
        }
        # Configurações dos projéteis do power-up 'Double Shoot';
        self.DOUBLE_BULLET = {
            'image': 'graphics/sprites/powerups/powerup_1.png',
            'width': 6,
            'height': 15,
            'color': (60, 200, 200),
            'allowed': 10
        }
        self.SHIELD = {
            'image': 'graphics/sprites/powerups/powerup_2.png'
        }
        self.SPEED = {
            'image': 'graphics/sprites/powerups/powerup_7.png',
        }
        # Configurações dos PowerUps
        self.POWERUP = {
            'speed': 2,
        }
        # Configurações dos alienigenas;
        self.ALIEN = {
            'image': 'graphics/sprites/aliens/alien_1.png',
            'drop_speed': 20,
            'speedup_scale': .2,
            'points': 50
        }
        # Configurações dos projéteis dos alienigenas;
        self.ALIEN_BULLET = {
            'width': 6,
            'height': 15,
            'color': (200, 200, 60),
            'allowed': 3
        }
        # Definição do nivel inicial do jogo
        self.LEVEL = 1
        # Configurações do SCOREUP
        self.SCOREUP = {
            'font': ('fonts/Android Assassin.ttf', 26),
            'color': (255, 255, 255),
            'speed': 2,
            'scale': 2.5
        }
        # Configurações dos planos de fundo do jogo;
        self.BACKGROUND = {
            'menu': 'graphics/backgrounds/title_menu_bg.jpg',
            'game': 'graphics/backgrounds/gameplay_bg.jpg'
        }
        # Configuraçẽos da GUI na tela de gameplay;
        self.HUD = {
            'lvl_font': ('fonts/conthrax-sb.otf', 22),
            'lvl_text': "LV ",
            'score_font': ('fonts/conthrax-sb.otf', 22),
            'score_text': "PONTOS: ",
            'lives_font': ('fonts/conthrax-sb.otf', 22),
            'lives_text': "VIDAS: ",
            'color': (255, 255, 255)
        }
        # Configurações do Menu Principal;
        self.TITLE_MENU = {
            'logo_image': "graphics/images/logo.png",
            'menu': {
                "Jogar": 'play',
                "Recordes": "records",
                "Opções": "options",
                "Créditos": "credits",
                "Sair": "quit"
            }
        }
        # Configurações dos botões
        self.BUTTONS = {
            'font': ("fonts/conthrax-sb.otf", 16)
        }
        self.transition_effect = None
        # Configurações do rodapé
        self.BASEBOARD = {
            'text': "Criado por Luiz R. Dererita, Copyright - 2023",
            'font': ("fonts/conthrax-sb.otf", 12)
        }
        # Configurações do Menu de Opções;
        self.OPTIONS = {"Level ": self.LEVEL,
                        "Idioma": ["Português", "Español", "English"],
                        "Editar Perfil": "profile_edit"}
        # Configura da Tela de Créditos;
        self.credits = False
        