import numpy as np
import pandas as pd
import sys
import glob
import os
import shutil
#myself module
from . import OperateFpath
from .debug_functions import DebugModeCorrelation
from .correlation import correlation
from .subsubscript import extract_element_array
from .subsubscript import plot_graph
#class object
debug_mode = DebugModeCorrelation()
operate_fpath = OperateFpath.CorrelationOperateFpath()


class CombPlaceOverThreshold:
    """
    Get combination of places over threshold using cross-correlation of basic statstics.
    """
    def __init__(self, cross_corr, magnification):
        self.cross_corr = cross_corr
        self.magnification = magnification


    def StatMatrix(self):
        """
        Calculate basic statistics of cross-correlation target sensor data against other sensor data.
        """
        stat_data_matrix = []
        column_number = np.array(self.cross_corr).shape[0]
        row_number = np.array(self.cross_corr).shape[1]
        for i in range(column_number):
            row = []
            for j in range(row_number):
                mean = np.mean(self.cross_corr[i][j])
                std = np.sqrt(np.var(self.cross_corr[i][j]))
                row.append([mean, std])
            stat_data_matrix.append(row)

        debug_mode.DisplayStatMatrix(stat_data_matrix, 0)
        return stat_data_matrix


    def ThresholdMatrix(self, stat_matrix):
        """
        Generate threshold matrix with statistics of cross-correlation matrix.
        """
        mean_k = 0
        std_k = 1
        
        threshold_matrix = []
        column_number = np.array(stat_matrix).shape[0]
        row_number = np.array(stat_matrix).shape[1]
        for i in range(column_number):
            row = []
            for j in range(row_number):
                mean = stat_matrix[i][j][mean_k]
                std = stat_matrix[i][j][std_k]
                threshold = mean + self.magnification * std
                if threshold > 1:
                    threshold = 1
                row.append(threshold)
            threshold_matrix.append(row)

        debug_mode.DisplayThresholdMatrix(threshold_matrix, 0)
        return threshold_matrix


    def ThresholdMoreDataMatrix(self, threshold_matrix, judge_number):
        """
        Generate matrix of being able to judging over threshold.
        """
        def NotZerotoOne(data):
            """
            Transform data to 0 or 1.
            If data is not 0, return 1. Else, return 0.
            """
            if data != 0:
                return 1
            else:
                return 0
            
        MoreData_matrix = []
        over_threshold_length_matrix = []
        zeroorone_matrix = []
        comb_places = []
        
        column_number = np.array(threshold_matrix).shape[0]
        row_number = np.array(threshold_matrix).shape[1]
        for i in range(column_number):
            row = []
            row_data_length = []
            row_zeroorone = []
            for j in range(row_number):
                moredata_list = []
                threshold = threshold_matrix[i][j]
                crosscorr_list = self.cross_corr[i][j]
                moredata_list = [crosscorr for crosscorr in crosscorr_list if crosscorr >= threshold]
                data_len = len(moredata_list)
                zeroorone = NotZerotoOne(data_len)
                if zeroorone == 1:
                    comb_places.append((i,j))
                else:
                    pass
                row.append(moredata_list)
                row_data_length.append(data_len)
                row_zeroorone.append(zeroorone)
            MoreData_matrix.append(row)
            over_threshold_length_matrix.append(row_data_length)
            zeroorone_matrix.append(row_zeroorone)

        debug_mode.DisplayOverThresholdLengthMatrix(over_threshold_length_matrix, 0)
        debug_mode.DisplayOverThresholdMatrix(zeroorone_matrix, comb_places, judge_number)
        return comb_places


    def DeleteSingleAutocorrelation(self, comb_places_number):
        """
        Delete auto-correlation only in row vector of matrix.
        """
        target_number_list = [comb[0] for comb in comb_places_number]
        target_unique_number_list = list(set(target_number_list))
        
        deleted_comb_places_number = []
        for target_number in target_unique_number_list:
            number_group = [comb for comb in comb_places_number if comb[0] == target_number]
            if len(number_group) == 1:
                for comb in number_group:
                    if comb[0] != comb[1]:
                        deleted_comb_places_number.append(number_group)
            else:
                for comb in number_group:
                    deleted_comb_places_number.append(comb)

        debug_mode.DisplayDeleteNotOneList(deleted_comb_places_number, 0)
        return deleted_comb_places_number


    def GenerateCombObsPlace(self, delete_places_number, obs_place_dic):
        """
        Get combination place name over threshold.
        """
        comb_obsplace_list = []
        for element in delete_places_number:
            comb_obsplace = extract_element_array.TransformNumberToPlace(obs_place_dic, element[0], element[1])
            comb_obsplace_list.append(comb_obsplace)
        return comb_obsplace_list

    
    def GetCombPlaceOverThreshold(self, obs_place_dic, judge_number=0):
        """
        All process in CombPlaceOverThreshold class
        judge_number : standard output yes->1 or no->0
        """
        stat_matrix = self.StatMatrix()
        threshold_matrix = self.ThresholdMatrix(stat_matrix)
        comb_places_number = self.ThresholdMoreDataMatrix(threshold_matrix, judge_number=judge_number)
        delete_places_number = self.DeleteSingleAutocorrelation(comb_places_number)
        comb_places_list = self.GenerateCombObsPlace(delete_places_number, obs_place_dic)
        return comb_places_list


    def GetDeletePlaceNumber(self):
        """
        Process StatMatrix -> DeleteSingleAutocorrelation
        """
        stat_matrix = self.StatMatrix()
        threshold_matrix = self.ThresholdMatrix(stat_matrix)
        comb_places_number = self.ThresholdMoreDataMatrix(threshold_matrix, judge_number=0)
        delete_places_number = self.DeleteSingleAutocorrelation(comb_places_number)
        return delete_places_number

    
    def GetCombPlacesNumber(self):
        """
        Process StatMatrix -> ThresholdMoreDataMatrix
        """
        stat_matrix = self.StatMatrix()
        threshold_matrix = self.ThresholdMatrix(stat_matrix)
        comb_places_number = self.ThresholdMoreDataMatrix(threshold_matrix, judge_number=0)     
        return comb_places_number   


