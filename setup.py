# Author: Kristian Sallberg - kristian(at)purestyle(punkt)se
# Platform: OSX 10.7.5
# Python version: 2.7.5
# This code is my own work.

import os
from setuptools import setup

setup(name             = 'wallstreet_tycoon',
      version          = '0.5',
      author           = 'Kristian Sallberg',
      author_email     = 'kristian@purestyle.se',
      url              = 'https://github.com/ksallberg/wallstreet_tycoon',
      description      = 'A stock simulation game.',
      install_requires = ['Django >= 1.5.1',
                          'pyglet >= 1.1.4',
                          'tiledtmxloader >= 3.0.3',
                          'pygame>=1.9.1',
                         ],
      
     )