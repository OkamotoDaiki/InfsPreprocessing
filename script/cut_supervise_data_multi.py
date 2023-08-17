import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import glob
import shutil
import json
from subscript import FindArrivalTime
from subscript import ConvertUnixTime
from subscript import OperateFpath

def arrival_times(timestamp, obs_place, vol_place):
    tropo_arrival_time, strato_arrival_time, themo_arrival_time = FindArrivalTime.ArrivalTimeValues(obs_place, vol_place)
    obs_time_Unix = int(ConvertUnixTime.GetUnixTime(timestamp))
    tropo_arrival_time = tropo_arrival_time + obs_time_Unix
    strato_arrival_time = strato_arrival_time + obs_time_Unix
    themo_arrival_time = themo_arrival_time + obs_time_Unix
    return [tropo_arrival_time, strato_arrival_time, themo_arrival_time]


def generate_time_series_graph_vline(fname, x, y, timestamp, obs_place, vol_place):
    """
    Generate time series graph adding arrival time vertical line.
    """

    fname_png = fname + ".png"
    plt.clf()
    plt.plot(x, y)
    plt.xlabel("time [s]")
    plt.ylabel("amp")
    plt.xlim(min(x), max(x))
    plt.ylim(min(y), max(y))
    
    #vline
    vline_list = arrival_times(timestamp, obs_place, vol_place)
    count = 0

    #error dash line
    error_time = 30
    tropo_error = vline_list[0] - error_time
    plt.vlines(tropo_error, min(y), max(y), colors='yellow', linestyles='dashed', linewidth=0.5)
    max_period_InThemo = 25
    themo_error = vline_list[2] + max_period_InThemo + error_time
    plt.vlines(themo_error, min(y), max(y), colors='red', linestyles='dashed', linewidth=0.5)

    for time in vline_list:
        #print(time)
        #if time - min(x) > 0 and max(x) - time > 0:
            #print("ok")
        #else:
            #print("No")

        if count == 0:
            colors = "yellow"
        elif count == 1:
            colors = "orange"
        elif count == 2:
            colors = "red"
        plt.vlines(time, min(y), max(y), colors=colors, linewidth=1)
        #plt.vlines(time, min(y), max(y), colors=colors, linewidth=0.5, alpha=1)
        count += 1
    plt.savefig(fname_png)
    print("save : {}".format(fname_png))
    return 0


def get_csv_data(fpath):
    df = pd.read_csv(fpath)
    times = df['SensorTimeStamp'].tolist()
    data = df['InfAC'].tolist()
    return times, data


def write_csv(fpath, times, data):
    fpath_csv = fpath + ".csv"
    in_dataframe = [[times[number], data[number]] for number in range(len(data))]
    header = ['SensorTimeStamp', 'InfAC']
    df_write = pd.DataFrame(in_dataframe, columns=header)
    df_write.to_csv(fpath_csv)
    print("save : {}".format(fpath_csv))
    return 0


def sample_number_supervise_data(tropo_time, themo_time, times, data_length):
    """
    Definition number of supervise sample data. 
    Output start array number, end array number.

    Rule: 1024 = 2*(other + 30) + (themo_time - tropo_time)
    この式は論文を参照.
    """
    error_time = 30 #分精度の誤差を反映. 単位は[s]
    tropo_error = tropo_time - error_time
    max_period_InThemo = 25 #熱圏での火山噴火波形の継続時間. 単位は[s]
    themo_error = themo_time + max_period_InThemo + error_time

    number1 = 0
    for time in times:
        if time - tropo_error >= 0:
            start_cut_number = number1
            break
        number1 += 1

    number2 = 0
    for time in times:
        if time - themo_error >= 0:
            end_cut_number = number2
            break
        number2 += 1
    
    #edit
    try:
        center_number = int((end_cut_number - start_cut_number) / 2) + start_cut_number
        one_side_length = int(data_length / 2)
        start_cut_number = center_number - one_side_length
        end_cut_number = center_number + one_side_length
        print("new supervise definition : {}".format(end_cut_number - start_cut_number))
        
        #error
        data_length = one_side_length * 2
        if end_cut_number - start_cut_number != data_length:
            print("Error : Cutting data length is not 2 power.")
            sys.exit()
        
        if start_cut_number < 0 or end_cut_number > len(times):
            print("start cut number : {}".format(start_cut_number))
            print("end cut number : {}".format(end_cut_number))
            print("Error : short of data length. Give more data length.")
            start_cut_number = 0
            end_cut_number = 0

    except UnboundLocalError:
        print("Error! Need to investigate programming.")
        start_cut_number = 0
        end_cut_number = 0

    return start_cut_number, end_cut_number


