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
    return render(request, "dashboard/pages/about.html", context=None)


def documentation(request: HttpRequest):
    outageData = getDataOutages()
    outageDict = {"outage": outageData}
    return render(request, "dashboard/pages/documentation.html", context=outageDict)


def customQuery(request: HttpRequest):
    form = RawQueryForm(request.POST or None)
    context = {"form": form, "queryResults": []}
    previousQuery = ""
    formData = {"rawQuery": ""}

    if request.method == "POST":
        try:
            formData = getUserRawQuery(request)
            if not formData:
                context = {"form": form, "errorMessage": "Please enter a query."}
                return render(request, "dashboard/pages/customquery.html", context)

            queryResults = getRawQueryResults(formData)
            context = {
                "queryResults": [
                    {key: value for key, value in zip(queryResults[0].keys(), row)}
                    for row in queryResults
                ],
                "form": form,
                "rawQuery": formData.get("rawQuery"),
            }

            return renderRawQueryPage(
                request, context, formData.get("rawQuery"), queryResults=queryResults
            )

        except Exception as e:
            errorMessage = str(e)
            context = {
                "form": RawQueryForm(initial={"rawQuery": formData.get("rawQuery")}),
                "errorMessage": errorMessage,
            }
            context.update(formData)
            return renderRawQueryPage(
                request,
                context,
                formData.get("rawQuery"),
                errorMessage=errorMessage,
                fromExcept=True,
            )

    else:
        previousQuery = request.GET.get("query", "")
        form = RawQueryForm(initial={"rawQuery": previousQuery})
        return renderRawQueryPage(request, context, formData.get("rawQuery"))
