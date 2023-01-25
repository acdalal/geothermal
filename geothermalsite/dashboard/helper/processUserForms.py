import dateparser
import re
from ..forms import (
    TempVsTimeForm,
    TempVsDepthForm,
    QuerySelectionForm,
    StratigraphyForm,
)
from django.http import HttpRequest


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

    download = cleanedData["download"]

    return {
        "boreholeNumber": boreholeNumber,
        "depth": depth,
        "startDateUtc": startDateUtc,
        "endDateUtc": endDateUtc,
        "download": download,
    }


def getTempVsDepthFormData(cleanedData: dict) -> dict:
    """
    Processes the temperature vs depth form data and outputs it in an easily accessible format
    """
    boreholeNumber = cleanedData["boreholeNumber"]

    timestamp = cleanedData["timestamp"]
    timestampUtc = dateparser.parse(timestamp).__str__()

    download = cleanedData["download"]

    return {
        "timestampUtc": timestampUtc,
        "boreholeNumber": boreholeNumber,
        "download": download,
    }


def getStratigraphyFormData(cleanedData: dict) -> dict:
    """
    Processes the stratigraphy form data and outputs it in an easily accessible format
    """
    boreholeNumber = cleanedData["boreholeNumber"]
    depth = cleanedData["depth"]

    dateRange = cleanedData["dateRange"]
    dateList = re.findall(r"../../....", dateRange)
    startDate, endDate = dateList

    startDateUtc = dateparser.parse(startDate).__str__()
    endDateUtc = dateparser.parse(endDate).__str__()

    download = cleanedData["download"]

    return {
        "boreholeNumber": boreholeNumber,
        "depth": depth,
        "startDateUtc": startDateUtc,
        "endDateUtc": endDateUtc,
        "download": download,
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
