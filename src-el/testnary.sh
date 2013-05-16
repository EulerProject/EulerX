euler -g -$1 $2 -d $3 -t "<"
time for (( i=0; i<$4; i++ )); do euler -i foo_n$1_$2.txt -e mnpw; done;
