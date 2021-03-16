import pygame 

class Object(pygame.sprite.Sprite):

    def __init__(self, image, x, y):        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, screen, camera):
        self.draw( screen, camera )
    
    def draw(self, screen, camera):
        screen.blit(self.image, self.rect.topleft + camera.position)

