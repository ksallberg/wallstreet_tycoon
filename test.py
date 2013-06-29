import pygame
from pygame import *
import math
import datetime
import time

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'djangosettings'

from gamemodels.models import *

newSkill       = Skill()
newSkill.name  = 'johnny apa'
newSkill.price = 34
newSkill.save()

skills = Skill.objects.all()

for skill in skills:
   print skill.name

pygame.init()
screen = pygame.display.set_mode((1200, 800))
now = datetime.datetime.now()
pygame.display.set_caption(str(now))
clock = pygame.time.Clock()

while True:
      
      for event in pygame.event.get():
         if(event.type == KEYDOWN):
            print 'down'
         elif(event.type == KEYUP):
            print 'up'
      
      screen.fill((0x99, 0x99, 0x99))
      
      pygame.display.flip()
      clock.tick(13)