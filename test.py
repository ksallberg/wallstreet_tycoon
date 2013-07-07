import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangosettings'
import control.savesLookup
import view.character
from view.character import Character
import pygame
import math
import datetime
import time
import tiledtmxloader
from utils.AStar import findPath, AStar
import copy
from pygame import *
from control.scheduledEvents import *
from view.map import *

# starts the background process that simulates
# the real time price changes and bot purchases
#modelInit()

def loadImage(sheet, indexX, indexY):
   rect = Rect((indexX,indexY, 32, 48))
   image = Surface(rect.size, SRCALPHA)
   image.blit(sheet, (0, 0), rect)
   image.set_colorkey(-1, RLEACCEL)
   return image

class Main():
   
   currentMap        = TownMap()
   widthInTiles      = 29
   heightInTiles     = 19
   screen            = None
   clock             = None
   charSheet         = None
   renderer          = None
   camera            = None
   mainCharPosBackup = (0,0)

   def __init__(self):
      pygame.init()
      self.screen = pygame.display.set_mode((self.widthInTiles*32, self.heightInTiles*32))
      
      pygame.display.set_caption('Wallstreet Tycoon')
      self.clock = pygame.time.Clock()

      self.charSheet = pygame.image.load(os.path.join('resources','characters.png'))

      self.renderer = tiledtmxloader.helperspygame.RendererPygame()

      self.camera = [0,0]
      self.renderer.set_camera_position_and_size(self.camera[0],self.camera[1],self.widthInTiles*32,self.heightInTiles*32,'topleft')

   def mainLoop(self):
   
      while True:
         
         (mouseX,mouseY) = pygame.mouse.get_pos()
         (xdiff,ydiff) = (mouseX%32,mouseY%32)
         
         for event in pygame.event.get():
            if   event.type == MOUSEBUTTONDOWN:
               if self.currentMap.blockingLayer.content2D[(mouseY+self.camera[1])/32][(mouseX+self.camera[0])/32] == None:
                  mc = self.currentMap.mainChar
                  mc.startpoint = ((mc.x)/32,(mc.y)/32)
                  mc.endpoint   = (pygame.mouse.get_pos()[0]/32+self.camera[0]/32,pygame.mouse.get_pos()[1] / 32+self.camera[1]/32)
                  mc.pathlines = findPath(mc.startpoint,mc.endpoint,(self.currentMap.width,self.currentMap.height),self.currentMap.aStarMap)
                  mc.setMovingPositions(mc.pathlines)
            
            elif event.type == pygame.KEYDOWN:
               if   event.key == pygame.K_UP:
                  print 'up'
               elif event.key == pygame.K_DOWN:
                  print 'down'
               elif event.key == pygame.K_RIGHT:
                  print 'right'
               elif event.key == pygame.K_LEFT:
                  print 'left'
            elif event.type == pygame.KEYUP:
               print 'up'
      
         self.camera[0] = self.currentMap.mainChar.x + 16     - (self.widthInTiles / 2) * 32 - 32
         self.camera[1] = self.currentMap.mainChar.y + 33 +16 - (self.heightInTiles / 2) * 32 - 64
      
         if self.camera[0] < 0:
            self.camera[0] = 0
         
         if self.camera[1] < 0:
            self.camera[1] = 0
         
         if self.camera[0] > (self.currentMap.width * 32) - (self.widthInTiles) * 32:
            self.camera[0] = (self.currentMap.width * 32) - (self.widthInTiles) * 32
         
         if self.camera[1] > (self.currentMap.height * 32) - (self.heightInTiles) * 32:
            self.camera[1] = (self.currentMap.height * 32) - (self.heightInTiles) * 32
         
         self.renderer.set_camera_position(self.camera[0],self.camera[1],'topleft')
      
         self.screen.fill((0, 0, 0))
      
         for sprite_layer in self.currentMap.spriteLayers:
            if sprite_layer.is_object_group:
               continue
            else:
               if sprite_layer.layer_idx != 2:
                  self.renderer.render_layer(self.screen, sprite_layer)
      
         mouseColor = None
         if self.currentMap.blockingLayer.content2D[(mouseY-ydiff+self.camera[1])/32][(mouseX-xdiff+self.camera[0])/32] == None:
            mouseColor = (0,255,255)
         else:
            mouseColor = (255,0,0)
      
         s = pygame.Surface((32,32))
         s.set_alpha(80)
         s.fill(mouseColor)
         self.screen.blit(s, (mouseX-xdiff,mouseY-ydiff))
      
         # draw characters
         for ch in self.currentMap.characters:
            chpos = ch.getOffset()
            img = loadImage(self.charSheet,
                            chpos[0],
                            chpos[1]
                           )
            self.screen.blit(img, (ch.x-self.camera[0]-16, ch.y-33-self.camera[1]))
      
         # time to teleport?
         if (self.currentMap.mainChar.x/32,self.currentMap.mainChar.y/32) in self.currentMap.teleportTiles:
         
            if self.currentMap.tag == 'town':
               self.mainCharPosBackup = (self.currentMap.mainChar.x,self.currentMap.mainChar.y)
               self.currentMap.destroy()
               self.currentMap = HouseMap()
            else:
               self.currentMap.destroy()
               self.currentMap = TownMap()
               self.currentMap.mainChar.x = self.mainCharPosBackup[0]
               self.currentMap.mainChar.y = self.mainCharPosBackup[1] + 32
            
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            pygame.time.delay(200)
            self.clock.tick(25)
            continue
         
         pygame.display.flip()
         self.clock.tick(25)
      
if __name__ == '__main__':
   main = Main()
   main.mainLoop()