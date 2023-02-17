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
    renderRawQueryError,
)

from .forms import RawQueryForm


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
                formData["units"],
            )
            return renderTempProfilePage(
                request, formData["units"], groupBy, queryResults, int(borehole)
            )

        elif "temperature-time" in request.POST:
            formData = getUserTempVsTimeQuery(request)
            borehole = formData["boreholeNumber"]
            queryResults = getTempVsTimeResults(
                borehole,
                formData["depth"],
                formData["startDateUtc"],
                formData["endDateUtc"],
                formData["units"],
            )
            return renderTempVsTimePage(
                request, formData["units"], queryResults, int(borehole)
            )

        if "temperature-depth" in request.POST:
            formData = getUserTempVsDepthQuery(request)
            borehole = formData["boreholeNumber"]
            queryResults = getTempVsDepthResults(
                borehole, formData["timestampUtc"], formData["units"]
            )
            return renderTempVsDepthPage(
                request, formData["units"], queryResults, int(borehole)
            )
    else:
        return renderIndexPage(request)


def about(request: HttpRequest):
    return render(request, "dashboard/about.html", context=None)


def documentation(request: HttpRequest):
    outageData = getDataOutages()
    outageDict = {"outage": outageData}
    return render(request, "dashboard/documentation.html", context=outageDict)


def customQuery(request: HttpRequest):
    form = RawQueryForm(request.POST or None)
    previousQuery = ""

    if request.method == "POST":
        formData = getUserRawQuery(request)
        if formData != TypeError:
            queryResults = getRawQueryResults(formData)
            if queryResults != SyntaxError:
                context = {
                    "queryResults": [
                        {key: value for key, value in zip(queryResults[0].keys(), row)}
                        for row in queryResults
                    ],
                    "form": form,
                    "rawQuery": formData["rawQuery"],
                }

                return renderRawQueryPage(
                    request, context, formData, queryResults=queryResults
                )
            else:
                context = {"errorMessage": "Error connecting to the database"}
                return renderRawQueryError(request, context)
        else:
            context = {"errorMessage": "ERROR: Please enter a query before submitting"}
            return renderRawQueryError(request, context)
    else:
        previousQuery = request.GET.get("query", "")
        form = RawQueryForm(initial={"rawQuery": previousQuery})

        context = {"form": form}
        return renderRawQueryPage(request, context, form)
