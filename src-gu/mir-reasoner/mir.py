#!/usr/bin/env python

import subprocess
import sys
from distutils.spawn import find_executable

def usage():
    print 'USAGE: python mir.py input_file output_file provenance_flag pw_flag benchmark_flag'
    
def main(infile, outfile, isProvenance, isPW, isBenchmark):
    if(isPW in ['True', 'true', 't', '1']):
        mirPW(infile, outfile, isProvenance, isBenchmark)
    else:
        mirNoPW(infile, outfile, isProvenance, isBenchmark)
        
def mirNoPW(infile, outfile, isProvenance, isBenchmark):
    args = infile + ' standard ' + outfile + ' ' + isProvenance
    src_path = find_executable('mir.py') + '/../src'
    if(isBenchmark in ['True', 'true', 't', '1']):
        cmd = 'time -f "real\t%es\nuser\t%Us\nsys\t%Ss" java -cp ./src reasoner.ApplyMIRReasoner ' + args
    else:
#        cmd = 'java -cp ./src reasoner.ApplyMIRReasoner ' + args
        cmd = 'java -cp ' + src_path + ' reasoner.ApplyMIRReasoner ' + args
    subprocess.call(cmd, shell=True)
    
def mirPW(infile, outfile, isProvenance, isBenchmark):
    args = infile + ' standard ' + outfile + ' standard ' + isProvenance
    src_path = find_executable('mir.py') + '/../src'
    if(isBenchmark in ['True', 'true', 't', '1']):
        cmd = 'time -f "real\t%es\nuser\t%Us\nsys\t%Ss" java -cp ./src reasoner.ApplyMIRReasonerPW ' + args
    else:
#        cmd = 'java -cp ./src reasoner.ApplyMIRReasonerPW ' + args
        cmd = 'java -cp ' + src_path + ' reasoner.ApplyMIRReasonerPW ' + args
    subprocess.call(cmd, shell=True)
    
if __name__ == "__main__":
    if len(sys.argv) == 6:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        usage()