def generate_time_series_graph(fpath, times, data):
    fpath_png = fpath + ".png"
    plt.clf()
    plt.xlabel("times")
    plt.ylabel("pressure variation [mPa]")
    plt.plot(times, data)
    plt.savefig(fpath_png)
    print("save : {}".format(fpath_png))
    return 0


def cut_label_zero(times, data, start_cut_number, end_cut_number, save_fpath, file_name, data_length=1024):
    """
    Cut label 0 and generate csv and png file.
    Overview:
        based on forward eruption time. but unable to generate, back eruption time.
    """
    def generate_files(fpath_supervise_zero, times, data):
        """
        Generate csv and png file.
        """
        write_csv(fpath_supervise_zero, times, data)
        generate_time_series_graph(fpath_supervise_zero, times, data)
        return 0

    
    if start_cut_number - data_length < 0:
        print("Error! Unable to make forward supervise data not eruption.")
        if end_cut_number + data_length > len(data):
            print("Error! this data is unable to make supervise data 0.")
        else:
            """
            able to make supervise data back.
            """
            fname_supervise_zero = "supervise_label_0_back_" + file_name
            label_zero_start_cut_number = end_cut_number
            label_zero_end_cut_number = end_cut_number + data_length
            #edit now
            #print("back start = {}".format(label_zero_start_cut_number))
            #print(label_zero_end_cut_number - label_zero_start_cut_number)
            #print("back end = {}".format(label_zero_end_cut_number))
            #sys.exit()
            #edit end
    else:
        """
        able to make supervise data forward.
        """
        fname_supervise_zero = "supervise_label_0_forward_" + file_name
        label_zero_start_cut_number = start_cut_number - data_length
        label_zero_end_cut_number = start_cut_number
        print(label_zero_end_cut_number - label_zero_start_cut_number)
    
    folder_supervise_zero = save_fpath + "label_0/"
    fpath_supervise_zero = folder_supervise_zero + fname_supervise_zero
    try:
        os.mkdir(folder_supervise_zero)
        generate_files(fpath_supervise_zero, times[label_zero_start_cut_number:label_zero_end_cut_number], data[label_zero_start_cut_number:label_zero_end_cut_number])
    except FileExistsError:
        generate_files(fpath_supervise_zero, times[label_zero_start_cut_number:label_zero_end_cut_number], data[label_zero_start_cut_number:label_zero_end_cut_number])
    return 0


def cut_label_one(times, data, start_cut_number, end_cut_number, save_fpath, file_name, obs_time_JMA, obs_place, vol_place):
    """
    Cut label 1 and generate csv and png file.
    Overview:
        generate supervise label 1 data with eruption arrival time
    """

    def generate_files(save_fname, times, data, obs_time_JMA, obs_place, vol_place):
        """
        Generate csv and png file.
        """
        generate_time_series_graph_vline(save_fname, times, data, obs_time_JMA, obs_place, vol_place)
        write_csv(save_fname, times, data)
        return 0

    folder_supervise_one = save_fpath + "label_1/"

    fname_supervise_one = "supervise_" + file_name
    save_fname = folder_supervise_one + fname_supervise_one

    if len(times[start_cut_number:end_cut_number]) == 0 or len(data[start_cut_number:end_cut_number]) == 0:
        print("error: times[supervise cut] and data[supervise cut] is no data.")
    else:
        try:
            os.mkdir(folder_supervise_one)
            generate_files(save_fname, times[start_cut_number:end_cut_number], data[start_cut_number:end_cut_number], obs_time_JMA, obs_place, vol_place)
        except FileExistsError:
            generate_files(save_fname, times[start_cut_number:end_cut_number], data[start_cut_number:end_cut_number], obs_time_JMA, obs_place, vol_place)
    return 0


