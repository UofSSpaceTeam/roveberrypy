from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourcefiles = ['interface.pyx']

extensions = [Extension("interface", sourcefiles)]

setup(
  name = 'interface',
  cmdclass = {'build_ext': build_ext},
  ext_modules = extensions
)