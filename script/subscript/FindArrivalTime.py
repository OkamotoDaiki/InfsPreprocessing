import pandas as pd

def ArrivalTimeValues(obs_place, vol_place):
    """
    Extract arrival time specify observatory name and volcano name.
    """
    def ExtractArrivalTime(arrival_time_data):
        """
        Extract arrival time using cross tabulation data
        """
        df = pd.read_csv(arrival_time_data)
        obs_place_number = df.columns.tolist().index(obs_place)
        vol_place_number = df["place"].tolist().index(vol_place)
        arrival_time = df.iat[vol_place_number, obs_place_number]
        return arrival_time


    tropo_arrival_time_data = "../arrival_time_data/time_troposphere_list_cross.csv"
    strato_arrival_time_data = "../arrival_time_data/time_stratosphere_list_cross.csv"
    themo_arrival_time_data = "../arrival_time_data/time_themosphere_list_cross.csv"

    tropo_arrival_time = ExtractArrivalTime(tropo_arrival_time_data)
    strato_arrival_time = ExtractArrivalTime(strato_arrival_time_data)
    themo_arrival_time = ExtractArrivalTime(themo_arrival_time_data)

    return tropo_arrival_time, strato_arrival_time, themo_arrival_time

def main():
    fpath = "../Infs/Kirisimayama_Shinmoedake_20180310/infs_Kuroshiotyou_Kamikawaguti.csv"
    fname = fpath.split("/")[-1].split(".")[0]
    vol_place = "Sakurazima_Ontake"
    obs_place = fname.split("_")[1] + "_" + fname.split("_")[2]

    print(ArrivalTimeValues(obs_place, vol_place))

    return 0

if __name__ == "__main__":
    main()