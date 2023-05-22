import pygame, logicaSemaforo
import ctypes
import os
import json
ctypes.windll.user32.SetProcessDPIAware()
pygame.font.init()

assets = {
    "pt": {
        "buttons": pygame.image.load("./assets/pt/TitleButtons.png"),
        "cursors": pygame.image.load("./assets/pt/Cursors.png"),
    },
    "en": {
        "buttons": pygame.image.load("./assets/en/TitleButtons.png"),
        "cursors": pygame.image.load("./assets/en/Cursors.png"),
    },
    "tabuleiro": pygame.image.load("./assets/global/tabuleiro.png"),
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

    def is_hovered(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                screen.blit(self.image_hover[0], self.rect, self.image_hover[1])
            else:
                screen.blit(self.image[0], self.rect, self.image[1])

    def is_clicked(self, event):
        self.is_hovered(event)
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
                # como aqui não faz diferença (image_hover é sempre igual à imagem) e não estamos a usar
                # nada hovered vamos comentar p/ evitar load desnecessário
                # screen.blit(self.image_hover, self.rect, self.iconCoords)
                screen.blit(self.imgScaled3, self.avatarPos, self.avatarCoords)
            # mesma coisa, não estamos a usar nada hovered, não faz diferença
            # else:
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

screen = pygame.display.set_mode((1920, 1080)) ## tentar resolver problema das outras resoluções depois
pygame.display.set_caption("Semáforo")
pygame_icon = assets["logo"]
pygame.display.set_icon(pygame_icon)
n = 1

cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3*(2147/1920))

pygame.mixer.music.load(assets["welcomeToTheMato"])
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(0)
muteButtonAsset = {
    "muted": (137 * 3*(2147/1920), 384 * 3*(2147/1920), 9 * 3*(2147/1920), 8 * 3*(2147/1920)),
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
                NomePersonagem()
                menuPrincipal(False)

            if loadGameButton.is_clicked(ev):
                continue

            if rulesButton.is_clicked(ev):
                continue

            if creditsButton.is_clicked(ev):
                SettingseCredits()
                menuPrincipal(False)

            if languageButton.is_clicked(ev):
                lang = "en" if lang == "pt" else "pt"
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def SettingseCredits(running = True):
    global lang
    soBoard = pygame.transform.scale_by(assets["specialOrdersBoard"], 4.5)
    screen.blit(soBoard, (202, 100), (0, 0, 337*4.5, 197*4.5))

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


def NomePersonagem(running = True):
    global lang
    tabuleiro = pygame.transform.scale_by(assets["tabuleiro"], 6)
    screen.blit(tabuleiro, (0, 0), (320 * 6, 0, 320*6, 180*6))

    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))
    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 2*(2147/1920))


    input_box = pygame.Rect(1150, 725, 200, 200)
    color_inactive = pygame.Color((86,22,12))
    color_active = pygame.Color((86,22,12))
    color = color_inactive
    active = False
    text = ''

    buttonback = Button((1755, 1005),  # posição
                   (66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920)),  # tamanho
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920), 66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),  # imagem default
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920)+27 * 2.5*(2147/1920),66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),
                   )
    buttonback.draw(screen)

    ok = Button((1330, 430),  # posição
                   (65 * 2*(2147/1920), 65 * 2*(2147/1920)),  # tamanho
                   (cursors, (127 * 2*(2147/1920), 255 * 2*(2147/1920), 65 * 2*(2147/1920), 65 * 2*(2147/1920))),  # imagem default
                   (cursors, (127 * 2*(2147/1920), 255 * 2*(2147/1920), 65 * 2*(2147/1920), 65 * 2*(2147/1920))),
                   )
    ok.draw(screen)



    characters = importCharacters()
    avis = []


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

            if buttonback.is_clicked(ev):
                running = False

            if ok.is_clicked(ev):
                NomePersonagem2()
                NomePersonagem(False)

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

