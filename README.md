# 🐱 Spirit Cat

Jogo desenvolvido como projeto prático da disciplina de **Matemática Computacional Aplicada (Prática)**, em Python com Pygame-CE.

## 🎮 Sobre o jogo

Um espírito está perseguindo um gatinho, e só a inteligência do jogador pode salvá-lo. A cada rodada, o jogador responde a uma pergunta de matemática:

- **Resposta certa:** o espírito é afastado.
- **Resposta errada:** o gatinho perde uma vida e o espírito se aproxima.

### Regras

- O gato começa com **3 vidas**.
- Cada partida tem **5 perguntas**.
- Responder as 5 perguntas sem perder todas as vidas é **vitória**.
- Perder as 3 vidas é **derrota**: o espírito pega o gatinho.

## 🖼️ Telas

| Tela | Descrição |
| --- | --- |
| Menu | Título do jogo, com os botões **Iniciar** e **Instruções**. |
| Nickname | O jogador digita seu nome (até 12 caracteres) antes de começar. |
| Tutorial | "Como jogar": explica as regras da partida. |
| Partida | Perguntas de matemática, vidas e espírito. |
| Resultado | Tela de vitória ou derrota, com as opções **Jogar novamente** e **Tela inicial**. |

Todo o visual (gato, espíritos, fundo, botões e painéis) é desenhado por código, sem imagens externas.

## 🚀 Como executar

### Requisitos

- Python 3.12 ou superior
- [Pygame-CE](https://pyga.me/) 2.5.8

### Passo a passo

```bash
# 1. (opcional) crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. instale a dependência
pip install -r requirements.txt

# 3. rode o jogo
python main.py
```

## 📁 Estrutura do projeto

```
./
|-- main.py          # Ponto de entrada e gerenciador de telas
|-- config.py        # Constantes: tamanho da janela, FPS, vidas, nº de perguntas e cores
|-- ui.py            # Componentes visuais: botões, painéis, campo de texto, gato e espírito
|-- requirements.txt # Dependências do projeto
|-- .gitignore       # Ignora .venv, __pycache__ e arquivos de editor
`-- telas/
    |-- menu.py      # Tela inicial
    |-- nick.py      # Entrada do nome do jogador
    |-- tutorial.py  # Instruções do jogo
    |-- partida.py   # Tela da partida
    `-- resultado.py # Vitória e derrota
```

Cada tela é uma classe com os métodos `ao_entrar`, `eventos`, `atualizar` e `desenhar`. O `Gerenciador`, em `main.py`, controla o laço principal e a troca entre elas (`trocar`), com uma transição suave de fade.

Para ajustar o jogo, edite o `config.py`. Por exemplo, `VIDAS` e `TOTAL_PERGUNTAS` mudam as regras, e as constantes `COR_*` mudam a paleta.

## 🧮 Matemática Computacional

Os conceitos estudados na disciplina serão aplicados às mecânicas do jogo, incluindo a utilização de cálculos matemáticos e algoritmos para a criação das perguntas e o funcionamento da partida.

## 🛠️ Tecnologias

- [Python](https://www.python.org/)
- [Pygame-CE](https://pyga.me/)

## 👥 Integrantes

* Arthur de Castro Oliveira
* José Glycério Emerick
* José Luiz Martins Silva
* Leonardo Gabriel Gomes dos Santos
* Priscila Bianca Alves

## 🚧 Status

🟡 **Em desenvolvimento**

- [x] Menu inicial
- [x] Tela de nickname
- [x] Tela de tutorial
- [x] Tela de resultado (vitória e derrota)
- [ ] Tela da partida: no momento é um *placeholder*, e as teclas `V` e `D` levam ao resultado de vitória ou derrota
- [ ] Banco de perguntas de matemática
- [ ] Lógica de vidas e de aproximação do espírito

Projeto desenvolvido para a disciplina de **Matemática Computacional Aplicada (Prática)**, com orientação do professor Julio Vilela da Silva Neto.
