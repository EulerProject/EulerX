mkdir output >/dev/null 2>&1
rm -rf output/$1
mkdir output/$1
python ../src/main.py -i $1.txt -r $1 -m output/$1  -v "ncd" -n "all_articulations" -T 10 -w "possible"  -h -o done_$1.html

