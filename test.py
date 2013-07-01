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

from control.scheduledEvents import handleHour, debugPrintCompany, debugPrintInvestors

if connection.introspection.table_names() == []:
   print 'save file DOES NOT exist'
   
   call(["python", "manage.py", "syncdb"])
   
   # load names to create
   loader           = Loader()
   compNameSettings = loader.loadJSON('json/company_names.json')
   inveNameSettings = loader.loadJSON('json/investor_names.json')
   companyNames     = []
   investorNames    = []
   
   for i in range(1,50): #create 50 companies
      newCompany = generateCompanyName(compNameSettings,companyNames)
      companyNames.append(newCompany)
   
   for i in range(1,3): #create 3 investors
      newInvestor = generateInvestorName(inveNameSettings,investorNames)
      investorNames.append(newInvestor)
   
   generateNewRound(companyNames,investorNames)

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
            #debugPrintCompany()
         elif(event.type == KEYUP):
            print 'up'
            #debugPrintInvestors()
      
      screen.fill((0x99, 0x99, 0x99))
      
      pygame.display.flip()
      clock.tick(13)