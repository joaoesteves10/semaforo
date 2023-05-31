import asyncio
from websockets.server import serve
import json
import logicaSemaforo as s
import random, string
import datetime

games = {}

def reloadGames():
    return games

async def echo(websocket):
    global games
    async for message in websocket:
        print("-------------------------------------------------")
        print(f"{message}")
        print("**********")
        print(games)

        if message == "semáforo":
            await websocket.send("semáforo indeed")
        else:
            jsonS = json.loads(message)

            if jsonS[0] == "newGame":
                gameID = get_random_string(6)
                gameData = s.initGameData(jsonS[1], "NOTYETAVAILABLE", jsonS[2], "NOTYETAVAILABLE", "online", gameID, jsonS[3])
                gameInfo = ([0], gameData, jsonS[3])
                games[gameID] = gameInfo
                jsonS = json.dumps(("newGameCreated", gameID))
                await websocket.send(jsonS)

            elif jsonS[0] == "sendGameData":
                games = reloadGames()
                gameID = jsonS[1]
                jsonS = json.dumps(games[gameID][1])
                await websocket.send(jsonS)

            elif jsonS[0] == "sendPlay":
                gameID = jsonS[1]
                player = jsonS[2]
                play = jsonS[3]
                gameData = games[gameID][1]
                receivedGameData = jsonS[4]
                if player == games[gameID][1]["turn"]:
                    gameData = s.play(gameData, play)
                    gameData["history"][-1] = (gameData["history"][-1][0], gameData["history"][-1][1], gameData["history"][-1][2], receivedGameData["history"][-1][3])
                    print(receivedGameData)
                    if gameData == receivedGameData:
                        games[gameID][1] = gameData

            elif jsonS[0] == "listGames":
                acum = []
                for e in games.values():
                    if e[2]:

                        startTime = datetime.datetime.fromtimestamp(e[1]["startTime"])
                        now = datetime.datetime.now()
                        timeElapsed = now - startTime

                        if not e[1]["ended"] and len(e[0]) == 1 and e[1] and timeElapsed < datetime.timedelta(minutes=5):
                            acum.append(e)

                if acum == []:
                    jsonS = json.dumps(("noOpenGames", None))
                else:
                    jsonS = json.dumps(("openGames", acum))
                await websocket.send(jsonS)

            elif jsonS[0] == "checkGame":
                gameID = jsonS[1]
                name = jsonS[2]
                playerNumber = jsonS[3]
                if gameID in games:
                    if playerNumber in games[gameID][0] and games[gameID][1]["playerNames"][playerNumber] == name:
                        if len(games[gameID][0]) == 2:
                            jsonS = json.dumps(("gameExists, TWOPLAYERS", games[gameID][1]))
                            await websocket.send(jsonS)
                        else:
                            jsonS = json.dumps(("gameExists, ONEPLAYER", None))
                            await websocket.send(jsonS)

                    else:
                        games[gameID][0].append(playerNumber)
                        games[gameID][1]["playerNames"][playerNumber] = name
                        games[gameID][1]["playerAvatars"][playerNumber] = jsonS[4]
                        jsonS = json.dumps(("gameExists, PLAYERADDED", None))
                        await websocket.send(jsonS)
                else:
                    jsonS = json.dumps(("gameDoesNotExist", None))
                    await websocket.send(jsonS)

def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

async def main():
    async with serve(echo, port=11816):
        print("listening on port 11816")
        await asyncio.Future()  # run forever

def storeGameData(gameID, gd):
    global games
    games[gameID][1] = gd

asyncio.run(main())