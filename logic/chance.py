import random

# input: an int between 1 and 100
def applyChance(percentage):
   if random.randrange(1,100) < percentage:
      return True
   else:
      return False