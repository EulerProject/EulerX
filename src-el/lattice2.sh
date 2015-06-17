# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

curdir=$(pwd)
euler=$(which euler)
srcdir=$(dirname $euler)
prodir=$(dirname $srcdir)
cd $prodir
cd bbox-lattice
input=$curdir/$1

echo "preprocessing..."
echo "creating the lattice without color...";
python preprocess.py $input;
echo "saving all worlds...";
python awf.py -filter=i,o expWorlds.asp;
#dlv -silent -filter=up  wexp-up.asp expWorlds_aw.asp > up.dlv;
echo "running euler to get MIS...";
euler2 align $input -e mnpw --repair=HST > output.txt;
echo "from MIS to MAC and get lattice..."
python lattice.py $input $curdir;
echo "finish";
