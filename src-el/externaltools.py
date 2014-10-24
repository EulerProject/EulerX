from subprocess import call

def runLattice(fileName):
    call("lattice.sh " + fileName, shell=True)
    
def runAddID(fileName):
    s = ""
    for i in range(len(fileName)):
        s = s + " -i " + fileName[i]
    call("input-wizard/addID" + s, shell=True)
    
def runAddIsa(fileName):
    call("input-wizard/addIsa -i " + fileName, shell=True)

def runP2C(fileName):
    call("input-wizard/p2c -i " + fileName, shell=True)

def runP2CT(fileName):
    call("input-wizard/p2c -i " + fileName[0] + " -t " + fileName[1], shell=True)

def runAddArt(fileName):
    call("input-wizard/addArt -i " + fileName, shell=True)

def runAddArtT(fileName):
    s = ""
    for i in range(1, len(fileName)):
        s = s + " -t " + fileName[i]
    call("input-wizard/addArt -i " + fileName[0] + s, shell=True)