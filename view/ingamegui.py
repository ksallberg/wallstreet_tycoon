from gamemodels.models           import Company, Stock, Investor
from logic.portfolioManipulation import *
from django.db.models            import Max
from view.gui                    import *
import os
import pygame
import math
from pygame                     import *
from utils.loading              import loadImageSize
from view.scrollbar             import ScrollBar
from math                       import fabs, floor

class MarketGUI(AbstractGUI):
   
   width               = 326
   height              = 517
   x                   = 375
   y                   = 28
   sheet               = pygame.image.load(os.path.join('resources','marketGUI.png'))
   buyButtonSheet      = pygame.image.load(os.path.join('resources','buyButton.png'))
   buyButtonImage      = None
   
   scrollbar           = ScrollBar()
   scrolledContentYTop = 119
   scrolledContentY    = 0
   
   guiRowDist          = 23
   roundCounter        = 0
   
   buyStockGUI         = BuyStock()
   buyStockOpen        = False
   buyAmount           = ''
   buttonPressed       = 0
   
   def __init__(self):
      
      self.scrollbar.x = 669
      self.scrollbar.y = 119
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
      
      self.buyButtonImage = loadImageSize(self.buyButtonSheet,
                                          0,
                                          0,
                                          127,
                                          42
                                         )
      
      closeBtn        = Button()
      closeBtn.x      = 379
      closeBtn.y      = 483
      closeBtn.width  = 185
      closeBtn.height = 60
      closeBtn.label  = 'closeGUI'
      self.buttons.append(closeBtn)
      
      companies = Company.objects.all()
      self.cacheList = pygame.Surface((500,len(companies)*(self.guiRowDist*6)-self.guiRowDist), pygame.SRCALPHA, 32)
      self.cacheList = self.cacheList.convert_alpha()
   
   # override to find when the user has pressed buy
   def findPressed(self,x,y):
      
      if self.buyStockOpen:
         
         if x >= 335 and x <= 335+127 and y >= 332 and y <= 332+41:
            self.buyStockOpen = False
         elif x >= 466 and x <= 466+127 and y >= 332 and y <= 332+41:
            
            #register the buy in the model
            
            player                   = Investor.objects.get(type='player')
            
#            portfolio                = getCurrentPortfolio(player)
            
            
            
            company                  = Company.objects.get(id=int(self.buttonPressed+1))
            
            print company
            
            buyStock(player,company,int(self.buyAmount))
            
            # add the stock
 #           portfolioEntity          = Portfolio()
 #           portfolioEntity.investor = player
 #           portfolioEntity.amount   = int(buyAmount)
 #           portfolioEntity.company  = company
 #           portfolioEntity.save()
            
            self.buyStockOpen = False
            
      else:
      
         for button in self.buttons:
         
            if x >= 504 and x <= 631:
               relativePosition = (y + (-self.scrolledContentY) + self.scrolledContentYTop - 155)%138 #the position in the entire Surface
                                                                                  #self.scrolledContentY will be positive at first and then negative
            
               if relativePosition >= 0 and relativePosition <= 38:
               
                  #138 pixels between every button
                  self.buttonPressed = floor(((-self.scrolledContentY)+y)/138)
                  self.buyStockOpen = True
                  self.buyAmount = '' # reset this pop up gui
               
            if (x >= button.x and x <= button.x + button.width and
                y >= button.y and y <= button.y + button.height):
                return button
         
      return None
   
   def readEvent(self,event):
      self.scrollbar.readEvent(event)
      
      if self.buyStockOpen:
         
         # This is listening to the text field
         if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == 'backspace':
               self.buyAmount = self.buyAmount[:-1]
            elif pygame.key.name(event.key) in ['1','2','3','4','5','6','7','8','9','0'] and len(self.buyAmount) < 5:
               self.buyAmount += pygame.key.name(event.key)
      
   def drawExtra(self,screen):
      
      self.scrollbar.blit(screen)
      
      companies = Company.objects.all()
      self.scrolledContentY = self.scrolledContentYTop - ((len(companies)*(self.guiRowDist*6))-self.guiRowDist) * self.scrollbar.percentage + 336 * self.scrollbar.percentage
      
      if self.roundCounter == 0:
         
         s = pygame.Surface((500,len(companies)*(self.guiRowDist*6)), pygame.SRCALPHA, 32)
         s = s.convert_alpha()
         
         i = 0
         for company in companies:
            
            s.blit(self.buyButtonImage,(275,i*self.guiRowDist+35))
            
            font  = pygame.font.SysFont('monospace',16)
            label = font.render(company.name, 1, (255,255,255))
            s.blit(label,(0,i*self.guiRowDist))
         
            font  = pygame.font.SysFont('monospace',16)
            label = font.render('cash:'+str(company.cash), 1, (255,255,255))
            s.blit(label,(0,(i+1)*self.guiRowDist))
         
            font  = pygame.font.SysFont('monospace',16)
            label = font.render('ticker:'+company.ticker, 1, (255,255,255))
            s.blit(label,(0,(i+2)*self.guiRowDist))
         
            font  = pygame.font.SysFont('monospace',16)
            label = font.render('number of shares:'+str(company.shares), 1, (255,255,255))
            s.blit(label,(0,(i+3)*self.guiRowDist))
         
            lastTime = company.priceHistory.all().aggregate(Max('time'))
            currentPrice = company.priceHistory.get(time=lastTime['time__max'])
         
            font  = pygame.font.SysFont('monospace',16)
            label = font.render('price:'+str(currentPrice), 1, (255,255,255))
            s.blit(label,(0,(i+4)*self.guiRowDist))
            i += 6
         
         self.cacheList.fill(0)
         self.cacheList.blit(s,(0,0))
         
      screen.blit(self.cacheList, (227,self.scrolledContentYTop),Rect(0,self.scrolledContentYTop-self.scrolledContentY,415,336))
      
      if self.buyStockOpen:
         screen.blit(self.buyStockGUI.image,(self.buyStockGUI.x,self.buyStockGUI.y))
         
         font  = pygame.font.SysFont('monospace',20)
         label = font.render(self.buyAmount, 1, (78,49,11))
         screen.blit(label,(408,282))
         
      #increment roundCounter for next round
      if self.roundCounter < 100:
         self.roundCounter += 1
      else:
         self.roundCounter = 0
      
