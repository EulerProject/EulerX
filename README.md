Thank you for using Euler toolkit.
====================

![Alt text](http://euler.cs.ucdavis.edu/_/rsrc/1366832610901/home/logo_small.png)

On this page:

* [Introduction](https://bitbucket.org/eulerx/euler-project/overview#markdown-header-introduction)
* [Structure of This Toolkit](https://bitbucket.org/eulerx/euler-project/overview#markdown-header-structure-of-this-toolkit)
* [Installation Steps](https://bitbucket.org/eulerx/euler-project/overview#markdown-header-installation-steps)
* [Software Dependencies](https://bitbucket.org/eulerx/euler-project/overview#markdown-header-software-dependencies)
* [Examples of Running EulerFO](https://bitbucket.org/eulerx/euler-project/overview#markdown-header-examples-of-running-eulerfo)
* [Examples of Running EulerASP](https://bitbucket.org/eulerx/euler-project/overview#markdown-header-examples-of-running-eulerasp)
* [Contact](https://bitbucket.org/eulerx/euler-project/overview#markdown-header-Contact)

# Introduction

Euler is an open source toolkit (mostly written in Python) for merging taxonomies (taxonomical organized datasets) and visualizing the results. (See our [website][euler] for more info).

We have all the EulerFO source code, EulerASP source code, and a bunch of use cases in this toolkit. EulerFO is a modified version of CleanTax which was firstly developed by Dave Thau. CleanTax/EulerFO are built upon Prover9/Mace4 reasoning software. EulerASP is a brand new taxonomy reasoning tool that Mingmin built from scratch. EulerASP is built based on popular ASP reasoners DLV and Potassco.

# Structure of This Toolkit

  DIRECTORIES       |  Description                                                          
 :----------------- | :---------------------------------------------------------------------
 `.hg/`             |  internal Mercurial folder (e.g. use `branch` file to switch branches)
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

1. If you are a first-time user for hg/mercury, please download and install it [here][mercury].
2. Click the button called **Clone** on top right of the page, copy the line `hg clone https://bitbucket.org/eulerx/euler-project` in tab HTTPS. (if you have logged-in to bitbucket, you will see something like `hg clone https://YOUR_USER_NAME@bitbucket.org/eulerx/euler-project`)
3. Open your shell, go to a folder which you want to install Euler, paste this line and click **Enter**. It will download the Euler repository (in folder `euler-project/`) under this folder.
4. The default branch is the released version. If you want to use the latest version with more functions support, please update to **main** branch. By doing this, open the file called `branch` under folder `euler-project/.hg/`, you will see the contents as **"default"**, change it to be **"main"**, save and close this file.
5. Type `hg update` in shell, it will update to the latest version of Euler in main branch.
6. **[IMPORTANT]** You need to make sure your machine has met the minimal software requirements before run Euler. (Please see section **Software Dependencies** in detail)
7. You can add main entry of source code (e.g. `src-el/` of EulerASP) into your PATH env. 

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
[mercury]: http://mercurial.selenic.com/
[p9m4]: http://www.cs.unm.edu/~mccune/mace4/
[graphviz]: http://www.graphviz.org/
[dlv]: http://www.dlvsystem.com/
[potassco]: http://potassco.sourceforge.net/
