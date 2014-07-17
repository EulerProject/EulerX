#!/usr/bin/env sh

./testcase.sh pw1 dlv mnpw
./testcase.sh pw1 gringo mnpw
./testcase.sh pw2 dlv mnpw
./testcase.sh pw2 gringo mnpw
./testcase.sh pw3 dlv mnpw
./testcase.sh pw3 gringo mnpw
./testcase.sh abstract4 dlv mnpw
./testcase.sh abstract4 gringo mnpw
./testcase.sh ltds dlv mnpw
./testcase.sh ltds gringo mnpw
./testcase.sh eqoldj dlv mnpw
./testcase.sh ltoldj dlv mnpw
./testcase.sh gtoldj dlv mnpw
./testcase.sh gtltdj dlv mnpw
./testcase.sh singleton dlv vrpw
### TODO binary encoding for gringo may not be working well,
###      gringo4 may be needed
## ./testcase.sh eqoldj gringo vrpw
## ./testcase.sh ltoldj gringo vrpw
## ./testcase.sh singleton gringo vrpw

