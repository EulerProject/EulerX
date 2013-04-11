euler -g -$1 $2 -d $3 $4
time for (( i=0; i<$4; i++ )); do euler -i foo_$1$2_$3.txt -e mnpw -N; done;
