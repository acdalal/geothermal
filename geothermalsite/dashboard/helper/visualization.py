from datetime import datetime
import time


def toChartJsTempVsTime(queryResults: list, borehole: int) -> dict:
    """
    Takes the database query output from temperature vs time query and modifies it to fit the format for the flot library
    """
    temperatures, labels = list(), list()
    for datapoint in queryResults:
        temperature = float(datapoint["temperature_c"])
        datetimeString = datapoint["datetime_utc"]
        temperatures.append(temperature)
        labels.append(datetimeString)

    return {"x": temperatures, "y": labels}


def toChartJsTempVsDepth(queryResults: list, borehole: int) -> dict:
    """
    Takes the database query output from temperature vs depth query and modifies it to fit the format for the flot library
    """
    temperatures, labels = list(), list()

    for datapoint in queryResults:
        temperature = float(datapoint["temperature_c"])
        depth = int(datapoint["depth_m"])
        labels.append(depth)
        temperatures.append(temperature)

    return {"x": temperatures, "y": labels}
