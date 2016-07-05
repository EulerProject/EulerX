#!/usr/bin/env sh
echo "\n---- Testing pw1 ----"
./testcase.sh pw1 dlv mnpw
./testcase.sh pw1 gringo mnpw
echo "\n---- Testing pw2 ----"
./testcase.sh pw2 dlv mnpw
./testcase.sh pw2 gringo mnpw
echo "\n---- Testing pw3 ----"
./testcase.sh pw3 dlv mnpw
./testcase.sh pw3 gringo mnpw
echo "\n---- Testing abstract4 ----"
./testcase.sh abstract4 dlv mnpw
./testcase.sh abstract4 gringo mnpw
echo "\n---- Testing ltds ----"
./testcase.sh ltds dlv mnpw
./testcase.sh ltds gringo mnpw
echo "\n---- Testing other dlv ----"
./testcase.sh eqoldj dlv mnpw
./testcase.sh ltoldj dlv mnpw
./testcase.sh gtoldj dlv mnpw
./testcase.sh gtltoldj dlv mnpw
./testcase.sh singleton dlv vrpw
### [NEXT] binary encoding for gringo may not be working well,
### [NEXT] gringo4 may be needed
## ./testcase.sh eqoldj gringo vrpw
## ./testcase.sh ltoldj gringo vrpw
## ./testcase.sh singleton gringo vrpw

