import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import glob
import os
import sys
import shutil
import json
from subscript import OperateFpath

def highpass_filter(freq_seq, fft_data, dF, cutpoint):
    """
    Highpass Filter
    """
    fc = dF * cutpoint
    fft_highpass = copy.copy(fft_data)

    count = 0
    for freq in freq_seq:
        if freq - fc >=0:
            break
        count += 1
    fft_highpass[:count] = 0
    fft_highpass[len(fft_highpass) - count:] = 0
    return fft_highpass


def cut_or_padding(data, supervised_data_length=512):
    """
    Arange to rule of supervised data.
    If larger than supervied data length, cut. Else if smaller than supervised data length, zero padding.
    """
    def cut_data(delta_supervised, data):
        if delta_supervised % 2 == 0:
            start_delete = int(delta_supervised / 2)
            end_delete = int(delta_supervised / 2)
        elif delta_supervised % 2 != 0:
            start_delete = int(delta_supervised / 2) + 1
            end_delete = int(delta_supervised / 2)
        else:
            print("error : multiple of 2 programing error.")
        return data[start_delete: data_length - end_delete]
    
    
    def zero_padding(delta_supervised, data):
        delta_supervised = abs(delta_supervised)
        if delta_supervised % 2 == 0:
            zeros = np.zeros(int(delta_supervised / 2))
            data = np.concatenate([zeros, data, zeros])
        elif delta_supervised % 2 != 0:
            zeros_start = np.zeros(int(delta_supervised / 2) + 1)
            zeros_end = np.zeros(int(delta_supervised / 2))
            data = np.concatenate([zeros_start, data, zeros_end])
        else:
            print("error : multiple of 2 programing error.")
        return data
    
    
    data_length = len(data)
    delta_supervised = data_length - supervised_data_length
    if delta_supervised < 0:
        data = zero_padding(delta_supervised, data)
    elif delta_supervised > 0:
        data = cut_data(delta_supervised, data)
    elif delta_supervised == 0:
        data = data
    else:
        print("error : Conditional branch is error. Modify programming")
    return data


def find_cut_point(freq_seq, nq_fft_list):
    """
    Find Cutpoint for highpass-filter.
    """
    magnitude = 1
    count = 0
    threshold_list = []
    for i in range(len(nq_fft_list)):
        mean_fft_amp = np.mean(nq_fft_list)
        var_fft_amp = np.std(nq_fft_list)
        threshold = mean_fft_amp + magnitude * var_fft_amp
        analysis_freq = nq_fft_list[i]
        if analysis_freq >= threshold:
            nq_fft_list[i] = 0
            count += 1
        else:
            min_freq = freq_seq[i+1]
            min_array_number = count+1
            print("min frequency = {}".format(min_freq))
            break    
        threshold_list.append(threshold)
    return min_freq, min_array_number, threshold_list


def plot_series_graph(fpath, times, data):
    plt.clf()
    fname = fpath + ".png"
    plt.plot(times, data)
    plt.xlabel("time")
    plt.ylabel("pressure variation [mPa]")
    plt.savefig(fname)
    print("save : {}".format(fname))
    return 0


def main():
    # JSONファイルを読み込む
    with open('./script/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    fpath = config["input_fpath"]
    vol_place = config["vol_obs_place"]
    JMA_obs_place = config["JMA_obs_place"]
    folder_names = OperateFpath.get_multi_folder(fpath, vol_place, JMA_obs_place)

    for folder_name in folder_names:
        supervise_fpath = fpath + folder_name + "/cut_supervise_data/label_1/"
        csv_supervise_fpath = supervise_fpath + "*.csv"
        csv_files = glob.glob(csv_supervise_fpath)
        
        write_folder_name = fpath + folder_name + "/Preprocessing_supervise_data/"
        try:
            shutil.rmtree(write_folder_name)
            os.mkdir(write_folder_name)
        except FileNotFoundError:
            os.mkdir(write_folder_name) 

        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            s1_InfAC = df["InfAC"].tolist()
            s1_times = df["SensorTimeStamp"].tolist()

            N = len(s1_times)
            fs = config["fs"]
            cutpoint = config["cutpoint"]
            dF = fs / N
            freq_seq = np.arange(0, fs, dF)
            windowed_data1 = np.hamming(len(s1_InfAC)) * s1_InfAC
            fft1 = np.fft.fft(windowed_data1)
            nq_fft_list = abs(fft1)[:int(N / 2)]
            try:
                min_freq, min_array_number, threshold_list = find_cut_point(freq_seq, nq_fft_list)
                fft1_highpass = highpass_filter(freq_seq, fft1, dF, min_array_number)
                iFFT1_highpass = np.fft.ifft(fft1_highpass)

                supervise_data_name = csv_file.split("/")[-1].split(".")[0] + "." + csv_file.split("/")[-1].split(".")[-2]
                write_csv_name = "Preprocessing_" + supervise_data_name + ".csv"
                write_fpath = write_folder_name + write_csv_name
                header = ['SensorTimeStamp', 'InfAC_highpass']
                write_df = [[s1_times[i], np.real(iFFT1_highpass[i])] for i in range(len(iFFT1_highpass))] #miss?
                df1 = pd.DataFrame(write_df, columns=header)
                df1.to_csv(write_fpath)
                print("save : {}".format(write_fpath))
                png_fpath = write_folder_name + "Preprocessing_" + supervise_data_name
                plot_series_graph(png_fpath, s1_times, iFFT1_highpass)
            except UnboundLocalError:
                print("UnboundLocalError: Modify programming.")

    return 0

if __name__=="__main__":
    main()