echo "preprocessing..."
python preprocess.py $1;
echo "saving all worlds...";
python awf.py i,o expWorlds.asp;
echo "creating the lattice without color...";
dlv -silent -filter=up  wexp-up.asp expWorlds_aw.asp > up.dlv;
echo "running euler to get MIS...";
euler -i $1.txt -e mnpw --ie > output.txt;
echo "from MIS to MAC and get lattice..."
python lattice.py $1;
dot -Tpdf $1_lat.dot -o $1_lat.pdf;
dot -Tpdf $1_fulllat.dot -o $1_fulllat.pdf
echo "finish";
