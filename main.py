import pygame
import logicaSemaforo as s
import ctypes
import os
import json
import onlinePlay as o
import time

ctypes.windll.user32.SetProcessDPIAware()


pygame.font.init()
boolValonline = 0
boolValbot = 0


assets = {
    "pt": {
        "buttons": pygame.image.load("./assets/pt/TitleButtons.png"),
        "skip": pygame.image.load("./assets/pt/skip.png"),
        "save": pygame.image.load("./assets/pt/Billboard.pt-BR.png"),
        "cursors": pygame.image.load("./assets/pt/Cursors.png"),
        "tot1": pygame.image.load("./assets/pt/tot1.png"),
        "tot2": pygame.image.load("./assets/pt/tot2.png"),
        "tot3": pygame.image.load("./assets/pt/tot3.png"),
        "tot4": pygame.image.load("./assets/pt/tot4.png"),
        "tot5": pygame.image.load("./assets/pt/tot5.png"),
        "tot6": pygame.image.load("./assets/pt/tot6.png"),
    },
    "en": {
        "buttons": pygame.image.load("./assets/en/TitleButtons.png"),
        "skip": pygame.image.load("./assets/en/skip.png"),
        "save": pygame.image.load("./assets/en/Billboard.png"),
        "cursors": pygame.image.load("./assets/en/Cursors.png"),
        "tot1": pygame.image.load("./assets/en/tot1.png"),
        "tot2": pygame.image.load("./assets/en/tot2.png"),
        "tot3": pygame.image.load("./assets/en/tot3.png"),
        "tot4": pygame.image.load("./assets/en/tot4.png"),
        "tot5": pygame.image.load("./assets/en/tot5.png"),
        "tot6": pygame.image.load("./assets/en/tot6.png"),
    },
    "tabuleiro": pygame.image.load("./assets/global/tabuleiro.png"),
    "tabuleiro2": pygame.image.load("./assets/global/tabuleiro2.png"),
    "online": pygame.image.load("./assets/global/online.png"),
    "win": pygame.image.load("./assets/global/win.png"),
    "cursors2": pygame.image.load("./assets/global/Cursors.png"),
    "logo": pygame.image.load("./assets/global/novalogo2.png"),
    "clouds": pygame.image.load("./assets/global/Clouds.png"),
    "background": pygame.image.load("./assets/global/stardewPanorama.png"),
    "specialOrdersBoard": pygame.image.load("./assets/global/SpecialOrdersBoard.png"),
    "welcomeToTheMato": "./assets/music/welcomeToTheMato.mp3",
    "click": "./assets/sounds/click.mp3",
    "crops": pygame.image.load("./assets/global/crops.png"),
    "font": "./assets/fonts/Stardew_Valley.ttf"
}

font = pygame.font.Font(assets["font"], 30)


with open("./assets/textos.json", encoding="UTF-8") as f:
    textos = json.load(f)

class Button(object):
    def __init__(self, position, size, image, image_hover=None, image_down=None):

        self.image = image

        if image_hover is None:
            self.image_hover = image
        else:
            self.image_hover = image_hover

        if image_down is None:
            self.image_down = image
        else:
            self.image_down = image_down

        self.rect = pygame.Rect(position, size)

    def draw(self, screen):
        screen.blit(self.image[0], self.rect, self.image[1])

    def is_hovered(self, event, noHover=False):
        if event.type == pygame.MOUSEMOTION and not noHover:
            if self.rect.collidepoint(event.pos):
                screen.blit(self.image_hover[0], self.rect, self.image_hover[1])
            else:
                screen.blit(self.image[0], self.rect, self.image[1])

    def is_clicked(self, event, noHover=False):
        self.is_hovered(event, noHover)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickSound = pygame.mixer.Sound(assets["click"])
            pygame.mixer.Sound.set_volume(clickSound, 0.2)
            pygame.mixer.Sound.play(clickSound)
            if event.button == 1:
                # como não estamos a usar isto em nenhum vamos comentar p/ evitar load desnecessário
                # screen.blit(self.image_down[0], self.rect, self.image_down[1])
                return self.rect.collidepoint(event.pos)


