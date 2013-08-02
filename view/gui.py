import os
import pygame
import math
from math                       import ceil
from pygame                     import *
from utils.loading              import loadImageSize
from view.scrollbar             import ScrollBar


class Button():
   x      = 3
   y      = 0
   width  = 0
   heigth = 0
   label  = ''

class AbstractGUI(Button):
   
   buttons = []
   
   sheet  = ''
   image  = None
   
   def __init__(self):
      self.buttons = []
   
   def drawExtras(self,screen,input):
      print 'draw extras'
   
   def findPressed(self,x,y):
      
      for button in self.buttons:
         if (x >= button.x and x <= button.x + button.width and
             y >= button.y and y <= button.y + button.height):
             return button
      return None
      
   def readEvent(self,event):
      print 'readEvent'

class StartScreen(AbstractGUI):
   
   width     = 600
   height    = 600
   sheet     = pygame.image.load(os.path.join('resources','menuFrame.png'))
   
   def __init__(self):
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )

class BuyStock(AbstractGUI):
   
   x         = 310
   y         = 216
   width     = 310
   height    = 182
   sheet     = pygame.image.load(os.path.join('resources','stockBuy.png'))
   
   def __init__(self):
      AbstractGUI.__init__(self)
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )

class SellStock(AbstractGUI):
   
   x         = 310
   y         = 216
   width     = 310
   height    = 182
   sheet     = pygame.image.load(os.path.join('resources','stockSell.png'))
   
   def __init__(self):
      AbstractGUI.__init__(self)
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )

class StartMainMenu(AbstractGUI):
   
   x         = 355
   y         = 28
   width     = 219
   height    = 465
   sheet     = pygame.image.load(os.path.join('resources','startMainMenu.png'))
   
   def __init__(self):
      AbstractGUI.__init__(self)
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
      
      loadCharacter        = Button()
      loadCharacter.x      = 360
      loadCharacter.y      = 160
      loadCharacter.width  = 228
      loadCharacter.height = 80
      loadCharacter.label  = 'loadChar'
      self.buttons.append(loadCharacter)
      
      createCharacter        = Button()
      createCharacter.x      = 360
      createCharacter.y      = 252
      createCharacter.width  = 228
      createCharacter.height = 80
      createCharacter.label  = 'createChar'
      self.buttons.append(createCharacter)
      
      instructions        = Button()
      instructions.x      = 360
      instructions.y      = 355
      instructions.width  = 228
      instructions.height = 80
      instructions.label  = 'instructions'
      self.buttons.append(instructions)
      
      exit        = Button()
      exit.x      = 360
      exit.y      = 421
      exit.width  = 228
      exit.height = 80
      exit.label  = 'exit'
      self.buttons.append(exit)

