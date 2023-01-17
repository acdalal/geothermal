"""This file contains helper functions for dashboard/views.py"""

from datetime import datetime
import dateparser
import re
import time


def _getQuerySelectionData(cleanedData: dict) -> dict:
    queryType = cleanedData["queryType"]
    return {"queryType": queryType}


def _getTempVsTimeFormData(cleanedData: dict) -> dict:
    boreholeNumber = cleanedData["boreholeNumber"]
    depth = cleanedData["depth"]

    dateRange = cleanedData["dateRange"]
    dateList = re.findall(r"../../....", dateRange)
    startDate, endDate = dateList

    startDateUtc = dateparser.parse(startDate).__str__()
    endDateUtc = dateparser.parse(endDate).__str__()

    return {
        "boreholeNumber": boreholeNumber,
        "depth": depth,
        "startDateUtc": startDateUtc,
        "endDateUtc": endDateUtc,
    }


def _getTempVsDepthFormData(cleanedData: dict) -> dict:
    boreholeNumber = cleanedData["boreholeNumber"]

    timestamp = cleanedData["timestamp"]
    timestampUtc = dateparser.parse(timestamp).__str__()

    return {"timestampUtc": timestampUtc, "boreholeNumber": boreholeNumber}


def _convertToTempVsTimeGraphData(queryResults: list, borehole: int) -> list:
    graphData = list()

    for datapoint in queryResults:
        temperature = float(datapoint["temperature_c"])
        datetimeString = datapoint["datetime_utc"]
        dateTime = datetime.strptime(datetimeString, "%Y-%m-%d %H:%M:%S")
        jsTime = int(time.mktime(dateTime.timetuple()))
        graphData.append([jsTime, temperature])

    return [graphData]


def _convertToTempVsDepthData(queryResults: list, borehole: int) -> list:
    graphData = list()

    for datapoint in queryResults:
        temperature = float(datapoint["temperature_c"])
        depth = int(datapoint["depth_m"])
        graphData.append([depth, temperature])

    return [graphData]


def _truncateDateTime(dates):
    truncatedDates = []
    for i in range(len(dates)):
        dateDict = dates[i]
        start = dateDict.get("start_time").date()
        end = dateDict.get("end_time").date()
        truncatedDates.append({"startDate": start, "endDate": end})
    return truncatedDates
