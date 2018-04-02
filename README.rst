xplan_to_sbol
########################################

xplan_to_sbol is a Python app for converting JSON-formatted XPLANs to the Synthetic Biology Open Language (SBOL).

.. contents::

.. section-numbering::


Installation
============

Windows
-------------

xplan_to_sbol requires that Git and Python 3 be installed first. To install xplan_to_sbol, checkout this repository from GitHub and run the following in the Command Prompt from the xplan_to_sbol directory:

.. code-block:: powershell

    python setup.py install

This command will automatically download and install the pySBOLx package that it depends on from GitHub.


Usage
=====

xplan_to_sbol can be run from the Command Prompt as follows:

.. code-block:: powershell

    xplan_to_sbol -i [path to input XPLAN (JSON file)] -o1 [path for output SBOL plan (RDF/XML file)] -o2 [path for output SBOL experiment (RDF/XML file)] 

xplan_to_sbol can also be imported and used as a Python module like so:

.. code-block:: python

    import xplan_to_sbol.__main__ as xbol

    args = ['-i', 'path to input XPLAN (JSON file)', '-o1', 'path for output SBOL plan (RDF/XML file)', '-o2', 'path for output SBOL experiment (RDF/XML file)']

    xbol.main(args)

Example
--------

Run the following from the xplan_to_sbol directory:

.. code-block:: powershell

    xplan_to_sbol -xp example/xplan/draft_protstab_plan-v2.json -o1 example/sbol/draft_protstab_plan-v2.xml -o2 draft_protstab_experiment-v2.xml

An example of importing xplan_to_sbol can be found in the Jupyter notebook xplan_to_sbol.ipynb.