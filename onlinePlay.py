import asyncio
from websockets.server import serve
from websockets.sync.client import connect
import logicaSemaforo as s
import json

def mkWebSocket(ip, port):
    try:
        with connect("ws://"+ip+":"+port) as websocket:
            websocket.send("semáforo")
            message = websocket.recv()
            if message == "semáforo indeed":
                return websocket
            else:
                return False
    except ConnectionRefusedError:
        return False


with open("config.json", "r") as configFile:
    config = json.load(configFile)

ip = config["ip"]
port = config["port"]

def newGame(name, avatar, public):
    with connect("ws://"+ip+":"+port) as ws:
        jsonS = json.dumps(("newGame", name, avatar, public))
        ws.send(jsonS)
        message = ws.recv()
        content = json.loads(message)
        if content[0] == "newGameCreated":
            return "newGameCreated", content[1]
        else:
            return "error", content

def waitForGame(gameID, name, playerNumber, avatar=None):
    with connect("ws://"+ip+":"+port) as ws:
        jsonS = json.dumps(("checkGame", gameID, name, playerNumber, avatar))
        ws.send(jsonS)
        message = ws.recv()
        content = json.loads(message)
        if content[0] == "gameExists, ONEPLAYER":
            return content[0], None
        elif content[0] == "gameExists, TWOPLAYERS":
            jsonS = json.dumps(("sendGameData", gameID))
            ws.send(jsonS)
            message = ws.recv()
            gameData = json.loads(message)
            return content[0], gameData
        elif content[0] == "gameExists, PLAYERADDED":
            print("jogo encontrado")
            return content[0], None
        elif content[0] == "gameDoesNotExist":
            print("jogo não encontrado")
            return "Error", None
        else:
            print("erro")
            return "Error", None

def listGames():
    with connect("ws://"+ip+":"+port) as ws:
        jsonS = json.dumps(("listGames",))
        ws.send(jsonS)
        message = ws.recv()
        content = json.loads(message)
        if content[0] == "openGames":
            return content[0], content[1]
        elif content[0] == "noOpenGames":
            return content[0], None
        else:
            return "Error", None

def sendPlay(player, play, gameData):
    with connect("ws://"+ip+":"+port) as ws:
        jsonS = json.dumps(("sendPlay", gameData["onlineGameID"], player, play, gameData))
        ws.send(jsonS)

        jsonS2 = json.dumps(("sendGameData", gameData["onlineGameID"]))
        ws.send(jsonS2)
        message = ws.recv()
        updatedData = json.loads(message)

        if updatedData["history"][-1][-1] == gameData["history"][-1][-1]:
            return "ok"
        else:
            return("jogada não aceite " + str(gameData) + str(updatedData))


def getPlay(gameData):
    gameID = gameData["onlineGameID"]
    with connect("ws://"+ip+":"+port) as ws:
        jsonS = json.dumps(("sendGameData", gameID))
        ws.send(jsonS)
        message = ws.recv()
        receivedGameData = json.loads(message)
        if len(receivedGameData["history"]) > len(gameData["history"]):
            gameData = s.play(gameData, receivedGameData["history"][-1][1])
            if gameData["board"] == receivedGameData["board"]:
                return receivedGameData
        else:
            return False