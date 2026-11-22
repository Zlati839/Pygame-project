import pygame
import math
import random as rng
TileSize = (64 , 64)
class Generate():
     def __init__(self):
        self.LastTriggered = 60
        self.Width = 64
        self.Height = 64
        self.HighLightI = 0
        self.HighLightQ = 0
        self.waterSizeX = rng.randint(13, 25)
        self.waterSizeY = rng.randint(13, 25)
        self.waterSizeSmollX = rng.randint(5, 10)
        self.waterSizeSmoolY = rng.randint(5, 10)
        self.Map_Width = TileSize[0] * self.Width
        self.Map_Height = TileSize[1] * self.Height
        self.RandomColumn = rng.randint(0, self.Width)
        self.RandomRow = rng.randint(0, self.Height)
        self.ValueAsATileBeing = 0
        self.TileList = []
        self.Grass1 =  pygame.image.load("TileSet/Sprite-0001.png").convert_alpha()
        self.Grass2 =  pygame.image.load("TileSet/Sprite-0004.png").convert_alpha()
        self.Water =  pygame.image.load("TileSet/Sprite-0005.png").convert_alpha()
        self.FlowersW =  pygame.image.load("TileSet/Sprite-0002.png").convert_alpha()
        self.FlowersB = pygame.image.load("TileSet/Sprite-0003.png").convert_alpha()
        self.Seed  = pygame.image.load("TileSet/Sprite-0006.png").convert_alpha()
        self.TreeUP = pygame.image.load("TileSet/TreeUP.png").convert_alpha()
        self.TreeDown = pygame.image.load("TileSet/TreeDown.png").convert_alpha()
        self.TreeUPlight = pygame.image.load("TileSet/TreeUPLIGHT.png").convert_alpha()
        self.TreeDownlight = pygame.image.load("TileSet/TreeDownLIGHT.png").convert_alpha()
        self.AlreadyLoaded = False
        self.lock = False
        self.Inventory = {}
        self.Generate_random()
        
     def Generate_random(self):
              for i in range(self.Height):
                  rows = []
                  for q in range(self.Width) :
                      que  = rng.randint(0, 4)
                      if que == 4:
                          qus  = rng.randint(1, 15)
                          if qus == 1:
                             rows.append(5)
                          else :
                              rows.append(0)
                      else :
                        rows.append(que)
                  self.TileList.append(rows)
     def GenerateWater(self,screen, camera , small, WaterID):
         if not small:
             width = self.waterSizeX
             height = self.waterSizeY
         else:
             width = self.waterSizeSmollX
             height = self.waterSizeSmoolY


         # Generate position only once per lake
         if not hasattr(self, "WaterPositions"):
             self.WaterPositions = {}
         if WaterID not in self.WaterPositions:
             RandomColumn = rng.randint(0, self.Width - width)
             RandomRow = rng.randint(0, self.Height - height)
             self.WaterPositions[WaterID] = (RandomColumn, RandomRow)
         RandomColumn, RandomRow = self.WaterPositions[WaterID]

         x = RandomColumn * TileSize[0]
         y = RandomRow * TileSize[1]
         startingX = x
         centerX = width / 2
         centerY = height / 2

         ValueAsATileBeing = min(width, height) / 2

         for q in range(height):
             for i in range(width):
                 distance = math.sqrt((i - centerX) ** 2 +(q - centerY) ** 2)

                 if distance < ValueAsATileBeing:
                     screen.blit(self.Water,(x - camera.offset.x,y - camera.offset.y))
                     xList = int(x/64)
                     yList = int(y/64)
                     self.TileList[yList][xList] = -1
                 x += TileSize[0]
             y += TileSize[1]
             x = startingX

     def GrowAll(self):
      for y, row in enumerate(self.TileList):
            for x, tile in enumerate(row):
                if tile == 5:
                    if y > 0 and not self.TileList[y - 1][x] == -1 :
                        self.TileList[y][x] = 10
                        self.TileList[y - 1][x] = 11
    
     def AddItem(self, item, amount=1):
        self.Inventory[item] = self.Inventory.get(item, 0) + amount

     def HasItem(self, item, amount=1):
            return self.Inventory.get(item, 0) >= amount

     def RemoveItem(self, item, amount=1):
      if self.Inventory.get(item, 0) >= amount:
        self.Inventory[item] -= amount
        if self.Inventory[item] == 0:
            del self.Inventory[item]
        return True
      return False
     
     def Load(self, screen , camera):
              CurrentTile = [0,0]
              CurrentImage = None
              for y, i in enumerate(self.TileList):
                 for x, q in enumerate(i):
                      if q == 0 :
                          CurrentImage = self.Grass1
                      if q == 1 :
                          CurrentImage = self.Grass2
                      if q == 2 :
                          CurrentImage = self.FlowersW
                      if q == 3 :
                          CurrentImage = self.FlowersB
                      if q == 5 :
                          if y == 0 or self.TileList[y - 1][x] == -1 or self.TileList[y - 1][x] == 5:
                              q = 1
                              CurrentImage = self.Grass1
                          else:
                              CurrentImage = self.Seed
                      if q == 10 :
                          CurrentImage = self.TreeDown
                      if q == 11 :
                          CurrentImage = self.TreeUP
                      if q == 12 :
                          CurrentImage = self.TreeDownlight
                      if q == 13 :
                          CurrentImage = self.TreeUPlight
                      screen.blit(CurrentImage, (CurrentTile[0]- camera.offset.x ,CurrentTile[1]- camera.offset.y ))
                      CurrentTile[0] += 64 
                 CurrentTile[1] += 64
                 CurrentTile[0] = 0 
     def CheckTile(self, player):
         x = int(player.pos.x // 64)
         Xother = int((player.pos.x + player.width - 1) // 64)
         y = int(player.pos.y // 64)
         Yother = int((player.pos.y + player.height - 1) // 64)
         for y in range(y , Yother + 1):
             for x in range(x,Xother + 1):
                if self.TileList[y][x] == -1:
                    return "Water"
                if self.TileList[y][x] == 10 or self.TileList[y][x] == 11 or  self.TileList[y][x] == 12 or self.TileList[y][x] == 13:
                    return "Tree"
         return "NONE"
     def CheckClose(self, pos):
        self.DistanceHighLight = 30000
        closest = None
        player_pos = pygame.math.Vector2(pos)
        for y, row in enumerate(self.TileList):
            for x, tile in enumerate(row):
                if tile == 10 or tile == 12 :
                    self.TileList[y][x] = 10
                    self.TileList[y - 1][x] = 11
                    self.lock = False
                    dist = player_pos.distance_squared_to(pygame.math.Vector2(x * 64, y * 64))
                    if dist < self.DistanceHighLight:
                        self.DistanceHighLight = dist
                        closest = (x, y)
        if closest:
            x, y = closest
            self.TileList[y][x] = 12
            self.TileList[y - 1][x] = 13
    
         

     def Grow(self):
         Timer = pygame.time.get_ticks()
         sec = Timer/ 1000
         if sec >= self.LastTriggered:
             self.LastTriggered = sec + 30
             for y, row in enumerate(self.TileList):
                for x, tile in enumerate(row):
                    if tile == 5:
                        Chance = rng.randint(1, 4)
                        if Chance == 2:
                            self.TileList[y][x] = 10
                            self.TileList[y - 1][x] = 11
     def CutDown(self):
        for y, row in enumerate(self.TileList):
            for x, tile in enumerate(row):
                if tile == 12 :
                    self.TileList[y][x] = 1
                    self.TileList[y - 1][x] = 1
                    self.AddItem("seed")
                    self.AddItem("Wood")
     def Plant(self , player):
         x = int(player.pos.x // 64)
         Xother = int((player.pos.x + player.width - 1) // 64)
         y = int(player.pos.y // 64)
         Yother = int((player.pos.y + player.height - 1) // 64)
         for y in range(y , Yother + 1):
            for x in range(x,Xother + 1):
                if self.HasItem("seed") and self.TileList[y][x] != 5 and self.TileList[y-1][x] != 5 and self.TileList[y+1][x] != 5:
                    self.TileList[y][x] = 5
                    self.RemoveItem("seed")
                
                
        
             
