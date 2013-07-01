import json

# Class to load the JSON file
class Loader():
   def loadJSON(self,fileName):
      json_data = None
      try:
         json_data = open(fileName)
      except IOError:
         print 'Could not load JSON file!'
         return None
      data = json.load(json_data)
      json_data.close()
      return data