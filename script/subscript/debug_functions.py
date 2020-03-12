class DebugModeCorrelation:
    """
    threshold_magnitude_correlation.py debug mode class. The functions is standard output etc...
    standard output : judge 0 -> no 1 -> yes
    """
    def ReadCSVfile(self, count, csv_fpath, judge):
        if judge == 1:
            print("{} : {}".format(count, csv_fpath))
        else:
            pass
        return 0


    def MatchObsPlaceAndNumber(self, obsplace_dic, judge):
        """
        Dislay match of observation place and number.
        """
        if judge == 1:
            print("---match of observation place and number---")
            for i in obsplace_dic.items():
                print(i)
        else:
            pass
        return 0
    

    def DisplayCountRow(self, row_numbers, judge):
        """
        Display row numbers of matrix.
        """
        if judge == 1:
            print("---Row numbers of matrix---")
            print(row_numbers)
        else:
            pass
        return 0
    

    def DisplayStatMatrix(self, stat_data_matrix, judge):
        """
        Display elements of matrix of basic statistics. 
        """
        if judge == 1:
            print("---matrix of statistics[mean, SD] cross-correlation---")
            for row in stat_data_matrix:
                print(row)
        else:
            pass
        return 0
    

    def DisplayThresholdMatrix(self, threshold_matrix, judge):
        """
        Display threhold matrix.
        """
        if judge == 1:
            print("---threshold matrix---")
            for row in threshold_matrix:
                print(row)
        else:
            pass
        return 0


    def DisplayOverThresholdLengthMatrix(self, over_threshold_length_matrix, judge):
        """
        Display data length of over threshold matrix.
        """
        if judge == 1:
            print("---data length of over threshold matrix---")
            for row in over_threshold_length_matrix:
                print(row)
        else:
            pass
        return 0


    def DisplayOverThresholdMatrix(self, zeroorone_matrix, one_list, judge):
        """
        Display data length matrix.
        """
        if judge == 1:
            print("---Over threshold matrix---")
            count = 0
            for row in zeroorone_matrix:
                count += 1
                if count == 1:
                    print(*[i for i in range(1,len(row)+1)])
                print("{: >3}, {}".format(count,row))
            print("combination of over threshold of cross-correlation length = {}".format(len(one_list)))
        else:
            pass
        return 0


    def DisplayDeleteNotOneList(self, delete_not_one_list, judge):
        """
        Display combination deleteing not one list.
        """
        if judge == 1:
            print("---combination deleteing auto-correlation---")
            print(delete_not_one_list)
        else:
            pass
        return 0


    def DisplayCombPlaces(self, comb_places_list, judge):
        """
        Display combination deleteing not one list.
        """
        if judge == 1:
            print("---combination places list---")
            print(comb_places_list)
        else:
            pass
        return 0


    def DisplayCopyDirectory(self, copy_supervise_csvfpath, judge):
        """
        Display combination deleteing not one list.
        """
        if judge == 1:
            print("copy : {}".format(copy_supervise_csvfpath))
        else:
            pass
        return 0

    
    def DisplayPlotGraph(self, png_fname, judge):
        """
        Display combination deleteing not one list.
        """
        if judge == 1:
            print("save : {}".format(png_fname))
        else:
            pass
        return 0