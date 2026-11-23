
import math
import random
import pygame
from config import *

_fontes = {}
_cache = {}


def agora():

    return pygame.time.get_ticks() / 1000.0


def fonte(tamanho, negrito=False):
    chave = (tamanho, negrito)
    if chave not in _fontes:
        _fontes[chave] = pygame.font.SysFont(FONTE, tamanho, bold=negrito)
    return _fontes[chave]


def texto(tela, conteudo, tamanho, cor=COR_TEXTO, centro=None, topo_esq=None, negrito=False):
    superficie = fonte(tamanho, negrito).render(conteudo, True, cor)
    rect = superficie.get_rect()
    if centro:
        rect.center = centro
    elif topo_esq:
        rect.topleft = topo_esq
    tela.blit(superficie, rect)
    return rect


def quebrar_texto(conteudo, tamanho, largura_max):
   
    linhas, atual = [], ""
    for palavra in conteudo.split():
        teste = (atual + " " + palavra).strip()
        if fonte(tamanho).size(teste)[0] <= largura_max:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def texto_gradiente(tela, conteudo, tamanho, centro, cor_a=COR_GRAD_A, cor_b=COR_GRAD_B, negrito=True):
   
    surf = fonte(tamanho, negrito).render(conteudo, True, (255, 255, 255)).convert_alpha()
    grad = _gradiente(surf.get_width(), surf.get_height(), cor_a, cor_b, True)
    surf.blit(grad, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    tela.blit(surf, surf.get_rect(center=centro))



def _gradiente(largura, altura, cor_a, cor_b, horizontal):
    chave = ("grad", largura, altura, cor_a, cor_b, horizontal)
    if chave not in _cache:
        surf = pygame.Surface((largura, altura))
        n = largura if horizontal else altura
        for i in range(n):
            t = i / max(1, n - 1)
            cor = tuple(int(cor_a[k] + (cor_b[k] - cor_a[k]) * t) for k in range(3))
            if horizontal:
                pygame.draw.line(surf, cor, (i, 0), (i, altura))
            else:
                pygame.draw.line(surf, cor, (0, i), (largura, i))
        _cache[chave] = surf.convert_alpha()
    return _cache[chave]


def _arredondar(surf, raio):
    mascara = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(mascara, (255, 255, 255, 255), mascara.get_rect(), border_radius=raio)
    surf.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return surf


def gradiente_arredondado(largura, altura, cor_a, cor_b, raio, horizontal=True):
    chave = ("grad_arr", largura, altura, cor_a, cor_b, raio, horizontal)
    if chave not in _cache:
        surf = _gradiente(largura, altura, cor_a, cor_b, horizontal).copy()
        _cache[chave] = _arredondar(surf, raio)
    return _cache[chave]



def sombra(tela, rect, raio=20, alpha=12, dy=10, camadas=6):
    m = camadas * 4 + 4
    chave = ("sombra", rect.w, rect.h, raio, alpha, camadas)
    if chave not in _cache:
        surf = pygame.Surface((rect.w + 2 * m, rect.h + 2 * m), pygame.SRCALPHA)
        for i in range(camadas):                
            g = (camadas - i) * 4
            r = pygame.Rect(m - g, m - g, rect.w + 2 * g, rect.h + 2 * g)
            pygame.draw.rect(surf, (0, 0, 0, alpha * (i + 1)), r, border_radius=raio + g)
        _cache[chave] = surf
    tela.blit(_cache[chave], (rect.x - m, rect.y - m + dy))


def painel(tela, rect, raio=26):
  
    sombra(tela, rect, raio, alpha=12, dy=14)
    chave = ("painel", rect.w, rect.h, raio)
    if chave not in _cache:
        surf = _gradiente(rect.w, rect.h, COR_PAINEL_A, COR_PAINEL_B, False).copy()
        _arredondar(surf, raio)
        pygame.draw.rect(surf, COR_BORDA, surf.get_rect(), 2, border_radius=raio)
        _cache[chave] = surf
    tela.blit(_cache[chave], rect.topleft)



class Fundo:


    def __init__(self):
        rnd = random.Random(7)
        self.estrelas = [
            (rnd.uniform(0, LARGURA), rnd.uniform(0, ALTURA), rnd.uniform(0.8, 2.2),
             rnd.uniform(0, 6.28), rnd.uniform(3, 12))
            for _ in range(80)
        ]
        self.base = None

    def _montar(self):
        base = _gradiente(LARGURA, ALTURA, COR_FUNDO_A, COR_FUNDO_B, False).copy()
        brilho = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        for r in range(460, 10, -6):
            a = int(48 * (1 - r / 460) ** 1.5)
            pygame.draw.circle(brilho, (*COR_GRAD_A, a), (LARGURA // 2, 0), r)
        base.blit(brilho, (0, 0))
        self.base = base

    def desenhar(self, tela, t):
        if self.base is None:
            self._montar()
        tela.blit(self.base, (0, 0))
        for x, y0, raio, fase, vel in self.estrelas:
            y = (y0 - t * vel) % ALTURA
            luz = 0.5 + 0.5 * math.sin(t * 1.6 + fase)
            c = int(80 + 130 * luz)
            pygame.draw.circle(tela, (c, c, min(255, c + 35)), (int(x), int(y)), max(1, int(raio)))



class Botao:
    def __init__(self, rotulo, centro, largura=320, altura=58, estilo="primario", tamanho=24):
        self.rotulo = rotulo
        self.rect = pygame.Rect(0, 0, largura, altura)
        self.rect.center = centro
        self.estilo = estilo          
        self.tamanho = tamanho
        self.ativo = True
        self.hover = 0.0

    def clicou(self, evento):
        return (self.ativo and evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1 and self.rect.collidepoint(evento.pos))

    def desenhar(self, tela):
        sobre = self.ativo and self.rect.collidepoint(pygame.mouse.get_pos())
        self.hover += ((1.0 if sobre else 0.0) - self.hover) * 0.25
        r = self.rect.move(0, int(-3 * self.hover))
        raio = r.h // 2
        cor_texto = COR_TEXTO

        if not self.ativo:
            pygame.draw.rect(tela, COR_BOTAO_OFF, r, border_radius=raio)
            cor_texto = COR_TEXTO_SUAVE
        elif self.estilo == "primario":
            sombra(tela, r, raio, alpha=10, dy=8, camadas=5)
            tela.blit(gradiente_arredondado(r.w, r.h, COR_GRAD_A, COR_GRAD_B, raio), r.topleft)
            if self.hover > 0.02:
                luz = pygame.Surface(r.size, pygame.SRCALPHA)
                pygame.draw.rect(luz, (255, 255, 255, int(45 * self.hover)),
                                 luz.get_rect(), border_radius=raio)
                tela.blit(luz, r.topleft)
        else:
            fundo = pygame.Surface(r.size, pygame.SRCALPHA)
            pygame.draw.rect(fundo, (255, 255, 255, int(10 + 22 * self.hover)),
                             fundo.get_rect(), border_radius=raio)
            tela.blit(fundo, r.topleft)
            pygame.draw.rect(tela, (125, 112, 190), r, 2, border_radius=raio)

        texto(tela, self.rotulo, self.tamanho, cor_texto, centro=r.center, negrito=True)



def campo_texto(tela, rect, conteudo, placeholder, t):
   
    brilho = pygame.Surface((rect.w + 40, rect.h + 40), pygame.SRCALPHA)
    for i in range(5, 0, -1):
        r = pygame.Rect(20 - i * 3, 20 - i * 3, rect.w + i * 6, rect.h + i * 6)
        pygame.draw.rect(brilho, (*COR_GRAD_A, 14 * (6 - i)), r, border_radius=rect.h // 2 + i * 3)
    tela.blit(brilho, (rect.x - 20, rect.y - 20))

    pygame.draw.rect(tela, COR_CAMPO, rect, border_radius=rect.h // 2)
    pygame.draw.rect(tela, COR_GRAD_A, rect, 2, border_radius=rect.h // 2)

    f = fonte(24)
    x = rect.x + 24
    if conteudo:
        surf = f.render(conteudo, True, COR_TEXTO)
        tela.blit(surf, (x, rect.centery - surf.get_height() // 2))
        x += surf.get_width() + 3
    else:
        surf = f.render(placeholder, True, (110, 106, 150))
        tela.blit(surf, (x, rect.centery - surf.get_height() // 2))
    if int(t * 2) % 2 == 0:
        pygame.draw.line(tela, COR_TEXTO, (x, rect.centery - 13), (x, rect.centery + 13), 2)



def _elipse_alpha(tela, cor, rect):
    s = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(s, cor, s.get_rect())
    tela.blit(s, rect.topleft)


def brilho(tela, pos, tam, cor=(255, 226, 150)):
   
    x, y = pos
    q = tam * 0.25
    pts = [(x, y - tam), (x + q, y - q), (x + tam, y), (x + q, y + q),
           (x, y + tam), (x - q, y + q), (x - tam, y), (x - q, y - q)]
    pygame.draw.polygon(tela, cor, pts)


def gato(tela, centro, escala=1.0, t=0.0, feliz=False):
   
    s = escala
    cx = centro[0]
    cy = centro[1] + math.sin(t * 2.0) * 4 * s
    corpo, claro = COR_GATO, COR_GATO_CLARO

    _elipse_alpha(tela, (0, 0, 0, 70), pygame.Rect(cx - 48 * s, centro[1] + 90 * s, 96 * s, 14 * s))

  
    for k in range(14):
        a = k / 13
        x = cx + 38 * s + 34 * s * math.sin(a * 2.4) + math.sin(t * 3 + a * 2.5) * 7 * s * a
        y = cy + 52 * s - 86 * s * a
        pygame.draw.circle(tela, corpo, (int(x), int(y)), int(max(2, (9 - 4 * a) * s)))

   
    pygame.draw.ellipse(tela, corpo, pygame.Rect(cx - 50 * s, cy + 8 * s, 100 * s, 84 * s))
    for dx in (-22, 22):
        pygame.draw.ellipse(tela, claro, pygame.Rect(cx + dx * s - 16 * s, cy + 78 * s, 32 * s, 18 * s))

    
    for lado in (-1, 1):
        ext = [(cx + lado * 44 * s, cy - 34 * s), (cx + lado * 40 * s, cy - 82 * s), (cx + lado * 8 * s, cy - 52 * s)]
        interna = [(cx + lado * 38 * s, cy - 44 * s), (cx + lado * 37 * s, cy - 70 * s), (cx + lado * 18 * s, cy - 52 * s)]
        pygame.draw.polygon(tela, corpo, ext)
        pygame.draw.polygon(tela, COR_ROSA, interna)

   
    pygame.draw.ellipse(tela, corpo, pygame.Rect(cx - 48 * s, cy - 59 * s, 96 * s, 82 * s))

  
    piscando = (t % 4.0) > 3.88
    for dx in (-19, 19):
        ex, ey = cx + dx * s, cy - 18 * s
        larg = max(2, int(3 * s))
        if feliz:
            pygame.draw.arc(tela, COR_OLHO, pygame.Rect(ex - 11 * s, ey - 6 * s, 22 * s, 20 * s), 0.35, 2.8, larg)
        elif piscando:
            pygame.draw.line(tela, COR_OLHO, (ex - 10 * s, ey), (ex + 10 * s, ey), larg)
        else:
            pygame.draw.ellipse(tela, COR_OLHO, pygame.Rect(ex - 11 * s, ey - 13 * s, 22 * s, 26 * s))
            pygame.draw.ellipse(tela, (20, 16, 32), pygame.Rect(ex - 3 * s, ey - 11 * s, 6 * s, 22 * s))
            pygame.draw.circle(tela, (255, 255, 255), (int(ex + 4 * s), int(ey - 6 * s)), max(1, int(3 * s)))

    # nariz, boca e bigodes
    pygame.draw.polygon(tela, COR_ROSA, [(cx - 5 * s, cy - 8 * s), (cx + 5 * s, cy - 8 * s), (cx, cy - 2 * s)])
    larg = max(1, int(2 * s))
    pygame.draw.line(tela, claro, (cx, cy - 2 * s), (cx, cy + 3 * s), larg)
    pygame.draw.line(tela, claro, (cx, cy + 3 * s), (cx - 6 * s, cy + 7 * s), larg)
    pygame.draw.line(tela, claro, (cx, cy + 3 * s), (cx + 6 * s, cy + 7 * s), larg)
    for lado in (-1, 1):
        for i in range(3):
            pygame.draw.line(tela, (200, 200, 225),
                             (cx + lado * 28 * s, cy - 4 * s + i * 4 * s),
                             (cx + lado * 64 * s, cy - 12 * s + i * 9 * s), larg)


def fantasma(tela, centro, escala=1.0, t=0.0):
   
    s = escala
    w, h = int(110 * s), int(130 * s)
    cx = centro[0]
    cy = centro[1] + math.sin(t * 2.2 + 1) * 7 * s

    aura = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
    for i in range(7):
        rad = int(w * 0.95 - i * w * 0.11)
        pygame.draw.circle(aura, (*COR_GRAD_A, 10 + i * 5), (w, h), rad)
    tela.blit(aura, (int(cx - w), int(cy - h)))

    sf = pygame.Surface((w + 4, h + 12), pygame.SRCALPHA)
    cor = (238, 234, 255, 230)
    r = w // 2
    n = 4
    rr = w / (2 * n)
    pygame.draw.circle(sf, cor, (2 + r, 2 + r), r)
    pygame.draw.rect(sf, cor, pygame.Rect(2, 2 + r, w, int(h - r - rr)))
    for i in range(n):                         # barra ondulada
        onda = math.sin(t * 4 + i * 1.3) * 3 * s
        pygame.draw.circle(sf, cor, (int(2 + rr * (2 * i + 1)), int(2 + h - rr + onda)), int(rr))

    escuro = (44, 34, 92, 255)
    for dx in (0.33, 0.67):
        pygame.draw.ellipse(sf, escuro, pygame.Rect(int(2 + w * dx - 7 * s), int(2 + r * 0.85), int(14 * s), int(20 * s)))
        pygame.draw.circle(sf, (255, 150, 200, 120), (int(2 + w * dx + (-1 if dx < 0.5 else 1) * 14 * s), int(2 + r * 1.3)), max(2, int(6 * s)))
    pygame.draw.ellipse(sf, escuro, pygame.Rect(int(2 + w / 2 - 8 * s), int(2 + r * 1.35), int(16 * s), int(22 * s)))
    tela.blit(sf, (int(cx - w / 2 - 2), int(cy - h / 2 - 2)))


def cabecalho(tela, t):

    fantasma(tela, (112, 52), 0.28, t)
    gato(tela, (70, 54), 0.22, t)
    texto(tela, NOME_JOGO, 30, COR_TEXTO, topo_esq=(150, 24), negrito=True)
    texto(tela, SUBTITULO, 15, COR_TEXTO_SUAVE, topo_esq=(150, 60))
