## módulo com a lógica para o jogo do semáforo
import random, json, os, time

def initGameData(player1, player2, avatar1=None, avatar2=None):
    return {
        "startTime": time.time(), # timestamp do início do jogo, usado para display nos saves
        "ended": False, # se o jogo já acabou, usado para display nos saves
        "playerNames": [player1, player2],
        "playerAvatars": [avatar1, avatar2], # será usado pela GUI, desnecessário para a lógica e CLI
        "turn": random.randint(0,1), # 0 = player1, 1 = player2
        "board": [[0,0,0,0],[0,0,0,0],[0,0,0,0]], # matriz, 0 = vazio, 1 = verde, 2 = amarelo, 3 = vermelho
        "history": [] # lista de tuplas (jogador, jogada, (peça antes, peça depois), timestamp)
    }

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


def passarVez(gameData):
    gameData["turn"] = (gameData["turn"] + 1) % 2

def checkWin(gameData):
    board = gameData["board"]

    if gameData["ended"]:
        return True

    for row in gameData["board"]:
        if row[0] == row[1] == row[2] != 0 or row[1] == row[2] == row[3] != 0:
            gameData["ended"] = True
            return True

    for col in range(4):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            gameData["ended"] = True
            return True

    if (board[0][0] == board[1][1] == board[2][2] != 0):
        gameData["ended"] = True
        return True
    if board[0][2] == board[1][1] == board[2][0] != 0:
        gameData["ended"] = True
        return True
    if board[0][1] == board[1][2] == board[2][3] != 0:
        gameData["ended"] = True
        return True
    if board[0][3] == board[1][2] == board[2][1] != 0:
        gameData["ended"] = True
        return True

    return False

def play(gameData, play):
    player = gameData["turn"]
    if play == "pass":
        gameData["history"].append((player, play, (None, None), time.time()))
        passarVez(gameData)
        return gameData

    beforeValue = gameData["board"][int(play[0])-1][int(play[1])-1]
    gameData["board"][int(play[0])-1][int(play[1])-1] += 1
    afterValue = gameData["board"][int(play[0])-1][int(play[1])-1]
    gameData["history"].append((player, play, (beforeValue, afterValue), time.time()))

    return gameData

def saveGame(gameData):
    games = []
    if os.path.exists("save.json"):
        with open("save.json", "r") as saveFile:
            games = json.load(saveFile)
    games.append(gameData)
    with open("save.json", "w") as saveFile:
        json.dump(games, saveFile)

    if os.path.exists("autosave.json"):
        os.remove("autosave.json") # já não é necessário termos o autosave

def autoSave(gameData):
    with open("autosave.json", "w") as saveFile:
        json.dump(gameData, saveFile)

def loadGames():
    with open("save.json", "r") as saveFile:
        return json.load(saveFile)

def loadAutoSave():
    with open("autosave.json", "r") as saveFile:
        return json.load(saveFile)