import csv

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import (
    TempVsTimeForm,
    TempVsTimeDownloadForm,
    TempVsDepthForm,
    QuerySelectionForm,
)
from .api import getTempVsDepthResults, getTempVsTimeResults, getDataOutages
from .processUserForms import (
    getQuerySelectionData,
    getTempVsDepthFormData,
    getTempVsTimeFormData,
)
from .visualization import convertToTempVsDepthGraphData, convertToTempVsTimeGraphData
from .constants import DATA_START_DATE, DATA_END_DATE


def _truncateDateTime(dates):
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
    return render(
        request,
        "dashboard/tempvstime.html",
        context={
            "form": TempVsTimeForm(),
            "queryData": queryResults,
            "graphData": graphData,
            "dataStartDate": DATA_START_DATE,
            "dataEndDate": DATA_END_DATE,
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
    truncated_outageList = _truncateDateTime(outageList)
    return render(
        request,
        "dashboard/tempvstime.html",
        context={
            "form": TempVsDepthForm(),
            "queryData": queryResults,
            "graphData": graphData,
            "dataStartDate": DATA_START_DATE,
            "dataEndDate": DATA_END_DATE,
            "outageList": truncated_outageList,
        },
    )


def getUserQueryType(request) -> str:
    """
    From the front-page query selection form, extracts the user response
    """
    userForm = QuerySelectionForm(request.POST)
    assert userForm.is_valid()

    formData = getQuerySelectionData(userForm.cleaned_data)
    queryType = formData["queryType"]
    return queryType


def getUserTempsVsTimeQuery(request) -> dict:
    """
    From the temperature vs time form, extracts the user response and formats it into a dictionary
    """
    userForm = TempVsTimeForm(request.POST)
    assert userForm.is_valid()
    formData = getTempVsTimeFormData(userForm.cleaned_data)

    return formData


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


def tempVsTime(request):
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


def tempVsTimeDownload(request):
    if request.method == "POST":
        userForm = TempVsTimeDownloadForm(request.POST)
        if userForm.is_valid():
            print("hiii")
            formData = getTempVsTimeFormData(userForm.cleaned_data)
            print(formData)
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

        # return back to same page in the case of invalid form data
        else:
            return render(
                request, "dashboard/tempvstime.html", context={"form": TempVsTimeForm()}
            )

    else:
        return render(
            request, "dashboard/tempvstime.html", context={"form": TempVsTimeForm()}
        )


def tempVsDepth(request):
    if request.method == "POST":
        userForm = TempVsDepthForm(request.POST)
        if userForm.is_valid():
            formData = getTempVsDepthFormData(userForm.cleaned_data)

            queryResults = getTempVsDepthResults(
                formData["boreholeNumber"], formData["timestampUtc"]
            )

            graphData = convertToTempVsDepthGraphData(
                queryResults, formData["boreholeNumber"]
            )
            return render(
                request,
                "dashboard/tempvsdepth.html",
                {
                    "queryData": queryResults,
                    "graphData": graphData,
                    "dataStartDate": DATA_START_DATE,
                    "dataEndDate": DATA_END_DATE,
                },
            )
        else:
            print(userForm.errors)
            return render(
                request,
                "dashboard/tempvsdepth.html",
                {
                    "queryData": "error",
                    "form": TempVsDepthForm(),
                    "dataStartDate": DATA_START_DATE,
                    "dataEndDate": DATA_END_DATE,
                },
            )

    else:
        outageList = getDataOutages()
        truncatedOutageList = _truncateDateTime(outageList)
        return render(
            request,
            "dashboard/tempvsdepth.html",
            {
                "form": TempVsDepthForm(),
                "dataStartDate": DATA_START_DATE,
                "dataEndDate": DATA_END_DATE,
                "outageList": truncatedOutageList,
            },
        )


def tempVsDepthDownload(request):
    if request.method == "POST":
        userForm = TempVsDepthForm(request.POST)
        if userForm.is_valid():
            formData = getTempVsDepthFormData(userForm.cleaned_data)

            queryResults = getTempVsDepthResults(
                formData["boreholeNumber"], formData["timestampUtc"]
            )

            graphData = convertToTempVsDepthGraphData(
                queryResults, formData["boreholeNumber"]
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

        # return back to same page in the case of invalid form data
        else:
            return render(
                request,
                "dashboard/tempvsdepth.html",
                context={"form": TempVsDepthForm()},
            )

    else:
        return render(
            request, "dashboard/tempvstime.html", context={"form": TempVsDepthForm()}
        )


def _getQuerySelectionData(cleanedData: dict) -> dict:
    queryType = cleanedData["queryType"]
    return {"queryType": queryType}
