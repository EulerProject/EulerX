from helper import *

class template:
    global encErrMsg
    encErrMsg = "\nEncoding error, please contact Mingmin at michen@ucdavis.edu"

    global aspVrCon              # Base vr concept encoding
    global aspMnCon              # Base mn concept encoding
    global aspDlCon              # Base dl concept encoding
    global aspDrCon              # Base dr concept encoding
    global aspCbCon              # Base cb new concept encoding
    global aspPwDc               # Base pw decoding
    global aspAllDc              # Base pw decoding with "--all"
    global aspCbDc               # Base cb decoding

    # Base constraints of regions for several encodings
    aspRnCnt = "%%% Constraints of regions.\n"\
	     + "irs(X) :- ir(X, _).\n"\
	     + "vrs(X) :- vr(X, _).\n"\
	     + "vr(X, X) :- not irs(X), r(X).\n"\
	     + "ir(X, X) :- not vrs(X), r(X).\n"\
	     + "ie(prod(A,B)) :- vr(X, A), ir(X, B), ix.\n"\
	     + ":- vrs(X), irs(X), pw.\n\n"\
	     + "%%% Inconsistency Explanation.\n"\
	     + "ie(s(R, A, Y)) :- pie(R, A, Y), not cc(R, Y), ix.\n"\
	     + "cc(R, Y) :- c(R, _, Y), ix.\n"

    aspVrCon = "\n%%% power\n"\
	     + "p(0,1).\n"\
	     + "p(N,M) :- r(N),N=N1+1,p(N1,M1),M=M1*2.\n\n"\
	     + "%%% bit\n"\
	     + "bit(M, N, 1):-r(M),count(N),not bit(M,N,0).\n\n"\
	     + "%%% Meaning of regions\n"\
             + "in(X, M) :- not out(X, M), r(M),concept(X,_,N),count(N).\n"\
             + "out(X, M) :- not in(X, M), r(M),concept(X,_,N),count(N).\n"\
	     + "in(X, M) :- r(M),concept(X,_,N),bit(M,N,1).\n"\
	     + "out(X, M) :- r(M),concept(X,_,N),bit(M,N,0).\n\n"\
	     + "ir(M, fi) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n"\
	     + "irs(M) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n"\
             + aspRnCnt

    aspMnCon = "\n\n%%% Meaning of regions\n"\
             + "in(X, M) :- r(M),concept(X,T,N),N1=N+1,bit(M,T,N1).\n"\
             + "out(X, M) :- r(M),concept(X,T,N),N1=N+1,not bit(M,T,N1).\n"\
             + "in(X, M) :- r(M),concept2(X,_),not out(X, M).\n"\
             + "out(X, M) :- out3(X, M, _), ix.\n"\
             + "irs(M) :- in(X, M), out(X, M), r(M), concept2(X,_).\n\n"\
             + aspRnCnt

    aspCbCon = "cb(X) :- newcon(X, _, _, _).\n"\
             + "cp(X) :- concept2(X, _).\n"\
             + "con(X) :- cb(X).\n"\
             + "con(X) :- cp(X).\n"\
	     + "combined2(C, 0) :- newcon(C, A, B, _), not rel(A, B, \"><\"), not rel(B, A, \"><\").\n"\
             + "in(X, M) :- newcon(X, Y, Z, 0), in(Y, M), out(Z, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 0), out(Y, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 0), in(Z, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 0), out(X, M), in(Y, M), out(Z, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 0), in(X, M), out(Y, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 0), in(X, M), in(Z, M).\n"\
             + "in(X, M) :- newcon(X, Y, Z, 1), in(Y, M), in(Z, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 1), out(Y, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 1), out(Z, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 1), out(X, M), in(Y, M), in(Z, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 1), in(X, M), out(Y, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 1), in(X, M), out(Z, M).\n"\
             + "in(X, M) :- newcon(X, Y, Z, 2), out(Y, M), in(Z, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 2), in(Y, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 2), out(Z, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 2), out(X, M), out(Y, M), in(Z, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 2), in(X, M), in(Y, M).\n"\
             + "%irs(M) :- newcon(X, Y, Z, 2), in(X, M), out(Z, M).\n"\
             + "%%%% concept to combined concept\n"\
	     + "%cnotcc(C,CC, T) :- concept2(C, T), cb(CC), in(C, M), out(CC, M), vrs(M).\n"\
	     + "%cnotcc(C,CC, T) :- concept2(C, T), cb(CC), out(C, M), in(CC, M), vrs(M).\n"\
	     + "%cnotcc(C,CC, T) :- concept2(C, T), cb(CC), in(CC, M), irs(M).\n"\
	     + "%ctocc(C, CC, T) :- concept2(C, T), cb(CC), not cnotcc(C, CC, T).\n"\
	     + "%ctocc(C, CC, 2) :- newcon(C, X, Y, 0), ctocc(X, XC, _), ctocc(Y, YC, _), minus(XC, YC, CC).\n"\
	     + "%ctocc(C, CC, 2) :- newcon(C, X, Y, 1), ctocc(X, XC, _), ctocc(Y, YC, _), and(XC, YC, CC).\n"\
	     + "%ctocc(C, CC, 2) :- newcon(C, X, Y, 2), ctocc(X, XC, _), ctocc(Y, YC, _), minus(YC, XC, CC).\n"\
             + "%\n%%% and op\n"\
	     + "%nand(X, Y, Z) :- con(X), con(Y), con(Z), r(M), out(X, M), in(Z, M).\n"\
	     + "%nand(X, Y, Z) :- con(X), con(Y), con(Z), r(M), out(Y, M), in(Z, M).\n"\
	     + "%nand(X, Y, Z) :- con(X), con(Y), con(Z), r(M), in(X, M), in(Y, M), out(Z, M).\n"\
	     + "%and(X, Y, Z) :- con(X), con(Y), con(Z), not nand(X, Y, Z).\n"\
             + "%\n%%% minus op\n"\
	     + "%nminus(X, Y, Z) :- con(X), con(Y), con(Z), r(M), out(X, M), in(Z, M).\n"\
	     + "%nminus(X, Y, Z) :- con(X), con(Y), con(Z), r(M), in(X, M), out(Y, M), out(Z, M).\n"\
	     + "%nminus(X, Y, Z) :- con(X), con(Y), con(Z), r(M), in(X, M), in(Y, M), in(Z, M).\n"\
	     + "%minus(X, Y, Z) :- con(X), con(Y), con(Z), not nminus(X, Y, Z).\n"


    aspDlCon = "%%% Meaning of regions\n"\
	     + "in(X, M) :- r(M),concept(X,_,N),bit(M,N).\n"\
	     + "in(X, M) v out(X, M) :- r(M),concept(X,_,N),bit(M,N1), N<>N1.\n"\
	     + "irs(M) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n\n"\
	     + "vrs(M) :- r(M), not irs(M).\n\n"\
             + aspRnCnt


    aspDrCon = "\n% GENERATE possible labels\n"\
	     + "node(X) :- concept(X, _, _).\n"\
             + "rel(X, Y, R) :- label(X, Y, R), X < Y.\n"\
	     + "label(X, X, eq) :- node(X).\n"\
	     + "label(X,Y,eq) v label(X,Y,ds) v label(X,Y,in) v label(X,Y,ls) v label(X,Y,ol) :-\n"\
	     + "	    node(X),node(Y), X <> Y.\n\n"\
             + "% Make sure they are pairwise disjoint\n"\
             + ":- label(X,Y,eq), label(X,Y,ds).\n"\
             + ":- label(X,Y,eq), label(X,Y,in).\n"\
             + ":- label(X,Y,eq), label(X,Y,ls).\n"\
             + ":- label(X,Y,eq), label(X,Y,ol).\n"\
             + ":- label(X,Y,ds), label(X,Y,in).\n"\
             + ":- label(X,Y,ds), label(X,Y,ls).\n"\
             + ":- label(X,Y,ds), label(X,Y,ol).\n"\
	     + ":- label(X,Y,in), label(X,Y,ls).\n"\
	     + ":- label(X,Y,in), label(X,Y,ol).\n"\
	     + ":- label(X,Y,ls), label(X,Y,ol).\n"\
             + "% integrity constraint for weak composition\n"\
             + "label(X, Y, in) :- label(Y, X, ls).\n"\
             + "label(X, Y, ls) :- label(Y, X, in).\n"\
             + "label(X, Y, ol) :- label(Y, X, ol).\n"\
             + "label(X, Y, ds) :- label(Y, X, ds).\n"\
             + "sum(X, Y, Z) :- sum(X, Z, Y).\n"\
             + "label(X, Y, in) :- sum(X, Y, _).\n"\
	     + "label(X,Z,eq) :- label(X,Y,eq), label(Y,Z,eq).\n"\
	     + "label(X,Z,in) :- label(X,Y,eq), label(Y,Z,in).\n"\
	     + "label(X,Z,ls) :- label(X,Y,eq), label(Y,Z,ls).\n"\
	     + "label(X,Z,ol) :- label(X,Y,eq), label(Y,Z,ol).\n"\
	     + "label(X,Z,ds) :- label(X,Y,eq), label(Y,Z,ds).\n"\
	     + "label(X,Z,in) :- label(X,Y,in), label(Y,Z,eq).\n"\
	     + "label(X,Z,in) :- label(X,Y,in), label(Y,Z,in).\n"\
	     + "label(X,Z,eq) v label(X,Z,in) v label(X,Z,ol) v label(X,Z,ls) :- label(X,Y,in), label(Y,Z,ls).\n"\
	     + "label(X,Z,in) v label(X,Z,ol) :- label(X,Y,in), label(Y,Z,ol).\n"\
	     + "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,in), label(Y,Z,ds).\n"\
	     + "label(X,Z,ls) :- label(X,Y,ls), label(Y,Z,eq).\n"\
	     + "%% Any of RCC5 is possible for X vs Z\n"\
	     + "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,ol) :- label(X,Y,ls), label(Y,Z,in).\n"\
	     + "label(X,Z,ls) :- label(X,Y,ls), label(Y,Z,ls).\n"\
	     + "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ls), label(Y,Z,ol).\n"\
	     + "label(X,Z,ds) :- label(X,Y,ls), label(Y,Z,ds).\n"\
	     + "label(X,Z,ol) :- label(X,Y,ol), label(Y,Z,eq).\n"\
	     + "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ol), label(Y,Z,in).\n"\
	     + "label(X,Z,ol) v label(X,Z,ls) :- label(X,Y,ol), label(Y,Z,ls).\n"\
	     + "%% Any of RCC5 is possible for X vs Z\n"\
	     + "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,in) v label(X,Z,ls) v label(X,Z,ol) :- label(X,Y,ol), label(Y,Z,ol).\n"\
	     + "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ol), label(Y,Z,ds).\n"\
	     + "label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,eq).\n"\
	     + "label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,in).\n"\
	     + "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,ls).\n"\
	     + "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,ol).\n"\
	     + "%% Any of RCC5 is possible for X vs Z\n"\
	     + "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,in) v label(X,Z,ls) v label(X,Z,ol) :- label(X,Y,ds), label(Y,Z,ds).\n\n"\
             + "label(X, Y, ds) :- sum(X, X1, X2), label(X1, Y, ds), label(X2, Y, ds).\n"\
             + "sum(X, Y, X2) :- sum(X, X1, X2), label(X1, Y, eq).\n"\
             + "sum(Y, X1, X2) :- sum(X, X1, X2), label(X, Y, eq).\n"\
             + "%% A + (B + C) = (A + B) + C\n"\
             + "label(X, Y, eq) :- sum(X, A, X1), sum(X1, B, C), sum(Y, B, Y1), sum(Y1, A, C).\n"\
             + "label(X, Y, ol) v label(X, Y, in) :- sum(X, X1, X2), label(X1, Y, ol), label(X2, Y, ol).\n"\
             + "label(X, Y, R) :- sum(X, X1, X2), sum(Y, Y1, Y2), label(X1, Y1, eq), label(X2, Y2, R).\n"\
             + "label(X2, Y2, R) :- sum(X, X1, X2), sum(Y, Y1, Y2), label(X1, Y1, eq), label(X, Y, R).\n"\
             + "label(X, Y, in) v label(X, Y, eq) :- sum(Y, Y1, Y2), label(X, Y1, in), label(X, Y2, in).\n"\

    aspPwDc = "%%% Decoding now\n"\
            + ":- rel(X, Y, \"=\"), rel(X, Y, \"<\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \"=\"), rel(X, Y, \">\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \"=\"), rel(X, Y, \"><\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \"=\"), rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \"<\"), rel(X, Y, \">\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \"<\"), rel(X, Y, \"><\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \"<\"), rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \">\"), rel(X, Y, \"><\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \">\"), rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- rel(X, Y, \"><\"), rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), pw.\n"\
            + ":- not rel(X, Y, \"=\"), not rel(X, Y, \"<\"), not rel(X, Y, \">\"), not rel(X, Y, \"><\"), not rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), N1 < N2, not ncf(X), not ncf(Y), pw.\n\n"\
            + "rel(X, Y, \"=\") :- not hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2), pw.\n"\
            + "rel(X, Y, \"<\") :- not hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2), pw.\n"\
            + "rel(X, Y, \">\") :- hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2), pw.\n"\
            + "rel(X, Y, \"><\") :- hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2), pw.\n"\
            + "rel(X, Y, \"!\") :- hint(X, Y, 0), not hint(X, Y, 1), hint(X, Y, 2), pw.\n\n\n"



    hintart = "hint(X, Y, 0) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), in(X, R), out(Y, R), not ncf(X), not ncf(Y), pw.\n"\
            + "hint(X, Y, 1) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), in(X, R), in(Y, R), not ncf(X), not ncf(Y), pw.\n"\
            + "hint(X, Y, 2) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), out(X, R), in(Y, R), not ncf(X), not ncf(Y), pw.\n\n"

    hintall = "hint(X, Y, 0) :- concept2(X, N1), concept2(Y, N2), X < Y, vrs(R), in(X, R), out(Y, R), not ncf(X), not ncf(Y), pw.\n"\
            + "hint(X, Y, 1) :- concept2(X, N1), concept2(Y, N2), X < Y, vrs(R), in(X, R), in(Y, R), not ncf(X), not ncf(Y), pw.\n"\
            + "hint(X, Y, 2) :- concept2(X, N1), concept2(Y, N2), X < Y, vrs(R), out(X, R), in(Y, R), not ncf(X), not ncf(Y), pw.\n\n"

    aspAllDc = aspPwDc + hintall

    aspPwDc += hintart

    aspCbDc  = aspPwDc
            #+  "combined(XC,0,3) :- ctocc(X, XC, _), combined(X,2,_).\n"\
            #+  "combined(Y,0,2) :- relcc(X,Y,\"=\"), newcon(X, _, _, 1), newcon(Y, _, _, 0).\n"\
            #+  "combined(Y,0,2) :- relcc(X,Y,\"=\"), newcon(X, _, _, 1), newcon(Y, _, _, 2).\n"\
            #+  "combined(Y,0,2) :- relcc(Y,X,\"=\"), newcon(X, _, _, 1), newcon(Y, _, _, 0).\n"\
            #+  "combined(Y,0,2) :- relcc(Y,X,\"=\"), newcon(X, _, _, 1), newcon(Y, _, _, 2).\n"\
            #+  "combined(XC,0,2) :- rel(X,Y,\"><\"), ctocc(X, XC, _).\n"\
            #+  "combined(YC,0,2) :- rel(X,Y,\"><\"), ctocc(Y, YC, _).\n"\
            #+  "combined2(Y,0) :- relcc(X,Y,\"=\"),cb(Y).\n"\
            #+  "hant(X, Y, 0) :- combined(X,1,Z), combined(Y,1,W), not hant(X, Y, 3), vrs(R), in(X, R), out(Y, R).\n"\
            #+  "hant(X, Y, 0) :- combined(X,1,2), combined(Y,1,2), not hant(X, Y, 3), vrs(R), in(X, R), out(Y, R).\n"\
            #+  "hant(X, Y, 1) :- combined(X,1,Z), combined(Y,1,W), not hant(X, Y, 3), vrs(R), in(X, R),  in(Y, R).\n"\
            #+  "hant(X, Y, 1) :- combined(X,1,2), combined(Y,1,2), not hant(X, Y, 3), vrs(R), in(X, R),  in(Y, R).\n"\
            #+  "hant(X, Y, 2) :- combined(X,1,Z), combined(Y,1,W), not hant(X, Y, 3), vrs(R), out(X, R), in(Y, R).\n"\
            #+  "hant(X, Y, 2) :- combined(X,1,2), combined(Y,1,2), not hant(X, Y, 3), vrs(R), out(X, R), in(Y, R).\n"\
            #+  "combined2(X,0) :- relcc(X,Y,\"><\").\n"\
            #+  "combined2(Y,0) :- relcc(X,Y,\"><\").\n"\
    aspCbDc += "%%% Combined concept decoding\n"\
            +  "combined(X,1,0) :- rel(X,Y,\">\").\n"\
            +  "combined(X,1,0) :- rel(X,Y,\"<\").\n"\
            +  "combined(X,1,0) :- rel(X,Y,\"=\").\n"\
            +  "combined(X,1,0) :- rel(X,Y,\"!\").\n"\
            +  "combined(Y,1,1) :- rel(X,Y,\">\").\n"\
            +  "combined(Y,1,1) :- rel(X,Y,\"<\").\n"\
            +  "combined(Y,1,1) :- rel(X,Y,\"=\").\n"\
            +  "combined(Y,1,1) :- rel(X,Y,\"!\").\n"\
            +  "combined(Z,1,2) :- rel(X,Y,\"><\"), newcon(Z, X, Y, _).\n"\
            +  "%%% unhide the overlap concepts\n"\
            +  "combined(X,1,0) :- rel(X,Y,\"><\").\n"\
            +  "combined(X,0,0) :- rel(X,Y,\"><\"), hide.\n"\
            +  "%%% unhide the overlap concepts\n"\
            +  "combined(Y,1,1) :- rel(X,Y,\"><\").\n"\
            +  "combined(Y,0,1) :- rel(X,Y,\"><\"), hide.\n"\
            +  "combined2(X,Y) :- combined(X,Y,Z).\n"\
            +  "combined2(X,1) :- not combined2(X,0), con(X).\n"\
            +  "combined2(X,2) :- combined2(X,1), not combined2(X,0), con(X).\n"\
            +  "combined2(X,1) :- relcc(X,Y,\"<\").\n"\
            +  "combined2(X,1) :- relcc(X,Y,\">\").\n"\
            +  "combined2(X,1) :- relcc(X,Y,\"=\").\n"\
            +  "combined2(X,1) :- relcc(X,Y,\"!\").\n"\
            +  "combined2(Y,1) :- relcc(X,Y,\"<\").\n"\
            +  "combined2(Y,1) :- relcc(X,Y,\">\").\n"\
            +  "combined2(Y,1) :- relcc(X,Y,\"=\"),con(Y).\n"\
            +  "combined2(Y,1) :- relcc(X,Y,\"!\").\n"\
            +  "hant(X, X, 3) :- combined2(X,1).\n"\
            +  "hant(X, Y, 0) :- combined2(X,1), combined2(Y,1), not hant(X, Y, 3), vrs(R), in(X, R), out(Y, R).\n"\
            +  "hant(X, Y, 1) :- combined2(X,1), combined2(Y,1), not hant(X, Y, 3), vrs(R), in(X, R),  in(Y, R).\n"\
            +  "hant(X, Y, 2) :- combined2(X,1), combined2(Y,1), not hant(X, Y, 3), vrs(R), out(X, R), in(Y, R).\n"\
            +  "relcc(X, Y, \"=\") :- X<Y, not hant(X, Y, 0), hant(X, Y, 1), not hant(X, Y, 2), pw.\n"\
            +  "relcc(X, Y, \"<\") :- X<Y, not hant(X, Y, 0), hant(X, Y, 1), hant(X, Y, 2), pw.\n"\
            +  "relcc(X, Y, \">\") :- X<Y, hant(X, Y, 0), hant(X, Y, 1), not hant(X, Y, 2), pw.\n"\
            +  "relcc(X, Y, \"><\") :- X<Y, hant(X, Y, 0), hant(X, Y, 1), hant(X, Y, 2), pw.\n"\
            +  "relcc(X, Y, \"!\") :- X<Y, hant(X, Y, 0), not hant(X, Y, 1), hant(X, Y, 2), pw.\n"\
            +  "%combined2(Z,1) :- relcc(X,Y,\"><\"), and(X, Y, Z).\n"\
            +  "%%%% unhide the overlap concepts\n"\
            +  "%combined2(X,1) :- relcc(X,Y,\"><\"), and(X, Y, Z).\n"\
            +  "%combined2(X,0) :- relcc(X,Y,\"><\"), and(X, Y, Z), hide.\n"\
            +  "%%%% unhide the overlap concepts\n"\
            +  "%combined2(Y,1) :- relcc(X,Y,\"><\"), and(X, Y, Z).\n"\
            +  "%combined2(Y,0) :- relcc(X,Y,\"><\"), and(X, Y, Z), hide.\n"\
            +  "%combined2(Z,1) :- relcc(X,Y,\"><\"), minus(X, Y, Z).\n"\
            +  "%%%% unhide the overlap concepts\n"\
            +  "%combined2(X,1) :- relcc(X,Y,\"><\"), minus(X, Y, Z).\n"\
            +  "%combined2(X,0) :- relcc(X,Y,\"><\"), minus(X, Y, Z), hide.\n"\
            +  "%%%% unhide the overlap concepts\n"\
            +  "%combined2(Y,1) :- relcc(X,Y,\"><\"), minus(X, Y, Z).\n"\
            +  "%combined2(Y,0) :- relcc(X,Y,\"><\"), minus(X, Y, Z), hide.\n"\
            +  "%combined2(Z,1) :- relcc(X,Y,\"><\"), minus(Y, X, Z).\n"\
            +  "%%%% unhide the overlap concepts\n"\
            +  "%combined2(X,1) :- relcc(X,Y,\"><\"), minus(Y, X, Z).\n"\
            +  "%combined2(X,0) :- relcc(X,Y,\"><\"), minus(Y, X, Z), hide.\n"\
            +  "%%%% unhide the overlap concepts\n"\
            +  "%combined2(Y,1) :- relcc(X,Y,\"><\"), minus(Y, X, Z).\n"\
            +  "%combined2(Y,0) :- relcc(X,Y,\"><\"), minus(Y, X, Z), hide.\n"\
            +  "relout(X, Y, Z) :- relcc(X, Y, Z), combined2(X, 2), combined2(Y, 2).\n"
            #+  "relout(X, Y, Z) :- relcc(X, Y, Z), combined(X, 2, T), combined(Y, 2, S), T<S.\n"\
            #+  "relout(X, Y, Z) :- relcc(X, Y, Z), combined(X, 2, 2), combined(Y, 2, 2).\n"

    #if self.enc & encode["cb"]:
    #    dlvDc += "hint(X, Y, 0) :- concept2(X, N1), concept2(Y, N2), vrs(R), in(X, R), out(Y, R), pw.\n"
    #    dlvDc += "hint(X, Y, 1) :- concept2(X, N1), concept2(Y, N2), vrs(R), in(X, R), in(Y, R), pw.\n"
    #    dlvDc += "hint(X, Y, 2) :- concept2(X, N1), concept2(Y, N2), vrs(R), out(X, R), in(Y, R), pw.\n\n"

    # Binary encoding base constraints
    def getAspVrCon():
        global aspVrCon
        return aspVrCon

    # Polynomial encoding base constraints
    def getAspMnCon():
        global aspMnCon
        return aspMnCon

    # Probability encoding base constraints
    def getAspDlCon():
        global aspDlCon
        return aspDlCon

    # Direct encoding base constraints
    def getAspDrCon():
        global aspDrCon
        return aspDrCon

    def getAspCbCon():
        global aspCbCon
        return aspCbCon

    def getAspPwDc():
        global aspPwDc
        return aspPwDc

    def getAspAllDc():
        global aspAllDc
        return aspAllDc

    def getAspCbDc():
        global aspCbDc
        return aspCbDc

    def getEncErrMsg():
        global encErrMsg
        return encErrMsg

    getAspVrCon = Callable(getAspVrCon)
    getAspMnCon = Callable(getAspMnCon)
    getAspDlCon = Callable(getAspDlCon)
    getAspDrCon = Callable(getAspDrCon)
    getAspCbCon = Callable(getAspCbCon)
    getAspPwDc  = Callable(getAspPwDc)
    getAspAllDc  = Callable(getAspAllDc)
    getAspCbDc  = Callable(getAspCbDc)
    getEncErrMsg= Callable(getEncErrMsg)
