import sys, os
from datetime import datetime
from termcolor import colored
import logicaSemaforo as s
import time
import onlinePlay as o
import json

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def regras():
    clear()
    print("O objetivo deste jogo é ser o primeiro a conseguir uma linha de três peças da mesma cor na horizontal, vertical ou diagonal.")
    print("O jogo realiza-se num tabuleiro, inicialmente vazio, de 3x4. Em cada jogada, cada jogador realiza uma das seguintes ações:")
    print("-> Colocar uma peça verde num quadrado vazio;")
    print("-> Substituir uma peça verde por uma peça amarela;")
    print("-> Substituir uma peça amarela por uma peça vermelha.")
    print("-> Passar a vez.")
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
        case 1:
            clear()
            print("NOVO JOGO ----")
            print("1: Jogador contra jogador")
            print("2: Jogador contra computador")
            print("3: Jogar online")
            print("4: Voltar ao menu principal")
            escolha = int(input("\nEscolha uma opção: "))
            match escolha:
                case 1: novoJogoPvP()
                case 2: novoJogoPvB()
                case 3: playOnline()
                case 4: mainMenu()
                case _:
                    input("opção inválida, clique em qualquer tecla para voltar ao menu principal")
                    mainMenu()
        case 2: carregarJogo()
        case 3: regras()
        case 4: sys.exit()
        case _:
            input("opção inválida, clique em qualquer tecla para voltar ao menu principal")
            mainMenu()

with open("config.json", "r") as configFile:
    config = json.load(configFile)

ip = config["ip"]
port = config["port"]

def playOnline():
    print("A estabelecer ligação ao servidor...")
    websocket = o.mkWebSocket(ip, port)
    if websocket == False:
        print("Não foi possível estabelecer ligação ao servidor.")
    else:
        escolha = 0
        while escolha not in ["1", "2", "3", "4"]:
            clear()
            print("Conectado ao servidor " + "ws://"+ip+":"+port)
            print("JOGAR ONLINE ----")
            print("1: Criar um novo jogo")
            print("2: Entrar num jogo existente")
            print("3: Ver jogos públicos disponíveis")
            print("4: Voltar ao menu principal")
            escolha = input("\nEscolha uma opção: ")
            match escolha:
                case "1":
                    escolha = ""
                    public = False
                    while escolha not in [1, 2]:
                        escolha = int(input("Deseja criar um jogo público ou privado? [1/2]: "))
                        if escolha == 1:
                            public = True

                    name = input("Nome: ")
                    print("A criar novo jogo...")
                    response = o.newGame(name, None, public)
                    if response[0] == "newGameCreated":
                        print("criado jogo com ID", response[1])
                        gameID = response[1]
                        gameData = False
                        waiting = True
                        trycount = 10
                        while waiting and not gameData:
                            waiting, gameData = o.waitForGame(gameID, name, 0)
                            if waiting == "gameExists, ONEPLAYER" and trycount == 10:
                                print(gameID + ": à espera de outro jogador...")
                                trycount = 0
                            trycount += 1
                            if waiting == "Error":
                                print("ERRO!")
                            time.sleep(0.5)
                        if gameData:
                            gameLoop(gameData, localPlayer=0)
                    else:
                        print("Erro ao criar jogo:", response)

                case "2":
                    gameID = input("ID do jogo: ")
                    name = input("Nome: ")
                    print("A tentar entrar no jogo", gameID, "...")
                    gameData = False
                    waiting = True
                    while waiting and not gameData:
                        waiting, gameData = o.waitForGame(gameID, name, 1, None)
                        if waiting == "Error":
                            print("ERRO!")
                        time.sleep(0.5)
                    if gameData:
                        gameLoop(gameData, localPlayer=1)

                case "3":
                    print("A procurar jogos públicos...")
                    games = o.listGames()
                    validGameList = []
                    if games[0] == "openGames":
                        print("JOGOS DISPONÍVEIS ----")
                        for g in games[1]:
                            ggd = g[1]
                            gID = ggd["onlineGameID"]
                            gPlayer1 = ggd["playerNames"][0]
                            print(f"[{gID}] JOGO DE {gPlayer1}")
                            validGameList.append(gID)
                        print("--------------------")
                        escolha = ""
                        while escolha not in validGameList:
                            escolha = input("Escolha um jogo pelo seu ID (\"back\" para voltar): ")
                            if escolha == "back":
                                break
                            elif escolha in validGameList:
                                name = input("Nome: ")
                                print("A tentar entrar no jogo", escolha, "...")
                                gameData = False
                                waiting = True
                                while waiting and not gameData:
                                    waiting, gameData = o.waitForGame(escolha, name, 1, None)
                                    if waiting == "Error":
                                        print("ERRO!")
                                    time.sleep(0.5)
                                if gameData:
                                    gameLoop(gameData, localPlayer=1)
                                    quit()
                            else:
                                print("Escolha inválida!")
                    else:
                        print("Não foram encontrados jogos públicos.")


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

cores = ["light_blue", "light_magenta"]

