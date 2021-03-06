# Author: Kristian Sallberg - kristian(at)purestyle(punkt)se
# Platform: OSX 10.7.5
# Python version: 2.7.5
# This code is my own work.

import json
from pygame                     import *

# functions to cut sub surfaces from sheets

def loadImage(sheet, indexX, indexY):
   rect = Rect((indexX,indexY, 32, 48))
   image = Surface(rect.size, SRCALPHA)
   image.blit(sheet, (0, 0), rect)
   image.set_colorkey(-1, RLEACCEL)
   return image

def loadImageSize(sheet, x, y, w, h):
   rect = Rect((x, y, w, h))
   image = Surface(rect.size, SRCALPHA)
   image.blit(sheet, (0, 0), rect)
   image.set_colorkey(-1, RLEACCEL)
   return image

# Class to load the JSON file
class Loader():
   def loadJSON(self,fileName):
      json_data = None
      try:
         json_data = open(fileName)
      except IOError:
         print 'Could not load JSON file!'
         return None
      data = json.load(json_data)
      json_data.close()
      return data