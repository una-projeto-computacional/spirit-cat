
import math
import pygame
from config import *
from ui import Botao, texto, painel, cabecalho, gato, fantasma, brilho, agora


class TelaResultado:
    def __init__(self, g):
        self.g = g
        self.venceu = False
        cx = LARGURA // 2
        self.card = pygame.Rect(0, 0, 600, 470)
        self.card.midtop = (cx, 100)
        self.b_novamente = Botao("Jogar novamente", (cx, 465), largura=340, altura=52)
        self.b_inicio = Botao("Tela inicial", (cx, 527), largura=340, altura=52,
                              estilo="secundario")

    def ao_entrar(self, venceu=False, **dados):
        self.venceu = venceu

    def eventos(self, evento):
        if self.b_novamente.clicou(evento):
            self.g.trocar("partida")      # mantém o mesmo nick
        elif self.b_inicio.clicou(evento):
            self.g.trocar("menu")

    def atualizar(self):
        pass

    def desenhar(self, tela):
        t = agora()
        cx = LARGURA // 2
        cabecalho(tela, t)
        painel(tela, self.card)

        if self.venceu:
            titulo, cor = "Vitória!", COR_VITORIA
            msg = f"Parabéns, {self.g.nick}! Você salvou o gatinho!"
            sub = "O espírito foi embora. Que inteligência a sua, obrigado! Eu te amo!😻"
            gato(tela, (cx, 205), 0.85, t, feliz=True)
            for i in range(6):                      
                ang = t * 1.2 + i * math.pi / 3
                pos = (cx + math.cos(ang) * 120, 200 + math.sin(ang) * 55)
                brilho(tela, pos, 7 + 4 * abs(math.sin(t * 3 + i)))
        else:
            titulo, cor = "Derrota", COR_DERROTA
            msg = f"Você me deixou morrer, seu monstro!😿 {self.g.nick}..."
            sub = "Tente de novo e use sua inteligência!"
            fantasma(tela, (cx + 85, 205), 0.95, t)
            gato(tela, (cx - 85, 210), 0.8, t)

        texto(tela, titulo, 52, cor, centro=(cx, 335), negrito=True)
        texto(tela, msg, 22, COR_TEXTO, centro=(cx, 384))
        texto(tela, sub, 17, COR_TEXTO_SUAVE, centro=(cx, 414))
        self.b_novamente.desenhar(tela)
        self.b_inicio.desenhar(tela)
