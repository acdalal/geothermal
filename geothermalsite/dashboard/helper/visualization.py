from datetime import datetime
import time


def toChartJsTempVsTime(queryResults: list, borehole: int) -> list:
    """
    Takes the database query output from temperature vs time query and modifies it to fit the format for the flot library
    """
    graphData = list()
    for datapoint in queryResults:
        temperature = float(datapoint["temperature_c"])
        datetimeString = datapoint["datetime_utc"]
        graphData.append({"x": datetimeString, "y": temperature})

    return graphData


def toChartJsTempVsDepth(queryResults: list, borehole: int) -> list:
    """
    Takes the database query output from temperature vs depth query and modifies it to fit the format for the flot library
    """
    graphData = list()

    for datapoint in queryResults:
        temperature = float(datapoint["temperature_c"])
        depth = float(datapoint["depth_m"])
        graphData.append({"x": depth, "y": temperature})

    return graphData


def toChartJsStratigraphy(queryResults: list, borehole: int) -> list:
    pass
