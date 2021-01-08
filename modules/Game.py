import sys
from modules.Player import Player
from modules.Sprites import *
from modules.Drawer import Drawer, ray_casting_walls


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.screen_minimap = pygame.Surface(MINIMAP_RES)
        self.to_render = self
        self.sprites = Sprites()
        self.clock = pygame.time.Clock()
        self.player = Player(self.sprites)
        self.drawer = Drawer(self.screen, self.screen_minimap)
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('data/textures/menu.png')
        pygame.mixer.music.load('data/music/sc_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate()

    def game_loop(self):
        if self.menu_trigger:
            self.menu()
            return
        self.check_events()
        self.player.movement()
        self.sprites.objects_list[0].action(self.player)

        self.screen.fill(BLACK)
        self.drawer.background(self.player.ang)
        self.drawer.world(
            ray_casting_walls(self.player, self.drawer.textures) + [
                obj.object_locate(self.player) for obj in
                self.sprites.objects_list])
        self.drawer.fps(self.clock)
        self.drawer.mini_map(self.player, self.sprites.objects_list[0])
        self.drawer.interface(self.player)

        pygame.display.flip()
        self.clock.tick(FPS)

    def menu(self):
        self.check_events()
        self.screen.blit(self.menu_picture, (0, 0), (0, 0, WIDTH, HEIGHT))
        start, exit, startf, exitf = self.draw_buttons()
        pygame.draw.rect(self.screen, BLACK, start, border_radius=25, width=10)
        self.screen.blit(startf, (start.centerx - 175, start.centery - 40))

        pygame.draw.rect(self.screen, BLACK, exit, border_radius=25, width=10)
        self.screen.blit(exitf, (exit.centerx - 120, exit.centery - 40))

        label = self.font.render('Evill Stuff', 1, (0, 33, 92))
        self.screen.blit(label, (280, 20))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if start.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, BLACK, start,
                             border_radius=25)
            self.screen.blit(startf,
                             ((start.centerx - 175, start.centery - 40)))
            if mouse_click[0]:
                self.menu_trigger = False
                pygame.mouse.set_visible(False)
                pygame.mixer.music.stop()
        elif exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, BLACK, exit, border_radius=25)
            self.screen.blit(exitf, ((exit.centerx - 120, exit.centery - 40)))
            if mouse_click[0]:
                self.terminate()

        pygame.display.flip()

    def draw_buttons(self):
        self.font = pygame.font.Font('data/fonts/pixels.otf', 72)
        start = self.font.render('START', 1, pygame.Color((0, 33, 92)))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = self.font.render('EXIT', 1, pygame.Color((0, 33, 92)))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200
        return button_start, button_exit, start, exit

    def terminate(self):
        pygame.quit()
        sys.exit()
