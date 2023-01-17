from django.shortcuts import render
from ..forms import TempVsTimeForm, TempVsDepthForm, QuerySelectionForm

from .constants import DATA_END_DATE, DATA_START_DATE
from .visualization import convertToTempVsDepthGraphData, convertToTempVsTimeGraphData
from .api import getDataOutages


def truncateDateTime(dates):
    """
    TODO
    """
    truncatedDates = []
    for i in range(len(dates)):
        dateDict = dates[i]
        start = dateDict.get("start_time").date()
        end = dateDict.get("end_time").date()
        truncatedDates.append({"startDate": start, "endDate": end})
    return truncatedDates


def renderIndexPage(request):
    """
    A shortcut function that renders index.html and generates the query selection form
    """
    return render(
        request, "dashboard/index.html", context={"form": QuerySelectionForm()}
    )


def renderTempVsTimePage(request, queryResults=None, borehole=None):
    """
    A shortcut function that renders tempvstime.html, generates the respective form, and displays query results if available
    """
    if queryResults and borehole:
        graphData = convertToTempVsTimeGraphData(queryResults, borehole)
    else:
        graphData = None

    outageList = getDataOutages()
    truncated_outageList = truncateDateTime(outageList)
    # print(outageList)
    return render(
        request,
        "dashboard/tempvstime.html",
        context={
            "form": TempVsTimeForm(),
            "queryData": queryResults,
            "graphData": graphData,
            "dataStartDate": DATA_START_DATE,
            "dataEndDate": DATA_END_DATE,
            "outageList": truncated_outageList,
        },
    )


def renderTempVsDepthPage(request, queryResults=None, borehole=None):
    """
    A shortcut function that renders tempvstime.html, generates the respective form, and displays query results if available
    """
    if queryResults and borehole:
        graphData = convertToTempVsDepthGraphData(queryResults, borehole)
    else:
        graphData = None

    outageList = getDataOutages()
    truncated_outageList = truncateDateTime(outageList)
    # print(outageList)
    return render(
        request,
        "dashboard/tempvsdepth.html",
        context={
            "form": TempVsDepthForm(),
            "queryData": queryResults,
            "graphData": graphData,
            "dataStartDate": DATA_START_DATE,
            "dataEndDate": DATA_END_DATE,
            "outageList": truncated_outageList,
        },
    )
