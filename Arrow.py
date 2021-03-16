from DynamicObject import DynamicObject
import pygame
class Arrow(DynamicObject):
    def __init__(self, image, x, y, orientation, speed, maxRange, direction):
        super().__init__(image, x, y, orientation, speed, direction)
        self.startPosition = pygame.math.Vector2(x, y)
        self.maxRange = maxRange
    def handleOutOfBounds(self, screen):
        outOfBoundsX = self.rect.x > screen.get_width() - self.rect.width or self.rect.x < 0
        outOfBoundsY = self.rect.y > screen.get_height() - self.rect.height or self.rect.y < 0

        outOfBounds = outOfBoundsX or outOfBoundsY 
        outOfRange = abs( self.position.x - self.startPosition.x ) > self.maxRange
        if outOfBounds or outOfRange:
            pygame.sprite.Sprite.kill(self)
