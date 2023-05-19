import pygame

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
            clickSound = pygame.mixer.Sound("onlymp3.to - Video Game Beep - Sound Effect-B14L61fYZlc-256k-1656775583625.mp3")
            pygame.mixer.Sound.set_volume(clickSound, 0.2)
            pygame.mixer.Sound.play(clickSound)
            if event.button == 1:
                screen.blit(self.image_down[0], self.rect, self.image_down[1])
                return self.rect.collidepoint(event.pos)

assets = {
    "pt": {
        "buttons": pygame.image.load("TitleButtons.pt-BR.png"),
        "cursors": pygame.image.load("Cursors.pt-BR.png"),
        "logo": pygame.image.load("logo.png"),
        "specialOrdersBoard": pygame.image.load("SpecialOrdersBoard.png"),
    },
    "clouds": pygame.image.load("Clouds.png"),
    "background": pygame.image.load("stardewPanorama.png")
}

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

pygame.mixer.music.load("onlymp3.to - Marco Brasil Filho - Welcome To The Mato ft. Dj Kevin (Clipe Oficial)-MbEcjsE0UOc-256k-1655037402619.mp3")
pygame.mixer.music.play(0)
pygame.mixer.music.set_volume(0.1)
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
