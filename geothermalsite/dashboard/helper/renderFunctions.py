from django.shortcuts import render
from ..forms import (
    TempVsTimeForm,
    TempVsDepthForm,
    StratigraphyForm,
)
from datetime import datetime

from .constants import DATA_END_DATE, DATA_START_DATE
from .visualization import (
    toChartJsTempVsTime,
    toChartJsTempVsDepth,
    toChartJsStratigraphy,
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
    context = {
        "temperatureProfileForm": StratigraphyForm(),
        "tempOverTimeForm": TempVsTimeForm(),
        "tempOverDepthForm": TempVsDepthForm(),
        "dataStartDate": DATA_START_DATE,
        "dataEndDate": DATA_END_DATE,
        "outageList": truncatedOutageList,
    }
    return render(request, "dashboard/index.html", context=context)


def _getPageContext(
    queryData: list,
    graphData: list,
    outageList: list,
    type: str,
) -> dict():
    return {
        "queryData": queryData,
        "graphData": graphData,
        "dataStartDate": DATA_START_DATE,
        "dataEndDate": DATA_END_DATE,
        "outageList": outageList,
        "type": type,
    }


def renderTempVsTimePage(request: HttpRequest, queryResults=None, borehole=None):
    """
    TODO
    """
    if queryResults and borehole:
        graphData = toChartJsTempVsTime(queryResults, borehole)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        queryResults, graphData, truncatedOutageList, "tempvstime"
    )
    return render(
        request,
        "dashboard/index.html",
        context,
    )


def renderTempVsDepthPage(
    request: HttpRequest, queryResults: list = None, borehole=None
):
    """
    TODO
    """
    if queryResults and borehole:
        graphData = toChartJsTempVsDepth(queryResults, borehole)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        queryResults, graphData, truncatedOutageList, "tempvsdepth"
    )

    return render(
        request,
        "dashboard/index.html",
        context,
    )


def renderTempProfilePage(
    request: HttpRequest, groupBy: int = None, queryResults: list = None, borehole=None
):
    """
    TODO
    """
    if queryResults and borehole:
        graphData = toChartJsStratigraphy(queryResults, borehole, groupBy)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        queryResults, graphData, truncatedOutageList, "tempprofile"
    )
    context["groupBy"] = groupBy
    return render(
        request,
        "dashboard/index.html",
        context,
    )


def renderRawQueryPage(request: HttpRequest, queryResults: list = None):
    return render(request, "dashboard/customquery.html", {"queryResults": queryResults})
