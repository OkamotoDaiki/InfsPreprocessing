import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from . import name_format
from ..debug_functions import DebugModeCorrelation
#class object
debug_mode = DebugModeCorrelation()


def PlotCorrelationGraph(time_lag, cross_corr_series, threshold, fpath, comb_obsplace, eruption_datetime, magnification):
    """
    Plot 3 graphs.
    1: cross-correlation against time lag wittern threshold.
    2: scatter graph of cross-correlation against time lag wittern threshold.
    3. histgram correlation values wittern threshold.
    """
    plt.clf()
    plt.subplots_adjust(wspace=0.8)
    #timelag plot
    plt.subplot(131)
    plt.ylim(-1,1)
    plt.xlabel("time lag [s]")
    plt.hlines(threshold, min(time_lag), max(time_lag), color='r', linestyle='dashed')
    plt.plot(time_lag, cross_corr_series)
    #scatter
    plt.subplot(132)
    plt.ylim(-1,1)
    plt.xlabel("time lag [s]")
    plt.hlines(threshold, min(time_lag), max(time_lag), color='r', linestyle='dashed')
    plt.scatter(time_lag, cross_corr_series, marker='.')
    #hist
    plt.subplot(133)
    plt.ylabel("Frequency")
    #plt.yscale('log')
    hist_array = plt.hist(cross_corr_series)[0]
    plt.xlim(-1, 1)
    plt.ylim(0, max(hist_array))
    plt.vlines(threshold, 0, max(hist_array), color='r', linestyle='dashed')
    #save
    str_magnification = name_format.TransformMagnification(magnification)
    png_fname = fpath + eruption_datetime + "_threshold_" + str_magnification + "_" + str(comb_obsplace) +"_correlation.png"
    plt.savefig(png_fname, dpi=150)
    debug_mode.DisplayPlotGraph(png_fname, 0)
    return 0