# Author: Kristian Sallberg - kristian(at)purestyle(punkt)se
# Platform: OSX 10.7.5
# Python version: 2.7.5
# This code is my own work.

import random

# input: an int between 1 and 100
def applyChance(percentage):
   if random.randrange(1,100) < percentage:
      return True
   else:
      return False