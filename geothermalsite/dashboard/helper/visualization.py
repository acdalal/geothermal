from datetime import datetime
from collections import defaultdict
from .constants import GROUPS, DAYS, WEEKS, MONTHS, YEARS


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


def toChartJsStratigraphy(
    queryResults: list, borehole: int, groupBy: int
) -> dict[list[dict]]:
    assert groupBy in GROUPS
    results = defaultdict(list)
    for row in queryResults:
        date = datetime.strptime(queryResults["datetime_utc"], "%Y-%m-%d %H:%M:%S")
        if groupBy == DAYS:
            group = f"{date.month}/{date.day}/{date.year}"
        if groupBy == WEEKS:
            group = f"Week {date.isocalendar()[1]}"
        if groupBy == MONTHS:
            group = f"{date.month}/xx/{date.year}"
        if groupBy == YEARS:
            group = f"{date.year}"

        datapoint = {"x": row["temperature_c"], "y": row["depth_m"]}

        results[group].append(datapoint)

    return results
