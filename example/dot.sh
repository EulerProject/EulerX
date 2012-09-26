cd $1
list=$(ls *dot)
for i in $list
do
    NAME=`echo "$i" | cut -d'.' -f1`
    dot $i -Tpdf -o$NAME.pdf
done
