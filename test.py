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

from pygame import *
from control.scheduledEvents import *

# starts the background process that simulates
# the real time price changes and bot purchases
#modelInit()

pygame.init()
screen = pygame.display.set_mode((1184, 800))
now = datetime.datetime.now()
pygame.display.set_caption('Wallstreet Tycoon')
clock = pygame.time.Clock()

characters = []

char = Character()
char.x = 100
char.y = 100
char.setType(char.type4)
characters.append(char)

char2 = Character()
char2.x = 200
char2.y = 100
char2.setType(char2.type2)
characters.append(char2)

char3 = Character()
char3.x = 300
char3.y = 100
char3.setType(char3.type3)
characters.append(char3)

char4 = Character()
char4.x = 400
char4.y = 100
char4.setType(char4.type4)
characters.append(char4)

char5 = Character()
char5.x = 500
char5.y = 100
char5.setType(char5.type5)
characters.append(char5)

char6 = Character()
char6.x = 600
char6.y = 100
char6.setType(char6.type6)
characters.append(char6)

char7 = Character()
char7.x = 700
char7.y = 100
char7.setType(char7.type7)
characters.append(char7)

char8 = Character()
char8.x = 800
char8.y = 100
char8.setType(char8.type8)
characters.append(char8)

charSheet = pygame.image.load('resources/characters.png')

"""
map!
"""

townmap = tiledtmxloader.tmxreader.TileMapParser().parse_decode('resources/town.tmx')

resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
resources.load(townmap)

townmap.orientation = 'orthogonal'

renderer = tiledtmxloader.helperspygame.RendererPygame()

camera = [0,0]

renderer.set_camera_position_and_size(camera[0],camera[1],1184,800,'topleft')

sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

"""
map!
"""

def loadImage(sheet, indexX, indexY):
    rect = Rect((indexX,indexY, 32, 48))
    image = Surface(rect.size, SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    image.set_colorkey(-1, RLEACCEL)
    return image

def main():
   while True:
      for event in pygame.event.get():
         if event.type == pygame.KEYDOWN:
            characters[0].setState(char.STATE_WALKING)
            if   event.key == pygame.K_UP and camera[1] > 0:
               camera[1] -= townmap.tileheight
               characters[0].setDir("north")
            elif event.key == pygame.K_DOWN and camera[1] < 2400:
               camera[1] += townmap.tileheight
               characters[0].setDir("south")
            elif event.key == pygame.K_RIGHT and camera[0] < 2016:
               camera[0] += townmap.tilewidth
               characters[0].setDir("east")
            elif event.key == pygame.K_LEFT  and camera[0] > 0:
               camera[0] -= townmap.tilewidth
               characters[0].setDir("west")
         elif event.type == pygame.KEYUP:
            characters[0].setState(char.STATE_STANDING)
      
      renderer.set_camera_position(camera[0],camera[1],'topleft')
      
      screen.fill((0, 0, 0))
      
      for sprite_layer in sprite_layers:
         if sprite_layer.is_object_group:
            continue
         else:
            renderer.render_layer(screen, sprite_layer)
      
      (mouseX,mouseY) = pygame.mouse.get_pos()
      (aa,bb) = (mouseX%32,mouseY%32)
      
      s = pygame.Surface((32,32))
      s.set_alpha(80)
      s.fill((0,255,255))
      screen.blit(s, (mouseX-aa,mouseY-bb))
      
      # draw characters
      for ch in characters:
         chpos = ch.getOffset()
         img = loadImage(charSheet,
                         chpos[0],
                         chpos[1]
                        )
         screen.blit(img, (ch.x, ch.y))
      
      pygame.display.flip()
      clock.tick(60)
      
if __name__ == '__main__':
   main()