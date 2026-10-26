import pygame

# Esse código é só para ver se o Pygame-CE está instalado corretamente e funcionando.



# Inicializa o pygame
pygame.init()

# Mostra a versão no terminal para você confirmar que é o CE
print(f"Versão instalada: {pygame.__version__}")

# Abre uma janela simples de 400x400
tela = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Teste do Pygame-CE")

# Loop principal para manter a janela aberta
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()

