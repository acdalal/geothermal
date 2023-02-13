import csv

from django.shortcuts import render
from django.http import HttpRequest

from .helper.api import (
    getTempVsDepthResults,
    getTempVsTimeResults,
    getTempProfileResults,
    getDataOutages,
    getRawQueryResults,
)
from .helper.processUserForms import (
    getUserTempVsTimeQuery,
    getUserTempVsDepthQuery,
    getGrouping,
    getUserRawQuery,
    getUserTempProfileQuery,
)
from .helper.renderFunctions import (
    renderIndexPage,
    renderTempVsDepthPage,
    renderTempVsTimePage,
    renderTempProfilePage,
    renderRawQueryPage,
)


def index(request: HttpRequest):
    if request.method == "POST":
        if "temperature-profile" in request.POST:
            formData = getUserTempProfileQuery(request)
            groupBy = getGrouping(formData["startDateUtc"], formData["endDateUtc"])
            borehole = formData["boreholeNumber"]
            queryResults = getTempProfileResults(
                borehole,
                formData["startDateUtc"],
                formData["endDateUtc"],
                formData["dailyTimestamp"],
                groupBy,
            )
            return renderTempProfilePage(request, groupBy, queryResults, int(borehole))

        elif "temperature-time" in request.POST:
            formData = getUserTempVsTimeQuery(request)
            borehole = formData["boreholeNumber"]
            queryResults = getTempVsTimeResults(
                borehole,
                formData["depth"],
                formData["startDateUtc"],
                formData["endDateUtc"],
            )
            return renderTempVsTimePage(request, queryResults, int(borehole))

        if "temperature-depth" in request.POST:
            formData = getUserTempVsDepthQuery(request)
            borehole = formData["boreholeNumber"]
            queryResults = getTempVsDepthResults(
                borehole,
                formData["timestampUtc"],
            )
            return renderTempVsDepthPage(request, queryResults, int(borehole))
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


def tempProfile(request: HttpRequest):
    if request.method == "POST":
        formData = getUserTempProfileQuery(request)
        groupBy = getGrouping(formData["startDateUtc"], formData["endDateUtc"])

        queryResults = getTempProfileResults(
            borehole,
            formData["startDateUtc"],
            formData["endDateUtc"],
            formData["dailyTimestamp"],
            groupBy,
        )
        borehole = int(borehole)
        return renderTempProfilePage(request, groupBy, queryResults, borehole)

    else:
        return renderTempProfilePage(request)


def customQuery(request: HttpRequest):
    if request.method == "POST":
        formData = getUserRawQuery(request)
        queryResults = getRawQueryResults(formData)
        print("THIS IS THE QUERY RESULTS", queryResults)
        context = {
            "queryResults": [
                {key: value for key, value in zip(queryResults[0].keys(), row)}
                for row in queryResults
            ]
        }
        print("THIS IS THE DATA:", context)
        return renderRawQueryPage(request, context)
    else:
        return renderRawQueryPage(request)