class GenerateFilesCorrelation:
    """
    Generating png files and moving over threshold correlation place files.
    """
    def __init__(self, cross_corr, magnification, obsplace_dic):
        self.cross_corr = cross_corr
        self.magnification = magnification
        self.obsplace_dic = obsplace_dic


    def CopySuperviseData(self, target_supervise_fpath, supervise_csvfpath_list):
        """
        Copy supervise dataset to supervise directory.
        """
        for supervise_csvfpath in supervise_csvfpath_list:
            copy_supervise_csvfpath = target_supervise_fpath + supervise_csvfpath.split('/')[-1]
            shutil.copyfile(supervise_csvfpath, copy_supervise_csvfpath)
            debug_mode.DisplayCopyDirectory(copy_supervise_csvfpath, 0)
        return 0


    def GetPlotSpecifiedCrossCorr(self, stat_data, obs_number, target_number_list, fpath, eruption_datetime, fs=2):
        """
        Get plot cross-correlation only specified.
        """
        matrix_number = np.array(self.cross_corr).shape
        column_number = matrix_number[0]
        row_number = matrix_number[1]
        partner_number_list = [coor[1] for coor in target_number_list]
        for i in range(column_number):
            if i == obs_number:
                for j in range(row_number):
                    threshold = stat_data[i][j][0] + self.magnification * stat_data[i][j][1]
                    cross_corr_series = self.cross_corr[i][j]
                    comb_obsplace = extract_element_array.TransformNumberToPlace(self.obsplace_dic, i, j)
                    time_lag = np.arange(0, len(cross_corr_series) / fs, 1 / fs)
                    if j in partner_number_list:
                        plot_graph.PlotCorrelationGraph(time_lag, cross_corr_series, threshold, fpath, comb_obsplace, eruption_datetime, self.magnification)
                    else:
                        less_threshold_fpath = fpath + "Less_threshold" + "/"
                        try:
                            os.mkdir(less_threshold_fpath)
                            plot_graph.PlotCorrelationGraph(time_lag, cross_corr_series, threshold, fpath, comb_obsplace, eruption_datetime, self.magnification)
                        except FileExistsError:
                            plot_graph.PlotCorrelationGraph(time_lag, cross_corr_series, threshold, fpath, comb_obsplace, eruption_datetime, self.magnification)
            else:
                pass
        return 0


    def ProcessGeneratingFiles(self, supervise_fpath, fpath, raw_supervise_csv_fpath, eruption_datetime):
        """
        Generate corr_supervise_data directory. Process generating supervise .csv and .png in corr_supervise_data.
        """
        #class object
        comb_place_over_threshold = CombPlaceOverThreshold(self.cross_corr, self.magnification)

        comb_places_list = comb_place_over_threshold.GetCombPlaceOverThreshold(self.obsplace_dic, judge_number=0)
        stat_matrix = comb_place_over_threshold.StatMatrix()
        comb_places_number = comb_place_over_threshold.GetCombPlacesNumber()

        os.mkdir(supervise_fpath)
        print("make folder : {}".format(supervise_fpath))
        label_folder_list = ["label_1", "label_0"]
        for label_folder_name in label_folder_list:
            print("Processing {}".format(label_folder_name))
            supervise_label_fpath = supervise_fpath + "/" + label_folder_name
            os.mkdir(supervise_label_fpath)

            for specified_obsplace in list(self.obsplace_dic.keys()):
                specified_list = []
                
                #target number
                obs_number = extract_element_array.GetTargetNumber(specified_obsplace, self.obsplace_dic)
                target_number_list = extract_element_array.GetTargetNumberList(obs_number, comb_places_number)
                
                for comb_place in comb_places_list:
                    if comb_place[0] == specified_obsplace:
                        specified_list.append(comb_place)
                    else:
                        pass

                #output csvfile name for "raw" supervise data.
                raw_supervise_csv_label_folder_fpath = raw_supervise_csv_fpath + label_folder_name
                raw_csv_fpaths = glob.glob(raw_supervise_csv_label_folder_fpath + "/*.csv")
                supervise_csvfpath_list = []
                for raw_csv_fpath in raw_csv_fpaths:
                    for comb in specified_list:
                        target_place_name = comb[1]
                        if target_place_name in raw_csv_fpath:
                            supervise_csvfpath_list.append(raw_csv_fpath)
                        else:
                            pass
                #make folder of sensor place name.
                target_supervise_fpath = supervise_label_fpath + "/" + specified_obsplace + "/"
                os.mkdir(target_supervise_fpath)
                if label_folder_name == "label_1":
                    self.CopySuperviseData(target_supervise_fpath, supervise_csvfpath_list)
                    self.GetPlotSpecifiedCrossCorr(stat_matrix, obs_number, target_number_list, target_supervise_fpath, eruption_datetime, fs=2)
                elif label_folder_name == "label_0":
                    self.CopySuperviseData(target_supervise_fpath, supervise_csvfpath_list)
                else:
                    print("Error: Modify programming.")
        return 0
    

