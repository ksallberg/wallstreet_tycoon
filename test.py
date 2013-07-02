import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'djangosettings'
import control.savesLookup
import pygame
import math
import datetime
import time

from pygame import *
from control.scheduledEvents import *

# starts the background process that simulates
# the real time price changes and bot purchases
#modelInit()

pygame.init()
screen = pygame.display.set_mode((1200, 800))
now = datetime.datetime.now()
pygame.display.set_caption(str(now))
clock = pygame.time.Clock()

while True:
   for event in pygame.event.get():
      if(event.type == KEYDOWN):
         print 'down'
         #debugPrintCompany()
      elif(event.type == KEYUP):
         print 'up'
         #debugPrintInvestors()
      
   screen.fill((0x99, 0x99, 0x99))
   
   pygame.display.flip()
   clock.tick(13)