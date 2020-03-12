import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import glob
import shutil
from subscript import FindArrivalTime
from subscript import ConvertUnixTime
from subscript import OperateFpath

def ArrivalTimes(timestamp, obs_place, vol_place):
    tropo_arrival_time, strato_arrival_time, themo_arrival_time = FindArrivalTime.ArrivalTimeValues(obs_place, vol_place)
    obs_time_Unix = int(ConvertUnixTime.GetUnixTime(timestamp))
    tropo_arrival_time = tropo_arrival_time + obs_time_Unix
    strato_arrival_time = strato_arrival_time + obs_time_Unix
    themo_arrival_time = themo_arrival_time + obs_time_Unix
    return [tropo_arrival_time, strato_arrival_time, themo_arrival_time]


def GenerateTimeSeriesGraph_vline(fname, x, y, timestamp, obs_place, vol_place):
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
    vline_list = ArrivalTimes(timestamp, obs_place, vol_place)
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


def GetCsvData(fpath):
    df = pd.read_csv(fpath)
    times = df['SensorTimeStamp'].tolist()
    data = df['InfAC'].tolist()
    return times, data


def WriteCSV(fpath, times, data):
    fpath_csv = fpath + ".csv"
    in_dataframe = [[times[number], data[number]] for number in range(len(data))]
    header = ['SensorTimeStamp', 'InfAC']
    df_write = pd.DataFrame(in_dataframe, columns=header)
    df_write.to_csv(fpath_csv)
    print("save : {}".format(fpath_csv))
    return 0


def SampleNumber_SuperviseData(tropo_time, themo_time, times):
    """
    Definition number of supervise sample data. 
    Output start array number, end array number.

    Rule: 1024 = 2*(other + 30) + (themo_time - tropo_time)
    """
    error_time = 30
    tropo_error = tropo_time - error_time
    max_period_InThemo = 25
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
        one_side_length = 512
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

def GenerateTimeSeriesGraph(fpath, times, data):
    fpath_png = fpath + ".png"
    plt.clf()
    plt.xlabel("times")
    plt.ylabel("pressure variation [mPa]")
    plt.plot(times, data)
    plt.savefig(fpath_png)
    print("save : {}".format(fpath_png))
    return 0


def CutlabelZero(times, data, start_cut_number, end_cut_number, save_fpath, file_name, data_length=1024):
    """
    Cut label 0 and generate csv and png file.
    Overview:
        based on forward eruption time. but unable to generate, back eruption time.
    """
    def GenerateFiles(fpath_supervise_zero, times, data):
        """
        Generate csv and png file.
        """
        WriteCSV(fpath_supervise_zero, times, data)
        GenerateTimeSeriesGraph(fpath_supervise_zero, times, data)
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
        GenerateFiles(fpath_supervise_zero, times[label_zero_start_cut_number:label_zero_end_cut_number], data[label_zero_start_cut_number:label_zero_end_cut_number])
    except FileExistsError:
        GenerateFiles(fpath_supervise_zero, times[label_zero_start_cut_number:label_zero_end_cut_number], data[label_zero_start_cut_number:label_zero_end_cut_number])
    return 0


def CutlabelOne(times, data, start_cut_number, end_cut_number, save_fpath, file_name, obs_time_JMA, obs_place, vol_place):
    """
    Cut label 1 and generate csv and png file.
    Overview:
        generate supervise label 1 data with eruption arrival time
    """

    def GenerateFiles(save_fname, times, data, obs_time_JMA, obs_place, vol_place):
        """
        Generate csv and png file.
        """
        GenerateTimeSeriesGraph_vline(save_fname, times, data, obs_time_JMA, obs_place, vol_place)
        WriteCSV(save_fname, times, data)
        return 0

    folder_supervise_one = save_fpath + "label_1/"

    fname_supervise_one = "supervise_" + file_name
    save_fname = folder_supervise_one + fname_supervise_one

    if len(times[start_cut_number:end_cut_number]) == 0 or len(data[start_cut_number:end_cut_number]) == 0:
        print("error: times[supervise cut] and data[supervise cut] is no data.")
    else:
        try:
            os.mkdir(folder_supervise_one)
            GenerateFiles(save_fname, times[start_cut_number:end_cut_number], data[start_cut_number:end_cut_number], obs_time_JMA, obs_place, vol_place)
        except FileExistsError:
            GenerateFiles(save_fname, times[start_cut_number:end_cut_number], data[start_cut_number:end_cut_number], obs_time_JMA, obs_place, vol_place)
    return 0


def CutLabelData(fpath, folder_name, save_fpath, obs_time_JMA, vol_place):
    """
    Cut label data.
    Get csv fpath and generate label 0 and 1.
    """
    infs_number = 6
    lack_rate_number = -1

    csv_fpath = fpath + "/" + folder_name + "/interpolation_data/*.csv"

    csv_files = glob.glob(csv_fpath)
    for csv_file in csv_files:
        file_name = csv_file.split("/")[-1].split(".")[0] + "." + csv_file.split("/")[-1].split(".")[-2]
        obs_place = OperateFpath.GetObsPlaceName(csv_file, infs_number, lack_rate_number)

        #data
        times, data = GetCsvData(csv_file)

        ArrivalTime_list = ArrivalTimes(obs_time_JMA, obs_place, vol_place)
        start_cut_number, end_cut_number = SampleNumber_SuperviseData(ArrivalTime_list[0], ArrivalTime_list[2], times)

        #supervise data, label 0
        CutlabelZero(times, data, start_cut_number, end_cut_number, save_fpath, file_name, data_length=1024)

        #supervise data, label 1
        print("label 1")
        CutlabelOne(times, data, start_cut_number, end_cut_number, save_fpath, file_name, obs_time_JMA, obs_place, vol_place)
    return 0

def main():
    fpath = "../Infs"
    vol_place = "Sakurazima_Ontake"
    JMA_obs_place = "Higashikorimoto"
    folder_names = OperateFpath.GetMultiFolder(fpath, vol_place, JMA_obs_place)

    data_length = 1024

    for folder_name in folder_names:
        obs_time_JMA, csv_fpath, graph_fpath = OperateFpath.SingleGetSavePathandTime(fpath, folder_name)
        save_fpath = fpath + "/" + folder_name + "/cut_supervise_data/"
        try:
            shutil.rmtree(save_fpath)
            try:
                os.mkdir(save_fpath)
                try:
                    CutLabelData(fpath, folder_name, save_fpath, obs_time_JMA, vol_place)
                except UnboundLocalError:
                    print("Error! Need to investigate programming.")

            except FileExistsError:
                try:
                    CutLabelData(fpath, folder_name, save_fpath, obs_time_JMA, vol_place)
                except UnboundLocalError:
                    print("Error! Need to investigate programming.")

        except FileNotFoundError:
            try:
                os.mkdir(save_fpath)
                try:
                    CutLabelData(fpath, folder_name, save_fpath, obs_time_JMA, vol_place)
                except UnboundLocalError:
                    print("Error! Need to investigate programming.")

            except FileExistsError:
                try:
                    CutLabelData(fpath, folder_name, save_fpath, obs_time_JMA, vol_place)
                except UnboundLocalError:
                    print("Error! Need to investigate programming.")
    
    return 0

if __name__=="__main__":
    main()