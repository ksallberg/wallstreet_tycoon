# Author: Kristian Sallberg - kristian(at)purestyle(punkt)se
# Platform: OSX 10.7.5
# Python version: 2.7.5
# This code is my own work.

from os import listdir
from os.path import isfile, join
from time import gmtime, strftime

# It does not seem possible to change the name variable of Django's ORM
# settings file run time, so it has to be changed before Django looks at it
def createSettingsFile(dbName):
   print 'Creating settings file'
   
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

# Look in the saves folder, and return
# all wallstreet game save files.
def findExistingRounds():
   return [fi for fi in listdir('saves') if (
                                             isfile(join('saves',fi)) and
                                             fi.split('.')[1] == 'save'
                                            )
          ]

def createNewFile():
   currTime = join('saves',strftime("%Y-%m-%d-%H-%M-%S", gmtime())+'.save')
   createSettingsFile(currTime)