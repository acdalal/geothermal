import time
import dateparser
import re
import csv


def getQuerySelectionData(cleanedData: dict) -> dict:
    """
    Gets the type of database query the user wants to perform
    """
    queryType = cleanedData["queryType"]
    return {"queryType": queryType}


def getTempVsTimeFormData(cleanedData: dict) -> dict:
    """
    Processes the temperature vs time form data and outputs it in an easily accessible format
    """
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


def getTempVsDepthFormData(cleanedData: dict) -> dict:
    """
    Processes the temperature vs depth form data and outputs it in an easily accessible format
    """
    boreholeNumber = cleanedData["boreholeNumber"]

    timestamp = cleanedData["timestamp"]
    timestampUtc = dateparser.parse(timestamp).__str__()

    return {"timestampUtc": timestampUtc, "boreholeNumber": boreholeNumber}
