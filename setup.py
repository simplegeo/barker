from setuptools import setup, find_packages

setup(name='clive',
      version="0.1.3",
      description='Clive is a hive mind for your clusters.',
      author='Paul Lathrop',
      author_email='paul@simplegeo.com',
      url='https://github.com/plathrop/clive',
      packages=find_packages(),
      install_requires=['kombu', 'eventlet'],
      tests_require=['coverage',
                     'nose',
                     'mock>=0.6.0'],
      test_suite="nose.collector",
      entry_points={'console_scripts':
                        ['clive = clive.cli:main']}
      )
