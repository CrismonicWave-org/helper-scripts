# Pylint_to_sarif converter

This script takes the output from Pylint and converts it to a 2.1.0 SARIF format.  It is a simple conversion and it can then be imported into the GitHub CodeQL user experience.  The out put can also be used in any other SARIF viewing tool you may want to use.

Here is the link to the code [pylint_to_sarif.py](./pylint_to_sarif.py)

To see how to leverage this script and subsequently import the converted SARIF file into CodeQL, please see the following GitHub Workflow [HERE](../../.github/workflows/pylint-codeql.yml)

In this workflow you will see pykint being executed, then the conversion of the pylint output to SARIF output then uploaded to the CodeQL.

Any enhancements, please email me at ```kencrismon@crismonicwave.com``` or clone it, create a branch and propose a change, enhancement etcetera.

