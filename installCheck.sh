#!/usr/bin/env sh
echo "Start check minimal dependencies first..."
if ! which python > /dev/null; then
echo "Python check failed o_O	Please install Python 2.0 or later or make sure it is in your path !!!!"
else
echo "Python check passed	:)"
fi

if ! which dlv > /dev/null; then
echo "DLV check failed		o_0	Please install DLV or make sure it is in your path !!!!"
else
echo "DLV check passed	:)"
fi

if ! which dot > /dev/null; then
echo "GraphViz check failed o_0	Please install GraphViz or make sure it is in your path !!!!"
else
echo "GraphViz check passed	:)"
fi

echo "=== End of checking minimal dependecies. You can run Euler if all of the above are passed. ==="
echo ""
echo "Start checking full dependencies..."

if ! which prover9 > /dev/null; then
echo "Prover9 check failed	o_O	Please install Prover9 or make sure it is in your path !!!!"
else
echo "Prover9 check passed	:)"
fi

if ! which mace4 > /dev/null; then
echo "Mace4 check failed	o_O	Please install Mace4 or make sure it is in your path !!!!"
else
echo "Mace4 check passed	:)"
fi

if ! which gringo > /dev/null; then
echo "gringo check failed	o_O	Please install gringo-3.0.3 or make sure it is in your path !!!!"
else
echo "gringo check passed	:)"
fi

if ! which claspD > /dev/null; then
echo "claspD check failed	o_O	Please install claspD-1.1.4  or make sure it is in your path !!!!"
else
echo "claspD check passed	:)"
fi

echo "=== End of checking full dependecies. You can run Euler with all supported reasoners. ==="
#export PATH=src-el:$PATH
#echo "Please  and restart your terminal since PATH has changed"
