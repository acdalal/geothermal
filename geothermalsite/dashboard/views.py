import csv

from django.shortcuts import render
from django.http import HttpRequest

from .helper.api import (
    getTempVsDepthResults,
    getTempVsTimeResults,
    getStratigraphyResults,
)
from .helper.processUserForms import (
    getUserTempsVsTimeQuery,
    getUserTempVsDepthQuery,
    getUserQueryType,
    getUserStratigraphyQuery,
)
from .helper.renderFunctions import (
    renderIndexPage,
    renderTempVsDepthPage,
    renderTempVsTimePage,
)


def index(request: HttpRequest):
    if request.method == "POST":
        queryType = getUserQueryType(request)

        if queryType == "tempvstime":
            return renderTempVsTimePage(request)
        if queryType == "tempvsdepth":
            return renderTempVsDepthPage(request)
        else:
            raise (
                'User selected query type is invalid, should be "tempvstime" or "tempvsdepth"'
            )

    else:
        return renderIndexPage(request)


def about(request: HttpRequest):
    return render(request, "dashboard/about.html", context=None)


def documentation(request: HttpRequest):
    return render(request, "dashboard/documentation.html", context=None)


def tempVsTime(request: HttpRequest):
    if request.method == "POST":
        formData = getUserTempsVsTimeQuery(request)
        queryResults = getTempVsTimeResults(
            formData["boreholeNumber"],
            formData["depth"],
            formData["startDateUtc"],
            formData["endDateUtc"],
        )

        borehole = int(formData["boreholeNumber"])
        return renderTempVsTimePage(request, queryResults, borehole)

    else:
        return renderTempVsTimePage(request)


def tempVsDepth(request: HttpRequest):
    if request.method == "POST":
        formData = getUserTempVsDepthQuery(request)
        queryResults = getTempVsDepthResults(
            formData["boreholeNumber"], formData["timestampUtc"]
        )
        borehole = int(formData["boreholeNumber"])
        return renderTempVsDepthPage(request, queryResults, borehole)

    else:
        return renderTempVsDepthPage(request)


def stratigraphy(request: HttpRequest):
    if request.method == "POST":
        formData = getUserStratigraphyQuery(request)
        # start, end =
        queryResults = getStratigraphyResults(
            formData["boreholeNumber"],
            formData["startDateUtc"],
            formData["endDateUtc"],
        )
        borehole = int(formData["boreholeNumber"])
        return renderTempVsDepthPage(request, queryResults, borehole)

    else:
        return renderTempVsDepthPage(request)
