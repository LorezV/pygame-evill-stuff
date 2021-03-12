import pygame
import sys
from modules.Game import Game


def main():
    pygame.init()
    pygame.display.set_caption("Evil Stuff | PyGame")
    game = Game()
    while game.running:
        game.game_loop()
    pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
