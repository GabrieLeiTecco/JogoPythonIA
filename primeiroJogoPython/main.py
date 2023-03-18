import sys

import pygame
import random
import os

# Temos que definir constantes
# A largura da tela, altura da tela, etc
# Definir como constante (Letra maiuscula)
TELA_LARGURA = 500
TELA_ALTURA = 800

# Imagens
# Primeiro um código para dobrar o tamanho da imagem para ela não ficar pequena
IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
# Depois o comando para carregar uma imagem pelo caminho dela
IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
# E no final um comando usando a biblioteca OS pra "juntar" o caminho para a imagem que vai ser selecionada
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
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
        # O valor y no pygame é: quanto menor, mais alto e quanto maior, mais baixo
        self.velocidade = -8.5
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
        # retorna uma mascara para fazer uma colisão pixel perfect
        return pygame.mask.from_surface(self.imagem)

# Classe do cano
class Cano:
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
        # executa a função de pegar a mascara do passaro
        passaro_mask = passaro.get_mask()
        # pega a mascara do cano do topo
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        # pega a mascara do cano da base
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        # pega a distancia entre o cano e o passaro
        # primeiro a distancia do x depois a do y
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # o momento onde colide a colisão do cano com o passaro
        # resultado "True" ou "False"
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        # confere se o passaro colidiu ou não
        if base_ponto or topo_ponto:
            return True
        else:
            return False

# Classe do chão
class Chao:
    # Constantes do chão
    VELOCIDADE = 5
    LARGURA = IMG_CHAO.get_width()
    IMAGEM = IMG_CHAO

    # Função iniciar
    def __init__(self, y):
        self.y = y
        # O valor horizontal das imagens duplicadas que vão ser usadas
        self.x1 = 0
        self.x2 = self.LARGURA

    # Função mover
    def mover(self):
        # mexe as imagens para a esquerda
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        # se a imagem sair totalmente da tela ela vai pro outro lado
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.LARGURA

    # Função desehar
    def desenhar(self, tela):
        # desenha as duas imagens na tela
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

# Função desenhar tela do jogo
def desenhar_tela(tela, passaros, canos, chao, pontos):
    # insere o background na tela na posição 0,0
    tela.blit(IMG_BACKGROUND, (0, 0))

    # cria os passaros e os canos na tela
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    # cria o texto que vai mostrar a pontuação, (texto, com serifa 1 ou sem serifa 0, cor em rgb)
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    # coloca o texto na tela
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    # desenha o chao na tela
    chao.desenhar(tela)
    # atualiza a tela
    pygame.display.update()

def main():
    # dando os parametros que cada classe precisa
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    # configurando a tela
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    # o tempo do jogo (frames)
    relogio = pygame.time.Clock()
    # variavel que confere se o jogo esta rodando
    rodando = True

    # jogo rodando
    while rodando:
        # faz o tempo passar
        relogio.tick(30)

        # Interação com o usuário
        # verifica se um "evento" aconteceu
        for evento in pygame.event.get():
            # Se o evento for quitar ele fecha o jogo e atribui "falso" à variavel rodando
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
                sys.exit()

            # se o evento for uma tecla pressionada
            if evento.type == pygame.KEYDOWN:
                # se for o espaço
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        # faz as coisas se moverem
        for passaro in  passaros:
            passaro.mover()
        chao.mover()

        # cria variaveis para a criação e remoção do cano
        adicionar_cano = False
        remover_canos = []

        # verifica cada cano
        for cano in canos:
            # verifica cada passaro
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    # apaga o passaro
                    passaros.pop(i)
                    quit()
                    sys.exit()
                # verifica se a função cano.passou é falsa mas o passaro passou do cano
                if not cano.passou and passaro.x > cano.x:
                    # ativa a função cano passou
                    cano.passou = True
                    # muda a variavel para verdadeira
                    adicionar_cano = True
            # move o cano
            cano.mover()
            # se o cano sair da tela
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                # remove o cano
                remover_canos.append(cano)

        # se a variavel adicionar_cano for true
        if adicionar_cano:
            # adiciona pontos
            pontos += 1
            # cria um cano fora da tela
            canos.append(Cano(600))
        # verifica os canos dentro da lista remover_canos
        for cano in remover_canos:
            # remove os canos dentro dessa lista
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            # verifica se o passaro saiu da tela por cima ou por baixo
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                # apaga o passaro que fizer isso
                passaros.pop(i)
                quit()
                sys.exit()

        # desenha a tela
        desenhar_tela(tela, passaros, canos, chao, pontos)

# caso esse seja o arquivo principal, executa main()
if __name__ == '__main__':
    main()
