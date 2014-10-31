from subprocess import call

def runLattice(fileName):
    call("lattice.sh " + fileName, shell=True)
    
def runAddID(fileName):
    s = ""
    for i in range(len(fileName)):
        s = s + " -i " + fileName[i]
    call("addID" + s, shell=True)
    
def runAddIsa(fileName):
    call("addIsa -i " + fileName, shell=True)

def runP2C(fileName):
    call("p2c -i " + fileName, shell=True)

def runP2CT(fileName):
    call("p2c -i " + fileName[0] + " -t " + fileName[1], shell=True)

def runAddArt(fileName):
    call("addArt -i " + fileName, shell=True)

def runAddArtT(fileName):
    s = ""
    for i in range(1, len(fileName)):
        s = s + " -t " + fileName[i]
    call("addArt -i " + fileName[0] + s, shell=True)

def runC2CSV(fileName):
    call("c2csv -i " + fileName, shell=True)