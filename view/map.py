from view.character import *
import tiledtmxloader

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
      
      self.teleportTiles = [(14,19),(29,21),(39,19),(60,19),(72,19),(84,19),(95,14),
                            (10,49),(17,49),(35,49),(42,49),(56,49),(87,49),(96,82),
                            (87,92),(80,84),(56,84),(42,84),(10,84)]
      
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
   
   def injectCharacters(self,investors):
      
      #print investors
      for investor in investors:
         if investor.type == 'bot':
            char = Character()
            char.x = 26 * 32 + 16
            char.y = 29 * 32 + 16
            char.setType(self.mapPlayerToSprite(investor.sprite))
            self.characters.append(char)
         elif investor.type == 'player':
            char = Character()
            char.x = self.mainSpawnPos[0]
            char.y = self.mainSpawnPos[1]
            char.setType(self.mapPlayerToSprite(investor.sprite))
            self.characters.append(char)
            self.mainChar = char
         else:
            print 'town map! wrong player type!'
      """
      char = Character()
      #char.x = 3*32+16
      #char.y = 10*32+16
      char.setType(char.type3)
      char.startpoint = (3,10)
      self.characters.append(char)
      self.mainChar = char

      char2 = Character()
      #char2.x = 26 * 32 + 16
      #char2.y = 29 * 32 + 16
      char2.setType(char2.type2)
      self.characters.append(char2)

      char3 = Character()
      #char3.x = 46 * 32 + 16
      #char3.y = 41 * 32 + 16
      char3.setType(char3.type3)
      self.characters.append(char3)

      char4 = Character()
      #char4.x = 44 * 32 + 16
      #char4.y = 64 * 32 + 16
      char4.setType(char4.type4)
      self.characters.append(char4)

      char5 = Character()
      #char5.x = 73 * 32 + 16
      #char5.y = 63 * 32 + 16
      char5.setType(char5.type5)
      self.characters.append(char5)

      char6 = Character()
      #char6.x = 72 * 32 + 16
      #char6.y = 88 * 32 + 16
      char6.setType(char6.type6)
      self.characters.append(char6)

      char7 = Character()
      #char7.x = 13 * 32 + 16
      #char7.y = 90 * 32 + 16
      char7.setType(char7.type7)
      self.characters.append(char7)

      char8 = Character()
      char8.x = 16 * 32 + 16
      char8.y = 66 * 32 + 16
      char8.setType(char8.type8)
      self.characters.append(char8)
      """
class HouseMap(AbstractMap):
   
   def __init__(self):
      AbstractMap.__init__(self)
      self.tag = 'house'
      
      self.teleportTiles = [(13,18),(14,18)]
      
      self.setWidthInTiles(29)
      self.setHeightInTiles(19)
      
      char = Character()
      char.x = 13*32+16
      char.y = 17*32+16
      char.startpoint = (3,10)
      char.setType(char.type3)
      self.characters.append(char)
      self.mainChar = char
      
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