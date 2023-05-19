## módulo com a lógica para o jogo do semáforo
import random, json

def initGameData(player1, player2):
    return {
        "playerNames": [player1, player2],
        "turn": random.randint(0,1),
        "board": [[0,0,0,0],[0,0,0,0],[0,0,0,0]],
        "history": [] # lista de tuplas (jogador, jogada, (peça antes, peça depois))
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

    for row in gameData["board"]:
        if row[0] == row[1] == row[2] != 0:
            return True

    for col in range(4):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            return True

    if board[0][0] == board[1][1] == board[2][2] != 0:
        return True
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return True
    if board[0][1] == board[1][2] == board[2][3] != 0:
        return True
    if board[0][3] == board[1][2] == board[2][1] != 0:
        return True

    return False

def play(gameData, play):
    beforeValue = gameData["board"][int(play[0])-1][int(play[1])-1]
    gameData["board"][int(play[0])-1][int(play[1])-1] += 1
    afterValue = gameData["board"][int(play[0])-1][int(play[1])-1]
    player = gameData["turn"]
    gameData["history"].append((player, play, (beforeValue, afterValue)))

    return gameData

def saveGame(gameData):
    with open("save.json", "w") as saveFile:
        json.dump(gameData, saveFile)

def loadGame():
    with open("save.json", "r") as saveFile:
        return json.load(saveFile)