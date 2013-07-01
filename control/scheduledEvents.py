from logic.priceManipulation import calcNewPrice
from gamemodels.models import Company
from django.db.models import Max

# Every hour of the stock, this function
# handles calculating new prices for each of
# the companies in the stock market.
def handleHour():
   
   comps = Company.objects.all()

   print str(comps)

   # For each company, find the latest price and 
   # calculate a new one
   for comp in comps:
      
      lastPrice = comp.priceHistory.all().aggregate(Max('price'))
      print "price: " + str(lastPrice)