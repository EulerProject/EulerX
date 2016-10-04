#!/usr/bin/env sh
timestampfile=$USER-$HOSTNAME-lastrun.timestamp
euler2 align cases/$1.txt -e $3 -r $2 >& $1.out
folder=$(head -n 1 $timestampfile)
if [[ -n "$(diff $folder/3-MIR/$1_mir.csv expected/$1_mir.expected)" ]]; then
  diff $folder/3-MIR/$1_mir.csv expected/$1_mir.expected > $1.dif;
  echo "There is new dif in $1.dif!"
  echo "$1 $2 Failed!"
else
  rm $1.out;
  echo "$1 $2 Passed!"
  rm -rf $USER-$HOSTNAME
  rm $timestampfile
  rm report.csv
fi
