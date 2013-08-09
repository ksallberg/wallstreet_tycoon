# Author: Kristian Sallberg - kristian(at)purestyle(punkt)se
# Platform: OSX 10.7.5
# Python version: 2.7.5
# This code is my own work.

from view.character import *
import tiledtmxloader
from random import choice

class AbstractMap():
   
   width             = 0
   height            = 0
   characters        = []
   mainChar          = None
   mapFile           = ''
   resources         = None
   spriteLayers      = None
   blockingLayer     = None
   aStarMap          = []
   teleportTiles     = []
   tag               = ''
   
   def __init__(self):
      self.resources  = tiledtmxloader.helperspygame.ResourceLoaderPygame()
      self.characters = []
      self.aStarMap   = []
   
   def setWidthInTiles(self,width):
      self.width = width
      
   def setHeightInTiles(self,height):
      self.height = height
      
   def destroy(self):
      self.width = 0
      self.height = 0
      self.characters    = []
      self.mainChar      = None
      self.mapFile       = ''
      self.resources     = None
      self.spriteLayers  = None
      self.blockingLayer = None
      self.aStarMap      = []
      self.teleportTiles = []
      self.tag           = ''
      
   def mapPlayerToSprite(self,spriteName):
      if   spriteName == 'char1':
         return Character.type1
      elif spriteName == 'char2':
         return Character.type2
      elif spriteName == 'char3':
         return Character.type3
      elif spriteName == 'char4':
         return Character.type4
      elif spriteName == 'char5':
         return Character.type5
      elif spriteName == 'char6':
         return Character.type6
      elif spriteName == 'char7':
         return Character.type7
      elif spriteName == 'char8':
         return Character.type8

class TownMap(AbstractMap):
   
   #spawn positions as (x,y)
   spawnPositions = [(26 * 32 + 16,29 * 32 + 16),
                     (46 * 32 + 16,41 * 32 + 16),
                     (44 * 32 + 16,64 * 32 + 16),
                     (73 * 32 + 16,63 * 32 + 16),
                     (72 * 32 + 16,88 * 32 + 16),
                     (13 * 32 + 16,90 * 32 + 16),
                     (16 * 32 + 16,66 * 32 + 16)
                    ]
   
   mainSpawnPos   = (3*32+16,10*32+16)
   
   def __init__(self):
      AbstractMap.__init__(self)
      self.tag = 'town'
      
      self.teleportTiles = [(14,19),(29,21),(39,19),(60,19),(72,19),
                            (84,19),(95,14),(10,49),(17,49),(35,49),
                            (42,49),(56,49),(87,49),(96,82),(87,92),
                            (80,84),(56,84),(42,84),(10,84)]
      
      self.setWidthInTiles(100)
      self.setHeightInTiles(100)
      
      self.mapFile = tiledtmxloader.tmxreader.TileMapParser().parse_decode(os.path.join('resources','town.tmx'))
      self.resources.load(self.mapFile)
      self.spriteLayers = tiledtmxloader.helperspygame.get_layers_from_map(self.resources)
      
      # testing blocking layers
      for layer in self.spriteLayers:
         if layer.layer_idx == 2:
            self.blockingLayer = layer
      
      for i in range(0,self.height):
         for j in range(0,self.width):
            if self.blockingLayer.content2D[i][j] == None:
               self.aStarMap.append(1)
            else:
               self.aStarMap.append(-1)
   
   def injectCharacters(self,investors):
      
      #print investors
      for investor in investors:
         
         # create character for the map
         char = Character()
         spawnPos = choice(self.spawnPositions) #random spawnign position
         char.x = spawnPos[0]
         char.y = spawnPos[1]
         char.setType(self.mapPlayerToSprite(investor.sprite))
         char.setName(investor.name)
         
         if investor.type == 'player':
            char.x = self.mainSpawnPos[0]
            char.y = self.mainSpawnPos[1]
            self.mainChar = char
            
         self.characters.append(char)
      
      # when creating the map, insert all the current total capital
      # to the characters, this is needed before the model thread
      # gets access to the characters
      for ch in self.characters:
         
         from gamemodels.models           import Investor
         from logic.portfolioManipulation import calcCurrentPortfolioWorth
         
         inv           = Investor.objects.get(name=ch.name)
         investorStock = calcCurrentPortfolioWorth(inv)
         totalCapital  = investorStock + inv.cash
      
         ch.setTempTotalCapital(totalCapital)
      
class HouseMap(AbstractMap):
   
   def __init__(self):
      AbstractMap.__init__(self)
      self.tag = 'house'
      
      self.teleportTiles = [(13,18),(14,18)]
      
      self.setWidthInTiles(29)
      self.setHeightInTiles(19)
      
      self.mapFile = tiledtmxloader.tmxreader.TileMapParser().parse_decode(os.path.join('resources','insidehouse.tmx'))
      self.resources.load(self.mapFile)
      self.spriteLayers = tiledtmxloader.helperspygame.get_layers_from_map(self.resources)
      
      # testing blocking layers
      for layer in self.spriteLayers:
         if layer.layer_idx == 2:
            self.blockingLayer = layer
            
      for i in range(0,self.height):
         for j in range(0,self.width):
            if self.blockingLayer.content2D[i][j] == None:
               self.aStarMap.append(1)
            else:
               self.aStarMap.append(-1)
               
   def injectMainCharacter(self,investor):
      char = Character()
      char.x = 13*32+16
      char.y = 17*32+16
      char.startpoint = (3,10)
      char.setType(self.mapPlayerToSprite(investor.sprite))
      char.setName(investor.name)
      self.characters.append(char)
      self.mainChar = char
      
      # when creating the map, insert the current total
      # capital to the character this is needed before 
      # the model thread gets access to the characters
      from gamemodels.models           import Investor
      from logic.portfolioManipulation import calcCurrentPortfolioWorth
         
      inv           = Investor.objects.get(name=char.name)
      investorStock = calcCurrentPortfolioWorth(inv)
      totalCapital  = investorStock + inv.cash
      
      char.setTempTotalCapital(totalCapital)