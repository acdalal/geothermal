import csv

from django.shortcuts import render
from django.http import HttpRequest

from .helper.api import (
    getTempVsDepthResults,
    getTempVsTimeResults,
    getStratigraphyResults,
    getDataOutages,
    getRawQueryResults,
)
from .helper.processUserForms import (
    getUserTempVsTimeQuery,
    getUserTempVsDepthQuery,
    getUserStratigraphyQuery,
    getGrouping,
    getUserRawQuery,
)
from .helper.renderFunctions import (
    renderIndexPage,
    renderTempVsDepthPage,
    renderTempVsTimePage,
    renderStratigraphyPage,
    renderRawQueryPage,
)

from .forms import RawQueryForm

def index(request: HttpRequest):
    if request.method == "POST":
        if "temperature-profile" in request.POST:
            formData = getUserStratigraphyQuery(request)
            groupBy = getGrouping(formData["startDateUtc"], formData["endDateUtc"])
            borehole = int(borehole)
            queryResults = getStratigraphyResults(
                borehole,
                formData["startDateUtc"],
                formData["endDateUtc"],
                formData["dailyTimestamp"],
                groupBy,
            )
            return renderStratigraphyPage(request, groupBy, queryResults, borehole)

        elif "temperature-time" in request.POST:
            formData = getUserTempVsTimeQuery(request)
            borehole = int(borehole)
            queryResults = getTempVsTimeResults(
                borehole,
                formData["depth"],
                formData["startDateUtc"],
                formData["endDateUtc"],
            )
            return renderTempVsTimePage(request, groupBy, queryResults, borehole)

        if "temperature-depth" in request.POST:
            formData = getUserTempVsDepthQuery(request)
            groupBy = getGrouping(formData["startDateUtc"], formData["endDateUtc"])
            borehole = int(borehole)
            queryResults = getTempVsDepthResults(
                borehole,
                formData["timestampUtc"],
            )
            return renderStratigraphyPage(request, groupBy, queryResults, borehole)
    else:
        return renderIndexPage(request)


def about(request: HttpRequest):
    return render(request, "dashboard/about.html", context=None)


def documentation(request: HttpRequest):
    outageData = getDataOutages()
    outageDict = {"outage": outageData}
    return render(request, "dashboard/documentation.html", context=outageDict)


def tempVsTime(request: HttpRequest):
    if request.method == "POST":
        formData = getUserTempVsTimeQuery(request)
        queryResults = getTempVsTimeResults(
            borehole,
            formData["depth"],
            formData["startDateUtc"],
            formData["endDateUtc"],
        )

        borehole = int(borehole)
        return renderTempVsTimePage(request, queryResults, borehole)

    else:
        return renderTempVsTimePage(request)


def tempVsDepth(request: HttpRequest):
    if request.method == "POST":
        formData = getUserTempVsDepthQuery(request)
        queryResults = getTempVsDepthResults(borehole, formData["timestampUtc"])
        borehole = int(borehole)
        return renderTempVsDepthPage(request, queryResults, borehole)

    else:
        return renderTempVsDepthPage(request)


def stratigraphy(request: HttpRequest):
    if request.method == "POST":
        formData = getUserStratigraphyQuery(request)
        groupBy = getGrouping(formData["startDateUtc"], formData["endDateUtc"])

        queryResults = getStratigraphyResults(
            borehole,
            formData["startDateUtc"],
            formData["endDateUtc"],
            formData["dailyTimestamp"],
            groupBy,
        )
        borehole = int(borehole)
        return renderStratigraphyPage(request, groupBy, queryResults, borehole)

    else:
        return renderStratigraphyPage(request)


def customQuery(request: HttpRequest):
    form = RawQueryForm(request.POST or None)
    previousQuery = ''

    if request.method == "POST":
        formData = getUserRawQuery(request)
        queryResults = getRawQueryResults(formData)
        print("THIS IS THE QUERY RESULTS", queryResults)
        context = {
            "queryResults": [
                {key: value for key, value in zip(queryResults[0].keys(), row)}
                for row in queryResults
            ],
            "form": form,
            "rawQuery":formData['rawQuery']

        }

        print("THIS IS THE DATA:", context)
        return renderRawQueryPage(request, context, formData, queryResults=queryResults)
    else:
        previousQuery = request.GET.get('query', '')
        form = RawQueryForm(initial={'rawQuery': previousQuery})
        
        context = {'form': form}
        return renderRawQueryPage(request, context, form)
