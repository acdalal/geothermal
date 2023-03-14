import csv

from django.shortcuts import render
from django.http import HttpRequest

from .helper.api import (
    # getTempVsDepthResults,
    getTempVsTimeResults,
    getTempProfileResults,
    getDataOutages,
    getRawQueryResults,
)
from .helper.processUserForms import (
    getUserTempVsTimeQuery,
    # getUserTempVsDepthQuery,
    getGrouping,
    getUserRawQuery,
    getUserTempProfileQuery,
)
from .helper.renderFunctions import (
    renderIndexPage,
    # renderTempVsDepthPage,
    renderTempVsTimePage,
    renderTempProfilePage,
    renderRawQueryPage,
)
from .helper.logging import (
    log_query_as_INFO,
    get_user_ip_address,
)
from .forms import RawQueryForm


def index(request: HttpRequest):
    if request.method == "POST":
        # execute temp profile query, log the query, and render the temp
        # profile page with the results
        if "temperature-profile" in request.POST:
            formData = getUserTempProfileQuery(request)
            groupBy = getGrouping(formData["startDateUtc"], formData["endDateUtc"])
            borehole = formData["boreholeNumber"]
            queryResults, queryStats = getTempProfileResults(
                borehole,
                formData["startDateUtc"],
                formData["endDateUtc"],
                formData["dailyTimestamp"],
                groupBy,
                formData["units"],
            )
            log_query_as_INFO(
                get_user_ip_address(request),
                queryStats["query"],
                queryStats["executionTime"],
                queryStats["totalRecords"],
            )
            return renderTempProfilePage(
                request, formData["units"], groupBy, queryResults, int(borehole)
            )

        # execute temp vs. time query, log the query, and render the
        # temp vs. time page with the results
        elif "temperature-time" in request.POST:
            formData = getUserTempVsTimeQuery(request)
            borehole = formData["boreholeNumber"]
            queryResults, queryStats = getTempVsTimeResults(
                borehole,
                formData["depth"],
                formData["startDateUtc"],
                formData["endDateUtc"],
                formData["units"],
            )
            log_query_as_INFO(
                get_user_ip_address(request),
                queryStats["query"],
                queryStats["executionTime"],
                queryStats["totalRecords"],
            )
            return renderTempVsTimePage(
                request, formData["units"], queryResults, int(borehole)
            )

        # execute temp vs. depth query, log the query, and render the
        # temp vs. depth page with the results
        # if "temperature-depth" in request.POST:
        #     formData = getUserTempVsDepthQuery(request)
        #     borehole = formData["boreholeNumber"]
        #     queryResults, queryStats = getTempVsDepthResults(
        #         borehole, formData["timestampUtc"], formData["units"]
        #     )
        #     log_query_as_INFO(
        #         get_user_ip_address(request),
        #         queryStats["query"],
        #         queryStats["executionTime"],
        #         queryStats["totalRecords"],
        #     )
        #     return renderTempVsDepthPage(
        #         request, formData["units"], queryResults, int(borehole)
        #     )

    # if the request was not POST, but rather GET, render the index page
    else:
        return renderIndexPage(request)


def about(request: HttpRequest):
    return render(request, "dashboard/pages/about.html", context=None)


def documentation(request: HttpRequest):
    """Renders the documentation page template with the most recent data outages"""
    outageData = getDataOutages()
    outageDict = {"outage": outageData}
    return render(request, "dashboard/pages/documentation.html", context=outageDict)


def customQuery(request: HttpRequest):
    form = RawQueryForm(request.POST or None)
    context = {"form": form, "queryResults": []}
    previousQuery = ""
    formData = {"rawQuery": ""}

    if request.method == "POST":
        # try to execute the query and return the raw query page with the
        # results if successful
        try:
            formData = getUserRawQuery(request)

            # check if the user submitted a blank form
            if not formData:
                context = {"form": form, "errorMessage": "Please enter a query."}
                return render(request, "dashboard/pages/customquery.html", context)

            # log the query
            queryResults, queryStats = getRawQueryResults(formData)
            log_query_as_INFO(
                get_user_ip_address(request),
                queryStats["query"],
                queryStats["executionTime"],
                queryStats["totalRecords"],
            )

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

        # throw an exception and render it on the raw query page
        # if the query was not successfully executed
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

    # if the request is a GET, render the raw query page
    else:
        previousQuery = request.GET.get("query", "")
        form = RawQueryForm(initial={"rawQuery": previousQuery})
        return renderRawQueryPage(request, context, formData.get("rawQuery"))
