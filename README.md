Preprocessing infrasound data of volcanic eruption
====

Overview

Preprocess infrasound generateed from volcanic eruption data with python and shell-script.

##Description
Preprocess inf01 data csv file you insert infrasound data to./Infs/(eruption folder).
Threorder of processing is as follows.
1. cut_supervise_data_multi.py
cut raw data from eruption volcano 30min data, label 1 and label 0.

2. preprocessing_data.py
dynamic highpass-filter to cutting raw data.

3. correlation_mag_variable.py
correlation each sensor processing preprocessing wave data
supervise dataset is moved "move_supervise_data" folder, "supervise_data" folder is temp.

3.5. (option) bash count_supervise_csv_mag_variable.sh
count number of supervise data file.

After run all script, move prerpcessing infrasound data in "move_supervise_data" to directory extracting feature script.

##Requirement
numpy, matplotlib, pandas

##Usage
Run infs_preprocessing.sh only with bash command

>>>bash infs_preprocessing.sh

So, user need to be able to use shell script.

##LICENSE
MIT
