euler -g -n $1 -d $2
time for (( i=0; i<10; i++ )); do euler -i foo_$1_$2.txt -e mnpw; done
