import sys, os
from termcolor import colored
import logicaSemaforo as s

class Button(object):
    def __init__(self, position, size, image, image_hover=None, image_down=None):

        self.image = image

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
        # case 2: carregarJogo() # ainda não implementado
        case 3: regras()
        case 4: sys.exit()
        case _:
            print("opção inválida")
            mainMenu()

        if image_down is None:
            self.image_down = image
        else:
            self.image_down = image_down

        self.rect = pygame.Rect(position, size)

def novoJogoPvP():
    player1 = input("Nome do jogador 1: ")
    player2 = input("Nome do jogador 2: ")
    gameData = s.initGameData(player1, player2)
    print(f"O jogador", gameData["playerNames"][gameData["turn"]], "joga primeiro.")
    input("Prima ENTER para começar o jogo.")
    gameLoop(gameData)

def gameLoop(gameData):
    while not s.checkWin(gameData):
        clear()
        printBoard(gameData)
        while True:
            play = input("Jogador " + gameData["playerNames"][gameData["turn"]] + " (linha, coluna): ")

            if len(play) == 2 and play[0] in "123" and play[1] in "1234":
                if gameData["board"][int(play[0])-1][int(play[1])-1] == 3:
                    print("jogada inválida, não pode substituir uma peça vermelha")
                elif not s.checkAvailablePieces(gameData, play):
                    print("jogada inválida, não há peças disponíveis")
                else:
                    gameData["board"][int(play[0])-1][int(play[1])-1] += 1
                    break
            else:
                print("jogada inválida")
        gameData["turn"] = (gameData["turn"] + 1) % 2
    gameData["turn"] = (gameData["turn"] + 1) % 2 # para voltar ao jogador que ganhou
    print("Fim do jogo")
    printBoard(gameData)
    print("O jogador", gameData["playerNames"][gameData["turn"]], "ganhou!")

    def is_clicked(self, event):
        self.is_hovered(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickSound = pygame.mixer.Sound(assets["click"])
            pygame.mixer.Sound.set_volume(clickSound, 0.2)
            pygame.mixer.Sound.play(clickSound)
            if event.button == 1:
                screen.blit(self.image_down[0], self.rect, self.image_down[1])
                return self.rect.collidepoint(event.pos)

pygame.init()

lang = "pt"
FPS = 144

screen = pygame.display.set_mode((1920, 1080)) ## tentar resolver problema das outras resoluções depois
pygame.display.set_caption("Semáforo")
pygame_icon = assets[lang]["logo"]
pygame.display.set_icon(pygame_icon)
n = 1

buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5)
cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3)

pygame.mixer.music.load(assets["welcomeToTheMato"])
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(0)
muteButtonAsset = {
    "muted": (137 * 3, 384 * 3, 9 * 3, 8 * 3),
    "unmuted": (128 * 3, 384 * 3, 9 * 3, 8 * 3),
}
muteButton = Button((200, 120), # posição
                    (9 * 3, 8 * 3), # tamanho
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
    screen.fill(0x93bcf8, (200, 120, 9 * 3, 8 * 3))
    muteButton = Button((200, 120), # posição
                    (9 * 3, 8 * 3), # tamanho
                    (cursors, muteButtonAsset[muteStatus]), # imagem default
    )
    muteButton.draw(screen)

def menuPrincipal():
    bgImage = pygame.transform.scale_by(assets["background"], 2.7)
    screen.blit(bgImage, (190, -100))

    clouds = pygame.transform.scale_by(assets["clouds"], 2)
    screen.blit(clouds, (200, 200), (0*2, 470*2 , 150*2, 80*2))
    screen.blit(clouds, (1600, 200), (150*2, 430*2 , 150*2, 80*2))
    screen.blit(clouds, (1400, 400), (400*2, 465*2 , 140*2, 70*2))

    logo = pygame.transform.scale_by(assets[lang]["logo"], 2)
    screen.blit(logo, (560, 200))

    muteButton.draw(screen)

    newGameButton = Button((570, 650), # posição
                        (74 * 2.5, 58 * 2.5), # tamanho
                        (buttons, (0 * 2.5, 245 * 2.5 - 58 * 2.5, 74 * 2.5, 58 * 2.5)), # imagem default
                        (buttons, (0 * 2.5, 245 * 2.5, 74 * 2.5, 58 * 2.5)), # imagem hover
    )
    newGameButton.draw(screen)

    loadGameButton = Button((770, 650), # posição
                        (74 * 2.5, 58 * 2.5), # tamanho
                        (buttons, (74 * 2.5, 245 * 2.5 - 58 * 2.5, 74 * 2.5, 58 * 2.5)), # imagem default
                        (buttons, (74 * 2.5, 245 * 2.5, 74 * 2.5, 58 * 2.5)), # imagem hover
    )
    loadGameButton.draw(screen)

    rulesButton = Button((970, 650), # posição
                        (74 * 2.5, 58 * 2.5), # tamanho
                        (buttons, (148 * 2.5, 245 * 2.5 - 58 * 2.5, 74 * 2.5, 58 * 2.5)), # imagem default
                        (buttons, (148 * 2.5, 245 * 2.5, 74 * 2.5, 58 * 2.5)), # imagem hover
    )
    rulesButton.draw(screen)

    quitButton = Button((1170, 650), # posição
                        (74 * 2.5, 58 * 2.5), # tamanho
                        (buttons, (222 * 2.5, 245 * 2.5 - 58 * 2.5, 74 * 2.5, 58 * 2.5)), # imagem default
                        (buttons, (222 * 2.5, 245 * 2.5, 74 * 2.5, 58 * 2.5)), # imagem hover
    )
    quitButton.draw(screen)

    creditsButton = Button((1590, 900), # posição
                        (22 * 2.5, 25 * 2.5), # tamanho
                        (buttons, (8 * 2.5, 458 * 2.5, 22 * 2.5, 25 * 2.5)), # imagem default
                        (buttons, (8 * 2.5 + 22 * 2.5, 458 * 2.5, 22 * 2.5, 25 * 2.5)), # imagem hover
    )
    creditsButton.draw(screen)

    languageButton = Button((1650, 900), # posição
                        (27 * 2.5, 25 * 2.5), # tamanho
                        (buttons, (52 * 2.5, 458 * 2.5, 27 * 2.5, 25 * 2.5)), # imagem default
                        (buttons, (52 * 2.5 + 27 * 2.5, 458 * 2.5, 27 * 2.5, 25 * 2.5)), # imagem hover
    )
    languageButton.draw(screen)

    clock = pygame.time.Clock()
    running = True
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
                continue

            if loadGameButton.is_clicked(ev):
                continue

            if rulesButton.is_clicked(ev):
                continue

            if creditsButton.is_clicked(ev):
                continue

            if languageButton.is_clicked(ev):
                continue

        pygame.display.flip()
        clock.tick(FPS)

menuPrincipal()
