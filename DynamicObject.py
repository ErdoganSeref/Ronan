from Object import Object
import pygame

class DynamicObject(Object):

    def __init__(self, image, x, y, orientation, speed, direction):
        super().__init__(image, x, y)
        self.position = pygame.math.Vector2(x, y)
        self.orientation = orientation
        self.speed = speed
        self.direction = pygame.math.Vector2(direction)
        
    def update(self, screen, camera):
        self.move()
        self.handleOutOfBounds(screen)
        super().update(screen, camera)

    def draw(self, screen, camera):
        if self.orientation == -1:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect.topleft + camera.position)
        elif self.orientation == 1:
            screen.blit(self.image, self.rect.topleft + camera.position)
 
    
    def handleOutOfBounds(self, screen):
        if self.rect.x > screen.get_width() - self.rect.width:
            self.rect.x = screen.get_width() - self.rect.width
            self.position.x = screen.get_width() - self.rect.width
        elif self.rect.x < 0:
            self.rect.x = 0
            self.position.x = 0
        if self.rect.y > screen.get_height() - self.rect.height:
            self.rect.y = screen.get_height() - self.rect.height
            self.position.y = screen.get_height() - self.rect.height
        elif self.rect.y < 0:
            self.rect.y = 0
            self.position.y = 0

    def move(self):
        if self.direction.length() > 0:
            if (self.direction.x > 0 and self.orientation == -1) or (self.direction.x < 0 and self.orientation == 1):
                self.orientation *= -1
            
            pygame.math.Vector2.scale_to_length(self.direction, 1)
            self.position += self.direction * self.speed
            self.rect.topleft = self.position
