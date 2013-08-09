# Author: Kristian Sallberg - kristian(at)purestyle(punkt)se
# Platform: OSX 10.7.5
# Python version: 2.7.5
# This code is my own work.

import random

# Currently randomly without heuristics
def calcNewPrice(oldPrice):
   
   #percentage is from 0.95 to 1.05
   percentage = 1 + random.random() * 0.15 - random.random() * 0.15
   
   newPrice = oldPrice * percentage
   
   return int(newPrice)