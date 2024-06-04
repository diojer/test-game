from .imports import *
from pytmx.util_pygame import load_pygame

NEIGHBOR_OFFSET = [(-1,  -1), (-1, -0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
PHYSICS_TILES = {"walls"}

@dataclass
class Tilemap:
    game: "Game"
    level: str
    tile_size: int = 16
    

    def __post_init__(self):
        # self.assets = self.game.assets["tilemap"]
        self.tilemap = {}
        self.offgrid_tiles = []
        self.tmx = load_pygame(f"data/tilemaps/{self.level}.tmx")
        # for layer in self.tmx.layers:
        #     for x, y, tile in layer.tiles():
        #         tilePos = Vector2(x, y)
        #         self.tilemap[layer] = {
        #             "tile": tile,
        #             "pos": tilePos
        #         }
        

    def render(self, surf: pygame.Surface, offset: Vector2):
        for layer in self.tmx.layers:
            for x, y, tile in layer.tiles():
                surf.blit(tile, (x * self.tile_size - offset.x, y * self.tile_size - offset.y))
        
    
    def tiles_around(self, pos: Vector2):
        tiles = []
        tile_loc = Vector2(int(pos.x // self.tile_size), int(pos.y // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(int(tile_loc.x) + offset[0]) + ";" + str(int(tile_loc.y) + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos) -> list[pygame.Rect]:
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size))
        
        return rects