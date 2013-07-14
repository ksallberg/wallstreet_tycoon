#from distutils.core import setup
from setuptools import setup

setup(name       = 'wallstreet_tycoon',
      version    = '0.5',
      author     = 'Kristian Sallberg',
      author_email = 'kristian@purestyle.se',
      packages = [],
      scripts = [],
      url = 'https://github.com/ksallberg/wallstreet_tycoon',
      license = '',
      description = 'A stock simulation game.',
      long_description = '',
      install_requires = ['pygame >= 1.9.2',
                          'pyglet >= 1.1.4',
                          'tiledtmxloader >= 3.0.3.114',
                          'Django >= 3.0.3',
                         ],
      
     )