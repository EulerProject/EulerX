echo "saving all worlds...";
python awf.py i,o expWorlds.asp;
echo "creating the lattice without color...";
#dlv -silent -filter=up  wexp-up.asp expWorlds_aw.asp;
echo "running euler to get MIS";
euler -i $1.txt -e mnpw --ie > output.txt;
echo "from MIS to MAC and get lattice"
python lattice.py $1;
