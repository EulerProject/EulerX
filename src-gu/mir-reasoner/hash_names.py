#!/usr/bin/env python
import sys
import string
import json


""" basic  usage information """
def usage():
    print 'USAGE: python infile.txt'


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


def main(infile): 
    inputfile = open(infile, 'r')
    ident = 1
    taxonomy = 0
    mapping = {}
    taxonomy1id = ""
    taxonomy2id = ""
    taxonomy1desc = ""
    taxonomy2desc = ""
    for line in inputfile:
        # taxonomy section start
        if is_taxonomy(line): 
            taxonomy = taxonomy_id(line)
            if taxonomy1id == "":
                taxonomy1id = line.split()[1]
                taxonomy1desc = line.split()[2]
            elif taxonomy2id == "":
                taxonomy2id = line.split()[1]
                taxonomy2desc = line.split()[2]
            sys.stdout.write(line)
        # hirearchical spec
        elif is_hierarchy(line):
            sys.stdout.write('(')
            terms = hierarchy_terms(line)
            for i in range(len(terms)): 
                term = terms[i]
                plain_id = str(ident)
                old_id = taxonomy + '.' + term
                new_id = taxonomy + '.' + plain_id
                if old_id not in mapping:
                    mapping[old_id] = new_id
                    ident += 1
                else:
                    new_id = mapping[old_id]
                    plain_id = new_id.split('.')[1]
                sys.stdout.write(plain_id)
                if i != len(terms) - 1:
                    sys.stdout.write(' ')
            sys.stdout.write(')\n')
        # articulation section
        elif is_articulation_header(line):
            tmpStr = "\narticulation " + taxonomy1id+taxonomy2id + " " +  taxonomy1desc+taxonomy2desc + "\n"
            sys.stdout.write(tmpStr)
        elif is_articulation(line):
            terms = articulation_terms(line)
            sys.stdout.write('[' + mapping[terms[0]] + ' ')
            for term in terms[1:-1]:
                sys.stdout.write(term + ' ')
            sys.stdout.write(mapping[terms[-1]] + ']\n')            
    # write out the mapping
    inputfile.close()
    outputfile = open('hash_values.json', 'w')
    outputfile.write(json.dumps(mapping))
    outputfile.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main(sys.argv[1])
