import pygame
from pygame import *
import math
import datetime
import time
from time import gmtime, strftime
from subprocess import call

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'djangosettings'

from utils.loading import Loader
from utils.roundCreator import *
from utils.generation import generateCompanyName

compNamesLoader = Loader()
nameSettings    = compNamesLoader.loadJSON('json/company_names.json')
companyNames    = []
for i in range(1,100):
   newComp = generateCompanyName(nameSettings,companyNames)
   companyNames.append(newComp)

print companyNames
raise SystemExit

if findExistingRounds() == []:
   print 'save file DOES NOT exist'
   currTime = 'saves/'+strftime("%Y-%m-%d-%H-%M-%S", gmtime())+'.sqlite'
   createSettingsFile(currTime)
   call(["python", "manage.py", "syncdb"])
   createNewRound()
else:
   print 'save file exists'
   fileName = 'saves/'+findExistingRounds()[0]
   createSettingsFile(fileName)


from gamemodels.models import *
comps = Company.objects.all()

for comp in comps:
   print comp.name

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