import dateparser
from datetime import datetime, timedelta
import re
from ..forms import (
    TempVsTimeForm,
    TempVsDepthForm,
    TemperatureProfileForm,
    RawQueryForm,
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
    boreholeNumber = cleanedData.get("boreholeNumber")
    depth = cleanedData.get("tempVsTimeDepth")

    dateRange = cleanedData.get("tempVsTimeDateRange")
    dateList = re.findall(r"../../....", dateRange)
    startDate, endDate = dateList

    startDateUtc = dateparser.parse(startDate)
    endDateUtc = dateparser.parse(endDate).replace(hour=23, minute=59, second=59)

    units = int(cleanedData.get("tempVsTimeUnits"))

    return {
        "boreholeNumber": boreholeNumber,
        "depth": depth,
        "startDateUtc": startDateUtc,
        "endDateUtc": endDateUtc,
        "units": units,
    }


def getTempVsDepthFormData(cleanedData: dict) -> dict:
    """
    Processes the temperature vs depth form data and outputs it in an easily accessible format
    """
    boreholeNumber = cleanedData.get("boreholeNumber")

    timestamp = cleanedData.get("tempVsDepthTimestamp")
    timestampUtc = dateparser.parse(timestamp).__str__()

    units = int(cleanedData.get("tempVsDepthUnits"))

    return {
        "timestampUtc": timestampUtc,
        "boreholeNumber": boreholeNumber,
        "units": units,
    }


def getTempProfileFormData(cleanedData: dict) -> dict:
    """
    Processes the temperature profile form data and outputs it in an easily accessible format
    """
    boreholeNumber = cleanedData["boreholeNumber"]

    dateRange = cleanedData["temperatureProfileDateRange"]
    dateList = re.findall(r"../../....", dateRange)
    startDate, endDate = dateList

    dailyTimestampString = cleanedData.get("temperatureProfileTimeSelector")

    startDateUtc: datetime = dateparser.parse(startDate).replace(
        hour=0, minute=0, second=0
    )
    endDateUtc = dateparser.parse(endDate).replace(hour=23, minute=59, second=59)
    dailyTimestamp: datetime = dateparser.parse(dailyTimestampString)

    units = int(cleanedData.get("tempProfileUnits"))

    return {
        "boreholeNumber": boreholeNumber,
        "startDateUtc": startDateUtc,
        "endDateUtc": endDateUtc,
        "dailyTimestamp": dailyTimestamp,
        "units": units,
    }


def getUserTempVsTimeQuery(request: HttpRequest) -> dict:
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


def getUserTempProfileQuery(request: HttpRequest) -> dict:
    """
    From the temperature profile graph form, extracts the user response and formats it into a dictionary
    """
    userForm = TemperatureProfileForm(request.POST)
    assert userForm.is_valid()
    formData = getTempProfileFormData(userForm.cleaned_data)
    return formData


def getGrouping(start: datetime, end: datetime) -> int:
    range: timedelta = end - start
    if range <= timedelta(days=1):
        return HOURS
    if range <= timedelta(days=15):
        return DAYS
    if range <= timedelta(weeks=15):
        return WEEKS
    if range <= timedelta(days=450):
        return MONTHS
    else:
        return YEARS


def getUserRawQuery(request: HttpRequest) -> str:

    userForm = RawQueryForm(request.POST)
    assert userForm.is_valid()

    formData = userForm.cleaned_data
    return formData
