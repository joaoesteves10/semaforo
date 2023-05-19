import sys, os
from termcolor import colored
import logicaSemaforo as s

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
        case 1: novoJogoPvP() # implementar PvB e BvB depois
        case 2: carregarJogo() # ainda não implementado
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

def novoJogoPvP():
    player1 = input("Nome do jogador 1: ")
    player2 = input("Nome do jogador 2: ")
    gameData = s.initGameData(player1, player2)
    gameLoop(gameData)


def carregarJogo():
    gameData = s.loadGame()
    gameLoop(gameData)

def numToColor(num):
    match num:
        case 1: return "verde"
        case 2: return "amarela"
        case 3: return "vermelha"
        case _: return None

def printPlay(gameData, play):
    lastPlay = gameData["history"][play]
    outString = gameData["playerNames"][lastPlay[0]] + " jogou em " + lastPlay[1] + ", "
    beforeColor = numToColor(lastPlay[2][0])
    afterColor = numToColor(lastPlay[2][1])
    if beforeColor == None:
        outString += "colocando uma peça " + afterColor + "."
    else:
        outString += "substituindo uma peça " + beforeColor + " por uma peça " + afterColor + "."
    print(outString)

def printLastPlay(gameData):
    if gameData["history"] == []:
        print(gameData["playerNames"][gameData["turn"]], "joga primeiro.")
        return

    if len(gameData["history"]) > 1:
        printPlay(gameData, -2)

    printPlay(gameData, -1)
    return

inGame = True
def gameLoop(gameData):
    global inGame
    while (not s.checkWin(gameData)) and inGame:
        s.autoSave(gameData)
        clear()
        printLastPlay(gameData)
        printBoard(gameData)
        while True:

            play = input("Jogador " + gameData["playerNames"][gameData["turn"]] + " (linha, coluna): ")

            if play == "sair":
                s.saveGame(gameData)
                inGame = False
                break

            elif len(play) == 2 and play[0] in "123" and play[1] in "1234":
                if gameData["board"][int(play[0])-1][int(play[1])-1] == 3:
                    print("jogada inválida, não pode substituir uma peça vermelha")
                elif not s.checkAvailablePieces(gameData, play):
                    print("jogada inválida, não há peças disponíveis")
                else:
                    s.play(gameData, play)
                    break
            else:
                print("jogada inválida")
        gameData["turn"] = (gameData["turn"] + 1) % 2
    gameData["turn"] = (gameData["turn"] + 1) % 2 # para voltar ao jogador que ganhou
    if inGame:
        s.saveGame(gameData)
        clear()
        printPlay(gameData, -1)
        print("Fim do jogo")
        printBoard(gameData)
        print(gameData["playerNames"][gameData["turn"]], "ganhou!")
    else:
        print("Jogo guardado com sucesso.")
mainMenu()
