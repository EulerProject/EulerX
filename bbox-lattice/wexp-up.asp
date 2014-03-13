% worlds
w(I) :- i(I,_).
w(I) :- o(I,_).

% In the powerset lattice, there is an edge Wi -> Wj if Wj = Wi + {x} 
% We say that Wj is in up(Wi), otherwise nu(Wi,Wj) holds
up(I,J) :-
	w(I), w(J), I != J, not nu(I,J).

nu(I,J) :- 
	w(I), w(J), 
	i(I,X), o(J,X). % if I has X, but J doesn't, then I->J is out (I isn't a subset of J)
nu(I,J) :- 
	w(I), w(J), 
	i(J,X1), i(J,X2), X1 != X2, % J has two X1, X2, but ... 
	o(I,X1), o(I,X2).           % I doesn't have them, then I->J is out (delta is at leat 2 elements)

% Each world is green or red: 
%g(I) :- w(I), not r(I).
%r(I) :- w(I), not g(I).

% green (consistent) propagates downward:
%g(I) :- g(J), up(I,J).

% red (inconsistent) propagates upward:
%r(J) :- r(I), up(I,J).
