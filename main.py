import pygame
pygame.init()

pygame.mixer.music.load("onlymp3.to - Marco Brasil Filho - Welcome To The Mato ft. Dj Kevin (Clipe Oficial)-MbEcjsE0UOc-256k-1655037402619.mp3")
pygame.mixer.music.play(0, 0.0)
pygame.mixer.music.set_volume(0.3)
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Semaforo")
pygame_icon = pygame.image.load("stardewPanorama.png")
pygame.display.set_icon(pygame_icon)
n = 1


def menu():
 image = pygame.image.load("stardewPanorama.png")
 screenUpdate = pygame.transform.scale_by(image, 2.7)
 screen.blit(screenUpdate, (190, -100))

 my_image = pygame.image.load("Clouds.png")
 my_image2 = pygame.transform.scale_by(my_image, 2)
 screen.blit(my_image2, (200, 200), (0*2, 470*2 , 150*2, 80*2))
 screen.blit(my_image2, (1600, 200), (150*2, 430*2 , 150*2, 80*2))
 screen.blit(my_image2, (1400, 400), (400*2, 465*2 , 140*2, 70*2))

 my_image = pygame.image.load("logo.png")
 my_image2 = pygame.transform.scale_by(my_image, 2)
 screen.blit(my_image2, (560, 200))

menu()

my_image5 = pygame.image.load("Cursors.pt-BR.png")
my_image6 = pygame.transform.scale_by(my_image5, 3)
screen.blit(my_image6, (200, 120), (128 * 3, 384 * 3, 9 * 3, 8 * 3))

my_image3 = pygame.image.load("TitleButtons.pt-BR.png")
my_image4 = pygame.transform.scale_by(my_image3, 2.5)


while True:
    mouse = pygame.mouse.get_pos()
    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONDOWN:
            sound = pygame.mixer.Sound("onlymp3.to - Video Game Beep - Sound Effect-B14L61fYZlc-256k-1656775583625.mp3")
            pygame.mixer.Sound.play(sound)

            if 1170 <= mouse[0] <= 1170 + 74 * 2.5 and 650 <= mouse[1]<= 650 + 58 * 2.5:
                pygame.quit()

            if 970 <= mouse[0] <= 970 + 74 * 2.5 and 650 <= mouse[1]<= 650 + 58 * 2.5:
                pygame.quit()

            if 770 <= mouse[0] <= 770 + 74 * 2.5 and 650 <= mouse[1]<= 650 + 58 * 2.5:
                n = n + 1

                if (n % 2) == 0:
                    pygame.mixer.music.pause()
                    menu()
                    screen.blit(my_image6, (200, 120), (137 * 3, 384 * 3, 9 * 3, 8 * 3))
                elif (n % 2) != 0:
                    pygame.mixer.music.unpause()
                    menu()
                    screen.blit(my_image6, (200, 120), (128 * 3, 384 * 3, 9 * 3, 8 * 3))

            if 570 <= mouse[0] <= 570 + 74 * 2.5 and 650 <= mouse[1]<= 650 + 58 * 2.5:
                pygame.quit()

            if 1650 <= mouse[0] <= 1650 + 22 * 2.5 and 800 <= mouse[1]<= 800 + 25 * 2.5:
                pygame.quit()

            if 1650 <= mouse[0] <= 1650 + 27 * 2.5 and 880 <= mouse[1]<= 880 + 25 * 2.5:
                pygame.quit()

    if 1170 <= mouse[0] <= 1170 + 74 * 2.5 and 650 <= mouse[1] <= 650 + 58 * 2.5:
        screen.blit(my_image4, (1170, 650), (222 * 2.5, 245 * 2.5, 74 * 2.5, 58 * 2.5))
    else:
        screen.blit(my_image4, (1170, 650), (222 * 2.5, 245 * 2.5-58* 2.5, 74 * 2.5, 58 * 2.5))

    if 970 <= mouse[0] <= 970 + 74 * 2.5 and 650 <= mouse[1] <= 650 + 58 * 2.5:
        screen.blit(my_image4, (970, 650), (222 * 2.5-74*2.5, 245 * 2.5, 74 * 2.5, 58 * 2.5))
    else:
        screen.blit(my_image4, (970, 650), (222 * 2.5-74*2.5, 245 * 2.5-58* 2.5, 74 * 2.5, 58 * 2.5))

    if 770 <= mouse[0] <= 770 + 74 * 2.5 and 650 <= mouse[1] <= 650 + 58 * 2.5:
        screen.blit(my_image4, (770, 650), (222 * 2.5-74*5, 245 * 2.5, 74 * 2.5, 58 * 2.5))
    else:
        screen.blit(my_image4, (770, 650), (222 * 2.5-74*5, 245 * 2.5-58* 2.5, 74 * 2.5, 58 * 2.5))

    if  570 <= mouse[0] <= 570 + 74 * 2.5 and 650 <= mouse[1] <= 650 + 58 * 2.5:
        screen.blit(my_image4, (570, 650), (222 * 2.5-74*7.5, 245 * 2.5, 74 * 2.5, 58 * 2.5))
    else:
        screen.blit(my_image4, (570, 650), (222 * 2.5-74*7.5, 245 * 2.5-58 * 2.5, 74 * 2.5, 58 * 2.5))

    if  1650 <= mouse[0] <= 1650 + 22 * 2.5 and 800 <= mouse[1] <= 800 + 25 * 2.5:
        screen.blit(my_image4, (1650, 800), (8 * 2.5 + 22 * 2.5, 458 * 2.5 , 22 * 2.5, 25 * 2.5))
    else:
        screen.blit(my_image4, (1650, 800), (8 * 2.5, 458 * 2.5, 22 * 2.5, 25 * 2.5))

    if  1650 <= mouse[0] <= 1650 + 27 * 2.5 and 880 <= mouse[1] <= 880 + 25 * 2.5:
        screen.blit(my_image4, (1650, 880), (52 * 2.5 + 27 * 2.5, 458 * 2.5, 27 * 2.5, 25 * 2.5))
    else:
        screen.blit(my_image4, (1650, 880), (52 * 2.5, 458 * 2.5, 27 * 2.5, 25 * 2.5))
    pygame.display.flip()