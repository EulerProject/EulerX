Thank you for using Euler toolkit.
====================

![Alt text](http://euler.cs.ucdavis.edu/_/rsrc/1366832610901/home/logo_small.png)

On this page:

* [Introduction](https://github.com/EulerProject/EulerX#introduction)
* [Structure of This Toolkit](https://github.com/EulerProject/EulerX#structure-of-this-toolkit)
* [Installation Steps](https://github.com/EulerProject/EulerX#installation-steps)
* [Software Dependencies](https://github.com/EulerProject/EulerX#software-dependencies)
* [Examples of Running EulerFO](https://github.com/EulerProject/EulerX#examples-of-running-eulerfo)
* [Examples of Running EulerASP](https://github.com/EulerProject/EulerX#examples-of-running-eulerasp)
* [Contact](https://github.com/EulerProject/EulerX#Contact)

# Introduction

Euler is an open source toolkit (mostly written in Python) for merging taxonomies (taxonomical organized datasets) and visualizing the results. (See our [website][euler] for more info).

We have all the EulerFO source code, EulerASP source code, and a bunch of use cases in this toolkit. EulerFO is a modified version of CleanTax which was firstly developed by Dave Thau. CleanTax/EulerFO are built upon Prover9/Mace4 reasoning software. EulerASP is a brand new taxonomy reasoning tool that Mingmin built from scratch. EulerASP is built based on popular ASP reasoners DLV and Potassco.

Euler is designed for UNIX-like operating systems (Linux, Mac, etc). If you are running on Windows, you need to install a virtual machine to run Euler.

# Structure of This Toolkit

  DIRECTORIES       |  Description                                                          
 :----------------- | :---------------------------------------------------------------------
 `.git/`            |  internal git folder 
 `example/`         |  subfolders with all Euler use cases
 `regress/`         |  for Regression testing
 `src-ct/ `         |  EulerFO source code
 `src-el/`          |  EulerASP source code

  FILES             |  Description                                    
 :----------------- | :---------------------------------------------------------------------
 `README.md`        |  file used on Bitbucket homepage
 `installCheck.sh`  |  installation requirements check
 `src-ct/main.py`   |  main entry of CleanTax++ source code
 `src-el/euler`     |  main entry of EulerASP source code
 `example/runct.sh` |  shell script to run EulerFO

# Installation Steps

1. If you are a first-time user for git, please download and install it [here][gitdownloads].
2. Open your shell, go to a folder which you want to install Euler, clone the repository under "main branch" to your local disk by copy and run `git clone -b "main" https://github.com/EulerProject/EulerX.git` in terminal.
3. **[IMPORTANT]** You need to make sure your machine has met the minimal software requirements before run Euler. (Please see section **Software Dependencies** in detail)
4. You can add main entry of source code (e.g. `src-el/` of EulerASP) into your PATH env. 
5. When there is a new commit of the source, you can update it by running `git pull`.

# Software Dependencies

Please run `installCheck.sh` and make sure the dependency check passes before running this toolkit.

The whole toolkit is written in **Python**, so you need have Python 2.X or later installed in your computer. You also need the following dependent software to run this toolkit.

EulerFO dependencies:

1. [Prover9/Mace4][p9m4]
2. [GraphViz][graphviz]

EulerASP dependencies:

1. [DLV][dlv] (version: static, no ODBC support)
2. [Potassco][potassco]
	- gringo-3.0.3
	- claspD-1.1.4
3. [GraphViz][graphviz]

# Examples of Running EulerFO

Here are examples under `example/` directory,

1. cd to `example/` directory
2. run `./test.sh`, you will find the output files in `output/test/`
3. `./runct.sh abstract`, you will find the output files in `output/abstract/`
4. `./runct.sh abstract2`, you will find the output files in `output/abstract2/`
5. `./runct.sh abstract3`, you will find the output files in `output/abstract3/`
6. `./runct.sh abstract3b`, you will find the output files in `output/abstract3b/`, it is the "Bertram" mode for abstract3.
7. `./runct.sh abstract2c`, you will find the output files in `output/abstract2c/`, it is the test case with articulation confidence for abstract2.

# Examples of Running EulerASP

Still under `example/` directory (assuming `src-el/` is in your PATH env, and gringo, claspD, dlv in your PATH env),

0. `euler --help` wil give you the options that you have
1. `euler -i example/abstract4.txt -e vr`, you will get all the mir relations in the generated output file using binary encoding.
2. `euler -i example/abstract4.txt -e vrpw`, you will get all the possible worlds in the console using binary encoding.
3. `euler -i example/abstract4.txt -e vrve`, you will get all the valid euler regions in the console using binary encoding.
4. `euler -i example/abstract4.txt -e mn`, you will get all the mir relations in the generated output file using polynomial encoding.
5. `euler -i example/abstract4.txt -e mnpw`, you will get all the possible worlds in the console using polynomial encoding.
6. `euler -i example/abstract4.txt -e mnve`, you will get all the valid euler regions in the console using polynomial encoding.

# Contact

If you have any question or comments, please contact Mingmin Chen at michen@ucdavis.edu.

[euler]: http://euler.cs.ucdavis.edu/
[gitdownloads]:http://git-scm.com/downloads/ 
[p9m4]: http://www.cs.unm.edu/~mccune/mace4/
[graphviz]: http://www.graphviz.org/
[dlv]: http://www.dlvsystem.com/
[potassco]: http://potassco.sourceforge.net/
