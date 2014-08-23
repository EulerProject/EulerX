
from subprocess import call

def main(): 
    print 'Compiling files ...'
    files = 'src/common_classes/*.java src/converter/*.java src/reasoner/*.java'
    call('javac -cp ./src ' + files, shell=True)

if __name__ == "__main__":
    main()

