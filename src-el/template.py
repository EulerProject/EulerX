from helper import *

class template:
    global dlvPwDc
    global dlvCbDc

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

    def getDlvPwDc():
        global dlvPwDc
        return dlvPwDc

    def getDlvCbDc():
        global dlvCbDc
        return dlvCbDc

    getDlvPwDc = Callable(getDlvPwDc)
    getDlvCbDc = Callable(getDlvCbDc)
