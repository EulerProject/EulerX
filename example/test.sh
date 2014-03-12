mkdir output >/dev/null 2>&1
rm -rf output/test/
mkdir output/test/
python ../src/main.py -i email_090904.txt -t "[('shawn1','t1'),('shawn2','t2')]"  -r test -m output/test  -v "ncd" -n "all_nodes" -T 30 -w "possible"  -c "equals,includes,is_included_in,overlaps,disjoint" -h -o done_test.html


