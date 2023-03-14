from datetime import datetime
from collections import defaultdict
from .constants import (
    GROUPS,
    HOURS,
    DAYS,
    WEEKS,
    MONTHS,
    YEARS,
    MONTH_SHORTHAND,
    METRIC,
)


def toChartJsTempVsTime(queryResults: list, units: str) -> list:
    """
    Takes the database query output from temperature vs time query and modifies it to fit the format for the flot library
    """
    graphData = list()
    for datapoint in queryResults:
        if units == METRIC:
            temperature = float(datapoint["temperature_c"])
        else:
            temperature = float(datapoint["temperature_f"])

        datetimeString = datapoint["datetime_utc"]
        graphData.append({"x": datetimeString, "y": temperature})

    return graphData


# def toChartJsTempVsDepth(queryResults: list, units: str) -> list:
#     """
#     Takes the database query output from temperature vs depth query and modifies it to fit the format for the flot library
#     """
#     graphData = list()

#     for datapoint in queryResults:
#         if units == METRIC:
#             temperature = float(datapoint["temperature_c"])
#             depth = float(datapoint["depth_m"])
#         else:
#             temperature = float(datapoint["temperature_f"])
#             depth = float(datapoint["depth_ft"])

#         graphData.append({"x": depth, "y": temperature})

#     return graphData


def toChartJsTempProfile(
    queryResults: list, groupBy: int, units: str
) -> dict[dict[list[dict]]]:
    assert groupBy in GROUPS
    results = defaultdict(lambda: defaultdict(list))

    for row in queryResults:
        date = datetime.strptime(row["datetime_utc"], "%Y-%m-%d %H:%M:%S")
        if units == METRIC:
            datapoint = {"x": row["temperature_c"], "y": row["depth_m"]}
        else:
            datapoint = {"x": row["temperature_f"], "y": row["depth_ft"]}

        if groupBy == HOURS:
            group = f"{date.hour}:00:00"
            results[group][str(date)].append(datapoint)
        else:
            if groupBy == DAYS:
                group = f"{MONTH_SHORTHAND[date.month-1]} {date.day}, {date.year}"
            if groupBy == WEEKS:
                group = f"Week {date.isocalendar()[1]}, {date.year}"
            if groupBy == MONTHS:
                group = f"{MONTH_SHORTHAND[date.month-1]}, {date.year}"
            if groupBy == YEARS:
                group = f"{date.year}"

            results[group][str(date.date())].append(datapoint)

    # convert the defaultdict to a regular dict so that it automatically converts to javascript dict
    for group in results.keys():
        results[group] = dict(results[group])
    results = dict(results)
    return results
