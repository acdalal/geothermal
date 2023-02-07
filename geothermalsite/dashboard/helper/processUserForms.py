import dateparser
from datetime import datetime, timedelta
import re
from ..forms import (
    TempVsTimeForm,
    TempVsDepthForm,
    QuerySelectionForm,
    StratigraphyForm,
)
from django.http import HttpRequest
from .constants import HOURS, DAYS, WEEKS, MONTHS, YEARS


def getQuerySelectionData(cleanedData: dict) -> dict[str:str]:
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

    startDateUtc = dateparser.parse(startDate)
    endDateUtc = dateparser.parse(endDate).replace(hour=23, minute=59, second=59)

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

    return {
        "timestampUtc": timestampUtc,
        "boreholeNumber": boreholeNumber,
    }


def getStratigraphyFormData(cleanedData: dict) -> dict:
    """
    Processes the stratigraphy form data and outputs it in an easily accessible format
    """
    boreholeNumber = cleanedData["boreholeNumber"]

    dateRange = cleanedData["dateRange"]
    dateList = re.findall(r"../../....", dateRange)
    startDate, endDate = dateList

    dailyTimestampString = cleanedData["timeSelector"]

    startDateUtc: datetime = dateparser.parse(startDate).replace(
        hour=0, minute=0, second=0
    )
    endDateUtc = dateparser.parse(endDate).replace(hour=23, minute=59, second=59)
    dailyTimestamp: datetime = dateparser.parse(dailyTimestampString)

    return {
        "boreholeNumber": boreholeNumber,
        "startDateUtc": startDateUtc,
        "endDateUtc": endDateUtc,
        "dailyTimestamp": dailyTimestamp,
    }


def getUserTempsVsTimeQuery(request: HttpRequest) -> dict:
    """
    From the temperature vs time form, extracts the user response and formats it into a dictionary
    """
    userForm = TempVsTimeForm(request.POST)
    assert userForm.is_valid()
    formData = getTempVsTimeFormData(userForm.cleaned_data)

    return formData


def getUserTempVsDepthQuery(request: HttpRequest) -> dict:
    """
    From the temperature vs depth form, extracts the user response and formats it into a dictionary
    """
    userForm = TempVsDepthForm(request.POST)
    assert userForm.is_valid()
    formData = getTempVsDepthFormData(userForm.cleaned_data)
    return formData


def getUserStratigraphyQuery(request: HttpRequest) -> dict:
    """
    From the stratigraphy graph form, extracts the user response and formats it into a dictionary
    """
    userForm = StratigraphyForm(request.POST)
    assert userForm.is_valid()
    formData = getStratigraphyFormData(userForm.cleaned_data)
    return formData


def getUserQueryType(request: HttpRequest) -> str:
    """
    From the front-page query selection form, extracts the user response
    """
    userForm = QuerySelectionForm(request.POST)
    assert userForm.is_valid()

    formData = getQuerySelectionData(userForm.cleaned_data)
    queryType = formData["queryType"]
    return queryType


def getGrouping(start: datetime, end: datetime) -> int:
    range: timedelta = end - start
    if range <= timedelta(days=1):
        return HOURS
    if range <= timedelta(days=15):
        return DAYS
    if range <= timedelta(weeks=10):
        return WEEKS
    if range <= timedelta(days=450):
        return MONTHS
    else:
        return YEARS
