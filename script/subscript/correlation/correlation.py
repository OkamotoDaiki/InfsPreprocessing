import numpy as np
import sys
from ..debug_functions import DebugModeCorrelation

#limit rate against all data of correlation data because of few probably distribution
save_rate = 0.8
#class object
debug_mode = DebugModeCorrelation()

def CrossCorrelation(*args):
    """
    Cross Correlation function.
    """
    def CovarianceFunc(base_data, lag_data):
        base_mean = np.mean(base_data)
        lag_mean = np.mean(lag_data)
        cov_list = []
        
        for lag in range(len(lag_data)):
            terms = []
            for n in range(len(base_data[lag:])):
                term = (base_data[n] - base_mean) * (lag_data[n-lag] - lag_mean)
                terms.append(term)
            c_k = np.mean(terms)
            cov_list.append(c_k)

        cross_covariance = cov_list
        return cross_covariance
    
    
    def CrossCovariance(data):
        #init
        no_lag = 0
        cross_cov = []
        
        for i in range(len(data)):
            cross_cov_row = []
            for j in range(len(data)):
                cov = CovarianceFunc(data[i], data[j])
                cross_cov_row.append(cov)
            cross_cov.append(cross_cov_row)
        return cross_cov
    

    def CountColumn(matrix):
        """
        Count column of matrix.
        """
        return len(matrix)
    

    def CountRow(matrix):
        """
        Count row of matrix.
        """
        row_numbers = [len(row) for row in matrix]
        #debug
        debug_mode.DisplayCountRow(row_numbers, 0)
        #debug end
        #judge square matrix
        row_number = set(row_numbers)
        if len(set(row_numbers)) == 1:
            return list(row_number)[0]
        else:
            print("Error : This matrix is not square matrix.")
            sys.exit()
            return -1

    #init
    no_lag = 0
    cross_corr = []
    
    data = np.array(args)
    cross_cov = CrossCovariance(data)
    
    matrix_column = CountColumn(cross_cov)
    matrix_row = CountRow(cross_cov)
    for i in range(matrix_column):
        i_var = cross_cov[i][i][no_lag]
        cross_corr_row = []
        for j in range(matrix_row):
            j_var = cross_cov[j][j][no_lag]
            corr_coef = cross_cov[i][j] / (np.sqrt(i_var * j_var))
            cross_corr_row.append(corr_coef[:int(save_rate * len(corr_coef))])
        cross_corr.append(cross_corr_row)
    return cross_corr