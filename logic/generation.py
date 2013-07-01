import random
from gamemodels.models import Stock, Company

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
   while (str(first + " " + second + " " + third),str(ticker)) in existingNames:
      first  = json["firstNames" ][random.randint(0,firstLen) ]
      second = json["secondNames"][random.randint(0,secondLen)]
      third  = json["thirdNames" ][random.randint(0,thirdLen) ]
      ticker = first[0] + second[0] + third[0]
   
   return (str(first + " " + second + " " + third),str(ticker))
   
# Populate a new savefile with some randomized
# content so that a new round can begin
def generateNewRound(names):
   
   # Create 100 random companies
   for i in range(0,len(names)-1):
      
      st       = Stock()
      st.time  = 0
      st.price = random.randint(3,300) # the initial stock price
      st.save()
      
      newComp           = Company()
      newComp.name      = names[i][0]
      newComp.ticker    = names[i][1]
      newComp.cash      = random.randint(500000,100000000) #500,000 to 100 million
      newComp.shares    = 100000
      newComp.save()
      
      newComp.priceHistory.add(st)