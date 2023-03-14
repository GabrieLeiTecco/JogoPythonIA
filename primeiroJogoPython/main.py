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
    def desenhar(self):
        