from datetime import datetime
import time


def convertToTempVsTimeGraphData(queryResults: list, borehole: int) -> list:
    """
    Takes the database query output from temperature vs time query and modifies it to fit the format for the flot library
    """
    graphData = list()

    for datapoint in queryResults:
        temperature = float(datapoint["temperature_c"])
        datetimeString = datapoint["datetime_utc"]
        dateTime = datetime.strptime(datetimeString, "%Y-%m-%d %H:%M:%S")
        jsTime = int(time.mktime(dateTime.timetuple()))
        graphData.append([jsTime, temperature])

    return [graphData]


def convertToTempVsDepthGraphData(queryResults: list, borehole: int) -> list:
    """
    Takes the database query output from temperature vs depth query and modifies it to fit the format for the flot library
    """
    graphData = list()

    for datapoint in queryResults:
        temperature = float(datapoint["temperature_c"])
        depth = int(datapoint["depth_m"])
        graphData.append([depth, temperature])

    return [graphData]
