
import subprocess
import sys


def usage():
    print 'USAGE: python mir.py input_file output_file'

def main(infile, outfile): 
    args = infile + ' standard ' + outfile
    cmd = 'java -cp ./src reasoner.ApplyMIRReasoner ' + args
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
    else:
        main(sys.argv[1], sys.argv[2])

