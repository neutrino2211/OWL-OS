#@owldoc

'''@
This script is used the build the c++ api
@'''
from distutils.core import setup, Extension

ext = Extension("owlapi",sources=['owlapi.cc'])

setup(name = "owlapi",version = "0.1",ext_modules=[ext])