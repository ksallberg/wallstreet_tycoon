from logic.priceManipulation     import calcNewPrice
from gamemodels.models           import Company, Stock, Investor
from django.db.models            import Max
from logic.chance                import applyChance
from logic.portfolioManipulation import buyStock, getCurrentPortfolio, sellStock

# Every hour of the stock, this function
# handles calculating new prices for each of
# the companies in the stock market.
def handleHour():
   
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
      
         # iterate through all companies, and it's a 5% chance
         # each investor will buy each stock
         for comp in comps:
            if applyChance(20):
               print 'buy stock'
               success = buyStock(investor,comp,5)
      
         # iterate through the portfolio, and apply a 20% chance of
         # selling each company
         portfolio = getCurrentPortfolio(investor)
         for entry in portfolio:
            if applyChance(20):
               
               print 'sell stock'
               
               # get the corresponding company to sell
               comp = Company.objects.get(name=entry)
               
               # then delegate the object modification
               # to sellStock
               sellStock(investor,comp,portfolio[entry])
   
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