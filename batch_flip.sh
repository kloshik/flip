#!/bin/bash

if [ "$#" -ne 2 ] ; then
    echo "Usage:"
    echo "$0 'input_folder' output_folder'"
    exit
fi



input_folder="$1"
output_folder="$2"



if [ ! -d "$output_folder" ]; then
    mkdir -p "$output_folder"
fi

for file in "$1/"*; do

    filename=`basename "$file"`
    file_type=`file $file | cut -d " " -f 2`

    if [ "$file_type" == "JPEG" ] || [ "$file_type" == "PNG" ] || [ "$file_type" == "BMP" ]; then
        echo "Processing $filename"
    else
        continue
    fi


    ./flip_bmp.py "$file" "$output_folder/$filename"

done