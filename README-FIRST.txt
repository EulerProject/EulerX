DIRECTORIES:
- .hg		% internal Mercurial folder (e.g. use 'branch' file to switch branches
- dlv		% old auto-generated DLV folder (no longer used)
- example	% subfolders with Euler examples
- regress	% for Regression testing   
- src-ct	% CleanTax Source
- src-el	% Euler-ASP Source Code
- src2		% old source from Shizhuo (move / merge / reorganize !?)

FILES: 
- README.md	% File used on bitbucket homepage
- install.sh	% installation check: Euler-Full
- mini-install.sh % installation check: Euler-Minimal


TODO:
- fix and rename install / mini-install:
-- check-euler-minimal.sh
--- check the minimal installation requirements for Euler:
i.e., all functions but not necessarily all reasoners, here: 
    Python2.7.X 
    AND graphviz XYZ 
    AND (DLV-2011 
    	 OR (gringo-3.0.3 AND claspD1.1.4)) 
-- check-euler-full.sh  
   check-euler-minimal
AND Prover9/Mace4 
AND PYRCC 
AND both DLV-2011 AND Gringo/claspD

----------------------------------------------------------------------
GETTING STARTED
