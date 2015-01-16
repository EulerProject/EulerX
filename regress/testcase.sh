#!/usr/bin/env sh

euler -i cases/$1.txt -e $3 --reasoner=$2 -o ./ >& $1.out
if [[ -n "$(diff 3-MIR/$1_mir.csv expected/$1_mir.expected)" ]]; then
  diff 3-MIR/$1_mir.csv expected/$1_mir.expected > $1.dif;
  echo "There is new dif in $1.dif!"
  echo "$1 $2 Failed!"
else
  #rm $1_mir.csv;
  rm $1.out;
  echo "$1 $2 Passed!"
  #rm *txt >& /dev/null
  #rm *yaml >& /dev/null
  #rm *out >& /dev/null
  #rm *stderr >& /dev/null
  #rm *dot >& /dev/null
  #rm *pw >& /dev/null
  #rm *png >& /dev/null
  #rm *pdf >& /dev/null
  rm -rf 0-input
  rm -rf 1-ASP-input-code
  rm -rf 2-ASP-output
  rm -rf 3-MIR
  rm -rf 4-PWs-yaml
  rm -rf 5-PWs-dot
  rm -rf 6-PWs-pdf
  rm -rf 7-PWs-aggregate
  rm -rf logs
  rm -rf $USER-$HOSTNAME
fi