class boolButton(object):
    def __init__(self, position, size, image, posON, posOFF, backgroundColor):

            self.size = size
            self.position = position
            self.rect = pygame.Rect(position, size)
            self.image = image
            self.ipos = [posOFF, posON]
            self.backgroundColor = backgroundColor

    def draw(self, screen, boolVal):
        screen.fill(self.backgroundColor, self.rect)
        if boolVal:
            screen.blit(self.image, self.rect, self.ipos[1])
        else:
            screen.blit(self.image, self.rect, self.ipos[0])

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)

class boardButton(object):
    def __init__(self, position, piece):

        size = (40 * 6, 40 * 6)
        self.position = position
        self.tabuleiro = pygame.transform.scale_by(assets["tabuleiro"], 6)
        self.crops = pygame.transform.scale_by(assets["crops"], 3.6)
        self.cropsP = [None, (208 * 3.6, 518 * 3.6, 48 * 3.6, 53 * 3.6), (112 * 3.6, 525 * 3.6, 48 * 3.6, 53 * 3.6), (162 * 3.6, 518 * 3.6, 44 * 3.6, 53 * 3.6)]
        self.rect = pygame.Rect(position, size)
        self.piece = piece

    def draw(self, screen):
        screen.blit(self.tabuleiro, self.rect, (534 * 6, 18 * 6, 40 * 6, 40 * 6),)
        if self.piece != 0:
            screen.blit(self.crops, (self.position[0]+32, self.position[1]+26, 40*6, 40*6), self.cropsP[self.piece])

    def is_hovered(self, event, noHover=False):
        if event.type == pygame.MOUSEMOTION and not noHover:
            if self.rect.collidepoint(event.pos):
                pass
                #screen.blit(self.image_hover[0], self.rect, self.image_hover[1])
            else:
                pass
                #screen.blit(self.image[0], self.rect, self.image[1])

    def is_clicked(self, event, noHover=False):
        self.is_hovered(event, noHover)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickSound = pygame.mixer.Sound(assets["click"])
            pygame.mixer.Sound.set_volume(clickSound, 0.2)
            pygame.mixer.Sound.play(clickSound)
            if event.button == 1:
                # como não estamos a usar isto em nenhum vamos comentar p/ evitar load desnecessário
                # screen.blit(self.image_down[0], self.rect, self.image_down[1])
                return self.rect.collidepoint(event.pos)

class characterSelectButton(object):

    def __init__(self, position, image, name, size=(64 * 1.3 , 64 * 1.3), image_hover=None, image_down=None, avatarPos=(1308, 132), avatarCoords=(0 , 0, 64 * 3, 64 * 3), iconCoords=(0, 0, 64 * 1.3, 64 * 1.3)):
        self.image = image

        if image_hover is None:
            self.image_hover = image
        else:
            self.image_hover = image_hover

        if image_down is None:
            self.image_down = image
        else:
            self.image_down = image_down

        self.rect = pygame.Rect(position, size)
        self.iconCoords = iconCoords
        self.avatarCoords = avatarCoords
        self.avatarPos = avatarPos
        self.imgScaled13 = pygame.transform.scale_by(image, 1.3)
        self.imgScaled3 = pygame.transform.scale_by(image, 3)
        self.image_hover = pygame.transform.scale_by(self.image_hover, 1.3)
        self.image_down = pygame.transform.scale_by(self.image_down, 1.3)
        self.name = name

    def draw(self, screen):
        screen.blit(self.imgScaled13, self.rect, self.iconCoords)

    def drawAvi(self, screen):
        screen.fill(0xfab05a, (1308, 132, 58 * 3.2 + 7, 58 * 3.2 + 7))
        screen.blit(self.image_hover, self.rect, self.iconCoords)
        screen.blit(self.imgScaled3, self.avatarPos, self.avatarCoords)

    def is_hovered(self, event, noHover=False):
        if event.type == pygame.MOUSEMOTION and not noHover:
            if self.rect.collidepoint(event.pos):
                screen.fill(0xfab05a, (1308, 132, 58 * 3.2 + 7, 58 * 3.2 + 7))
                # screen.blit(self.image_hover, self.rect, self.iconCoords)
                screen.blit(self.imgScaled3, self.avatarPos, self.avatarCoords)
            #    screen.blit(self.imgScaled13, self.rect, self.iconCoords)

    def is_clicked(self, event, noHover=False):
        self.is_hovered(event, noHover)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickSound = pygame.mixer.Sound(assets["click"])
            pygame.mixer.Sound.set_volume(clickSound, 0.2)
            pygame.mixer.Sound.play(clickSound)
            if event.button == 1:
                # screen.blit(self.image_down, self.rect, self.iconCoords)
                return self.rect.collidepoint(event.pos)


