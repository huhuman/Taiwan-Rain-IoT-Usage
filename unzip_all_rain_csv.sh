#!/bin/bash
root="$1"
save_path="$root/../Rain_Unzip"
rm -rf $save_path
mkdir $save_path
for unzip_folder in $root/*/
do
    target=`basename $unzip_folder/`
    for zip_file in $unzip_folder/*.zip
        do
        unzip $zip_file -d $save_path
        done
done
