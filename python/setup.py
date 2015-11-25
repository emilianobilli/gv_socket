from distutils.core import setup, Extension
setup(name='gv_socket',
      version='0.1',
      description='Python GaVer Socket',
      author='Emiliano A Billi',
      author_email='emiliano.billi@gmail.com',
      url='http://www.gaverprotocol.com',
      py_modules=["gv_socket"],
      ext_modules=[
      Extension("pylibgv", ["pylibgv.c"],include_dirs=['./', '/usr/include/python2.6/'],libraries=['gv']),
                  ])
