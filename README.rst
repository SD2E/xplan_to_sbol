xplan_to_sbol
########################################

xplan_to_sbol is a Python app for converting JSON-formatted XPLANs to the Synthetic Biology Open Language (SBOL).

.. contents::

.. section-numbering::


Installation
============

Windows
-------------

xplan_to_sbol requires that Git and Python 3 be installed first, and it currently depends on a version of pySBOL that is only compatible with 64-bit Windows. To install xplan_to_sbol, checkout this repository from GitHub and run the following in the Command Prompt from the xplan_to_sbol directory:

.. code-block:: powershell

    python setup.py install

This command will automatically download and install the pySBOL and pySBOLx packages that xplan_to_sbol depends on from GitHub.


Usage
=====

xplan_to_sbol can be run from the Command Prompt as follows:

.. code-block:: powershell

    xplan_to_sbol -xp [path to XPLAN JSON file] -sp [path for output SBOL RDF/XML file] -hm [authority to prefix generated URIs]

xplan_to_sbol can also be imported and used as a Python module like so:

.. code-block:: python

    import xplan_to_sbol.__main__ as xbol

    args = ['-xp', 'path to input XPLAN JSON file', '-sp', 'path for output SBOL RDF/XML file', '-hm', 'authority to prefix generated URIs']

    xbol.main(args)

Example
--------

Run the following from the xplan_to_sbol directory:

.. code-block:: powershell

    xplan_to_sbol -xp example/xplan/yeastGates-Q0.json -sp example/sbol/yeastGates-Q0.xml -hm http://sift.net

An example of importing xplan_to_sbol can be found in the Jupyter notebook xplan_to_sbol.ipynb.