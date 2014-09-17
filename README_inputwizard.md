Euler Input Wizard Tools Manual


NAME
addID - add identifier column to input csv file
wizard - generate csv file of pairs of element with a relation in between, either “ISA” or “?” (user needs to define)
p2c - generate a txt file with CleanTax syntax from pairs csv file

SYNOPSIS
 cat in1_csv_file | addID > in2_csv_file
wizard  cat in2_csv_file | wizard > in3_csv_file
p2c  cat in3_csv_file | p2c -i  in1_csv_file> output_csv_file

DESCRIPTION
 addID
Note: It is assumed that the first line is a header line
Receives a csv file with 3 column <Simple_Name, According_To, Rank> as input and adds a new column <ID> to each row. The ID is of format <TaxonID>.<Rank><No>, in which <TaxonID> is the taxonomy id (a number assigned to each According_To value), <Rank> is a pair tuple produced by mapping the <Rank> column in the input into (one letter, number) where number shows the position of this rank in  and <No> is an incremental number that is assigned to the rows sorted based on <Rank, Simple_Name>.

 wizard 
Receives a csv file with 4 column  <ID, Simple_Name, According_To, Rank> as input and returns a csv file of suggested ISA pairs: 
<ID>, <TaxonID>,<Rank>, <No>,<Scientific_Name>, ISA, <ID>, <TaxonID>,<Rank>,<No>,<Scientific_Name> 
and suggested articulation pairs: 
<ID>, <TaxonID>,<Rank>, <No>,<Scientific_Name>, ? , <ID>, <TaxonID>,<Rank>,<No>,<Scientific_Name> 

the user is then asked to revise these relations and replace the ? with appropriate articulation. 

 p2c
Receives a csv file of revised articulation and ISA pairs, as well as the input file with the name of each taxonomic group, and converts it to standard cleanTax format.  