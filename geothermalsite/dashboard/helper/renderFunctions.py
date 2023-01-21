from django.shortcuts import render
from ..forms import TempVsTimeForm, TempVsDepthForm, QuerySelectionForm

from .constants import DATA_END_DATE, DATA_START_DATE
from .visualization import toChartJsTempVsTime, toChartJsTempVsDepth
from .api import getDataOutages


def truncateDateTime(dates):
    """
    A function that trims the data outages from the database into YYYY-MM-DD format.
    The timestamp is unneccesary for disabling day(s) in the daterangepicker (calendar).
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
        graphData = toChartJsTempVsTime(queryResults, borehole)
    else:
        graphData = dict()

    outageList = getDataOutages()
    truncated_outageList = truncateDateTime(outageList)
    print(graphData)

    return render(
        request,
        "dashboard/tempvstime.html",
        context={
            "form": TempVsTimeForm(),
            "queryData": queryResults,
            "xData": graphData.get("x"),
            "yData": graphData.get("y"),
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
        graphData = toChartJsTempVsDepth(queryResults, borehole)
    else:
        graphData = dict()

    outageList = getDataOutages()
    print("1", graphData)
    truncated_outageList = truncateDateTime(outageList)
    return render(
        request,
        "dashboard/tempvsdepth.html",
        context={
            "form": TempVsDepthForm(),
            "queryData": queryResults,
            "xData": graphData.get("x"),
            "yData": graphData.get("y"),
            "dataStartDate": DATA_START_DATE,
            "dataEndDate": DATA_END_DATE,
            "outageList": truncated_outageList,
        },
    )
