mkdir output >/dev/null 2>&1
rm -rf output/$1
mkdir output/$1
TEST=$1
if [ $# -eq 1 ]
then
python ../src-ct/main.py -i $1.txt -r $1 -m output/$1  -v "ncd" -n "all_articulations" -T 10 -w "possible"  -h -o done_$1.html 
else
shift
python ../src-ct/main.py -i $TEST.txt -r $TEST -m output/$TEST  -v "ncd" -n "all_articulations" -T 10 -w "possible"  -h -o done_$TEST.html $@
fi
./dot.sh output/$TEST