def GetPreprocessedDataAndObsplace(csv_fpaths):
    """
    Get preprocessed data and observation place from csv_fpath.
    """
    times_list = []
    data_list = []
    obs_place_list = []

    count = 0
    obsplace_dic = {}
    for csv_fpath in csv_fpaths:
        debug_mode.ReadCSVfile(count, csv_fpath, 0)
        
        obs_place = operate_fpath.GetObsPlace(csv_fpath)
        obsplace_dic[obs_place] = count
        obs_place_list.append(obs_place)
        
        df = pd.read_csv(csv_fpath)
        times = df["SensorTimeStamp"].tolist()
        InfAC = df["InfAC_highpass"].tolist()
        times_list.append(times)
        data_list.append(InfAC)
        count += 1
    return times_list, data_list, obs_place_list, obsplace_dic


def CorrelationMain(magnification, eruption_data_folder):
    """
    Main function of correlation.
    It is possible to edit output directory and file name.
    Caution! Behind time lag of correlation funciton is few number of probably distribution. 
            So limit rate against all data of correlation data. Edit .correaltion.correlation -> "save_rate" global variable
    """
    fpath = "../Infs"

    #get script
    fpath_preprocessing = fpath + "/" + eruption_data_folder + "/Preprocessing_supervise_data/"
    eruption_datetime = eruption_data_folder.split("_")[-3] + "_" + eruption_data_folder.split("_")[-2]
    csv_fpath = fpath_preprocessing + "*.csv"
    csv_fpaths = glob.glob(csv_fpath)

    times_list, data_list, obs_place_list, obsplace_dic = GetPreprocessedDataAndObsplace(csv_fpaths)
    debug_mode.MatchObsPlaceAndNumber(obsplace_dic, 0)
    #correlation
    print("calucurate correlation function...")
    cross_corr = correlation.CrossCorrelation(*data_list)
    comb_place_over_threshold = CombPlaceOverThreshold(cross_corr, magnification)
    comb_places_list = comb_place_over_threshold.GetCombPlaceOverThreshold(obsplace_dic, judge_number=1)
    debug_mode.DisplayCombPlaces(comb_places_list, 1)
    
    supervise_folder_name = "corr_supervise_data"
    supervise_fpath = fpath + "/" + eruption_data_folder + "/" + supervise_folder_name
    print("\ncorr_supervise_data folder \n{}".format(supervise_fpath))
    raw_supervise_csv_fpath = fpath + "/" + eruption_data_folder + "/" + "cut_supervise_data/"          
    generating_files = GenerateFilesCorrelation(cross_corr, magnification, obsplace_dic)

    print("Copy supervise dataset to supervise directory...")
    print("Generate ploting correlation function and histgram of correlation values...")
    try:
        try:
            shutil.rmtree(supervise_fpath)
            generating_files.ProcessGeneratingFiles(supervise_fpath, fpath, raw_supervise_csv_fpath, eruption_datetime)
        except FileNotFoundError:
            generating_files.ProcessGeneratingFiles(supervise_fpath, fpath, raw_supervise_csv_fpath, eruption_datetime)
    except ValueError:
        print("ValueError : Modify programming.")
    return 0

if __name__=="__main__":
    pass