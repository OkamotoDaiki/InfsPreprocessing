#!/bin/sh

cd ./script
echo Run cut_supervise_data_multi.py
python cut_supervise_data_multi.py
echo -e \\nRun preprocessing_data.py
python preprocessing_data.py
echo -e \\nRun correlation_mag_variable.py
python correlation_mag_variable.py
echo -e \\nRun count_supervise_csv_mag_variable.sh
bash count_supervise_csv_mag_variable.sh