pygame.init()

lang = "pt"
FPS = 144

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Semáforo")
pygame_icon = assets["logo"]
pygame.display.set_icon(pygame_icon)
n = 1

cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3*(2147/1920))

pygame.mixer.music.load(assets["welcomeToTheMato"])
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(0)
muteButtonAsset = {
    "muted": (137 * 3*(2147/1920)+1, 384 * 3*(2147/1920), 9 * 3*(2147/1920), 8 * 3*(2147/1920)),
    "unmuted": (128 * 3*(2147/1920), 384 * 3*(2147/1920), 9 * 3*(2147/1920), 8 * 3*(2147/1920)),
}
muteButton = Button((20, 20), # posição
                    (9 * 3*(2147/1920), 8 * 3*(2147/1920)), # tamanho
                    (cursors, muteButtonAsset["unmuted"]), # imagem default
)
def toggleMusic():
    global muteButton
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        muteStatus = "muted"
    else:
        pygame.mixer.music.unpause()
        muteStatus = "unmuted"
    screen.fill(0x93bcf8, (20, 20, 9 * 3*(2147/1920), 8 * 3*(2147/1920)))
    muteButton = Button((20, 20), # posição
                    (9 * 3*(2147/1920), 8 * 3*(2147/1920)), # tamanho
                    (cursors, muteButtonAsset[muteStatus]), # imagem default
    )
    muteButton.draw(screen)

