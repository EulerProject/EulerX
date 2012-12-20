# Thank you for using Euler toolkit.

# Introduction

Euler is an open source toolkit (mostly written in Python) for merging taxonomies and visualizing the results. (see https://sites.google.com/site/eulerdi/ for more info).

We have all the CleanTax++ source code, EulerDLV source code, and a bunch of use cases in this toolkit. CleanTax++ is a modified version of CleanTax which was firstly developed by Dave Thau. CleanTax/CleanTax++ are built upon Prover9/Mace4 reasoning software. EulerDLV is a brand new taxonomy reasoning tool that Mingmin built from scratch. EulerDLV is built based on DLV.

# Structure of this toolkit
src-ct/             # directory of CleanTax++ source code
src-ct/main.py      # main entry of CleanTax++ source code

src-el/             # directory of EulerDLV source code
src-el/euler        # main entry of EulerDLV source code

example/            # directory of all the use cases
example/runct.sh    # shell script to run CleanTax++, see the example section for more information
example/abstract    # abstract example
example/abstract4   # abstract4 example
example/pw1         # pw1 example
example/..          # other examples


# Software Dependencies
Assuming you have Python 2.X or later installed in your computer, you also need the following dependent software to run this toolkit.

CleanTax++ dependencies:
* Prover9/Mace4:  http://www.cs.unm.edu/~mccune/mace4/
* GraphViz:       http://www.graphviz.org/

EulerDLV dependencies:
* DLV:            http://www.dlvsystem.com/

# Examples of Running CleanTax++

Here are examples under example/ directory, 

1. cd to example/ directory
2. run test.sh by "./test.sh", you will find the output files in output/test/
3. "./runct.sh abstract", you will find the output files in output/abstract/
4. "./runct.sh abstract2", you will find the output files in output/abstract2/
5. "./runct.sh abstract3", you will find the output files in output/abstract3/
6. "./runct.sh abstract3b", you will find the output files in output/abstract3b/, it is the "Bertram" mode for abstract3.
7. "./runct.sh abstract2c", you will find the output files in output/abstract2c/, it is the test case with articulation confidence for abstract2.

# Examples of Running EulerDLV

Still under example/ directory (assuming src-el/ is in your PATH env),

0. "euler --help" wil give you the options that you have
1. "euler -i example/abstract4.txt -e vr", you will get all the mir relations in the generated output file using binary encoding.
2. "euler -i example/abstract4.txt -e vrpw", you will get all the possible worlds in the console using binary encoding.
3. "euler -i example/abstract4.txt -e vrve", you will get all the valid euler regions in the console using binary encoding.
4. "euler -i example/abstract4.txt -e pl", you will get all the mir relations in the generated output file using polynomial encoding.
5. "euler -i example/abstract4.txt -e plpw", you will get all the possible worlds in the console using polynomial encoding.
6. "euler -i example/abstract4.txt -e plve", you will get all the valid euler regions in the console using polynomial encoding.

# Contact

If you have any question or comments, please contact Mingmin Chen at michen@ucdavis.edu.
