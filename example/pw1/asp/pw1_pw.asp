%%% Euler regions
r(1..8).

%%% Concepts
tax(t1,0).
concept2(A, B) :- concept(A,B,_).
concept2(c1_a,0).
concept(c1_b,0,0).
concept(c1_e,0,1).
tax(t2,1).
concept2(A, B) :- concept(A,B,_).
concept2(c2_c,1).
concept(c2_d,1,0).
concept(c2_f,1,1).
%%% Euler Bit
bit(M, 0, V):-r(M),M1=M/1, V = M1 #mod 3.
bit(M, 1, V):-r(M),M1=M/3, V = M1 #mod 3.


%%% Meaning of regions
in(X, M) :- r(M),concept(X,T,N),N1=N+1,bit(M,T,N1).
out(X, M) :- r(M),concept(X,T,N),N1=N+1,not bit(M,T,N1).
in(X, M) :- r(M),concept2(X,_),not out(X, M).
out(X, M) :- out3(X, M, _), ix.
irs(M) :- in(X, M), out(X, M), r(M), concept2(X,_).

%%% Constraints of regions.
irs(X) :- ir(X, _).
vrs(X) :- vr(X, _).
vr(X, X) :- not irs(X), r(X).
ir(X, X) :- not vrs(X), r(X).
ie(prod(A,B)) :- vr(X, A), ir(X, B), ix.
:- vrs(X), irs(X), pw.

%%% Inconsistency Explanation.
ie(s(R, A, Y)) :- pie(R, A, Y), not cc(R, Y), ix.
cc(R, Y) :- c(R, _, Y), ix.

%%% Parent-Child relations
%% ISA
% c1_b isa c1_a
ir(X, r0) :- in(c1_b, X), out(c1_a, X), pw.
ir(X, prod(r0,R)) :- in(c1_b,X), out3(c1_a, X, R), ix.
:- [vrs(X): in(c1_b, X): in(c1_a, X)]0.
pie(r0, A, 1) :- ir(X, A), in(c1_b, X), in(c1_a, X), ix.
c(r0, A, 1) :- vr(X, A), in(c1_b, X), in(c1_a, X), ix.

% c1_e isa c1_a
ir(X, r1) :- in(c1_e, X), out(c1_a, X), pw.
ir(X, prod(r1,R)) :- in(c1_e,X), out3(c1_a, X, R), ix.
:- [vrs(X): in(c1_e, X): in(c1_a, X)]0.
pie(r1, A, 1) :- ir(X, A), in(c1_e, X), in(c1_a, X), ix.
c(r1, A, 1) :- vr(X, A), in(c1_e, X), in(c1_a, X), ix.

%% coverage
out3(c1_a, X, r2) :- out(c1_b, X), out(c1_e, X), ix.
out(c1_a, X) :- out(c1_b, X), out(c1_e, X), pw.
%% sibling disjointness
% c1_b ! c1_e
ir(X, r3) :- in(c1_b, X), in(c1_e, X).
:- [vrs(X): in(c1_b, X): out(c1_e, X)]0, pw.
:- [vrs(X): out(c1_b, X): in(c1_e, X)]0, pw.
pie(r3, A, 1) :- ir(X, A), in(c1_b, X), out(c1_e, X), ix.
c(r3, A, 1) :- vr(X, A), in(c1_b, X), out(c1_e, X), ix.
pie(r3, A, 2) :- ir(X, A), out(c1_b, X), in(c1_e, X), ix.
c(r3, A, 2) :- vr(X, A), out(c1_b, X), in(c1_e, X), ix.

%% ISA
% c2_d isa c2_c
ir(X, r4) :- in(c2_d, X), out(c2_c, X), pw.
ir(X, prod(r4,R)) :- in(c2_d,X), out3(c2_c, X, R), ix.
:- [vrs(X): in(c2_d, X): in(c2_c, X)]0.
pie(r4, A, 1) :- ir(X, A), in(c2_d, X), in(c2_c, X), ix.
c(r4, A, 1) :- vr(X, A), in(c2_d, X), in(c2_c, X), ix.

% c2_f isa c2_c
ir(X, r5) :- in(c2_f, X), out(c2_c, X), pw.
ir(X, prod(r5,R)) :- in(c2_f,X), out3(c2_c, X, R), ix.
:- [vrs(X): in(c2_f, X): in(c2_c, X)]0.
pie(r5, A, 1) :- ir(X, A), in(c2_f, X), in(c2_c, X), ix.
c(r5, A, 1) :- vr(X, A), in(c2_f, X), in(c2_c, X), ix.