def novoJogoPvP():
    player1 = input("Nome do " + colored("jogador 1", cores[0]) + ": ")
    player2 = input("Nome do " + colored("jogador 2", cores[1]) + ": ")
    gameData = s.initGameData(player1, player2)
    gameLoop(gameData)

def novoJogoPvB():
    gameData = s.initGameData("player", "computador", gameType="bot")
    gameLoop(gameData)

def carregarJogo():
    clear()
    print("CARREGAR JOGO ----")

    if os.path.exists("autosave.json"):
        print("Foi encontrado um jogo guardado automaticamente:")
        continuar = ""
        valid = False
        try:
            autosaved = s.loadAutoSave()
            print(f"Jogo autosave iniciado em {datetime.utcfromtimestamp(autosaved['startTime']).strftime('%Y-%m-%d %H:%M:%S')}")
            print("Jogadores:", autosaved["playerNames"][0], "contra", autosaved["playerNames"][1])
            if autosaved["ended"]:
                print("Jogo terminado em", datetime.utcfromtimestamp(autosaved["history"][-1][3]).strftime('%Y-%m-%d %H:%M:%S'), "com vitória de", autosaved["playerNames"][autosaved["turn"]])
            else:
                print("Jogo em curso, é a vez de", autosaved["playerNames"][autosaved["turn"]])
            printBoard(autosaved)
            valid = True
        except:
            print("Erro ao carregar o jogo guardado automaticamente; listanado jogos guardados manualmente.")
            continuar = "n"

        while valid and (continuar.lower() not in ["s", "n"]):
            continuar = input("Deseja continuar este jogo? [s/n]: ")

            if continuar.lower() == "s":
                gameLoop(autosaved)
                return
            elif continuar.lower() == "n":
                clear()
                print("CARREGAR JOGO ----")
            else:
                print("Escolha inválida!")

    games = s.loadGames()
    validGamesList = []
    for g in games:
        if "gameType" not in g:
            type = "local"
        else:
            type = g["gameType"]
        print(f"Jogo {type} {games.index(g)} iniciado em", datetime.utcfromtimestamp(g["startTime"]).strftime('%Y-%m-%d %H:%M:%S'))
        print("Jogadores:", g["playerNames"][0], "contra", g["playerNames"][1])
        if g["ended"]:
            print("Jogo terminado em", datetime.utcfromtimestamp(g["history"][-1][3]).strftime('%Y-%m-%d %H:%M:%S'), "com vitória de", g["playerNames"][g["turn"]])
        else:
            print("Jogo em curso, é a vez de", g["playerNames"][g["turn"]])

        printBoard(g)
        print("--------------------")
        validGamesList.append(games.index(g))

    while True:
        escolha = None
        while (escolha not in validGamesList) and (escolha not in [-1, "back"]):
            escolha = input("Escolha um jogo pelo seu número, ou escreva -1 para escolher o mais recente (\"back\" para voltar): ")
            if escolha == "back":
                mainMenu()
                return
            try:
                escolha = int(escolha)
            except:
                print("Escolha inválida!")
                continue

        if games[escolha]["ended"]:
            watchReplay = ""
            while (watchReplay.lower() not in ["s", "n"]):
                watchReplay = input("Este jogo já terminou, ver replay? [s/n]: ")

                if watchReplay.lower() == "s":
                    replayGame(games[escolha])
                    return
                elif watchReplay.lower() == "n":
                    continue
                else:
                    print("Escolha inválida!")

        else:
            gameLoop(games[escolha])
            return

def numToColor(num):
    match num:
        case 1: return "verde"
        case 2: return "amarela"
        case 3: return "vermelha"
        case _: return None

def printPlay(gameData, play):
    lastPlay = gameData["history"][play]
    if lastPlay[1] == "pass":
        print(colored(gameData["playerNames"][lastPlay[0]], cores[lastPlay[0]]), "passou a vez.")
        return

    outString = colored(gameData["playerNames"][lastPlay[0]], cores[lastPlay[0]]) + " jogou em " + lastPlay[1] + ", "
    beforeColor = numToColor(lastPlay[2][0])
    afterColor = numToColor(lastPlay[2][1])
    if beforeColor == None:
        outString += "colocando uma peça " + afterColor + "."
    else:
        outString += "substituindo uma peça " + beforeColor + " por uma peça " + afterColor + "."
    print(outString)

