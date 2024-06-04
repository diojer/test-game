from .imports import *

@dataclass
class Camera:
    pos: Vector2
    game: "Game"
    entity_tracking: "KinematicBody | None" = None
    rate: float = 0.1
    
    def __post_init__(self):
        self.target_pos: Vector2 = self.pos
    
    def set_entity(self, e: "KinematicBody | None"):
        self.entity_tracking = e

    def set_target_pos(self, pos: Vector2):
        self.target_pos = pos
    
    def update(self):
        if self.entity_tracking:
            target_x = (self.entity_tracking.rect().centerx - self.game.display.get_width()/2 - self.pos.x) * self.rate
            target_y = (self.entity_tracking.rect().centery - self.game.display.get_height()/2 - self.pos.y) * self.rate
            self.set_target_pos(Vector2(target_x, target_y))
        self.pos += self.target_pos