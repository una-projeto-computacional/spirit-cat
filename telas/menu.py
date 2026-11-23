
import math
from config import *
from ui import Botao, texto, texto_gradiente, gato, fantasma, agora


class TelaMenu:
    def __init__(self, g):
        self.g = g
        cx = LARGURA // 2
        self.b_iniciar = Botao("Iniciar", (cx, 470))
        self.b_instrucoes = Botao("Instruções", (cx, 540), estilo="secundario")

    def ao_entrar(self, **dados):
        pass

    def eventos(self, evento):
        if self.b_iniciar.clicou(evento):
            self.g.trocar("nick")
        elif self.b_instrucoes.clicou(evento):
            self.g.trocar("tutorial")

    def atualizar(self):
        pass

    def desenhar(self, tela):
        t = agora()
        cx = LARGURA // 2
        texto_gradiente(tela, NOME_JOGO, 76, (cx, 100))
        texto(tela, SUBTITULO, 22, COR_TEXTO_SUAVE, centro=(cx, 165))

        
        fantasma(tela, (cx + 150 - 14 * math.sin(t * 1.3), 320), 1.05, t)
        gato(tela, (cx - 80, 325), 1.0, t)

        self.b_iniciar.desenhar(tela)
        self.b_instrucoes.desenhar(tela)
        texto(tela, "Use sua inteligência para salvar o gatinho!", 16, COR_TEXTO_SUAVE,
              centro=(cx, 610))
