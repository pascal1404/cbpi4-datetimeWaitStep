from setuptools import setup

setup(name='cbpi4-datetimeWaitStep',
      version='0.0.1',
      description='CraftBeerPi Plugin to wait unil a defined datetime is reached',
      author='Pascal Scholz',
      author_email='pascal1404@gmx.de',
      url='https://github.com/pascal1404/cbpi4-datetimeWaitStep',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-datetimeWaitStep': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-datetimeWaitStep'],
     )