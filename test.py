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

currentMap = TownMap()

widthInTiles  = 29
heightInTiles = 19

pygame.init()
screen = pygame.display.set_mode((widthInTiles*32, heightInTiles*32))
now = datetime.datetime.now()
pygame.display.set_caption('Wallstreet Tycoon')
clock = pygame.time.Clock()

charSheet = pygame.image.load(os.path.join('resources','characters.png'))

renderer = tiledtmxloader.helperspygame.RendererPygame()

camera = [0,0]
renderer.set_camera_position_and_size(camera[0],camera[1],widthInTiles*32,heightInTiles*32,'topleft')

def loadImage(sheet, indexX, indexY):
    rect = Rect((indexX,indexY, 32, 48))
    image = Surface(rect.size, SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    image.set_colorkey(-1, RLEACCEL)
    return image

def main():
   while True:
      for event in pygame.event.get():
         if   event.type == MOUSEBUTTONDOWN:
            if currentMap.blockingLayer.content2D[(mouseY-bb+camera[1])/32][(mouseX-aa+camera[0])/32] == None:
               mc = currentMap.mainChar
               mc.startpoint = ((mc.x)/32,(mc.y)/32)
               mc.endpoint   = (pygame.mouse.get_pos()[0]/32+camera[0]/32,pygame.mouse.get_pos()[1] / 32+camera[1]/32)
               mc.pathlines = findPath(mc.startpoint,mc.endpoint,(currentMap.width,currentMap.height),currentMap.aStarMap)
               mc.setMovingPositions(mc.pathlines)
            
         elif event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_UP and camera[1] > 0:
               camera[1] -= townmap.tileheight
            elif event.key == pygame.K_DOWN and camera[1] < 2400:
               camera[1] += townmap.tileheight
            elif event.key == pygame.K_RIGHT and camera[0] < 2016:
               camera[0] += townmap.tilewidth
            elif event.key == pygame.K_LEFT  and camera[0] > 0:
               camera[0] -= townmap.tilewidth
         elif event.type == pygame.KEYUP:
            print 'up'
      
      camera[0] = currentMap.mainChar.x + 16 - (widthInTiles / 2) * 32 - 32
      camera[1] = currentMap.mainChar.y + 33 +16 - (heightInTiles / 2) * 32 - 64
      
      if camera[0] < 0:
         camera[0] = 0
         
      if camera[1] < 0:
         camera[1] = 0
         
      if camera[0] > (currentMap.width * 32) - (widthInTiles) * 32:
         camera[0] = (currentMap.width * 32) - (widthInTiles) * 32
         
      if camera[1] > (currentMap.height * 32) - (heightInTiles) * 32:
         camera[1] = (currentMap.height * 32) - (heightInTiles) * 32
         
      renderer.set_camera_position(camera[0],camera[1],'topleft')
      
      screen.fill((0, 0, 0))
      
      for sprite_layer in currentMap.spriteLayers:
         if sprite_layer.is_object_group:
            continue
         else:
            if sprite_layer.layer_idx != 2:
               renderer.render_layer(screen, sprite_layer)
      
      (mouseX,mouseY) = pygame.mouse.get_pos()
      
      (xdiff,ydiff) = (mouseX%32,mouseY%32)
      
      mouseColor = None
      if currentMap.blockingLayer.content2D[(mouseY-ydiff+camera[1])/32][(mouseX-xdiff+camera[0])/32] == None:
         mouseColor = (0,255,255)
      else:
         mouseColor = (255,0,0)
      
      s = pygame.Surface((32,32))
      s.set_alpha(80)
      s.fill(mouseColor)
      screen.blit(s, (mouseX-xdiff,mouseY-ydiff))
      
      # draw characters
      for ch in currentMap.characters:
         chpos = ch.getOffset()
         img = loadImage(charSheet,
                         chpos[0],
                         chpos[1]
                        )
         screen.blit(img, (ch.x-camera[0]-16, ch.y-33-camera[1]))
      
      pygame.display.flip()
      clock.tick(25)
      
if __name__ == '__main__':
   main()