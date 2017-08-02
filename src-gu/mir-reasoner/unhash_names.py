#!/usr/bin/env python2.7
import sys
import string
import json


""" basic  usage information """
def usage():
    print 'USAGE: python hashedinfile.txt hashfile.json'


""" return true if line is a taxonomy """
def is_taxonomy(line): 
    words = line.split()
    return len(words) == 3 and words[0].lower() == 'taxonomy'


""" return the taxonomy identifier """
def taxonomy_id(line): 
    words = line.split()
    return words[1]


""" return true if line is a hierarchy line """
def is_hierarchy(line): 
    return len(line) > 0 and line[0] == '('


""" returns a list of hierarchy terms """
def hierarchy_terms(line): 
    return [s.replace('(','').replace(')','') for s in line.split()]


""" return true if line is an articulation header """
def is_articulation_header(line):
    words = line.split()
    return len(words) > 0 and words[0] == 'articulation'


""" return true if line is an articulation """
def is_articulation(line):
    return (line) > 0 and line[0] == '['


""" returns a list of articulation terms """
def articulation_terms(line): 
    return [s.replace('[','').replace(']','') for s in line.split()]


""" return true if line is an Possible Worlds header """
def is_pw_header(line):
    words = line.split()
    return len(words) > 0 and words[0] == 'Possible'


def main(infile, hashfile): 
    inputfile = open(infile, 'r')
    hashedfile = open(hashfile, 'r')
    mapping = json.load(hashedfile)
    hashedfile.close()
    inv_mapping = {v: k for k, v in mapping.items()}

    taxonomy = ''
    for line in inputfile:
        # taxonomy section start
        if is_taxonomy(line):
            taxonomy = taxonomy_id(line)
            sys.stdout.write(line)
        # hirearchical spec
        elif is_hierarchy(line):
            terms = hierarchy_terms(line)
            sys.stdout.write('(')
            for term in terms[0:-1]:
                new_id = inv_mapping[taxonomy + '.' + term].split('.')[1]
                sys.stdout.write(new_id + ' ')
            sys.stdout.write(inv_mapping[taxonomy+'.'+terms[-1]].split('.')[1])
            sys.stdout.write(')\n')
        # articulation section
        elif is_articulation_header(line): 
            sys.stdout.write("\n"+line)
        elif is_articulation(line):
            terms = articulation_terms(line)
            sys.stdout.write('[' + inv_mapping[terms[0]] + ' ')
            for term in terms[1:-1]:
                sys.stdout.write(term + ' ')
            sys.stdout.write(inv_mapping[terms[-1]] + ']\n')
        # possible worlds section
        elif is_pw_header(line): 
            sys.stdout.write("\n"+line)            
    # write out the mapping
    inputfile.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        main(sys.argv[1], sys.argv[2])
