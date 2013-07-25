import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangosettings'
import control.savesLookup
from control.savesLookup        import findExistingRounds, createSettingsFile, createNewFile
import view.character
from view.character             import Character
import pygame
import math
import datetime
import time
import tiledtmxloader
from utils.AStar                import findPath, AStar
import copy
from pygame                     import *
from view.map                   import *
from logic.chance               import applyChance
from view.gui                   import *
import random
from utils.loading              import loadImage, loadImageSize
from view.scrollbar             import ScrollBar

class Test():
   
   screen             = None
   clock              = None
   camera             = None
   gameRunning        = True
   scrollBar          = ScrollBar()
   
   def __init__(self):
      
      self.scrollBar.x = 20
      self.scrollBar.y = 20
      
      self.currentGUI = StartMainMenu()
      
      pygame.init()
      self.screen = pygame.display.set_mode((500, 500))
      
      pygame.display.set_caption('Wallstreet Tycoon')
      self.clock = pygame.time.Clock()

   def exit(self):
      self.gameRunning = False
      raise SystemExit
   
   def mainLoop(self):
      
      while self.gameRunning:
         
         self.screen.fill((255,255,255))
         
         (mouseX,mouseY) = pygame.mouse.get_pos()
         (xdiff,ydiff) = (mouseX%32,mouseY%32)
      
         self.scrollBar.blit(self.screen)
      
         for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
               self.scrollBar.readEvent(event)
            if event.type == MOUSEBUTTONUP:
               self.scrollBar.readEvent(event)
            elif event.type == QUIT:
               self.exit()
            elif event.type == pygame.KEYDOWN:
               print 'keydown'
               
         pygame.display.flip()
         self.clock.tick(60)

if __name__ == '__main__':
   main = Test()
   main.mainLoop()