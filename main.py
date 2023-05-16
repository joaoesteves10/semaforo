import sys, os, random
from termcolor import colored, cprint

gameData = {
    "playerNames": [], # lista dos nomes, playerNames[0] para o player 1, playerNames[1] para o player 2
    "turn": 0,
    "board": [[0,0,0,0],[0,0,0,0],[0,0,0,0]] # board como lista de listas, cada lista representa uma linha, board[1][2] é a segunda linha, terceira coluna
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

def printBoard(gameData):
    print("  1 | 2 | 3 | 4 |")
    for i in range(3):
        print(i+1, end=" ")
        for j in range(4):
            printPiece(gameData["board"][i][j])
            print(" | ", end="")
        print()

def printPiece(piece):
    match piece:
        case 0: print(colored(" ", "white"), end="")
        case 1: print(colored("1", "green"), end="")
        case 2: print(colored("2", "yellow"), end="")
        case 3: print(colored("3", "red"), end="")

def novoJogoPvP(gameData):
    gameData["playerNames"].append(input("Nome do jogador 1: "))
    gameData["playerNames"].append(input("Nome do jogador 2: "))
    gameData["turn"] = random.randint(0,1)
    print(f"O jogador", gameData["playerNames"][gameData["turn"]], "joga primeiro.")
    gameLoop(gameData)


def checkWin(gameData):
    return False

def checkAvailablePieces(gameData, play):
    counts = {
        0: 0,
        1: 0,
        2: 0,
        3: 0
    }

    testGameBoard = []
    for bl in gameData["board"]:
        testGameBoard.append(bl.copy())
    testGameBoard[int(play[0])-1][int(play[1])-1] += 1
    for i in range(3):
        for j in range(4):
            counts[testGameBoard[i][j]] += 1

    del counts[0]
    for i in counts.values():
        if i > 8:
            return False

    return True



def gameLoop(gameData):
    while not checkWin(gameData):
        clear()
        printBoard(gameData)
        while True:
            play = input("Jogador " + gameData["playerNames"][gameData["turn"]] + " (linha, coluna): ")

            if len(play) == 2 and play[0] in "123" and play[1] in "1234":
                if gameData["board"][int(play[0])-1][int(play[1])-1] == 3:
                    print("jogada inválida, não pode substituir uma peça vermelha")
                elif not checkAvailablePieces(gameData, play):
                    print("jogada inválida, não há peças disponíveis")
                else:
                    gameData["board"][int(play[0])-1][int(play[1])-1] += 1
                    break
            else:
                print("jogada inválida")
        gameData["turn"] = (gameData["turn"] + 1) % 2

mainMenu()