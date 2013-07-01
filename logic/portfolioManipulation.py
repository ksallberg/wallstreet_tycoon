from gamemodels.models       import *
from django.db.models        import Max

# Logics for byuing a stock
def buyStock(investor,company,amount):

   # find the last time that was entered
   lastTime = company.priceHistory.all().aggregate(Max('time'))
   
   # find a reference to that stock entry
   stockHandle = company.priceHistory.get(time=lastTime['time__max'])

   if investor.cash < stockHandle.price * amount:
      return 'transaction failed'
   else:
      # Create a new TradingRegister entry, of buy type
      # this is just to log what has happened
      entry = TradingRegister()
      entry.investor = investor
      entry.action   = 'buy'
      entry.company  = company
      entry.stock    = stockHandle
      entry.amount   = amount
      entry.save()
   
      # Create a portfolio entry, this will be used to
      # calculate profits when selling
      (obj,created) = Portfolio.objects.get_or_create(investor=investor,company=company,
                                                      defaults={'amount':amount})
      
      # if a new registry was created,
      # the amount is already set because of defaults
      # above
      if created:
         obj.save()
      # if not, then just increment the amount and
      # save
      else:
         obj.amount += amount
         obj.save()
   
      # this investor's cash is used to pay the transaction
      investor.cash -= stockHandle.price * amount
      investor.save()
      return 'transaction complete'

def sellStock(investor,company,amount):
   
   # find the last time that was entered
   lastTime = company.priceHistory.all().aggregate(Max('time'))
   
   # find a reference to that stock entry
   stockHandle = company.priceHistory.get(time=lastTime['time__max'])
   
   entry = TradingRegister()
   entry.investor = investor
   entry.action   = 'sell'
   entry.company  = company
   entry.stock    = stockHandle
   entry.amount   = amount
   entry.save()
   
   # delete from the portfolio entry to clear
   # it from the list of owned stocks
   portEntry = Portfolio.objects.get(investor=investor,company=company)
   
   if(portEntry.amount - amount < 0):
      print 'PORTFOLIOMANIPULATION: SELL STOCK: ERROR: SELLING MORE THAN OWNED!'
   else:
      portEntry.amount = portEntry.amount - amount
      portEntry.save()
   
   # to speed up getCurrentPortfolio
   portEntry.amount == 0
   portEntry.delete()
   
   investor.cash += stockHandle.price * amount
   investor.save()
   
def getCurrentPortfolio(investor):
   
   # get all stocks this investor currently owns
   portfolio = Portfolio.objects.filter(investor=investor)
   
   return map((lambda obj: (obj.company.name,obj.amount)),portfolio)
   
def calcCurrentPortfolioWorth(investor):
   
   # get all stocks this investor currently owns
   portfolio = Portfolio.objects.filter(investor=investor)
   totSum = 0
   
   for portfolioEntry in portfolio:
      # find the last time that was entered
      lastTime = portfolioEntry.company.priceHistory.all().aggregate(Max('time'))
   
      # find a reference to that stock entry
      stockHandle = portfolioEntry.company.priceHistory.get(time=lastTime['time__max'])
   
      totSum += stockHandle.price * portfolioEntry.amount
   
   return totSum