def printLastPlay(gameData, timeStamp = False):
    if gameData["history"] == []:
        if timeStamp:
            print(datetime.utcfromtimestamp(gameData["startTime"]).strftime('%Y-%m-%d %H:%M:%S'), end=": ")
        print(colored(gameData["playerNames"][gameData["turn"]], cores[gameData["turn"]]), "joga primeiro.")
    else:
        if timeStamp:
            print(datetime.utcfromtimestamp(gameData["history"][0][3]).strftime('%Y-%m-%d %H:%M:%S'), end=": ")
        print(colored(gameData["playerNames"][gameData["history"][0][0]], cores[gameData["history"][-1][0]]), "joga primeiro.")

    for i in gameData["history"]:
        if timeStamp:
            print(datetime.utcfromtimestamp(gameData["history"][gameData["history"].index(i)][3]).strftime('%Y-%m-%d %H:%M:%S'), end=": ")
        printPlay(gameData, gameData["history"].index(i))

    if gameData["ended"] == True:
        if timeStamp:
            print(datetime.utcfromtimestamp(gameData["history"][-1][3]).strftime('%Y-%m-%d %H:%M:%S'), end=": ")
        print(colored(gameData["playerNames"][gameData["history"][-1][0]], cores[gameData["turn"]]), "ganhou!")


inGame = True
def gameLoop(gameData, localPlayer=0):
    global inGame
    while (not s.checkWin(gameData)) and inGame:
        s.autoSave(gameData)
        clear()
        printLastPlay(gameData)
        printBoard(gameData)
        if gameData["gameType"] == "bot":
            if gameData["turn"] == 1:
                print("O computador está a pensar...")
                time.sleep(1)
                s.botPlay(gameData)
                continue
        elif gameData["gameType"] == "online":
            if gameData["turn"] != localPlayer:
                t = 10
                rGameData = False
                while not rGameData:
                    if t==10:
                        print("à espera da jogada adversária...")
                        t=0
                    rGameData = o.getPlay(gameData)
                    t+=1
                    time.sleep(0.5)
                continue

        while True:
            play = input("Jogador " + colored(gameData["playerNames"][gameData["turn"]], cores[gameData["turn"]]) +
                          " (linha, coluna / \"pass\" / \"sair\"): ")

            if play == "sair":
                s.saveGame(gameData)
                inGame = False
                break

            if play == "pass":
                s.play(gameData, play)

                if gameData["gameType"] == "online":
                    send = o.sendPlay(localPlayer, play, gameData)
                    if send == "ok":
                        print("jogada enviada com sucesso, continuando")
                        break
                    else:
                        print("erro ao enviar jogada")
                        print(send)
                        exit()

                break

            elif len(play) == 2 and play[0] in "123" and play[1] in "1234":
                if gameData["board"][int(play[0])-1][int(play[1])-1] == 3:
                    print("jogada inválida, não pode substituir uma peça vermelha")
                elif not s.checkAvailablePieces(gameData, play):
                    print("jogada inválida, não há peças disponíveis")
                else:
                    s.play(gameData, play)

                    if gameData["gameType"] == "online":
                        send = o.sendPlay(localPlayer, play, gameData)
                        if send == "ok":
                            print("jogada enviada com sucesso, continuando")
                            break
                        else:
                            print("erro ao enviar jogada")
                            print(send)
                            exit()

                    break
            else:
                print("jogada inválida")

    s.passarVez(gameData) # para voltar ao jogador que ganhou
    if inGame:
        s.saveGame(gameData)
        clear()
        printLastPlay(gameData)
        printBoard(gameData)
    else:
        print("Jogo guardado com sucesso.")

def replayGame(gameData):
    clear()
    print("Replay do jogo iniciado em", datetime.utcfromtimestamp(gameData["startTime"]).strftime('%Y-%m-%d %H:%M:%S'))
    print("Jogadores:", gameData["playerNames"][0], "contra", gameData["playerNames"][1])
    print("Board final:")
    printBoard(gameData)
    print("--------------------")
    for play in gameData["history"]:
        print(datetime.utcfromtimestamp(play[3]).strftime('%Y-%m-%d %H:%M:%S'), end=": ")
        printPlay(gameData, gameData["history"].index(play))
    escolha = ""
    while escolha.lower() not in ["s", "n"]:
        escolha = input("Deseja rever este jogo play-by-play? [s/n]: ")
        if escolha.lower() == "s":
            playCount = -1
            replay = s.initReplayEngine(gameData)
            while (playCount < len(gameData["history"]) and not s.checkWin(replay)):
                clear()
                printLastPlay(replay)
                printBoard(replay)
                print("--------------------")
                print("ESCOLHA 0 PARA PLAY ANTERIOR, ENTER PARA PLAY SEGUINTE, -1 PARA SAIR")
                avancar = " "
                while avancar not in ["-1", "0", ""]:
                    avancar = input()
                    if avancar == "":
                        playCount += 1
                        s.play(replay, gameData["history"][playCount][1])
                        s.passarVez(replay)
                        continue
                    elif avancar == "-1":
                        return
                    elif avancar == "0" and playCount > -1:
                        playCount -= 1
                        replay = s.reverseLastPlay(replay)
                    else:
                        print("Escolha inválida!")

            replay["turn"] = (replay["turn"] + 1) % 2 # para voltar ao jogador que ganhou
            clear()
            printPlay(replay, -1)
            print("Fim do jogo")
            printBoard(replay)
            print(replay["playerNames"][replay["turn"]], "ganhou!")
        elif escolha.lower() == "n":
            break
        else:
            print("Escolha inválida!")

mainMenu()
