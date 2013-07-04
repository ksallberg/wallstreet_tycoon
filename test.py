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

def main():
   while True:
      for event in pygame.event.get():
         if(event.type == pygame.KEYDOWN):
            if   event.key == pygame.K_UP and camera[1] > 0:
               camera[1] -= townmap.tileheight
            elif event.key == pygame.K_DOWN and camera[1] < 2400:
               camera[1] += townmap.tileheight
            elif event.key == pygame.K_RIGHT and camera[0] < 2016:
               camera[0] += townmap.tilewidth
            elif event.key == pygame.K_LEFT  and camera[0] > 0:
               camera[0] -= townmap.tilewidth
      
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
      
      pygame.display.flip()
      clock.tick(13)
      
if __name__ == '__main__':
   main()