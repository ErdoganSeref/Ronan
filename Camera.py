from pygame.math import Vector2

class Camera():

    def __init__(self):
        self.position = Vector2(0, 0)

    def move(self, direction):
        self.position += direction
    
