import os

from logic.priceManipulation     import calcNewPrice
from gamemodels.models           import Company, Stock, Investor
from django.db.models            import Max
from logic.chance                import applyChance
from logic.portfolioManipulation import *
from django.db                   import connection
from utils.timer                 import RepeatedTimer
from subprocess                  import call
from utils.loading               import Loader
from logic.generation            import *

# start up the game
def modelInit(playerInput,mainRef):
   if connection.introspection.table_names() == [] and playerInput != None:
      print 'save file does NOT exist'
      
      call(["python", "manage.py", "syncdb"])
      
      # load names to create
      loader           = Loader()
      compNameSettings = loader.loadJSON(os.path.join('json','company_names.json'))
      inveNameSettings = loader.loadJSON(os.path.join('json','investor_names.json'))
      companyNames     = []
      investorNames    = []
      
      for i in range(1,50): #create 50 companies
         newCompany = generateCompanyName(compNameSettings,companyNames)
         companyNames.append(newCompany)
      
      for i in range(1,16): #create 16 investors
         newInvestor = generateInvestorName(inveNameSettings,investorNames)
         investorNames.append(newInvestor)
   
      generateNewRound(companyNames,investorNames,playerInput)
      
   rt = RepeatedTimer(20,handleHour,mainRef) # 10 game seconds is one hour
   handleHour(mainRef)
   return rt

# Every hour of the stock, this function
# handles calculating new prices for each of
# the companies in the stock market.
def handleHour(mainRef):
   
   comps = Company.objects.all()

   # For each company, find the latest price and 
   # calculate a new one
   for comp in comps:
      
      # find the last time that was entered
      lastTime = comp.priceHistory.all().aggregate(Max('time'))
      
      # find the price associated with that time
      lastEntry = comp.priceHistory.get(time=lastTime['time__max'])
      
      # If the company's stock price is 0
      # the company is in bancruptcy
      if lastEntry.price > 0:
      
         newEntry = Stock()
         newEntry.time = lastEntry.time + 1
         newEntry.price = calcNewPrice(lastEntry.price)
         newEntry.save()
      
         comp.priceHistory.add(newEntry)
         comp.save()
      
   print 'new prices calculated'
   
   investors = Investor.objects.all()
   
   # For each investor, except the player, 
   # make some random buys and sells
   for investor in investors:
      
      # don't do this for the player
      if investor.type == 'bot':
      
         # iterate through all companies, and it's a 20% chance
         # each investor will buy each stock
         for comp in comps:
            if applyChance(2):
               success = buyStock(investor,comp,100)
      
         # iterate through the portfolio, and apply a 50% chance of
         # selling each company
         portfolio = getCurrentPortfolio(investor)
         for entry in portfolio:
            if applyChance(20):
               
               # get the corresponding company to sell
               comp = Company.objects.get(name=entry[0])
               
               # then delegate the object modification
               # to sellStock
               sellStock(investor,comp,entry[1])
   
   # get the current cash amount of the investor
   if mainRef.currentMap.characters != None:
      
      for ch in mainRef.currentMap.characters:
      
         inv           = Investor.objects.get(name=ch.name)
         investorStock = calcCurrentPortfolioWorth(inv)
         totalCapital  = investorStock + inv.cash
      
         ch.setTempTotalCapital(totalCapital)

def debugPrintCompany():
   
   comps = Company.objects.all()

   # For each company, find the latest price and
   # calculate a new one
   for comp in comps:
      
      print 'company: ' + comp.name
      
      priceHist = comp.priceHistory.all()
      
      for stock in priceHist:
         
         print '  :::' + str(stock.price)
      
   print 'new prices calculated'
   
def debugPrintInvestors():
   
   investors = Investor.objects.all()
   
   for investor in investors:
      
      print 'investor: ' + investor.name