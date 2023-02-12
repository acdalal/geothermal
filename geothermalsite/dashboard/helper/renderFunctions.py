from django.shortcuts import render
from ..forms import (
    TempVsTimeForm,
    TempVsDepthForm,
    StratigraphyForm,
)

from .constants import DATA_END_DATE, DATA_START_DATE
from .visualization import (
    toChartJsTempVsTime,
    toChartJsTempVsDepth,
    toChartJsStratigraphy,
)
from .api import getDataOutages
from django.http import HttpRequest


def truncateDateTime(dates: list):
    """
    A function that trims the data outages from the database into YYYY-MM-DD format.
    The timestamp is unneccesary for disabling day(s) in the daterangepicker (calendar).
    """
    truncatedDates = []
    for i in range(len(dates)):
        dateDict = dates[i]
        start = dateDict.get("start_time").date().__str__()
        end = dateDict.get("end_time").date().__str__()
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
    form: TempVsTimeForm or TempVsDepthForm,
    queryData: list,
    graphData: list,
    outageList: list,
) -> dict():
    return {
        "form": form,
        "queryData": queryData,
        "graphData": graphData,
        "dataStartDate": DATA_START_DATE,
        "dataEndDate": DATA_END_DATE,
        "outageList": outageList,
    }


def renderTempVsTimePage(request: HttpRequest, queryResults=None, borehole=None):
    """
    A shortcut function that renders tempvstime.html, generates the respective form, and displays query results if available
    """
    if queryResults and borehole:
        graphData = toChartJsTempVsTime(queryResults, borehole)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        TempVsTimeForm(), queryResults, graphData, truncatedOutageList
    )
    return render(
        request,
        "dashboard/tempvstime.html",
        context,
    )


def renderTempVsDepthPage(
    request: HttpRequest, queryResults: list = None, borehole=None
):
    """
    A shortcut function that renders tempvstime.html, generates the respective form, and displays query results if available
    """
    if queryResults and borehole:
        graphData = toChartJsTempVsDepth(queryResults, borehole)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        TempVsDepthForm(), queryResults, graphData, truncatedOutageList
    )

    return render(
        request,
        "dashboard/tempvsdepth.html",
        context,
    )


def renderStratigraphyPage(
    request: HttpRequest, groupBy: int = None, queryResults: list = None, borehole=None
):
    """
    A shortcut function that renders tempvstime.html, generates the respective form, and displays query results if available
    """
    if queryResults and borehole:
        graphData = toChartJsStratigraphy(queryResults, borehole, groupBy)
    else:
        graphData = list()

    outageList = getDataOutages()
    truncatedOutageList = truncateDateTime(outageList)
    context = _getPageContext(
        StratigraphyForm(), queryResults, graphData, truncatedOutageList
    )
    context["groupBy"] = groupBy
    return render(
        request,
        "dashboard/stratigraphy.html",
        context,
    )