class CharacterLoading(AbstractGUI):
   x                 = 222
   y                 = 28
   width             = 486
   height            = 516
   currentSelected   = None
   
   wantedSaveName    = ''
   saveFiles         = []
   
   sheet             = pygame.image.load(os.path.join('resources','loadCharacter.png'))
   selectorSheet     = pygame.image.load(os.path.join('resources','selector.png'))
   
   selectorImage     = None
   
   index             = 0
   
   def __init__(self):
      AbstractGUI.__init__(self)
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
                                
      self.selectorImage = loadImageSize(self.selectorSheet,
                                         0,
                                         0,
                                         24,
                                         25
                                        )
      
      self.saveFiles = []    
      backBtn        = Button()
      backBtn.x      = 271
      backBtn.y      = 56
      backBtn.width  = 65
      backBtn.height = 44
      backBtn.label  = 'backBtn'
      self.buttons.append(backBtn)
      
      forwBtn        = Button()
      forwBtn.x      = 607
      forwBtn.y      = 56
      forwBtn.width  = 65
      forwBtn.height = 44
      forwBtn.label  = 'forwBtn'
      self.buttons.append(forwBtn)
      
      btn1        = Button()
      btn1.x      = 225
      btn1.y      = 115
      btn1.width  = 607
      btn1.height = 56
      btn1.label  = 'loading1'
      self.buttons.append(btn1)
      
      btn2        = Button()
      btn2.x      = 225
      btn2.y      = 185
      btn2.width  = 607
      btn2.height = 56
      btn2.label  = 'loading2'
      self.buttons.append(btn2)
      
      btn3        = Button()
      btn3.x      = 225
      btn3.y      = 254
      btn3.width  = 607
      btn3.height = 56
      btn3.label  = 'loading3'
      self.buttons.append(btn3)
      
      btn4        = Button()
      btn4.x      = 225
      btn4.y      = 326
      btn4.width  = 607
      btn4.height = 56
      btn4.label  = 'loading4'
      self.buttons.append(btn4)
      
      btn5        = Button()
      btn5.x      = 225
      btn5.y      = 396
      btn5.width  = 607
      btn5.height = 56
      btn5.label  = 'loading5'
      self.buttons.append(btn5)
      
      menuBtn        = Button()
      menuBtn.x      = 246
      menuBtn.y      = 470
      menuBtn.width  = 216
      menuBtn.height = 72
      menuBtn.label  = 'backToMenu'
      self.buttons.append(menuBtn)
      
      loadBtn        = Button()
      loadBtn.x      = 468
      loadBtn.y      = 470
      loadBtn.width  = 216
      loadBtn.height = 72
      loadBtn.label  = 'doLoad'
      self.buttons.append(loadBtn)
      
   def injectLoadData(self,data):
      self.saveFiles = data
      self.setSelector('loading1') #the first
      
   def drawExtras(self,screen,input):
      spaceCounter = 0 # just to simplify placing texts on the screen
      endLoopAt = self.index * 5 + 5 # end the loop at index + 5
                                   # which draws max 5 files
      if endLoopAt > len(self.saveFiles):
         endLoopAt = len(self.saveFiles)
      for i in range(self.index*5,endLoopAt):
         font  = pygame.font.SysFont('monospace',20)
         label = font.render(self.saveFiles[i], 1, (78,49,11))
         screen.blit(label,(262,130+spaceCounter*70))
         spaceCounter += 1
         
      if self.currentSelected != None:
         screen.blit(self.selectorImage, (688, 128 + self.currentSelected*71))
   
   # checks that it's safe to select the wanted button as
   # the current selected load file
   def setSelector(self,number):
      if len(self.saveFiles) > (int(number[7])-1) + self.index * 5:
         self.currentSelected = int(number[7])-1 #take the number from the name and subtract 1 to make it an index
         self.wantedSaveName  = self.saveFiles[self.currentSelected + self.index * 5]
   
   # index is to determine which files to draw if more then
   # five save files exist...
   def incIndex(self):
      if self.index < (len(self.saveFiles)-1) / 5:
         self.index += 1
         self.setSelector('loading1') # a little hack to make the selector go to the top
   
   def decIndex(self):
      if self.index > 0:
         self.index -= 1
         self.setSelector('loading1')
   
