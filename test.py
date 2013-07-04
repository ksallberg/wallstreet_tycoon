import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangosettings'
import control.savesLookup
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
screen = pygame.display.set_mode((1184, 800)) # (37*32,25*32)
now = datetime.datetime.now()
pygame.display.set_caption('Wallstreet Tycoon')
clock = pygame.time.Clock()

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
    rect = Rect((indexX,indexY, 32, 32))
    image = Surface(rect.size, SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    image.set_colorkey(-1, RLEACCEL)
    return image

def tileIdentifierToPos(id):
   {
      'rol' : (3,42), #rock left
      'ror' : (4,42), #rock right
      'rwl' : (3,44), #rock water left
      'rwr' : (4,44), #rock water right
      'flo' : 2,      #floor
      'sf1' : (3,43), #sea front continuing1
      'sf2' : (3,43), #sea front continuing2
      'sfl' : 2,      #sea front left
      'sfr' : 3,      #sea front right
   }[id]

def main():
   while True:
      for event in pygame.event.get():
         if(event.type == pygame.KEYDOWN):
            if   event.key == pygame.K_UP:
               camera[1] -= townmap.tileheight
            elif event.key == pygame.K_DOWN:
               camera[1] += townmap.tileheight
            elif event.key == pygame.K_RIGHT:
               camera[0] += townmap.tilewidth
            elif event.key == pygame.K_LEFT:
               camera[0] -= townmap.tilewidth
      
      renderer.set_camera_position(camera[0],camera[1],'topleft')
      
      screen.fill((0, 0, 0))
      
      for sprite_layer in sprite_layers:
         if sprite_layer.is_object_group:
            continue
         else:
            renderer.render_layer(screen, sprite_layer)
      
      pygame.display.flip()
      clock.tick(13)
      
if __name__ == '__main__':
   main()