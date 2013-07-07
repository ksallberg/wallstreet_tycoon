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
from utils import AStar
import copy
from pygame import *
from control.scheduledEvents import *

# starts the background process that simulates
# the real time price changes and bot purchases
#modelInit()

widthInTiles  = 29#37
heightInTiles = 20

totalWidthInTiles  = 100
totalHeightInTiles = 100

pygame.init()
screen = pygame.display.set_mode((widthInTiles*32, heightInTiles*32))
now = datetime.datetime.now()
pygame.display.set_caption('Wallstreet Tycoon')
clock = pygame.time.Clock()

characters = []

char = Character()
char.x = 1*32
char.y = 20*32
char.setType(char.type8)
characters.append(char)

char2 = Character()
char2.x = 34 * 32
char2.y = 20 * 32
char2.setType(char2.type2)
characters.append(char2)

char3 = Character()
char3.x = 26 * 32
char3.y = 50 * 32
char3.setType(char3.type3)
characters.append(char3)

char4 = Character()
char4.x = 24 * 32
char4.y = 78 * 32
char4.setType(char4.type4)
characters.append(char4)

char5 = Character()
char5.x = 83 * 32
char5.y = 85 * 32
char5.setType(char5.type5)
characters.append(char5)

char6 = Character()
char6.x = 93 * 32
char6.y = 93 * 32
char6.setType(char6.type6)
characters.append(char6)

char7 = Character()
char7.x = 88 * 32
char7.y = 69 * 32
char7.setType(char7.type7)
characters.append(char7)

char8 = Character()
char8.x = 73 * 32
char8.y = 20 * 32
char8.setType(char8.type8)
characters.append(char8)

charSheet = pygame.image.load(os.path.join('resources','characters.png'))

"""
map!
"""

townmap = tiledtmxloader.tmxreader.TileMapParser().parse_decode(os.path.join('resources','town.tmx'))

resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
resources.load(townmap)

renderer = tiledtmxloader.helperspygame.RendererPygame()

camera = [0,0]



renderer.set_camera_position_and_size(camera[0],camera[1],widthInTiles*32,heightInTiles*32,'topleft')

sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

aStarMap = []
blockingLayer = None
global startpoint
startpoint = (6,14)
#endpoint   = (31,14)
global endpoint
endpoint   = (14,19)
global pathlines
pathlines = []



# testing blocking layers
for layer in sprite_layers:
   if layer.layer_idx == 2:
      blockingLayer = layer

for i in range(0,totalHeightInTiles):#heightInTiles):
   for j in range(0,totalWidthInTiles):#widthInTiles):
      
      if i == startpoint[0] and j == startpoint[1]:
         aStarMap.append(5)
      elif i == endpoint[0] and j == endpoint[1]:
         aStarMap.append(6)
      else:
         
         if blockingLayer.content2D[i][j] == None:
            aStarMap.append(1)
         else:
            aStarMap.append(-1)




"""
map!
"""

def findPath():
   astar = AStar.AStar(AStar.SQ_MapHandler(aStarMap,totalWidthInTiles,totalHeightInTiles))
   start = AStar.SQ_Location(startpoint[0],startpoint[1])
   end   = AStar.SQ_Location(endpoint[0],endpoint[1])
   
   p = astar.findPath(start,end)

   if not p:
      print 'No path found!'
   else:
      #print 'Path found!' + str(len(p.nodes))
      _pathlines = []
      _pathlines.append((start.x*32+16,start.y*32+16))
      for n in p.nodes:
          _pathlines.append((n.location.x*32+16,n.location.y*32+16))
      _pathlines.append((end.x*32+16,end.y*32+16))

      return _pathlines

pathlines = findPath()
char.setMovingPositions(copy.deepcopy(pathlines))

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
            if blockingLayer.content2D[(mouseY-bb+camera[1])/32][(mouseX-aa+camera[0])/32] == None:
               global endpoint
               global startpoint
               startpoint = ((char.x)/32,(char.y)/32)
               endpoint   = (pygame.mouse.get_pos()[0]/32+camera[0]/32,pygame.mouse.get_pos()[1] / 32+camera[1]/32)#(round(camera[0]/32+pygame.mouse.get_pos()[0] / 32),round(camera[1]/32+pygame.mouse.get_pos()[1] / 32))
               #print "new endpoint" + str(endpoint)
               global pathlines
               pathlines = findPath()
               char.setMovingPositions(copy.deepcopy(pathlines))
            
            #print camera
            
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
      
      camera[0] = char.x + 16 - (widthInTiles / 2) * 32
      camera[1] = char.y + 33 +16 - (heightInTiles / 2) * 32
      
      if camera[0] < 0:
         camera[0] = 0
         
      if camera[1] < 0:
         camera[1] = 0
         
      if camera[0] > (totalWidthInTiles * 32) - (widthInTiles) * 32:
         camera[0] = (totalWidthInTiles * 32) - (widthInTiles) * 32
         
      if camera[1] > (totalHeightInTiles * 32) - (heightInTiles) * 32:
         camera[1] = (totalHeightInTiles * 32) - (heightInTiles) * 32
         
      renderer.set_camera_position(camera[0],camera[1],'topleft')
      
      screen.fill((0, 0, 0))
      
      for sprite_layer in sprite_layers:
         if sprite_layer.is_object_group:
            continue
         else:
            if sprite_layer.layer_idx != 2:
               renderer.render_layer(screen, sprite_layer)
      
      (mouseX,mouseY) = pygame.mouse.get_pos()
      
      (aa,bb) = (mouseX%32,mouseY%32)
      
      mouseColor = None
      
      #if blockingLayer.content2D[(mouseX+camera[0]-(camera[0]%32))/32][(mouseY+camera[1]-(camera[1]%32))/32] == None:
      
      if blockingLayer.content2D[(mouseY-bb+camera[1])/32][(mouseX-aa+camera[0])/32] == None:
         mouseColor = (0,255,255)
      else:
         mouseColor = (255,0,0)
      
      s = pygame.Surface((32,32))
      s.set_alpha(80)
      s.fill(mouseColor)
      screen.blit(s, (mouseX-aa,mouseY-bb))
      
      # draw characters
      for ch in characters:
         chpos = ch.getOffset()
         img = loadImage(charSheet,
                         chpos[0],
                         chpos[1]
                        )
         screen.blit(img, (ch.x-camera[0]-16, ch.y-33-camera[1]))
      
      #pathlines = findPath()
      
#      if pathlines and len(pathlines) > 0:
#         pygame.draw.lines(screen, (255,255,255,255), 0, [(x-camera[0],y-camera[1]) for (x,y) in pathlines])
      
      pygame.display.flip()
      clock.tick(25)
      
if __name__ == '__main__':
   main()