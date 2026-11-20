import pygame
from sys import exit
import math
from Generate import Generate
import Camera as Cameraa
pygame.init()
pygame.display.set_caption("Photo puzzel")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Game = True
ScreenWidth = screen.get_width()
ScreenHeight = screen.get_height()
LoadLock = False
PlayerSize = (40, 40)

class Player():
    def __init__(self , x, y):
        super().__init__()
        self.sprint = 2.5
        self.speed = 0
        self.SpawnX = x
        self.SpawnY = y
        self.lock = False
        self.OnFloor = False
        self.width, self.height = PlayerSize
        self.velocity_x = 0
        self.velocity_y = 0
        self.image = pygame.Surface(PlayerSize)
        self.image.fill("Yellow")
        self.rect = self.image.get_rect(topleft = (self.SpawnX,self.SpawnY))
        self.pos = pygame.math.Vector2(ScreenWidth / 2, ScreenHeight / 2)
        self.SaveCords = []
    def UserInput(self):
        self.velocity_x = 0
        self.velocity_y = 0
        if Map.CheckTile(player) == "Water":
            player.speed = 0.25
            self.sprint = 1
        else:
            self.sprint = 2.5
            self.speed = 1.5
        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            self.speed = self.sprint 
        if key[pygame.K_w]:
            self.velocity_y = -self.speed
        if key[pygame.K_s]:
            self.velocity_y = self.speed
        if key[pygame.K_d]:
            self.velocity_x = self.speed
        if key[pygame.K_a]:
            self.velocity_x = -self.speed
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x *= math.sqrt(2)/2
            self.velocity_y *= math.sqrt(2)/2
    def UpdatePos(self):
        self.rect.topleft = self.pos
        self.pos.x += self.velocity_x
        self.pos.y += self.velocity_y

    def UpdatePlayer(self):
        self.UserInput()
        self.UpdatePos()
        
    

player = Player(100 , 100)
Map = Generate()
Camera = Cameraa.Camera(player)
while Game:
    screen.fill("black")
    Map.Load(screen, Camera)
    player.UpdatePlayer()
    Camera.camera_draw(Map)
    Map.GenerateWater(screen, Camera, False, 0)
    Map.GenerateWater(screen, Camera, True, 1)
    Map.GenerateWater(screen, Camera, True, 2)
    Map.Grow()
    screen.blit(player.image, (player.pos.x - Camera.offset.x , player.pos.y - Camera.offset.y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                Map.GrowAll()
    pygame.display.update()