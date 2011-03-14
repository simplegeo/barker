from setuptools import setup, find_packages

setup(name='clive',
      version='0.0.1',
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
                    ['clive-pod = clive.pod:clive_pod_cmd',
                     'clive-publish-pod = clive.publish:clive_publish_pod_cmd',
                     'clive-demo-listener = clive.publish:clive_demo_listener_cmd']}
      )
