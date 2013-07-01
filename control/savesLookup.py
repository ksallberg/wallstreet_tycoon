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
                                             fi.split('.')[1] == 'sqlite'
                                            )
          ]

# !!!!!!!!!!!!_______
# This is run straigh here in the code, because this 
# needs to be done before any django models are imported.
if findExistingRounds() == []:
   currTime = 'saves/'+strftime("%Y-%m-%d-%H-%M-%S", gmtime())+'.sqlite'
   createSettingsFile(currTime)