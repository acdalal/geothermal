from django.shortcuts import render
import csv
from django.http import HttpResponse, HttpResponseRedirect

from .forms import (
    TempVsTimeForm,
    TempVsTimeDownloadForm,
    TempVsDepthForm,
    QuerySelectionForm,
)
from .api import getTempVsDepthResults, getTempVsTimeResults, getDataOutages

from .constants import DATA_START_DATE, DATA_END_DATE

from .viewshelpers import (
    _getQuerySelectionData,
    _getTempVsTimeFormData,
    _getTempVsDepthFormData,
    _convertToTempVsTimeGraphData,
    _convertToTempVsDepthData,
    _truncateDateTime,
)


def index(request):
    if request.method == "POST":
        userForm = QuerySelectionForm(request.POST)
        if userForm.is_valid():
            formData = _getQuerySelectionData(userForm.cleaned_data)
            queryType = formData["queryType"]
            return HttpResponseRedirect(
                "dashboard/{queryPath}/".format(queryPath=queryType),
            )

        # return back to same page in the case of invalid form data
        else:
            return render(
                request, "dashboard/index.html", context={"form": QuerySelectionForm()}
            )

    else:
        return render(
            request, "dashboard/index.html", context={"form": QuerySelectionForm()}
        )


def about(request):
    return render(request, "dashboard/about.html", context=None)


def documentation(request):
    return render(request, "dashboard/documentation.html", context=None)


def tempVsTime(request):
    if request.method == "POST":
        userForm = TempVsTimeForm(request.POST)
        if userForm.is_valid():
            formData = _getTempVsTimeFormData(userForm.cleaned_data)
            queryResults = getTempVsTimeResults(
                formData["boreholeNumber"],
                formData["depth"],
                formData["startDateUtc"],
                formData["endDateUtc"],
            )

            borehole = int(formData["boreholeNumber"])
            graphData = _convertToTempVsTimeGraphData(queryResults, borehole)

            return render(
                request,
                "dashboard/tempvstime.html",
                context={
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
                "dashboard/tempvstime.html",
                {
                    "queryData": "error",
                    "dataStartDate": DATA_START_DATE,
                    "dataEndDate": DATA_END_DATE,
                },
            )

    else:
        outageList = getDataOutages()
        truncatedOutageList = _truncateDateTime(outageList)
        return render(
            request,
            "dashboard/tempvstime.html",
            context={
                "form": TempVsTimeForm(),
                "dataStartDate": DATA_START_DATE,
                "dataEndDate": DATA_END_DATE,
                "outageList": truncatedOutageList,
            },
        )


def tempVsTimeDownload(request):
    if request.method == "POST":
        userForm = TempVsTimeDownloadForm(request.POST)
        if userForm.is_valid():
            formData = _getTempVsTimeFormData(userForm.cleaned_data)
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
            formData = _getTempVsDepthFormData(userForm.cleaned_data)

            queryResults = getTempVsDepthResults(
                formData["boreholeNumber"], formData["timestampUtc"]
            )

            graphData = _convertToTempVsDepthData(
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
            formData = _getTempVsDepthFormData(userForm.cleaned_data)

            queryResults = getTempVsDepthResults(
                formData["boreholeNumber"], formData["timestampUtc"]
            )

            graphData = _convertToTempVsDepthData(
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
