from scripts.imports import *

from scripts.utils import load_image, get_spritesheet_images, Animation, get_sheet_images
from scripts.entities import KinematicBody, Player, NPC
from scripts.camera import Camera
from scripts.tilemap import Tilemap

class Game:
    def __init__(self) -> None:        
        pygame.init()
        self.screen_size: tuple = (1280, 720)
        self.screen = pygame.display.set_mode((self.screen_size[0], self.screen_size[1]), pygame.RESIZABLE)
        self.display = pygame.Surface((self.screen_size[0]//2, self.screen_size[1]//2))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Dungeon Souls")
        
        #-------------

        self.assets: dict[str, dict[str, pygame.Surface | Animation | list[pygame.Surface]]] = {
            "player": {
                "still": load_image("player/still.png"),
                "idle": Animation(get_spritesheet_images((120, 80), load_image("player/idle.png")), 14),
                "running": Animation(get_spritesheet_images((120, 80), load_image("player/running.png")), 4),
                "rolling": Animation(get_spritesheet_images((120, 80), load_image("player/rolling.png")), 3, False),
                "crouched": Animation([load_image("player/crouched.png")], 1),
                "crouch_walking": Animation(get_spritesheet_images((120, 80), load_image("player/crouch_walking.png")), 5),
                "attacking_1": Animation(get_spritesheet_images((120, 80), load_image("player/attacking_1.png")), 5, False),
                "attacking_2": Animation(get_spritesheet_images((120, 80), load_image("player/attacking_2.png")), 5, False),
            },
            "slime": {
                "idle": Animation(get_spritesheet_images((16, 16), load_image("enemies/slime/idle.png")), 10)
            },
            "tilemap": {
                "floor_tiles": get_sheet_images((32, 32), load_image("tiles/floor.png")),
                "wall_tiles": get_sheet_images((32, 32), load_image("tiles/walls.png"))
            }
        }
        
        #-------------
        
        self.background: list = []
        self.foreground: list[KinematicBody] = []
        
        #-------------
        self.tilemap = Tilemap(self, "level1")
        self.player = Player(pos=Vector2(0, 0), game=self, type="player")
        self.enemies = [
            NPC(pos=Vector2(60, 60), game=self, type="enemy", name="slime")
        ]
        for enemy in self.enemies:
            self.foreground.append(enemy)
        self.foreground.append(self.player)
        self.camera = Camera(Vector2(0, 0), self, entity_tracking=self.player)

    def run(self):
        while True:
            #-- Background
            self.display.fill((150, 220, 255))
            self.tilemap.render(self.display, self.camera.pos)
            
            #-- Camera
            self.camera.update()
            
            #-- Foreground
            
            for thing in self.foreground:
                thing.update()
                thing.render(self.camera.pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.going["up"] = True
                    if event.key == pygame.K_a:
                        self.player.going["left"] = True
                    if event.key == pygame.K_s:
                        self.player.going["down"] = True
                    if event.key == pygame.K_d:
                        self.player.going["right"] = True
                    if event.key == pygame.K_SPACE:
                        self.player.set_action("rolling")
                    if event.key == pygame.K_LSHIFT:
                        self.player.sneaking = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.set_action("attacking_1")
                    if event.button == 3:
                        self.player.set_action("attacking_2")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player.going["up"] = False
                    if event.key == pygame.K_a:
                        self.player.going["left"] = False
                    if event.key == pygame.K_s:
                        self.player.going["down"] = False
                    if event.key == pygame.K_d:
                        self.player.going["right"] = False
                    if event.key == pygame.K_LSHIFT:
                        self.player.sneaking = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60) #60fps

Game().run()
