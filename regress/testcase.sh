#!/usr/bin/env sh

euler -i cases/$1.txt -e mnpw --reasoner=$2 >& $1.out
if [[ -n "$(diff $1_mir.csv expected/$1_mir.expected)" ]]; then
  diff $1_mir.csv expected/$1_mir.expected > $1.dif;
  echo "There is new dif in $1.dif!"
  echo "$1 $2 Failed!"
else
  rm $1_mir.csv;
  rm $1.out;
  echo "$1 $2 Passed!"
fi
rm *txt
rm *dot
rm *png
rm -rf asp