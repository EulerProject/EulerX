# Thank you for using Euler toolkit.

# Introduction

Euler is an open source toolkit (mostly written in Python) for merging taxonomies (taxonomical organized datasets) and visualizing the results. (see https://sites.google.com/site/eulerdi/ for more info).

We have all the CleanTax++ source code, EulerASP source code, and a bunch of use cases in this toolkit. CleanTax++ (EulerFO) is a modified version of CleanTax which was firstly developed by Dave Thau. CleanTax/CleanTax++ are built upon Prover9/Mace4 reasoning software. EulerASP is a brand new taxonomy reasoning tool that Mingmin built from scratch. EulerASP is built based on popular ASP reasoners DLV and clingo/gringo.

# Structure of this toolkit
src-ct/             # directory of CleanTax++ source code
src-ct/main.py      # main entry of CleanTax++ source code

src-el/             # directory of EulerASP source code
src-el/euler        # main entry of EulerASP source code

example/            # directory of all the use cases
example/runct.sh    # shell script to run CleanTax++, see the example section for more information
example/abstract    # abstract example
example/abstract4   # abstract4 example
example/pw1         # pw1 example
example/..          # other examples


# Software Dependencies
The whole toolkit is written in Python, so you need have Python 2.X or later installed in your computer. You also need the following dependent software to run this toolkit.

CleanTax++ dependencies:

1. Prover9/Mace4:  http://www.cs.unm.edu/~mccune/mace4/
2. GraphViz:       http://www.graphviz.org/

EulerASP dependencies:

1. DLV:            http://www.dlvsystem.com/
2. Potassco:       http://potassco.sourceforge.net/
  - gringo-3.0.3
  - claspD-1.1.4
3. GraphViz:       http://www.graphviz.org/

####################### IMPORTANT #########################
Please run checkdep.sh and make sure the dependency check passes before running this toolkit.
###########################################################

# Examples of Running CleanTax++

Here are examples under example/ directory,

1. cd to example/ directory
2. run test.sh by "./test.sh", you will find the output files in output/test/
3. "./runct.sh abstract", you will find the output files in output/abstract/
4. "./runct.sh abstract2", you will find the output files in output/abstract2/
5. "./runct.sh abstract3", you will find the output files in output/abstract3/
6. "./runct.sh abstract3b", you will find the output files in output/abstract3b/, it is the "Bertram" mode for abstract3.
7. "./runct.sh abstract2c", you will find the output files in output/abstract2c/, it is the test case with articulation confidence for abstract2.

# Examples of Running EulerASP

Still under example/ directory (assuming src-el/ is in your PATH env, and gringo, claspD, dlv in your PATH env),

0. "euler --help" wil give you the options that you have
1. "euler -i example/abstract4.txt -e vr", you will get all the mir relations in the generated output file using binary encoding.
2. "euler -i example/abstract4.txt -e vrpw", you will get all the possible worlds in the console using binary encoding.
3. "euler -i example/abstract4.txt -e vrve", you will get all the valid euler regions in the console using binary encoding.
4. "euler -i example/abstract4.txt -e mn", you will get all the mir relations in the generated output file using polynomial encoding.
5. "euler -i example/abstract4.txt -e mnpw", you will get all the possible worlds in the console using polynomial encoding.
6. "euler -i example/abstract4.txt -e mnve", you will get all the valid euler regions in the console using polynomial encoding.

# Contact

If you have any question or comments, please contact Mingmin Chen at michen@ucdavis.edu.
