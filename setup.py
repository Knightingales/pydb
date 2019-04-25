from setuptools import setup

setup(name='pydb',
      version='0.1',
      description='pydb',
      url='',
      author='Knightingale',
      author_email='',
      license='',
      packages=['pydb', 'pydb/engines'],
      install_requires=['redis', 'pymongo'
      ],
      zip_safe=False)
