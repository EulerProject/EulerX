Euler Input Wizard Tool Set Manual
-------------------------------------

NAME
addID - takes a csv file as input and adds an extra identifier column to it
(if multiple files are given as input, it merges them and operates on them as a unified file)

addIsa - takes one (or more) input files, groups them based on groupID outputs file ,"isa" + groupID, which contains a set of suggested ISA pairs for each group

addArt - takes one (or more) input files, and optionally one (or more) files of suggested ISA pairs, and outputs a set of suggested articulation pairs between the groups elements

p2c - generates a txt file with CleanTax syntax from pairs csv file

c2csv - generates a 3 column csv file from a cleanTax file

SYNOPSIS
./addID -i csv_file -i csv_file .... > csv_file

./addIsa  -i csv_file -i csv_file .... 

./addArt -i csv_file -i csv_file ....  -t isa1_csv_file -t -t isa2_csv_file > csv_file

./p2c  csv_file -i  csv_file> cleanTax_file 

./c2csv  -i  cleanTax_file > csv_file 

DESCRIPTION
 addID
Note: It is assumed that the first line is a header line
Receives one or more csv file with 3 column <Simple_Name, According_To, Rank> as input and adds a new column <ID> to each row. 
The ID is of format <TaxonID>.<Rank><No>, in which <TaxonID> is the taxonomy id (a number assigned to each According_To value),
 <Rank> is a pair tuple produced by mapping the <Rank> column in the input into (one letter, number) where number shows the position of this rank in  
 and <No> is an incremental number that is assigned to the rows sorted based on <Rank, Simple_Name>.

 addIsa 
Receives one or more csv file with 4 column  <ID, Simple_Name, According_To, Rank> as input and for each groupID, returns a csv file of suggested ISA pairs: 
<ID>, <TaxonID>,<Rank>, <No>,<Scientific_Name>, ISA, <ID>, <TaxonID>,<Rank>,<No>,<Scientific_Name> 
the user is then asked to verify these isa relations and use the result as input for the next step
* the user can use p2c to convert the suggested ISA pais to cleanTax format and visualize it using Euler visualizer (i.e. use c2y to convert it to yaml and y2d to convert to dot). 

 addArt
 Receives one or more csv file with 4 column  <ID, Simple_Name, According_To, Rank>, and optionally one or more files of suggested ISA pairs, as input and returns a csv file of suggested articulation pairs: 
 <ID>, <TaxonID>,<Rank>, <No>,<Scientific_Name>, ? , <ID>, <TaxonID>,<Rank>,<No>,<Scientific_Name> 
the user is then asked to revise these relations and replace the ? with appropriate articulation. 

 p2c
Receives a csv file of revised articulation or ISA pairs, or both as well as the input file with the name of each taxonomic group, and converts it to standard cleanTax format.  

c2csv
Receives a cleanTax file as input and returns a 3 column <Name, Author, Rank> csv file that can be used as an input for input wizard. 
The goal is to reverse engineer cleanTax files and compared the suggested articulation pairs by input wizard with the correct ones to gauge its efficiency.