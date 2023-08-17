import numpy as np
import shutil
import os
import sys
import subprocess
import json
from subscript import threshold_magnitude_correlation as threshold_correlation
from subscript import OperateFpath

def get_eruption_data_folders(config):
    fpath = config["input_fpath"]
    vol_place = config["vol_place"]
    JMA_obs_place = config["JMA_obs_place"]

    eruption_data_folders = OperateFpath.GetMultiFolder(fpath, vol_place, JMA_obs_place)
    return eruption_data_folders


def main():
    # JSONファイルを読み込む
    with open('./script/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    #folders
    min_mag = config["min_mag"]
    max_mag = config["max_mag"]
    mag_interval = config["mag_interval"]
    eruption_data_folders = get_eruption_data_folders(config)
    mag_variable_list = np.arange(min_mag, max_mag, mag_interval)

    generate_fpath = "../"
    supervise_data_file = "supervise_data"
    supervise_move_data_file = "move_supervise_data"

    try:
        shutil.rmtree(generate_fpath + supervise_data_file)
    except FileNotFoundError:
        print("test")
    try:
        shutil.rmtree(generate_fpath + supervise_move_data_file)
    except FileNotFoundError:
        print("test")

    generate_origin_fpath = generate_fpath + supervise_data_file + "/"
    os.mkdir(generate_origin_fpath)
    generate_move_folder_fpath = generate_fpath + supervise_move_data_file + "/"
    os.mkdir(generate_move_folder_fpath)
    for mag in mag_variable_list:
        mag_file_fpath = generate_origin_fpath + str(int(10 * mag)) + "div10mag"
        os.mkdir(mag_file_fpath)
        for eruption_data_folder in eruption_data_folders:
            threshold_correlation.CorrelationMain(mag, eruption_data_folder)
        print("copy supervise folder...")
        cmd = "bash copy_supervise_data_mag_variable.sh"
        subprocess.run(cmd, shell=True)
    return 0


if __name__=="__main__":
    main()