def menuPrincipal(running=True):
    global lang
    global boolValbot
    global boolValonline
    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))

    bgImage = pygame.transform.scale_by(assets["background"], 3*(2147/1920))
    screen.blit(bgImage, (0, -250))

    clouds = pygame.transform.scale_by(assets["clouds"], 2*(2147/1920))
    screen.blit(clouds, (100, 200), (0*2*(2147/1920), 470*2*(2147/1920) , 150*2*(2147/1920), 80*2*(2147/1920)))
    screen.blit(clouds, (1700, 200), (150*2*(2147/1920), 430*2*(2147/1920) , 150*2*(2147/1920), 80*2*(2147/1920)))
    screen.blit(clouds, (1450, 400), (400*2*(2147/1920), 465*2*(2147/1920) , 140*2*(2147/1920), 70*2*(2147/1920)))

    logo = pygame.transform.scale_by(assets["logo"], 490/200)
    screen.blit(logo, (370, 120))

    muteButton.draw(screen)

    newGameButton = Button((481, 650), # posição
                        (74 *2.5*(2147/1920), 58 *2.5*(2147/1920)), # tamanho
                        (buttons, (0 *2.5*(2147/1920), 245 *2.5*(2147/1920) - 58 *2.5*(2147/1920), 74 *2.5*(2170/1920), 58 *2.5*(2170/1920))), # imagem default
                        (buttons, (0 *2.5*(2147/1920), 245 *2.5*(2147/1920), 74 *2.5*(2165/1920), 58 *2.5*(2165/1920))), # imagem hover
    )
    newGameButton.draw(screen)

    loadGameButton = Button((731, 650), # posição
                        (74 *2.5*(2147/1920), 58 *2.5*(2147/1920)), # tamanho
                        (buttons, (74 *2.5*(2147/1920), 245 *2.5*(2147/1920) - 58 *2.5*(2147/1920), 74 *2.5*(2165/1920), 58 *2.5*(2165/1920))), # imagem default
                        (buttons, (74 *2.5*(2147/1920), 245 *2.5*(2147/1920), 74 *2.5*(2165/1920), 58 *2.5*(2165/1920))), # imagem hover
    )
    loadGameButton.draw(screen)

    rulesButton = Button((981, 650), # posição
                        (74 *2.5*(2147/1920), 58 *2.5*(2147/1920)), # tamanho
                        (buttons, (148 *2.5*(2147/1920), 245 *2.5*(2147/1920) - 58 *2.5*(2147/1920), 74 *2.5*(2165/1920), 58 *2.5*(2165/1920))), # imagem default
                        (buttons, (148 *2.5*(2147/1920), 245 *2.5*(2147/1920), 74 *2.5*(2165/1920), 58 *2.5*(2165/1920))), # imagem hover
    )
    rulesButton.draw(screen)

    quitButton = Button((1231, 650), # posição
                        (74 *2.5*(2147/1920), 58 *2.5*(2147/1920)), # tamanho
                        (buttons, (222 *2.5*(2147/1920), 245 *2.5*(2147/1920) - 58 *2.5*(2147/1920), 74 *2.5*(2165/1920), 58 *2.5*(2165/1920))), # imagem default
                        (buttons, (222 *2.5*(2147/1920), 245 *2.5*(2147/1920), 74 *2.5*(2165/1920), 58 *2.5*(2165/1920))), # imagem hover
    )
    quitButton.draw(screen)

    creditsButton = Button((1785, 1011), # posição
                        (22 *2.5*(2147/1920), 25 *2.5*(2147/1920)), # tamanho
                        (buttons, (8 *2.5*(2147/1920), 458 *2.5*(2147/1920), 22 *2.5*(2147/1920), 25 *2.5*(2147/1920))), # imagem default
                        (buttons, (8 *2.5*(2147/1920) + 22 *2.5*(2147/1920), 458 *2.5*(2147/1920), 22 *2.5*(2147/1920), 25 *2.5*(2147/1920))), # imagem hover
    )
    creditsButton.draw(screen)

    languageButton = Button((1845, 1011), # posição
                        (27 *2.5*(2147/1920), 25 *2.5*(2147/1920)), # tamanho
                        (buttons, (52 *2.5*(2147/1920), 458 *2.5*(2147/1920), 27 *2.5*(2147/1920), 25 *2.5*(2147/1920))), # imagem default
                        (buttons, (52 *2.5*(2147/1920) + 27 *2.5*(2147/1920), 458 *2.5*(2147/1920), 27 *2.5*(2147/1920), 25 *2.5*(2147/1920))), # imagem hover
    )
    languageButton.draw(screen)

    clock = pygame.time.Clock()

    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if muteButton.is_clicked(ev):
                toggleMusic()

            if quitButton.is_clicked(ev):
                pygame.quit()
                exit()

            if newGameButton.is_clicked(ev):
                player0name, player0avatar = NomePersonagem(1, 0)
                if boolValonline == 1:
                    MenuOnline(player0name, player0avatar)
                player1name, player1avatar = NomePersonagem(1, 1)
                if boolValbot == 1:
                    gameData = s.initGameData(player0name, "Bot", player0avatar, "Krobus", "bot")
                else:
                    gameData = s.initGameData(player0name, player1name, player0avatar, player1avatar)
                print(gameData)
                while not s.checkWin(gameData):
                    s.autoSave(gameData)

                    if boolValbot == 1:
                        if gameData["gameType"] == "bot" and gameData["turn"] == 1:
                            mostrarBoard(gameData, False)
                            pygame.display.flip()
                            time.sleep(0.5)
                            s.botPlay(gameData)
                            continue

                    mostrarBoard(gameData)
                win(gameData)

            if loadGameButton.is_clicked(ev):
                saves()
                menuPrincipal(False)

            if rulesButton.is_clicked(ev):
                for i in range(1, 7):
                    Tutorial(i)
                menuPrincipal(False)

            if creditsButton.is_clicked(ev):
                SettingseCredits()
                menuPrincipal(False)

            if languageButton.is_clicked(ev):
                lang = "en" if lang == "pt" else "pt"
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def saves(running = True):
    global lang
    soBoard = pygame.transform.scale_by(assets[lang]["save"], 4.5)
    screen.blit(soBoard, (202, 100), (0, 0, 337*4.5, 197*4.5))


    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 5)
    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))

    saves = s.loadGames()

    if os.path.exists("autosave.json"):
        save1 = s.loadAutoSave()
        save2 = saves[-1] if len(saves) >= 1 else None
        save3 = saves[-2] if len(saves) >= 2 else None
    else:
        if len(saves) >= 1:
            save1 = saves[-1]
        if len(saves) >= 2:
            save2 = saves[-2]
        if len(saves) >= 3:
            save3 = saves[-3]

    save1B = Button((575, 380), # posição
                        (48 * 5, 67 * 5), # tamanho
                        (cursors, (511 * 5, 398 * 5, 48 * 5, 67 * 5)), # imagem default
    )
    save1B.draw(screen)

    save2B = Button((850, 270), # posição
                        (48 * 5, 67 * 5), # tamanho
                        (cursors, (511 * 5, 398 * 5, 48 * 5, 67 * 5)), # imagem default
    )
    save2B.draw(screen)

    save3B = Button((1125, 460), # posição
                        (48 * 5, 67 * 5), # tamanho
                        (cursors, (511 * 5, 398 * 5, 48 * 5, 67 * 5)), # imagem default
    )
    save3B.draw(screen)


    buttonback = Button((1755, 1005),  # posição
                   (66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920)),  # tamanho
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920), 66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),  # imagem default
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920)+27 * 2.5*(2147/1920),66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),
                   )
    buttonback.draw(screen)

    muteButton.draw(screen)

    clock = pygame.time.Clock()

    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if save1B.is_clicked(ev):
                gameData = save1
                while not s.checkWin(gameData):
                    s.autoSave(gameData)
                    mostrarBoard(gameData)
                win(gameData)


            if save2B.is_clicked(ev):
                gameData = save2
                while not s.checkWin(gameData):
                    s.autoSave(gameData)
                    mostrarBoard(gameData)
                win(gameData)

            if save3B.is_clicked(ev):
                gameData = save3
                while not s.checkWin(gameData):
                    s.autoSave(gameData)
                    mostrarBoard(gameData)
                win(gameData)

            if muteButton.is_clicked(ev):
                toggleMusic()

            if buttonback.is_clicked(ev):
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def Metercodigo(player1name, player1avatar, running = True):
    global lang
    soBoard = pygame.transform.scale_by(assets["specialOrdersBoard"], 5)
    screen.blit(soBoard, (592, 0), (513*5, 13*5, 147*5, 175*5))
    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))

    buttonback = Button((1755, 1005),  # posição
                   (66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920)),  # tamanho
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920), 66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),  # imagem default
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920)+27 * 2.5*(2147/1920),66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),
                   )
    buttonback.draw(screen)

    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3)

    exitB = Button((1884, -3),  # posição
                   (12 * 3, 12 * 3),  # tamanho
                   (cursors, (337 * 3, 493 * 3, 12 * 3, 12 * 3),  # imagem default
                   ))
    exitB.draw(screen)


    clock = pygame.time.Clock()

    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if exitB.is_clicked(ev):
                pygame.quit()
                exit()

            if buttonback.is_clicked(ev):
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def EncontarJogo(playername, playeravatar, running = True):
    global lang
    soBoard = pygame.transform.scale_by(assets["specialOrdersBoard"], 5)
    screen.blit(soBoard, (592, 0), (352*5, 14*5, 147*5, 168*5))
    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))

    buttonback = Button((1755, 1005),  # posição
                   (66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920)),  # tamanho
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920), 66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),  # imagem default
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920)+27 * 2.5*(2147/1920),66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),
                   )
    buttonback.draw(screen)

    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3)

    exitB = Button((1884, -3),  # posição
                   (12 * 3, 12 * 3),  # tamanho
                   (cursors, (337 * 3, 493 * 3, 12 * 3, 12 * 3),  # imagem default
                   ))
    exitB.draw(screen)

    clock = pygame.time.Clock()

    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if exitB.is_clicked(ev):
                pygame.quit()
                exit()

            if buttonback.is_clicked(ev):
                running = False

        pygame.display.flip()
        clock.tick(FPS)