def cut_label_data(fpath, folder_name, save_fpath, obs_time_JMA, vol_place, config):
    """
    Cut label data.
    Get csv fpath and generate label 0 and 1.
    """
    infs_number = config["infs_number"] #なぞの数字。たぶんインフラサウンドcsvデータ名から取っている。
    lack_rate_number = config["lack_rate_number"] #なぞの数字。たぶんインフラサウンドcsvデータ名から決まっている。
    data_length = config["data_length"] #データ長

    csv_fpath = fpath + "/" + folder_name + "/interpolation_data/*.csv"

    csv_files = glob.glob(csv_fpath)
    for csv_file in csv_files:
        file_name = csv_file.split("/")[-1].split(".")[0] + "." + csv_file.split("/")[-1].split(".")[-2]
        obs_place = OperateFpath.get_obs_place_name(csv_file, infs_number, lack_rate_number)

        #data
        times, data = get_csv_data(csv_file)

        #対流圏から熱圏のインフラサウンド到着予測時間の取得
        ArrivalTime_list = arrival_times(obs_time_JMA, obs_place, vol_place) #tropo, strato, themoの三種類
        start_cut_number, end_cut_number = sample_number_supervise_data(ArrivalTime_list[0], ArrivalTime_list[2], times, data_length) #カットの最初と最後を取得

        #supervise data, label 0
        print("label 0")
        cut_label_zero(times, data, start_cut_number, end_cut_number, save_fpath, file_name, data_length)

        #supervise data, label 1
        print("label 1")
        cut_label_one(times, data, start_cut_number, end_cut_number, save_fpath, file_name, obs_time_JMA, obs_place, vol_place)
    return 0


def main():
    # JSONファイルを読み込む
    with open('./script/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    fpath = config["input_fpath"] #インプットフォルダ
    vol_place = config["vol_place"] #火山名
    JMA_obs_place = config["JMA_obs_place"] #気象庁の観測場所
    folder_names = OperateFpath.get_multi_folder(fpath, vol_place, JMA_obs_place)

    for folder_name in folder_names:
        obs_time_JMA, csv_fpath, graph_fpath = OperateFpath.single_get_save_path_and_time(fpath, folder_name)
        save_fpath = fpath + "/" + folder_name + "/cut_supervise_data/"
        try:
            shutil.rmtree(save_fpath)
            try:
                os.mkdir(save_fpath)
                try:
                    cut_label_data(fpath, folder_name, save_fpath, obs_time_JMA, vol_place, config)
                except UnboundLocalError:
                    print("Error! Need to investigate programming.")

            except FileExistsError:
                try:
                    cut_label_data(fpath, folder_name, save_fpath, obs_time_JMA, vol_place, config)
                except UnboundLocalError:
                    print("Error! Need to investigate programming.")

        except FileNotFoundError:
            try:
                os.mkdir(save_fpath)
                try:
                    cut_label_data(fpath, folder_name, save_fpath, obs_time_JMA, vol_place, config)
                except UnboundLocalError:
                    print("Error! Need to investigate programming.")

            except FileExistsError:
                try:
                    cut_label_data(fpath, folder_name, save_fpath, obs_time_JMA, vol_place, config)
                except UnboundLocalError:
                    print("Error! Need to investigate programming.")
    return 0

if __name__=="__main__":
    main()