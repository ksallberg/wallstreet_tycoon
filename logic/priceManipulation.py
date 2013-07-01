import random

# Currently completely randomly without heuristics
def calcNewPrice(oldPrice):
   
   #percentage is from 0.95 to 1.05
   percentage = 1 + random.random() * 0.05 - random.random() * 0.05
   
   newPrice = oldPrice * percentage
   
   return int(newPrice)