def NomePersonagem2(running = True):
    global lang
    tabuleiro = pygame.transform.scale_by(assets["tabuleiro"], 6)
    screen.blit(tabuleiro, (0, 0), (320 * 6, 0, 320*6, 180*6))

    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))
    cursors = pygame.transform.scale_by(assets[lang]["cursors"], 2*(2147/1920))


    input_box = pygame.Rect(1150, 725, 200, 200)
    color_inactive = pygame.Color((86,22,12))
    color_active = pygame.Color((86,22,12))
    color = color_inactive
    active = False
    text = ''

    buttonback = Button((1755, 1005),  # posição
                   (66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920)),  # tamanho
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920), 66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),  # imagem default
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920)+27 * 2.5*(2147/1920),66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),
                   )
    buttonback.draw(screen)

    ok = Button((1330, 430),  # posição
                   (65 * 2*(2147/1920), 65 * 2*(2147/1920)),  # tamanho
                   (cursors, (127 * 2*(2147/1920), 255 * 2*(2147/1920), 65 * 2*(2147/1920), 65 * 2*(2147/1920))),  # imagem default
                   (cursors, (127 * 2*(2147/1920), 255 * 2*(2147/1920), 65 * 2*(2147/1920), 65 * 2*(2147/1920))),
                   )
    ok.draw(screen)



    characters = importCharacters()
    avis = []


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

            if buttonback.is_clicked(ev):
                running = False

            if ok.is_clicked(ev):
                Tabuleiro()
                NomePersonagem2(False)

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

def Tabuleiro(running = True):
    global lang

    tabuleiro = pygame.transform.scale_by(assets["tabuleiro"], 6)
    screen.blit(tabuleiro, (0, 0), (0 , 0, 320*6, 180*6))

    buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))

    buttonback = Button((1755, 1005),  # posição
                   (66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920)),  # tamanho
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920), 66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),  # imagem default
                   (buttons, (296 * 2.5*(2147/1920), 252 * 2.5*(2147/1920)+27 * 2.5*(2147/1920),66 * 2.5*(2147/1920), 27 * 2.5*(2147/1920))),
                   )
    buttonback.draw(screen)

    quadradro1 = Button((300, 300),  # posição
                   (40 * 6, 40 * 6),  # tamanho
                   (tabuleiro, (534 * 6, 18 * 6, 40 * 6, 40 * 6)),  # imagem default
                   )
    quadradro1.draw(screen)

    quadradro2 = Button((600, 300),  # posição
                        (40 * 6, 40 * 6),  # tamanho
                        (tabuleiro, (534 * 6, 18 * 6, 40 * 6, 40 * 6)),  # imagem default
                        )
    quadradro2.draw(screen)

    quadradro3 = Button((900, 300),  # posição
                        (40 * 6, 40 * 6),  # tamanho
                        (tabuleiro, (534 * 6, 18 * 6, 40 * 6, 40 * 6)),  # imagem default
                        )
    quadradro3.draw(screen)

    clock = pygame.time.Clock()

    while running:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if quadradro1.is_clicked(ev):
                crops = pygame.transform.scale_by(assets["crops"], 3.6)
                screen.blit(crops, (334, 326), (208 * 3.6, 518 * 3.6, 48 * 3.6, 53 * 3.6))

            if quadradro2.is_clicked(ev):
                crops = pygame.transform.scale_by(assets["crops"], 3.7)
                screen.blit(crops, (631, 327), (112 * 3.7, 525 * 3.7, 48 * 3.7, 53 * 3.7))

            if quadradro3.is_clicked(ev):
                crops = pygame.transform.scale_by(assets["crops"], 3.6)
                screen.blit(crops, (936, 326), (162 * 3.6, 518 * 3.6, 44 * 3.6, 53 * 3.6))

            if buttonback.is_clicked(ev):
                running=False

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

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        # tx = x - fw / 2
        tx = x-x/2
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh

while True:
    menuPrincipal()