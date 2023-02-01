from datetime import datetime
import dateparser
from collections import defaultdict
from .constants import GROUPS, HOURS, DAYS, WEEKS, MONTHS, YEARS


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
) -> dict[dict[list[dict]]]:
    assert groupBy in GROUPS
    results = defaultdict(lambda: defaultdict(list))

    for row in queryResults:
        date = datetime.strptime(row["datetime_utc"], "%Y-%m-%d %H:%M:%S")

        # The query results have multiple measurements per day, and each line on the graph is one measurement
        # if groupBy in [DAYS, HOURS]:
        datapoint = {"x": row["temperature_c"], "y": row["depth_m"]}

        if groupBy == HOURS:
            group = f"{date.month}/{date.day}/{date.year}:{date.hour}"
            results[group][str(date)].append(datapoint)
        else:
            if groupBy == DAYS:
                group = f"{date.month}/{date.day}/{date.year}"
            if groupBy == WEEKS:
                group = f"Week {date.isocalendar()[1]}"
            if groupBy == MONTHS:
                group = f"{date.month}/xx/{date.year}"
            if groupBy == YEARS:
                group = f"{date.year}"

            results[group][str(date.date())].append(datapoint)
    # convert the defaultdict to a regular dict so that it automatically converts to javascript dict
    for group in results.keys():
        results[group] = dict(results[group])
    results = dict(results)
    return results