class CharacterCreation(AbstractGUI):
   
   char1Name = 'char1'
   char2Name = 'char2'
   char3Name = 'char3'
   char4Name = 'char4'
   char5Name = 'char5'
   char6Name = 'char6'
   char7Name = 'char7'
   char8Name = 'char8'
   
   x                 = 230
   y                 = 28
   width             = 427
   height            = 504
   sheet             = pygame.image.load(os.path.join('resources','charCreation.png'))
   selectorSheet     = pygame.image.load(os.path.join('resources','selector.png'))
   selectorPos       = (302,330)
   
   selectorImage     = None
   
   defaultName       = 'Player'
   name              = ''
   character         = char1Name
   
   def __init__(self):
      
      AbstractGUI.__init__(self)
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
                                
      self.selectorImage = loadImageSize(self.selectorSheet,
                                         0,
                                         0,
                                         24,
                                         25
                                        )
      
      menuBtn        = Button()
      menuBtn.x      = 270
      menuBtn.y      = 479
      menuBtn.width  = 162
      menuBtn.height = 60
      menuBtn.label  = 'backToMenu'
      self.buttons.append(menuBtn)
      
      saveBtn        = Button()
      saveBtn.x      = 495
      saveBtn.y      = 479
      saveBtn.width  = 162
      saveBtn.height = 60
      saveBtn.label  = 'saveChar'
      self.buttons.append(saveBtn)
      
      char1        = Button()
      char1.x      = 290
      char1.y      = 266
      char1.width  = 60
      char1.height = 70
      char1.label  = self.char1Name
      self.buttons.append(char1)
      
      char2        = Button()
      char2.x      = 384
      char2.y      = 266
      char2.width  = 60
      char2.height = 70
      char2.label  = self.char2Name
      self.buttons.append(char2)
      
      char3        = Button()
      char3.x      = 478
      char3.y      = 266
      char3.width  = 60
      char3.height = 70
      char3.label  = self.char3Name
      self.buttons.append(char3)
      
      char4        = Button()
      char4.x      = 577
      char4.y      = 266
      char4.width  = 60
      char4.height = 70
      char4.label  = self.char4Name
      self.buttons.append(char4)
      
      char5        = Button()
      char5.x      = 289
      char5.y      = 364
      char5.width  = 60
      char5.height = 70
      char5.label  = self.char5Name
      self.buttons.append(char5)
      
      char6        = Button()
      char6.x      = 388
      char6.y      = 364
      char6.width  = 60
      char6.height = 70
      char6.label  = self.char6Name
      self.buttons.append(char6)
      
      char7        = Button()
      char7.x      = 478
      char7.y      = 364
      char7.width  = 60
      char7.height = 70
      char7.label  = self.char7Name
      self.buttons.append(char7)
      
      char8        = Button()
      char8.x      = 579
      char8.y      = 364
      char8.width  = 60
      char8.height = 70
      char8.label  = self.char8Name
      self.buttons.append(char8)
      
   def addNameChar(self,char):
      
      if len(char) == 1 or char == 'backspace': # only count chars of len1 and backspace
         if char == 'backspace':
            self.name = self.name[:len(self.name)-1]
         elif len(self.name) < 16:
            self.name += str(char)
   
   def drawExtras(self,screen,input):
      
      screen.blit(self.selectorImage, (self.selectorPos[0], self.selectorPos[1]))
      
      font  = pygame.font.SysFont('monospace',20)
      label = font.render(self.name, 1, (78,49,11))
      screen.blit(label,(262,164))
   
   def setSelector(self,character):
      
      self.character = character
      
      if character == self.char1Name:
         self.selectorPos = (302,330)
      elif character == self.char2Name:
         self.selectorPos = (399,330)
      elif character == self.char3Name:
         self.selectorPos = (495,330)
      elif character == self.char4Name:
         self.selectorPos = (591,330)
      elif character == self.char5Name:
         self.selectorPos = (302,425)
      elif character == self.char6Name:
         self.selectorPos = (399,425)
      elif character == self.char7Name:
         self.selectorPos = (495,425)
      elif character == self.char8Name:
         self.selectorPos = (591,425)
         
class MainMenu(AbstractGUI):
   
   maxHeight = 208
   minHeight = 41
   width     = 135
   height    = minHeight
   isOpen    = False
   sheet     = pygame.image.load(os.path.join('resources','menu.png'))
   image     = None
   
   def __init__(self):
      AbstractGUI.__init__(self)
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
      
      portfolioBtn        = Button()
      portfolioBtn.x      = 0
      portfolioBtn.y      = 44
      portfolioBtn.width  = 132
      portfolioBtn.height = 40
      portfolioBtn.label  = 'portfolio'
      self.buttons.append(portfolioBtn)
      
      opponentsBtn        = Button()
      opponentsBtn.x      = 0
      opponentsBtn.y      = 90
      opponentsBtn.width  = 132
      opponentsBtn.height = 40
      opponentsBtn.label  = 'opponents'
      self.buttons.append(opponentsBtn)
      
      marketBtn        = Button()
      marketBtn.x      = 0
      marketBtn.y      = 134
      marketBtn.width  = 132
      marketBtn.height = 40
      marketBtn.label  = 'market'
      self.buttons.append(marketBtn)
      
      exitBtn        = Button()
      exitBtn.x      = 0
      exitBtn.y      = 172
      exitBtn.width  = 132
      exitBtn.height = 40
      exitBtn.label  = 'exit'
      self.buttons.append(exitBtn)
      
   def open(self):
      self.height = self.maxHeight
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
      self.isOpen = True
      
   def close(self):
      self.height = self.minHeight
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
      self.isOpen = False