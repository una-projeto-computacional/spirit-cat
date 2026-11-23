
import pygame
from config import *
from ui import Botao, texto, painel, gato, cabecalho, campo_texto, agora


class TelaNick:
    def __init__(self, g):
        self.g = g
        self.nick = ""
        cx = LARGURA // 2
        self.card = pygame.Rect(0, 0, 640, 430)
        self.card.midtop = (cx, 115)
        self.campo = pygame.Rect(0, 0, 380, 54)
        self.campo.center = (cx, 425)
        self.b_ok = Botao("Começar aventura →", (cx, 500), largura=380, altura=54)
        self.b_voltar = Botao("← Voltar", (100, 605), largura=140, altura=40,
                              estilo="secundario", tamanho=18)

    def ao_entrar(self, **dados):
        self.nick = ""

    def _confirmar(self):
        if self.nick.strip():
            self.g.nick = self.nick.strip()
            self.g.trocar("partida")

    def eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                self._confirmar()
            elif evento.key == pygame.K_BACKSPACE:
                self.nick = self.nick[:-1]
            elif evento.unicode and evento.unicode.isprintable() and len(self.nick) < MAX_NICK:
                self.nick += evento.unicode
        if self.b_ok.clicou(evento):
            self._confirmar()
        elif self.b_voltar.clicou(evento):
            self.g.trocar("menu")

    def atualizar(self):
        self.b_ok.ativo = bool(self.nick.strip())

    def desenhar(self, tela):
        t = agora()
        cx = LARGURA // 2
        cabecalho(tela, t)
        painel(tela, self.card)

        gato(tela, (cx, 218), 0.7, t)
        texto(tela, "Entre nessa aventura!", 36, COR_TEXTO, centro=(cx, 316), negrito=True)
        texto(tela, "Um espírito está perseguindo o gatinho. Você consegue salvá-lo?", 17,
              COR_TEXTO_SUAVE, centro=(cx, 350))
        texto(tela, "Qual é o seu nome?", 17, COR_TEXTO, topo_esq=(self.campo.x + 6, 374), negrito=True)
        campo_texto(tela, self.campo, self.nick, "Digite seu nome...", t)
        self.b_ok.desenhar(tela)

        self.b_voltar.desenhar(tela)
        texto(tela, "Use sua inteligência para salvar o gatinho!", 15, COR_TEXTO_SUAVE,
              centro=(cx, 605))
