#!/bin/sh

# Flattens a depth-two folder of submissions into a single folder.

mkdir 2-Flat
> PartIDs.txt

for prefile in 1-Unmarked/*/* ; do

    path=${prefile#*/}
    file=${path#*/}
    folder=${path%/*}
    partno=${folder//[^0-9]}

    echo "${partno}" >> PartIDs-temp.txt
    
    cp -r "$prefile" "2-Flat/${partno}-${file}"
    echo "Copied Participant ${partno} file ${file}"
    
done

sort -u PartIDs-temp.txt > PartIDs.txt
rm PartIDs-temp.txt

