from modules.Settings import *
from modules.Sprites import noteicons_group
import pygame


class GamePause():
    def __init__(self, game):
        self.game = game

    def render(self):
        pause_text = self.game.font.render('PAUSE', 1, RED)
        self.game.screen.blit(pause_text, (
            WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))


class LabirintInterface():
    def __init__(self, game):
        self.game = game

        self.note_group = pygame.sprite.Group()
        self.notes = [note for note in self.game.sprites.objects_list if
                      note.flag == "note"]
        self.update_notes_list()

    def update_notes_list(self):
        for i in range(len(self.game.sprites.objects_list)):
            sprite = self.game.sprites.objects_list[
                len(self.game.sprites.objects_list) - i - 1]
            if sprite.flag == 'note':
                sprite.noteIcon.move((WIDTH - 70) - i * 50, 10)

    def render(self):
        noteicons_group.draw(self.game.screen)
        noteicons_group.update()
