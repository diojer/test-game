from .imports import *
if TYPE_CHECKING:
    from utils import Animation

@dataclass(kw_only=True)
class KinematicBody:
    pos: Vector2
    game: "Game"
    type: str
    size: tuple = (0, 0)
    vel: Vector2 = field(default_factory=lambda: Vector2(2, 2))
    flip: bool = field(init=False, default=False)
    movement: dict = field(init=False, default_factory=lambda: dict(left = False, right = False, up = False, down = False))

    def update(self):
        self.pos.x += self.dir().x * self.vel.x

        self.pos.y += self.dir().y * self.vel.y
        
        if self.dir().x > 0:
            self.flip = False
        if self.dir().x < 0:
            self.flip = True
    def render(self):
        pass
    
    def dir(self) -> Vector2:
        direction = Vector2(self.movement["right"] - self.movement["left"], self.movement["down"] - self.movement["up"])
        if direction.length(): direction = direction.normalize()
        return direction

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos, self.size)


@dataclass
class Player(KinematicBody):
    
    action: str = field(init=False, default="")
    going: dict = field(init=False, default_factory=lambda: dict(left = False, right = False, up = False, down = False))
    sneaking: bool = field(init=False, default=False)
    
    def __post_init__(self):
        self.assets = self.game.assets["player"]
        self.UNINTERRUPTABLE = {"rolling", "attacking"}
        self.set_action("idle")
        self.size = self.animation.img().get_size()
        self.og_vel = self.vel.copy()
        
    def set_action(self, action):
        if not action == self.action and (not self.action in self.UNINTERRUPTABLE or self.animation.done):
            self.action = action
            self.animation = self.assets[self.action].copy()

    def update(self):    
        if self.action == "rolling":
            self.vel = Vector2(self.og_vel.x * 1.2, self.og_vel.y * 1.2)
            if self.dir().y == 0:
                if self.flip:
                    self.movement["left"] = True
                else:
                    self.movement["right"] = True
        elif self.action == "crouch_walking":
            self.vel = Vector2(self.og_vel.x * 0.5, self.og_vel.y * 0.5)
        elif "attack" in self.action:
            self.vel = Vector2(0, 0)
        else:
            self.vel = self.og_vel.copy()
            
        if self.animation.done:
            self.set_action("idle")
            self.movement = self.going.copy()
            
        if not self.action == "rolling" and self.animation.loop:
            # Need to shallow copy going or else it will be modified when movement is modified
            self.movement = self.going.copy()
        super().update()
                

    def get_rect(self):
        return pygame.Rect(self.pos, self.animation.img().get_size())
    
    def render(self, offset: Vector2 = Vector2(0, 0)):
        if "attack" in self.action:
            pass
        elif self.sneaking:
            if self.dir().x == 0 and self.dir().y == 0:
                self.set_action("crouched")
            else:
                self.set_action("crouch_walking")
        elif self.dir().x == 0 and self.dir().y == 0:
            self.set_action("idle")
        else:
            if self.action == "idle" or self.action == "crouch_walking":
                self.set_action("running")
        self.animation.update()
        self.game.display.blit(pygame.transform.flip(self.animation.img(), self.flip, False), self.pos - offset)
        
@dataclass
class NPC(KinematicBody):
    name: str
    action: str = field(init=False, default="")
    
    def __post_init__(self):
        self.assets = self.game.assets[self.name]
        self.set_action("idle")
        self.size = self.animation.img().get_size()
        self.og_vel = self.vel.copy()
        
    def set_action(self, action):
        if not action == self.action:
            self.action = action
            self.animation = self.assets[self.action].copy()
            
    def update(self):
        if self.type == "enemy":
            self.pos = self.pos.lerp((self.game.player.rect().centerx, self.game.player.rect().centery + self.game.player.rect().h/2 - self.size[1]), 0.01)
        super().update()
    
    def render(self, offset: Vector2 = Vector2(0, 0)):
        self.animation.update()
        self.game.display.blit(pygame.transform.flip(self.animation.img(), self.flip, False), self.pos - offset)
    
    
        

