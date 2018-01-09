from setuptools import setup

setup(name='xplan_to_sbol',
      version='0.1',
      description='Converter from XPLAN JSON format to SBOL.',
      url='https://github.com/SD2E/data-representation/sbol/xplan_to_sbol',
      author='Nicholas Roehner',
      author_email='nicholasroehner@gmail.com',
      packages=['xplan_to_sbol'],
      entry_points={
          'console_scripts': [
              'xplan_to_sbol = xplan_to_sbol.__main__:main'
          ]
      },
      install_requires=[
          'sbol',
          'pySBOLx'
      ],
      dependency_links=[
        'git+https://git@github.com/nroehner/pySBOL_Win_64_3.git#egg=sbol',
        'git+https://git@github.com/nroehner/pySBOLx_Win_64_3.git#egg=pySBOLx'
      ],
      zip_safe=False)