def SettingseCredits(running = True):
    global lang
    soBoard = pygame.transform.scale_by(assets["specialOrdersBoard"], 4.5)
    screen.blit(soBoard, (202, 100), (0, 0, 337*4.5, 197*4.5))
    font = pygame.font.Font(assets["font"], 30)
    renderTextCenteredAt(textos[lang]["creditos"], font,(86,22,12),2040,240,screen,600)


    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))

    buttonback = Button((1755, 1005),  # posição
                   (66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920)),  # tamanho
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920), 66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),  # imagem default
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920)+27 * 2.5*(2147/1920),66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),
                   )
    buttonback.draw(screen)

    muteButton.draw(screen)

    clock = pygame.time.Clock()

    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if muteButton.is_clicked(ev):
                toggleMusic()

            if buttonback.is_clicked(ev):
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def importCharacters():
    characters = []
    chars = os.listdir("./assets/global/Portraits/")
    for c in chars:
        if c.split(".")[1] == "png":
            characters.append((c.split(".")[0], pygame.image.load("./assets/global/Portraits/" + c)))
    return characters

characters = importCharacters()

def NomePersonagem(running = True, char=0):
    global boolValbot
    global boolValonline

    global lang
    tabuleiro = pygame.transform.scale_by(assets["tabuleiro"], 6)
    screen.blit(tabuleiro, (0, 0), (320 * 6, 0, 320*6, 180*6))
    font = pygame.font.Font(assets["font"], 60)

    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))
    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 2*(2147/1920))


    input_box = pygame.Rect(1200, 800, 500, 200)
    color_inactive = pygame.Color((86,22,12))
    color_active = pygame.Color((86,22,12))
    color = color_inactive
    active = False
    text = ''

    ok = Button((1330, 380),  # posição
                   (65 * 2*(2147/1920), 65 * 2*(2147/1920)),  # tamanho
                   (cursors, (127 * 2*(2147/1920), 255 * 2*(2147/1920), 65 * 2*(2147/1920), 65 * 2*(2147/1920))),  # imagem default
                   (cursors, (127 * 2*(2147/1920), 255 * 2*(2147/1920), 65 * 2*(2147/1920), 65 * 2*(2147/1920))),
                   )
    ok.draw(screen)

    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 4)

    if (char ==1):
        renderTextCenteredAt(textos[lang]["player2"], font,(86,22,12),2550,725,screen,600)

        renderTextCenteredAt("Bot", font,(86,22,12),2800,568,screen,600)
        bot = boolButton((1360, 580),
                   (9 * 4, 9 * 4),
                   (cursors),
                   (236 * 4, 425 * 4, 9 * 4, 9 * 4),
                   (227 * 4, 425 * 4, 9 * 4, 9 * 4),
                   "0xfadc97"
                   )
        bot.draw(screen, boolValbot)

    else:
        renderTextCenteredAt(textos[lang]["player1"], font,(86,22,12),2550,725,screen,600)

        renderTextCenteredAt("Online", font,(86,22,12),2700,568,screen,600)
        online = boolButton((1310, 580),
                   (9 * 4, 9 * 4),
                   (cursors),
                   (236 * 4, 425 * 4, 9 * 4, 9 * 4),
                   (227 * 4, 425 * 4, 9 * 4, 9 * 4),
                   "0xfadc97"
                   )
        online.draw(screen, boolValbot)


    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3)

    avis = []

    exitB = Button((1884, -3),  # posição
                   (12 * 3, 12 * 3),  # tamanho
                   (cursors, (337 * 3, 493 * 3, 12 * 3, 12 * 3),  # imagem default
                   ))
    exitB.draw(screen)

    yy = 217
    cc = 0
    while yy < 217+108*6 and cc < len(characters):
        xx = 191
        while xx < 191+108*6 and cc < len(characters):
            avis.append(characterSelectButton((xx, yy), characters[cc][1], characters[cc][0]))
            cc += 1
            xx += 110
        yy += 111.5


    for a in avis:
        a.draw(screen)

    screen.fill(0xfab05a, (1308, 132, 58 * 3.2 + 7, 58 * 3.2 + 7))

    clock = pygame.time.Clock()

    clicked = None
    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if exitB.is_clicked(ev):
                pygame.quit()
                exit()

            if (char == 1):
                if bot.is_clicked(ev):
                    if boolValbot == 1:
                        boolValbot = 0
                    else:
                        boolValbot = 1
                    bot.draw(screen, boolValbot)

            if (char == 0):
                if online.is_clicked(ev):
                    if boolValonline == 1:
                        boolValonline = 0
                    else:
                        boolValonline = 1
                    online.draw(screen, boolValonline)

            if ok.is_clicked(ev):
                return text, clicked
                running=False

            if clicked == None:
                for a in avis:
                    if a.is_clicked(ev, noHover=False):
                        clicked = a.name
            else:
                for a in avis:
                    if a.name == clicked:
                        a.drawAvi(screen)
                    if a.is_clicked(ev, noHover=True):
                        clicked = a.name
                        a.drawAvi(screen)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(ev.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if ev.type == pygame.KEYDOWN:
                if active:
                    if ev.key == pygame.K_RETURN:
                        print(text)
                        text = ''
                    elif ev.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += ev.unicode

        txt_surface = font.render(text, False, color)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.display.flip()
        clock.tick(FPS)

def mostrarBoard(gameData, running = True):
    global lang

    charAvis = [None, None]
    for c in characters:
        if c[0] == gameData["playerAvatars"][0]:
            charAvis[0] = pygame.transform.scale_by(c[1], 4)
        if c[0] == gameData["playerAvatars"][1]:
            charAvis[1] = pygame.transform.scale_by(c[1], 4)

    tabuleiro2 = pygame.transform.scale_by(assets["tabuleiro2"], 6)
    screen.blit(tabuleiro2, (0, 0), (0 , 0, 320*6, 180*6))

    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 4)
    screen.blit(cursors, (1370, 112), (588 * 4 , 413 * 4, 320 * 4, 100 * 4))

    if gameData["turn"] == 0:

        screen.blit(charAvis[0], (1450, 136), (0, 0, 64 * 4, 64 * 4))

        f = pygame.font.Font(assets["font"], 60)
        texto1 = f.render(gameData["playerNames"][0], False, (88, 12, 22))
        fw1, _ = f.size(gameData["playerNames"][0])
        tx1 = 1564 - fw1 / 2

        screen.blit(texto1, (tx1, 422))

    else:
        screen.blit(charAvis[1], (1450, 136), (0, 0, 64 * 4, 64 * 4))

        f = pygame.font.Font(assets["font"], 60)
        texto2 = f.render(gameData["playerNames"][1], False, (88, 12, 22))
        fw2, _ = font.size(gameData["playerNames"][1])
        tx2 = 1564 - fw2 / 2

        screen.blit(texto2, (tx2, 422))

    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3)


    exitB = Button((1884, -3),  # posição
                   (12 * 3, 12 * 3),  # tamanho
                   (cursors, (337 * 3, 493 * 3, 12 * 3, 12 * 3),  # imagem default
                   ))
    exitB.draw(screen)


    bb = [[None, None, None, None], [None, None, None, None], [None, None, None, None]]

    yy = 150
    for l in range(3):
        xx = 186
        for c in range(4):
            bb[l][c] = boardButton((xx, yy), gameData["board"][l][c])
            bb[l][c].draw(screen)
            xx += 270
        yy += 270

    skip = pygame.transform.scale_by(assets[lang]["skip"], 1)

    skip = Button((842, 966),  # posição
                   (59 * 4 , 27 * 4 ),  # tamanho
                   (skip, (0, 0,  60 * 4 , 27 * 4)),  # imagem default
                   )
    skip.draw(screen)

    last15plays = gameData["history"][-15:]
    texto = ""
    for play in last15plays:
        texto += (gameData["playerNames"][play[0]] + " jogou " + play[1] + "\n")

    f = pygame.font.Font(assets["font"], 30)
    renderTextCenteredAt(texto, f, (88, 12, 22), 1564, 600, screen, 600)

    clock = pygame.time.Clock()

    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if exitB.is_clicked(ev):
                pygame.quit()
                exit()

            if skip.is_clicked(ev):
                s.play(gameData, "pass")
                running = False

            for linha in bb:
                for b in linha:
                    if b.is_clicked(ev, noHover=True):
                        l = bb.index(linha) + 1
                        c = linha.index(b) + 1
                        print("clicked")
                        print(l, c)
                        if gameData["board"][l-1][c-1] < 3:
                            if s.checkAvailablePieces(gameData, (l, c)):
                                s.play(gameData, str(l) + str(c))
                                print(gameData["board"])
                                running = False
        pygame.display.flip()
        clock.tick(FPS)