%% coverage
out3(c2_c, X, r6) :- out(c2_d, X), out(c2_f, X), ix.
out(c2_c, X) :- out(c2_d, X), out(c2_f, X), pw.
%% sibling disjointness
% c2_d ! c2_f
ir(X, r7) :- in(c2_d, X), in(c2_f, X).
:- [vrs(X): in(c2_d, X): out(c2_f, X)]0, pw.
:- [vrs(X): out(c2_d, X): in(c2_f, X)]0, pw.
pie(r7, A, 1) :- ir(X, A), in(c2_d, X), out(c2_f, X), ix.
c(r7, A, 1) :- vr(X, A), in(c2_d, X), out(c2_f, X), ix.
pie(r7, A, 2) :- ir(X, A), out(c2_d, X), in(c2_f, X), ix.
c(r7, A, 2) :- vr(X, A), out(c2_d, X), in(c2_f, X), ix.


%%% Articulations
% 1.a equals 2.c
ir(X, r8) :- out(c1_a,X), in(c2_c,X).
ir(X, r8) :- in(c1_a,X), out(c2_c,X).
ir(X, prod(r8,R)) :- out3(c1_a, X, R), in(c2_c,X), ix.
ir(X, prod(r8,R)) :- in(c1_a,X), out3(c2_c, X, R), ix.
pie(r8, A, 1) :- ir(X, A), in(c1_a, X), in(c2_c, X), ix.
c(r8, A, 1) :- vr(X, A), in(c1_a, X), in(c2_c, X), ix.


% 1.b {is_included_in equals} 2.d
ir(X, r9) :- in(c1_b,X), out(c2_d,X).
ir(X, prod(r9,R)) :- in(c1_b,X), out3(c2_d, X, R), ix.
vr(X, r9) | ir(X, r9) :- out(c1_b,X), in(c2_d,X).
pie(r9, A, 1) :- ir(X, A), in(c1_b, X), in(c2_d, X), ix.
c(r9, A, 1) :- vr(X, A), in(c1_b, X), in(c2_d, X), ix.


% 1.e {includes equals} 2.f
ir(X, r10) :- out(c1_e,X), in(c2_f,X).
ir(X, prod(r10,R)) :- out3(c1_e, X, R), in(c2_f,X), ix.
vr(X, r10) | ir(X, r10) :- in(c1_e,X), out(c2_f,X).
pie(r10, A, 1) :- ir(X, A), in(c1_e, X), in(c2_f, X), ix.
c(r10, A, 1) :- vr(X, A), in(c1_e, X), in(c2_f, X), ix.


%%% Decoding now
:- rel(X, Y, "="), rel(X, Y, "<"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, "="), rel(X, Y, ">"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, "="), rel(X, Y, "><"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, "="), rel(X, Y, "!"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, "<"), rel(X, Y, ">"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, "<"), rel(X, Y, "><"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, "<"), rel(X, Y, "!"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, ">"), rel(X, Y, "><"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, ">"), rel(X, Y, "!"), concept2(X, N1), concept2(Y, N2), pw.
:- rel(X, Y, "><"), rel(X, Y, "!"), concept2(X, N1), concept2(Y, N2), pw.
:- not rel(X, Y, "="), not rel(X, Y, "<"), not rel(X, Y, ">"), not rel(X, Y, "><"), not rel(X, Y, "!"), concept2(X, N1), concept2(Y, N2), N1 < N2, not ncf(X), not ncf(Y), pw.

rel(X, Y, "=") :- not hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2), pw.
rel(X, Y, "<") :- not hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2), pw.
rel(X, Y, ">") :- hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2), pw.
rel(X, Y, "><") :- hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2), pw.
rel(X, Y, "!") :- hint(X, Y, 0), not hint(X, Y, 1), hint(X, Y, 2), pw.


hint(X, Y, 0) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), in(X, R), out(Y, R), not ncf(X), not ncf(Y), pw.
hint(X, Y, 1) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), in(X, R), in(Y, R), not ncf(X), not ncf(Y), pw.
hint(X, Y, 2) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), out(X, R), in(Y, R), not ncf(X), not ncf(Y), pw.

