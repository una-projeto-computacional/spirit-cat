
import pygame
from config import *
from ui import Botao, texto, painel, cabecalho, quebrar_texto, gradiente_arredondado, agora

REGRAS = [
    f"Você começa com {VIDAS} vidas.",
    f"Serão {TOTAL_PERGUNTAS} perguntas por partida.",
    "Cada resposta errada tira uma vida.",
    f"Responda as {TOTAL_PERGUNTAS} perguntas sem perder todas as vidas para vencer.",
    "Se as vidas acabarem, o espírito pega o gatinho e você perde.",
]


class TelaTutorial:
    def __init__(self, g):
        self.g = g
        self.card = pygame.Rect(0, 0, 720, 440)
        self.card.midtop = (LARGURA // 2, 110)
        self.b_voltar = Botao("Voltar", (LARGURA // 2, 595), largura=220, altura=50,
                              estilo="secundario")

    def ao_entrar(self, **dados):
        pass

    def eventos(self, evento):
        if self.b_voltar.clicou(evento):
            self.g.trocar("menu")

    def atualizar(self):
        pass

    def desenhar(self, tela):
        cabecalho(tela, agora())
        painel(tela, self.card)
        texto(tela, "Como jogar", 38, COR_TEXTO, centro=(self.card.centerx, self.card.y + 50),
              negrito=True)

        y = self.card.y + 105
        for i, regra in enumerate(REGRAS, start=1):
            linhas = quebrar_texto(regra, 20, self.card.w - 170)
            altura = max(40, len(linhas) * 26 + 10)
            tela.blit(gradiente_arredondado(38, 38, COR_GRAD_A, COR_GRAD_B, 19, False),
                      (self.card.x + 48, y))
            texto(tela, str(i), 20, COR_TEXTO, centro=(self.card.x + 67, y + 19), negrito=True)
            for j, linha in enumerate(linhas):
                texto(tela, linha, 20, COR_TEXTO, topo_esq=(self.card.x + 108, y + 6 + j * 26))
            y += altura + 14
        self.b_voltar.desenhar(tela)
