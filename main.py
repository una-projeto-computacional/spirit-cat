
import sys
import pygame
from config import *
from ui import Fundo, agora
from telas.menu import TelaMenu
from telas.nick import TelaNick
from telas.tutorial import TelaTutorial
from telas.partida import TelaPartida
from telas.resultado import TelaResultado


class Gerenciador:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()
        self.nick = ""         
        self.fundo = Fundo()

     
        self.cortina = pygame.Surface((LARGURA, ALTURA))
        self.cortina.fill(COR_FUNDO_B)
        self.fade = 0

        self.telas = {
            "menu": TelaMenu(self),
            "nick": TelaNick(self),
            "tutorial": TelaTutorial(self),
            "partida": TelaPartida(self),
            "resultado": TelaResultado(self),
        }
        self.atual = None
        self.trocar("menu")

    def trocar(self, nome, **dados):
       
        self.atual = self.telas[nome]
        self.atual.ao_entrar(**dados)
        self.fade = 220

    def rodar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.atual.eventos(evento)
            self.atual.atualizar()

            self.fundo.desenhar(self.tela, agora())
            self.atual.desenhar(self.tela)

            if self.fade > 0:
                self.cortina.set_alpha(self.fade)
                self.tela.blit(self.cortina, (0, 0))
                self.fade = max(0, self.fade - 16)

            pygame.display.flip()
            self.relogio.tick(FPS)


if __name__ == "__main__":
    Gerenciador().rodar()
