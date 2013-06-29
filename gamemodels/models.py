# Using Djano's ORM, this is the definitions
# of the models used in the game.

from django.db import models

# This is a table that for each stock, 
# holds a history of prices
class Stock(models.Model):
   time  = models.DateTimeField('event_time')
   price = models.IntegerField()
   
   def __unicode__(self):
      return str(self.time)

# Each company has a name, a history of prices 
# and some cash
class Company(models.Model):
   name         = models.CharField(max_length=100)
   priceHistory = models.ManyToManyField(Stock)
   lastPrice    = models.ForeignKey(Stock,related_name='last_price')
   cash         = models.IntegerField()

   def __unicode__(self):
      return self.name

# A collection of companies
class Portfolio(models.Model):
   name      = models.CharField(max_length=100)
   companies = models.ManyToManyField(Company)
   
   def __unicode__(self):
      return self.name
      
# The player, and opponents, are modeled as 
# investors with some cash, a name and a portfolio
class Investor(models.Model):
   name      = models.CharField(max_length=100)
   portfolio = models.ForeignKey(Portfolio)
   cash      = models.IntegerField()
   
   def __unicode__(self):
      return self.name