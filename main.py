import pygame, logicaSemaforo
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

assets = {
    "pt": {
        "buttons": pygame.image.load("./assets/pt/TitleButtons.png"),
        "cursors": pygame.image.load("./assets/pt/Cursors.png"),
    },
    "en": {
        "buttons": pygame.image.load("./assets/en/TitleButtons.png"),
        "cursors": pygame.image.load("./assets/en/Cursors.png"),
    },
    "logo": pygame.image.load("./assets/novalogo2.png"),
    "clouds": pygame.image.load("./assets/global/Clouds.png"),
    "background": pygame.image.load("./assets/global/stardewPanorama.png"),
    "specialOrdersBoard": pygame.image.load("./assets/global/SpecialOrdersBoard.png"),
    "welcomeToTheMato": "./assets/music/welcomeToTheMato.mp3",
    "click": "./assets/sounds/click.mp3"
}

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
                screen.blit(self.image_down[0], self.rect, self.image_down[1])
                return self.rect.collidepoint(event.pos)

pygame.init()

lang = "pt"
FPS = 144

screen = pygame.display.set_mode((1920, 1080)) ## tentar resolver problema das outras resoluções depois
pygame.display.set_caption("Semáforo")
pygame_icon = assets["logo"]
pygame.display.set_icon(pygame_icon)
n = 1

buttons = pygame.transform.scale_by(assets[lang]["buttons"], 2.5*(2147/1920))
cursors = pygame.transform.scale_by(assets[lang]["cursors"], 3*(2147/1920))

pygame.mixer.music.load(assets["welcomeToTheMato"])
pygame.mixer.music.set_volume(0.1)
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
                continue

            if loadGameButton.is_clicked(ev):
                continue

            if rulesButton.is_clicked(ev):
                continue

            if creditsButton.is_clicked(ev):
                continue

            if languageButton.is_clicked(ev):
                lang = "en" if lang == "pt" else "pt"
                running = False

        pygame.display.flip()
        clock.tick(FPS)

while True:
    menuPrincipal()
