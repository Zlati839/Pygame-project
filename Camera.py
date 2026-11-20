import pygame
import random as rng
class Camera():
    def __init__(self , Player):
        self.player = Player
        self.Width, self.Height = pygame.display.get_surface().get_size()
        self.offset = pygame.math.Vector2()
    
    
    def camera_draw(self , Map):
        self.offset.x = self.player.rect.centerx - self.Width // 2
        self.offset.x = max(0, self.offset.x)
        self.offset.y  = self.player.rect.centery - self.Height // 2 
        self.offset.y = max(0 , self.offset.y)
        self.offset.x = max(0, min(self.offset.x, Map.Map_Width - self.Width))
        self.offset.y = max(0, min(self.offset.y, Map.Map_Height - self.Height))
