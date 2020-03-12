#!/bin/sh

cd ../supervise_data/
mag_folder_list=(`ls -d *`)
for folder in ${mag_folder_list[@]}
do
  #make place folder
  place_names=(Akishi_Nishihama Touyoutyou_Ikumi Murotoshi_Murotomisakityou Kounanshi_Yasutyou_temusubi Kamishi_Tosayamadatyou_Miyanokuti Nangokushi_Monobe Koutishi_Harunotyou_Yoshihara Tosashi_Usatyou_Usa Kuroshiotyou_Kamikawaguti Kuroshiotyou_Ninagawa Kuroshiotyou_Ukibuti Kuroshiotyou_Deguti Kuroshiotyou_Umani Tosashimizushi_Ashizurimisaki1 Tosashimizushi_Ashizurimisaki2 Tosashimizushi_Ashizurimisaki3 Sukumoshi_Kodukushityou)
  rm -r ${folder}/supervise_label_1
  mkdir ${folder}/supervise_label_1
  cd ${folder}/supervise_label_1/
  for place_name in ${place_names[@]}
  do
  mkdir ${place_name}
  done

  cd ../../
  rm -r ${folder}/supervise_label_0
  mkdir ${folder}/supervise_label_0
  cd ${folder}/supervise_label_0/
  for place_name in ${place_names[@]}
  do
  mkdir ${place_name}
  done

  cd ../../../Infs/

  #append supervise folder
  file_names=()
  for file in *
  do
  if [ `echo ${file} | grep 'Sakurazima_Ontake_Higashikorimoto'` ]
  then
    file_names+=( ${file} )
  fi
  done

  #supervise label
  supervise_label_type=(label_0 label_1)

  for label in ${supervise_label_type[@]}
  do
    for file in ${file_names[@]}
    do
      ls -d */
      cd ${file}
      cd corr_supervise_data
      cd ${label}
      #get folder
      label_place_names=()
      for place_name in *
      do
        label_place_names+=( ${place_name} )
      done
      for place_name in ${label_place_names[@]}
      do
        cd ${place_name}
        ls *.csv
        #cp supervise_label_0_*${place_name}*.csv ../../../../../supervise_label_0/${place_name}
        cp *.csv ../../../../../supervise_data/${folder}/supervise_${label}/${place_name}
        cp *.png ../../../../../supervise_data/${folder}/supervise_${label}/${place_name}
        cd ../
      done
      cd ../../../
    done
  done
done

#move mag folder

cd ../supervise_data/
for folder in ${mag_folder_list[@]}
do
  mv ${folder} ../move_supervise_data
done