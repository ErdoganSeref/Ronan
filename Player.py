from DynamicObject import DynamicObject
from pygame.math import Vector2

class Player(DynamicObject):

    def  __init__(self, image, x, y, orientation, HP, speed, reloadTime, fireRate, ammunitionCapacity, direction=(0,0)):
        super().__init__(image, x, y, orientation, speed, direction)
        self.camera = Vector2(0, 0)
        self.HP = HP
        self.reloadTime = reloadTime
        self.fireRate = fireRate
        self.ammunitionCapacity = ammunitionCapacity
        self.ammunition = ammunitionCapacity
        self.lastReload = 0
        self.lastShot = 0
        self.lastGotHit = 0
        self.reloading = False
        
    def update(self, screen, camera):
        if self.reloading:
            self.direction.xy = (0, 0)
        self.move(camera)
        self.handleOutOfBounds(screen)
        self.draw(screen, camera)
        self.direction.xy = (0, 0)

    def move(self, camera):
        if self.direction.length() > 0:
            if (self.direction.x > 0 and self.orientation == -1) or (self.direction.x < 0 and self.orientation == 1):
                self.orientation *= -1
            
            pygame.math.Vector2.scale_to_length(self.direction, 1)
            camera.move( self.direction * self.speed )
            self.position += self.direction * self.speed
            self.rect.topleft = self.position

    def reload(self):
        self.reloading = True
        self.ammunition = self.ammunitionCapacity
        

        



