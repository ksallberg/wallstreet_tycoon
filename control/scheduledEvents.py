from logic.priceManipulation import calcNewPrice
from gamemodels.models import Company, Stock
from django.db.models import Max

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
      
      newEntry = Stock()
      newEntry.time = lastEntry.time + 1
      newEntry.price = calcNewPrice(lastEntry.price)
      newEntry.save()
      
      comp.priceHistory.add(newEntry)
      comp.save()
      
   print 'new prices calculated'
   
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