import sys, os, random, pygame
from termcolor import colored, cprint

gameData = {
    "playerNames": [], # lista dos nomes, playerNames[0] para o player 1, playerNames[1] para o player 2
    "turn": 0,
    "board": [[],[],[]] # board como lista de listas, cada lista representa uma linha, board[1][2] é a segunda linha, terceira coluna
}



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def regras():
    clear()
    print("O objetivo deste jogo é ser o primeiro a conseguir uma linha de três peças da mesma cor na horizontal, vertical ou diagonal.")
    print("O jogo realiza-se num tabuleiro, inicialmente vazio. Em cada jogada, cada jogador realiza uma das seguintes ações:")
    print("-> Colocar uma peça verde num quadrado vazio;")
    print("-> Substituir uma peça verde por uma peça amarela;")
    print("-> Substituir uma peça amarela por uma peça vermelha.")
    print("É importante realçar que as peças vermelhas não podem ser substituídas, o que significa que à medida que o tabuleiro fica com peças vermelhas, é inevitável que surja uma linha de três peças.")

def mainMenu():
    clear()
    print("SEMÁFORO ----")
    print("1: Jogar uma partida")
    print("2: Carregar uma partida a partir de um ficheiro")
    print("3: Apresentar uma descrição do jogo")
    print("4: Sair da aplicação")
    escolha = int(input("\nEscolha uma opção: "))
    match escolha:
        case 1: novoJogoPvP(gameData) # implementar PvB e BvB depois
        # case 2: carregarJogo() # ainda não implementado
        case 3: regras()
        case 4: sys.exit()
        case _:
            print("opção inválida")
            mainMenu()

"""
A. Caso o utilizador selecione a opção A devem ser realizadas as seguintes operações:
1. Pedir o Nome do jogador.
2. Selecionar aleatoriamente quem é o primeiro jogador, humano ou BOT.
3. Construir a interface do jogo, ou seja, desenhar na consola todos os elementos
necessários para visualizar o desenrolar da partida:
a. O tabuleiro de jogo.
b. Identificar cada jogador pela cor com que vai jogar.
4. Realizar o turno do primeiro jogador. Considera-se um turno de um jogador o conjunto
das ações que esse jogador executa até passar a vez ao jogador seguinte ou até o jogo
terminar. Só devem ser autorizadas as ações possíveis em cada fase.
a. Quando for o jogador humano a jogar seguir a sequência da jogada:
I. Escolher uma peça
II. Escolher o posicionamento
III. Passar a vez
IV. Sair (além de interromper o jogo deve gravar o estado do mesmo).
b. Quando for o Jogador BOT a jogar, aplicar um algoritmo para o BOT mostrando
as ações escolhidas pelo mesmo.
c. Tomada a decisão da ação escolhida (humano ou BOT), realizá-la e atualizar a
consola com os novos dados.
d. Depois de uma ação de qualquer Jogador (Humano ou BOT) gravar SEMPRE o
estado atual do jogo, de modo a ser possível dar a opção do jogador de
interromper para continuar mais tarde.
e. Todas as ações dos jogadores devem ser mantidas em memória, apresentando
na consola as ações do último turno dos dois jogadores.
5. Repetir alternadamente os turnos dos jogadores até que ocorra o final da partida.
6. Apresentar o vencedor do jogo.
"""
def novoJogoPvP(gameData):
    gameData["playerNames"].append(input("Nome do jogador 1: "))
    gameData["playerNames"].append(input("Nome do jogador 2: "))
    gameData["turn"] = random.randint(0,1)
    print(f"O jogador", gameData["playerNames"][gameData["turn"]], "joga primeiro.")

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # sair
            running = False

    screen.fill("white")

    # board de teste
    h = 80 # start height
    while h < 600:
        w = 240 # start width
        while w < 1000:
            pygame.draw.rect(screen, "black", pygame.Rect(w, h, 200, 200), 2)
            w += 200
        h += 200
    pygame.draw.rect(screen, "black", pygame.Rect(240, 80, 800, 600), 4)
        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()