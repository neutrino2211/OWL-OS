from distutils.core import setup, Extension

ext = Extension("owlapi",sources=['hello.cc'])

setup(name = "owlapi",version = "0.1",ext_modules=[ext])