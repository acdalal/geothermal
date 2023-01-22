import csv

from django.shortcuts import render
from django.http import HttpResponse

from .helper.api import getTempVsDepthResults, getTempVsTimeResults, getDataOutages
from .helper.processUserForms import (
    getUserTempsVsTimeQuery,
    getUserTempVsDepthQuery,
    getUserQueryType,
)
from .helper.constants import DATA_START_DATE, DATA_END_DATE
from .helper.renderFunctions import (
    renderIndexPage,
    renderTempVsDepthPage,
    renderTempVsTimePage,
)


def index(request):
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


def about(request):
    return render(request, "dashboard/about.html", context=None)


def documentation(request):
    return render(request, "dashboard/documentation.html", context=None)


def tempVsTimeDownload(request):
    if request.method == "POST":
        formData = getUserTempsVsTimeQuery(request)
        queryResults = getTempVsTimeResults(
            formData["boreholeNumber"],
            formData["depth"],
            formData["startDateUtc"],
            formData["endDateUtc"],
        )

        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="tempVsTimeDownload.csv"'
            },
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "channel_id",
                "measurement_id",
                "datetime_utc",
                "data_id",
                "temperature_c",
                "depth_m",
            ]
        )
        for dictionary in queryResults:
            writer.writerow(dictionary.values())

        return response

    else:
        return False


def tempVsTime(request):
    if request.method == "POST":
        formData = getUserTempsVsTimeQuery(request)
        queryResults = getTempVsTimeResults(
            formData["boreholeNumber"],
            formData["depth"],
            formData["startDateUtc"],
            formData["endDateUtc"],
        )
        if formData["download"]:
            response = HttpResponse(
                content_type="text/csv",
                headers={
                    "Content-Disposition": 'attachment; filename="tempVsTimeDownload.csv"'
                },
            )

            writer = csv.writer(response)
            writer.writerow(
                [
                    "channel_id",
                    "measurement_id",
                    "datetime_utc",
                    "data_id",
                    "temperature_c",
                    "depth_m",
                ]
            )
            for dictionary in queryResults:
                writer.writerow(dictionary.values())

            return response

        borehole = int(formData["boreholeNumber"])
        return renderTempVsTimePage(request, queryResults, borehole)

    else:
        return renderTempVsTimePage(request)


def tempVsDepth(request):
    if request.method == "POST":
        formData = getUserTempVsDepthQuery(request)
        queryResults = getTempVsDepthResults(
            formData["boreholeNumber"], formData["timestampUtc"]
        )
        if formData["download"]:
            response = HttpResponse(
                content_type="text/csv",
                headers={
                    "Content-Disposition": 'attachment; filename="tempVsTimeDownload.csv"'
                },
            )

            writer = csv.writer(response)
            writer.writerow(
                [
                    "channel_id",
                    "measurement_id",
                    "datetime_utc",
                    "data_id",
                    "temperature_c",
                    "depth_m",
                ]
            )
            for dictionary in queryResults:
                writer.writerow(dictionary.values())

            return response
        borehole = int(formData["boreholeNumber"])
        return renderTempVsDepthPage(request, queryResults, borehole)

    else:
        return renderTempVsDepthPage(request)


def tempVsDepthDownload(request):
    if request.method == "POST":
        formData = getUserTempVsDepthQuery(request)
        queryResults = getTempVsDepthResults(
            formData["boreholeNumber"], formData["timestampUtc"]
        )
        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="tempVsDepthDownload.csv"'
            },
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "channel_id",
                "measurement_id",
                "datetime_utc",
                "data_id",
                "temperature_c",
                "depth_m",
            ]
        )
        for dictionary in queryResults:
            writer.writerow(dictionary.values())

        return response

    else:
        return renderTempVsDepthPage(request)
