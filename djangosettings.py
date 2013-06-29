SECRET_KEY = '!'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     'saves/db.sqlite'
    }
}

INSTALLED_APPS = (
   'gamemodels'
)