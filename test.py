import pygame
from pygame import *
import math
import datetime
import time
from time import gmtime, strftime
from subprocess import call
from django.conf import settings

from utils.roundCreator import *

currTime = 'saves/'+strftime("%Y-%m-%d-%H-%M-%S", gmtime())+'.sqlite'

if findExistingRounds() == []:
   print 'save file DOES NOT exist'
   createSettingsFile(currTime)
   #createNewRound()
#   dbName = 'saves/'+currTime+'.sqlite'
   
   #djangosettings.DATABASES['default']['NAME'] = 'novo_banco'#'saves/'+currTime+'.sqlite'
   call(["python", "manage.py", "syncdb"])
else:
   print 'save file exists'
   fileName = 'saves/'+findExistingRounds()[0]
   createSettingsFile(fileName)

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'djangosettings'

from gamemodels.models import *
#createNewRound()

#newSkill       = Skill()
#newSkill.name  = 'johnny apa'
#newSkill.price = 34
#newSkill.save()

#skills = Skill.objects.all()

#for skill in skills:
#   print skill.name

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