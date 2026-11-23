
import pygame
from config import *
from ui import texto


class TelaPartida:
    def __init__(self, g):
        self.g = g

    def ao_entrar(self, **dados):
        pass

    def eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_v:
                self.g.trocar("resultado", venceu=True)
            elif evento.key == pygame.K_d:
                self.g.trocar("resultado", venceu=False)

    def atualizar(self):
        pass

    def desenhar(self, tela):
        texto(tela, f"Partida de {self.g.nick} (placeholder)", 32, COR_TEXTO,
              centro=(LARGURA // 2, 250))
        texto(tela, "Aperte V para vitória ou D para derrota", 24, COR_TEXTO_SUAVE,
              centro=(LARGURA // 2, 320))
