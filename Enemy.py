from DynamicObject import DynamicObject
import pygame
class Enemy(DynamicObject):

    def update(self, screen, camera, player):
        pygame.math.Vector2.update(self.direction, player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        super().update(screen, camera)
