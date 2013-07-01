import random

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