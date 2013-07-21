import os
from pygame import *
import pygame

class Button():
   x      = 0
   y      = 0
   width  = 0
   heigth = 0
   label  = ''

class AbstractGUI(Button):
   
   buttons = []
   
   sheet  = ''
   
   def findPressed(self,x,y):
      for button in self.buttons:
         if (x >= button.x and x <= button.x + button.width and
             y >= button.y and y <= button.y + button.height):
             return button
      return None
            
class MainMenu(AbstractGUI):
   
   maxHeight = 208
   minHeight = 41
   width     = 135
   height    = minHeight
   isOpen    = False
   sheet     = pygame.image.load(os.path.join('resources','menu.png'))
   
   def __init__(self):
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
      self.isOpen = True
      
   def close(self):
      self.height = self.minHeight
      self.isOpen = False