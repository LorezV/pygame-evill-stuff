import pygame
import sys


def terminate():
    pygame.quit()
    sys.exit()


FPS = 60
SIZE = HEIGHT, WIDTH = 800, 600
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

while True:
    screen.fill("blue")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pygame.display.flip()
    clock.tick(FPS)