class PortfolioGUI(AbstractGUI):
   
   width     = 326
   height    = 517
   x         = 375
   y         = 28
   sheet     = pygame.image.load(os.path.join('resources','portfolioGUI.png'))
   scrollbar = ScrollBar()
   
   def __init__(self):
      
      self.scrollbar.x = 669
      self.scrollbar.y = 119
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
      
      closeBtn        = Button()
      closeBtn.x      = 379
      closeBtn.y      = 483
      closeBtn.width  = 185
      closeBtn.height = 60
      closeBtn.label  = 'closeGUI'
      self.buttons.append(closeBtn)
      
   def readEvent(self,event):
      self.scrollbar.readEvent(event)
      
   def drawExtra(self,screen):
      self.scrollbar.blit(screen)
      
class OpponentsGUI(AbstractGUI):
   
   width               = 326
   height              = 517
   x                   = 375
   y                   = 28
   sheet               = pygame.image.load(os.path.join('resources','opponentsGUI.png'))
   scrollbar           = ScrollBar()
   scrolledContentYTop = 119
   scrolledContentY    = 0
   
   guiRowDist          = 23
   roundCounter        = 0
   
   cacheList           = None #used to optimize drawing of texts
   
   def __init__(self):
      
      self.scrollbar.x = 669
      self.scrollbar.y = 119
      
      self.image = loadImageSize(self.sheet,
                                 0,
                                 0,
                                 self.width,
                                 self.height
                                )
      
      closeBtn        = Button()
      closeBtn.x      = 379
      closeBtn.y      = 483
      closeBtn.width  = 185
      closeBtn.height = 60
      closeBtn.label  = 'closeGUI'
      self.buttons.append(closeBtn)
      
      investors = Investor.objects.all()
      self.cacheList = pygame.Surface((500,len(investors)*self.guiRowDist+self.guiRowDist), pygame.SRCALPHA, 32)
      self.cacheList = self.cacheList.convert_alpha()
      
   def readEvent(self,event):
      self.scrollbar.readEvent(event)
   
   # this function is optimized to only redraw the
   # texts each 100:th round
   def drawExtra(self,screen):
      
      self.scrollbar.blit(screen)
      
      investors = Investor.objects.all()
      self.scrolledContentY = self.scrolledContentYTop - ((len(investors)*self.guiRowDist)+self.guiRowDist) * self.scrollbar.percentage + 336 * self.scrollbar.percentage

      if self.roundCounter == 0:
      
         h = len(investors)*self.guiRowDist
      
         s = pygame.Surface((500,len(investors)*self.guiRowDist+self.guiRowDist), pygame.SRCALPHA, 32)
         s = s.convert_alpha()
      
         font  = pygame.font.SysFont('monospace',16)
         label = font.render('Investor:', 1, (255,255,255))
         s.blit(label,(0,0))
      
         font  = pygame.font.SysFont('monospace',16)
         label = font.render('Cash:', 1, (255,255,255))
         s.blit(label,(200,0))
      
         font  = pygame.font.SysFont('monospace',16)
         label = font.render('Stock:', 1, (255,255,255))
         s.blit(label,(275,0))
      
         font  = pygame.font.SysFont('monospace',16)
         label = font.render('Total:', 1, (255,255,255))
         s.blit(label,(350,0))
      
         i = 1
         for investor in investors:
            font  = pygame.font.SysFont('monospace',16)
            label = font.render(investor.name, 1, (255,255,255))
            s.blit(label,(0,i*self.guiRowDist))
         
            investorStock = calcCurrentPortfolioWorth(investor)
            totalCapital  = investorStock + investor.cash
         
            font  = pygame.font.SysFont('monospace',16)
            label = font.render(str(investor.cash), 1, (255,255,255))
            s.blit(label,(200,i*self.guiRowDist))
         
            font  = pygame.font.SysFont('monospace',16)
            label = font.render(str(investorStock), 1, (255,255,255))
            s.blit(label,(275,i*self.guiRowDist))
         
            font  = pygame.font.SysFont('monospace',16)
            label = font.render(str(totalCapital), 1, (255,255,255))
            s.blit(label,(350,i*self.guiRowDist))
            i += 1
      
         self.cacheList.fill(0)
         self.cacheList.blit(s,(0,0))
      
      screen.blit(self.cacheList, (227,self.scrolledContentYTop),Rect(0,self.scrolledContentYTop-self.scrolledContentY,415,336))
      
      #increment roundCounter for next round
      if self.roundCounter < 100:
         self.roundCounter += 1
      else:
         self.roundCounter = 0