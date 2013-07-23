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
from control.scheduledEvents    import *
from view.map                   import *
from logic.chance               import applyChance
from view.gui                   import *
from gamemodels.models          import  Investor

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

class Main():
   
   STATE_START_SCREEN       = 'stateStartScreen'
   STATE_CHARACTER_CREATION = 'stateCharacterCreation'
   STATE_CHARACTER_LOADING  = 'stateCharacterLoading'
   STATE_GAME_MODE          = 'stateGameMode'
   
   currentState       = STATE_START_SCREEN # initialize with the start screen
   currentMap         = TownMap()
   widthInTiles       = 29
   heightInTiles      = 19
   screen             = None
   clock              = None
   charSheet          = None
   renderer           = None
   camera             = None
   mainCharPosBackup  = (0,0)
   charClippingOffset = 32
   repeatedTimer      = None
   mainMenu           = MainMenu()
   currentGUI         = None
   gameRunning        = True
   startScreen        = StartScreen()
   

   def __init__(self):
      
      self.currentGUI = StartMainMenu()
      
      pygame.init()
      self.screen = pygame.display.set_mode((self.widthInTiles*32, self.heightInTiles*32))
      
      pygame.display.set_caption('Wallstreet Tycoon')
      self.clock = pygame.time.Clock()

      self.charSheet = pygame.image.load(os.path.join('resources','characters.png'))

      self.renderer = tiledtmxloader.helperspygame.RendererPygame()

      self.camera = [0,0]
      self.renderer.set_camera_position_and_size(self.camera[0],self.camera[1],self.widthInTiles*32,self.heightInTiles*32,'topleft')
   
   def exit(self):
      self.gameRunning = False
      if self.repeatedTimer != None:
         self.repeatedTimer.stop()
      raise SystemExit
   
   def renderStartScreen(self):
      self.screen.fill((0,0,0))
      
      # draw background for the frame
      s = pygame.Surface((560,560))
      s.fill((34, 16, 94))
      self.screen.blit(s, (190,30))
      
      (mouseX,mouseY) = pygame.mouse.get_pos()
      (xdiff,ydiff) = (mouseX%32,mouseY%32)
      
      # Draw the main menu
      startScreenImg = loadImageSize(self.startScreen.sheet,
                                     0,
                                     0,
                                     self.startScreen.width,
                                     self.startScreen.height
                                    )
      self.screen.blit(startScreenImg, (167, 8))
         
      interfacesImg = loadImageSize(self.currentGUI.sheet,
                                    0,
                                    0,
                                    self.currentGUI.width,
                                    self.currentGUI.height
                                   )
      self.screen.blit(interfacesImg, (self.currentGUI.x, self.currentGUI.y))
      
      if self.currentState == self.STATE_CHARACTER_CREATION:
         self.currentGUI.drawExtras(self.screen,None)
      elif self.currentState == self.STATE_CHARACTER_LOADING:
         self.currentGUI.drawExtras(self.screen,None)
         
      for event in pygame.event.get():
         if event.type == MOUSEBUTTONDOWN:
            
            btn = self.currentGUI.findPressed(mouseX,mouseY)
            
            # some sort of event handling for the start screen
            if btn != None:
               print btn.label
               if btn.label == 'createChar':
                  self.currentGUI   = CharacterCreation()
                  self.currentState = self.STATE_CHARACTER_CREATION
               elif btn.label == 'backToMenu':
                  self.currentGUI   = StartMainMenu()
                  self.currentState = self.STATE_START_SCREEN
               elif btn.label == 'exit':
                  self.exit()
               elif btn.label[:4] == 'char' or btn.label[:7] == 'loading':
                  self.currentGUI.setSelector(btn.label)
               elif btn.label == 'loadChar':
                  self.currentGUI   = CharacterLoading()
                  self.currentGUI.injectLoadData(findExistingRounds())
                  self.currentState = self.STATE_CHARACTER_LOADING
               elif btn.label == 'doLoad':
                  if self.currentGUI.currentSelected != None:
                     createSettingsFile(self.currentGUI.wantedSaveName)
                     self.repeatedTimer = modelInit(None)
                     self.currentState = self.STATE_GAME_MODE
               elif btn.label == 'saveChar':
                  #createNewFile()
                  self.repeatedTimer = modelInit((self.currentGUI.name,self.currentGUI.character))
                  self.currentMap.injectCharacters(Investor.objects.all())
                  self.currentState = self.STATE_GAME_MODE
                     
         elif event.type == QUIT:
            self.exit()
         
         elif event.type == pygame.KEYDOWN:
            
            if self.currentState == self.STATE_CHARACTER_CREATION:
               self.currentGUI.addNameChar(pygame.key.name(event.key))
            
            if   event.key == K_k:
               print 'k!'
            elif event.key == pygame.K_DOWN:
               'down'
            elif event.key == pygame.K_RIGHT:
               print 'right'
            elif event.key == pygame.K_LEFT:
               print 'left'
         elif event.type == pygame.KEYUP:
            'up'
   
   def renderMap(self):
      (mouseX,mouseY) = pygame.mouse.get_pos()
      (xdiff,ydiff) = (mouseX%32,mouseY%32)
   
      for event in pygame.event.get():
         if   event.type == MOUSEBUTTONDOWN:
         
            # if the main menu is used
            if (mouseX >= self.mainMenu.x and mouseX <= self.mainMenu.x + self.mainMenu.width and
                mouseY >= self.mainMenu.y and mouseY <= self.mainMenu.y + self.mainMenu.height
               ):
               if self.mainMenu.isOpen:
               
                  btn = self.mainMenu.findPressed(mouseX,mouseY)
               
                  if btn != None:
                     if btn.label == 'exit':
                        self.exit()
                  
                  self.mainMenu.close()
               else:
                  self.mainMenu.open()
         
            elif self.currentMap.blockingLayer.content2D[(mouseY+self.camera[1])/32][(mouseX+self.camera[0])/32] == None:
               mc = self.currentMap.mainChar
               mc.startpoint = ((mc.x)/32,(mc.y)/32)
               mc.endpoint   = (pygame.mouse.get_pos()[0]/32+self.camera[0]/32,pygame.mouse.get_pos()[1] / 32+self.camera[1]/32)
               mc.pathlines = findPath(mc.startpoint,mc.endpoint,(self.currentMap.width,self.currentMap.height),self.currentMap.aStarMap)
               mc.setMovingPositions(mc.pathlines)
      
         elif event.type == QUIT:
            self.exit()
         
         elif event.type == pygame.KEYDOWN:
            if   event.key == K_k:
               print 'k!'
            elif event.key == pygame.K_DOWN:
               print 'down'
            elif event.key == pygame.K_RIGHT:
               print 'right'
            elif event.key == pygame.K_LEFT:
               print 'left'
         elif event.type == pygame.KEYUP:
            print 'up'

      self.camera[0] = self.currentMap.mainChar.x + 16     - (self.widthInTiles / 2)  * 32 - 32
      self.camera[1] = self.currentMap.mainChar.y + 33 +16 - (self.heightInTiles / 2) * 32 - 64

      if self.camera[0] < 0:
         self.camera[0] = 0
   
      if self.camera[1] < 0:
         self.camera[1] = 0
   
      if self.camera[0] > (self.currentMap.width * 32) - (self.widthInTiles) * 32:
         self.camera[0] = (self.currentMap.width * 32) - (self.widthInTiles) * 32
   
      if self.camera[1] > (self.currentMap.height * 32) - (self.heightInTiles) * 32:
         self.camera[1] = (self.currentMap.height * 32) - (self.heightInTiles) * 32
   
      self.renderer.set_camera_position(self.camera[0],self.camera[1],'topleft')

      self.screen.fill((0, 0, 0))

      for sprite_layer in self.currentMap.spriteLayers:
         if sprite_layer.is_object_group:
            continue
         else:
            if sprite_layer.layer_idx != 2:
               self.renderer.render_layer(self.screen, sprite_layer)

      mouseColor = None
      if self.currentMap.blockingLayer.content2D[(mouseY-ydiff+self.camera[1])/32][(mouseX-xdiff+self.camera[0])/32] == None:
         mouseColor = (0,255,255)
      else:
         mouseColor = (255,0,0)

      s = pygame.Surface((32,32))
      s.set_alpha(80)
      s.fill(mouseColor)
      self.screen.blit(s, (mouseX-xdiff,mouseY-ydiff))

      # draw characters
      for ch in self.currentMap.characters:
      
         chpos = ch.getOffset()
      
         #character clipping!
         if (ch.x >= self.camera[0] - self.charClippingOffset and
             ch.x <= self.camera[0] + self.widthInTiles  * 32 + self.charClippingOffset and
             ch.y >= self.camera[1] - self.charClippingOffset and
             ch.y <= self.camera[1] + self.heightInTiles * 32 + self.charClippingOffset):
          
            img = loadImage(self.charSheet,
                            chpos[0],
                            chpos[1]
                           )
            self.screen.blit(img, (ch.x-self.camera[0]-16, ch.y-33-self.camera[1]))
      
            # walk somewhere?
            if ch != self.currentMap.mainChar:
               if applyChance(5):
                  if ch.movingPositions == []:
                     ch.startpoint = ((ch.x)/32,(ch.y)/32)
                     ch.endpoint   = (ch.startpoint[0]+random.randint(0,10)-random.randint(0,10),ch.startpoint[1]+random.randint(0,10)-random.randint(0,10))
                     if (ch.endpoint[0] < self.currentMap.width and
                        ch.endpoint[1] < self.currentMap.height and
                        ch.endpoint[0] > 0 and ch.endpoint[1] > 0):
                     # if the endpoint is a valid point, let's go there!
                        if self.currentMap.blockingLayer.content2D[ch.endpoint[1]][ch.endpoint[0]] == None:
                           ch.pathlines = findPath(ch.startpoint,ch.endpoint,(self.currentMap.width,self.currentMap.height),self.currentMap.aStarMap)
                           ch.setMovingPositions(ch.pathlines)
               
      # time to teleport?
      if (self.currentMap.mainChar.x/32,self.currentMap.mainChar.y/32) in self.currentMap.teleportTiles:
   
         if self.currentMap.tag == 'town':
            self.mainCharPosBackup = (self.currentMap.mainChar.x,self.currentMap.mainChar.y)
            self.currentMap.destroy()
            self.currentMap = HouseMap()
         else:
            self.currentMap.destroy()
            self.currentMap = TownMap()
            self.currentMap.injectCharacters(Investor.objects.all())
            self.currentMap.mainChar.x = self.mainCharPosBackup[0]
            self.currentMap.mainChar.y = self.mainCharPosBackup[1] + 32 + 16
      
         self.screen.fill((0, 0, 0))
         pygame.time.delay(200)
         
   
      # Draw the main menu
      mainMenuImg = loadImageSize(self.mainMenu.sheet,
                                  0,
                                  0,
                                  self.mainMenu.width,
                                  self.mainMenu.height
                                 )
      self.screen.blit(mainMenuImg, (10, 10))
   
   def mainLoop(self):
   
      while self.gameRunning:
         
         if (self.currentState == self.STATE_START_SCREEN       or
             self.currentState == self.STATE_CHARACTER_CREATION or
             self.currentState == self.STATE_CHARACTER_LOADING
            ):
            self.renderStartScreen()
         elif self.currentState == self.STATE_GAME_MODE:
            self.renderMap()
         else:
            print 'ERROR: Main class: In an Unsupported State!'
         
         pygame.display.flip()
         self.clock.tick(25)

if __name__ == '__main__':
   main = Main()
   main.mainLoop()