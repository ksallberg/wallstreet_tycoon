import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'djangosettings'
import control.savesLookup
import pygame
from pygame import *
import math
import datetime
import time
from django.db import connection

from subprocess import call

from utils.loading import Loader
from logic.generation import *

from control.scheduledEvents import handleHour

if connection.introspection.table_names() == []:
   print 'save file DOES NOT exist'
   
   call(["python", "manage.py", "syncdb"])
   
   # load names to create
   compNamesLoader = Loader()
   nameSettings    = compNamesLoader.loadJSON('json/company_names.json')
   companyNames    = []
   for i in range(1,100): #create 100 companies
      newComp = generateCompanyName(nameSettings,companyNames)
      companyNames.append(newComp)
   
   generateNewRound(companyNames)

from utils.timer import RepeatedTimer
rt = RepeatedTimer(5,handleHour) # 10 game seconds is one hour

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