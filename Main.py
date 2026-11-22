import pygame
from sys import exit
import math
from Generate import Generate
import Camera as Cameraa
import asyncio
pygame.init()
pygame.display.set_caption("Photo puzzel")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Game = True
ScreenWidth = screen.get_width()
ScreenHeight = screen.get_height()
LoadLock = False
PlayerSize = (40, 40)
clock = pygame.time.Clock()
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
    def UserInput(self):
        self.velocity_x = 0
        self.velocity_y = 0
        if Map.CheckTile(player) == "Water":
            player.speed = 0.25
            self.sprint = 1
        else:
            self.sprint = 10
            self.speed = 7
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
        dt = min(clock.tick(60), 50) * 0.06
        old_pos = self.pos.copy()
        self.rect.topleft = self.pos
        self.pos.x += self.velocity_x * dt
        self.pos.y += self.velocity_y * dt
        self.pos.x = max(0, min(self.pos.x, Map.Map_Width - self.width))
        self.pos.y = max(0, min(self.pos.y, Map.Map_Height - self.height))    
        if Map.CheckTile(player) == "Tree":
                    self.pos = old_pos
                    self.rect.center = self.pos
    def UpdatePlayer(self):
        self.UserInput()
        self.UpdatePos()

player = Player(100 , 100)
Map = Generate()
Camera = Cameraa.Camera(player)

text_font = pygame.font.SysFont("None" , 30)
tutorial_font = pygame.font.SysFont("None" , 35)
big_font = pygame.font.SysFont("None", 40)    
def draw_text(text , font , text_color , x ,y ):
    img = font.render(text , True , text_color)
    screen.blit(img,(x,y)) 
async def main():
    global Game , player , Map , Camera
    while Game:
        screen.fill("black")
        Map.Load(screen, Camera)
        player.UpdatePlayer()
        Camera.camera_draw(Map)
        Map.GenerateWater(screen, Camera, False, 0)
        Map.GenerateWater(screen, Camera, False, 1)
        Map.GenerateWater(screen, Camera, True, 2)
        Map.GenerateWater(screen, Camera, True, 3)
        Map.GenerateWater(screen, Camera, True, 4)
        Map.Grow()
        Map.CheckClose(player.pos)
        screen.blit(player.image, (player.pos.x - Camera.offset.x , player.pos.y - Camera.offset.y))
        draw_text(f"Seeds: {Map.Inventory.get('seed', 0)}", big_font, (0, 150, 0), 20, 20)
        draw_text(f"Wood: {Map.Inventory.get('Wood', 0)}", big_font, (100, 0, 0), 20, 60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    Map.GrowAll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    Map.CutDown()
                if event.key == pygame.K_9:
                    Map.Plant(player)
        pygame.display.update()
        await asyncio.sleep(0)
asyncio.run(main())