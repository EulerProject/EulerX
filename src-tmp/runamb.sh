python checkamb.py $1;
list=$(ls *_rep*)
for i in $list
do
	euler -i $i
done
