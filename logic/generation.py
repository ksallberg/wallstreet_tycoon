# Author: Kristian Sallberg - kristian(at)purestyle(punkt)se
# Platform: OSX 10.7.5
# Python version: 2.7.5
# This code is my own work.

# this file has code to handle parsing of the JSON files and
# combine data to create opponent names and company names etc

import random
from random import choice
from gamemodels.models import *

# a company name generator
# based on the company_names.json file
# 
# Does not pick any already existing names.
# When all names are exhaused, this function 
# will freeze! Watch out!
#
# Returns normal strings rather than unicode string
#
# Names do not affect company performance, but it adds
# difficulity to human players, as they might prefer
# some names to others.
def generateCompanyName(json,existingNames):
   
   firstLen  = len(json["firstNames" ]) - 1
   secondLen = len(json["secondNames"]) - 1
   thirdLen  = len(json["thirdNames" ]) - 1
   
   # Pick three words, each from its 
   # designated array in the json file
   first  = json["firstNames" ][random.randint(0,firstLen) ]
   second = json["secondNames"][random.randint(0,secondLen)]
   third  = json["thirdNames" ][random.randint(0,thirdLen) ]
   
   # Create ticker, which the first
   # letter form each word
   ticker = first[0] + second[0] + third[0]
   
   # TODO: Smarter algorithm for making sure
   # company names are unique?
   # Pretty ugly now... Just keeps finding new
   # names until they're all unique.
   while ((str(first) + " " + str(second) + " " + str(third)),str(ticker)) in existingNames:
      first  = json["firstNames" ][random.randint(0,firstLen) ]
      second = json["secondNames"][random.randint(0,secondLen)]
      third  = json["thirdNames" ][random.randint(0,thirdLen) ]
      ticker = first[0] + second[0] + third[0]
   
   return ((str(first) + " " + str(second) + " " + str(third)),str(ticker))

def generateInvestorName(json,existingNames):
   
   firstLen  = len(json["firstNames"] ) - 1
   secondLen = len(json["familyNames"]) - 1
   
   first     = json["firstNames" ][random.randint(0,firstLen) ]
   family    = json["familyNames"][random.randint(0,secondLen)]
   
   while ((str(first) + " " + str(family)) in existingNames):
      first  = json["firstNames" ][random.randint(0,firstLen) ]
      family = json["familyNames"][random.randint(0,secondLen)]
      
   return (str(first) + " " + str(family))
   
# Populate a new savefile with some randomized
# content so that a new round can begin
def generateNewRound(companyNames,investorNames,playerInput):
   
   # Create random companies
   for i in range(0,len(companyNames)): # TODO: Check if its correct ot not have len - 1
      
      st       = Stock()
      st.time  = 0
      st.price = random.randint(3,300) # the initial stock price
      st.save()
      
      newComp           = Company()
      newComp.name      = companyNames[i][0]
      newComp.ticker    = companyNames[i][1]
      newComp.cash      = random.randint(500000,100000000) #500,000 to 100 million
      newComp.shares    = 100000
      newComp.save()
      
      newComp.priceHistory.add(st)
      
   # Create random investors
   for i in range(0,len(investorNames)):
      
      inv        = Investor()
      inv.name   = investorNames[i].split(' ')[0][2:] + ' ' + investorNames[i].split(' ')[1] #remove m_ or f_ for sprite sex
      
      #if investor's name is male, then pick a male sprite
      if investorNames[i].split(' ')[0][:2] == 'm_':
         inv.sprite = choice(['char1','char3','char4','char5'])
      #else pick a female sprite
      elif investorNames[i].split(' ')[0][:2] == 'f_':
         inv.sprite = choice(['char2','char6','char7','char8'])
      else:
         print 'Error generation.py: generateNewRound: Non existing sex defined in json file.' 
      
      inv.cash   = 50000
      inv.type   = 'bot'
      inv.save()
      
   # Create the player
   player        = Investor()
   player.name   = playerInput[0]
   player.sprite = playerInput[1]
   player.cash   = 50000
   player.type   = 'player'
   player.save()