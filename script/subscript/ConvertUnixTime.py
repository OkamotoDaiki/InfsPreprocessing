from datetime import datetime

def GetUnixTime(timestamp):
    """
    Transform timestamps yyyy-mm-dd hh:mm:ss format to unix time.
    """
    def DatetimeFormat(timestamp):
        """
        Transform datetime format.
        """
        date = timestamp.split(" ")[0]
        time = timestamp.split(" ")[1]

        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        day = int(date.split("-")[2])

        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        sec = int(time.split(":")[2])
        return datetime(year, month, day, hour, minute, sec)

    obs_time_unix = int(DatetimeFormat(timestamp).strftime('%s'))
    return obs_time_unix

def main():
    obs_time_JMA = "2018-03-10 01:54:00"
    print(GetUnixTime(obs_time_JMA))
    return 0

if __name__ == "__main__":
    main()