def MenuOnline(playername1, playeravatar1 ,running=True):

    online = pygame.transform.scale_by(assets["online"], 3)
    screen.blit(online, (0, 0), (0, 0, 640*3, 360*3))

    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3)

    exitB = Button((1884, -3),  # posição
                   (12 * 3, 12 * 3),  # tamanho
                   (cursors, (337 * 3, 493 * 3, 12 * 3, 12 * 3),  # imagem default
                   ))
    exitB.draw(screen)

    cursors = pygame.transform.scale_by(assets["cursors2"], 6)


    Criar = Button((410, 700),  # posição
                   (50 * 6, 31 * 6),  # tamanho
                   (cursors, (461 * 6, 1875 * 6, 50 * 6, 31 * 6),  # imagem default
                   ))
    Criar.draw(screen)

    Entrar = Button((810, 700),  # posição
                   (50 * 6, 31 * 6),  # tamanho
                   (cursors, (461 * 6, 1875 * 6, 50 * 6, 31 * 6),  # imagem default
                   ))
    Entrar.draw(screen)

    Ver = Button((1210, 700),  # posição
                   (50 * 6, 31 * 6),  # tamanho
                   (cursors, (461 * 6, 1875 * 6, 50 * 6, 31 * 6),  # imagem default
                   ))
    Ver.draw(screen)

    f = pygame.font.Font(assets["font"], 50)
    renderTextCenteredAt(textos[lang]["online1"], f, (255, 215, 137), 940, 770, screen, 600)
    renderTextCenteredAt(textos[lang]["online2"], f, (255, 215, 137), 1700, 770, screen, 600)
    renderTextCenteredAt(textos[lang]["online3"], f, (255, 215, 137), 2480, 770, screen, 600)

    pygame.display.flip()

    clock = pygame.time.Clock()
    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if exitB.is_clicked(ev):
                pygame.quit()
                exit()

            if Criar.is_clicked(ev):
                public = 0
                response = o.newGame(playername1, playeravatar1, public)
                if response[0] == "newGameCreated":
                    gameCode = response[1]
                print(gameCode)

                pygame.quit()
                exit()

            if Entrar.is_clicked(ev):
                Metercodigo(playername1, playeravatar1)
                MenuOnline(False)

            if Ver.is_clicked(ev):
                EncontarJogo(playername1, playeravatar1)
                MenuOnline(False)

        clock.tick(FPS)

