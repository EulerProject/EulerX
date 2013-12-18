#!/usr/bin/env sh
echo "Minimal installation requirements check:"
echo ""

if ! which python > /dev/null; then
echo "Python check failed o_O"
echo "Please install Python 2.0 or later or make sure it is in your path !!!!"
fi
echo "Python check passed    #############"

if ! which dlv > /dev/null; then
echo "DLV check failed o_O"
echo "Please install DLV or make sure it is in your path !!!!"
fi
echo "DLV check passed       #############"

if ! which dot > /dev/null; then
echo "GraphViz check failed o_O"
echo "Please install GraphViz or make sure it is in your path !!!!"
fi
echo "GraphViz check passed  #############"

echo "You have installed all minimal requirements of Euler."
#export PATH=src-el:$PATH
#echo "Please  and restart your terminal since PATH has changed"
exit
if ! which gringo > /dev/null; then
echo "gringo check failed o_O"
echo "Please install gringo or make sure it is in your path !!!!"
fi
echo "gringo check passed    #############"

if ! which claspD > /dev/null; then
echo "claspD check failed o_O"
echo "Please install claspD or make sure it is in your path !!!!"
fi
echo "claspD check passed    #############"

if ! which prover9 > /dev/null; then
echo "Prover9 check failed o_O"
echo "Please install Prover9 or make sure it is in your path !!!!"
fi
echo "Prover9 check passed   #############"

if ! which mace4 > /dev/null; then
echo "Mace4 check failed o_O"
echo "Please install Mace4 or make sure it is in your path !!!!"
fi
echo "Mace4 check passed     #############"

