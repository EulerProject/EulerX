1-  Run   
./addRank input.csv > output.csv 
input.csv is a MIR file 
output.csv is a 3 column csv file <Name, Year, Rank>. You will see a number of question marks (?) in Rank column in this file, these are elements in Order ranking group. You can fill those with correct ranks before proceeding to the next step

2-  Run
 ./mirStats -i input.csv -r ranks.csv > out.txt
input.csv is the same MIR as previous step 
ranks.csv is the output of the previous step 

The output is a text file which contains a table in a similar format to the one in the paper (with some additional information). To get the best view of the table, you'll need to maximize the size of the text file.
If you see some non-zero values in the "?" row, it means, there are still some "?" in the ranks file that need to be replaced with the correct ranks.