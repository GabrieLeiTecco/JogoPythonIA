import pygame
import random
import os

# Temos que definir constantes
# A largura da tela, altura da tela, etc
# Definir como constante (Letra maiuscula)
TELA_LARGURA = 500
TELA_ALTURA = 800

# Imagens
IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
# Primeiro um código para dobrar o tamanho da imagem pra ela não ficar pequena
IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
# Depois o comando para carregar uma imagem pelo caminho dela
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
# E no final um comando usando a biblioteca OS pra "juntar" o caminho para a imagem que vai ser selecionada
IMGS_PASSARO = [ # O passaro vai ter mais de uma imagem então tem que ser colocado em um array
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

# Fonte
pygame.font.init() #Precisa iniciar a função de fontes
FONTE_PONTOS = pygame.font.SysFont('arial', 50) # e colocar a fonte e o tamanho
# SysFont cria um objeto de uma fonte do sistema, fontes padrão em geral
# (e caso não tenha a fonte que você colocou vai usar a fonte padrão do sistema)

# Classes dos objetos do jogo
# Classe do passaro
class Passaro:
    # imagens do passaro
    IMGS = IMGS_PASSARO

    # animações de rotação
    ROTACAO_MAX = 25 # O valor máximo da rotação do passaro
    VELOCIDADE_ROTACAO = 20 # A velocidade da rotação do passaro
    TEMPO_ANIMACAO = 5 # Duração da animação da rotação do passaro

    # Funções
    # Função "iniciar" do passaro
    # Vulgo tudo que ele tem que ter quando é criado (vc da play no jogo)
    def __init__(self, x, y): # dentro dos () tem que ter os valores passados para o objeto
        self.x = x # o valor de x onde ele esta
        self.y = y # o valor y onde ele esta
        self.angulo = 0 # o angulo inicial
        self.velocidade = 0 # a velocidade inicial
        self.altura = self.y # a altura que ele esta
        self.tempo = 0 # a duracao inicial da parabola do pasasro
        self.imagem = self.IMGS[0] # a imagem inicial do passaro
        self.contagem_imagem = 0 # a contagem para mudar a imagem que está sendo usada

    # Função pular
    def pular(self):
        self.velocidade = -10.5
        # O valor y no pygame é: quanto menor, mais alto e quanto maior, mais baixo
        self.tempo = 0
        self.altura = self.y

    # Função mover
    def mover(self):
        # calcular o deslocamento
        self.tempo += 1 # ir aumentando a velocidade conforme o tempo passa
        deslocamento = 1.5 + (self.tempo**2) + self.velocidade * self.tempo
        # formula para calcular a parabola

        # Limites de movimento
        if deslocamento > 16:
            deslocamento = 16 # Limita o deslocamento
        elif deslocamento < 0:
            deslocamento -= 2 # Ajuda o pulo do passaro, para facilitar a gameplay

        self.y += deslocamento

        # Angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50): # deixa a rotação mais "natural"
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX # limita a rotação
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO # Limita a rotação

    # Função desenhar (coloca o passaro na tela)
    def desenhar(self, tela):
        # definir qual imagem do passaro vai ser usada
        self.contagem_imagem =+ 1

        # Definindo a animação do passaro
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o passaro estiver caindo não vai bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            # detalhe para o passaro bater asa pra baixo depois de cair
            self.contagem_imagem = self.TEMPO_ANIMACAO+2

        # desenhar a imagem
        # armazena a imagem do passaro no angulo que ela esta
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        # armazena o valor do centro da imagem usando de base o valor superior esquerdo da imagem
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        # cria o retangulo da imagem com o centro dela obtido acima
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        # insere a imagem na tela, usando de base os dados acima
        tela.blit(imagem_rotacionada, retangulo.topleft)

    # Função colisão/mascara
    def get_mask(self):
        # Esse codigo cria uma mascara para fazer uma colisão pixel perfect
        pygame.mask.from_surface(self.imagem)

# Classe do cano
class cano:
    # constantes
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        # pega a imagem do cano e inverte ela verticalmente (img, flipar x, flipar y)
        self.CANO_TOPO = pygame.transform.flip(IMG_CANO, False, True)
        self.CANO_BASE = IMG_CANO
        # identifica se o cano passou do passaro ou nao
        self.passou = False
        # Metodo que define altura do cano
        self.definir_altura()

    # Função definir altura
    def definir_altura(self):
        # gera um número aleatório dentro dos dois valores colocados
        self.altura = random.randrange(50, 450)
        # cria um cano usando de base o tamanho dele
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    # Função mover
    def mover(self):
        self.x -= self.VELOCIDADE

    # Função desenhar
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    # Função colidir
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_topo = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False
