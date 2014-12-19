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
euler -i $input -e mnpw --artRem > output.txt;
echo "from MIS to MAC and get lattice..."
python lattice.py $input $curdir;
echo "finish";