def Tutorial(i=1, running=True):
    global lang
    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3)
    tot = pygame.transform.scale_by(assets[lang]["tot"+ str(i)], 1)

    totB = Button((0, 0),  # posição
                 (1920, 1080),  # tamanho
                 (tot, (0, 0, 1920, 1080)),  # imagem default
                )
    totB.draw(screen)

    exitB = Button((1884, -3),  # posição
                   (12 * 3, 12 * 3),  # tamanho
                   (cursors, (337 * 3, 493 * 3, 12 * 3, 12 * 3),  # imagem default
                   ))
    exitB.draw(screen)

    clock = pygame.time.Clock()
    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if exitB.is_clicked(ev):
                pygame.quit()
                exit()

            if totB.is_clicked(ev):
               running = False

        pygame.display.flip()
        clock.tick(FPS)

def win(gameData, running = True):
    winner = gameData["history"][-1][0]
    winnerName = gameData["playerNames"][winner]
    winnerAvatar = gameData["playerAvatars"][winner]

    global lang
    print (screen)
    screen.fill(0xf6d992, (0, 0, 1920, 1080))

    font = pygame.font.Font(assets["font"], 30)
    renderTextCenteredAt("Winner: "+winnerName, font,(86,22,12),960,540,screen,600)

    clock = pygame.time.Clock()
    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(FPS)

def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = []
    textS = text.split("\n")
    for line in textS:
        if line != "":
            for l in line.split():
                words.append(l)
        else:
            words.append("\n")
        words.append("\n")

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            if words[0] == "\n":
                words.pop(0)
                break
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    while True:
        found = False
        xi = 1
        while xi < len(lines):
            if lines[xi] == "" and lines[xi] == lines [xi-1]:
                lines.pop(xi)
                found = True
            xi += 1

        if not found:
            break


    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        tx = x-x/2
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh

while True:
    menuPrincipal()