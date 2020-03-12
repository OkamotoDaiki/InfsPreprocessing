#!/bin/sh

supervise_folders=(supervise_label_0 supervise_label_1)
cd ../move_supervise_data
pwd

mag_folders=()
#append folder
mag_folders=(`ls -d *`)

#write csv
for mag_folder in ${mag_folders[@]}
do
    cd ${mag_folder}
    pwd
    for supervise_folder in ${supervise_folders[@]}
    do
        {
        cd ${supervise_folder}
        pwd
        folders=()
        #get place name
        for folder in *
        do
        folders+=( ${folder} )
        done
        #label1 count
        for folder in ${folders[@]}
        do
        cd ${folder}
        echo ${folder}','`ls -1 | wc -l`
        # echo -e '\r\n'
        cd ../
        done
        } > count_${mag_folder}_${supervise_folder}.csv
        echo "write count csv data."
        cd ../
    done
    cd ../
done
