from helper import *

class template:
    global dlvCbCon              # Base cb new concept encoding
    global dlvPwDc               # Base pw decoding
    global dlvCbDc               # Base cb decoding

    dlvCbCon = "cb(X) :- newcon(X, _, _, _).\n"\
             + "cp(X) :- concept2(X, _).\n"\
             + "con(X) :- cb(X).\n"\
             + "con(X) :- cp(X).\n"\
             + "in(X, M) :- newcon(X, Y, Z, 0), in(Y, M), out(Z, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 0), out(Y, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 0), in(Z, M).\n"\
             + "in(X, M) :- newcon(X, Y, Z, 1), in(Y, M), in(Z, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 1), out(Y, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 1), out(Z, M).\n"\
             + "in(X, M) :- newcon(X, Y, Z, 2), out(Y, M), in(Z, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 2), in(Y, M).\n"\
             + "out(X, M) :- newcon(X, Y, Z, 2), out(Z, M).\n"\

             + "%%% concept to combined concept\n"\
	     + "cnotcc(C,CC) :- concept2(C,_), cb(CC), in(C, M), out(CC, M), vrs(M).\n"\
	     + "cnotcc(C,CC) :- concept2(C,_), cb(CC), out(C, M), in(CC, M), vrs(M).\n"\
	     + "cnotcc(C,CC) :- concept2(C,_), cb(CC), in(CC, M), irs(M).\n"\
	     + "ctocc(C, CC) :- concept2(C,_), cb(CC), not cnotcc(C, CC).\n"\
	     + "ctocc(C, CC) :- newcon(C, X, Y, 0), ctocc(X, XC), ctocc(Y, YC), minus(XC, YC, CC).\n"\
	     + "ctocc(C, CC) :- newcon(C, X, Y, 1), ctocc(X, XC), ctocc(Y, YC), and(XC, YC, CC).\n"\
	     + "ctocc(C, CC) :- newcon(C, X, Y, 2), ctocc(X, XC), ctocc(Y, YC), minus(YC, XC, CC).\n"\

             + "\n%%% and op\n"\
	     + "nand(X, Y, Z) :- con(X), con(Y), con(Z), r(M), out(X, M), in(Z, M).\n"\
	     + "nand(X, Y, Z) :- con(X), con(Y), con(Z), r(M), out(Y, M), in(Z, M).\n"\
	     + "nand(X, Y, Z) :- con(X), con(Y), con(Z), r(M), in(X, M), in(Y, M), out(Z, M).\n"\
	     + "and(X, Y, Z) :- con(X), con(Y), con(Z), not nand(X, Y, Z).\n"\

             + "\n%%% minus op\n"\
	     + "nminus(X, Y, Z) :- con(X), con(Y), con(Z), r(M), out(X, M), in(Z, M).\n"\
	     + "nminus(X, Y, Z) :- con(X), con(Y), con(Z), r(M), in(X, M), out(Y, M), out(Z, M).\n"\
	     + "nminus(X, Y, Z) :- con(X), con(Y), con(Z), r(M), in(X, M), in(Y, M), in(Z, M).\n"\
	     + "minus(X, Y, Z) :- con(X), con(Y), con(Z), not nminus(X, Y, Z).\n"

   #self.baseCb += "\n%%% power\n"
   #self.baseCb += "p(1,1).\n"
   #self.baseCb += "p(N,M) :- #int(N),N>0,#succ(N1,N),p(N1,M1),M=M1*2.\n\n"
   
   #self.baseCb += "%%% bit2\n"
   #self.baseCb += "bit2(M, N, 0):-cb(M),r(N),p(N,P),M1=M/P,#mod(M1,2,0).\n"
   #self.baseCb += "bit2(M, N, 1):-cb(M),r(N),not bit2(M,N,0).\n\n"

    dlvPwDc = "%%% Decoding now\n"\
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
          + ":- not rel(X, Y, \"=\"), not rel(X, Y, \"<\"), not rel(X, Y, \">\"), not rel(X, Y, \"><\"), not rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), N1 < N2, pw.\n\n"\
          + "rel(X, Y, \"=\") :- not hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2), pw.\n"\
          + "rel(X, Y, \"<\") :- not hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2), pw.\n"\
          + "rel(X, Y, \">\") :- hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2), pw.\n"\
          + "rel(X, Y, \"><\") :- hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2), pw.\n"\
          + "rel(X, Y, \"!\") :- hint(X, Y, 0), not hint(X, Y, 1), hint(X, Y, 2), pw.\n\n\n"\
          + "hint(X, Y, 0) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), in(X, R), out(Y, R), pw.\n"\
          + "hint(X, Y, 1) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), in(X, R), in(Y, R), pw.\n"\
          + "hint(X, Y, 2) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), out(X, R), in(Y, R), pw.\n\n"


    dlvCbDc  = dlvPwDc
    dlvCbDc += "%%% Combined concept decoding\n"\
            +  "combined(XC,0) :- ctocc(X, XC).\n"\
            +  "combined(X,1) :- rel(X,Y,\">\").\n"\
            +  "combined(X,1) :- rel(X,Y,\"<\").\n"\
            +  "combined(X,1) :- rel(X,Y,\"=\").\n"\
            +  "combined(X,1) :- rel(X,Y,\"!\").\n"\
            +  "combined(Y,1) :- rel(X,Y,\">\").\n"\
            +  "combined(Y,1) :- rel(X,Y,\"<\").\n"\
            +  "combined(Y,1) :- rel(X,Y,\"=\").\n"\
            +  "combined(Y,1) :- rel(X,Y,\"!\").\n"\
            +  "combined(Z,1) :- rel(X,Y,\"><\"), newcon(Z, X, Y, _).\n"\
            +  "combined(Y,0) :- relcc(X,Y,\"=\"), newcon(X, _, _, 1), newcon(Y, _, _, 0).\n"\
            +  "combined(Y,0) :- relcc(X,Y,\"=\"), newcon(X, _, _, 1), newcon(Y, _, _, 2).\n"\
            +  "combined(Y,0) :- relcc(Y,X,\"=\"), newcon(X, _, _, 1), newcon(Y, _, _, 0).\n"\
            +  "combined(Y,0) :- relcc(Y,X,\"=\"), newcon(X, _, _, 1), newcon(Y, _, _, 2).\n"\
            +  "combined(XC,0) :- rel(X,Y,\"><\"), ctocc(X, XC).\n"\
            +  "combined(YC,0) :- rel(X,Y,\"><\"), ctocc(Y, YC).\n"\
            +  "combined(X,0) :- rel(X,Y,\"><\").\n"\
            +  "combined(Y,0) :- rel(X,Y,\"><\").\n"\
            +  "combined(X,0) :- not combined(X,1), con(X).\n"\
            +  "combined(X,2) :- combined(X,1), not combined(X,0), con(X).\n"\
            +  "combined(X,1) :- relcc(X,Y,\"<\").\n"\
            +  "combined(X,1) :- relcc(X,Y,\">\").\n"\
            +  "combined(X,1) :- relcc(X,Y,\"=\").\n"\
            +  "combined(X,1) :- relcc(X,Y,\"!\").\n"\
            +  "combined(Y,1) :- relcc(X,Y,\"<\").\n"\
            +  "combined(Y,1) :- relcc(X,Y,\">\").\n"\
            +  "combined(Y,1) :- relcc(X,Y,\"=\").\n"\
            +  "combined(Y,1) :- relcc(X,Y,\"!\").\n"\
            +  "hant(X, Y, 0) :- combined(X,1), combined(Y,1), not X=Y, vrs(R), in(X, R), out(Y, R).\n"\
            +  "hant(X, Y, 1) :- combined(X,1), combined(Y,1), not X=Y, vrs(R), in(X, R),  in(Y, R).\n"\
            +  "hant(X, Y, 2) :- combined(X,1), combined(Y,1), not X=Y, vrs(R), out(X, R), in(Y, R).\n"\
            +  "relcc(X, Y, \"=\") :- X<Y, not hant(X, Y, 0), hant(X, Y, 1), not hant(X, Y, 2), pw.\n"\
            +  "relcc(X, Y, \"<\") :- X<Y, not hant(X, Y, 0), hant(X, Y, 1), hant(X, Y, 2), pw.\n"\
            +  "relcc(X, Y, \">\") :- X<Y, hant(X, Y, 0), hant(X, Y, 1), not hant(X, Y, 2), pw.\n"\
            +  "relcc(X, Y, \"><\") :- X<Y, hant(X, Y, 0), hant(X, Y, 1), hant(X, Y, 2), pw.\n"\
            +  "relcc(X, Y, \"!\") :- X<Y, hant(X, Y, 0), not hant(X, Y, 1), hant(X, Y, 2), pw.\n"\
            +  "combined(X,0) :- relcc(X,Y,\"><\").\n"\
            +  "combined(Y,0) :- relcc(X,Y,\"><\").\n"\
            +  "combined(Z,1) :- relcc(X,Y,\"><\"), and(X, Y, Z).\n"\
            +  "combined(Z,1) :- relcc(X,Y,\"><\"), minus(X, Y, Z).\n"\
            +  "combined(Z,1) :- relcc(X,Y,\"><\"), minus(Y, X, Z).\n"\
            +  "relout(X, Y, Z) :- relcc(X, Y, Z), combined(X, 2), combined(Y, 2).\n"

    #if self.enc & encode["cb"]:
    #    dlvDc += "hint(X, Y, 0) :- concept2(X, N1), concept2(Y, N2), vrs(R), in(X, R), out(Y, R), pw.\n"
    #    dlvDc += "hint(X, Y, 1) :- concept2(X, N1), concept2(Y, N2), vrs(R), in(X, R), in(Y, R), pw.\n"
    #    dlvDc += "hint(X, Y, 2) :- concept2(X, N1), concept2(Y, N2), vrs(R), out(X, R), in(Y, R), pw.\n\n"

    def getDlvCbCon():
        global dlvCbCon
        return dlvCbCon

    def getDlvPwDc():
        global dlvPwDc
        return dlvPwDc

    def getDlvCbDc():
        global dlvCbDc
        return dlvCbDc

    getDlvPwDc = Callable(getDlvPwDc)
    getDlvCbDc = Callable(getDlvCbDc)
