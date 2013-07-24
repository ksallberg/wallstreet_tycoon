import os
import pygame
from pygame                     import *
from utils.loading              import loadImage, loadImageSize

class ScrollBar:
   
   sheet         = pygame.image.load(os.path.join('resources','scrollDragger.png'))
   image         = None
   width         = 32
   maxHeight     = 300
   draggerHeight = 36
   y             = 0
   x             = 0
   draggerX      = 0
   draggerY      = 0
   mouseYOffset  = 0 # if pressing lower than 0 on the dragger
                     # this prevents the dragger from jumping down
   dragging      = False
   percentage    = 0.0
   
   def __init__(self):
      
      self.dwiheifwhefiuheiufheiuf = 23
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 32,
                                 36
                                )
                                
   def readEvent(self,event):
      
      #(mouseX,mouseY) = pygame.mouse.get_pos()
      
      #if mouse is down and over the dragger:
      if event.type == MOUSEBUTTONDOWN:
         if (event.pos[0] - self.x >= self.draggerX and event.pos[0] - self.x <= self.draggerX + self.width and
             event.pos[1] - self.y >= self.draggerY and event.pos[1] - self.y <= self.draggerY + self.draggerHeight
            ):
            self.mouseYOffset = event.pos[1] - self.draggerY
            
            self.dragging = True
            
      if event.type == MOUSEBUTTONUP:
         self.dragging = False
      
   def blit(self,screen):
      
      (mouseX,mouseY) = pygame.mouse.get_pos()
      
      if self.dragging:
         
         self.draggerY = mouseY - self.mouseYOffset
         
         if self.draggerY  >= self.maxHeight - self.draggerHeight:
            self.draggerY   = self.maxHeight - self.draggerHeight
         
         if self.draggerY  <= 0:
            self.draggerY = 0
         
      self.percentage = float(float(self.draggerY) / (self.maxHeight-self.draggerHeight))
      
      print self.percentage
      
      # draw background for the frame
      s = pygame.Surface((32,self.maxHeight))
      s.fill((34, 16, 94, 10))
      screen.blit(s, (self.x,self.y))
      
      screen.blit(self.image, (self.draggerX+self.x, self.draggerY+self.y))