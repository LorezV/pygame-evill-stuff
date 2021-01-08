import os
import pygame

pygame.display.set_mode((1200, 800))

textures = {filename.split('.')[0]:pygame.image.load(f"data/sprites/slender/{filename}").convert_alpha() for filename in os.listdir(f"data/sprites/slender/")}