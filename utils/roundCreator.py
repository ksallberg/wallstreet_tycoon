from os import listdir
from os.path import isfile, join

# Look in the saves folder, and return
# all wallstreet game save files.
def findExistingRounds():
   return [fi for fi in listdir('saves') if (
                                             isfile(join('saves',fi)) and
                                             fi.split('.')[1] == 'sqlite'
                                            )
          ]

# Populate a new savefile with some randomized
# content so that a new round can begin
def createNewRound():
   
   from gamemodels.models import *
   
   # Create 100 random companies
   for i in range(0,10):
      st       = Stock()
      st.time  = 0
      st.price = 0
      st.save()
      
      newComp = Company()
      newComp.name = 'testcompany'
#      newComp.priceHistory = []
      newComp.lastPrice = st
      newComp.cash = 1000
      newComp.save()
      
      newComp.priceHistory.add(st)

# It does not seem possible to change the name variable of Django's ORM
# settings file run time, so it has to be changed before Django looks at it
def createSettingsFile(dbName):
   print 'CREATE SETTINGS FILE!!!'
   
   f = open('djangosettings.py', 'w')
   f.write("SECRET_KEY = '!'\n")
   f.write("DATABASES = {\n")
   f.write("    'default': {\n")
   f.write("        'ENGINE':   'django.db.backends.sqlite3',\n")
   f.write("        'NAME':     '"+dbName+"'\n")
   f.write("    }\n")
   f.write("}\n")
   f.write("INSTALLED_APPS = (\n")
   f.write("   'gamemodels'\n")
   f.write(")\n")