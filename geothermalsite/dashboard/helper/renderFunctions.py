from django.shortcuts import render
from ..forms import TempVsTimeForm, TempVsDepthForm, TemperatureProfileForm
from datetime import datetime

from .constants import DATA_END_DATE, DATA_START_DATE
from .visualization import (
    toChartJsTempVsTime,
    toChartJsTempVsDepth,
    toChartJsTempProfile,
)
from .api import getDataOutages
from django.http import HttpRequest


def truncateDateTime(dates: list[dict[str, datetime]]):
    """
    A function that trims the data outages from the database into YYYY-MM-DD format.
    The timestamp is unneccesary for disabling day(s) in the daterangepicker (calendar).
    """
    truncatedDates = []
    for date in dates:
        start = date.get("start_time").date().__str__()
        end = date.get("end_time").date().__str__()
        truncatedDates.append({"startDate": start, "endDate": end})
    return truncatedDates


def renderIndexPage(request: HttpRequest):
    """
    A shortcut function that renders index.html and generates the query selection form
    """
    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        queryData=None,
        graphData=None,
        outageList=truncatedOutageList,
        type=None,
        units=None,
    )
    return render(request, "dashboard/index.html", context=context)


def _getPageContext(
    queryData: list,
    graphData: list,
    outageList: list,
    type: str,
    units: str,
) -> dict():
    return {
        "temperatureProfileForm": TemperatureProfileForm(),
        "tempOverTimeForm": TempVsTimeForm(),
        "tempOverDepthForm": TempVsDepthForm(),
        "queryData": queryData,
        "graphData": graphData,
        "dataStartDate": DATA_START_DATE,
        "dataEndDate": DATA_END_DATE,
        "outageList": outageList,
        "type": type,
        "units": units,
    }


def renderTempVsTimePage(
    request: HttpRequest, units: int, queryResults=None, borehole=None
):
    """
    TODO
    """
    if queryResults and borehole:
        graphData = toChartJsTempVsTime(queryResults, units)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        queryData=queryResults,
        graphData=graphData,
        outageList=truncatedOutageList,
        type="tempvstime",
        units=units,
    )
    return render(
        request,
        "dashboard/index.html",
        context,
    )


def renderTempVsDepthPage(
    request: HttpRequest, units: int, queryResults: list = None, borehole=None
):
    """
    TODO
    """
    if queryResults and borehole:
        graphData = toChartJsTempVsDepth(queryResults, units)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        queryData=queryResults,
        graphData=graphData,
        outageList=truncatedOutageList,
        type="tempvsdepth",
        units=units,
    )

    return render(
        request,
        "dashboard/index.html",
        context,
    )


def renderTempProfilePage(
    request: HttpRequest,
    units: int,
    groupBy: int = None,
    queryResults: list = None,
    borehole=None,
):
    """
    TODO
    """
    if queryResults and borehole:
        graphData = toChartJsTempProfile(queryResults, groupBy, units)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        queryData=queryResults,
        graphData=graphData,
        outageList=truncatedOutageList,
        type="tempprofile",
        units=units,
    )
    context["groupBy"] = groupBy
    return render(
        request,
        "dashboard/index.html",
        context,
    )


def renderRawQueryPage(request: HttpRequest, context, form, queryResults: list = None):
    context.update({"queryResults": queryResults, "form": form})
    return render(request, "dashboard/customquery.html", context)
