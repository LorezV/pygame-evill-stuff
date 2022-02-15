import pygame
import sys
from modules.Game import Game

# Инициализация pygame
def main():
    pygame.init()
    pygame.display.set_caption("Evil Stuff | PyGame")
    programIcon = pygame.image.load('data/icon/ico.png')
    pygame.display.set_icon(programIcon)
    game = Game()
    while game.running:
        game.game_loop()
    pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
