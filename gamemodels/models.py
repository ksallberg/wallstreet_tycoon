# Using Djano's ORM, this is the definitions
# of the models used in the game.

from django.db import models

# This is a table that for each stock, 
# holds a history of prices
class Stock(models.Model):
   # For now, time is measured just in integers
   # didn't want to make sure it's daytime, not weekend etc
   time  = models.IntegerField()
   price = models.IntegerField()
   
   def __unicode__(self):
      return str(self.time)

# Each company has a name, a history of prices 
# and some cash
class Company(models.Model):
   name         = models.CharField(max_length=100)
   priceHistory = models.ManyToManyField(Stock)
   cash         = models.IntegerField()
   ticker       = models.CharField(max_length=3)
   shares       = models.IntegerField() #how many shares are outstanding

   def __unicode__(self):
      return self.name
      
# The player, and opponents, are modeled as 
# investors with some cash and a name
# 
# The portfolio is stored as
# a number of TradingRegister rows
class Investor(models.Model):
   name      = models.CharField(max_length=100)
   cash      = models.IntegerField()
   type      = models.CharField(max_length=6) #should be 'bot' or 'player'
   sprite    = models.CharField(max_length=100) #identifier of this player's sprite
   
   def __unicode__(self):
      return self.name

# Instead of an investor owning a portfolio,
# I let the portfolio represent a table where
# Companies are connected to investors, AND
# where the amount of shares owned are stated
class Portfolio(models.Model):
   investor  = models.ForeignKey(Investor)
   amount    = models.IntegerField()
   company   = models.ForeignKey(Company)

# Keeps track of all stocks that are sold
# and bought. To be able to see what
# players did during the game 
#
# This is not read from in the game, just
# for storage and for fun
class TradingRegister(models.Model):
   investor  = models.ForeignKey(Investor)
   action    = models.CharField(max_length=4) #should be 'buy' or 'sell'
   company   = models.ForeignKey(Company)
   stock     = models.ForeignKey(Stock)
   amount    = models.IntegerField()