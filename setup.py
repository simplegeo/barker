from setuptools import setup, find_packages

setup(name='barker',
      version="0.1.70",
      description='Barker is a hive mind for your clusters.',
      author='Paul Lathrop',
      author_email='paul@simplegeo.com',
      url='https://github.com/plathrop/barker',
      packages=find_packages(),
      install_requires=['kombu', 'eventlet'],
      tests_require=['coverage',
                     'nose',
                     'mock>=0.6.0'],
      test_suite="nose.collector",
      entry_points={'console_scripts':
                        ['barker = barker.cli:main']}
      )
