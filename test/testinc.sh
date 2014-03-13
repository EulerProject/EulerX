euler -g -$2 $3 -d $4 -I
time for (( i=0; i<$5; i++ )); do euler -i foo_$2$3_$4.txt -N --$6 --reasoner=$1; done;
