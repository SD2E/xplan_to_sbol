from setuptools import setup

setup(name='xplan_to_sbol',
      version='0.1',
      description='Converter from XPLAN JSON format to SBOL.',
      url='https://github.com/SD2E/xplan_to_sbol',
      author='Nicholas Roehner',
      author_email='nicholasroehner@gmail.com',
      packages=['xplan_to_sbol'],
      entry_points={
          'console_scripts': [
              'xplan_to_sbol = xplan_to_sbol.__main__:main'
          ]
      },
      install_requires=[
        'synbiohub_adapter==0.0.1', 'sparqlwrapper'
      ],
      dependency_links=[
        'git+https://git@github.com/SD2E/synbiohub_adapter.git#egg=synbiohub_adapter-0.0.1'
      ],
      zip_safe=False)