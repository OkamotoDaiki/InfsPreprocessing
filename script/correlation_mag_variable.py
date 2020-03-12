import numpy as np
import shutil
import os
import sys
import subprocess
from subscript import test_threshold_magnitude_correlation as threshold_correlation
from subscript import OperateFpath

def GetEruptionDataFolders():
    fpath = "../Infs"
    vol_place = "Sakurazima_Ontake"
    JMA_obs_place = "Higashikorimoto"

    eruption_data_folders = OperateFpath.GetMultiFolder(fpath, vol_place, JMA_obs_place)
    return eruption_data_folders


def main():
    #folders
    eruption_data_folders = GetEruptionDataFolders()
    mag_variable_list = np.arange(0, 15.5, 0.5)

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